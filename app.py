import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from mysql.connector import IntegrityError
from werkzeug.security import generate_password_hash

from config import Config, get_db_connection

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Please provide both a username and a password.", "danger")
        return render_template("signup.html"), 400
    if len(username) > 100:
        flash("The username must be 100 characters or fewer.", "danger")
        return render_template("signup.html"), 400

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM tbl_user WHERE username = %s", (username,))
        if cursor.fetchone() is not None:
            flash("That username is already registered. Please choose another.", "danger")
            return render_template("signup.html"), 409

        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO tbl_user (username, password) VALUES (%s, %s)",
            (username, password_hash),
        )
        connection.commit()
    except IntegrityError:
        # unique database constraint to protects against simultaneous signups.
        if connection is not None:
            connection.rollback()
        flash("That username is already registered. Please choose another.", "danger")
        return render_template("signup.html"), 409
    except mysql.connector.Error:
        if connection is not None:
            connection.rollback()
        # exclude submitted form values or connector details in application logs.
        app.logger.error("Could not complete user registration because of a database error.")
        flash(
            "Registration could not be completed because the database is unavailable. "
            "Check your MySQL settings and try again.",
            "danger",
        )
        return render_template("signup.html"), 503
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    flash("Your account was created successfully.", "success")
    return redirect(url_for("signup"))


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
