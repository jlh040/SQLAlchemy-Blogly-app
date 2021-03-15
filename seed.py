"""This is a seed file to add some starting data into the database."""
from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
whiskey = User(first_name="Whiskey", last_name='Roberts')
bowser = User(first_name="Bowser", last_name="Redi")
spike = User(first_name="Spike", last_name="Dero")

# Add new object to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit--otherwise, this never gets saved!
db.session.commit()
