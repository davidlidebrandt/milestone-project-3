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


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        user_exists = mongo_con.db.users.find_one(
            {"user_name": request.form.get("user-login").lower()})
        if user_exists:
            if request.form.get("password-login") == user_exists["password"]:
                session["user"] = user_exists["user_name"]
                name = session["user"]
                flash(f"Welcome {name}")
    return render_template("index.html")


@app.route("/findmovies")
def find_movies():
    return render_template("findmovies.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(
        os.environ.get("PORT")), debug=True)
