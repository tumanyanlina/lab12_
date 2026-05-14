Prompt Log — Лабораторная работа №12
Вариант 27: Онлайн-торговля акциями

Студент: Туманян Лина Врежовна  
Группа: 220032-11  
Модель ИИ: Claude/GPT-4/DeepSeek


Задание 1: Создание полноценного веб-приложения

Промпт №1.1 (инициализация проекта)

Дата: 2026-05-14
Цель: Создать структуру проекта и начальные файлы

Промпт: Помоги создать структуру проекта для лабораторной работы №12 (вариант 27 - онлайн-торговля акциями).
Нужно:

1. Создать папку lab12-trading
2. Инициализировать git репозиторий
3. Создать файлы: .gitignore (для Python проекта), README.md (с ФИО, группой, вариантом, списком заданий), prompt_log.md (для записи всех промптов), requirements.txt (с базовыми зависимостями: fastapi, uvicorn, sqlalchemy, pytest и др.).
4. Создать папку app и пустой app/init.py
5. Сделать первый коммит с сообщением "chore: init project structure for lab12 trading app"

Результат: Выполнен первый коммит, создана базовая структура проекта.

.gitignore:

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite
*.sqlite3

# Environment
.env
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Docker
*.log
*.pid

# OS
.DS_Store
Thumbs.db

README.md:

Лабораторная работа №12
AI-ассистированная разработка

Студент: Туманян Лина Врежовна  
Группа: 220032-11  
Вариант: 27 (Платформа для онлайн-торговли акциями)  
Уровень сложности: Повышенный

Выполненные задания:
- Задание 1 — Полноценное веб-приложение
- Задание 2 — Code review сгенерированного кода
- Задание 4 — Интеграция ИИ в CI/CD
- Задание 7 — Генерация unit-тестов с покрытием ≥90%

requirements.txt:

fastapi==0.115.11
uvicorn[standard]==0.34.0
sqlalchemy==2.0.36
alembic==1.14.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.20
pydantic==2.10.4
pydantic-settings==2.7.0
email-validator==2.2.0
httpx==0.28.1
pytest==8.3.4
pytest-cov==6.0.0
python-dotenv==1.0.1

Промпт №1.2 (конфигурация базы данных)

Дата: 2026-05-14
Цель: Настроить подключение к базе данных SQLAlchemy с поддержкой SQLite (для разработки) и PostgreSQL (для продакшена), создать dependency-функцию get_db() для внедрения сессий в эндпоинты FastAP

Промпт: Ты — senior Python разработчик. Создай файл app/database.py для FastAPI приложения.

Требования:
1. Настройка SQLAlchemy с поддержкой SQLite (для разработки)
2. Функция get_db() для получения сессии БД (dependency injection)
3. Использование python-dotenv для переменных окружения
4. Поддержка PostgreSQL через DATABASE_URL (можно переключить)
5. Type hints, docstrings

Результат: Создан файл database.py со всеми требованиями.

database.py:

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trading.db")

connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency-функция для получения сессии базы данных.
    Используется в эндпоинтах FastAPI.

    Пример:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()

    Yields:
        Session: Сессия SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Промпт №1.3 (модели базы данных)

Дата: 2026-05-14
Цель: Создать SQLAlchemy модели для онлайн-торговли акциями: User, Stock, Portfolio, Transaction со связями один-ко-многим и валидацией полей.

Промпт: Создай файл app/models.py для торговой платформы.

Модели (4 сущности):
1. User: id, email(unique), username(unique), hashed_password, balance(default=100000), created_at
2. Stock: id, symbol(unique), name, current_price, last_updated
3. Portfolio: id, user_id(foreign), stock_id(foreign), quantity, average_buy_price
4. Transaction: id, user_id(foreign), stock_id(foreign), type(BUY/SELL), quantity, price_per_share, total_amount, created_at

Требования:
1. Все связи через relationship
2. Уникальные индексы на email, username, symbol
3. Тип TransactionType использовать Enum
4. Обратные связи для каскадного удаления
5. Чистый код, без лишних комментариев

Результат: Создан файл models.py со всеми требованиями.

models.py:

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
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
    balance = Column(Float, default=100000.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    current_price = Column(Float, nullable=False, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    portfolio_items = relationship("Portfolio", back_populates="stock")
    transactions = relationship("Transaction", back_populates="stock")


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)
    average_buy_price = Column(Float, nullable=False, default=0.0)

    user = relationship("User", back_populates="portfolio")
    stock = relationship("Stock", back_populates="portfolio_items")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Float, nullable=False)
    price_per_share = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
    stock = relationship("Stock", back_populates="transactions")

Промпт №1.4 (Pydantic схемы)

Дата: 2026-05-14
Цель: Создать Pydantic схемы для валидации данных и сериализации ответов API.

Промпт: Создай файл app/schemas.py для торговой платформы.

Схемы:
1. Auth: UserCreate, UserLogin, UserResponse, Token
2. Stock: StockCreate, StockResponse
3. Transaction: TransactionCreate (stock_symbol, type, quantity), TransactionResponse (включает stock_symbol, stock_name)
4. Portfolio: PortfolioItemResponse (stock_symbol, stock_name, quantity, average_buy_price, current_price, total_value, profit_loss, profit_loss_percent), PortfolioResponse (items, total_value, total_profit_loss)

Требования:
1. Валидация: email, username (min_length=3, max_length=50), password (min_length=6)
2. Stock символ: только заглавные буквы, максимум 5 символов (regex: ^[A-Z]{1,5}$)
3. Quantity: положительное число (gt=0)
4. Все response модели с Config from_attributes = True
5. Чистый код, без лишних комментариев

Результат: Создан файл schemas.py со всеми требованиями.

schemas.py:

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