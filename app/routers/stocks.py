from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Stock, User
from app.schemas import StockResponse
from app.auth import get_current_user

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("/", response_model=List[StockResponse])
def get_all_stocks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stocks = db.query(Stock).all()
    return stocks


@router.get("/{symbol}", response_model=StockResponse)
def get_stock_by_symbol(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stock = db.query(Stock).filter(Stock.symbol == symbol.upper()).first()
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Stock {symbol} not found")
    return stock