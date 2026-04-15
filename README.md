# Backend System – Online Shop

**Backend system** for managing an online shop, built with Python and FastAPI.
Supports clients, products, orders, and transactions, demonstrating **CRUD operations**, **JWT authentication**, **role-based access control**, **product moderation**, **database migrations** with Alembic, and **clean backend architecture**.

---

## Technologies
- Python 3.11
- FastAPI
- SQLAlchemy (async ORM)
- Alembic (Database migrations)
- PostgreSQL
- Docker & Docker Compose
- Redis (caching)
- JWT (PyJWT)
- bcrypt / passlib
- aiosmtplib (async email via SMTP)

---

## Project Structure

```
├── app/              # Routers (FastAPI endpoints)
├── services/         # Business logic
├── repositories/     # Database queries
├── models/           # SQLAlchemy models
├── schemas/          # Pydantic schemas
├── core/             # Config, custom exceptions, enums
├── database/         # Session, Unit of Work
├── utils/            # Password hashing, JWT dependencies
├── alembic/          # Migrations
├── Dockerfile
└── docker-compose.yml
```

---

## Key Concepts Demonstrated

- **Architecture:** Router → Service → Unit of Work → Repository → DB, strict layer separation with no cross-layer dependencies
- **Data Modeling:** 4 ORM models (Client, Order, Product, Transaction) with One-to-Many (Client → Orders, Transactions) and Many-to-Many (Order ↔ Products, Client ↔ Products) via association tables
- **Auth & Security:** JWT access + refresh token flow, bcrypt password hashing, email verification via UUID token stored in Redis (24h TTL)
- **RBAC:** 3 roles (client / moderator / superadmin) with role-based endpoint protection
- **Product Moderation:** pending → accept / rejected workflow, moderated by moderator or superadmin
- **Caching:** Redis with 60s TTL on list/stats endpoints, cache invalidation on every write
- **Business Logic:** order checkout (balance deduction + transaction creation), order refund (balance restore + refund transaction)
- **Infrastructure:** Docker Compose, Alembic migrations with custom PostgreSQL Enum types, async email via aiosmtplib (Gmail SMTP)
- **Testing:** 56 pytest tests (unit + integration), async setup with NullPool + FakeRedis

---

## Roles

| Role | Access |
|------|--------|
| `client` | Own resources only |
| `moderator` | Moderate products (approve / reject) |
| `superadmin` | Full access to all resources |

> First superadmin must be set directly in the database:
> ```sql
> UPDATE clients SET role='superadmin' WHERE email='your@email.com';
> ```

---

## How to Run

1. **Clone the repository**
```bash
git clone https://github.com/bogdan0089/OnlineShop.git
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

---

## API Endpoints

> 🔓 Public &nbsp; 🔒 Authenticated &nbsp; 🔑 Admin (superadmin) &nbsp; 🛡 Moderator (moderator or superadmin)

Auth:
| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /auth/register | 🔓 | Register new client |
| POST | /auth/client_login | 🔓 | Login, get access + refresh token |
| POST | /auth/refresh | 🔓 | Refresh access token |
| POST | /auth/change_password | 🔒 | Change password |
| POST | /auth/change_role/{client_id} | 🔑 | Change client role |
| GET | /auth/verify/{token} | 🔓 | Verify email via token |

Client:
| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /client/create_client | 🔓 | Register new client |
| GET | /client/me | 🔒 | Get my profile |
| GET | /client/me/stats | 🔒 | My statistics (orders, spent) |
| GET | /client/me/orders | 🔒 | My orders |
| GET | /client/get_clients | 🔑 | List all clients |
| GET | /client/{id} | 🔒 | Get client by ID |
| PUT | /client/{id} | 🔒 | Update client |
| DELETE | /client/{id} | 🔒 | Delete client |
| POST | /client/{id}/deposit | 🔒 | Deposit balance |
| POST | /client/{id}/withdraw | 🔒 | Withdraw balance |
| GET | /client/{id}/orders/count | 🔒 | Count client orders |

Product:
| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /product/ | 🔒 | Create product (status: pending) |
| GET | /product/all | 🔓 | List accepted products |
| GET | /product/search?name= | 🔓 | Search by name |
| GET | /product/filter?min_price=&max_price= | 🔓 | Filter by price |
| GET | /product/{id} | 🔓 | Get product by ID |
| PUT | /product/{id} | 🔑 | Update product |
| DELETE | /product/{id} | 🔑 | Delete product |
| PATCH | /product/{id}/moderate | 🛡 | Approve or reject product |

Order:
| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /order/create_orders | 🔒 | Create order |
| POST | /order/orders | 🔒 | Create order with product |
| GET | /order/get_orders | 🔑 | List all orders (pagination) |
| GET | /order/orders/{id} | 🔒 | Get order by ID |
| PUT | /order/order_update/{id} | 🔒 | Update order title |
| PUT | /order/{id}/status | 🔒 | Update order status |
| GET | /order/order/{id}/total_price | 🔒 | Get order total price |
| GET | /order/order_with_products/{id} | 🔒 | Order with products |
| POST | /order/{id}/products/{product_id} | 🔒 | Add product to order |
| DELETE | /order/{id}/order/{product_id}/product | 🔒 | Remove product from order |
| POST | /order/{id}/checkout | 🔒 | Checkout order |
| POST | /order/{id}/refund | 🔒 | Cancel order with refund |

Transaction:
| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /transaction/create_transaction | 🔒 | Create transaction |
| GET | /transaction/me/transactions | 🔒 | My transactions (pagination) |
| GET | /transaction/{id} | 🔒 | Get transaction by ID |
| GET | /transaction/{client_id}/transactions | 🔒 | Client transactions |
