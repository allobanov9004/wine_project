from flask import Flask, render_template, request, redirect, url_for, flash
from flask_admin import Admin
from flask_login import LoginManager

from models import Wine, User
from werkzeug.security import generate_password_hash
from flask_admin.contrib.sqla import ModelView


from db import db_session

from flask_login import LoginManager, login_user, current_user
from flask_paginate import Pagination, get_page_parameter, get_page_args






app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"

admin = Admin(app, name='wineproject')
admin.add_view(ModelView(User, db_session))
admin.add_view(ModelView(Wine, db_session))

login_manager = LoginManager()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/catalog")
def catalog():

    wines = Wine.query.all()


    def get_wines(offset=0, per_page=30):
        return wines[offset: offset + per_page]


    search = False
    total = len(wines)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')


    pagination_wines = get_wines(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, search=search, record_name='позиции')

    return render_template("catalog.html", data=pagination_wines, pagination=pagination, page=page, per_page=per_page)


@app.route("/wine/<int:id>")
def wine_card(id):
    wine = Wine.query.get(id)
    return render_template("wine.html", data=wine)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if len(request.form.get('username')) > 4 and request.form.get('password') == request.form.get('password2'):
            hash = generate_password_hash(request.form.get('password'))
            email = request.form.get('email')
            username = request.form.get('username')
            new_user = User(email=email, username=username, password_hash=hash)

            # try:
            db_session.add(new_user)
            db_session.commit()
            flash("вы успешно зарегистрировались")
            # except Exception as exc:
            #     print(exc)
         

        else:
            flash('Неверно введены данные')


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
