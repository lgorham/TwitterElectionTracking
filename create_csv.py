import sqlalchemy
import csv
from model import Tweet
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
    options = {"Clinton" : { "neg" : 0, "pos" : 0}, 
            "Trump" : {"neg" : 0, "pos" : 0},
            "Both" : {"neg" : 0, "pos" : 0}}

    tweets = Tweet.query.all()

    for tweet in tweets:
        date_string = tweet.timestamp.strftime('%Y/%m/%d')
        date_sorted[date_string] = date_sorted.get(date_string, options)
        print tweet.candidates[0].name
        print date_sorted[date_string][tweet.candidates[0].name]
        date_sorted[date_string][tweet.candidates[0].name][tweet.naive_bayes] += 1

    return date_sorted



################################################################################



def sort_location():
    """
    Query and sort all tweets based on location of the tweet and the pos/neg
    valence, and the referenced candidate
    """

    location_sorted = {}
    options = {"Clinton" : { "neg" : 0, "pos" : 0}, 
            "Trump" : {"neg" : 0, "pos" : 0},
            "Both" : {"neg" : 0, "pos" : 0}}

    location_tweets = Tweet.query.filter(Tweet.profile_location != None).all()

    for tweet in enumerate(location_tweets):
        location = str(tweet.profile_location)
        print "Start of loop: {}".format(location_sorted.keys())
        location_sorted[location] = location_sorted.get(location, options)
        print "After get method: {}".format(location_sorted.keys())
        print "After get method full dict: {}".format(location_sorted)
        location_sorted[location][tweet.candidates[0].name][tweet.naive_bayes] += 1
        print "Full dict after adding + 1: {}".format(location_sorted)



    # print location_sorted
    return location_sorted



################################################################################



def write_csv():
    """Export datetime sorted dictionary to csv format"""

    all_dates = sort_by_datetime()

    clinton_file = open("clinton_data.txt", "w")
    trump_file = open("trump_data.txt", "w")
    both_file = open("both_data.txt", "w")


    for date, counts in all_dates.iteritems():
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


if __name__ == '__main__':

    connect_to_db(app)
    # write_csv()
    sort_location()
