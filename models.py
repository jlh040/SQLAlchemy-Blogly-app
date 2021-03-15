"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect flask and SQLAlchemy."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Make the users table."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(20), unique = True)
    image_url = db.Column(
                db.Text(),  
                default="""https://images.unsplash.com/photo-1508624217470-5ef0f947d8be?ixid=
                MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80"""
    )

    

    


