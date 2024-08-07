from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

from helpers import apology, login_required, superuser_required

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
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    return render_template("index.html", user=user)

@app.route("/videos")
@login_required
def videos():
    all_comments = db.execute("SELECT * FROM comments")
    all_videos = db.execute("SELECT * FROM videos")

    return render_template("videos.html", all_videos=all_videos, all_comments=all_comments)

@app.route("/articles")
@login_required
def articles():
    all_articles = db.execute("SELECT * FROM articles")
    all_comments = db.execute("SELECT * FROM comments")

    return render_template("articles.html", all_articles=all_articles, all_comments=all_comments)

@app.route("/editarticles")
@login_required
@superuser_required
def editarticles():
    return render_template("editarticles.html")

@app.route("/editvideos")
@login_required
@superuser_required
def editvideos():
    return render_template("editvideos.html")

@app.route("/addarticle", methods=["POST"])
@login_required
@superuser_required
def addarticle():
    if not request.form.get("title") or not request.form.get("article") or not request.form.get("source"):
        return apology("Please enter the full data")
    
    title = request.form.get("title")
    article = request.form.get("article")
    source = request.form.get("source")
        
    db.execute("INSERT INTO articles (title, article, source) VALUES (?, ?, ?)", title, article, source)

    return redirect("/editarticles")
    
@app.route("/addvideo", methods=["POST"])
@login_required
@superuser_required
def addvideo():
    if not request.form.get("title") or not request.form.get("url"):
        return apology("Please enter the full data")
    
    title = request.form.get("title")
    url = request.form.get("url")
        
    db.execute("INSERT INTO videos (title, url) VALUES (?, ?)", title, url)

    return redirect("/editvideos")

@app.route("/deletevideo", methods=["POST"])
@login_required
@superuser_required
def deletevideo():
    if not request.form.get("id"):
        return apology("Please enter the full data")
    
    id = request.form.get("id")
        
    db.execute("DELETE FROM videos WHERE id = ?", id)

    return redirect("/editvideos")

@app.route("/deletearticle", methods=["POST"])
@login_required
@superuser_required
def deletearticle():
    if not request.form.get("id"):
        return apology("Please enter the full data")
    
    id = int(request.form.get("id"))
        
    db.execute("DELETE FROM articles WHERE id = ?", id)

    return redirect("/editarticles")

@app.route("/doctors")
@login_required
def doctors():
    all_doctors = db.execute("SELECT * FROM doctors")

    return render_template("doctors.html", all_doctors=all_doctors)

@app.route("/tests", methods=["POST", "GET"])
@login_required
def tests():
    if request.method == "POST":
        questions = db.execute("SELECT * FROM questions")
        result = 0
        user_id = session["user_id"]

        for i in questions:
            result += int(request.form.get(str(i["id"])))
        
        if result == 0 and result <= 4:
            db.execute("UPDATE users SET status= ? Where id = ?", "Minimal Anxiety", user_id)
        elif result >= 5 and result <= 9:
            db.execute("UPDATE users SET status= ? Where id = ?", "Mild Anxiety", user_id)
        elif result >= 10 and result <= 14:
           db.execute("UPDATE users SET status= ? Where id = ?", "Moderate Anxiety", user_id)
        elif result >= 15 and result <= 21:
            db.execute("UPDATE users SET status= ? Where id = ?", "Severe Anxiety", user_id)

        return redirect("/")
    else:
        all_questions = db.execute("SELECT * FROM questions")
        return render_template("tests.html", all_questions=all_questions)

@app.route("/comment", methods=["POST"])
@login_required
def comment():
    if not request.form.get("name") or not request.form.get("comment"):
            return apology("Please enter the full data")
    
    name = request.form.get("name")
    comment = request.form.get("comment")
    the_date = date.today()

    db.execute("INSERT INTO comments (username, comment, date) VALUES (?, ?, ?)", name, comment, the_date)

    return redirect("/articles")

@app.route("/editdoctors")
@login_required
@superuser_required
def editdoctors():
    return render_template("editdoctors.html")

@app.route("/adddoctor", methods=["POST"])
@login_required
@superuser_required
def adddoctor():
    if not request.form.get("name") or not request.form.get("address") or not request.form.get("rate") or not request.form.get("picture") or not request.form.get("email"):
        return apology("Please enter the full data")
    
    name = request.form.get("name")
    address = request.form.get("address")
    rate = request.form.get("rate")
    picture = request.form.get("picture")
    email = request.form.get("email")

        
    db.execute("INSERT INTO doctors (name, address, rate, picture, email) VALUES (?, ?, ?, ?, ?)", name, address, rate, picture, email)

    return redirect("/editdoctors")

@app.route("/deletedoctor", methods=["POST"])
@login_required
@superuser_required
def deletedoctor():
    if not request.form.get("id"):
        return apology("Please enter the full data")
    
    id = request.form.get("id")
        
    db.execute("DELETE FROM doctors WHERE id = ?", id)

    return redirect("/editdoctors")

@app.route("/editquestions")
@login_required
@superuser_required
def editquestions():
    return render_template("editquestions.html")

@app.route("/addquestion", methods=["POST"])
@login_required
@superuser_required
def addquestion():
    if not request.form.get("question") or not request.form.get("test_no"):
        return apology("Please enter the full data")
    
    question = request.form.get("question")
    test_no = request.form.get("test_no")

        
    db.execute("INSERT INTO questions (question, test_no) VALUES (?, ?)", question, test_no)

    return redirect("/editquestions")

@app.route("/deletequestion", methods=["POST"])
@login_required
@superuser_required
def deletequestion():
    if not request.form.get("id"):
        return apology("Please enter the full data")
    
    id = request.form.get("id")
        
    db.execute("DELETE FROM questions WHERE id = ?", id)

    return redirect("/editquestions")

@app.route("/deletecomment", methods=["POST", "GET"])
@login_required
@superuser_required
def deletecomment():
    if request.method == "POST":
        if not request.form.get("id"):
            return apology("Please enter the full data")
        
        id = request.form.get("id")
            
        db.execute("DELETE FROM comments WHERE id = ?", id)

        return redirect("/deletecomment")
    else:
        return render_template("deletecomment.html")
    
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

        elif not request.form.get("age") or int(request.form.get("age")) > 90 or int(request.form.get("age")) < 10:
            return apology("Enter a valid age", 403)
        
        checker = db.execute("Select * FROM users WHERE username = ?", request.form.get("username"))

        if len(checker) == 0:
            db.execute("INSERT INTO users (username, hash, age) VALUES (?, ?, ?)", request.form.get("username") , generate_password_hash(request.form.get("password")), request.form.get("age"))

            session["user_id"] = db.execute("Select id FROM users WHERE username = ?", request.form.get("username"))

            return redirect("/login")
        else:
            return apology("This user is already registered", 403)
        
    else:
        return render_template("register.html")

app.run(host="0.0.0.0", port=8080, threaded=True)
