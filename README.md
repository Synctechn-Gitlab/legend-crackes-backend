# Classic Legend Crackers E-Commerce REST API Backend

A production-ready, high-performance REST API backend for the Classic Legend Crackers e-commerce platform built with **Python 3.11+**, **FastAPI**, **SQLAlchemy 2.x**, **PostgreSQL**, **Pydantic v2**, and **Alembic**.

Designed from the ground up to support **3000+ products**, high-concurrency festival flash-sales, zero-trust server-side pricing recalculation, guest checkouts, and transactional inventory management with row locking.

---

## 🚀 Key Features

- **Engineered for 3000+ Products**: Server-side pagination (default 24, max 100), composite database indexes on `(category_id, is_active)`, `(is_active, is_featured)`, `product_code`, and `selling_price`.
- **Zero-Trust Order Pricing**: Never trusts client-submitted line totals or order sums. Prices, volume discounts, festival deductions, and delivery charges are strictly recalculated on the server using active database rates.
- **Transactional Stock Locking**: Prevents race conditions and overselling during festival rushes using database row locking (`with_for_update`) wrapped in an all-or-nothing rollback transaction block.
- **Dual-Mode Database**: Out-of-the-box local zero-config evaluation via SQLite, with full enterprise production support for PostgreSQL connection pooling (`pool_size`, `max_overflow`, `pool_recycle`).
- **Granular Clean Architecture**: Complete separation of concerns across `core/`, `models/`, `schemas/`, `repositories/`, `services/`, and `routers/`.
- **Admin JWT Security**: Secure `bcrypt` password hashing with salt (work factor 12), JWT access and refresh token rotation, and protected administrative routes.
- **Frontend Interoperability**: Seamlessly compatible with the React storefront (`crackers-store`), providing dual snake_case and camelCase response structures (`product_code` / `code`, `selling_price` / `price`, `stock_quantity` / `stock`).
- **Comprehensive Analytics**: Dashboard KPI metrics, daily/weekly/monthly revenue tracking, category sales share, and top-selling products.

---

## 🛠 Tech Stack

- **Framework**: FastAPI (Async ASGI)
- **ASGI Server**: Uvicorn with standard uvloop/httptools
- **ORM**: SQLAlchemy 2.x (with modern type annotations and 2.0 select syntax)
- **Database**: PostgreSQL (Driver: `psycopg2-binary`) & SQLite support
- **Data Validation & Settings**: Pydantic v2 & Pydantic-Settings
- **Migrations**: Alembic 1.x
- **Authentication**: PyJWT + Bcrypt
- **Testing**: Pytest + HTTPX

---

## 📁 Clean Architecture Project Structure

```
crackers-backend/
├── app/
│   ├── core/
│   │   ├── config.py         # Pydantic Settings & environment parsing
│   │   ├── database.py       # SQLAlchemy 2.x engine, connection pool & session
│   │   ├── dependencies.py   # Admin JWT bearer validation dependency
│   │   ├── logging.py        # Structured application and audit logging
│   │   └── security.py       # Bcrypt hashing & PyJWT token utilities
│   ├── models/
│   │   ├── admin_user.py     # Admin user credentials and roles
│   │   ├── category.py       # Fireworks categories and hierarchies
│   │   ├── product.py        # High-performance catalog model with composite indexes
│   │   ├── product_image.py  # Secondary product imagery
│   │   └── order.py          # Orders & OrderItems with snapshot integrity
│   ├── repositories/
│   │   ├── admin_repo.py     # Admin lookup and query repository
│   │   ├── analytics_repo.py # SQL aggregations, KPI summaries, and trends
│   │   ├── category_repo.py  # Category queries with live product counts
│   │   ├── order_repo.py     # Filtered, paginated order search
│   │   └── product_repo.py   # Indexed search, sorting, filtering & row-locking
│   ├── schemas/
│   │   ├── admin.py          # Admin login and JWT payload schemas
│   │   ├── category.py       # Category request/response schemas
│   │   ├── dashboard.py      # KPI cards, revenue charts, and inventory alerts
│   │   ├── inventory.py      # Stock modification schemas
│   │   ├── order.py          # Guest checkout and order status schemas
│   │   ├── product.py        # Validated product schemas with frontend aliases
│   │   └── revenue.py        # Sales analytics and period breakdown schemas
│   ├── services/
│   │   ├── analytics_service.py # KPI and revenue reporting logic
│   │   ├── auth_service.py   # Authentication, verification, and audit logs
│   │   ├── category_service.py # Category domain operations
│   │   ├── inventory_service.py # Stock adjustment & safety checks (prevents negative stock)
│   │   ├── order_service.py  # Atomic transactions, stock deduction & price recalculation
│   │   └── product_service.py# Catalog listing, slug lookups, and validations
│   ├── routers/
│   │   ├── auth.py           # /api/auth (login, refresh, me, logout)
│   │   ├── categories.py     # /api/categories (public browse & admin CRUD)
│   │   ├── products.py       # /api/products (public search, filter, admin CRUD)
│   │   ├── orders.py         # /api/orders (public guest order placement)
│   │   ├── admin_orders.py   # /api/admin/orders (management and status updates)
│   │   ├── admin_inventory.py# /api/admin/inventory (bulk catalog and stock controls)
│   │   ├── admin_dashboard.py# /api/admin/dashboard (KPI stats and quick actions)
│   │   └── admin_revenue.py  # /api/admin/revenue (financial insights and reports)
│   ├── utils/
│   │   ├── formatters.py     # Slugs, order numbers, and JSON response adapters
│   │   └── pagination.py     # Server-side pagination bounds validation
│   ├── main.py               # FastAPI application setup, CORS, and error handlers
│   └── seed.py               # 3000+ realistic product seeder script
├── alembic/                  # Database migration scripts
├── tests/                    # Comprehensive Pytest automated test suite
├── requirements.txt
├── .env.example
├── pytest.ini
└── run_server.py
```

---

## ⚡ Quick Start Guide

### 1. Set Up Environment

```bash
# Clone or navigate into crackers-backend
cd crackers-backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Default configuration in `.env`:
```ini
# PostgreSQL (Production / Local PostgreSQL service)
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/crackers_db
# Or zero-config SQLite:
# DATABASE_URL=sqlite:///./crackers.db

JWT_SECRET_KEY=sivakasi_fireworks_ultra_secure_production_secret_key_2026_x928a
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
```

### 3. Seed 3000+ Products, Categories & Default Admin

Run the high-performance database seeder:
```bash
python -m app.seed --count 3000
```
This automatically sets up:
- **Default Super Admin**:
  - Username: `admin` (or `admin@sivakasicrackers.com`)
  - Password: `admin123`
- **10 Core Fireworks Categories**: Aerial Shots, Multi-Shots, Sparklers, Flower Pots, Chakkars, Garlands/Wala, Sound Bombs, Rockets, Kids Specials, Gift Boxes, and Green Crackers.
- **3000+ Realistic Sivakasi Fireworks Products** with unique product codes (e.g. `SPK-1042`, `MLS-2104`), discounts, prices, stock quantities, and descriptions.
- **Initial Sample Orders** for instant dashboard analytics.

### 4. Run the API Server

```bash
python run_server.py
# Or directly via uvicorn:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API Base URL: `http://localhost:8000/api`
- Interactive Swagger Docs: `http://localhost:8000/docs`
- Redoc Documentation: `http://localhost:8000/redoc`

---

## 🧪 Running Automated Tests

Run the test suite with verbose output:
```bash
pytest -v
```

All 25 tests validate:
- Authentication & JWT token generation
- Server-side order price recalculation & anti-tampering
- Stock reservation and negative-inventory prevention
- Server-side pagination & 3000+ catalog search
- Admin category, order, and inventory management

---

## 📡 API Reference Overview

### 1. Authentication (`/api/auth`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/auth/login` | Authenticate with username/password | Public |
| `POST` | `/api/auth/refresh`| Refresh access token | Public |
| `GET` | `/api/auth/me` | Current admin profile | Admin |
| `POST` | `/api/auth/logout` | Session termination | Admin |

### 2. Products (`/api/products`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/products` | Paginated catalog (`page`, `limit`, `category`, `search`, `sort_by`, `price_min`, `price_max`) | Public |
| `GET` | `/api/products/{id}` | Single product by ID | Public |
| `GET` | `/api/products/slug/{slug}` | Single product by URL slug | Public |
| `GET` | `/api/products/featured` | Top featured showcase items | Public |
| `GET` | `/api/products/special-offers` | Top discounted festival offers | Public |
| `GET` | `/api/products/search` | Fast autocomplete search | Public |
| `POST` | `/api/products` | Create new product | Admin |
| `PUT` | `/api/products/{id}` | Update product details | Admin |
| `PATCH`| `/api/products/{id}/stock`| Fast stock adjustment (validates stock >= 0) | Admin |
| `DELETE`| `/api/products/{id}` | Delete product from catalog | Admin |

### 3. Categories (`/api/categories`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/categories` | List active categories with product counts | Public |
| `GET` | `/api/categories/{id}` | Get category details | Public |
| `POST` | `/api/categories` | Create category | Admin |
| `PUT` | `/api/categories/{id}` | Update category | Admin |
| `DELETE`| `/api/categories/{id}` | Delete category | Admin |

### 4. Orders (`/api/orders` & `/api/admin/orders`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/orders` | Guest checkout (Server recalculates all prices, locks stock, creates atomic order) | Public |
| `GET` | `/api/admin/orders` | Paginated orders with search & status filters | Admin |
| `GET` | `/api/admin/orders/{id}` | Detailed order breakdown | Admin |
| `PATCH`| `/api/admin/orders/{id}/status`| Update status (`Pending`, `Confirmed`, `Processing`, `Shipped`, `Delivered`, `Cancelled`) | Admin |

### 5. Inventory Management (`/api/admin/inventory`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/admin/inventory` | Paginated catalog with low-stock alerts | Admin |
| `POST` | `/api/admin/inventory/products` | Add product to inventory | Admin |
| `PUT` | `/api/admin/inventory/products/{id}` | Update inventory product | Admin |
| `PATCH`| `/api/admin/inventory/products/{id}/stock`| Inline stock adjustment | Admin |
| `DELETE`| `/api/admin/inventory/products/{id}` | Delete inventory product | Admin |

### 6. Dashboard & Analytics (`/api/admin/dashboard` & `/api/admin/revenue`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/admin/dashboard` | Overall KPI stats (totals, revenue, orders, low stock) | Admin |
| `GET` | `/api/admin/revenue` | Revenue trends (`daily`, `weekly`, `monthly`) | Admin |
| `GET` | `/api/admin/revenue/category` | Category-wise revenue contribution | Admin |
| `GET` | `/api/admin/revenue/top-products` | Top-selling products by units & gross revenue | Admin |

---

## 🔒 Security Best Practices Implemented

1. **Password Protection**: Passwords are never stored in plaintext. They are encrypted using `bcrypt` with unique cryptographic salts.
2. **JWT Route Protection**: All administration routes are guarded by JWT bearer tokens with configurable expiration (`ACCESS_TOKEN_EXPIRE_MINUTES`).
3. **Server-Side Price Recalculation**: Prevents client-side price tampering by recalculating all costs strictly against live database product records.
4. **SQL Injection Defense**: All database queries are executed through SQLAlchemy ORM parameterization.
5. **Standardized Error Responses**:
```json
{
  "success": false,
  "message": "Insufficient stock for '12 Shots Sky Bloom'. Available: 10, Requested: 50.",
  "detail": "Insufficient stock for '12 Shots Sky Bloom'. Available: 10, Requested: 50."
}
```
