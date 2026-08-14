# Expense Tracker

A small Python project for working with expenses using pure Python logic and SQLite.

## Features

- validate expense amounts and categories;
- calculate totals by category;
- find the largest valid expense;
- initialize an SQLite database;
- create expenses in SQLite;
- read all expenses as `list[dict]`;
- get one expense by `id`;
- keep database tests isolated with temporary SQLite databases.

## Expense structure

Each expense contains:

```text
id
amount
category
name
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

## Main database functions

```python
init_db()
create_expense(amount, category, name)
get_expenses()
get_expense_by_id(expense_id)
```

`get_expenses()` returns expenses in ascending `id` order as dictionaries.

Example:

```python
[
    {
        "id": 1,
        "amount": 100.0,
        "category": "food",
        "name": "pizza",
    }
]
```

## Tests

The project uses `pytest`.

Database tests use temporary SQLite databases, so the normal project database is not modified during testing.

The tests cover:

- database initialization;
- repeated `init_db()` calls;
- SQLite table structure;
- creating an expense and returning its `id`;
- reading an empty database;
- reading one or multiple expenses;
- expense ordering by `id`;
- getting an expense by `id`;
- missing expense lookup;
- integration between SQLite data and pure Python expense logic.

## Run tests

```bash
python -m pytest -q
```
