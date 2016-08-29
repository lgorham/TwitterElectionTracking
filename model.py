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


class Candidate(db.Model):
    """Table for each candidate (both for president and vp)"""

    __tablename__ = "candidates"

    candidate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    full_name = db.Column(db.String(25), nullable=False)
    position = db.Column(db.String(2), nullable=False)
    party_affiliation = db.Column(db.String(10), nullable=False)


class Tweet(db.Model):
    """Individual tweet"""

    __tablename__ = "tweets"

    # Primary Key
    tweet_id = db.Column(db.String(25), 
                        unique=True, 
                        primary_key=True)

    # Foreign Key - User
    user_id = db.Column(db.Integer, 
                        db.ForeignKey(User.user_id), 
                        nullable=False)

    # Foreign Key - Candidate
    referenced_candidate = db.Column(db.String(10), 
                                    db.ForeignKey(Candidate.name), 
                                    nullable=False)

    # Additional attributes of each tweet
    text = db.Column(db.String(400), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    naive_bayes = db.Column(db.String(5), nullable=True)
    profile_location = db.Column(db.String(30), nullable=True)
    place_id = db.Column(db.String(25), nullable=True)


    # Defining relationship to user (one user to many tweets)
    user = db.relationship("User", backref=db.backref("tweets", order_by=tweet_id))

    # Defining relationship to candidate (one candidate to many tweets)
    candidate = db.relationship("Candidate", backref=db.backref("candidate", order_by=tweet_id))

    # Defining relationship with keywords through association table (many-to-many)
    keywords = db.relationship("Keyword",
                                secondary="tweet_keywords",
                                backref="keywords")




class Keyword(db.Model):
    """Specific campaign specific keywords with designated word affiliations"""

    __tablename__ = "keywords"

    keyword_id = db.Column(db.Integer, 
                            autoincrement=True, 
                            primary_key=True)
    keyword = db.Column(db.String(30), nullable=False)
    related_candidate = db.Column(db.String(10), 
                                db.ForeignKey(Candidate.name), 
                                nullable=False)
    connotation = db.Column(db.String(10), nullable=True)

    candidate = db.relationship("Candidate", backref=db.backref("keywords"))





class TweetKeyword(db.Model):
    """Association table joining tweets and their related keywords"""

    __tablename__ = "tweet_keywords"

    tweet_key_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tweet_id = db.Column(db.String(25), db.ForeignKey(Tweet.tweet_id), nullable=False)
    keyword_id = db.Column(db.Integer, db.ForeignKey(Keyword.keyword_id), nullable=False)



# class TweetCandidate(db.Model):
#     """Association table joining tweets and the candidates referenced in the tweet"""

#     __tablename__ = "tweet_candidates"

#     tweet_candidate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     tweet_id = db.Column(db.String(25), db.ForeignKey(Tweet.tweet_id), nullable=False)
#     candidate_id = db.Column(db.Integer, db.ForeignKey(Candidate.candidate_id), nullable=False)



##table that checks when the last time you collected data would be
##if it has been long enough, starts collecting data


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sentiments'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

