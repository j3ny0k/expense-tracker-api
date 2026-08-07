from expense_logic import calculate_totals_by_category, find_largest_valid_expense


def test_calculate_totals_by_category():
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

    assert calculate_totals_by_category(expenses) == {
        "leisure": 200.0,
        "food": 550.0,
        "transport": 40.0,
    }


def test_calculate_totals_by_category_empty():
    expenses = []

    assert calculate_totals_by_category(expenses) == {}


def test_calculate_totals_by_category_1():
    expenses = [{"amount": 100.0, "category": "food", "name": "продукты"}]

    assert calculate_totals_by_category(expenses) == {"food": 100.0}


def test_calculate_totals_by_category_2():
    expenses = [
        {"amount": 100, "category": "food", "name": "продукты"},
        {"amount": 50.5, "category": "food", "name": "продукты"},
    ]

    assert calculate_totals_by_category(expenses) == {"food": 150.5}


def test_calculate_totals_without_category():
    expenses = [{"amount": 150, "name": "кафе"}]

    assert calculate_totals_by_category(expenses) == {}


def test_calculate_totals_without_amount():
    expenses = [{"category": "food", "name": "кафе"}]

    assert calculate_totals_by_category(expenses) == {}


def test_calculate_totals_with_amount_str():
    expenses = [{"amount": "150", "category": "food", "name": "кафе"}]

    assert calculate_totals_by_category(expenses) == {}


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
