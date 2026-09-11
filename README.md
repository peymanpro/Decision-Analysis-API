# Decision Analysis API

## Overview

Decision Analysis API is a REST API for structured decision analysis and weighted evaluation. It enables users to define decisions, establish evaluation criteria, score available options, and receive ranked results based on weighted scoring logic.

## Features

- User registration and JWT-based authentication
- User-owned decision hierarchies
- CRUD operations for decisions, criteria, and options
- Score management and validation
- Weighted decision evaluation with deterministic results
- Ranking calculation and automatic winner detection
- Tie detection and handling
- Criterion contribution analysis
- OpenAPI/Swagger documentation
- Comprehensive test coverage

## Domain Model

```
Decision
├── Criteria (weighted evaluation dimensions)
└── Options (alternative choices)
    └── Scores (option/criterion pairs)
```

Each decision belongs to one user. Users can only access their own resources. Each option/criterion pair has at most one score. Evaluation requires complete scoring data.

## API

**Base URL:** `/api/v1/`

### Authentication

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/register/` | User registration |
| POST | `/auth/token/` | Obtain JWT token |
| POST | `/auth/token/refresh/` | Refresh access token |

### Decisions

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/decisions/` | Create decision |
| GET | `/decisions/` | List user decisions |
| GET | `/decisions/{id}/` | Retrieve decision |
| PATCH | `/decisions/{id}/` | Update decision |
| DELETE | `/decisions/{id}/` | Delete decision |

### Criteria

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/decisions/{id}/criteria/` | Create criterion |
| GET | `/decisions/{id}/criteria/` | List criteria |
| PATCH | `/criteria/{id}/` | Update criterion |
| DELETE | `/criteria/{id}/` | Delete criterion |

### Options

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/decisions/{id}/options/` | Create option |
| GET | `/decisions/{id}/options/` | List options |
| PATCH | `/options/{id}/` | Update option |
| DELETE | `/options/{id}/` | Delete option |

### Scores

| Method | Endpoint | Purpose |
|--------|----------|---------|
| PUT | `/options/{option_id}/scores/{criterion_id}/` | Set or update score |

### Evaluation

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/decisions/{id}/evaluate/` | Execute weighted evaluation |
| GET | `/decisions/{id}/result/` | Retrieve evaluation results |

## Evaluation Model

The API performs weighted decision evaluation using the formula:

```
Final Score = (weight₁ × score₁) + (weight₂ × score₂) + ... + (weightₙ × scoreₙ)
```

Evaluation output includes:
- Individual weighted scores for each option
- Ranked options from highest to lowest score
- Automatically detected winner
- Tie detection when multiple options share the highest score
- Criterion contribution percentages

## Architecture

Decision Analysis API follows a modular monolith architecture:

```
HTTP Request
    ↓
DRF Views / ViewSets
    ↓
Serializers / Validation
    ↓
Service Layer
    ↓
Django ORM
    ↓
PostgreSQL
```

The service layer encapsulates business logic and evaluation algorithms, while views handle HTTP concerns. All resources are user-scoped through authentication middleware.

## Tech Stack

- **Language:** Python 3
- **Framework:** Django + Django REST Framework
- **Database:** PostgreSQL with Django ORM
- **Authentication:** JWT (JSON Web Tokens)
- **API Documentation:** OpenAPI 3.0 / Swagger
- **Testing:** pytest
- **Containerization:** Docker & Docker Compose

## Running Locally

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd decision-analysis-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```
   cp .env.example .env
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/v1/`.

## Swagger / OpenAPI

Interactive API documentation is available at:
- **Swagger UI:** `/api/docs/`
- **OpenAPI Schema:** `/api/schema/`

## Testing

Run the test suite with pytest:

```
pytest
```

Run with coverage:

```
pytest --cov
```

## Docker

A Docker Compose configuration is provided for local development.

### Build and run services:

```
docker-compose up -d
```

Services:
- **Django application:** Runs on `http://localhost:8000`
- **PostgreSQL database:** Configured in `docker-compose.yml`

To stop services:

```
docker-compose down
```

## Project Status

Completed. The API is production-ready for deployment on your own infrastructure.

## License

See LICENSE file for details.
