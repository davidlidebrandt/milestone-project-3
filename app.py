import os
import math
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
            if check_password_hash(user_exists["password"],
                                   request.form.get("password-login")):
                session["user"] = user_exists["user_name"]
                if user_exists["is_admin"] == "true":
                    session["admin"] = True
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
                "user-reg").lower(), "password": generate_password_hash(
                    request.form.get(
                        "password-reg").lower(), method='pbkdf2:sha256',
                salt_length=12), "user_email": request.form.get(
                                "email-reg"), "is_admin": "false"})
            reg_user = request.form.get("user-reg")
            session["user"] = request.form.get("user-reg")
            flash(f"Registration succesful, welcome {reg_user}")
    movies = mongo_con.db.movies.find()
    return render_template("index.html", choice=choice, movies=movies)


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("admin", None)
    return redirect(url_for("index"))


@app.route("/findmovies/", methods=["GET", "POST"])
@app.route("/findmovies/<int:page>", methods=["GET", "POST"])
def find_movies(page=1):
    if request.method == "POST":
        movies = list(mongo_con.db.movies.find(
            {"$text": {"$search": request.form.get("search")}}))
        return render_template("findmovies.html", movies=movies, pages=None)
    movies = list(mongo_con.db.movies.find())
    if page == 1:
        sub_list = movies[0:10]
    else:
        start = page * 10 - 10
        end = start + 10
        sub_list = movies[start:end]
    counter = 0
    for movie in movies:
        counter += 1
    counter = counter/10
    counter = math.ceil(counter)
    return render_template("findmovies.html", movies=sub_list, pages=counter)


@app.route("/moviepage/<title>", methods=["GET", "POST"])
def movie_page(title):
    get_movie = mongo_con.db.movies.find_one({"title": title})
    if request.method == "POST" and session["user"]:
        mongo_con.db.movies.update_one(
            {"_id": ObjectId(get_movie["_id"])}, {
                "$addToSet": {"reviews": {"description": request.form.get(
                    "review"), "by_user": session["user"]}}})
        return render_template(
            "moviepage.html", get_movie=get_movie)
    return render_template(
        "moviepage.html", get_movie=get_movie)




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(
        os.environ.get("PORT")), debug=True)
