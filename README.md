# Expense Tracker API

[![Tests](https://github.com/j3ny0k/expense-tracker-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/j3ny0k/expense-tracker-api/actions/workflows/ci.yml)

REST API for expense tracking built with **Python, Flask, SQLite, pytest, and Waitress**.

## Highlights

- API-key authentication with `X-API-Key`
- expense CRUD and bulk delete
- filtering by category, name, and amount range
- sorting and pagination with `X-Total-Count`
- SQL aggregation for category totals and total expenses
- largest-expense query with deterministic tie-breaking
- configurable SQLite persistence
- 87 automated tests
- GitHub Actions CI with runtime HTTP smoke testing
- production-style startup with Waitress

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
| GET    | `/health`           | Health check                              |
| GET    | `/expenses`         | List, filter, sort, and paginate expenses |
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
- `limit`
- `offset`

Filtering, sorting, and pagination can be combined.

Successful list responses include `X-Total-Count`, which reports the number of matching expenses before pagination.

## Authentication

`/health` is public.

All `/expenses` endpoints require an API key in the `X-API-Key` header:

```http
X-API-Key: your-api-key
```

The expected key is read from the `API_KEY` environment variable.

## Implementation

SQLite access is implemented in `db.py`.

Filtering, sorting, pagination, counting, and aggregations are performed directly in SQLite using parameterized queries.

The API validates input before values are passed to the database layer.

## Testing and CI

The project uses `pytest`.

Current test suite:

```text
87 passed
```

Tests cover API behavior, validation, authentication, database operations, filtering, sorting, pagination, aggregations, updates, and deletion.

Run the suite:

```bash
python -m pytest -q
```

GitHub Actions runs:

1. the full pytest suite;
2. the API with Waitress;
3. a `/health` readiness check;
4. `smoke.py` against the running API.

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

## Environment variables

| Variable         | Purpose                                     |
| ---------------- | ------------------------------------------- |
| `API_KEY`        | API key for protected `/expenses` endpoints |
| `DATABASE_PATH`  | Path to the SQLite database                 |
| `SMOKE_BASE_URL` | Base URL used by `smoke.py`                 |

Do not commit real secrets or production credentials.

## Project structure

```text
expense-tracker-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
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
