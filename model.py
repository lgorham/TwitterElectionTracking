"""Models for twitter election analysis project"""

from flask_sqlalchemy import SQLAlchemy 


db = SQLAlchemy()

################################################################################
#class definitions


class User(db.Model):
    """Twitter user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    handle = db.Column(db.String(80), nullable=False, unique=True)


class Tweet(db.Model):
    """Individual tweet"""

    __tablename__ = "tweets"

    tweet_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), nullable=False)
    text = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    nltk_score = db.Column(db.Integer, nullable=True)

    #defining relationship to user
    user = db.relationship("User", backref=db.backref("tweets", order_by=tweet_id))


class Keyword(db.Model):
    """Specific campaign specific keywords with designated word affiliations"""

    keyword_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    keyword = db.Column(db.String(10), nullable=False)
    word_affiliation = db.Column(db.String(10), nullable=True)


class TweetKeyword(db.Model):
    """Association table joining tweets and their related keywords"""

    __tablename__ = "tweet_keywords"

    tweet_key_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey(Tweet.tweet_id), nullable=False)
    keyword_id = db.Column(db.Integer, db.ForeignKey(Keyword.keyword_id), nullable=False)

    #specifying relationship to tweet
    tweet = db.relationship("Tweet", backref=db.backref("tweet_keywords", order_by=tweet_key_id))

    #specifying relationship to keyword
    keyword = db.relationship("Keyword", backref=db.backref("tweet_keywords", order_by=tweet_key_id))


class Candidate(db.Model):
    """Table for each candidate (both for president and vp)"""

    __tablename__ = "candidates"

    candidate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    party_affiliation = db.Column(db.String(10), nullable=False)



class TweetCandidate(db.Model):
    """Association table joining tweets and the candidates referenced in the tweet"""

    __tablename__ = "tweet_candidates"

    tweet_candidate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey(Tweet.tweet_id), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey(Candidate.candidate_id), nullable=False)
    dominant = db.Column(db.Boolean, nullable=False)

    #specifying relationship to tweet
    tweet = db.relationship("Tweet", backref=db.backref("tweet_candidates", order_by=tweet_candidate_id))

    #specifying relationship to candidate
    candidate = db.relationship("Candidate", backref=db.backref("tweet_candidates", order_by=tweet_candidate_id))




