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
            "Both" : {"neg" : 0}, "pos" : 0}

    tweets = Tweet.query.all()

    for tweet in tweets:
        date_sorted[tweet.datetime] = date_sorted.get(tweet.datetime, options)
        date_sorted[tweet.datetime][tweet.candidates][tweet.naive_bayes] += 1

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
            "Both" : {"neg" : 0}, "pos" : 0}

    location_tweets = Tweet.query.filter(Tweet.profile_location != None)

    for tweet in location_tweets:
        geocoded_location = geocoder.google(tweet.profile_location)
        location_sorted[geocoded_location] = date_sorted.get(geocoded_location, options)
        location_sorted[geocoded_location][tweet.candidates][tweet.naive_bayes] += 1

    return location_tweets



################################################################################



def write_csv():
    """Export datetime sorted dictionary to csv format"""

    all_dates = sort_by_datetime()

    csvwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for date in all_dates:
        csvwriter.writerow(date,
                            date["Clinton"]["neg"], 
                            date["Clinton"]["pos"],
                            date["Trump"]["neg"],
                            date["Trump"]["pos"],
                            date["Both"]["neg"],
                            date["Both"]["pos"]
            ])

    csvfile.close()


if __name__ == '__main__':

    connect_to_db(app)
    export_to_csv()
