"""Blogly application."""

from flask import Flask, request, redirect, flash, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
def show_add_post_form(user_id):
    """Show form to add a post for the user."""
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('add_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def handle_add_form(user_id):
    """Process the new post."""
    title = request.form['title']
    content = request.form['content']
    selected_tag_names = request.form.getlist('tag')

    post = Post(title = title, content = content, user_id = user_id)
    selected_tags = selected_tag_objs(selected_tag_names)
    post.tags.extend(selected_tags)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post and its tags."""
    post = Post.query.get(post_id)
    tags = post.tags
    return render_template('post_detail.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit_page(post_id):
    """Show the page to edit a post."""
    post = Post.query.get(post_id)
    user = post.user
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    """Handle the editing of a post."""
    edited_title = request.form['title']
    edited_content = request.form['content']
    selected_tag_names = request.form.getlist('tag')
    selected_tags = selected_tag_objs(selected_tag_names)

    post = Post.query.get(post_id)

    post.tags.clear()
    post.tags.extend(selected_tags)

    post.title = edited_title
    post.content = edited_content

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.filter(Post.id == post_id).one()
    user_id = post.user_id
    delete_post_tag_via_post(post_id)
    Post.query.filter(Post.id == post_id).delete()

    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/tags')
def list_tags():
    """Show a list of all tags."""
    all_tags = Tag.query.all()
    return render_template('list_tags.html', all_tags=all_tags)

@app.route('/tags/<int:tag_id>')
def show_tag_info(tag_id):
    """Show a tag's info."""
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template('tag_info.html', tag=tag, posts=posts)

@app.route('/tags/new')
def show_add_tag_page():
    """Show the page to add a tag."""
    return render_template('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def handle_new_tag():
    """Add new tag to db."""
    name_of_tag = request.form['tag-name']
    new_tag = Tag(name = name_of_tag)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag(tag_id):
    """Show edit tag page."""
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_edit_tag_form(tag_id):
    """Add the edited tag to the database."""
    edited_tag_name = request.form['edited-tag-name']
    orig_tag = Tag.query.get(tag_id)
    orig_tag.name = edited_tag_name

    db.session.add(orig_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag."""
    delete_post_tag_via_tag(tag_id)
    tag = Tag.query.filter(Tag.id == tag_id).delete()

    db.session.commit()

    return redirect('/tags')

def delete_post_tag_via_tag(tag_id):
    """Search the post_tag model for corresponding records and then delete."""
    post_tag_list = PostTag.query.filter_by(tag_id = tag_id).all()
    for post_tag in post_tag_list:
        db.session.delete(post_tag)

def delete_post_tag_via_post(post_id):
    """Search the post_tag model for corresponding records and then delete."""
    post_tag_list = PostTag.query.filter_by(post_id = post_id).all()
    for post_tag in post_tag_list:
        db.session.delete(post_tag)

def get_tag_names_in_db():
    tag_names = []
    tag_objs = Tag.query.all()
    for tag in tag_objs:
        tag_names.append(tag.name)
    
    return tag_names

def selected_tag_objs(tag_names):
    """Make tag objects and insert them into the database."""
    selected_tags = []
    for tag_name in get_tag_names_in_db():
        if tag_name in tag_names:
            tag = db.session.query(Tag).filter(Tag.name == tag_name).one()
            selected_tags.append(tag)

    return selected_tags

    