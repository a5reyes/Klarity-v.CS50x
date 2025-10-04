import os

from cs50 import SQL
from datetime import date, datetime
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology
import requests

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///klarity.db")

load_dotenv(".env.dev")
api_key = os.getenv("API_KEY")
search_url = os.getenv("SEARCH_URL")

@app.route("/")
def homepage():
    return render_template("home.html")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)
        session["user_id"] = rows[0]["id"]
        flash("You have successfully logged in.")
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif password != confirm:
            return apology("please confirm password", 400)
        else:
            if db.execute("SELECT * FROM users WHERE username = ?", username):
                return apology("username already taken", 400)
            else:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                           username, generate_password_hash(password))
                flash("You have successfully registered. Please login in.")
                return redirect("/")
    else:
        return render_template("register.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        name = request.form.get("name")
        bmi = request.form.get("bmi")
        fitnesslvl = request.form.get("fitnesslvl")
        age = request.form.get("age")
        weight = request.form.get("weight")
        if not name:
            return apology("must provide name", 400)
        elif not fitnesslvl:
            return apology("please confirm fitness level", 400)
        elif not age:
            return apology("please confirm age", 400)
        elif not weight:
            return apology("must provide weight", 400)
        else:
            username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
            # check if profile already exists then if so, update the fields chosen
            try:
                profile_exists = db.execute("SELECT name, bmi, fitnesslvl, age, weight FROM profiles WHERE id = ?", session["user_id"])[0]
                for field_name in profile_exists:
                    field = request.form.get(field_name)
                    if field_name == "bmi" or field_name == "age" or field_name == "weight":
                        field = int(request.form.get(field_name))
                    if profile_exists[field_name] != field:
                         db.execute("UPDATE profiles SET ? = ? WHERE id = ?", field_name, field, session["user_id"])
            except:
                db.execute("INSERT INTO profiles (id, username, name, bmi, fitnesslvl, age, weight) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], username, name, bmi, fitnesslvl, age, weight)
            flash("You have successfully updated your profile.")
            return redirect("/")
    else:
        return render_template("profile.html")


@app.route("/focus", methods=["GET", "POST"])
def focus():
    if request.method == "POST":
        location = request.form.get("location")
        focus = request.form.get("focus")
        #insert into database, location, focus
        try:
            db.execute("SELECT fitnesslvl FROM profiles WHERE id = ?", session["user_id"])[0]["fitnesslvl"]
            db.execute("SELECT weight FROM profiles WHERE id = ?", session["user_id"])[0]["weight"]
        except:
            return apology("please create profile", 400)
        return render_template("muscles.html", location=location, focus=focus)
    else:
        return render_template("focus.html")

@app.route("/exercises")
def exercises():
    videos = []
    if not request.args:
        return apology("please create profile and focus", 400)
    today = date.today()
    muscle = request.args.get("muscle")
    location = request.args.get("location")
    focus = request.args.get("focus")
    fitnesslvl = db.execute("SELECT fitnesslvl FROM profiles WHERE id = ?", session["user_id"])[0]["fitnesslvl"]
    weight = db.execute("SELECT weight FROM profiles WHERE id = ?", session["user_id"])[0]["weight"]
    #make sure a new workout isn't added everytime the user refreshes the page
    if not db.execute("SELECT * FROM workouts WHERE id = ? AND fitnesslvl = ? AND weight = ? AND location = ? AND focus = ? AND muscle = ? AND day = ? AND month = ? AND year = ?", session["user_id"], fitnesslvl, weight, location, focus, muscle, int(today.day), int(today.month), int(today.year)):
        db.execute("INSERT INTO workouts (id, fitnesslvl, weight, location, focus, muscle, day, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], fitnesslvl, weight, location, focus, muscle, int(today.day), int(today.month), int(today.year))
    #using youtube api to get short videos based on fitnesslvl, muscle and focus - ex. beginner abs warm-up
    params = { "part":"snippet", "q": f"{fitnesslvl} {muscle} {focus} exercises", "type": "video", "videoDuration": "short", "maxResults": 15, "key": api_key}
    response = requests.get(search_url, params=params)
    results = response.json()
    if response.status_code == 200:
        for item in results["items"]:
            videos.append(f"{item['id']['videoId']}")
    else:
        return apology("trouble accessing videos", 400)
    return render_template("videos.html", muscle=muscle, videos=videos)

@app.route("/plan", methods=["GET"])
def plan():
    today = date.today()
    month = today.month
    year = today.year
    try:
        days = {i: datetime(year, month, i).strftime("%A") for i in range(1, 32)}
    except:
        try:
            days = {i: datetime(year, month, i).strftime("%A") for i in range(1, 31)}
        except:
            try:
                days = {i: datetime(year, month, i).strftime("%A") for i in range(1, 30)}
            except:
                days = {i: datetime(year, month, i).strftime("%A") for i in range(1, 29)}
    month_name = datetime(year, month, day=1).strftime("%B")
    workout_day = request.args.get("day")
    workout_month = request.args.get("month")
    workout_year = request.args.get("year")
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    if workout_day and workout_month and workout_year:
        workouts = db.execute("SELECT * FROM workouts WHERE id = ? AND day = ? AND month = ? AND year = ?", session["user_id"], workout_day, workout_month, workout_year)
    else:
        workouts = ""
    return render_template("plan.html", year=year, month=month, month_name=month_name, days=days, workouts=workouts, username=username)
