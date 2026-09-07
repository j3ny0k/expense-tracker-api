# Expense Tracker API

A small REST API for managing expenses, built with **Python, Flask, SQLite, and pytest**.

The project includes:

- expense validation;
- SQLite persistence;
- full expense CRUD;
- partial updates with `PATCH`;
- HTTP error handling;
- isolated database and API tests;
- API key protection for expense endpoints.

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

## API

### Health check

```http
GET /health
```

Returns a simple liveness response without accessing the database.

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

## API authentication

All `/expenses` endpoints require an API key.

The client must send the key in the `X-API-Key` request header:

```http
X-API-Key: your-api-key
```

The server reads the expected key from the `API_KEY` environment variable.

If the header is missing or the key is incorrect, the API returns:

```text
401 Unauthorized
```

```json
{
  "error": "unauthorized"
}
```

`GET /health` does not require an API key.

### Local configuration

Example in PowerShell:

```powershell
$env:API_KEY = "local-development-key"
python app.py
```

For production, configure `API_KEY` as an environment variable on the deployment platform.

Do not store the real production API key in the repository, README, source code, or committed `.env` files.

---

### Create an expense

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

`amount`, `category`, and `name` are required.

Invalid input returns:

```text
400 Bad Request
```

---

### Get all expenses

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

Optional query parameters:

- `category` — filter expenses by category;
- `name` — filter expenses by name;
- `min_amount` — filter expenses with amount greater than or equal to this value;
- `max_amount` — filter expenses with amount less than or equal to this value;
- `limit` — maximum number of expenses to return;
- `offset` — number of expenses to skip; requires `limit`;
- `sort=amount_asc` — sort expenses by amount from lowest to highest;
- `sort=amount_desc` — sort expenses by amount from highest to lowest.

Examples:

```http
GET /expenses?category=food
GET /expenses?name=pizza
GET /expenses?category=food&name=pizza
GET /expenses?min_amount=100
GET /expenses?max_amount=500
GET /expenses?min_amount=100&max_amount=500
GET /expenses?category=food&min_amount=100
GET /expenses?limit=2
GET /expenses?limit=2&offset=1
GET /expenses?sort=amount_asc
GET /expenses?category=food&sort=amount_desc&limit=2
```

When multiple parameters are provided, an expense must match all of the specified filters.

`min_amount` and `max_amount` must be valid numbers.

Invalid amount filters return:

```text
400 Bad Request
```

If `min_amount` is greater than `max_amount`, the request also returns:

```text
400 Bad Request
```

Successful `GET /expenses` responses include the `X-Total-Count` header.

It contains the number of expenses after filtering and before pagination.

Example:

```text
X-Total-Count: 3
```

---

### Get one expense

```http
GET /expenses/<id>
```

Successful response:

```text
200 OK
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

### Get totals by category

```http
GET /expenses/totals
```

Returns the total expense amount for each category.

Successful response:

```text
200 OK
```

Example:

```json
{
  "food": 400.0,
  "transport": 600.0
}
```

If there are no expenses, the response is:

```json
{}
```

---

### Get largest expense

```http
GET /expenses/largest
```

Returns the expense with the largest amount.

Successful response:

```text
200 OK
```

Example:

```json
{
  "id": 2,
  "amount": 200.0,
  "category": "transport",
  "name": "bus"
}
```

If there are no expenses, the response is:

```json
null
```

---

### Update an expense

```http
PATCH /expenses/<id>
```

Only the fields included in the request are updated.

Example:

```json
{
  "amount": 200.0,
  "name": "dinner"
}
```

Fields that are not included remain unchanged.

Allowed fields:

```text
amount
category
name
```

Successful response:

```text
200 OK
```

Invalid values, an empty update, or unknown fields return:

```text
400 Bad Request
```

A missing expense returns:

```text
404 Not Found
```

---

### Delete one expense

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

### Delete all expenses

```http
DELETE /expenses
```

Successful response:

```text
204 No Content
```

## Database layer

Main functions in `db.py`:

```python
init_db()

create_expense(amount, category, name)

get_expenses()

get_expense_by_id(expense_id)

update_expense(expense_id, amount, category, name)

delete_expense(expense_id)

delete_expenses()
```

`get_expenses()` returns expenses ordered by `id` as dictionaries.

`update_expense()` supports partial updates: fields passed as `None` are left unchanged.

`delete_expense()` returns:

```text
True  - one expense was deleted
False - the expense did not exist
```

## Validation

The project validates:

- `amount` is an `int` or `float`;
- booleans are not accepted as amounts;
- `amount` must be greater than `0`;
- `category` must be a non-empty string;
- `name` must be a non-empty string.

Whitespace around `category` and `name` is removed before values are stored through the API.

## Tests

The project uses `pytest`.

Tests are split into:

```text
tests/test_expense_logic.py
tests/test_db.py
tests/test_app.py
```

Database and API tests use temporary SQLite databases, so the normal project database is not modified during testing.

The test suite covers:

- expense calculation logic;
- input validation behavior;
- database initialization;
- creating and reading expenses;
- partial expense updates;
- deleting expenses;
- repeated deletion;
- empty database behavior;
- GET success and 404 responses;
- POST success and validation errors;
- PATCH success, invalid requests, unknown fields, and missing expenses;
- DELETE success and missing expenses;
- deleting all expenses;
- filtering expenses by `category` and `name` query parameters;
- calculating expense totals by category through `GET /expenses/totals`;
- finding the largest expense through `GET /expenses/largest`;
- filtering expenses by `min_amount` and `max_amount` query parameters;
- pagination with `limit` and `offset`;
- sorting expenses by amount;
- `X-Total-Count` behavior with filters and pagination;
- API key authentication for protected expense endpoints;
- liveness check through `GET /health`.

## Run the tests

From the project directory:

```bash
python -m pytest -q
```

## Run the smoke test

The smoke test checks a running deployment through HTTP.

It verifies:

- public `GET /health`;
- `401 Unauthorized` for `GET /expenses` without an API key;
- authenticated expense creation;
- reading the created expense by its ID;
- deleting only the expense created by the smoke test.

The smoke test reads its target and API key from the `SMOKE_BASE_URL` and `API_KEY` environment variables.

Set both variables in your shell, then run:

```bash
python smoke.py
```

The script does not use bulk deletion. If a failure happens after creating the test expense, it attempts to delete only that expense.

## Run the API

Install the dependencies used by the project:

```bash
python -m pip install -r requirements.txt
```

### Development

Start the application with the Flask development server:

```bash
python app.py
```

The application initializes the SQLite database and starts the Flask development server.

### Production

Start the application with Waitress:

```bash
waitress-serve wsgi:app
```

`wsgi.py` initializes the SQLite database before exposing the Flask application to Waitress.

### Database path

By default, the application uses:

```text
expenses.db
```

The database path can be configured with the `DATABASE_PATH` environment variable.

Example in PowerShell:

```powershell
$env:DATABASE_PATH = "custom-expenses.db"
waitress-serve wsgi:app
```

If `DATABASE_PATH` is not set, the application falls back to `expenses.db`.

## Project structure

```text
expense-tracker-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app.py
├── db.py
├── expense_logic.py
├── requirements.txt
├── README.md
├── smoke.py
├── wsgi.py
└── tests/
    ├── test_app.py
    ├── test_db.py
    └── test_expense_logic.py
```
