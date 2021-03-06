from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    @classmethod
    def sort(cls):
        return cls.query.order_by(cls.last_name, cls.first_name)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(100), nullable=False, default="/static/images/user.png")

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
      return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>"



class Post(db.Model):
    __tablename__ = "posts"

    @classmethod
    def sort(cls):
        return cls.query.order_by(cls.created_at.desc())

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @property
    def time(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content[:100]} created_at={p.created_at}, user_id={p.user_id}>"



class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship("Post", secondary="post_tags", backref="tags")

    @classmethod
    def sort(cls):
        return cls.query.order_by(cls.name)

    def __repr__(self):
        t = self
        return f"<Tag id={t.id} name={t.name}>"



class PostTag(db.Model):
    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True, nullable=False)

    def __repr__(self):
        pt = self
        return f"<Post id={pt.post_id} Tag id={pt.tag_id}>"
