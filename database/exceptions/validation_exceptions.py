"""
Validation-related exceptions.
"""


class ValidationException(Exception):
    """Base exception for validation errors."""


class InvalidInputException(ValidationException):
    """Raised when an input value does not meet validation criteria."""

    def __init__(self, field, reason):
        super().__init__(f"Invalid input for {field}: {reason}")


class RoleNotFoundError(ValidationException):
    """Raised when the role does not exist."""

    def __init__(self, message="Role not found."):
        super().__init__(message)


class InvalidRoleNameError(ValidationException):
    """Raised when the role name is invalid."""

    def __init__(self, message="Role name is invalid."):
        super().__init__(message)
