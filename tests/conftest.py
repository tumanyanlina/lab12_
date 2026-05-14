import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models import User, Stock
from app.auth import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db):
    def _get_test_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = _get_test_db
    return TestClient(app)


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpass123"),
        balance=100000.00
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_stock(db):
    stock = Stock(
        symbol="TEST",
        name="Test Stock",
        current_price=100.00
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock


@pytest.fixture
def auth_token(client, test_user):
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}