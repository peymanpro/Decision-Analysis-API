# Decision Analysis API

A small Django REST API for structured decision analysis and deterministic weighted evaluation.

## Overview

Decision Analysis API allows authenticated users to create decisions, define criteria and options, assign criterion weights, score options, and obtain a deterministic weighted evaluation with ranking, tie handling, and explainable criterion contributions.

The project is intentionally small and focused on one core problem: turning a structured decision into a transparent, reproducible numerical evaluation.

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

Each decision belongs to one user, and users can access only their own decisions.

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
* Deterministic weighted evaluation — Implemented
* Ranking and tie handling — Implemented
* Explainable criterion contributions — Implemented
* OpenAPI / Swagger documentation — Implemented
* Automated tests — Implemented

## API

Base path:

```text
/api/v1/
```

### Health

```text
GET /health/
```

Returns the application health status.

Status: Implemented

### Authentication

```text
POST /api/v1/auth/register/
POST /api/v1/auth/token/
POST /api/v1/auth/token/refresh/
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

The total criterion weight must equal exactly `1` at evaluation time.

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
PUT /api/v1/options/{option_id}/scores/{criterion_id}/
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
POST /api/v1/decisions/{id}/evaluate/
GET  /api/v1/decisions/{id}/evaluate/
```

Both endpoints return the deterministic evaluation result.

Status: Implemented

### OpenAPI / Swagger

```text
GET /api/schema/
GET /api/docs/
```

The OpenAPI schema is generated with `drf-spectacular`.

Status: Implemented

## Evaluation Model

### Weight Constraints

Each criterion must satisfy:

$$
0 < weight_i \leq 1
$$

At evaluation time:

$$
\sum_{i=1}^{n} weight_i = 1
$$

Criterion weights may be entered incrementally. The final evaluation is accepted only when the total weight is exactly `1`.

### Score Constraints

Each score must satisfy:

$$
0 \leq score_i \leq 10
$$

Scores may contain at most two decimal places.

### Final Score

For an option:

$$
FinalScore(option) =
\sum_{i=1}^{n}
(weight_i \times score_i)
$$

### Criterion Contribution

For each criterion:

$$
Contribution_i =
weight_i \times score_i
$$

Domain calculations use Python `Decimal` arithmetic.

Intermediate calculation values are not rounded before aggregation. Rounding is applied only for presentation.

### Ranking

Options are ranked by descending final score:

$$
FinalScore_1 \geq FinalScore_2 \geq \dots \geq FinalScore_n
$$

### Tie Handling

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

An incomplete evaluation is rejected.

Missing scores are **never treated as zero**.

## Example

Consider two criteria:

```text
Cost       weight = 0.60
Quality    weight = 0.40
```

For an option with:

```text
Cost       score = 8.00
Quality    score = 9.00
```

The final score is:

$$
(0.60 \times 8.00) + (0.40 \times 9.00) = 8.40
$$

The criterion contributions are:

$$
Cost = 0.60 \times 8.00 = 4.80
$$

$$
Quality = 0.40 \times 9.00 = 3.60
$$

Therefore:

$$
FinalScore = 4.80 + 3.60 = 8.40
$$

## Tech Stack

* Python 3.12
* Django 6.1.1
* Django REST Framework 3.18.1
* PostgreSQL 17
* django-environ 0.14.0
* Psycopg 3.3.5
* PyJWT 2.13.0
* djangorestframework-simplejwt 5.5.1
* drf-spectacular 0.30.0
* Gunicorn 23.0.0
* Docker
* Docker Compose

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

Business logic is kept out of large views.

Meaningful application logic, especially the deterministic evaluation process, is implemented in the service layer.

The project deliberately avoids unnecessary distributed-system complexity such as microservices, message brokers, CQRS, event sourcing, or background workers.

## Run the Project Locally

The easiest way to use the project is:

**Fork → Clone → Configure → Run → Open Swagger**

### 1. Fork the repository

Open the GitHub repository and click **Fork**.

This creates your own copy of the project under your GitHub account.

### 2. Clone your fork

Clone your fork to your local machine:

```powershell
git clone https://github.com/YOUR_USERNAME/Decision-Analysis-API.git
cd Decision-Analysis-API
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3. Create the environment file

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

For local development, update `.env` as needed.

A typical local configuration is:

```text
SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
DATABASE_URL=postgresql://decision_user:change-me@localhost:5432/decision_analysis
```

Do not commit `.env` to Git.

### 4. Start the development environment

The project includes Docker Compose configuration for the application and PostgreSQL database.

```powershell
docker compose up -d --build
```

Check the running services:

```powershell
docker compose ps
```

### 5. Run database migrations

```powershell
docker compose exec web python manage.py migrate
```

### 6. Start Django

For a local development workflow similar to `npm start`, Django can run directly with its development server.

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Then run:

```powershell
python manage.py runserver 127.0.0.1:8000
```

The application will listen on:

```text
http://127.0.0.1:8000/
```

### 7. Check the API

Health endpoint:

```text
http://127.0.0.1:8000/health/
```

Swagger UI:

```text
http://127.0.0.1:8000/api/docs/
```

OpenAPI schema:

```text
http://127.0.0.1:8000/api/schema/
```

Swagger UI can be used to explore and execute the API endpoints interactively.

## Typical Usage Flow

A typical API workflow is:

```text
Register
   ↓
Obtain JWT access token
   ↓
Create Decision
   ↓
Create Criteria
   ↓
Assign Criterion Weights
   ↓
Create Options
   ↓
Assign Scores
   ↓
Evaluate Decision
   ↓
Read Ranking, Winner/Tie, and Contributions
```

The complete API can be explored through Swagger UI.

## Testing

The project uses Django's test framework together with Django REST Framework API tests.

Run the complete test suite:

```powershell
docker compose run --rm web python manage.py test apps.accounts apps.decisions -v 2
```

The test suite covers:

* Authentication
* Decision ownership
* Criteria
* Options
* Scores
* Weight validation
* Incomplete evaluations
* Deterministic evaluation
* Ranking
* Tie handling

## Project Status

The core application is implemented and usable locally.

Current functionality includes:

* JWT authentication
* Decision management
* Criteria management
* Option management
* Score management
* Deterministic weighted evaluation
* Ranking and tie handling
* Explainable criterion contributions
* OpenAPI / Swagger documentation
* Automated tests
* Dockerized local development

The project is currently intended to be run locally from a GitHub fork or clone.

## License

TBD
