# Flask User Auth

A small Flask application with a Bootstrap homepage and a signup form. It stores usernames and Werkzeug password hashes in a MySQL table named `tbl_user`.

## Prerequisites

- Python 3.10 or later
- MySQL Server and the MySQL command-line client (or another way to run SQL files)

## 1. Create and activate a virtual environment

Open PowerShell in this project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python directly with `\.venv\Scripts\python.exe`.

## 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Create the database and table

Make sure the MySQL server is running, then execute the included SQL file. Replace `root` if your MySQL account has a different username:

```powershell
Get-Content .\database.sql | mysql -u root -p
```

The script creates the `flask_user_auth` database and the `tbl_user` table. It is safe to run again if they already exist.

## 4. Configure environment variables

Copy the example file to `.env` and edit it with your local MySQL details:

```powershell
Copy-Item .env.example .env
```

Set `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`. Replace `SECRET_KEY` with a long random value. For example, generate one with:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the generated value into `.env`. The `.env` file is ignored by Git and should not be shared.

## 5. Run the application

```powershell
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Bootstrap is loaded from its CDN, so an internet connection is needed for its styling.

## 6. Register a user

Select **Sign up**, enter a username and password, and submit the form. The server checks both fields, rejects duplicate usernames, hashes the password, and inserts the values using a parameterized SQL statement.

To verify the stored value in MySQL, run:

```sql
USE flask_user_auth;
SELECT id, username, password, created_at FROM tbl_user;
```

The `password` column should contain a Werkzeug hash (typically beginning with `scrypt:`), not the password you entered.

## Database availability

The homepage and signup form can be opened without a running database. Submitting a valid signup requires a reachable MySQL server, the database and table above, and correct values in `.env`. If MySQL is unavailable, the form shows a database connection message and the application logs the underlying error without logging submitted passwords.
