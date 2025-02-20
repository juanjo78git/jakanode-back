"""
Database configuration
"""

import os
import sqlite3

from app.core.settings import DB_NAME, DB_PATH


def get_db_path():
    """
    Returns the file path of the database.

    Returns:
        str: The full file path to the database.
    """
    return os.path.join(DB_PATH, DB_NAME)


def init_db():
    """
    Initializes the database settings (e.g., enabling WAL mode).
    This should be run once at the start of the application.
    """
    conn = get_db_connection()
    conn.execute("PRAGMA journal_mode = WAL;")  # Allows concurrent writes
    conn.execute(
        "PRAGMA busy_timeout = 5000;"
    )  # Waits up to 5 seconds in case of a lock
    conn.execute("PRAGMA synchronous = NORMAL;")  # Better performance on writes
    conn.execute("PRAGMA cache_size = 10000;")  # Increases cache to reduce disk access
    conn.execute("PRAGMA wal_autocheckpoint = 1000;")  # More frequent checkpoints
    conn.commit()
    conn.close()


def get_db_connection():
    """
    Establishes and returns a connection to the database.

    Returns:
        sqlite3.Connection: A connection object to interact with the SQLite database.
    """
    conn = sqlite3.connect(get_db_path(), timeout=10)
    conn.execute("PRAGMA journal_mode = WAL;")  # Allows concurrent writes
    conn.execute(
        "PRAGMA busy_timeout = 5000;"
    )  # Waits up to 5 seconds in case of a lock
    conn.execute("PRAGMA synchronous = NORMAL;")  # Better performance on writes
    conn.execute("PRAGMA cache_size = 10000;")  # Increases cache to reduce disk access
    conn.execute("PRAGMA wal_autocheckpoint = 1000;")  # More frequent checkpoints
    conn.commit()
    return conn


def close_db_connection(connection):
    """
    Closes the provided database connection.

    Args:
        connection (sqlite3.Connection): The connection to be closed.
    """
    if connection:
        connection.close()


def commit_db_connection(connection):
    """
    Commits the current transaction on the provided database connection.

    Args:
        connection (sqlite3.Connection): The connection on which to commit the transaction.
    """
    if connection:
        connection.commit()


def rollback_db_connection(connection):
    """
    Rollback the current transaction on the provided database connection in case of an error.

    Args:
        connection (sqlite3.Connection): The connection on which to rollback the transaction.
    """
    if connection:
        connection.rollback()
