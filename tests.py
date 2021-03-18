from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debugging-toolbar']

db.drop_all()
db.create_all()

class BloglyRouteTestCase(TestCase):
    """Test some of the routes in the main app file."""

    def setUp(self):
        """Clear out the database and add sample users."""
        Post.query.delete()
        User.query.delete()

        user_1 = User(first_name = 'Mark', last_name = "Hammond")
        user_2 = User(first_name = 'Sally', last_name = "Witherspoon")
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

        self.user_id_1 = user_1.id
        self.user_id_2 = user_2.id

    def tearDown(self):
        """Clear out the session."""
        db.session.rollback()
        

    def test_show_all_users(self):
        """Test that the users appear on the page."""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertIn('Mark Hammond', html)
            self.assertIn('Sally Witherspoon', html)
    
    def test_create_user(self):
        """Test that a new user is created."""
        new_user = {'first-name': 'Jack', 'last-name': 'Skellington'}
        with app.test_client() as client:
            resp = client.post('/users/new', data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('Jack Skellington', html)

    def test_homepage_redirect(self):
        """Test that the '/' route is actually redirected."""
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(resp.status_code, 302)
    
    def test_delete_user(self):
        """Test that a user can be deleted."""
        with app.test_client() as client:
            # delete user 1
            resp = client.post(f'/users/{self.user_id_1}/delete', follow_redirects=True)

            # get user 2 from the database
            user_2 = User.query.filter(User.id == self.user_id_2).one()

            # make a request for all the users in the database
            req_for_all_users = User.query.all()

            # check that user 2 is the only one in the database
            self.assertEqual(req_for_all_users, [user_2])
    
    def test_post_creation(self):
        """Test that a post is created."""
        with app.test_client() as client:
            # Make a post
            resp_1 = client.post(f'/users/{self.user_id_2}/posts/new', data = {'title': 'My first post',
            'content': 'This is the content of my first post'}, follow_redirects = True)
            
            # Get that post
            user = User.query.get(self.user_id_2)
            post = user.posts[0]

            # Go to the page for that post
            resp_2 = client.get(f'/posts/{post.id}')
            html = resp_2.get_data(as_text = True)

            # Check that the expected text is on that post's page
            self.assertIn('My first post', html)
            self.assertIn('This is the content of my first post', html)
    
    def test_post_deletion(self):
        """Test that a post can be deleted."""
        with app.test_client() as client:
            # Make a post
            resp = client.post(f'/users/{self.user_id_1}/posts/new', data = {'title': 'This is yet another post',
            'content': 'Welcome to my beautiful post.'}, follow_redirects = True)

            # Get the post id
            post_id = Post.query.filter(Post.user_id == self.user_id_1).one().id

            # Delete the post
            client.post(f'/posts/{post_id}/delete', follow_redirects = True)
            
            # Check that the post is gone
            resp_2 = client.get(f'/users/{self.user_id_1}')
            html = resp_2.get_data(as_text = True)
            self.assertNotIn('This is yet another post', html)