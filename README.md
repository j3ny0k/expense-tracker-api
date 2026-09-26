# Expense Tracker API

[![Tests](https://github.com/j3ny0k/expense-tracker-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/j3ny0k/expense-tracker-api/actions/workflows/ci.yml)

REST API for expense tracking built with **Python, Flask, SQLite/PostgreSQL, pytest, and Waitress**.

## Highlights

- API-key authentication with `X-API-Key`
- expense CRUD and bulk delete
- filtering by category, name, and amount range
- sorting and pagination with `X-Total-Count`
- SQL aggregation for category totals and total expenses
- largest-expense query with deterministic tie-breaking
- SQLite by default with optional PostgreSQL via `DATABASE_URL`
- 91 automated tests
- GitHub Actions CI with runtime HTTP smoke testing
- production-style startup with Waitress
- Dockerized application runtime

## Expense structure

Each expense contains:

```json
{
  "id": 1,
  "amount": 100.0,
  "category": "food",
  "name": "pizza"
}
```

SQLite table:

```sql
expenses (
    id INTEGER PRIMARY KEY,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    name TEXT NOT NULL
)
```

---

## API

| Method | Endpoint            | Description                               |
| ------ | ------------------- | ----------------------------------------- |
| GET    | `/ready`            | Readiness check for database connectivity |
| GET    | `/health`           | Health check                              |
| GET    | `/expenses`         | List, filter, sort, and paginate expenses |
| GET    | `/expenses/summary` | Count, total amount, and largest expense  |
| POST   | `/expenses`         | Create an expense                         |
| GET    | `/expenses/<id>`    | Get one expense                           |
| PATCH  | `/expenses/<id>`    | Update an expense                         |
| DELETE | `/expenses/<id>`    | Delete one expense                        |
| DELETE | `/expenses`         | Delete all expenses                       |
| GET    | `/expenses/totals`  | Totals grouped by category                |
| GET    | `/expenses/total`   | Total amount of all expenses              |
| GET    | `/expenses/largest` | Largest expense                           |

## Query parameters

`GET /expenses` supports:

- `category`
- `name`
- `name_contains`
- `min_amount`
- `max_amount`
- `sort=amount_asc`
- `sort=amount_desc`
- `sort=name_asc`
- `sort=name_desc`
- `sort=category_asc`
- `sort=category_desc`
- `limit`
- `offset`

Filtering, sorting, and pagination can be combined.

Successful list responses include `X-Total-Count`, which reports the number of matching expenses before pagination.

## Authentication

`/health` and `/ready` are public.

All `/expenses` endpoints require an API key in the `X-API-Key` header:

```http
X-API-Key: your-api-key
```

The expected key is read from the `API_KEY` environment variable.

## Implementation

Database access is implemented in `db.py`.

SQLite is used by default. If `DATABASE_URL` is set, the application connects to PostgreSQL instead.

Filtering, sorting, pagination, counting, and aggregations are performed directly in the database using parameterized queries.

## Testing and CI

The project uses `pytest`.

Current test suite:

```text
91 passed
```

Tests cover API behavior, validation, authentication, database operations, filtering, sorting, pagination, aggregations, updates, and deletion.

Run the suite:

```bash
python -m pytest -q
```

GitHub Actions runs:

1. the full pytest suite;
2. builds the Docker image;
3. starts the API container;
4. checks `/health`;
5. runs `smoke.py` against the containerized API.

The runtime smoke test verifies authentication and a real create → read → update → delete flow.

---

## Running locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Set the API key in PowerShell:

```powershell
$env:API_KEY = "local-development-key"
```

Start the Flask development server:

```bash
python app.py
```

By default, the API stores data in `expenses.db`.

A different SQLite database can be selected with `DATABASE_PATH`:

```powershell
$env:DATABASE_PATH = "custom-expenses.db"
```

Using the same database path across restarts preserves stored expenses.

### Production-style startup

Run the application with Waitress:

```bash
waitress-serve wsgi:app
```

`wsgi.py` initializes the database before exposing the Flask application.

### Docker

Build the image:

```bash
docker build -t expense-tracker-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 -e API_KEY=local-development-key expense-tracker-api
```

Check the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

The API is served by Waitress on port `8000` inside the container.

### Docker Compose

Run the application and PostgreSQL together:

```bash
docker compose up -d --build
```

Check the services:

```bash
docker compose ps
```

The application is available at:

```text
http://127.0.0.1:8000
```

Docker Compose starts:

- the API container;
- a PostgreSQL 17 container;
- a persistent PostgreSQL volume.

The API connects to PostgreSQL through the internal Compose hostname `db`.

Stop the stack:

```bash
docker compose down
```

The PostgreSQL volume is preserved, so stored expenses survive container recreation.

## Environment variables

| Variable         | Purpose                                     |
| ---------------- | ------------------------------------------- |
| `API_KEY`        | API key for protected `/expenses` endpoints |
| `DATABASE_PATH`  | Path to the SQLite database                 |
| `SMOKE_BASE_URL` | Base URL used by `smoke.py`                 |
| `DATABASE_URL`   | PostgreSQL connection URL                   |

Do not commit real secrets or production credentials.

## Project structure

```text
expense-tracker-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .dockerignore
├── .gitignore
├── Dockerfile
├── compose.yml
├── app.py
├── db.py
├── expense_logic.py
├── README.md
├── requirements.txt
├── smoke.py
├── wsgi.py
└── tests/
    ├── test_app.py
    └── test_db.py
```
