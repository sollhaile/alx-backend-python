#!/usr/bin/env python3
"""
4-cache_query.py
Caches database query results to avoid redundant calls.
"""

import sqlite3
import functools

# Global cache dictionary: query string -> results
query_cache = {}

def with_db_connection(func):
    """
    Reuse: decorator that opens/closes DB connection automatically.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """
    Decorator that caches query results based on the query string.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Get the query string from args or kwargs
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query is None:
            # No query given, just call the function normally
            return func(conn, *args, **kwargs)

        # Check if result is cached
        if query in query_cache:
            print(f"[Cache] Returning cached result for query: {query}")
            return query_cache[query]

        # Otherwise, run the query and cache the results
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from DB; cache results to avoid duplicate queries.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    # First call - caches result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call - returns cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
