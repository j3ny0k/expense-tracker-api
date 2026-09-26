import pytest


@pytest.fixture(autouse=True)
def isolate_database(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
