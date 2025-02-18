"""
Token Schema for Authentication

This module defines the schema used for the authentication response,
which includes the access token and token type. The schema is used
to validate and serialize the response when a user successfully
authenticates.

Attributes:
    access_token (str): The JWT access token issued after authentication.
    token_type (str): The type of token, typically "bearer".

This schema is used in the authentication endpoints of the API to
ensure a consistent response format.
"""

from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Schema for the authentication response token.

    Attributes:
        access_token (str): The JWT access token issued after authentication.
        token_type (str): The type of token, typically "bearer".
    """

    access_token: str
    token_type: str
