# Backend System – Online Shop

**Backend system** for managing an online shop, built with Python and FastAPI.  
Supports clients, products, orders, and transactions, demonstrating **CRUD operations**, **database migrations** with Alembic, and **clean backend architecture**.

---

## 🛠 Technologies
- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- Alembic (Database migrations)
- PostgreSQL
- Docker & Docker Compose

---

## 📂 Project Structure



---

## ⚡ Key Concepts Demonstrated
- Clean Architecture & Layered Structure (Repository + Service pattern)
- Async backend development with SQLAlchemy + PostgreSQL
- Unit of Work pattern
- Transaction management
- CRUD operations for clients, products, orders, and transactions
- Database migrations with Alembic
- Dockerized environment

---

## 🚀 How to Run Locally

1. **Clone the repository**
```bash
git clone https://github.com/bogdan0089/Backend-System.git
cd "Project Online Shop"


python -m venv .venv
pip install -r requirements.txt


cp .env.example .env   # (Windows: copy .env.example .env)


docker-compose up --build