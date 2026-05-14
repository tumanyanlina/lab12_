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

Задание 1:

О проекте:

Веб-приложение для онлайн-торговли акциями. Пользователи могут:
- Регистрироваться и входить в систему (JWT аутентификация)
- Просматривать список доступных акций с текущими ценами
- Покупать и продавать акции
- Смотреть свой портфель (количество акций, средняя цена, текущая стоимость, прибыль/убыток)
- Просматривать историю транзакций

Технологии:

| Технология | Назначение |
|------------|------------|
| FastAPI | Веб-фреймворк |
| SQLAlchemy | ORM для работы с БД |
| SQLite | База данных (для разработки) |
| JWT | Аутентификация |
| Pydantic | Валидация данных |
| Uvicorn | ASGI сервер |

Сущности:

| Модель | Описание |
|--------|----------|
| User | Пользователь (email, username, баланс) |
| Stock | Акция (символ, название, текущая цена) |
| Portfolio | Портфель (связь пользователя с акциями, количество, средняя цена) |
| Transaction | Транзакция (покупка/продажа, количество, цена, сумма) |

Установка и запуск

1. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd laba12

2. Создать виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

3. Установить зависимости
```bash
pip install -r requirements.txt

4. Настроить переменные окружения
Создать файл .env (скопировать из .env.example):

```bash
cp .env.example .env
.env.example содержит:

env
DATABASE_URL=sqlite:///./trading.db
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Запустить приложение
```bash
uvicorn app.main:app --reload
Сервер запустится на http://localhost:8000

API Эндпоинты: 

        Аутентификация
Метод	Эндпоинт	        Описание
POST	/auth/register	    Регистрация пользователя
POST	/auth/login	        Вход, получение JWT токена

        Акции
Метод	Эндпоинт	        Описание
GET	    /stocks	            Список всех акций
GET	    /stocks/{symbol}	Информация об акции

        Портфель
Метод	Эндпоинт	        Описание
GET	    /portfolio	        Текущий портфель с расчётом P&L

        Транзакции
Метод	Эндпоинт	        Описание
POST	/transactions/buy	Покупка акций
POST	/transactions/sell	Продажа акций
GET	    /transactions	    История сделок (с пагинацией)

        Прочее
Метод	Эндпоинт	        Описание
GET	    /	                Информация о приложении
GET	    /health	            Healthcheck для Docker

Примеры запросов:

        Регистрация
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "user", "password": "123456"}'

        Логин
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "123456"}'

        Покупка акций (с токеном)
```bash
curl -X POST "http://localhost:8000/transactions/buy" \
  -H "Authorization: Bearer <ваш_токен>" \
  -H "Content-Type: application/json" \
  -d '{"stock_symbol": "AAPL", "type": "BUY", "quantity": 10}'

        Портфель
```bash
curl -X GET "http://localhost:8000/portfolio" \
  -H "Authorization: Bearer <ваш_токен>"

Тестовые данные:
При первом запуске в БД автоматически создаются тестовые акции:

Символ	Компания	             Цена
AAPL	Apple Inc.	             $175.50
GOOGL	Alphabet Inc.	         $140.25
MSFT	Microsoft Corporation	 $380.00
AMZN	Amazon.com Inc.	         $145.80
TSLA	Tesla Inc.	             $240.50
META	Meta Platforms Inc.	     $310.00
NVDA	NVIDIA Corporation	     $890.00
JPM	    JPMorgan Chase & Co.	 $190.00

Начальный баланс пользователя:   $100,000

Структура проекта:
lab12/
├── app/
│   ├── __init__.py
│   ├── main.py          # Главный файл, роутеры, CORS
│   ├── database.py      # Подключение к БД
│   ├── models.py        # SQLAlchemy модели
│   ├── schemas.py       # Pydantic схемы
│   ├── auth.py          # JWT аутентификация
│   ├── crud.py          # Бизнес-логика (покупка/продажа)
│   └── routers/
│       ├── auth.py      # Эндпоинты /auth
│       ├── stocks.py    # Эндпоинты /stocks
│       ├── portfolio.py # Эндпоинты /portfolio
│       └── transactions.py # Эндпоинты /transactions
├── .gitignore
├── .env.example
├── requirements.txt
├── README.md
└── prompt_log.md        # Лог всех промптов к ИИ

Документация
После запуска доступна интерактивная документация:
Swagger UI: http://localhost:8000/docs

