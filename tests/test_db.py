from db import (
    create_expense,
    delete_expense,
    get_connection,
    get_expense_by_id,
    get_expenses,
    init_db,
    update_expense,
)
from expense_logic import calculate_totals_by_category, find_largest_valid_expense


def test_init_db(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()
    init_db()

    connection = get_connection()
    columns = connection.execute("PRAGMA table_info(expenses)").fetchall()
    connection.close()

    assert columns[0][1] == "id"
    assert columns[0][2] == "INTEGER"

    assert columns[1][1] == "amount"
    assert columns[1][2] == "REAL"

    assert columns[2][1] == "category"
    assert columns[2][2] == "TEXT"

    assert columns[3][1] == "name"
    assert columns[3][2] == "TEXT"

    assert columns[0][5] == 1

    assert columns[1][3] == 1
    assert columns[2][3] == 1
    assert columns[3][3] == 1

    assert test_db.exists()


def test_create_expense(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    expense_id = create_expense(100.0, "food", "pizza")

    assert expense_id == 1

    connection = get_connection()
    row = connection.execute("SELECT * FROM expenses").fetchone()
    connection.close()

    assert row[0] == 1
    assert row[1] == 100.0
    assert row[2] == "food"
    assert row[3] == "pizza"


def test_get_expenses(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")

    result = get_expenses()

    assert result == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        }
    ]


def test_get_expenses_empty(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    result = get_expenses()

    assert result == []


def test_get_expenses_multiple(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "food", "bread")
    create_expense(300.0, "transport", "road")

    result = get_expenses()

    assert result == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        },
        {
            "id": 2,
            "amount": 200.0,
            "category": "food",
            "name": "bread",
        },
        {
            "id": 3,
            "amount": 300.0,
            "category": "transport",
            "name": "road",
        },
    ]


def test_calculate_totals_by_category(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "food", "bread")
    create_expense(300.0, "transport", "road")

    expenses = get_expenses()

    result = calculate_totals_by_category(expenses)

    assert result == {"food": 300.0, "transport": 300.0}


def test_calculate_totals_by_category_empty(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    expenses = get_expenses()

    result = calculate_totals_by_category(expenses)

    assert result == {}


def test_find_largest_valid_expense(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "food", "bread")
    create_expense(300.0, "transport", "road")

    expenses = get_expenses()

    result = find_largest_valid_expense(expenses)

    assert result == {"id": 3, "amount": 300.0, "category": "transport", "name": "road"}


def test_find_largest_valid_expense_empty(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    expenses = get_expenses()

    result = find_largest_valid_expense(expenses)

    assert result is None


def test_get_expense_by_id(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "food", "bread")
    create_expense(300.0, "transport", "road")

    result = get_expense_by_id(2)

    assert result == {"id": 2, "amount": 200.0, "category": "food", "name": "bread"}


def test_get_expense_by_id_missing(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    result = get_expense_by_id(999)

    assert result is None


def test_update_expense_amount(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")

    result = update_expense(1, 200, None, None)

    assert result == {
        "id": 1,
        "amount": 200.0,
        "category": "food",
        "name": "pizza",
    }


def test_update_expense_category(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "transport", "road")

    result = update_expense(1, None, "leisure", None)

    assert result == {
        "id": 1,
        "amount": 100.0,
        "category": "leisure",
        "name": "road",
    }


def test_update_expense_amount_and_name(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")

    result = update_expense(1, 200, None, "fast food")

    assert result == {
        "id": 1,
        "amount": 200.0,
        "category": "food",
        "name": "fast food",
    }


def test_update_expense_incorrect_id(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")

    result = update_expense(2, 200, None, None)

    assert result is None


def test_delete_expense(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")

    result = delete_expense(1)

    assert result is True


def test_delete_expense_found_is_none(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")

    delete_expense(1)

    result = get_expense_by_id(1)

    assert result is None


def test_delete_expense_double_is_false(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()

    create_expense(100.0, "food", "pizza")

    delete_expense(1)

    result = delete_expense(1)

    assert result is False
