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
