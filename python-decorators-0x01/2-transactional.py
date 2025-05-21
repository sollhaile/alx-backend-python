#!/usr/bin/env python3
"""
2-transactional.py
Manages DB transactions with automatic commit/rollback.
"""

import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator to automatically handle opening and closing the database connection.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Decorator to handle DB transactions:
    - Commit if successful
    - Rollback if an exception is raised
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e  # Optional: Re-raise the error for debugging/logging
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Update a user's email in the database.
    Transaction will be automatically committed or rolled back.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# ✅ Update user's email with automatic transaction and connection handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
