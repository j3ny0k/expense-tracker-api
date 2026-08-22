from app import app
from db import create_expense, init_db


def init_db_for_test(tmp_path, monkeypatch):
    test_db = tmp_path / "expenses.db"
    monkeypatch.setattr("db.DB_NAME", test_db)

    init_db()


def test_get_expenses_empty(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_expense_undefined_id(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses/1")

    assert response.status_code == 404
    assert response.get_json() == {"error": "expense not found"}


def test_get_expense_1(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    response = client.get("/expenses/1")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "amount": 100.0,
        "category": "food",
        "name": "pizza",
    }


def test_post_expense(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.post(
        "/expenses",
        json={
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "amount": 100.0,
        "category": "food",
        "name": "pizza",
    }


def test_post_expense_without_amount(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.post(
        "/expenses",
        json={
            "category": "food",
            "name": "pizza",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "amount is required"}


def test_post_expense_without_category(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.post(
        "/expenses",
        json={
            "amount": 100.0,
            "name": "pizza",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "category is required"}


def test_post_expense_without_name(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.post(
        "/expenses",
        json={
            "amount": 100.0,
            "category": "food",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "name is required"}


def test_patch_amount(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    response = client.patch(
        "/expenses/1",
        json={
            "amount": 200,
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 1,
        "amount": 200.0,
        "category": "food",
        "name": "pizza",
    }


def test_patch_amount_unknown_fields(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    response = client.patch(
        "/expenses/1",
        json={
            "amount": 200.0,
            "category": "food",
            "name": "pizza",
            "abc": "banana",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "unknown fields: abc"}


def test_patch_expense_empty_request(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    response = client.patch(
        "/expenses/1",
        json={},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "there must be at least one argument"}


def test_patch_amount_undefined_id(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.patch(
        "/expenses/999",
        json={
            "amount": 200.0,
            "category": "food",
            "name": "pizza",
        },
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "expense not found"}


def test_delete_expense(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    response = client.delete("/expenses/1")

    assert response.status_code == 204


def test_delete_expense_2_times(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    client.delete("/expenses/1")
    response = client.delete("/expenses/1")

    assert response.status_code == 404
    assert response.get_json() == {"error": "expense not found"}


def test_delete_expenses(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    response = client.delete("/expenses")

    assert response.status_code == 204

    response = client.get("/expenses")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_expenses(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")

    response = client.get("/expenses")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        },
        {
            "id": 2,
            "amount": 200.0,
            "category": "transport",
            "name": "bus",
        },
        {
            "id": 3,
            "amount": 300.0,
            "category": "food",
            "name": "bread",
        },
    ]


def test_get_expenses_filter_by_category(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")

    response = client.get("/expenses?category=food")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        },
        {
            "id": 3,
            "amount": 300.0,
            "category": "food",
            "name": "bread",
        },
    ]


def test_get_expenses_filter_by_name(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")

    response = client.get("/expenses?name=pizza")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        }
    ]


def test_get_expenses_filter_by_category_and_name(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")
    create_expense(400.0, "transport", "pizza")

    response = client.get("/expenses?category=food&name=pizza")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        }
    ]


def test_calculate_totals_by_category(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")
    create_expense(400.0, "transport", "pizza")

    response = client.get("/expenses/totals")

    assert response.status_code == 200
    assert response.get_json() == {"food": 400.0, "transport": 600.0}


def test_calculate_totals_by_category_empty(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses/totals")

    assert response.status_code == 200
    assert response.get_json() == {}


def test_find_largest_valid_expense(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")

    response = client.get("/expenses/largest")

    assert response.status_code == 200
    assert response.get_json() == {
        "id": 2,
        "amount": 200.0,
        "category": "transport",
        "name": "bus",
    }


def test_find_largest_valid_expense_empty(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses/largest")

    assert response.status_code == 200
    assert response.get_json() is None


def test_min_amount(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "pizza")

    response = client.get("/expenses?min_amount=200")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 2,
            "amount": 200.0,
            "category": "transport",
            "name": "bus",
        },
        {
            "id": 3,
            "amount": 300.0,
            "category": "food",
            "name": "pizza",
        },
    ]


def test_max_amount(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "pizza")

    response = client.get("/expenses?max_amount=200")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        },
        {
            "id": 2,
            "amount": 200.0,
            "category": "transport",
            "name": "bus",
        },
    ]


def test_min_and_max_amount(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "pizza")

    response = client.get("/expenses?min_amount=150&max_amount=250")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 2,
            "amount": 200.0,
            "category": "transport",
            "name": "bus",
        }
    ]


def test_min_amount_error(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    response = client.get("/expenses?min_amount=abc")

    assert response.status_code == 400
    assert response.get_json() == {"error": "amount is required"}


def test_max_amount_error(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")

    response = client.get("/expenses?max_amount=abc")

    assert response.status_code == 400
    assert response.get_json() == {"error": "amount is required"}


def test_min_and_max_amount_error(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "pizza")

    response = client.get("/expenses?min_amount=450&max_amount=250")

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "max amount must be greater than min amount"
    }


def test_min_amount0(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "pizza")

    response = client.get("/expenses?min_amount=0")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        },
        {
            "id": 2,
            "amount": 200.0,
            "category": "transport",
            "name": "bus",
        },
        {
            "id": 3,
            "amount": 300.0,
            "category": "food",
            "name": "pizza",
        },
    ]


def test_get_expenses_filter_by_category_and_min_amount(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")

    response = client.get("/expenses?category=food&min_amount=200")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 3,
            "amount": 300.0,
            "category": "food",
            "name": "bread",
        }
    ]


def test_get_expenses_limit(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")

    response = client.get("/expenses?limit=2")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        },
        {
            "id": 2,
            "amount": 200.0,
            "category": "transport",
            "name": "bus",
        },
    ]


def test_get_expenses_limit_and_offset(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")

    response = client.get("/expenses?limit=2&offset=1")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 2,
            "amount": 200.0,
            "category": "transport",
            "name": "bus",
        },
        {
            "id": 3,
            "amount": 300.0,
            "category": "food",
            "name": "bread",
        },
    ]


def test_get_expenses_offset_without_limit(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")

    response = client.get("/expenses?offset=1")

    assert response.status_code == 400
    assert response.get_json() == {"error": "limit is required when offset is provided"}


def test_get_expenses_limit_zero(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses?limit=0")

    assert response.status_code == 400
    assert response.get_json() == {"error": "limit must be greater than 0"}


def test_get_expenses_limit_negative(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses?limit=-1")

    assert response.status_code == 400
    assert response.get_json() == {"error": "limit must be greater than 0"}


def test_get_expenses_limit_abc(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses?limit=abc")

    assert response.status_code == 400
    assert response.get_json() == {"error": "limit must be an integer"}


def test_get_expenses_offset_negative(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses?limit=2&offset=-1")

    assert response.status_code == 400
    assert response.get_json() == {"error": "offset must be greater than or equal to 0"}


def test_get_expenses_offset_abc(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    response = client.get("/expenses?limit=2&offset=abc")

    assert response.status_code == 400
    assert response.get_json() == {"error": "offset must be an integer"}


def test_get_expenses_offset_zero(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")

    response = client.get("/expenses?limit=2&offset=0")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 1,
            "amount": 100.0,
            "category": "food",
            "name": "pizza",
        },
        {
            "id": 2,
            "amount": 200.0,
            "category": "transport",
            "name": "bus",
        },
    ]


def test_get_expenses_filter_before_pagination(tmp_path, monkeypatch):
    init_db_for_test(tmp_path, monkeypatch)

    client = app.test_client()

    create_expense(100.0, "food", "pizza")
    create_expense(200.0, "transport", "bus")
    create_expense(300.0, "food", "bread")
    create_expense(400.0, "transport", "taxi")

    response = client.get("/expenses?category=food&limit=1&offset=1")

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "id": 3,
            "amount": 300.0,
            "category": "food",
            "name": "bread",
        }
    ]
