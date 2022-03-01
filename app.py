from flask import Flask, render_template, request, redirect, flash, session, jsonify
from models import db, connect_db, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "w57h63ff9"

connect_db(app)
db.create_all()


@app.route("/")
def home():
    return redirect("/users")


@app.route("/users")
def list_users():
    users = User.sort()
    return render_template("users.html", users=users)


@app.route("/users/new")
def add_user_form():
    return render_template("add-user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    if request.form["image_url"] != "":
        image_url = request.form["image_url"]
    else:
        image_url = None
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<id>")
def user_profile(id):
    user = User.query.get_or_404(id)
    return render_template("user-profile.html", user=user)


@app.route("/users/<id>/edit")
def edit_user_form(id):
    user = User.query.get_or_404(id)
    return render_template("user-edit.html", user=user)


@app.route("/users/<id>/edit", methods=["POST"])
def edit_user(id):
    user = User.query.get(id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    if request.form["image_url"] != "":
        user.image_url = request.form["image_url"]
    else:
        user.image_url = "/static/images/user.png"
    db.session.commit()
    return redirect("/users")


@app.route("/users/<id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
