from unittest import TestCase
from app import app
from models import db, User

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