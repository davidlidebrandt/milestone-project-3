import os
import math
import datetime
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for,
    )
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import choice
import string
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# This turtorial was used to help set up how to send emails:
# https://overiq.com/flask-101/sending-email-in-flask/
app.config["MAIL_SERVER"] = "smtp.office365.com."
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
mongo_con = PyMongo(app)

mail = Mail(app)



def send_welcome(user, email):

    """
    Sends a welcome mail to newly registered users.
    Takes two arguments, user and email.
    """

    msg = Message(f"Welcome {user}",
                  sender="my-flask-manager@outlook.com", recipients=[email])
    msg.body = "Welcome to Movie Ratings And Reviews"
    mail.send(msg)


# Answer by user MSeifert was used to generate a random string
# https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits/41464693#41464693
def generate_random_string(length):

    """
    Generates a random string.
    Takes 1 argument, length.
    """

    reset_link = "".join([choice(string.ascii_uppercase + string.digits)
                         for i in range(length)])
    return reset_link


@app.route("/")
@app.route("/index")
def index():

    """
    Triggers when user accesses URL specified in route,
    retrives lists of movies from a database and
    renders a HTML template.
    """

    top_rated_movies = list(
        mongo_con.db.movies.find().sort("rating", -1).limit(5))
    newest_movies = list(mongo_con.db.movies.find().sort("year", -1).limit(5))
    recently_added_movies = list(mongo_con.db.movies.find().sort(
        "_id", -1).limit(5))
    return render_template(
        "index.html", recently_added_movies=recently_added_movies,
        newest_movies=newest_movies, top_rated_movies=top_rated_movies)


@app.route("/register", methods=["POST"])
def register():

    """
    Triggers when a user posts the register form.
    Checks if the user already exists, otherwise
    adds a new account and logs in the new user.
    """

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
        flash(f"""Registration succesful, welcome {reg_user}. A welcome mail has been sent,
        please check your junk mail box if you haven't recived it""")
        send_welcome(reg_user, request.form.get("email-reg"))
    return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def log_in():

    """
    Triggers when a user posts the log in form.
    Checks if username and password is correct and
    logs in a valid user or displays an error if incorrect.
    """

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

    """
    Triggers when the Log out button is pressed,
    Logs out the user and renders the index template.
    """

    session.pop("user", None)
    session.pop("admin", None)
    flash("You have been logged out")
    top_rated_movies = list(
        mongo_con.db.movies.find().sort("rating", -1).limit(5))
    newest_movies = list(mongo_con.db.movies.find().sort("year", -1).limit(5))
    recently_added_movies = list(mongo_con.db.movies.find().sort(
        "_id", -1).limit(5))
    return render_template(
        "index.html", recently_added_movies=recently_added_movies,
        newest_movies=newest_movies, top_rated_movies=top_rated_movies)


@app.route("/findmovies/")
@app.route("/findmovies/<int:page>")
def find_movies(page=1):

    """
    Triggers when the Findmovies link is pressed
    or user navigates the pagination buttons.
    Displays ten results at a time based on which
    page is loaded.
    """

    movies = list(mongo_con.db.movies.find())
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


@app.route("/findmvoies/search", methods=["POST"])
def search_movies():

    """
    Triggers when the search bar form is submitted.
    Searches for a match in the database.
    """

    if request.method == "POST":
        sub_list = list(mongo_con.db.movies.find(
            {"$text": {"$search": request.form.get("search")}}))
        ratings = []
        for movie in sub_list:
            if movie.get("rating"):
                ratings.append({"title": movie.get(
                    "title"), "rating": movie.get("rating")})
        return render_template(
            "findmovies.html", movies=sub_list,
            pages=None, ratings=ratings, post=True)


@app.route("/findmovies/recent")
@app.route("/findmovies/recent/<int:page>")
def find_recent(page=1):

    """
    Triggers when the movie list is displayed by date added.
    Sorts the movies by the date added in descending order.
    """

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

    """
    Triggers when the movie list is displayed by rating.
    Sorts the movies by rating in descending order.
    """

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

    """
    Triggers when the movie list is displayed by release year.
    Sorts the movies by release year in descending order.
    """

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


@app.route("/moviepage/<title>")
def movie_page(title):

    """
    Triggers when a user clicks a link for a
    particular movie.
    """

    get_movie = mongo_con.db.movies.find_one({"title": title})
    has_rating = get_movie.get("rating")
    return render_template(
        "moviepage.html", get_movie=get_movie, rating=has_rating)


@app.route("/moviepage/delete_movie/<title>", methods=["DELETE"])
def delete_movie(title):
    if request.method == "DELETE" and session["admin"]:
        mongo_con.db.movies.delete_one({"title": title})
        flash("Movie was deleted")
    return "Movie was deleted"


@app.route("/moviepage/rate/<title>", methods=["POST"])
def rate_movie(title):

    """
    Triggers when a rating is posted.
    Checks if a user is logged in and if they have rated
    the current movie before.
    """

    if request.method == "POST" and session["user"]:
        get_movie = mongo_con.db.movies.find_one({"title": title})
        has_rating = get_movie.get("rating")
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


@app.route("/moviepage/review/<title>", methods=["POST"])
def review_movie(title):

    """
    Triggers when a new review is posted.
    Checks if a user is logged in and if they
    have made a review for the current movie before.
    """

    if request.method == "POST" and session["user"]:
        get_movie = mongo_con.db.movies.find_one({"title": title})
        has_review = get_movie.get("reviews")
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

    """
    Get method triggers when an admin clicks the add movie button
    and renders a template for adding movies.
    Post method triggers when a admin submits the form for adding movies.
    """

    if request.method == "POST" and session["admin"]:
        already_exist = mongo_con.db.movies.find_one(
            {"title": request.form.get("title")})
        if already_exist:
            flash("Movie already exists")
            return redirect(url_for("index"))
        else:
            cast_list = list(request.form.get("cast").split(","))
            mongo_con.db.movies.insert_one(
                {"title": request.form.get(
                    "title").strip(), "directors": request.form.get(
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


@app.route("/deletereview/<title>/<user>", methods=["DELETE"])
def delete_review(title, user):

    """
    Triggers when the delete review button is pressed.
    Checks if the user sending the request is the same as
    the user that is logged in or is an admin. Deletes
    the review if true.
    """

    if user == session["user"] or session["admin"]:
        mongo_con.db.movies.update_one(
            {"title": title}, {"$pull": {"reviews": {"by_user": user}}})
        flash("Review deleted")
        return "Review deleted"


@app.route("/editreview/<title>/<user>/<description>", methods=["GET", "POST"])
def edit_review(title, user, description):

    """
    Triggers when a user presses the edit review button.
    Renders a template with a form prefilled with the
    old review.
    """

    if session["user"] == user:
        get_movie = mongo_con.db.movies.find_one({"title": title})
        return render_template(
            "editreview.html", get_movie=get_movie,
            description=description, user=user)
    return redirect(url_for("index"))


@app.route("/updatereview/<title>/<user>", methods=["PUT"])
def update_review(title, user):

    """
    Triggers when a logged in user submits an updated version
    of an already made review.
    """

    if user == session["user"]:
        mongo_con.db.movies.update_one(
            {"title": title, "reviews.by_user": user},
            {"$set": {"reviews.$.description": request.get_json(
            )["description"]}})
        flash("Your review was edited")
    return "Review updated"


@app.route("/editmovie/<title>", methods=["GET", "POST"])
def edit_movie(title):

    """
    Triggers when the edit movie button is pressed by an admin.
    Renders the editmovie template with the present values prefilled.
    Updates the movie fields upon submitting the form.
    """

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

    """
    Triggers when a page is not found or
    is sent a request with a method not allowed.
    """

    return render_template("404.html", error=error)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(
        os.environ.get("PORT")), debug=True)
