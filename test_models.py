from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_add_user(self):
        user = User(first_name="Test", last_name="Denson", image_url="/static/images/user.png")
        self.assertEquals(user.full_name, "Test Denson")
        self.assertEquals(user.image_url, "/static/images/user.png")
