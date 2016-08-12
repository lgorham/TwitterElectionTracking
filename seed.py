from sqlalchemy import func
from model import Tweet, User, Keyword, TweetKeyword, Candidate, TweetCandidate

from model import connect_to_db, db
from server import app
from datetime import date
import re

def load_users():
    """Load twitter handles from twitter users file into database"""

    #deleting all existing rows so we don't duplicate
    #might want to take out if I'm update my database? Or create different 
    #'update' function
    User.query.delete()

    for row in open("seed_date/data_file.txt"):
        row = row.rstrip()
        handle, tweet_id, content, timestamp, profile_location, geotag = row.split("|")
        try:
            user = User(handle=handle)
        except UniqueViolation:
            #uniqueness of handles enforced in class, as same user can have multiple tweets in file
            continue

        db.session.add(user)

    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()