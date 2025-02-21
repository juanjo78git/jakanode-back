"""
Database-related exceptions.
"""

class DatabaseException(Exception):
    """Base exception for database-related errors."""


class UserNotFoundException(DatabaseException):
    """Raised when a user is not found in the database."""

    def __init__(self, user_id):
        super().__init__(f"User with ID {user_id} not found.")


class UserAlreadyExistsException(DatabaseException):
    """Raised when trying to create a user that already exists."""

    def __init__(self, username):
        super().__init__(f"User with username '{username}' already exists.")


class InvalidUserStatusException(DatabaseException):
    """Raised when an invalid status is provided for a user."""

    def __init__(self, status):
        super().__init__(f"Invalid user status: {status}.")


class DatabaseError(Exception):
    """Base class for database errors."""


class RecordNotFound(DatabaseError):
    """Raised when a record is not found in the database."""

    def __init__(self, message="Record not found"):
        super().__init__(message)


class IntegrityError(DatabaseError):
    """Raised when a database constraint is violated (e.g., unique constraint)."""

    def __init__(self, message="Integrity error"):
        super().__init__(message)
