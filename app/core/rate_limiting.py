"""
Rate Limiting Configuration for FastAPI using slowapi.

This module configures rate limiting by creating a Limiter instance
that uses the client's remote address as the key for limiting requests.
It also provides an exception handler (_rate_limit_exceeded_handler)
to return a proper HTTP 429 response when the rate limit is exceeded.

Usage:
    - Import `limiter` and `_rate_limit_exceeded_handler` from this module.
    - In your main application, associate the limiter with the app's state
      and add the exception handler.
"""
# pylint: disable=W0611
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

# Create a Limiter instance using the client's IP address as the key.
limiter = Limiter(key_func=get_remote_address)
