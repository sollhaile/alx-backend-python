#!/usr/bin/env python3
"""
1-with_db_connection.py
Automatically handle opening and closing the database connection.
"""

import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that opens a database connection,
    passes it to the function, and ensures it is closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            # Pass the open connection as the first argument
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Get a single user by ID using an open database connection.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# ✅ Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
