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