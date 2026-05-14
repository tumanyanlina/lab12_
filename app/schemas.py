from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import List, Optional
from enum import Enum


class TransactionTypeEnum(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


# Auth schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Stock schemas
class StockCreate(BaseModel):
    symbol: str = Field(..., pattern=r'^[A-Z]{1,5}$')
    name: str
    current_price: float = Field(..., gt=0)


class StockResponse(BaseModel):
    id: int
    symbol: str
    name: str
    current_price: float
    last_updated: datetime

    class Config:
        from_attributes = True


# Transaction schemas
class TransactionCreate(BaseModel):
    stock_symbol: str = Field(..., pattern=r'^[A-Z]{1,5}$')
    type: TransactionTypeEnum
    quantity: float = Field(..., gt=0)

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class TransactionResponse(BaseModel):
    id: int
    stock_symbol: str
    stock_name: str
    type: TransactionTypeEnum
    quantity: float
    price_per_share: float
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True


# Portfolio schemas
class PortfolioItemResponse(BaseModel):
    stock_symbol: str
    stock_name: str
    quantity: float
    average_buy_price: float
    current_price: float
    total_value: float
    profit_loss: float
    profit_loss_percent: float


class PortfolioResponse(BaseModel):
    items: List[PortfolioItemResponse]
    total_value: float
    total_profit_loss: float