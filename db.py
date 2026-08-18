from sqlite3 import connect

DB_NAME = "expenses.db"


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


def get_expenses():
    connection = get_connection()

    cursor = connection.execute(
        "SELECT id, amount, category, name FROM expenses ORDER BY id ASC"
    )

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
