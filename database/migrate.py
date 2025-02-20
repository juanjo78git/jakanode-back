"""
Database Migration Runner

This script executes pending database migrations by dynamically loading and
running the `upgrade()` function from migration files located in `database/migrations/`.

How it works:
- It checks the `migrations` table to determine which migrations have already been applied.
- It scans the `database/migrations/` folder for new migration files.
- It applies only the migrations that have not been executed yet.
- After a successful migration, it records the migration filename in the database.

Usage:
Run this script after deploying new code to ensure the database is up to date:

    python -m database.migrate

The script will automatically execute only the necessary migrations.
"""

import importlib
import os
import sys

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
    rollback_db_connection,
)

# Root module for migrations
MIGRATIONS_DIR = "database.migrations"

# Connect to the database
connection = get_db_connection()
cursor = connection.cursor()

# Create the migrations table if it does not exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
)
commit_db_connection(connection)

# Get the list of already applied migrations
cursor.execute("SELECT filename FROM migrations")
applied_migrations = {row[0] for row in cursor.fetchall()}

# Get the list of available migration scripts
migration_files = sorted(
    f[:-3]
    for f in os.listdir("database/migrations")
    if f.endswith(".py") and f.startswith("00")
)

# Track successfully applied migrations in this run
applied_this_run = []

# Execute only the pending migrations
for migration in migration_files:
    if migration not in applied_migrations:
        print(f"Applying migration: {migration}")
        try:
            # Begin transaction
            cursor.execute("BEGIN TRANSACTION")

            # Dynamically import the migration module
            module = importlib.import_module(f"{MIGRATIONS_DIR}.{migration}")

            # Run the upgrade() function
            module.upgrade()

            # Record the migration as applied
            cursor.execute("INSERT INTO migrations (filename) VALUES (?)", (migration,))
            commit_db_connection(connection)
            applied_this_run.append(migration)  # Track applied migrations
            print(f"Migration {migration} applied successfully.")

        except Exception as e:  # pylint: disable=broad-exception-caught
            # Rollback transaction in case of error
            rollback_db_connection(connection)
            print(f"Error applying {migration}: {e}")

            # Rollback all migrations applied in this run
            print("Rolling back applied migrations...")
            for rollback_migration in reversed(applied_this_run):
                try:
                    print(f"Reverting {rollback_migration}...")
                    module = importlib.import_module(
                        f"{MIGRATIONS_DIR}.{rollback_migration}"
                    )
                    module.downgrade()

                    # Remove from migrations table
                    cursor.execute(
                        "DELETE FROM migrations WHERE filename = ?",
                        (rollback_migration,),
                    )
                    commit_db_connection(connection)
                    print(f"Migration {rollback_migration} reverted successfully.")
                except (
                    Exception  # pylint: disable=broad-exception-caught
                ) as rollback_error:
                    print(f"Error rolling back {rollback_migration}: {rollback_error}")

            sys.exit(1)  # Stop execution to prevent further issues

# Close the database connection
close_db_connection(connection)
print("Migrations completed successfully.")
