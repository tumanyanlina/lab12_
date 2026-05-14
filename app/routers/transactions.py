from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import TransactionCreate, TransactionResponse
from app.auth import get_current_user
from app.models import User
from app.crud import purchase_stock, sell_stock, get_transaction_history

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/buy", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def buy_stock(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if transaction_data.type != "BUY":
        raise HTTPException(status_code=400, detail="Invalid transaction type. Use 'BUY'")

    try:
        transaction = purchase_stock(
            db=db,
            user_id=current_user.id,
            stock_symbol=transaction_data.stock_symbol,
            quantity=transaction_data.quantity
        )
        return {
            "id": transaction.id,
            "stock_symbol": transaction.stock.symbol,
            "stock_name": transaction.stock.name,
            "type": transaction.type.value,
            "quantity": transaction.quantity,
            "price_per_share": transaction.price_per_share,
            "total_amount": transaction.total_amount,
            "created_at": transaction.created_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sell", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def sell_stock(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if transaction_data.type != "SELL":
        raise HTTPException(status_code=400, detail="Invalid transaction type. Use 'SELL'")

    try:
        transaction = sell_stock(
            db=db,
            user_id=current_user.id,
            stock_symbol=transaction_data.stock_symbol,
            quantity=transaction_data.quantity
        )
        return {
            "id": transaction.id,
            "stock_symbol": transaction.stock.symbol,
            "stock_name": transaction.stock.name,
            "type": transaction.type.value,
            "quantity": transaction.quantity,
            "price_per_share": transaction.price_per_share,
            "total_amount": transaction.total_amount,
            "created_at": transaction.created_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_transaction_history(db, current_user.id, limit, offset)