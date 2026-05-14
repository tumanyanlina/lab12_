from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.database import engine, Base, SessionLocal
from app.models import Stock
from app.routers import auth, stocks, portfolio, transactions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)


def init_db():
    db = SessionLocal()
    try:
        if db.query(Stock).count() == 0:
            test_stocks = [
                Stock(symbol="AAPL", name="Apple Inc.", current_price=175.50),
                Stock(symbol="GOOGL", name="Alphabet Inc.", current_price=140.25),
                Stock(symbol="MSFT", name="Microsoft Corporation", current_price=380.00),
                Stock(symbol="AMZN", name="Amazon.com Inc.", current_price=145.80),
                Stock(symbol="TSLA", name="Tesla Inc.", current_price=240.50),
                Stock(symbol="META", name="Meta Platforms Inc.", current_price=310.00),
                Stock(symbol="NVDA", name="NVIDIA Corporation", current_price=890.00),
                Stock(symbol="JPM", name="JPMorgan Chase & Co.", current_price=190.00),
            ]
            for stock in test_stocks:
                db.add(stock)
            db.commit()
            logger.info(f"Created {len(test_stocks)} test stocks")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


init_db()

app = FastAPI(
    title="Trading Platform API",
    description="API для онлайн-торговли акциями",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(stocks.router)
app.include_router(portfolio.router)
app.include_router(transactions.router)


@app.get("/")
def root():
    return {
        "app_name": "Trading Platform API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth/register, /auth/login",
            "stocks": "/stocks",
            "portfolio": "/portfolio",
            "transactions": "/transactions/buy, /transactions/sell, /transactions"
        },
        "documentation": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}