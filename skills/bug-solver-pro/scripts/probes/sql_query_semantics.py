#!/usr/bin/env python3
"""Isolated in-memory SQL controls for join grain and null-sensitive exclusion.

Python standard library only. No production database, files, network or migrations.
"""

import json
import sqlite3


def probe():
    with sqlite3.connect(":memory:") as database:
        database.executescript("""
            CREATE TABLE orders (id INTEGER PRIMARY KEY, amount INTEGER NOT NULL);
            INSERT INTO orders VALUES (1, 100), (2, 100), (3, 30);
            CREATE TABLE tags (order_id INTEGER, label TEXT);
            INSERT INTO tags VALUES (1, 'a'), (1, 'b'), (1, 'c'), (3, 'd');
            CREATE TABLE candidates (id INTEGER);
            INSERT INTO candidates VALUES (1), (2), (NULL);
            CREATE TABLE excluded (id INTEGER);
            INSERT INTO excluded VALUES (2), (NULL);
        """)
        joined_ids = [row[0] for row in database.execute(
            "SELECT o.id FROM orders o LEFT JOIN tags t ON t.order_id = o.id ORDER BY o.id, t.label")]
        naive = database.execute(
            "SELECT SUM(o.amount) FROM orders o LEFT JOIN tags t ON t.order_id = o.id").fetchone()[0]
        distinct_amounts = database.execute(
            "SELECT SUM(DISTINCT o.amount) FROM orders o LEFT JOIN tags t ON t.order_id = o.id").fetchone()[0]
        at_order_grain = database.execute("""
            SELECT SUM(amount) FROM (
                SELECT o.id, o.amount FROM orders o
                LEFT JOIN tags t ON t.order_id = o.id GROUP BY o.id, o.amount
            )
        """).fetchone()[0]
        not_in_with_null = [row[0] for row in database.execute(
            "SELECT id FROM candidates WHERE id NOT IN (SELECT id FROM excluded) ORDER BY id")]
        explicit_policy = [row[0] for row in database.execute("""
            SELECT c.id FROM candidates c WHERE c.id IS NOT NULL AND NOT EXISTS (
                SELECT 1 FROM excluded e WHERE e.id = c.id
            ) ORDER BY c.id
        """)]
        database.execute("DELETE FROM excluded WHERE id IS NULL")
        not_in_without_null = [row[0] for row in database.execute(
            "SELECT id FROM candidates WHERE id NOT IN (SELECT id FROM excluded) ORDER BY id")]
        database.execute("DELETE FROM excluded")
        not_in_empty_set = [row[0] for row in database.execute(
            "SELECT id FROM candidates WHERE id NOT IN (SELECT id FROM excluded) ORDER BY id")]
    # Independent fixture oracle: three intended orders, including two equal amounts.
    if (joined_ids, naive, distinct_amounts, at_order_grain) != ([1, 1, 1, 2, 3], 430, 130, 230):
        raise AssertionError("Join/cardinality prediction contradicted")
    if (not_in_with_null, not_in_without_null, not_in_empty_set, explicit_policy) != ([], [1], [None, 1, 2], [1]):
        raise AssertionError("Null membership prediction contradicted")
    return {
        "kind": "synthetic_sql_runtime_probe",
        "sqlite_version": sqlite3.sqlite_version,
        "join_grain": {"row_ids": joined_ids, "naive_sum": naive,
                       "distinct_amount_sum": distinct_amounts, "order_grain_sum": at_order_grain},
        "null_exclusion": {"not_in_with_null": not_in_with_null,
                           "not_in_without_null": not_in_without_null,
                           "not_in_empty_set": not_in_empty_set,
                           "explicit_non_null_identity_policy": explicit_policy},
        "limits": "SQLite in-memory fixtures only; no claim about production isolation, query plans, ORM behavior, or every provider. The explicit null policy is a fixture contract, not a universal replacement.",
    }


if __name__ == "__main__":
    print(json.dumps(probe(), indent=2))
