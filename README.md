# Backend System – Online Shop

**Backend system** for managing an online shop, built with Python and FastAPI.
Supports clients, products, orders, and transactions, demonstrating **CRUD operations**, **JWT authentication**, **database migrations** with Alembic, and **clean backend architecture**.

---

## Technologies
- Python 3.11
- FastAPI
- SQLAlchemy (async ORM)
- Alembic (Database migrations)
- PostgreSQL
- Docker & Docker Compose
- JWT (PyJWT)
- bcrypt / passlib

---

## Project Structure

```
├── app/              # Routers (FastAPI endpoints)
├── services/         # Business logic
├── repositories/     # Database queries
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── core/             # Config, custom exceptions
├── database/         # Session, Unit of Work
├── utils/            # Password hashing, JWT dependencies
├── alembic/          # Migrations
├── Dockerfile
└── docker-compose.yml
```

---

## Key Concepts Demonstrated
- Clean Architecture: Repository + Service pattern
- Async backend with SQLAlchemy + PostgreSQL
- Unit of Work pattern
- JWT authentication (register, login, protected endpoints)
- Password hashing with bcrypt
- CRUD operations for clients, products, orders, and transactions
- Database migrations with Alembic
- Dockerized environment

---

## How to Run

1. **Clone the repository**
```bash
git clone https://github.com/bogdan0089/Backend-System.git
cd "Project Online Shop"
```

2. **Create virtual environment**
```bash
python -m venv .venv
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
```

4. **Run with Docker**
```bash
docker compose up --build
```

API available at: `http://localhost:8000/docs`
