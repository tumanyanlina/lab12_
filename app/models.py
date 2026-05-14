from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class TransactionType(str, enum.Enum):
    BUY = "BUY"
    SELL = "SELL"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Numeric(20, 2), default=100000.00)
    created_at = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    current_price = Column(Numeric(20, 2), nullable=False, default=0.00)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    portfolio_items = relationship("Portfolio", back_populates="stock")
    transactions = relationship("Transaction", back_populates="stock")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    quantity = Column(Numeric(20, 2), nullable=False, default=0.00)
    average_buy_price = Column(Numeric(20, 2), nullable=False, default=0.00)

    user = relationship("User", back_populates="portfolio")
    stock = relationship("Stock", back_populates="portfolio_items")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Numeric(20, 2), nullable=False)
    price_per_share = Column(Numeric(20, 2), nullable=False)
    total_amount = Column(Numeric(20, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    stock = relationship("Stock", back_populates="transactions")