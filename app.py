from flask import Flask, jsonify, request

from db import (
    create_expense,
    delete_expense,
    delete_expenses,
    get_expense_by_id,
    get_expenses,
    init_db,
    update_expense,
)
from expense_logic import (
    calculate_totals_by_category,
    find_largest_valid_expense,
    validate_amount,
    validate_category,
    validate_name,
)

app = Flask(__name__)


@app.post("/expenses")
def api_create_expense():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object is required"}), 400

    if "amount" not in data or not validate_amount(data):
        return jsonify({"error": "amount is required"}), 400

    if "category" not in data or not validate_category(data):
        return jsonify({"error": "category is required"}), 400

    if "name" not in data or not validate_name(data):
        return jsonify({"error": "name is required"}), 400

    amount = data.get("amount")
    category = data.get("category").strip()
    name = data.get("name").strip()

    expense_id = create_expense(amount, category, name)
    expense = get_expense_by_id(expense_id)

    return jsonify(expense), 201


@app.get("/expenses")
def api_get_expenses():
    expenses = get_expenses()

    category = request.args.get("category")

    name = request.args.get("name")

    min_amount = request.args.get("min_amount")

    max_amount = request.args.get("max_amount")

    if category:
        filtered_expenses = []

        for e in expenses:
            if e["category"] == category:
                filtered_expenses.append(e)

        expenses = filtered_expenses

    if name:
        filtered_expenses = []

        for e in expenses:
            if e["name"] == name:
                filtered_expenses.append(e)

        expenses = filtered_expenses

    if min_amount is not None:
        try:
            min_amount = float(min_amount)
        except ValueError:
            return jsonify({"error": "amount is required"}), 400

    if max_amount is not None:
        try:
            max_amount = float(max_amount)
        except ValueError:
            return jsonify({"error": "amount is required"}), 400

    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        return jsonify({"error": "max amount must be greater than min amount"}), 400

    if min_amount is not None:
        filtered_expenses = []

        for e in expenses:
            if e["amount"] >= min_amount:
                filtered_expenses.append(e)

        expenses = filtered_expenses

    if max_amount is not None:
        filtered_expenses = []

        for e in expenses:
            if e["amount"] <= max_amount:
                filtered_expenses.append(e)

        expenses = filtered_expenses

    return jsonify(expenses), 200


@app.get("/expenses/<int:expense_id>")
def api_get_expense_by_id(expense_id):
    expense = get_expense_by_id(expense_id)

    if expense is None:
        return jsonify({"error": "expense not found"}), 404

    return jsonify(expense), 200


@app.get("/expenses/totals")
def api_calculate_totals_by_category():
    expenses = get_expenses()

    totals = calculate_totals_by_category(expenses)

    return jsonify(totals), 200


@app.get("/expenses/largest")
def api_find_largest_valid_expense():
    expenses = get_expenses()

    largest = find_largest_valid_expense(expenses)

    return jsonify(largest), 200


@app.patch("/expenses/<int:expense_id>")
def api_update_expense(expense_id):
    expense = get_expense_by_id(expense_id)

    if expense is None:
        return jsonify({"error": "expense not found"}), 404

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "JSON object is required"}), 400

    allowed_fields = {"amount", "category", "name"}

    unknown_fields = set(data) - allowed_fields

    if unknown_fields:
        return jsonify(
            {"error": f"unknown fields: {', '.join(sorted(unknown_fields))}"}
        ), 400

    if "amount" not in data and "category" not in data and "name" not in data:
        return jsonify({"error": "there must be at least one argument"}), 400

    if "amount" in data:
        if not validate_amount(data):
            return jsonify({"error": "amount is required"}), 400

        amount = data.get("amount")

    else:
        amount = None

    if "category" in data:
        if not validate_category(data):
            return jsonify({"error": "category is required"}), 400

        category = data.get("category").strip()

    else:
        category = None

    if "name" in data:
        if not validate_name(data):
            return jsonify({"error": "name is required"}), 400

        name = data.get("name").strip()

    else:
        name = None

    updated_expense = update_expense(expense_id, amount, category, name)

    return jsonify(updated_expense), 200


@app.delete("/expenses/<int:expense_id>")
def api_delete_expense(expense_id):
    if delete_expense(expense_id) is False:
        return jsonify({"error": "expense not found"}), 404

    return "", 204


@app.delete("/expenses")
def api_delete_expenses():
    delete_expenses()
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
