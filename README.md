# TaskFlow Backend - Take-Home Assignment

## 1. Overview

TaskFlow is a minimal yet production-structured task management backend that allows users to:

- Register and log in with JWT authentication
- Create and manage projects
- Create, update, assign, and delete tasks within projects

The focus of this project is on clean architecture, correct API design, and explicit tradeoffs rather than feature completeness.

### Tech Stack

- Backend: FastAPI (Python)
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- Authentication: JWT-based authentication with Bearer tokens
- Containerization: Docker & Docker Compose

---

## 2. Architecture Decisions

### Layered Architecture

The application is structured into clear layers:

- Routes (API layer): handle HTTP requests and responses
- Services (business logic): enforce rules like ownership and validation
- Database layer: SQLAlchemy models and persistence
- Schemas: request/response validation via Pydantic

Business logic is intentionally kept out of route handlers to avoid tightly coupled code and improve long-term maintainability.

---

### Authentication

JWT-based stateless authentication is used.

- Tokens contain `user_id` and `email`
- Expiry is set to 24 hours
- Passwords are hashed using bcrypt

This avoids server-side session storage and works well in containerized environments.

---

### Authorization (Ownership-Based)

Authorization is implemented using resource ownership:

- Projects can only be modified by their owner
- Tasks can only be modified by the task creator or project owner

Tradeoff:
- No RBAC (role-based access control)
- Would be added in a real system with roles like admin/member

---

### Database & Migrations

- PostgreSQL is used for relational consistency
- Alembic manages schema migrations (no auto-create tables)

This ensures version-controlled schema changes.

---

### Tradeoffs & Scope Decisions

- No refresh tokens → simpler auth flow
- No caching → unnecessary for current scale
- No background jobs → not required
- No RBAC → ownership-based access sufficient

---

### Design Principles

- Simplicity over overengineering
- Explicit over implicit behavior
- Clear separation of concerns

---


## 3. Running Locally

### Prerequisites

- Docker

### Steps

```
git clone https://github.com/prashantv04/taskflow-prashant
cd taskflow-prashant
cp .env.example .env
docker compose up --build
```

### Access

- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

---

## 4. Running Migrations

Migrations run automatically on container startup.

Manual commands (if needed):

```
docker compose exec backend alembic upgrade head
```
To create a new migration:
```
docker compose exec backend alembic revision --autogenerate -m "message"
```

## 5. Seeding Data

Seed data is included for quick testing.

To run manually:

Windows (PowerShell):

```
Get-Content backend/seed.sql | docker compose exec -T db psql -U postgres -d taskflow
```

macOS/Linux:

```
cat backend/seed.sql | docker compose exec -T db psql -U postgres -d taskflow
```

---

## 6. Test Credentials

Email: test@example.com  
Password: password123

---

## 7. API Reference

All endpoints (except `/auth/*`) require:

```
Authorization: Bearer <token>
```

### Login Example

POST `/auth/login`

Request:

```
{
    "email": "test@example.com",
    "password": "password123"
}
```
Response:

```
{
    "access_token": "<jwt>",
    "token_type": "bearer"
}
```

### Auth
- POST /auth/register
- POST /auth/login

### Projects
- GET /projects?page=1&limit=10
- POST /projects
- GET /projects/{id}
- PATCH /projects/{id}
- DELETE /projects/{id}
- GET /projects/{id}/stats

### Tasks
- GET /projects/{id}/tasks
- POST /projects/{id}/tasks
- PATCH /tasks/{id}
- DELETE /tasks/{id}

## 8. Error Handling

All errors follow a consistent structure:

### Unauthorized (401)

```
{
  "error": "unauthorized"
}
```

### Forbidden (403)

```
{
  "error": "forbidden"
}
```
### Not Found (404)

```
{
  "error": "not found"
}
```

### Validation Error (400)

```
{
  "error": "validation failed",
  "fields": {
    "field_name": "error message"
  }
}
```

## 9. What I'd Do With More Time

- Implement RBAC (role-based access control)
- Add refresh token flow
- Add integration tests
- Improve pagination metadata (total count, pages)
- Add Redis caching
- Add WebSocket support for real-time updates

---

## 10. Docker & Environment

- docker-compose runs PostgreSQL and backend
- Uses `.env` file for configuration
- `.env.example` is provided

---

## 11. Notes

- Alembic is used for migrations
- Passwords are hashed using bcrypt
- JWT secret is stored via environment variables

---
