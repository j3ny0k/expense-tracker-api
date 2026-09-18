import os
from sqlite3 import connect

DB_NAME = os.getenv("DATABASE_PATH", "expenses.db")


def get_connection():
    connection = connect(DB_NAME)
    return connection


def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            name TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_expense(amount, category, name):
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO expenses (amount, category, name) VALUES (?, ?, ?)",
        (amount, category, name),
    )

    connection.commit()

    expense_id = cursor.lastrowid

    connection.close()

    return expense_id


def get_expenses(
    category=None,
    name=None,
    min_amount=None,
    max_amount=None,
    sort=None,
    limit=None,
    offset=None,
):
    connection = get_connection()

    conditions = []
    params = []

    if category is not None:
        conditions.append("category = ?")
        params.append(category)

    if name is not None:
        conditions.append("name = ?")
        params.append(name)

    if min_amount is not None:
        conditions.append("amount >= ?")
        params.append(min_amount)

    if max_amount is not None:
        conditions.append("amount <= ?")
        params.append(max_amount)

    sql = "SELECT id, amount, category, name FROM expenses"

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    if sort == "amount_asc":
        sql += " ORDER BY amount ASC"
    elif sort == "amount_desc":
        sql += " ORDER BY amount DESC"
    else:
        sql += " ORDER BY id ASC"

    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)

        if offset is not None:
            sql += " OFFSET ?"
            params.append(offset)

    cursor = connection.execute(sql, params)

    expenses = []

    raws = cursor.fetchall()

    for raw in raws:
        result = {}

        result["id"] = raw[0]
        result["amount"] = raw[1]
        result["category"] = raw[2]
        result["name"] = raw[3]

        expenses.append(result)

    connection.close()

    return expenses


def get_expense_by_id(expense_id):
    connection = get_connection()

    cursor = connection.execute(
        "SELECT id, amount, category, name FROM expenses WHERE id = ?", (expense_id,)
    )

    raw = cursor.fetchone()

    expense = None

    if raw is not None:
        expense = {}

        expense["id"] = raw[0]
        expense["amount"] = raw[1]
        expense["category"] = raw[2]
        expense["name"] = raw[3]

    connection.close()

    return expense


def calculate_totals_by_category():
    connection = get_connection()

    cursor = connection.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    )

    raw = cursor.fetchall()

    totals = {}

    for category, amount in raw:
        totals[category] = amount

    connection.close()

    return totals


def update_expense(expense_id, amount, category, name):
    connection = get_connection()

    if amount is not None:
        connection.execute(
            "UPDATE expenses SET amount = ? WHERE id = ?", (amount, expense_id)
        )

    if category is not None:
        connection.execute(
            "UPDATE expenses SET category = ? WHERE id = ?", (category, expense_id)
        )

    if name is not None:
        connection.execute(
            "UPDATE expenses SET name = ? WHERE id = ?", (name, expense_id)
        )

    connection.commit()

    expense = get_expense_by_id(expense_id)

    connection.close()

    return expense


def delete_expense(expense_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,),
    )

    connection.commit()

    deleted_count = cursor.rowcount

    connection.close()

    return deleted_count == 1


def delete_expenses():
    connection = get_connection()

    connection.execute("DELETE FROM expenses")

    connection.commit()

    connection.close()

    return True


def count_expenses(category=None, name=None, min_amount=None, max_amount=None):
    connection = get_connection()

    conditions = []
    params = []

    if category is not None:
        conditions.append("category = ?")
        params.append(category)

    if name is not None:
        conditions.append("name = ?")
        params.append(name)

    if min_amount is not None:
        conditions.append("amount >= ?")
        params.append(min_amount)

    if max_amount is not None:
        conditions.append("amount <= ?")
        params.append(max_amount)

    sql = "SELECT COUNT(*) FROM expenses"

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    total_count = connection.execute(sql, params).fetchone()[0]

    connection.close()

    return total_count
