import sqlite3

import pytest

import migrations


def test_failed_migration_rolls_back_changes(monkeypatch):
    connection = sqlite3.connect(":memory:")

    def failing_migration(connection):
        connection.execute("CREATE TABLE partial_change (id INTEGER)")
        raise RuntimeError("migration failed")

    monkeypatch.setattr(
        migrations,
        "MIGRATIONS",
        [(99, failing_migration)],
    )

    with pytest.raises(RuntimeError):
        migrations.run_migrations(connection)

    partial_table = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'partial_change'
        """).fetchone()

    assert partial_table is None
