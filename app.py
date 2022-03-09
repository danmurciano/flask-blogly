from flask import Flask, render_template, request, redirect, flash, session, jsonify
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "w57h63ff9"

connect_db(app)
db.create_all()

tags= Tag.sort()


@app.route("/")
def home():
    posts= Post.sort().limit(10)
    return render_template("home.html", posts=posts)


# Users Routes

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


@app.route("/users/<user_id>")
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user-profile.html", user=user)


@app.route("/users/<user_id>/edit")
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user-edit.html", user=user)


@app.route("/users/<user_id>/edit", methods=["POST"])
def edit_user(user_id):
    user = User.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    if request.form["image_url"] != "":
        user.image_url = request.form["image_url"]
    else:
        user.image_url = "/static/images/user.png"
    db.session.commit()
    return redirect("/users")


@app.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<user_id>/posts/new")
def add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("add-post.html", user=user, tags=tags)


@app.route("/users/<user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")



# Posts Routes

@app.route("/posts/<post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/posts/<post_id>/edit")
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post-edit.html", post=post, tags=tags)


@app.route("/posts/<post_id>/edit", methods=["POST"])
def edit_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.route("/posts/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")



# Tags Routes

@app.route("/tags")
def list_tags():
    return render_template("tags.html", tags=tags)


@app.route("/tags/<tag_id>")
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag.html", tag=tag)


@app.route("/tags/new")
def add_tag_form():
    return render_template("add-tag.html")


@app.route("/tags/new", methods=["POST"])
def add_tag():
    name = request.form["name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<tag_id>/edit")
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag-edit.html", tag=tag)


@app.route("/tags/<tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag.name = request.form["name"]
    db.session.commit()
    return redirect("/tags")


@app.route("/tags/<tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
