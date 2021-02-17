import os
import math
import datetime
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
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
@app.route("/index", methods=['GET', 'POST'])
def index():

    movies = mongo_con.db.movies.find()
    return render_template("index.html", movies=movies)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
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
        return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
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
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("admin", None)
    flash("You have been logged out")
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
    ratings = []
    count = 0
    for i in movies:
        if i.get("ratings"):
            print(i.get("ratings"))
            for j in i.get("ratings"):
                print(j.get("rating"))
                count += float(j.get("rating"))
            ratings.append({"title": i.get(
                "title"), "rating": count/len(i.get("ratings"))})
            count = 0
    counter = len(movies)
    counter = counter/10
    counter = math.ceil(counter)
    return render_template(
        "findmovies.html", movies=sub_list, pages=counter, ratings=ratings)


@app.route("/moviepage/<title>/<rating>/<rate>", methods=["GET", "POST"])
@app.route("/moviepage/<title>/<delete_movie>", methods=["GET", "POST"])
@app.route("/moviepage/<title>", methods=["GET", "POST"])
def movie_page(title, delete_movie=False, rating=False, rate=False):
    get_movie = mongo_con.db.movies.find_one({"title": title})
    get_rating = get_movie.get("ratings")
    count = 0
    if get_rating:
        for i in get_rating:
            count += float(i.get("rating"))
        count = count/len(get_rating)

    if request.method == "POST" and session["admin"] and delete_movie:
        mongo_con.db.movies.delete_one({"title": title})
        flash("Movie was deleted")
        return redirect(url_for("index"))

    if request.method == "POST" and session["user"] and rating and rate:
        check_rating = mongo_con.db.movies.find_one({"title": title})
        if check_rating.get("rating"):
            for rating in check_rating["review"]:
                rating["by_user"]
                if rating["by_user"] == session["user"]:
                    flash("You have already rated this movie")
                    return redirect(url_for("index"))
        mongo_con.db.movies.update_one(
            {"title": title}, {
                "$addToSet": {"ratings": {"rating": request.form.get(
                    "rating"), "by_user": session["user"]}}})
        flash("Your rating was added")
        return redirect(url_for("index"))

    if request.method == "POST" and session["user"]:
        check_reviews = mongo_con.db.movies.find_one({"title": title})
        for review in check_reviews["reviews"]:
            review["by_user"]
            if review["by_user"] == session["user"]:
                flash("You have already made a review for this movie")
                return redirect(url_for("index"))
        mongo_con.db.movies.update_one(
            {"_id": ObjectId(get_movie["_id"])}, {
                "$addToSet": {"reviews": {"description": request.form.get(
                    "review"), "by_user": session["user"]}}})
        flash("Your review was added")
        return redirect(url_for("index"))

    return render_template(
        "moviepage.html", get_movie=get_movie, count=count)


@app.route("/addmovie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST" and session["admin"]:
        already_exist = mongo_con.db.movies.find_one(
            {"title": request.form.get("title")})
        if already_exist:
            flash("Movie already added to database")
            return redirect(url_for("index"))
        else:
            cast_list = list(request.form.get("cast").split(","))
            mongo_con.db.movies.insert_one(
                {"title": request.form.get(
                    "title"), "directors": request.form.get(
                        "directors"), "year": request.form.get(
                            "year"), "cast": cast_list, "img_url":
                                request.form.get("img_url")})
            flash("Movie Added")
            return redirect(url_for("index"))
    this_date = datetime.datetime.now()
    this_year = this_date.year
    return render_template("addmovie.html", this_year=this_year)


@app.route("/deletereview/<title>/<user>", methods=["GET", "POST"])
def delete_review(title, user):
    if request.method == "POST" and (
            user == session["user"] or session["admin"]):
        mongo_con.db.movies.update_one(
                {"title": title}, {"$pull": {"reviews": {"by_user": user}}})
        flash("Review deleted")
        return redirect(url_for("index"))
    else:
        flash("You are not authorized to make changes")
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/editmovie/<title>", methods=["GET", "POST"])
def edit_movie(title):
    if request.method == "POST" and session["admin"]:
        cast_list = list(request.form.get("cast").split(","))
        mongo_con.db.movies.update_one(
                {"title": title}, {"$set": {"title": request.form.get(
                    "title"), "directors": request.form.get(
                    "directors"), "year": request.form.get(
                    "year"), "cast": cast_list, "img_url":
                    request.form.get("img_url")}})
        flash("Movie Edited")
        return redirect(url_for("index"))
    get_movie = mongo_con.db.movies.find_one({"title": title})
    return redirect("index")

    temp = get_movie.get("cast")
    cast_string = ""
    if temp:
        for memeber in temp:
            cast_string += memeber
            cast_string += ","
        cast_string = cast_string[0:-1]
    return render_template(
        "editmovie.html", get_movie=get_movie, get_cast=cast_string)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(
        os.environ.get("PORT")), debug=True)
