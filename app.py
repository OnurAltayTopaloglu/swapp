import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.security import check_password_hash, generate_password_hash
import urllib.request
from werkzeug.utils import secure_filename
import psycopg2  # pip install psycopg2 <-#or#-> pip install psycopg2-binary
import psycopg2.extras

from helpers import (
    apology,
    login_required,
    lookup,
    usd,
    apology_login,
    apology_register,
)

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///swapp.db")

# Uploading necessities
UPLOAD_FOLDER = "static/uploads/"
app.secret_key = "secret key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

colors = [
    "Aqua",
    "Black",
    "Blue",
    "Fuchsia",
    "Gray",
    "Green",
    "Lime",
    "Maroon",
    "Navy",
    "Olive",
    "Purple",
    "Red",
    "Silver",
    "Teal",
    "White",
    "Yellow",
]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/search", methods=["GET"])
@login_required
def search():
    return render_template("search.html", colors=colors)

@app.route("/search", methods=["POST"])
@login_required
def searched():
    if not request.form.get("color") and not request.form.get("condition"):
        flash("Please select an option.")
        return render_template("search.html", colors=colors)
    if not request.form.get("condition"):
        items = db.execute(
            "SELECT * FROM upload WHERE color = (?)", request.form.get("color")
        )
        if items:
            flash("{} colored items".format(request.form.get("color")))
        else:
            flash("There is no such item.")
        return render_template("search.html", items=items, colors=colors)
    if not request.form.get("color"):
        items = db.execute(
            "SELECT * FROM upload WHERE condition = (?)", request.form.get("condition")
        )
        if items:
            flash("{} items".format(request.form.get("condition")))
        else:
            flash("There is no such item.")
        return render_template("search.html", items=items, colors=colors)
    else:
        items = db.execute(
            "SELECT * FROM upload WHERE condition = (?) AND color = (?)",
            request.form.get("condition"),
            request.form.get("color"),
        )
        if items:
            flash(
                "{} {} items".format(
                    request.form.get("condition"), request.form.get("color")
                )
            )
        else:
            flash("There is no such item.")
        return render_template("search.html", items=items, colors=colors)


@app.route("/")
@login_required
def home():
    items = db.execute("SELECT * FROM upload")
    return render_template("index.html", items=items)


@app.route("/my_items")
@login_required
def my_items():
    """Show history of transactions"""
    items = db.execute(
        "SELECT title,name,brand,color, condition FROM upload WHERE user_id = ?",
        session["user_id"],
    )
    return render_template("my_items.html", items=items)


@app.route("/sell", methods=["POST"])
@login_required
def upload_image():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)
    if not request.form.get("name"):
        flash("Please enter the name of the item")
        return redirect(request.url)
    if not request.form.get("brand"):
        flash("Please enter the brand of the item")
        return redirect(request.url)
    if not request.form.get("color"):
        flash("Please enter the color of the item")
        return redirect(request.url)
    if not request.form.get("condition"):
        flash("Please enter the condition of the item")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        db.execute(
            "INSERT INTO upload (title, user_id, username, name, brand, color, condition) VALUES (?,?,?,?,?,?,?)",
            filename,
            session["user_id"],
            session["name"],
            request.form.get("name").capitalize(),
            request.form.get("brand").capitalize(),
            request.form.get("color"),
            request.form.get("condition"),
        )

        flash("Image successfully uploaded and displayed below")
        items = db.execute(
            "SELECT title,name,brand,color, condition FROM upload WHERE user_id = ?",
            session["user_id"],
        )
        return render_template("my_items.html", items=items)
    else:
        flash("Allowed image types are - png, jpg, jpeg, gif")
        return redirect(request.url)


@app.route("/sell", methods=["GET"])
@login_required
def sells():
    return render_template("sell.html", colors=colors)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology_login("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology_login("Must provide password", 405)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology_login("Invalid username or password", 405)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["name"] = request.form.get("username")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology_register("Must provide username", 401)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology_register("must provide password", 402)

        # Ensure password is the same with confirmation
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology_register("Passwords must match", 403)
        # Ensure username is not taken
        taken = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(taken) == 1:
            return apology_register("Username taken", 401)
        else:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?,?)",
                request.form.get("username"),
                generate_password_hash(request.form.get("password")),
            )
            return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/display/<filename>")
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


if __name__ == "__main__":
    app.run()
