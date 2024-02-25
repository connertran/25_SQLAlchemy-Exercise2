from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test2'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample user and add sample post"""

        User.query.delete()

        user = User(first_name="Conner", last_name="Tran", image_url="https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        Post.query.delete()
        post = Post(title="Lunch", content ="It is time, let's go!", user_id =self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    
    def test_show_post_details(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<button class="btn btn-primary" id="edit-btn">Edit</button>',html)

    # def test_post_edit_page(self):
    #     with app.test_client() as client:
    #         resp = client.get(f'/posts/{self.post_id}/edit')
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code,200)
    #         self.assertIn('<label for="post-content">Post Content</label>',html)
    def test_post_edit_page(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="post-content">Post Content</label>', html)
            self.assertIn('<input type="text" id="post-content" name="post-content"', html)