# Expense Tracker API

[![Tests](https://github.com/j3ny0k/expense-tracker-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/j3ny0k/expense-tracker-api/actions/workflows/ci.yml)

A REST API for managing expenses, built with **Python, Flask, SQLite, pytest, and Waitress**.

The project demonstrates an end-to-end backend workflow:

- authenticated expense CRUD with `X-API-Key`;
- filtering by category, name, and amount;
- sorting and pagination;
- `X-Total-Count` metadata;
- SQL aggregation for totals by category;
- SQL query for the largest expense;
- input validation and controlled HTTP errors;
- configurable SQLite persistence through `DATABASE_PATH`;
- 84 automated API and database tests;
- GitHub Actions CI;
- production-style startup with Waitress;
- HTTP smoke testing.

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

# API

## Health check

```http
GET /health
```

The health endpoint is public and does not require an API key.

Successful response:

```text
200 OK
```

```json
{
  "status": "ok"
}
```

---

## Authentication

All `/expenses` endpoints require an API key.

The client must send it using the `X-API-Key` header:

```http
X-API-Key: your-api-key
```

The server reads the expected key from the `API_KEY` environment variable.

If the server key is missing, the client key is missing, or the key is incorrect:

```text
401 Unauthorized
```

```json
{
  "error": "unauthorized"
}
```

Example PowerShell configuration:

```powershell
$env:API_KEY = "local-development-key"
```

Do not store real API keys in the repository, README, source code, or committed `.env` files.

---

## Create an expense

```http
POST /expenses
```

Request body:

```json
{
  "amount": 100.0,
  "category": "food",
  "name": "pizza"
}
```

Successful response:

```text
201 Created
```

```json
{
  "id": 1,
  "amount": 100.0,
  "category": "food",
  "name": "pizza"
}
```

Required fields:

- `amount`;
- `category`;
- `name`.

Invalid input returns:

```text
400 Bad Request
```

---

## Get expenses

```http
GET /expenses
```

Successful response:

```text
200 OK
```

Example:

```json
[
  {
    "id": 1,
    "amount": 100.0,
    "category": "food",
    "name": "pizza"
  }
]
```

An empty database returns:

```json
[]
```

### Filters

Supported query parameters:

- `category` — exact category filter;
- `name` — exact name filter;
- `min_amount` — minimum amount;
- `max_amount` — maximum amount.

Examples:

```http
GET /expenses?category=food
GET /expenses?name=pizza
GET /expenses?min_amount=100
GET /expenses?max_amount=500
GET /expenses?min_amount=100&max_amount=500
GET /expenses?category=food&min_amount=100
```

When multiple filters are provided, an expense must match all of them.

`min_amount` and `max_amount` must be valid finite numbers.

If `min_amount` is greater than `max_amount`, the API returns:

```text
400 Bad Request
```

### Sorting

Supported values:

```text
sort=amount_asc
sort=amount_desc
```

Examples:

```http
GET /expenses?sort=amount_asc
GET /expenses?sort=amount_desc
```

`amount_asc` sorts from the smallest amount to the largest.

`amount_desc` sorts from the largest amount to the smallest.

Unknown sort values return:

```text
400 Bad Request
```

### Pagination

Supported parameters:

- `limit` — maximum number of expenses to return;
- `offset` — number of matching expenses to skip.

Examples:

```http
GET /expenses?limit=2
GET /expenses?limit=2&offset=1
```

`limit` must be greater than `0`.

`offset` must be greater than or equal to `0`.

`offset` can only be used together with `limit`.

Filtering, sorting, and pagination can be combined:

```http
GET /expenses?category=food&sort=amount_desc&limit=2&offset=1
```

### X-Total-Count

Successful `GET /expenses` responses include:

```text
X-Total-Count
```

The header contains the total number of matching expenses **after filtering but before pagination**.

Example:

```text
X-Total-Count: 4
```

A request such as:

```http
GET /expenses?category=food&limit=1
```

may therefore return one JSON object while `X-Total-Count` reports several matching expenses.

---

## Get one expense

```http
GET /expenses/<id>
```

Successful response:

```text
200 OK
```

Example:

```json
{
  "id": 1,
  "amount": 100.0,
  "category": "food",
  "name": "pizza"
}
```

If the expense does not exist:

```text
404 Not Found
```

```json
{
  "error": "expense not found"
}
```

---

## Totals by category

```http
GET /expenses/totals
```

Returns the total expense amount for each category.

The aggregation is performed directly in SQLite using `GROUP BY` and `SUM`.

Example:

```json
{
  "food": 400.0,
  "transport": 600.0
}
```

An empty database returns:

```json
{}
```

---

## Total expenses

```http
GET /expenses/total
```

Returns the total amount of all expenses.

The total is calculated directly in SQLite using `SUM`.

Example:

```json
{
  "total": 350.0
}
```

An empty database returns:

```json
{
  "total": 0
}
```

---

## Largest expense

```http
GET /expenses/largest
```

Returns the expense with the largest amount.

The largest expense is selected directly in SQLite using sorting and `LIMIT 1`.

Example:

```json
{
  "id": 1,
  "amount": 500.0,
  "category": "food",
  "name": "pizza"
}
```

If several expenses have the same largest amount, the expense with the smallest `id` is returned.

An empty database returns:

```json
null
```

---

## Update an expense

```http
PATCH /expenses/<id>
```

Only fields included in the request are updated.

Example:

```json
{
  "amount": 200.0,
  "name": "dinner"
}
```

Allowed fields:

```text
amount
category
name
```

Fields that are not provided remain unchanged.

Successful response:

```text
200 OK
```

Invalid values, unknown fields, or an empty update return:

```text
400 Bad Request
```

If the expense does not exist:

```text
404 Not Found
```

---

## Delete one expense

```http
DELETE /expenses/<id>
```

Successful deletion:

```text
204 No Content
```

If the expense does not exist:

```text
404 Not Found
```

---

## Delete all expenses

```http
DELETE /expenses
```

Successful response:

```text
204 No Content
```

---

# Database layer

SQLite access is implemented in `db.py`.

Main functions:

```python
init_db()

create_expense(amount, category, name)

get_expenses(
    category=None,
    name=None,
    min_amount=None,
    max_amount=None,
    sort=None,
    limit=None,
    offset=None,
)

get_expense_by_id(expense_id)

calculate_totals_by_category()

calculate_total_by_amount()

get_largest_expense()

update_expense(expense_id, amount, category, name)

delete_expense(expense_id)

delete_expenses()

count_expenses(
    category=None,
    name=None,
    min_amount=None,
    max_amount=None,
)
```

## Query behavior

`get_expenses()` performs filtering, sorting, and pagination directly in SQLite.

Filtering conditions use SQL parameters rather than inserting user values directly into the query.

`count_expenses()` applies the same filters used by `GET /expenses` and returns the number of matching rows before pagination.

`calculate_totals_by_category()` uses SQL aggregation:

```sql
GROUP BY category
SUM(amount)
```

`get_largest_expense()` orders expenses by:

```text
amount descending
id ascending
```

and uses:

```sql
LIMIT 1
```

to return only the required row.

`get_expense_by_id()` returns one expense or `None`.

`update_expense()` supports partial updates.

`delete_expense()` returns:

```text
True  - one expense was deleted
False - the expense did not exist
```

---

# Validation

Input validation is implemented before values are written through the API.

The project validates that:

- `amount` is an `int` or `float`;
- boolean values are not accepted as amounts;
- `amount` is greater than `0`;
- `amount` must be a finite number;
- `category` is a non-empty string;
- `name` is a non-empty string.

Whitespace around `category` and `name` is removed before values are stored through the API.

Amount filters are converted to numbers before they are passed to the database layer.

Invalid query parameters return controlled `400 Bad Request` responses instead of being passed directly into SQL.

---

# Tests

The project uses `pytest`.

Current test suite:

```text
84 passed
```

Tests are split into:

```text
tests/test_app.py
tests/test_db.py
```

Database and API tests use temporary SQLite databases, so running the tests does not modify the normal application database.

The suite covers:

- database initialization;
- creating expenses;
- reading one or many expenses;
- empty database behavior;
- filtering by category and name;
- minimum and maximum amount filters;
- combined filters;
- sorting;
- pagination;
- invalid pagination parameters;
- `X-Total-Count`;
- totals by category;
- largest-expense selection;
- equal largest amounts and deterministic `id` tie-breaking;
- partial updates;
- deleting one expense;
- repeated deletion;
- deleting all expenses;
- API authentication;
- POST validation;
- PATCH validation;
- 404 responses;
- public health endpoint.

Run the complete suite:

```bash
python -m pytest -q
```

---

# Continuous integration

The repository contains a GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

CI runs the automated test suite, starts the API with Waitress, waits for the health endpoint, and runs the HTTP smoke test.

---

# Smoke test

`smoke.py` performs HTTP checks against a running instance of the API.

It verifies:

- public `GET /health`;
- unauthorized access without an API key;
- authenticated expense creation;
- reading the created expense;
- updating the created expense with PATCH;
- reading the updated expense;
- deleting the expense created by the smoke test.

The script uses:

```text
SMOKE_BASE_URL
API_KEY
```

Example PowerShell configuration:

```powershell
$env:SMOKE_BASE_URL = "http://127.0.0.1:8000"
$env:API_KEY = "local-development-key"

python smoke.py
```

The smoke test does not delete all expenses.

If cleanup is required, it deletes only the expense created by that smoke run.

---

# Running locally

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Configure the API key

PowerShell:

```powershell
$env:API_KEY = "local-development-key"
```

## Development server

```bash
python app.py
```

The application initializes the SQLite database and starts the Flask development server.

---

# Production-style startup

The application can be served with Waitress:

```bash
waitress-serve wsgi:app
```

`wsgi.py` initializes the database before exposing the Flask application to Waitress.

---

# Database persistence

By default, the API uses:

```text
expenses.db
```

A different SQLite file can be selected with:

```text
DATABASE_PATH
```

Example in PowerShell:

```powershell
$env:DATABASE_PATH = "custom-expenses.db"
waitress-serve wsgi:app
```

If `DATABASE_PATH` is not set, the application falls back to:

```text
expenses.db
```

Using the same database path across application restarts preserves stored expenses.

---

# Environment variables

| Variable         | Purpose                                              |
| ---------------- | ---------------------------------------------------- |
| `API_KEY`        | Expected API key for protected `/expenses` endpoints |
| `DATABASE_PATH`  | Path to the SQLite database file                     |
| `SMOKE_BASE_URL` | Base URL used by `smoke.py`                          |

Do not commit real secrets or production credentials.

---

# Project structure

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

## Files

`app.py`
: Flask routes, request validation, authentication, and HTTP responses.

`db.py`
: SQLite persistence, filtering, sorting, pagination, counting, aggregation, and largest-expense queries.

`expense_logic.py`
: reusable validation helpers.

`wsgi.py`
: application entry point for Waitress.

`smoke.py`
: HTTP smoke checks against a running API.

`tests/test_app.py`
: API-level behavior.

`tests/test_db.py`
: database-layer behavior.

`.github/workflows/ci.yml`
: GitHub Actions CI configuration.

---

# Current capabilities

The API currently supports:

```text
health
authentication
create
read
update
delete
bulk delete
filtering
amount ranges
sorting
pagination
total-count metadata
totals by category
total expenses
largest expense
SQLite persistence
automated tests
CI
HTTP smoke testing
Waitress startup
```
