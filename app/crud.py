from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime
import logging

from app.models import User, Stock, Portfolio, Transaction, TransactionType
from app.schemas import PortfolioItemResponse, PortfolioResponse

logger = logging.getLogger(__name__)


def get_stock_by_symbol(db: Session, symbol: str) -> Optional[Stock]:
    return db.query(Stock).filter(Stock.symbol == symbol.upper()).first()


def get_portfolio_item(db: Session, user_id: int, stock_id: int) -> Optional[Portfolio]:
    return db.query(Portfolio).filter(
        Portfolio.user_id == user_id,
        Portfolio.stock_id == stock_id
    ).first()


def update_portfolio_after_buy(
    db: Session,
    user_id: int,
    stock_id: int,
    quantity: float,
    price_per_share: float
) -> Portfolio:
    portfolio_item = get_portfolio_item(db, user_id, stock_id)

    if portfolio_item:
        total_cost = portfolio_item.quantity * portfolio_item.average_buy_price + quantity * price_per_share
        new_quantity = portfolio_item.quantity + quantity
        portfolio_item.average_buy_price = total_cost / new_quantity
        portfolio_item.quantity = new_quantity
    else:
        portfolio_item = Portfolio(
            user_id=user_id,
            stock_id=stock_id,
            quantity=quantity,
            average_buy_price=price_per_share
        )
        db.add(portfolio_item)

    db.flush()
    return portfolio_item


def update_portfolio_after_sell(
    db: Session,
    user_id: int,
    stock_id: int,
    quantity: float
) -> Portfolio:
    portfolio_item = get_portfolio_item(db, user_id, stock_id)

    if not portfolio_item or portfolio_item.quantity < quantity:
        raise ValueError(f"Not enough shares. Available: {portfolio_item.quantity if portfolio_item else 0}")

    portfolio_item.quantity -= quantity

    if portfolio_item.quantity == 0:
        db.delete(portfolio_item)

    db.flush()
    return portfolio_item


def purchase_stock(
    db: Session,
    user_id: int,
    stock_symbol: str,
    quantity: float
) -> Transaction:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    stock = get_stock_by_symbol(db, stock_symbol)
    if not stock:
        raise ValueError(f"Stock {stock_symbol} not found")
    
    stock.last_updated = datetime.utcnow()

    total_amount = quantity * stock.current_price

    if user.balance < total_amount:
        raise ValueError(f"Insufficient funds. Need ${total_amount:.2f}, available ${user.balance:.2f}")

    try:
        user.balance -= total_amount
        update_portfolio_after_buy(db, user_id, stock.id, quantity, stock.current_price)

        transaction = Transaction(
            user_id=user_id,
            stock_id=stock.id,
            type=TransactionType.BUY,
            quantity=quantity,
            price_per_share=stock.current_price,
            total_amount=total_amount
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Transaction failed: {str(e)}")


def sell_stock(
    db: Session,
    user_id: int,
    stock_symbol: str,
    quantity: float
) -> Transaction:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    stock = get_stock_by_symbol(db, stock_symbol)
    if not stock:
        raise ValueError(f"Stock {stock_symbol} not found")
    
    stock.last_updated = datetime.utcnow()

    portfolio_item = get_portfolio_item(db, user_id, stock.id)
    if not portfolio_item or portfolio_item.quantity < quantity:
        available = portfolio_item.quantity if portfolio_item else 0
        raise ValueError(f"Not enough shares. Available: {available}")

    total_amount = quantity * stock.current_price

    try:
        user.balance += total_amount
        update_portfolio_after_sell(db, user_id, stock.id, quantity)

        transaction = Transaction(
            user_id=user_id,
            stock_id=stock.id,
            type=TransactionType.SELL,
            quantity=quantity,
            price_per_share=stock.current_price,
            total_amount=total_amount
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Transaction failed: {str(e)}")


def get_portfolio_summary(db: Session, user_id: int) -> PortfolioResponse:
    portfolio_items = db.query(Portfolio).options(
        joinedload(Portfolio.stock)
    ).filter(Portfolio.user_id == user_id).all()
    
    items_response = []
    total_value = 0.0
    total_cost = 0.0
    
    for item in portfolio_items:
        stock = item.stock
        current_price = float(stock.current_price)
        quantity = float(item.quantity)
        avg_price = float(item.average_buy_price)
        
        current_value = quantity * current_price
        cost_basis = quantity * avg_price
        profit_loss = current_value - cost_basis
        profit_loss_percent = (profit_loss / cost_basis * 100) if cost_basis > 0 else 0
        
        items_response.append(PortfolioItemResponse(
            stock_symbol=stock.symbol,
            stock_name=stock.name,
            quantity=quantity,
            average_buy_price=avg_price,
            current_price=current_price,
            total_value=current_value,
            profit_loss=profit_loss,
            profit_loss_percent=profit_loss_percent
        ))
        
        total_value += current_value
        total_cost += cost_basis
    
    total_profit_loss = total_value - total_cost
    
    return PortfolioResponse(
        items=items_response,
        total_value=total_value,
        total_profit_loss=total_profit_loss
    )


def get_transaction_history(
    db: Session,
    user_id: int,
    limit: int = 50,
    offset: int = 0
) -> List[dict]:
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(Transaction.created_at.desc()).offset(offset).limit(limit).all()

    result = []
    for t in transactions:
        result.append({
            "id": t.id,
            "stock_symbol": t.stock.symbol,
            "stock_name": t.stock.name,
            "type": t.type.value,
            "quantity": float(t.quantity),
            "price_per_share": float(t.price_per_share),
            "total_amount": float(t.total_amount),
            "created_at": t.created_at
        })

    return result