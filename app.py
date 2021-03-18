"""Blogly application."""

from flask import Flask, request, redirect, flash, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    return render_template('user_listing.html', users = users)

@app.route('/users/new')
def show_new_user_page():
    """Show the 'create user' page."""
    return render_template('add_user.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
    """Create a new user and return to users."""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form.get('image-url')

    user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show more details for the user."""
    user = User.query.get(user_id)
    posts = user.posts
    return render_template('user_detail.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """Show the edit page for a user."""
    user = User.query.get(user_id)
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
    """Edit the user's info."""
    edited_first_name = request.form['first-name']
    edited_last_name = request.form['last-name']
    edited_img_url = request.form['image-url']
    edited_img_url = edited_img_url if edited_img_url else None

    user = User.query.get(user_id)

    user.first_name = edited_first_name
    user.last_name = edited_last_name
    user.image_url = edited_img_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """Delete a user from our database."""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_for(user_id):
    """Show form to add a post for the user."""
    user = User.query.get(user_id)
    return render_template('add_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def handle_add_form(user_id):
    title = request.form['title']
    content = request.form['content']
    post = Post(title = title, content = content, user_id = user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

