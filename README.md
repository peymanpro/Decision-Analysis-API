# Decision Analysis API

A small REST API for structured decision analysis and weighted evaluation.

## Overview

Decision Analysis API allows authenticated users to create decisions, define criteria and options, assign criterion weights, score options, and obtain a deterministic weighted evaluation with ranking and explainable criterion contributions.

## Scope

The initial domain consists of:

- User
- Decision
- Criterion
- Option
- Score

```text
Decision
 ├── Criteria
 └── Options
       └── Scores
```

Each decision belongs to one user.

## Features

- JWT authentication — Planned
- Decision management — Planned
- Criterion management — Planned
- Option management — Planned
- Score management — Planned
- Weighted evaluation — Planned
- Ranking and tie handling — Planned
- Explainable criterion contributions — Planned
- OpenAPI / Swagger — Planned
- PostgreSQL — Planned
- Docker — In Progress
- Railway deployment — Planned

## API

Base path:

```text
/api/v1/
```

### Authentication

```text
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/
POST   /api/v1/auth/refresh/
```

Status: Planned

### Decisions

```text
POST   /api/v1/decisions/
GET    /api/v1/decisions/
GET    /api/v1/decisions/{id}/
PATCH  /api/v1/decisions/{id}/
DELETE /api/v1/decisions/{id}/
```

Status: Planned

### Criteria

```text
POST   /api/v1/decisions/{id}/criteria/
GET    /api/v1/decisions/{id}/criteria/
PATCH  /api/v1/criteria/{id}/
DELETE /api/v1/criteria/{id}/
```

Status: Planned

### Options

```text
POST   /api/v1/decisions/{id}/options/
GET    /api/v1/decisions/{id}/options/
PATCH  /api/v1/options/{id}/
DELETE /api/v1/options/{id}/
```

Status: Planned

### Scores

```text
PUT    /api/v1/options/{option_id}/scores/{criterion_id}/
```

Status: Planned

### Evaluation

```text
POST   /api/v1/decisions/{id}/evaluate/
GET    /api/v1/decisions/{id}/result/
```

Status: Planned

## Evaluation Model

### Weight Constraints

```text
0 < weight <= 1
Σ weight_i = 1
```

Criterion weights may be entered incrementally. At evaluation time, the sum of all criterion weights for the decision must equal exactly 1.

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

Domain calculations use Decimal arithmetic. Intermediate values are not rounded before aggregation; rounding is applied only for presentation.

### Ranking

```text
ORDER BY FinalScore DESC
```

Options are ranked from highest final score to lowest.

### Tie

Equal final scores receive the same rank. No artificial winner is selected.

When the highest-ranked options are tied:

```json
{
  "winner": null,
  "is_tie": true
}
```

### Missing Scores

Every option must have a score for every criterion before evaluation.

Incomplete evaluations are rejected rather than treating missing scores as zero.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT
- pytest
- Docker
- Railway

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

Business logic is kept out of large views. Services are used for meaningful application use cases such as evaluation.

## Running Locally

### Prerequisites

- Python 3.12
- Docker
- Docker Compose

### Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Django

```powershell
python manage.py runserver
```

PostgreSQL configuration and Docker-based local development will be completed during the implementation phases.

## Testing

pytest and pytest-django configuration will be added in the testing phase.

## Swagger / OpenAPI

OpenAPI schema and Swagger UI will be added during implementation.

## Deployment

The target production platform is Railway.

```text
GitHub
   ↓
Railway
   ├── Django Web Service
   └── PostgreSQL
```

Production and Swagger URLs will be added after deployment verification.

## Project Status

Bootstrap / In Progress

The domain model and API are not implemented yet.

## License

TBD
