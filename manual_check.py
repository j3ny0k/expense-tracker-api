from expense_logic import calculate_totals_by_category

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

assert calculate_totals_by_category(expenses=[]) == {}

assert calculate_totals_by_category(expenses=[{"amount": 100, "category": "food"}]) == {
    "food": 100
}

assert calculate_totals_by_category(
    expenses=[
        {"amount": 100, "category": "food"},
        {"amount": 50.5, "category": "food"},
    ]
) == {"food": 150.5}

assert (
    calculate_totals_by_category(
        expenses=[
            {"amount": 100},
        ]
    )
    == {}
)

assert (
    calculate_totals_by_category(
        expenses=[
            {"category": "food"},
        ]
    )
    == {}
)

assert (
    calculate_totals_by_category(
        expenses=[
            {"amount": "100", "category": "food"},
        ]
    )
    == {}
)
