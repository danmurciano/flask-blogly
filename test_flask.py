from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="Denson", image_url="/static/images/user.png")
        db.session.add(user)
        db.session.commit()

        self.id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Denson', html)


    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Buddy", "last_name": "Jones", "image_url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Buddy Jones", html)


    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Denson", html)
            self.assertIn(self.user.full_name, html)


    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "Ted", "last_name": "Denson", "image_url": ""}
            resp = client.post(f"/users/{self.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Ted Denson", html)



class PostViewsTestCase(TestCase):
    """Tests for views for posts."""

    def setUp(self):
        """Add sample post."""

        Post.query.delete()

        post = Post(title="Hello", content="Post content", user_id=1)
        db.session.add(post)
        db.session.commit()

        self.id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Hello', html)


    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Birds", "content": "Birds can fly", "user_id": 1}
            resp = client.post("/posts/new", data=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Birds can fly", html)


    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post Content", html)
            self.assertIn(self.post.created_at, html)


    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title": "Hi there!", "content": "This is a post"}
            resp = client.post(f"/posts/{self.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Hi there!", html)
            self.assertIn("This is a post", html)



class TagViewsTestCase(TestCase):
    """Tests for views for tags."""

    def setUp(self):
        """Add sample tag."""

        Tag.query.delete()

        tag = Tag(name="dogs")
        db.session.add(tag)
        db.session.commit()

        self.id = tag.id
        self.tag = tag

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_list_tags(self):
        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('dogs', html)


    def test_add_tag(self):
        with app.test_client() as client:
            d = {"name": "sports"}
            resp = client.tag("/tags/new", data=d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("sports", html)


    def test_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("dogs", html)


    def test_edit_tag(self):
        with app.test_client() as client:
            d = {"name": "funny dogs"}
            resp = client.tag(f"/tags/{self.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("funny dogs", html)
