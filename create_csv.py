import sqlalchemy
import csv
from model import Tweet, Candidate
from model import connect_to_db, db
from server import app
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

    for tweet in tweets:
        date_string = tweet.timestamp.strftime('%Y/%m/%d')
        date_sorted[date_string] = date_sorted.setdefault(date_string, {"Clinton" : { "neg" : 0, "pos" : 0}, 
                                                                        "Trump" : {"neg" : 0, "pos" : 0},
                                                                        "Both" : {"neg" : 0, "pos" : 0}})

        date_sorted[date_string][tweet.referenced_candidate][tweet.naive_bayes] += 1

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
        location_sorted[location] = location_sorted.setdefault(location, {"Clinton" : { "neg" : 0, "pos" : 0}, 
                                                                "Trump" : {"neg" : 0, "pos" : 0},
                                                                "Both" : {"neg" : 0, "pos" : 0}})

        location_sorted[location][tweet.referenced_candidate][tweet.naive_bayes] += 1



    print location_sorted
    return location_sorted



################################################################################



def sentiment_csv():
    """Export datetime sorted dictionary to csv format"""

    all_dates = sort_by_datetime()

    clinton_file = open("clinton_data.txt", "w")
    trump_file = open("trump_data.txt", "w")
    both_file = open("both_data.txt", "w")


    for date, counts in all_dates.iteritems():
        # for candidate in candidates:
        clinton_neg = counts["Clinton"]["pos"]
        clinton_pos = counts["Clinton"]["neg"]
        clinton_data = "|".join([date, str(clinton_neg), str(clinton_pos)])
        clinton_file.write("{}\n".format(clinton_data))

        trump_neg = counts["Trump"]["neg"]
        trump_pos = counts["Trump"]["pos"]
        trump_data = "|".join([date, str(trump_neg), str(trump_pos)])
        trump_file.write("{}\n".format(trump_data))

        both_neg = counts["Both"]["neg"]
        both_pos = counts["Both"]["pos"]
        both_data = "|".join([date, str(both_neg), str(both_pos)])
        both_file.write("{}\n".format(both_data))

    clinton_file.close()
    trump_file.close()
    both_file.close()

    print "File complete"


def location_csv():
    """Export location sorted dictionary to csv format"""

    all_locations = sort_location()

    candidates = db.session.query(Candidate.name).all()

    location_file = open("location_data.txt", "w")

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
    # sort_location()
    location_csv()
