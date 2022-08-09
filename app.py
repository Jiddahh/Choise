from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_session import Session
from tempfile import mkdtemp
from flask.helpers import get_flashed_messages
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import os

# configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# configure session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///choise.db'

# initialize database
db = SQLAlchemy(app)

# create database model
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<users {self.username}>"

    
@app.route("/")
def index():
    """show homepage"""
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get username and password from form
        username_submitted = request.form.get("username")
        password_submitted = request.form.get("pasword")

        # Query database for user
        user = users.query.filter_by(username=username_submitted).first()

        # Ensure a username was submitted 
        if not username_submitted or password_submitted:
            flash("must provide username and password", category="error")
            return redirect("/register")

        # Ensure the username doesn't exist 
        elif len(user) != 0:
            flash("username alredy exists", category="error")
            return redirect("/register")
        
        else:
            # Hash password
            hash = generate_password_hash(password_submitted)

            # Insert new user into database
            new_user = users(username=username_submitted, password=hash)

            try:
                db.session.add(new_user)
                db.session.commit()
                # Redirect user to homepage
                return redirect("/")
            except:
                return "error signing you up"

    # User reached route via GET (as by clicking a link or redirect) 
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """Log user in"""

    # Forget any user_id 
    session.clear()

    # User reached route via POST(as by submitting a form via POST)
    if request.method == "POST":

        # Get username and password from form
        username_submitted = request.form.get("username")
        password_submitted = request.form.get("pasword")

        # Ensure username and password was submitted
        if not username_submitted or not password_submitted:
            flash("username and password must be provided", category="error")
            return redirect("/login")

        # Query database for user
        user = users.query.filter_by(username=username_submitted).first()
        hash = user.password

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(hash, password_submitted):
            flash("invalid username and/or password", category="error")
            return redirect("/login")
            
        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET(as by clicking a link or redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect("/")

# @app.errorhandler(404)
# def not_found(e):
#     return render_template("404.html"), 404      

if __name__ == "__main__":
    app.run(debug=True)