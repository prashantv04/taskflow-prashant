# TaskFlow Backend - Take-Home Assignment

## 1. Overview

TaskFlow is a minimal task management backend system that allows users
to:

-   Register and log in with JWT authentication
-   Create and manage projects
-   Create, update, assign, and delete tasks within projects

### Tech Stack

-   Backend: FastAPI (Python)
-   Database: PostgreSQL
-   ORM: SQLAlchemy
-   Migrations: Alembic
-   Authentication: JWT-based authentication with Bearer tokens
-   Containerization: Docker & Docker Compose

------------------------------------------------------------------------

## 2. Architecture Decisions

### Structure

```
app/ 
├── api/      # Routes (controllers) 
├── services/ # Business logic 
├── db/       # Models & database setup 
├── schemas/  # Pydantic schemas 
├── core/     # Config & security 
├── utils/    # Helpers & error handling

```

### Key Decisions

-   FastAPI chosen for speed and built-in validation
-   SQLAlchemy + Alembic for proper schema control
-   Layered architecture for separation of concerns
-   JWT authentication with 24-hour expiry

### Tradeoffs

-   No refresh tokens (kept simple)
-   No caching layer
-   Minimal validation abstraction

------------------------------------------------------------------------

## 3. Running Locally

### Prerequisites

-   Docker installed

### Steps

```
git clone https://github.com/prashantv04/taskflow-prashant
cd taskflow-prashant
cp .env.example .env
docker compose up --build
```

### Access

-   API: http://localhost:8000
-   Swagger Docs: http://localhost:8000/docs

------------------------------------------------------------------------

## 4. Running Migrations

Migrations run automatically on container startup using:

- alembic upgrade head

------------------------------------------------------------------------

## 5. Test Credentials

- Email: test@example.com 
- Password: password123

------------------------------------------------------------------------

## 6. API Reference

Auth: 
- POST /auth/register 
- POST /auth/login

Projects: 
- GET /projects 
- POST /projects 
- GET /projects/{id} 
- PATCH /projects/{id} 
- DELETE /projects/{id}

Tasks: 
- GET /projects/{id}/tasks 
- POST /projects/{id}/tasks 
- PATCH /tasks/{id} 
- DELETE /tasks/{id}

Authorization: Bearer token required for all non-auth endpoints

Error format: 
```
{
  "error": "validation failed",
  "fields": {
    "field_name": "error message"
  }
}
```
------------------------------------------------------------------------

## 7. What I'd Do With More Time

-   Add refresh tokens
-   Add RBAC
-   Improve validation
-   Add tests
-   Add pagination
-   Add Redis caching
-   Improve logging

------------------------------------------------------------------------

## 8. Docker & Environment

-   docker-compose runs PostgreSQL and backend
-   Uses .env file
-   .env.example provided

------------------------------------------------------------------------

## 9. Notes

-   Alembic used for migrations
-   Passwords hashed with bcrypt
-   JWT secret via environment variables

------------------------------------------------------------------------

## 10. Submission

Run:

docker compose up

------------------------------------------------------------------------

## 11. Development Commands (Optional)

- These were used during development to create and manage migrations.
- All migrations are already included in the repository, and database schema is automatically applied on startup using Alembic.

### Generate migrations
```
docker compose exec backend alembic revision --autogenerate -m "message"
```
Apply migrations manually (handled automatically on startup)

```
docker compose exec backend alembic upgrade head
```

Seed database manually (optional)

Windows (PowerShell): 
```
Get-Content backend/seed.sql | docker compose exec -T db psql -U postgres -d taskflow
```

Linux/macOS equivalent:

``
cat backend/seed.sql | docker compose exec -T db psql -U postgres -d taskflow
``
------------------------------------------------------------------------
Thank you for reviewing this submission.
