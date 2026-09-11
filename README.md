# Decision Analysis API

A small REST API for structured decision analysis and deterministic weighted evaluation.

## Overview

Decision Analysis API allows authenticated users to create decisions, define criteria and options, assign criterion weights, score options, and obtain a deterministic weighted evaluation with ranking, tie handling, and explainable criterion contributions.

## Scope

The initial domain consists of:

* User
* Decision
* Criterion
* Option
* Score

```text
Decision
 ├── Criteria
 └── Options
       └── Scores
```

Each decision belongs to one user.

## Features

* Environment-based configuration — Implemented
* PostgreSQL database — Implemented
* Docker Compose development environment — Implemented
* Database health check — Implemented
* Application health endpoint — Implemented
* JWT authentication — Implemented
* Decision management — Implemented
* Criterion management — Implemented
* Option management — Implemented
* Score management — Implemented
* Weighted evaluation — Implemented
* Ranking and tie handling — Implemented
* Explainable criterion contributions — Implemented
* OpenAPI / Swagger — Implemented
* Automated tests — Implemented
* Railway deployment — Planned

## API

Base path:

```text
/api/v1/
```

### Health

```text
GET    /health/
```

Returns the application health status.

Status: Implemented

### Authentication

```text
POST   /api/v1/auth/register/
POST   /api/v1/auth/token/
POST   /api/v1/auth/token/refresh/
```

JWT-based authentication is used for protected API operations.

Status: Implemented

### Decisions

```text
POST   /api/v1/decisions/
GET    /api/v1/decisions/
GET    /api/v1/decisions/{id}/
PATCH  /api/v1/decisions/{id}/
DELETE /api/v1/decisions/{id}/
```

Users can access only their own decisions.

Status: Implemented

### Criteria

```text
POST   /api/v1/decisions/{id}/criteria/
GET    /api/v1/decisions/{id}/criteria/
PATCH  /api/v1/criteria/{id}/
DELETE /api/v1/criteria/{id}/
```

Criterion weights must satisfy:

```text
0 < weight <= 1
```

The total weight must equal exactly `1` at evaluation time.

Status: Implemented

### Options

```text
POST   /api/v1/decisions/{id}/options/
GET    /api/v1/decisions/{id}/options/
PATCH  /api/v1/options/{id}/
DELETE /api/v1/options/{id}/
```

Status: Implemented

### Scores

```text
PUT    /api/v1/options/{option_id}/scores/{criterion_id}/
```

The endpoint creates or updates the score for a specific option/criterion pair.

Score constraints:

```text
0 <= score <= 10
```

Scores support at most two decimal places.

Status: Implemented

### Evaluation

```text
POST   /api/v1/decisions/{id}/evaluate/
GET    /api/v1/decisions/{id}/evaluate/
```

Both endpoints return the deterministic evaluation result.

Status: Implemented

### OpenAPI / Swagger

```text
GET    /api/schema/
GET    /api/docs/
```

The OpenAPI schema is generated with `drf-spectacular`.

Status: Implemented

## Evaluation Model

### Weight Constraints

```text
0 < weight <= 1
Σ weight_i = 1
```

Criterion weights may be entered incrementally. At evaluation time, the sum of all criterion weights for the decision must equal exactly `1`.

### Score Constraints

```text
0 <= score <= 10
```

Scores may contain at most two decimal places.

### Final Score

```text
FinalScore(option) = Σ(weight_i × score_i)
```

### Contribution

```text
Contribution_i = weight_i × score_i
```

Domain calculations use `Decimal` arithmetic.

Intermediate calculation values are not rounded before aggregation. Rounding is applied only for presentation.

### Ranking

```text
ORDER BY FinalScore DESC
```

Options are ranked from highest final score to lowest.

### Tie

Equal final scores receive the same rank.

No artificial winner is selected.

When the highest-ranked options are tied:

```json
{
  "winner_option_id": null,
  "is_tie": true
}
```

### Missing Scores

Every option must have a score for every criterion before evaluation.

Incomplete evaluations are rejected rather than treating missing scores as zero.

## Example

Consider two criteria:

```text
Cost     weight = 0.60
Quality  weight = 0.40
```

For an option with:

```text
Cost     score = 8.00
Quality  score = 9.00
```

The final score is:

```text
(0.60 × 8.00) + (0.40 × 9.00) = 8.40
```

## Tech Stack

* Python 3.12
* Django 6.1.1
* Django REST Framework 3.18.1
* PostgreSQL 17
* django-environ 0.14.0
* Psycopg 3.3.5
* SimpleJWT 5.5.1
* drf-spectacular 0.30.0
* Docker
* Docker Compose
* Railway — Planned

## Architecture

The project uses a modular monolith architecture.

```text
HTTP Request
      ↓
DRF View / ViewSet
      ↓
Serializer / Validation
      ↓
Service Layer
      ↓
Django ORM
      ↓
PostgreSQL
```

Business logic is kept out of large views. Meaningful application logic, especially evaluation, is implemented in the service layer.

## Running Locally

### Prerequisites

* Python 3.12
* Docker
* Docker Compose

### Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Docker Compose

```powershell
docker compose up -d --build
```

### Database migrations

```powershell
docker compose exec web python manage.py migrate
```

### Health check

```text
http://127.0.0.1:8000/health/
```

### Swagger UI

```text
http://127.0.0.1:8000/api/docs/
```

### OpenAPI schema

```text
http://127.0.0.1:8000/api/schema/
```

## Testing

The project uses Django's test framework with Django REST Framework API tests.

Run the complete test suite inside Docker:

```powershell
docker compose run --rm web python manage.py test apps.accounts apps.decisions -v 2
```

The current test suite covers authentication, decision ownership, criteria, options, scores, evaluation, incomplete scores, weight validation, ranking, and ties.

## Deployment

The target production platform is Railway.

```text
GitHub
   ↓
Railway
   ├── Django Web Service
   └── PostgreSQL
```

Deployment verification remains planned.

## Project Status

Core application functionality is implemented:

* Authentication
* Decision management
* Criteria management
* Option management
* Score management
* Deterministic weighted evaluation
* Ranking and tie handling
* OpenAPI / Swagger
* Automated tests
* Dockerized development environment

Remaining work is focused on final quality checks, documentation polish, production configuration, and Railway deployment.

## License

TBD
