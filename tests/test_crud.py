import pytest
from app.crud import (
    get_stock_by_symbol,
    purchase_stock,
    sell_stock,
    get_portfolio_summary,
    get_transaction_history
)


def test_get_stock_by_symbol_success(db, test_stock):
    stock = get_stock_by_symbol(db, "TEST")
    assert stock is not None
    assert stock.symbol == "TEST"


def test_get_stock_by_symbol_not_found(db):
    stock = get_stock_by_symbol(db, "NONEXISTENT")
    assert stock is None


def test_purchase_stock_success(db, test_user, test_stock):
    initial_balance = test_user.balance
    transaction = purchase_stock(db, test_user.id, "TEST", 5)
    
    assert transaction is not None
    assert transaction.type.value == "BUY"
    assert transaction.quantity == 5
    assert transaction.total_amount == 500.00
    
    db.refresh(test_user)
    assert test_user.balance == initial_balance - 500.00


def test_purchase_stock_insufficient_funds(db, test_user, test_stock):
    with pytest.raises(ValueError, match="Insufficient funds"):
        purchase_stock(db, test_user.id, "TEST", 2000)


def test_purchase_stock_not_found(db, test_user):
    with pytest.raises(ValueError, match="Stock NOTFOUND not found"):
        purchase_stock(db, test_user.id, "NOTFOUND", 5)


def test_purchase_stock_negative_quantity(db, test_user, test_stock):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        purchase_stock(db, test_user.id, "TEST", -5)


def test_sell_stock_success(db, test_user, test_stock):
    purchase_stock(db, test_user.id, "TEST", 10)
    initial_balance = test_user.balance
    
    transaction = sell_stock(db, test_user.id, "TEST", 3)
    
    assert transaction is not None
    assert transaction.type.value == "SELL"
    assert transaction.quantity == 3
    assert transaction.total_amount == 300.00
    
    db.refresh(test_user)
    assert test_user.balance == initial_balance + 300.00


def test_sell_more_than_owned(db, test_user, test_stock):
    purchase_stock(db, test_user.id, "TEST", 5)
    
    with pytest.raises(ValueError, match="Not enough shares"):
        sell_stock(db, test_user.id, "TEST", 10)


def test_sell_stock_negative_quantity(db, test_user, test_stock):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        sell_stock(db, test_user.id, "TEST", -3)


def test_get_portfolio_summary(db, test_user, test_stock):
    purchase_stock(db, test_user.id, "TEST", 10)
    
    portfolio = get_portfolio_summary(db, test_user.id)
    assert portfolio.total_value == 1000.00
    assert len(portfolio.items) == 1
    assert portfolio.items[0].stock_symbol == "TEST"
    assert portfolio.items[0].quantity == 10


def test_get_transaction_history(db, test_user, test_stock):
    purchase_stock(db, test_user.id, "TEST", 5)
    purchase_stock(db, test_user.id, "TEST", 3)
    sell_stock(db, test_user.id, "TEST", 2)
    
    history = get_transaction_history(db, test_user.id, limit=10)
    assert len(history) >= 3
    assert history[0]["stock_symbol"] == "TEST"