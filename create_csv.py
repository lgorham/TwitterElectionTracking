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

    start = 0
    step = 10000
    stop = step
    tweets = True

    while tweets:
        tweets = db.session.query(Tweet).filter(Tweet.timestamp >= '2016-01-01').order_by(Tweet.timestamp).slice(start, stop).all()
        print len(tweets)

        for tweet in tweets:
            date_string = tweet.timestamp.strftime('%Y/%m/%d')
            print date_string
            date_sorted[date_string] = date_sorted.setdefault(date_string, deepcopy(CANDIDATE_COUNTS))

            date_sorted[date_string][tweet.referenced_candidate][tweet.naive_bayes] += 1

        start = stop
        stop = stop + step 

    print date_sorted
    return date_sorted



################################################################################



def sort_location():
    """
    Query and sort all tweets based on location of the tweet and the pos/neg
    valence, and the referenced candidate
    """

    location_sorted = {}
    start = 0
    step = 10000
    stop = step
    tweets = True

    while tweets:
        tweets = Tweet.query.filter(Tweet.profile_location != None).slice(start, stop).all()

        for tweet in tweets:
            location = tweet.profile_location
            location_sorted[location] = location_sorted.setdefault(location, deepcopy(CANDIDATE_COUNTS))

            location_sorted[location][tweet.referenced_candidate][tweet.naive_bayes] += 1

        start = stop
        stop = stop + step


    print location_sorted
    return location_sorted



################################################################################



def sentiment_csv():
    """
    Export datetime sorted dictionary to csv format
    """

    print "Starting query/export process"
    all_dates = sort_by_datetime()


    candidates = {"Clinton" : "seed_data/clinton_data.txt", 
                "Trump" : "seed_data/trump_data.txt", 
                "Both" : "seed_data/both_data.txt"}

    # Could potentially store in database as well (as view or seperate database)
    # Could be useful for capturing timeseries 


    for date in sorted(all_dates.keys()):
        counts = all_dates[date]
        for candidate in candidates.keys():
            print candidate
            negative = counts[candidate]["neg"]
            positive = counts[candidate]["pos"]
            candidate_data = "|".join([date, str(negative), str(positive)])
            candidate_file = open(candidates[candidate], "a")
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
    count = 0

    for location, sentiments in all_locations.iteritems():
        count +=1
        print count
        print location, sentiments
        location = geocoder.google(str(location))
        coordinates = location.latlng
        if coordinates:
            print "Coordinates: {}".format(coordinates)
            print "Lat: {}, Lng: {}".format(coordinates[0], coordinates[1])

            for candidate in candidates:
                neg = sentiments[candidate[0]]["neg"]
                pos = sentiments[candidate[0]]["pos"]

                if neg > 0:
                    print "Neg: {}, Candidate: {}".format(neg, candidate[0])
                    neg_data = "|".join([str(coordinates[0]), str(coordinates[1]), str(neg), candidate[0], "neg"])
                    location_file.write("{}\n".format(neg_data))
                if pos > 0: 
                    print "Pos: {}, Candidate: {}".format(pos, candidate[0])
                    pos_data = "|".join([str(coordinates[0]), str(coordinates[1]), str(pos), candidate[0], "pos"])
                    location_file.write("{}\n".format(pos_data))

    location_file.close()
        

if __name__ == '__main__':

    connect_to_db(app)
    # sentiment_csv()
    location_csv()
