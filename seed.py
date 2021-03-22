"""This is a seed file to add some starting data into the database."""
from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Post.query.delete()
Tag.query.delete()

# Add users
whiskey = User(first_name="Whiskey", last_name='Roberts')
bowser = User(first_name="Bowser", last_name="Redi")
spike = User(first_name="Spike", last_name="Dero")

db.session.add_all([whiskey, bowser, spike])
db.session.commit()

# Add posts
post_1 = Post(title = 'First day at the zoo' , content = 'It was a great day at the zoo' , user_id = 1 )
post_2 = Post(title = 'Going to the mall' , content = 'Going to the mall is great and fun' , user_id = 2)
post_3 = Post(title = 'Eating burger king for the 40th time' , content = 'I had some burger king today and wow' , user_id = 3)
post_4 = Post(title = 'Having a great computer room' , content = 'Where is the greatest computer room in the world?' , user_id = 3)

db.session.add_all([post_1, post_2, post_3, post_4])
db.session.commit()

# Add tags
tag_1 = Tag(name = 'Funny')
tag_2 = Tag(name = 'Scary')
tag_3 = Tag(name = 'Serious')
tag_4 = Tag(name = 'Virtuous')

db.session.add_all([tag_1, tag_2, tag_3, tag_4])
db.session.commit()

# Connect posts and tags
pt_1 = PostTag(post_id = 1, tag_id = 1)
pt_2 = PostTag(post_id = 1, tag_id = 3)
pt_3 = PostTag(post_id = 2, tag_id = 4)
pt_4 = PostTag(post_id = 3, tag_id = 1)
pt_5 = PostTag(post_id = 4, tag_id = 2)
pt_6 = PostTag(post_id = 3, tag_id = 4)

db.session.add_all([pt_1, pt_2, pt_3, pt_4, pt_5, pt_6])
db.session.commit()