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
    top_rated_movies = list(
        mongo_con.db.movies.find().sort("rating", -1).limit(5))
    newest_movies = list(mongo_con.db.movies.find().sort("year", -1).limit(5))
    recently_added_movies = list(mongo_con.db.movies.find().sort(
        "_id", -1).limit(5))
    return render_template(
        "index.html", recently_added_movies=recently_added_movies,
        newest_movies=newest_movies, top_rated_movies=top_rated_movies)


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
    movies = list(mongo_con.db.movies.find())
    if request.method == "POST":
        sub_list = list(mongo_con.db.movies.find(
            {"$text": {"$search": request.form.get("search")}}))
        ratings = []
        for movie in sub_list:
            if movie.get("rating"):
                ratings.append({"title": movie.get(
                    "title"), "rating": movie.get("rating")})
        return render_template(
            "findmovies.html", movies=sub_list, pages=None, ratings=ratings, post=True)
    if page == 1:
        sub_list = movies[0:10]
    else:
        start = page * 10 - 10
        end = start + 10
        sub_list = movies[start:end]
    counter = len(movies)
    counter = counter/10
    counter = math.ceil(counter)
    ratings = []
    for movie in sub_list:
        if movie.get("rating"):
            ratings.append({"title": movie.get(
                "title"), "rating": movie.get("rating")})
    return render_template(
        "findmovies.html", movies=sub_list, pages=counter, ratings=ratings)


@app.route("/findmovies/recent")
@app.route("/findmovies/recent/<int:page>")
def find_recent(page=1):
    movies = list(mongo_con.db.movies.find().sort(
        "_id", -1))
    if page == 1:
        sub_list = movies[0:10]
    else:
        start = page * 10 - 10
        end = start + 10
        sub_list = movies[start:end]
    counter = len(movies)
    counter = counter/10
    counter = math.ceil(counter)
    ratings = []
    for movie in sub_list:
        if movie.get("rating"):
            ratings.append({"title": movie.get(
                "title"), "rating": movie.get("rating")})
    return render_template(
        "findrecent.html", movies=sub_list,
        pages=counter, ratings=ratings)


@app.route("/findmovies/rating")
@app.route("/findmovies/rating/<int:page>")
def find_rating(page=1):
    movies = list(mongo_con.db.movies.find().sort(
        "rating", -1))
    if page == 1:
        sub_list = movies[0:10]
    else:
        start = page * 10 - 10
        end = start + 10
        sub_list = movies[start:end]
    counter = len(movies)
    counter = counter/10
    counter = math.ceil(counter)
    ratings = []
    for movie in sub_list:
        if movie.get("rating"):
            ratings.append({"title": movie.get(
                "title"), "rating": movie.get("rating")})
    return render_template(
        "findrating.html", movies=sub_list,
        pages=counter, ratings=ratings)


@app.route("/findmovies/year")
@app.route("/findmovies/year/<int:page>")
def find_year(page=1):
    movies = list(mongo_con.db.movies.find().sort(
        "year", -1))
    if page == 1:
        sub_list = movies[0:10]
    else:
        start = page * 10 - 10
        end = start + 10
        sub_list = movies[start:end]
    counter = len(movies)
    counter = counter/10
    counter = math.ceil(counter)
    ratings = []
    for movie in sub_list:
        if movie.get("rating"):
            ratings.append({"title": movie.get(
                "title"), "rating": movie.get("rating")})
    return render_template(
        "findyear.html", movies=sub_list,
        pages=counter, ratings=ratings)


@app.route("/moviepage/<title>", methods=["GET", "POST"])
def movie_page(title):
    get_movie = mongo_con.db.movies.find_one({"title": title})
    has_rating = get_movie.get("rating")
    return render_template(
        "moviepage.html", get_movie=get_movie, rating=has_rating)


@app.route("/moviepage/delete_movie/<title>", methods=["GET", "POST"])
def delete_movie(title):
    if request.method == "POST" and session["admin"]:
        mongo_con.db.movies.delete_one({"title": title})
        flash("Movie was deleted")
    return redirect(url_for("index"))


@app.route("/moviepage/rate/<title>", methods=["GET", "POST"])
def rate_movie(title):
    if request.method == "POST" and session["user"]:
        get_movie = mongo_con.db.movies.find_one({"title": title})
        has_rating = get_movie.get("ratings")
        check_rating_exists = get_movie.get("rated_by_users")
        if check_rating_exists:
            for user in check_rating_exists:
                if user == session["user"]:
                    flash("You have already rated this movie")
                    return redirect(url_for(
                        "movie_page", title=get_movie.get("title")))
        new_rating = None
        if has_rating:
            new_rating = (float(has_rating) + float(
                request.form.get("rating")))/2
        else:
            new_rating = float(request.form.get("rating"))
        user = session["user"]
        mongo_con.db.movies.update_one(
            {"title": title}, {
                "$push": {"rated_by_users": user}})
        mongo_con.db.movies.update_one({"title": title}, {
            "$set": {"rating": new_rating}
        })
        flash("Your rating was added")
        return redirect(url_for(
                        "movie_page", title=get_movie.get("title")))
    return redirect(url_for("index"))


@app.route("/moviepage/review/<title>", methods=["GET", "POST"])
def review_movie(title):
    get_movie = mongo_con.db.movies.find_one({"title": title})
    has_review = get_movie.get("reviews")
    if request.method == "POST" and session["user"]:
        if has_review:
            for review in has_review:
                if review["by_user"] == session["user"]:
                    flash("You have already made a review for this movie")
                    return redirect(url_for(
                        "movie_page", title=get_movie.get("title")))
        mongo_con.db.movies.update_one(
            {"_id": ObjectId(get_movie["_id"])}, {
                "$addToSet": {"reviews": {"description": request.form.get(
                    "review"), "by_user": session["user"]}}})
        flash("Your review was added")
        return redirect(url_for("movie_page", title=get_movie.get("title")))
    return redirect(url_for("index"))


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
    if session["admin"]:
        this_date = datetime.datetime.now()
        this_year = this_date.year
        return render_template("addmovie.html", this_year=this_year)
    else:
        return redirect(url_for("index"))


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
        return redirect(url_for("movie_page", title=title))
    if session["admin"]:
        get_movie = mongo_con.db.movies.find_one({"title": title})
        temp = get_movie.get("cast")
        cast_string = ""
        if temp:
            for memeber in temp:
                cast_string += memeber
                cast_string += ","
        cast_string = cast_string[0:-1]
        return render_template(
            "editmovie.html", get_movie=get_movie, get_cast=cast_string)
    else:
        return redirect(url_for("index"))


@app.errorhandler(404)
def no_such_page(error):
    return render_template("404.html", error=error)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(
        os.environ.get("PORT")), debug=True)
