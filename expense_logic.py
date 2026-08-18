def validate_amount(expense):
    amount = expense.get("amount")

    return (
        isinstance(amount, (int, float)) and not isinstance(amount, bool) and amount > 0
    )


def validate_category(expense):
    category = expense.get("category")

    return isinstance(category, str) and category.strip() != ""


def validate_name(expense):
    name = expense.get("name")

    return isinstance(name, str) and name.strip() != ""


def calculate_totals_by_category(expenses):
    result = {}

    for e in expenses:
        if validate_amount(e) and validate_category(e):
            amount = e.get("amount")
            category = e.get("category").strip()

            if category not in result:
                result[category] = 0

            result[category] += amount

    return result


def find_largest_valid_expense(expenses):
    result = None

    for e in expenses:
        if validate_amount(e) and validate_category(e):
            amount = e.get("amount")

            if result is None:
                result = e.copy()

            if amount > result["amount"]:
                result = e.copy()

    return result
