import json
import os
import sys
import urllib.error
import urllib.request

TIMEOUT_SECONDS = 10


class SmokeError(Exception):
    pass


base_url = os.getenv("SMOKE_BASE_URL")
api_key = os.getenv("API_KEY")


def build_url(path):
    return f"{base_url.rstrip('/')}{path}"


def open_json(request, step, expected_status):
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            if response.status != expected_status:
                raise SmokeError(
                    f"{step} failed: expected {expected_status}, got {response.status}"
                )

            try:
                return json.loads(response.read())
            except json.JSONDecodeError:
                raise SmokeError(f"{step} failed: invalid JSON") from None

    except urllib.error.HTTPError as error:
        raise SmokeError(f"{step} failed: HTTP {error.code}") from None
    except urllib.error.URLError:
        raise SmokeError(f"{step} failed: request error") from None


def open_no_content(request, step, expected_status):
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            if response.status != expected_status:
                raise SmokeError(
                    f"{step} failed: expected {expected_status}, got {response.status}"
                )

    except urllib.error.HTTPError as error:
        raise SmokeError(f"{step} failed: HTTP {error.code}") from None
    except urllib.error.URLError:
        raise SmokeError(f"{step} failed: request error") from None


def check_health():
    request = urllib.request.Request(
        build_url("/health"),
        method="GET",
    )

    body = open_json(request, "health", 200)

    if body != {"status": "ok"}:
        raise SmokeError("health failed: unexpected response")

    print("health: ok")


def check_expenses_without_key():
    request = urllib.request.Request(
        build_url("/expenses"),
        method="GET",
    )

    try:
        urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS)

    except urllib.error.HTTPError as error:
        if error.code != 401:
            raise SmokeError(
                f"expenses without key failed: HTTP {error.code}"
            ) from None

    except urllib.error.URLError:
        raise SmokeError("expenses without key failed: request error") from None

    else:
        raise SmokeError("expenses without key failed: request unexpectedly succeeded")

    print("expenses without key: ok")


def create_expense():
    payload = {
        "amount": 1.0,
        "category": "smoke",
        "name": "smoke-test",
    }

    request = urllib.request.Request(
        build_url("/expenses"),
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-API-Key": api_key,
        },
        method="POST",
    )

    body = open_json(request, "create", 201)

    expense_id = body.get("id")

    if not isinstance(expense_id, int):
        raise SmokeError("create failed: response has no valid id")

    print("create: ok")
    return expense_id, payload


def read_expense(expense_id, payload):
    request = urllib.request.Request(
        build_url(f"/expenses/{expense_id}"),
        headers={
            "X-API-Key": api_key,
        },
        method="GET",
    )

    body = open_json(request, "read", 200)

    expected = {
        "id": expense_id,
        **payload,
    }

    if body != expected:
        raise SmokeError("read failed: unexpected expense")

    print("read: ok")


def delete_expense(expense_id, step="delete"):
    request = urllib.request.Request(
        build_url(f"/expenses/{expense_id}"),
        headers={
            "X-API-Key": api_key,
        },
        method="DELETE",
    )

    open_no_content(request, step, 204)


def main():
    if not base_url or not api_key:
        print("smoke failed: SMOKE_BASE_URL and API_KEY are required")
        return 1

    created_id = None

    try:
        check_health()
        check_expenses_without_key()

        created_id, payload = create_expense()
        read_expense(created_id, payload)

        delete_expense(created_id)
        created_id = None
        print("delete: ok")

        print("smoke: ok")
        return 0

    except SmokeError as error:
        print(f"smoke failed: {error}")
        return 1

    finally:
        if created_id is not None:
            try:
                delete_expense(created_id, step="cleanup")
                print("cleanup: ok")
            except SmokeError:
                print("cleanup: failed")


if __name__ == "__main__":
    sys.exit(main())
