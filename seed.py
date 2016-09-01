import sqlalchemy
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from model import User, Tweet, Keyword, TweetKeyword, Candidate
from model import connect_to_db, db
from naive_bayes import run_classifier
from server import app
import datetime
import re
from nltk.tokenize import TweetTokenizer
import sys

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def load_users():
    """Load twitter handles from scraped twitter data file into database"""

    # Deleting all existing rows so we don't duplicate -might want to take out if I'm update my database?
    # Or create different 'update' function
    User.query.delete()

    for row in open("seed_data/data_file.txt"):
        row = row.rstrip()
        tweet_data = row.split("|")
        try:
            user = User(handle=tweet_data[0])
            print user.handle
            db.session.add(user)
            db.session.commit()
        except IntegrityError:

            # Uniqueness of handles enforced in class, as same user can have multiple tweets in file
            print "Duplicate instance of handle, not added: {}".format(tweet_data[0])
            db.session.rollback()
            continue

    db.session.commit()


################################################################################


def load_candidates():
    """Load presidential and vice presidential candidates"""

    Candidate.query.delete()

    for row in open("seed_data/candidates.txt"):
        row = row.rstrip()
        name, full_name, position, party_affiliation = row.split("|")

        candidate = Candidate(name=name, 
                            full_name=full_name, 
                            position=position, 
                            party_affiliation=party_affiliation)

        db.session.add(candidate)

    db.session.commit()


################################################################################


def parsing_candidates(tweet):
    """
    Parsing out references to candidates within tweet and returning either 
    Trump, Clinton, or Both
    """

    Clinton = set(["hillary", "clinton", "hilary", "hrc"])
    Trump = set(["trump", "donald"])

    tweet = tweet.lower()

    clinton_count = 0
    trump_count = 0

    for word in Clinton:
        if tweet.find(word) != -1:
            clinton_count += 1
            print "Word: {}, Clinton Count: {}".format(word, clinton_count)

    for word in Trump:
        if tweet.find(word) != -1:
            trump_count += 1
            print "Word: {}, Trump Count: {}".format(word, trump_count)

    if clinton_count > 0 and trump_count > 0:
        return "Both"

    if clinton_count > 0:
        return "Clinton"

    if trump_count > 0:
        return "Trump"



################################################################################



def load_tweets():
    """Load tweet data from scrapped twitter data file into database"""

    # Tweet.query.delete()

    for row in open("seed_data/data_file.txt"):
        row = row.rstrip()
        tweet_data = row.split("|")
        handle = tweet_data[0]

        # Foreign key to users table
        user_id = User.query.filter(User.handle == handle).first()

        # Converting UTC timestamp
        timestamp = datetime.datetime.fromtimestamp(float(tweet_data[3]))

        # For tweets that don't have location data
        tweet_data[4] = tweet_data[4] or None
        tweet_data[5] = tweet_data[5] or None

        # Removing URLs from the tweet
        clean_tweet = re.sub(r"http\S+", "", tweet_data[2])
        nb_classification = run_classifier([clean_tweet])

        # Returns Trump/Clinton/Both for sorting later
        candidate = parsing_candidates(clean_tweet)

        if candidate:
            try:
                tweet = Tweet(user_id=user_id.user_id,
                                tweet_id=tweet_data[1], 
                                text=clean_tweet, 
                                timestamp=timestamp, 
                                profile_location=tweet_data[4], 
                                place_id=tweet_data[5],
                                naive_bayes=nb_classification[0],
                                referenced_candidate=candidate)
                db.session.add(tweet)
                db.session.flush()
                db.session.commit()                
                print "Tweet added: {}, {}".format(tweet.tweet_id, tweet.timestamp)
            except sqlalchemy.exc.IntegrityError:
                print "******flush or integrity error, rolling back! : {}, {}".format(tweet.tweet_id, tweet.timestamp)
                # Preventing duplicate tweets from accidentally being added
                db.session.rollback()
                continue


################################################################################



# Need to actually create the keyword file!
def load_keywords():
    """Load keywords from predefined set of tagged keywords"""

    Keyword.query.delete()

    for row in open("seed_data/keywords.txt"):
        row = row.rstrip()
        keyword, candidate, connotation = row.split("|")
        keyword = Keyword(keyword=keyword, related_candidate=candidate, connotation=connotation)
        db.session.add(keyword)

    db.session.commit()


################################################################################


def load_tweetkeywords():
    """
    Check and see which keywords are used in each tweet, and load the association
    table linking tweets and keywords
    """

    TweetKeyword.query.delete()

    tweets = Tweet.query.all()
    keyword_query = Keyword.query.all()
    keywords = []
    [keywords.append(word.keyword) for word in keyword_query]

    tknzr = TweetTokenizer()

    for tweet in tweets:
        tokenized_tweets = tknzr.tokenize(tweet.text)

        for token in tokenized_tweets:
            if token in keywords:
                tweet_id = Tweet.query.filter(Tweet.tweet_id == tweet.tweet_id).one()
                keyword_id = Keyword.query.filter(Keyword.keyword == token).one()
                tweet_keyword = TweetKeyword(keyword_id=keyword_id.keyword_id, tweet_id=tweet_id.tweet_id)
                print "Added to TweetKeyword table: {}".format(tweet_keyword.keyword_id)
                db.session.add(tweet_keyword)

    db.session.commit()



################################################################################



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    # load_candidates()
    load_tweets()
    load_keywords()
    load_tweetkeywords()
