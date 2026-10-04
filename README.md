# Mini Store

A REST API for a small online store built with Django REST Framework.

The project handles products, categories, shopping carts, orders, authentication, and background tasks.

## Tech Stack

* Python
* Django 6
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* JWT Authentication
* Docker & Docker Compose
* drf-spectacular for API documentation

## Project Structure

The project uses a simple Service / Selector pattern:

* `services.py` → handles business logic and database changes.
* `selectors.py` → handles read-only database queries.
* `apis.py` → contains the API endpoints.

This keeps the API views simple and makes the business logic easier to test and maintain.

## Main Features

### Authentication

The API uses JWT authentication.

Users can log in and receive access and refresh tokens.

### Products

Products include information such as:

* Name
* Category
* Price
* Stock
* Active / inactive status

The product API also supports filtering, searching, ordering, and pagination.

### Cart

Users can:

* Add products to their cart
* Update quantities
* View their cart
* See the total price

Inactive products cannot be added to the cart, and users cannot add more items than the available stock.

### Orders

Users can create orders from their cart.

The checkout process uses database transactions to make sure stock and order data stay consistent.

The project also uses database locking when updating stock to handle multiple requests safely.

### Idempotency

The order API supports an `Idempotency-Key` header.

The key is associated with the authenticated user, so sending the same request again does not create another order for the same user.

### Background Tasks

Celery and Redis are used for tasks that can run in the background instead of blocking the API request.

## API Documentation

The API documentation is generated using OpenAPI and `drf-spectacular`.

After running the project, the Swagger documentation can be accessed from the API documentation endpoint.

## Running the Project

### Requirements

* Docker Desktop
* Git

### Environment Variables

Create a `.env` file in the project root based on `.env.example`.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=1
ALLOWED_HOSTS=*

DATABASE_URL=postgres://postgres:postgres@db:5432/mini_store
REDIS_URL=redis://redis:6379/0
```

### Start the Project

Run:

```bash
docker compose up --build
```

After the containers start, run the Django migrations:

```bash
docker compose exec web python manage.py migrate
```

The API can then be accessed through the configured local port.

## Development

The project uses:

* Ruff for linting and formatting
* Mypy for type checking
* Django REST Framework for API development

## Project Goal

The main goal of this project was to practice building a Django REST API with a structure that can be extended later as the application grows.
