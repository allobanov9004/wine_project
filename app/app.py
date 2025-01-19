from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Wine, User
from werkzeug.security import generate_password_hash

from db import db_session

from flask_login import LoginManager, login_user, current_user




app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/catalog")
def catalog():
    wines = Wine.query.all()
    return render_template("catalog.html", data=wines)


@app.route("/wine/<int:id>")
def wine_card(id):
    wine = Wine.query.get(id)
    return render_template("wine.html", data=wine)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password_hash')
    user = User.query.filter_by(email=email).first() 

    if user: 
        return redirect(url_for('login'))

    new_user = User(email=email, username=name, password_hash=password)

    db_session.add(new_user)
    # db_session.commit()
    return render_template('register.html')



@app.route("/login", methods=["GET", "POST"])
def login():

    return render_template("login.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route('/logout')
def logout():
    return 'Logout'


if __name__ == "__main__":
    app.run(debug=True)
