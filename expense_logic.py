import math


def validate_amount(expense):
    amount = expense.get("amount")

    return (
        isinstance(amount, (int, float))
        and not isinstance(amount, bool)
        and amount > 0
        and math.isfinite(amount)
    )


def validate_category(expense):
    category = expense.get("category")

    return isinstance(category, str) and category.strip() != ""


def validate_name(expense):
    name = expense.get("name")

    return isinstance(name, str) and name.strip() != ""


def calculate_budget_report(expenses, budget):
    spent = 0

    for e in expenses:
        spent += e["amount"]

    remaining = budget - spent
    over_budget = spent > budget

    return {
        "budget": budget,
        "spent": spent,
        "remaining": remaining,
        "over_budget": over_budget,
    }
