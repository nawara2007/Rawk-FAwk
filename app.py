import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]

    return render_template("index.html")

@app.route("/videos")
@login_required
def videos():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    return render_template("videos.html")

@app.route("/articles")
@login_required
def articles():
    all_articles = db.execute("SELECT * FROM articles");
    return render_template("articles.html", all_articles=all_articles)

@app.route("/addarticle", methods=["GET", "POST"])
@login_required
def addarticle():
    if request.method == "POST":
        if not request.form.get("title") or not request.form.get("article") or not request.form.get("source"):
            return apology("Please enter the full data")
        
        title = request.form.get("title")
        article = request.form.get("article")
        source = request.form.get("source")
            
        db.execute("INSERT INTO articles (title, article, source) VALUES (?, ?, ?)", title, article, source)

        return redirect("/addarticle")
    else:
        return render_template("addarticle.html")

@app.route("/doctors")
@login_required
def doctors():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    return render_template("doctors.html")

@app.route("/quizes")
@login_required
def quizes():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    return render_template("quizes.html")
 
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    if request.method == "POST":
        if not request.form.get("curr_password") or not request.form.get("new_password") or not request.form.get("confirm_password"):
            return apology("Please enter the passwords")
        
        if request.form.get("new_password") != request.form.get("confirm_password"):
            return apology("The passwords doesnot match")
        
        user_id = session["user_id"]
        curr_password = db.execute("Select hash FROM users WHERE id = ?", user_id)[0]["hash"]


        if check_password_hash(curr_password, request.form.get("curr_password")):
            if check_password_hash(curr_password, request.form.get("new_password")):
                return apology("It is already your password")
            
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(request.form.get("new_password")), user_id)

            return redirect("/")
        else:
            return apology("your current password is incorrect")

    else:
        return render_template("password.html")
    


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        elif not request.form.get("confirm_password") or request.form.get("password") != request.form.get("confirm_password"):
            return apology("The password does not match", 403)
        
        checker = db.execute("Select * FROM users WHERE username = ?", request.form.get("username"))

        if len(checker) == 0:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username") , generate_password_hash(request.form.get("password")))

            session["user_id"] = db.execute("Select id FROM users WHERE username = ?", request.form.get("username"))

            return redirect("/login")
        else:
            return apology("This user is already registered", 403)
        
    else:
        return render_template("register.html")

app.run(host="0.0.0.0", port=8050, threaded=True)
