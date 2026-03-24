# 🛒 FastAPI Shop

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.133.0-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

## 🚀 О проекте

**FastAPI Shop** — это современный, быстрый и масштабируемый backend для интернет-магазина, построенный на базе асинхронного фреймворка FastAPI. Проект решает проблему долгого старта при разработке e-commerce приложений, предоставляя готовое REST API для управления каталогом товаров, корзиной покупок и безопасной аутентификацией пользователей "из коробки".

## ✨ Ключевые особенности

* 🔐 **Безопасная аутентификация:** Полноценное управление пользователями (регистрация, логин, восстановление пароля) с использованием JWT-токенов на базе `fastapi-users`.
* 📦 **Управление каталогом:** Удобные CRUD-операции для категорий и товаров с поддержкой фильтрации.
* 🛒 **Умная корзина:** API для добавления товаров, изменения их количества, удаления и автоматического подсчета итоговой стоимости.
* ⚡ **Высокая производительность:** Полностью асинхронная работа с базой данных благодаря связке `SQLAlchemy 2.0` и `asyncpg`.
* 🔄 **Миграции БД:** Автоматизированное управление структурой базы данных с помощью `Alembic`.

## 🛠 Стек технологий

* **Язык:** [Python 3.12+](https://www.python.org/)
* **Фреймворк:** [FastAPI](https://fastapi.tiangolo.com/)
* **База данных:** [PostgreSQL](https://www.postgresql.org/) (драйвер `asyncpg`)
* **ORM & Миграции:** [SQLAlchemy](https://www.sqlalchemy.org/) (async) и [Alembic](https://alembic.sqlalchemy.org/)
* **Аутентификация:** [FastAPI Users](https://fastapi-users.github.io/fastapi-users/)
* **Менеджер зависимостей:** [uv](https://docs.astral.sh/uv/)

## 🧪 Запуск и тестирование проекта

Вы можете протестировать и запустить проект двумя способами: через Docker (изолированно) или локально (например, для разработки в PyCharm). 

Для начала склонируйте репозиторий:
```bash
git clone https://github.com/yourusername/fastapi-shop-app.git
cd fastapi-shop-app
```

### Способ 1: Запуск через Docker 🐳

При использовании Docker база данных и само приложение автоматически разворачиваются в изолированных контейнерах.

1. **Создайте файл окружения:**
   Скопируйте шаблон файла конфигурации:
   ```bash
   cp .env.template .env
   ```
2. **Настройте переменные для Docker:**
   ⚠️ **Важно:** Убедитесь, что в вашем `.env` файле раскомментирована ссылка для Docker, а переменная `APP_CONFIG__DB__URL` использует хост `db` (имя сервиса базы данных в docker-compose):
   ```dotenv
   APP_CONFIG__DB__URL=postgresql+asyncpg://my_db_user:my_super_secret_password@db:5432/fastshop_db
   ```
3. **Запустите проект:**
   ```bash
   docker-compose up -d --build
   ```
   *Приложение и база данных будут автоматически собраны и запущены.*

### Способ 2: Запуск локально (PyCharm / IDE) 💻

Если вы хотите запустить проект локально для разработки и отладки:

1. **Установите зависимости:**
   Проект использует современный и сверхбыстрый менеджер пакетов `uv`. Команда `uv sync` автоматически создаст виртуальное окружение и установит все пакеты.
   ```bash
   uv sync
   ```
2. **Создайте файл окружения:**
   Скопируйте шаблон:
   ```bash
   cp .env.template .env
   ```
3. **Настройте подключение к БД:**
   ⚠️ **Важно:** В файле `.env` закомментируйте URL для Docker и раскомментируйте/укажите URL для локального подключения (`localhost`).
   ```dotenv
   APP_CONFIG__DB__URL=postgresql+asyncpg://my_db_user:my_super_secret_password@localhost:5432/fastshop_db
   ```
4. **Подготовьте базу данных:**
   Создайте в вашей локальной СУБД (PostgreSQL) базу данных и пользователя **ровно с такими же именами**, которые вы указали в вашем `.env` файле (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`).
5. **Сгенерируйте и примените миграции:**
   Для создания таблиц в вашей базе данных сгенерируйте миграции через Alembic и примените их:
   ```bash
   uv run alembic revision --autogenerate -m "Initial migration"
   uv run alembic upgrade head
   ```
6. **Запустите сервер разработки:**
   Запустите проект через конфигурацию PyCharm или командой:
   ```bash
   uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 💻 Использование

После запуска сервера интерактивная документация API (Swagger UI) будет доступна по адресу:
`http://localhost:8000/docs`

![Скриншот Swagger UI](https://via.placeholder.com/800x400?text=Swagger+UI+Screenshot)

**Пример запроса на получение списка категорий:**
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/categories/' \
  -H 'accept: application/json'
```

## 📫 Контакты

* **GitHub:** [@ygrec4ka](https://github.com/ygrec4ka)
