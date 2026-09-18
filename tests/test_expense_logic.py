from expense_logic import find_largest_valid_expense


def test_find_largest_valid_expense():
    expenses = [
        {"amount": 120.0, "category": "leisure", "name": "кино"},
        {"amount": 250.0, "category": "food", "name": "продукты"},
        {"amount": 80.0, "category": "leisure", "name": "игра"},
        {"amount": 40, "category": "transport", "name": "автобус"},
        {"amount": 150, "category": "food", "name": "кафе"},
        {"amount": 150, "category": " food ", "name": "кафе"},
        {"category": "food", "name": "кафе"},
        {"amount": 150, "category": "", "name": "кафе"},
        {"amount": 150, "name": "кафе"},
        {"amount": "150", "category": "food", "name": "кафе"},
        {"amount": "", "category": "food", "name": "кафе"},
        {"amount": None, "category": "food", "name": "кафе"},
        {"amount": True, "category": "food", "name": "кафе"},
    ]

    assert find_largest_valid_expense(expenses) == {
        "amount": 250.0,
        "category": "food",
        "name": "продукты",
    }


def test_find_largest_valid_expense_empty():
    expenses = []

    assert find_largest_valid_expense(expenses) is None


def test_find_largest_valid_expense_1():
    expenses = [{"amount": 100.0, "category": "food", "name": "продукты"}]

    assert find_largest_valid_expense(expenses) == {
        "amount": 100.0,
        "category": "food",
        "name": "продукты",
    }


def test_find_largest_valid_expense_invalid():
    expenses = [
        {"category": "food", "name": "кафе"},
        {"amount": 150, "category": "", "name": "кафе"},
        {"amount": 150, "name": "кафе"},
        {"amount": "150", "category": "food", "name": "кафе"},
        {"amount": "", "category": "food", "name": "кафе"},
        {"amount": None, "category": "food", "name": "кафе"},
        {"amount": True, "category": "food", "name": "кафе"},
    ]

    assert find_largest_valid_expense(expenses) is None


def test_find_largest_valid_expense_2():
    expenses = [
        {"amount": 100.0, "category": "food", "name": "продукты"},
        {"amount": 100.0, "category": "leisure", "name": "rest"},
    ]

    assert find_largest_valid_expense(expenses) == {
        "amount": 100.0,
        "category": "food",
        "name": "продукты",
    }
