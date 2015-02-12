from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(25).all()
    return render_template("user_list.html", users=user_list)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/userdetail/<int:id>")
def get_user_details(id):
    this_user = model.session.query(model.User).get(id)
    this_user_ratings = model.session.query(model.User.id, model.Rating.rating, 
        model.Movie.title).join(model.Rating,model.Movie).filter(model.User.id == id).all() # get movie title, user's rating for each title
    return render_template("user_details.html",this_user=this_user, 
        this_user_ratings=this_user_ratings)

@app.route("/movielisting")
def show_movie_listings():
    movie_info = model.session.query(model.Movie.id, model.Movie.title, model.Movie.url).limit(25).all()
    print movie_info
    return render_template("movie_listings.html", movie_info=movie_info)

@app.route("/moviedetail/<int:id>")
def get_movie_details(id):
    return render_template("movie_detail.html")

@app.route("/addrating")
def add_rating():
    pass

if __name__ == "__main__":
    app.run(debug = True)