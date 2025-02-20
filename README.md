# Jakanode-back Project
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![pylint](https://img.shields.io/github/actions/workflow/status/juanjo78git/jakanode-back/pylint.yml?branch=main&label=pylint&logo=python)
![Version](https://img.shields.io/github/v/release/juanjo78git/jakanode-back)


A robust and versatile Back built with Python, designed to streamline automation and enhance user interaction.

## Installing and Setting Up

To set up *jakanode-back*, follow these steps to create a virtual environment and install the required dependencies:

### Create a Virtual Environment

First, create a virtual environment in the project's root directory. 
You can do this by running the following command:

```bash
python3 -m venv venv
```
This will create a folder named `venv` where the virtual environment will be stored.

### Activate the Virtual Environment

Before installing dependencies, activate the virtual environment:
```bash
source venv/bin/activate
```
After activation, your terminal prompt should change to indicate that the virtual environment is active.

### Install Dependencies

Once the virtual environment is activated, install the required dependencies by running:
```bash
pip install -r requirements.txt
```
This command will install all the necessary packages listed in the `requirements.txt` file for `jakanode-back` to work properly.

### Verify the Installation

After installing the dependencies, you can verify that everything is installed correctly by checking the installed packages:
```bash
pip list
```
This will show a list of installed packages, and you should see the required ones from the `requirements.txt` file.

---

Now, your environment is ready for running *jakanode-back* and executing commands or running itself.


## Environment Variables

This document explains the environment variables used in the `.env` file for configuring *jakanode-back*.

### Example `.env` File

```ini
# Auth Configuration
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
SECRET_KEY=supersecretkey

# Database Configuration
DB_NAME=db.sqlite3
DB_PATH=./database

# Logging Configuration
DEBUG=False
LOG_LEVEL=INFO
LOG_FILE=logs/jakanode_back.log
```

---

### Environment Variables Explanation

#### Auth Configuration

- `TELEGRAM_BOT_TOKEN`: The authentication token for your Telegram bot.
- `SECRET_KEY`: Secret key to create a JWT Token.

    ##### Generate secret key
    ```python
    import secrets
    
    secret_key = secrets.token_hex(32)  # Generates a 256-bit key
    print(secret_key)
    ```
#### Database Configuration

- `DB_NAME`: The name of the SQLite database file.
- `DB_PATH`: Directory where the database file is stored.

#### Logging Configuration

- `DEBUG`: Set to `True` to enable debug mode.
- `LOG_LEVEL`: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
- `LOG_FILE`: Log file.

---

#### How to Use the `.env` File

1. Create a `.env` file in the project root.
2. Copy and paste the example content above.
3. Replace the placeholder values with your actual configuration.
4. *Jakanode-back* will automatically load these settings when it starts.

For further assistance, refer to the project's documentation or contact the maintainer. 🚀


## Database Migrations

To manage database schema changes and ensure your database is up-to-date with the latest structure,
*jakanode-bot* includes a migration system. This system allows you to automatically apply any pending migrations,
including creating new tables or altering existing ones.

### Creating SQLite3 Database

To create the SQLite3 database, run the following command from the root directory of the project. 
If the database doesn't exist, it will be automatically created:

```bash
sqlite3 db.sqlite3
```
Make sure that the database-related variables in the `.env` file are correctly configured. 
These variables define the database connection settings that *jakanode-bot* will use.

### Running Database Migrations

To execute all pending database migrations and apply any necessary changes to your database, 
run the following command from the root directory of your project:

```bash
python -m database.migrate
```
And verify that the changes have been applied successfully by checking the database:

```bash
sqlite3 db.sqlite3
```
```sql
.headers on
.mode column
SELECT * FROM migrations;
.tables
```

## Run

You can run *jakanode-back*
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
or
```bash
python main.py
```
Note: The `--reload` flag is useful in development but should be removed in production.

## Features

### Admin Features

**Only the admin can execute these commands**

#### /admin
#### /dashboard


### Public Features

#### /health
Returns API health status.