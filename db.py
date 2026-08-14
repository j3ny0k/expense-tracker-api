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
        "SELECT id, amount, category, name FROM expenses WHERE id = ?",
        (expense_id,),
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
