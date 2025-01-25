from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from db import db_session
from config import host, user, password, db_name, port
from models import Wine, User
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

login_manager = LoginManager(app)
login_manager.init_app(app)
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



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

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Validate form data
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if not (username and password and email):
            return render_template("register.html", message="All fields are required.")
 
        db_session.add(User)
        db_session.commit()

        return redirect("/login")

    return render_template("register.html")





@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)