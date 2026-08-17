# Multi-Vendor E-commerce Backend API

A production-ready Multi-Vendor E-commerce Backend API built with FastAPI, PostgreSQL, SQLAlchemy 2.0, Redis, and Celery.

## Features

- **Role-Based Access Control**: Customers, Vendors, Admins, Super Admins, Delivery Agents.
- **Authentication**: JWT, Refresh Tokens, Password Hashing (bcrypt).
- **Vendor Management**: Vendor dashboards, approvals, and metrics.
- **Product Management**: Variants, inventory tracking, categories, brands.
- **Shopping Cart & Checkout**: Advanced pricing validation, coupon processing, and split-order logic for multi-vendor checkout.
- **Order Management**: Status tracking, parent/sub-orders for multi-vendor purchases.
- **Payment Abstraction**: Pluggable architecture for multiple payment gateways (Stripe, SSLCommerz, etc.).
- **Async Architecture**: Fully asynchronous database and API operations using `asyncpg` and FastAPI.

## Tech Stack

- **Framework**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL with SQLAlchemy 2.0 and Alembic
- **Caching**: Redis
- **Background Tasks**: Celery
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx & Uvicorn

## Installation & Setup

### Environment Variables

Copy the example env file and update the values:

```bash
cp .env.example .env
```

### Docker Setup (Recommended)

Start the entire stack (API, PostgreSQL, Redis) with Docker Compose:

```bash
docker-compose up --build
```

### Manual Setup

1. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Or `venv\\Scripts\\activate` on Windows
pip install -r requirements.txt
```

2. Start PostgreSQL and Redis locally, and update your `.env` file with the correct credentials.

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/api/v1/openapi.json` (or `/docs`)
- **ReDoc**: `http://localhost:8000/redoc`

## Folder Structure

- `app/api/v1/`: API endpoints organized by features.
- `app/core/`: Application settings, security, and database setup.
- `app/models/`: SQLAlchemy database models.
- `app/schemas/`: Pydantic models for request/response validation.
- `app/services/`: Core business logic separated from route handlers.
- `app/repositories/`: Data access layer for database operations.
"# versity_project" 
"# university-project" 
"# university-project" 
"# university-project" 
