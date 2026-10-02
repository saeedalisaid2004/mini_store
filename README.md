 Mini Store API

A production-ready e-commerce RESTful API built with **Django 6**, **Django REST Framework**, **PostgreSQL**, **Celery**, **Redis**, and **Docker Compose**. 

The architecture strictly adheres to enterprise-grade standards, enforcing **clean architecture principles**, **concurrency control**, **transactional safety**, **idempotency**, and strict **type-checking & code formatting**.

---

 Features

- Catalog Management:
  - Category hierarchy and product listing with multi-language support (`name_ar` / `name_en`).
  - Search, pagination, and multi-field filtering (by price range, active status, category).
- Cart Engine:
  - Session/User cart management with dynamic stock validation.
- Transactional Checkout & Orders:
  - Atomic database transactions with row-level locking (`select_for_update`) to eliminate race conditions and overselling.
  - State machine workflow for order status updates (`pending`, `paid`, `cancelled`).
  - Idempotent request protection via `Idempotency-Key` headers.
- Asynchronous Processing:
  - Celery background task processing hooked into Django's `transaction.on_commit()` for post-checkout order emails.

---

 Tech Stack & Tooling

- Backend Framework: Django 6, Django REST Framework (DRF)
- Database**: PostgreSQL
- Background Tasks & Caching**: Celery, Redis
- Containerization: Docker, Docker Compose
- Quality Assurance:
  - Linter & Formatter: Ruff
  - Type Checking: Mypy with `django-stubs`
  - Testing: Pytest

---

 Quick Start & Setup

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Git](https://git-scm.com/) installed.

### Installation Steps

1. Clone the repository:
   ```bash
   git clone [https://github.com/saeedalisaid2004/mini_store.git](https://github.com/saeedalisaid2004/mini_store.git)
   cd mini_store
