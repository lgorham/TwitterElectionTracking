import sqlalchemy
import csv
from model import Tweet, Candidate
from model import connect_to_db, db
from server import app
from global_dicts import CANDIDATE_COUNTS
from copy import deepcopy
import sys
import geocoder

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


def sort_by_datetime():
    """
    Create dictionary sorted by the number of pos/neg tweets for each candidate
    at a given datetime
    """

    date_sorted = {}

    tweets = Tweet.query.all()
    print len(tweets)

    for tweet in tweets:
        date_string = tweet.timestamp.strftime('%Y/%m/%d')
        date_sorted[date_string] = date_sorted.setdefault(date_string, deepcopy(CANDIDATE_COUNTS))

        date_sorted[date_string][tweet.referenced_candidate][tweet.naive_bayes] += 1

    print date_sorted
    return date_sorted



################################################################################



def sort_location():
    """
    Query and sort all tweets based on location of the tweet and the pos/neg
    valence, and the referenced candidate
    """

    location_sorted = {}

    location_tweets = Tweet.query.filter(Tweet.profile_location != None).all()

    for tweet in location_tweets:
        location = tweet.profile_location
        location_sorted[location] = location_sorted.setdefault(location, deepcopy(CANDIDATE_COUNTS))

        location_sorted[location][tweet.referenced_candidate][tweet.naive_bayes] += 1


    # Could potentially store in database as well (as view or seperate database)
    # Could be useful for capturing timeseries 

    print location_sorted
    return location_sorted



################################################################################



def sentiment_csv():
    """Export datetime sorted dictionary to csv format"""

    all_dates = sort_by_datetime()


    candidates = {"Clinton" : "seed_data/clinton_data.txt", 
                "Trump" : "seed_data/trump_data.txt", 
                "Both" : "seed_data/both_data.txt"}


    for date, counts in all_dates.iteritems():
        
        for candidate in candidates.keys():
            negative = counts[candidate]["neg"]
            positive = counts[candidate]["pos"]
            candidate_data = "|".join([date, str(negative), str(positive)])
            candidate_file = open(candidates[candidate], "w")
            candidate_file.write("{}\n".format(candidate_data))
            candidate_file.close()

    print "File complete"


################################################################################


def location_csv():
    """Export location sorted dictionary to csv format"""

    all_locations = sort_location()

    candidates = db.session.query(Candidate.name).all()

    location_file = open("seed_data/location_data.txt", "w")

    locations = []
    sentiment_dicts = []

    for location, sentiments in all_locations.iteritems():
        location = geocoder.google(str(location))
        coordinates = location.latlng

        for candidate in candidates:
            neg = sentiments[candidate[0]]["neg"]
            pos = sentiments[candidate[0]]["pos"]


            if neg > 0:
                print neg
                neg_data = "|".join([str(coordinates[0]), str(coordinates[1]), str(neg), candidate[0], "neg"])
                location_file.write("{}\n".format(neg_data))
            if pos > 0: 
                pos_data = "|".join([str(coordinates[0]), str(coordinates[1]), str(pos), candidate[0], "pos"])
                location_file.write("{}\n".format(pos_data))

    location_file.close()
        

if __name__ == '__main__':

    connect_to_db(app)
    sentiment_csv()
    # location_csv()
