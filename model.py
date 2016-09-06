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


################################################################################



class Candidate(db.Model):
    """Table for each candidate (both for president and vp)"""

    __tablename__ = "candidates"

    candidate_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(15), nullable=False, unique=True)
    full_name = db.Column(db.String(25), nullable=False)
    position = db.Column(db.String(2), nullable=False)
    party_affiliation = db.Column(db.String(10), nullable=False)


################################################################################



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
    profile_location = db.Column(db.String(100), nullable=True)
    place_id = db.Column(db.String(30), nullable=True)


    # Defining relationship to user (one user to many tweets)
    user = db.relationship("User", backref=db.backref("tweets", order_by=tweet_id))

    # Defining relationship to candidate (one candidate to many tweets)
    candidate = db.relationship("Candidate", backref=db.backref("candidate", order_by=tweet_id))

    # Defining relationship with keywords through association table (many-to-many)
    keywords = db.relationship("Keyword",
                                secondary="tweet_keywords",
                                backref="keywords")

    def __repr__(self):
        return "<Tweet id={}>".format(tweet_id)



################################################################################




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



################################################################################



class TweetKeyword(db.Model):
    """Association table joining tweets and their related keywords"""

    __tablename__ = "tweet_keywords"

    tweet_key_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tweet_id = db.Column(db.String(25), db.ForeignKey(Tweet.tweet_id), nullable=False)
    keyword_id = db.Column(db.Integer, db.ForeignKey(Keyword.keyword_id), nullable=False)



################################################################################


def example_data():
    """Create sample data for testing purposes"""

    # Creating users
    user1 = User(handle='@generictrumpsupporter')
    user2 = User(handle='@genericclintonsupporter')
    user3 = User(handle='@mythicalswingvoter')

    # Creating candidates
    clinton = Candidate(name='Clinton', 
                        full_name='Hiltlary Clinton', 
                        position='P', 
                        party_affiliation='Democrat')

    trump = Candidate(name='Trump', 
                        full_name='Donald Trump', 
                        position='P', 
                        party_affiliation='Republican')

    both = Candidate(name='Both', 
                        full_name='Both', 
                        position='P', 
                        party_affiliation='Both')

    # Creating tweets for each user
    tweet1 = Tweet(tweet_id='1', 
                    user_id='2', 
                    referenced_candidate='Trump',
                    text='Yay Trump! #MAGA',
                    naive_bayes='pos',
                    profile_location='Jackson, Mississippi',
                    place_id=None)

    tweet2 = Tweet(tweet_id='2', 
                    user_id='1', 
                    referenced_candidate='Clinton',
                    text='So proud of our first woman nominee, Hillary Clinton! #HillYes',
                    naive_bayes='pos',
                    profile_location='Manhattan, NY',
                    place_id=None)

    tweet3 = Tweet(tweet_id='3', 
                    user_id='3', 
                    referenced_candidate='Both',
                    text='I hate both of the candidates #CrookedHillary #DumpTrump',
                    naive_bayes='neg',
                    profile_location='Denver, CO',
                    place_id=None)

    db.session.add_all([user1, user2, user3, clinton, trump, both, tweet1, tweet2, tweet3])
    db.session.commit()

################################################################################


def connect_to_db(app, database='postgresql:///sentiments'):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    db.app = app
    db.init_app(app)

################################################################################

# TO IMPLEMENT: Table that checks when the last time you collected data would be
## if it has been long enough, starts collecting data


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

