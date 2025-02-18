"""
Logging configuration.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler

from app.core.settings import DEBUG, LOG_FILE, LOG_LEVEL

# Determine the logging level
level = logging.getLevelName(LOG_LEVEL.upper())  # INFO, DEBUG, etc.
# Log format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Size handler (rotates every time the file reaches 1 MB)
size_handler = RotatingFileHandler(LOG_FILE, maxBytes=int(1e6), backupCount=5)
size_handler.setLevel(level)
size_handler.setFormatter(formatter)

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(level)

# Add the handler to the logger (size only)
logger.addHandler(size_handler)

# If DEBUG is True, also add the StreamHandler for the console
if DEBUG:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
