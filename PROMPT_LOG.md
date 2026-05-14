Prompt Log — Лабораторная работа №12
Вариант 27: Онлайн-торговля акциями

Студент: Туманян Лина Врежовна  
Группа: 220032-11  
Модель ИИ: Claude/GPT-4/DeepSeek


Задание 1: Создание полноценного веб-приложения

Промпт №1.1 (инициализация проекта)

Дата: 2026-05-14
Цель: Создать структуру проекта и начальные файлы
Инструмент: DeepSeek

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
Инструмент: DeepSeek

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
Инструмент: DeepSeek

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
Инструмент: DeepSeek

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

Промпт №1.5 (JWT аутентификация)

Дата: 2026-05-14
Цель: Реализовать JWT аутентификацию: хеширование паролей, создание и проверка токенов, зависимость для получения текущего пользователя.
Инструмент: DeepSeek

Промпт: Создай файл app/auth.py для торговой платформы.

Функции и классы:
1. verify_password(plain_password, hashed_password)
2. get_password_hash(password)
3. authenticate_user(db, username, password)
4. create_access_token(data, expires_delta)
5. get_current_user(credentials: HTTPAuthorizationCredentials, db) — через JWT токен

Требования:
1. Использовать python-jose[cryptography] для JWT
2. Использовать passlib[bcrypt] для хеширования
3. Секретный ключ из переменной окружения SECRET_KEY
4. Время жизни токена из ACCESS_TOKEN_EXPIRE_MINUTES
5. Обработка ошибок: если токен невалидный или пользователь не найден -> HTTPException 401
6. Чистый код, type hints, без лишних комментариев

Результат: Создан файл auth.py со всеми требованиями.

auth.py:
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from app.database import get_db
from app.models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

Промпт №1.6 (бизнес-логика)

Дата: 2026-05-14
Цель: Реализовать бизнес-логику покупки/продажи акций, обновления портфеля и расчёта прибыли/убытка.
Инструмент: DeepSeek

Промпт: Создай файл app/crud.py для торговой платформы.

Функции:
1. get_stock_by_symbol(db, symbol) — получить акцию по тикеру
2. purchase_stock(db, user_id, stock_symbol, quantity) — покупка акций
3. sell_stock(db, user_id, stock_symbol, quantity) — продажа акций
4. get_portfolio_summary(db, user_id) — текущий портфель с расчётом P&L
5. get_transaction_history(db, user_id, limit, offset) — история сделок

Требования:
1. При покупке: проверить достаточно ли средств, списать деньги, обновить портфель (средневзвешенную цену)
2. При продаже: проверить достаточно ли акций, зачислить деньги, уменьшить количество в портфеле
3. Все операции в одной транзакции БД
4. Обработка ошибок через raise ValueError
5. Чистый код, type hints, без лишних комментариев

Результат: Создан файл crud.py со всеми требованиями.

crud.py:

from sqlalchemy.orm import Session
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
    portfolio_items = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    items_response = []
    total_value = 0.0
    total_cost = 0.0

    for item in portfolio_items:
        stock = item.stock
        current_price = stock.current_price
        current_value = item.quantity * current_price
        cost_basis = item.quantity * item.average_buy_price
        profit_loss = current_value - cost_basis
        profit_loss_percent = (profit_loss / cost_basis * 100) if cost_basis > 0 else 0

        items_response.append(PortfolioItemResponse(
            stock_symbol=stock.symbol,
            stock_name=stock.name,
            quantity=item.quantity,
            average_buy_price=item.average_buy_price,
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
            "quantity": t.quantity,
            "price_per_share": t.price_per_share,
            "total_amount": t.total_amount,
            "created_at": t.created_at
        })

    return result

Промпт №1.7 (роутеры API)

Дата: 2026-05-14
Цель: Создать API эндпоинты для аутентификации, работы с акциями, портфелем и транзакциями.
Инструмент: DeepSeek

Промпт: Создай 4 файла роутеров в папке app/routers/:

1. auth.py: POST /auth/register (UserCreate -> UserResponse), POST /auth/login (UserLogin -> Token)
2. stocks.py: GET /stocks (список всех акций), GET /stocks/{symbol} (одна акция)
3. portfolio.py: GET /portfolio (портфель текущего пользователя)
4. transactions.py: POST /transactions/buy (TransactionCreate -> TransactionResponse), POST /transactions/sell (TransactionCreate -> TransactionResponse), GET /transactions (история с пагинацией)

Требования:
1. Все эндпоинты кроме register/login требуют get_current_user
2. Использовать HTTPException с правильными статусами
3. Чистый код, type hints, docstrings

Результат: Созданы все 4 файла с нужными требованиями.

app/routers/auth.py:

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas import UserCreate, UserLogin, Token, UserResponse
from app.models import User
from app.auth import get_password_hash, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        balance=100000.0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

app/routers/stocks.py:

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

app/routers/portfolio.py:

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PortfolioResponse
from app.auth import get_current_user
from app.models import User
from app.crud import get_portfolio_summary

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/", response_model=PortfolioResponse)
def get_portfolio(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_portfolio_summary(db, current_user.id)

app/routers/transactions.py:

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