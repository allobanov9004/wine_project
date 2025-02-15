from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_admin import Admin
from flask_login import LoginManager

from models import Wine, User, Comment
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView


from db import db_session

from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from flask_paginate import Pagination, get_page_args



app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"

admin = Admin(app, name='wineproject')
admin.add_view(ModelView(User, db_session))
admin.add_view(ModelView(Wine, db_session))
admin.add_view(ModelView(Comment, db_session))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
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
    # comm = Comment.query.get(id)
    comm = Comment.query.filter_by(wine_id=id).all()
    return render_template("wine.html", data=wine, comm=comm)



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
            db_session.add(new_user)
            db_session.commit()
            flash("вы успешно зарегистрировались")
         
        else:
            flash('Неверно введены данные')

    return render_template('register.html')




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                flash(f"Вы вошли как {username}")
                login_user(user)

                next_page = request.args.get('next')

                redirect(next_page)
            else:
                flash("Логин или пароль не корректен")
        else:
            flash("Заполните поля почта и пароль")

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template("login.html")




@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/lgn')
@login_required
def admin_index():
    if current_user.is_admin:
        return 'Привет админ'
    else:
        return 'Ты не админ!'



@app.route("/create-comment/<wine_id>", methods=["POST"])
@login_required
def create_comment(wine_id):
    text = request.form.get('text')

    if not text:
        flash('Комментарий не может быть пустым', category='error')
    else:
        wine = Wine.query.filter_by(id = wine_id)
        if wine:
            comment = Comment(text=text, author=current_user.id, wine_id=wine_id)
            db_session.add(comment)
            db_session.commit()
            print(comment)
            flash("Комментарий сохранен")
        else:
            flash("Комментариев не найдено", category="error")

        
    return redirect(request.referrer)



if __name__ == "__main__":
    app.run(debug=True)
