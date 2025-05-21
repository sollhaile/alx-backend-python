#!/usr/bin/env python3
"""
0-log_queries.py
Log every SQL query before it is executed.
"""

import sqlite3
import functools


def log_queries(func):
    """
    Decorator that prints the SQL query passed to *func*
    before the function is executed.
    The query is expected either as the first positional
    argument or as the keyword argument ``query``.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query is not None:
            # -- Exactly one log line, no timestamps, no datetime import.
            print(f"SQL query: {query}")
        return func(*args, **kwargs)

    return wrapper


@log_queries        # ← NO parentheses, matches project prototype
def fetch_all_users(query):
    """Return every row from the users table."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Fetch users while logging the query
    users = fetch_all_users("SELECT * FROM users")
    print(users)
