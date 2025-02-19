"""
Core configuration module.

This module loads configuration variables from the environment
or a .env file and defines constants used throughout the application.
"""

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Auth
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Logging configuration
DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/jakanode_back.log")

# Database configuration
DB_NAME = os.getenv("DB_NAME", "db.sqlite3")
DB_PATH = os.getenv("DB_PATH", "./")
