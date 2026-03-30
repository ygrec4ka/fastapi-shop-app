# 🛒 FastAPI Shop

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.133.0-009688.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)

## 🚀 About the Project

**FastAPI Shop** provides a robust foundation for building online stores. It takes care of the routine setup of database connectivity, logging, configuration, and security, allowing developers to focus immediately on their core business logic. Whether you are building a small shop or a complex marketplace, this boilerplate offers the flexibility and performance needed for modern web development.

## ✨ Key Features

* 🔐 **Secure Authentication:** Full user management (registration, login, password recovery) using JWT tokens based on `fastapi-users`.
* 📦 **Catalog Management:** Robust CRUD operations for categories and products with built-in filtering support.
* 🛒 **Smart Shopping Cart:** Full-featured API for managing cart items, adjusting quantities, and automated total cost calculation.
* ⚡ **High Performance:** Fully asynchronous database interaction powered by `SQLAlchemy 2.0` and `asyncpg`.
* 🔄 **Database Migrations:** Seamless schema management and automated versioning using `Alembic`.

## 🛠 Tech Stack

The boilerplate includes a modern and high-performance stack:

* 🐍 **Python >= 3.13**
* ⚡ **FastAPI** — modern web framework.
* 🛡️ **FastAPI-Users** — ready-made Auth implementation (JWT / Database tokens).
* 🗄️ **SQLAlchemy 2.0 (Asyncio)** — next-generation ORM.
* 🐘 **Asyncpg** — the fastest asynchronous PostgreSQL driver.
* 🔄 **Alembic** — migration management (already configured with async template).
* ✅ **Pydantic v2 & Pydantic-Settings** — data validation and convenient configuration management.
* 🚀 **Uvicorn** — high-performance ASGI server.
* 📦 **uv** — lightning-fast package manager.

## 🧪 Installation & Running

I provide two main ways to work with the project. Both methods run locally but differ in the level of environment isolation.

### Preparation (Common for both methods)
1. **Clone the repository:**
   ```bash
   git clone https://github.com/ygrec4ka/fastapi-shop-app.git
   cd fastapi-shop-app
   ```
2. **Setup environment variables:**
   Copy the template:
   ```bash
   cp .env.template .env
   ```
   *Edit `.env` to set your passwords and choose the correct database URL (Docker or Local).*

---

### Method 1: Full Isolation via Docker 🐳 (Recommended)

In this mode, everything (database, backend, frontend, pgAdmin) runs in containers. You don't need to have Python or PostgreSQL installed on your host machine.

1. **Build and start containers:**
   ```bash
   docker compose up -d --build
   ```
2. **Apply migrations (REQUIRED):**
   This creates the database tables. Run this once at the start or whenever models change:
   ```bash
   docker compose exec backend alembic upgrade head
   ```
3. **Seed the database:**
   To populate the store with initial data (50 items and categories), run the seeding script:
   ```bash
   docker compose exec backend python -m backend.utils.seed_db --reset
   ```

---

### Method 2: Development via IDE 💻

This method is convenient for active coding sessions and debugging.

1. **Install dependencies:**
   I use the modern package manager `uv`. Sync your environment to create a virtual environment:
   ```bash
   uv sync
   ```
   *This will create a `.venv` folder and install all dependencies from `pyproject.toml`.*

2. **Prepare a local database:**
   - Install PostgreSQL.
   - Create an **empty database** and a user.
   - **Important:** The database name, username, and password must **strictly match** what you specified in the `.env` file (`POSTGRES_USER`, `POSTGRES_DB`, etc.).

3. **Configure `.env`:**
   Ensure `APP_CONFIG__DB__URL` points to `localhost:5432` instead of `db:5432`.

4. **Run migrations locally:**
   ```bash
   uv run alembic upgrade head
   ```

5. **Start the server:**
   In your IDE (e.g., PyCharm), create a "FastAPI" run configuration or run the command:
   ```bash
   uv run uvicorn backend.main:app --reload
   ```

---

## 🏗 Migrations (Important Note)

The database does not automatically know about changes in your `models/*.py` files.
- If you add a new entity (table) or field, create a new migration:
   ```bash
   # In Docker:
   docker compose exec backend alembic revision --autogenerate -m "Add new table"
   # Locally:
   uv run alembic revision --autogenerate -m "Add new table"
   ```
- Don't forget to apply it using `alembic upgrade head`.

## 💻 Usage

After starting the server:
- **Swagger API:** [http://localhost:8000/docs](http://localhost:8000/docs) — full list of endpoints and documentation.
- **Frontend (Store):** [http://localhost:8080](http://localhost:8080) — the user interface.
- **pgAdmin:** [http://localhost:5050](http://localhost:5050) — database management interface.

## 📫 Contacts
* **GitHub:** [@ygrec4ka](https://github.com/ygrec4ka)
