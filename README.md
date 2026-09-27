# FastAPI E-Commerce & Inventory Management API

A modern, production-grade, scalable REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.0**, **Alembic**, and **Pydantic v2**. 

This project follows clean software architecture principles, separating API boundaries, business logic, and database entities, complete with secure JWT authentication and version-controlled database migrations.

---

## Tech Stack & Tools

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance, async web framework)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Data Validation & Serialization**: [Pydantic v2](https://docs.pydantic.dev/) & [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Security & Authentication**: [PyJWT](https://pyjwt.readthedocs.io/) & [Bcrypt](https://pypi.org/project/bcrypt/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)

---

## Project Architecture

The project follows a **Layered Architecture** designed to scale into enterprise fullstack applications:

```text
fastapi-app/
├── app/
│   ├── api/
│   │   ├── deps.py               # Security dependencies (get_current_user, get_current_admin)
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py       # Authentication routes (signup, login)
│   │       │   ├── products.py   # Product CRUD endpoints
│   │       │   └── users.py      # User management endpoints
│   │       └── router.py         # Master v1 API router
│   ├── core/
│   │   ├── config.py             # Pydantic Settings reading from .env
│   │   ├── database.py           # Engine, SessionLocal, get_db generator
│   │   └── security.py           # Bcrypt password hashing & JWT generation
│   ├── crud/
│   │   ├── product.py            # Isolated product database operations
│   │   └── user.py               # User queries & authentication logic
│   ├── models/                   # SQLAlchemy ORM database models
│   │   ├── product.py            # Product entity (product table)
│   │   └── user.py               # User entity (users table)
│   └── schemas/                  # Pydantic validation & response schemas
│       ├── product.py            # ProductCreate, ProductUpdate, ProductResponse
│       ├── token.py              # Token, TokenData
│       └── user.py               # UserCreate, UserResponse (password excluded!)
├── alembic/                      # Alembic database migrations
│   ├── versions/                 # Versioned migration scripts
│   └── env.py                    # Alembic configuration connected to app.models
├── alembic.ini                   # Alembic settings
├── .env.example                  # Environment configuration template
├── requirements.txt              # Project dependencies
└── main.py                       # Application entrypoint & CORS middleware
```

---

## Features Implemented

### Phase 1: Modular Architecture & Alembic Migrations
- **Separation of Concerns**: Strict boundary between API endpoints, database models, Pydantic schemas, and CRUD queries.
- **Product Management (CRUD)**:
  - `GET /api/v1/products/`: Paginated product listing with `skip` and `limit`.
  - `GET /api/v1/products/{id}`: Fetch single product by primary key.
  - `POST /api/v1/products/`: Create product with PostgreSQL auto-incrementing IDs.
  - `PATCH /api/v1/products/{id}`: Partial product update.
  - `DELETE /api/v1/products/{id}`: Remove product from database.
- **Alembic Database Version Control**: Tracks database schema history; supports `upgrade` and `downgrade`.

### Phase 2: Authentication, Authorization & Security
- **Secure Password Hashing**: Passwords are encrypted with **Bcrypt** and unique cryptographic salts (defeats rainbow tables).
- **Stateless JWT Authentication**: Issues standard signed JWT Bearer tokens with configurable expiration (`HS256`).
- **OAuth2 Password Bearer Flow**: Built-in support for Swagger UI's **Authorize 🔓** modal.
- **Security Guards**: Dependency injection (`Depends(get_current_user)`) guards protected routes before endpoint execution.
- **Data Filtering & Leak Prevention**: `UserResponse` schema whitelists only public user fields; sensitive data like `hashed_password` is never sent over the network.

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- PostgreSQL server installed and running

### 2. Clone & Setup Environment
```bash
# Clone the repository
git clone https://github.com/Shahriar220/fast-api-learning.git
cd fast-api-learning

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your database credentials:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
PROJECT_NAME="FastAPI E-Commerce"
API_V1_STR="/api/v1"
DATABASE_URL="postgresql+psycopg2://postgres:your_password@localhost:5432/fastapi"
DEBUG=True

SECRET_KEY="your-super-secret-key-change-this"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Run Database Migrations
Apply all version-controlled migrations to PostgreSQL:
```bash
alembic upgrade head
```

### 5. Start the Server
```bash
uvicorn main:app --reload
```
The server will start at **`http://127.0.0.1:8000`**.

---

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints Reference

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/auth/signup` | Register a new user | No |
| `POST` | `/api/v1/auth/login` | Login with OAuth2 form to get JWT token | No |

### Users (`/api/v1/users`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/users/me` | Get current logged-in user profile | **Yes (Bearer JWT)** |

### Products (`/api/v1/products`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/products/` | List products with pagination (`skip`, `limit`) | No |
| `GET` | `/api/v1/products/{id}` | Get product details by ID | No |
| `POST` | `/api/v1/products/` | Create a new product | No |
| `PATCH` | `/api/v1/products/{id}` | Partially update product details | No |
| `DELETE` | `/api/v1/products/{id}` | Delete a product | No |

---

## Database Migrations Cheat Sheet

```bash
# Check current migration revision
alembic current

# Generate a new migration after modifying models
alembic revision --autogenerate -m "describe_changes"

# Apply all pending migrations
alembic upgrade head

# Rollback the last migration
alembic downgrade -1
```

---

## Engineering Roadmap

- [x] **Phase 1**: Clean Layered Architecture & Alembic Migrations
- [x] **Phase 2**: Authentication, JWT Tokens & Password Hashing
- [ ] **Phase 3**: Relational Schemas (Categories, Orders) & Advanced Queries
- [ ] **Phase 4**: Redis In-Memory Caching & Background Task Queues (Celery / ARQ)
- [ ] **Phase 5**: Docker & Multi-Container Docker Compose Setup
- [ ] **Phase 6**: Modern Frontend Integration (Next.js / TypeScript)
- [ ] **Phase 7**: Production Networking & Nginx Load Balancing
- [ ] **Phase 8**: Kubernetes (K8s) Cluster Deployment & Auto-scaling