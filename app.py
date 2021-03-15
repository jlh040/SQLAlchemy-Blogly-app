"""Blogly application."""

from flask import Flask, request, redirect, flash, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = '4bx8a1m3x'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def show_home_page():
    """Redirect the user to the users page."""
    return redirect('/users')

@app.route('/users')
def show_all_users():
    """Show all the users."""
    users = User.query.all()
    return render_template('user_listing.html', users=users)

@app.route('/user/<user_id>')
def show_user_detail():
    """Show more details for the user."""
    


