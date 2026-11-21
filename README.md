# Banksys

REST API для учёта банковских вкладов: клиенты, виды депозитов и открытые счета.
Доступ по OAuth2 (JWT), права разграничены по ролям сотрудников.

## Стек

- Python 3.12, FastAPI
- SQLAlchemy 2 (async) + asyncpg, PostgreSQL 16
- Alembic — миграции
- Pydantic v2 / pydantic-settings — схемы и конфигурация
- PyJWT + pwdlib (argon2) — авторизация и хэширование паролей
- Docker / docker compose

## Структура проекта

```
backend/
├── main.py              # создание приложения, lifespan, подключение роутеров
├── dependencies.py      # зависимости FastAPI: сессия БД, сервисы, текущий пользователь, роли
├── core/
│   ├── config.py        # настройки (pydantic-settings, читаются из .env)
│   ├── exceptions.py    # ошибки бизнес-логики и их обработчик
│   ├── models/          # Base, DatabaseHelper (engine + сессии), ORM-модели
│   └── utils/           # JWT, хэширование паролей, стартовые данные
├── repositories/        # работа с БД (BaseRepository + репозиторий на каждую сущность)
├── services/            # бизнес-логика (CRUD-сервисы, авторизация, заполнение БД)
├── schemas/             # Pydantic-схемы запросов и ответов
└── routers/             # HTTP-эндпоинты
alembic/                 # миграции
```

Запрос проходит слои `router → service → repository → БД`. Роутеры не содержат логики,
сервисы бросают ошибки из `core/exceptions.py`, а обработчик превращает их
в HTTP-ответ `{"detail": "..."}`.

## Настройка

Скопируйте `.env.example` в `.env` и заполните:

| Переменная | Описание | Пример |
|---|---|---|
| `SECRET_KEY` | ключ подписи JWT | длинная случайная строка |
| `ALGORITHM` | алгоритм JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | время жизни access-токена, мин | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | время жизни refresh-токена, дни | `7` |
| `DATABASE_URL` | строка подключения к БД | `postgresql+asyncpg://user:pass@localhost:5432/mydb` |
| `ADMIN_FIRST_USERNAME` | логин первого администратора | `admin` |
| `ADMIN_FIRST_PASSWORD` | пароль первого администратора | |

Сгенерировать `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Запуск в Docker

```bash
docker compose up --build
```

- Контейнер `fastapi` при старте сам применяет миграции (`alembic upgrade head`).
- `DATABASE_URL` для контейнера задаётся в `docker-compose.yml` и указывает на сервис `postgres`.
  Значение из `.env` используется только при локальном запуске.
- Логин, пароль и имя БД Postgres можно переопределить переменными
  `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`. По умолчанию это `myuser` / `secret` / `mydb`.

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # Linux / macOS
pip install -r backend/requirements.txt

docker compose up -d postgres     # или свой PostgreSQL
alembic upgrade head
uvicorn backend.main:app --reload
```

Все команды выполняются из корня проекта.

Документация API: http://localhost:8000/docs

При первом запуске приложение создаёт администратора из `.env` и заливает демо-данные
(5 депозитов, 3 клиента, 3 счёта). Демо-данные добавляются только в пустую БД,
поэтому повторный запуск ничего не дублирует.

## Миграции

```bash
alembic revision --autogenerate -m "описание"   # создать миграцию по изменениям моделей
alembic upgrade head                            # применить
alembic downgrade -1                            # откатить последнюю
```

## Авторизация

1. Получите токен: `POST /oauth/token` (form-data: `username`, `password`).
2. Передавайте его в заголовке: `Authorization: Bearer <access_token>`.

В Swagger (`/docs`) для этого есть кнопка **Authorize**.

### Роли

| Роль | Права |
|---|---|
| `admin` | всё, включая регистрацию пользователей |
| `bank_operator` | создание, изменение и удаление клиентов и счетов |
| `deposit_manager` | создание, изменение и удаление видов депозитов |
| `analyst` | только чтение |

## API

| Метод | Путь | Доступ | Описание |
|---|---|---|---|
| POST | `/oauth/token` | все | вход, выдача access-токена |
| POST | `/oauth/register` | admin | создать пользователя |
| GET | `/oauth/me` | авторизованные | текущий пользователь |
| POST | `/oauth/logout?refresh_token=...` | все | отозвать refresh-токен |
| GET | `/oauth/getusers` | все | список пользователей |
| GET | `/client/` | все | список клиентов |
| GET | `/client/{client_id}` | все | клиент по id |
| POST | `/client/new` | bank_operator, admin | создать клиента |
| PATCH | `/client/{client_id}` | bank_operator, admin | изменить клиента |
| DELETE | `/client/{client_id}` | bank_operator, admin | удалить клиента |
| GET | `/deposit/` | все | список депозитов |
| GET | `/deposit/{deposit_id}` | все | депозит по id |
| POST | `/deposit/new` | deposit_manager, admin | создать депозит |
| PATCH | `/deposit/{deposit_id}` | deposit_manager, admin | изменить депозит |
| DELETE | `/deposit/{deposit_id}` | deposit_manager, admin | удалить депозит |
| GET | `/account/` | все | список счетов |
| GET | `/account/{account_numb}` | все | счёт по номеру |
| POST | `/account/new` | bank_operator, admin | открыть счёт |
| PATCH | `/account/{account_numb}` | bank_operator, admin | изменить счёт |
| DELETE | `/account/{account_numb}` | bank_operator, admin | удалить счёт |

Клиента или депозит, к которым привязаны счета, удалить нельзя: API вернёт `400`.

### Коды ошибок

| Код | Когда |
|---|---|
| 400 | удаление записи, на которую ссылаются счета |
| 401 | нет токена, токен неверный или истёк, неверный логин/пароль |
| 403 | недостаточно прав для роли |
| 404 | запись не найдена |
| 409 | пользователь с таким именем уже существует |
| 422 | ошибка валидации входных данных |
