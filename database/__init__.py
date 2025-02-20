"""
Database module
This module contains utility functions and operations for interacting with the SQLite database,
including connection handling, transaction management, and user-related queries.

Functions include:
- Getting a connection to the database
- Committing and rolling back transactions
- Closing the database connection
- Performing various user-related operations like creating, fetching, updating, and deleting users
"""

from .db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
    rollback_db_connection,
)

__all__ = [
    "get_db_connection",
    "close_db_connection",
    "commit_db_connection",
    "rollback_db_connection",
]
