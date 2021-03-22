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
    image_url = db.Column(db.Text(),  default="https://images.unsplash.com/photo-1508624217470-5ef0f947d8be?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1650&q=80")

class Post(db.Model):
    """Make the posts table."""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, default = db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref = 'posts')

class Tag(db.Model):
    """Make the tags table."""

    __tablename__ == 'tags'

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.Text, unique = True, nullable = False)

    posts = db.relationship('Post', secondary = 'post_tag', backref = 'tags')

class PostTag(db.Model):
    """Make a join table for posts and tags."""

    ___tablename__ = 'post_tag'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)






