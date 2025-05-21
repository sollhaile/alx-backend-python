#!/usr/bin/env python3
"""
0-log_queries.py
Log every SQL query before it is executed, with timestamp.
"""

import sqlite3
import functools
from datetime import datetime  # ✅ As required by spec

def log_queries(func):
    """
    Decorator that logs the SQL query with a timestamp
    before the function is executed.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query:
            # ✅ Log with timestamp
            print(f"[{datetime.now()}] SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """Return every row from the users table."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # Fetch users while logging the query with timestamp
    users = fetch_all_users("SELECT * FROM users")
    print(users)
