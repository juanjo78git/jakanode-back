# pylint: disable=invalid-name
"""
migrations/0001_create_auth_and_roles_tables.py

Run:
python -m database.migrations.0001_create_auth_and_roles_tables upgrade

Run rollback:
python -m database.migrations.0001_create_auth_and_roles_tables downgrade
"""

import sys

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)


def upgrade():
    """
    Create authentication, roles, and permissions tables.

    Raises:
        sqlite3.DatabaseError: If there is an error executing the SQL query.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    # Crear tabla de usuarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            password_salt TEXT,
            full_name TEXT,
            language TEXT DEFAULT 'en',
            status TEXT DEFAULT 'active',
            failed_attempts INTEGER DEFAULT 0,
            last_failed_attempt TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Crear tabla de métodos de autenticación
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            provider TEXT NOT NULL, -- 'telegram', 'google', 'password'
            provider_id TEXT NOT NULL, -- ID de Telegram, Google o NULL si es password
            last_login TIMESTAMP DEFAULT NULL,
            linked_user_id INTEGER NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, provider),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """
    )

    # Crear tabla de datos específicos de Telegram
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_telegram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            telegram_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            photo_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """
    )

    # Crear tabla de datos específicos de Google
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_google (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            google_id TEXT NOT NULL UNIQUE,
            full_name TEXT,
            email TEXT UNIQUE NOT NULL,
            picture TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """
    )

    # Crear tabla de roles
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Crear tabla de relación usuario-rol
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, role_id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
        );
    """
    )

    # Crear tabla de permisos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    )

    # Crear tabla de relación rol-permisos
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS role_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(role_id, permission_id),
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
            FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
        );
    """
    )

    # Crear tabla de auditoría de eventos de autenticación
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL, -- 'login_success', 'login_failed', 'role_change', etc.
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );
    """
    )

    # Crear índices para mejorar rendimiento
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_auth_providers_provider_id ON auth_providers(provider_id);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_auth_telegram_telegram_id ON auth_telegram(telegram_id);"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_auth_google_google_id ON auth_google(google_id);"
    )

    commit_db_connection(connection)
    close_db_connection(connection)
    print("Migration applied successfully!")


def downgrade():
    """
    Drop all authentication, roles, and permissions tables.

    Raises:
        sqlite3.DatabaseError: If there is an error executing the SQL query.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS audit_logs;")
    cursor.execute("DROP TABLE IF EXISTS role_permissions;")
    cursor.execute("DROP TABLE IF EXISTS permissions;")
    cursor.execute("DROP TABLE IF EXISTS user_roles;")
    cursor.execute("DROP TABLE IF EXISTS roles;")
    cursor.execute("DROP TABLE IF EXISTS auth_google;")
    cursor.execute("DROP TABLE IF EXISTS auth_telegram;")
    cursor.execute("DROP TABLE IF EXISTS auth_providers;")
    cursor.execute("DROP TABLE IF EXISTS users;")

    commit_db_connection(connection)
    close_db_connection(connection)
    print("Migration rolled back successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == "upgrade":
            upgrade()
        elif command == "downgrade":
            downgrade()
        else:
            print("Invalid command. Use 'upgrade' or 'downgrade'.")
    else:
        print("Please specify 'upgrade' or 'downgrade'.")
