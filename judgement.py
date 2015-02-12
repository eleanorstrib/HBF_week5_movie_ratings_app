from flask import Flask, render_template, redirect, request, g, url_for, flash, make_response 
from flask import session as f_sess
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key='\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined #this throws an error if a var is undefined

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(25).all()
    return render_template("user_list.html", users=user_list)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
    print "login func running"
    email = request.form['email']
    password = request.form['password']
    print (email, password)

    login_user = model.session.query(model.User.email, model.User.id).filter(model.User.email == email).all()   #get back a list with a tuple in it (email, user id)
    print login_user
    if email == login_user[0][0]:
        if 'client' not in f_sess:
            f_sess['client'] = []
            f_sess['client'] = [email,login_user[0][1]]
    print f_sess
    flash(email + " is logged in.")

    return redirect("/movielistings")

@app.route("/userdetail/<int:id>")
def get_user_details(id):
    this_user = model.session.query(model.User).get(id)
    this_user_ratings = model.session.query(model.User.id, model.Rating.rating, 
        model.Movie.title).join(model.Rating,model.Movie).filter(model.User.id == id).all() # get movie title, user's rating for each title
    return render_template("user_details.html",this_user=this_user, 
        this_user_ratings=this_user_ratings)

@app.route("/movielistings")
def show_movie_listings():
    movie_info = model.session.query(model.Movie.id, model.Movie.title, model.Movie.url).limit(25).all()
    return render_template("movie_listings.html", movie_info=movie_info)

@app.route("/moviedetail/<int:id>")
def get_movie_details(id):
    movie_info = model.session.query(model.Movie.title, model.Movie.rel_date, model.Movie.url, model.Movie.id).filter(model.Movie.id==id).all()
    print movie_info
    movie_date = (movie_info[0][1]).strftime("%B %d, %Y")
    print movie_date
    return render_template("movie_detail.html", movie_info=movie_info, movie_date=movie_date)

@app.route("/addrating/<int:id>", methods=["POST"])
def add_rating(id):
    new_rating = model.Rating(user_id = f_sess['client'][1],
                        movie_id = id, rating = request.form['rating'])
    model.session.add(new_rating)
    model.session.commit()
    flash("You rated the movie " + request.form['rating'] + " stars!")
    return redirect('/movielistings')

if __name__ == "__main__":
    app.run(debug = True)