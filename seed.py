from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from model import User, Tweet, Keyword, TweetKeyword, Candidate, TweetCandidate
from model import connect_to_db, db
from server import app
import datetime
import re

def load_users():
    """Load twitter handles from scraped twitter data file into database"""

    #deleting all existing rows so we don't duplicate
    #might want to take out if I'm update my database? Or create different 
    #'update' function
    User.query.delete()

    for row in open("seed_data/data_file.txt"):
        row = row.rstrip("")
        # handle, tweet_id, content, timestamp, profile_location, geotag = row.split("|")
        tweet_data = row.split("|")
        try:
            user = User(handle=tweet_data[0])
            print user.handle
            db.session.add(user)
            db.session.flush()
        except IntegrityError:
            #uniqueness of handles enforced in class, as same user can have multiple tweets in file
            print "Duplicate instance of handle, not added: {}".format(tweet_data[0])
            db.session.rollback()
            continue

    db.session.commit()

# ADD FOREIGN KEY - USER_ID
def load_tweets():
    """Load tweet data from scrapped twitter data file into database"""

    User.query.delete()

    for row in open("seed_data/data_file.txt"):
        row = row.rstrip()
        tweet_data = row.split("|")
        print tweet_data
        print tweet_data[0]

        # handle, tweet_id, content, timestamp, profile_location, geotag = tweet_data
        # print tweet_data[0]
        user_id = User.query.filter(User.handle==tweet_data[0]).first()
        print "user id: {}".format(user_id)

        timestamp = datetime.datetime.fromtimestamp(float(tweet_data[3]))
        if tweet_data[4] == "":
            tweet_data[4] = None
        if tweet_data[5] == "":
            tweet_data[5] = None
        tweet = Tweet(user_id=user_id.user_id, tweet_id=tweet_data[1], text=tweet_data[2], timestamp=tweet_data[3], profile_location=tweet_data[4], place_id=tweet_data[5])

        db.session.add(tweet)

    db.session.commit()

#Need to actually create the keyword file!
# def load_keywords():
#     """Load keywords from predefined set of tagged keywords"""

#     User.query.delete()

#     for row in open("seed_data/keywords.txt"):
#         row = row.rstrip()
#         keyword, word_affiliation = Keyword(keyword=keyword, word_affiliation=word_affiliation)






if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_tweets()
