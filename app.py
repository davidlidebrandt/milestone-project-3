import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo_con = PyMongo(app)


@app.route("/index/<choice>", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index(choice=None):
    if request.method == "POST" and choice == "login":
        user_exists = mongo_con.db.users.find_one(
            {"user_name": request.form.get("user-login").lower()})
        if user_exists:
            if request.form.get("password-login") == user_exists["password"]:
                session["user"] = user_exists["user_name"]
                name = session["user"]
                flash(f"Welcome {name}")
            else:
                flash("Incorrect username or password")
        else:
            flash("Incorrect username or password")
    elif request.method == "POST" and choice == "register":
        user_taken = mongo_con.db.users.find_one(
            {"user_name": request.form.get("user-reg")})
        if user_taken:
            flash("Username already taken")
        else:
            mongo_con.db.users.insert_one({"user_name": request.form.get(
                "user-reg").lower(), "password": request.form.get(
                    "password-reg").lower(), "user_email": request.form.get(
                        "email-reg"), "is_admin": "false"})
            reg_user = request.form.get("user-reg")
            session["user"] = request.form.get("user-reg")
            flash(f"Registration succesful, welcome {reg_user}")
    return render_template("index.html", choice=choice)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/findmovies/")
def find_movies():
    movies = mongo_con.db.movies.find()
    return render_template("findmovies.html", movies=movies)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(
        os.environ.get("PORT")), debug=True)
