"""Flask site for """

from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
from model import Tweet, Candidate, connect_to_db, db
from datetime import datetime
import sqlalchemy
from sqlalchemy import func
from global_dicts import POSITIVE_COLORS, NEGATIVE_COLORS, GOOGLE_MAPS_COLORS, SEED_DATA_DIR


app = Flask(__name__)
app.secret_key = "h65Tgx4RTzS21"


def load_sentiment_data(filename):
    """
    Load file with sentiment data for a given candidate, and returns a list of lists
    containing data on dates, number of negative tweets on that day, and number of
    positive tweets on that day

        >>> load_sentiment_data("test_data/sentiment_data_test.txt")
        [['2016/01/01', '2016/01/02'], ['704', '832'], ['125', '781']]
    """

    dates = []
    pos_scores = []
    neg_scores = []

    for row in open(filename):
        row = row.rstrip()
        items = row.split("|")
        dates.append(items[0])
        neg_scores.append(items[1])
        pos_scores.append(items[2])



    return [dates, neg_scores, pos_scores]



################################################################################



def load_location_data(filename):
    """
    Load file with location based data - returns a list containing tuples with the latlong
    geotagged in the tweets, the number of tweets for a particular candidate/valence

        >>> load_location_data('test_data/location_data_test.txt')
        [({'lat': 33.836081, 'lng': -81.1637245}, 4.0, 'Trump', 'neg'), ({'lat': 42.9506714, 'lng': -73.2636079}, 1.0, 'Both', 'neg')]
    """

    location_data = []

    for row in open(filename):
        row = row.rstrip()
        lat, lng, tweets, candidate, sentiment = row.split("|")
        location_data.append(({"lat" : float(lat), "lng" : float(lng)}, float(tweets), candidate, sentiment))

    return location_data


################################################################################


def pos_line_chart(candidate):
    """
    Generate a json object for sentiment line chart using global dictionary

        >>> dict = pos_line_chart('Clinton')
        >>> dict['backgroundColor']
        'rgba(143, 211, 228, 0.2)'

        >>> dict = pos_line_chart('Trump')
        >>> dict['borderColor']
        'rgba(253, 175, 175,1)'

        >>> dict = pos_line_chart('Both')
        >>> dict['pointBorderColor']
        'rgba(128, 239, 133, 1)'
    """

    chart_specs = {
                "label": "",
                "fill": False,
                "lineTension": 0.5,
                "backgroundColor": POSITIVE_COLORS[candidate]["backgroundColor"],
                "borderColor": POSITIVE_COLORS[candidate]["borderColor"],
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": POSITIVE_COLORS[candidate]["pointBorderColor"],
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": POSITIVE_COLORS[candidate]["pointHoverBorderColor"],
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": [0], 
                "spanGaps": False}

    return chart_specs


################################################################################




def neg_line_chart(candidate):
    """Generate a json object for sentiment line chart using a global dictionary

        >>> dict = neg_line_chart('Clinton')
        >>> dict['pointHoverBorderColor']
        'rgba(55,7,247,1)'

        >>> dict = neg_line_chart('Trump')
        >>> dict['pointBorderColor']
        'rgba(182,6,6,1)'

        >>> dict = neg_line_chart('Both')
        >>> dict['backgroundColor']
        'rgba(17, 130, 53, 0.2)'


    """


    chart_specs = {
                "label": "",
                "fill": False,
                "lineTension": 0.5,
                "backgroundColor": NEGATIVE_COLORS[candidate]["backgroundColor"],
                "borderColor": NEGATIVE_COLORS[candidate]["borderColor"],
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": NEGATIVE_COLORS[candidate]["pointBorderColor"],
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": NEGATIVE_COLORS[candidate]["pointHoverBorderColor"],
                "pointHoverBorderWidth": 2,
                "pointHitRadius": 10,
                "data": [0], 
                "spanGaps": False}

    return chart_specs


################################################################################



@app.route("/")
def homepage():
    """Data visualization page"""

    return render_template("homepage_charts.html")


################################################################################


@app.route("/sentiment_data.json")
def load_csv():
    """Load in data from csv format
    """


    options = {SEED_DATA_DIR + "/clinton_data.txt" : {"pos_label": "Clinton - Positive", "neg_label": "Clinton - Negative", "candidate" : "Clinton"},
            SEED_DATA_DIR + "/trump_data.txt" : {"pos_label": "Trump - Positive", "neg_label": "Trump - Negative", "candidate" : "Trump"},
            SEED_DATA_DIR + "/both_data.txt" : {"pos_label" : "Both Referenced - Positive", "neg_label": "Both Referenced - Negative", "candidate" : "Both"}}

             

    datasets = []

    for option in options.keys():
        dates, neg_nums, pos_nums = load_sentiment_data(option)

        pos_json_object = pos_line_chart(options[option]["candidate"])
        pos_json_object["label"] = options[option]["pos_label"]
        pos_json_object["data"] = pos_nums
        datasets.append(pos_json_object)

        neg_json_object = neg_line_chart(options[option]["candidate"])
        neg_json_object["label"] = options[option]["neg_label"]
        neg_json_object["data"] = neg_nums
        datasets.append(neg_json_object)

    sentiment_json = {
        "labels": dates,
        "datasets": datasets
    }

    return jsonify(sentiment_json)


################################################################################


@app.route("/donut_chart.json/<candidate>")
def load_clinton_donut(candidate):
    """Create donut chart representing total neg/pos of tweets about the passed in candidate"""


    pos_tweets = db.session.query(func.count(Tweet.tweet_id)).filter((Tweet.naive_bayes == "pos") & (Tweet.referenced_candidate == candidate)).one()
    neg_tweets = db.session.query(func.count(Tweet.tweet_id)).filter((Tweet.naive_bayes == "neg") & (Tweet.referenced_candidate == candidate)).one()

    datasets = [{"data" : [pos_tweets[0], neg_tweets[0]], 
                "backgroundColor" : [POSITIVE_COLORS[candidate]["borderColor"], NEGATIVE_COLORS[candidate]["borderColor"]]}]
   

    donut_json = {
        "labels": ["Positive", "Negative"],
        "datasets": datasets
    }

    return jsonify(donut_json)



################################################################################



@app.route("/sum_comparison.json")
def sum_comparison():
    """Create horizontal chart representing total neg/pos of tweets about Clinton"""

    clinton_tweets = db.session.query(func.count(Tweet.tweet_id)).filter(Tweet.referenced_candidate == 'Clinton').one()    
    trump_tweets = db.session.query(func.count(Tweet.tweet_id)).filter(Tweet.referenced_candidate == 'Trump').one()
    both_tweets = db.session.query(func.count(Tweet.tweet_id)).filter(Tweet.referenced_candidate == 'Both').one()

    # Potentially - backup database - have flask check which database it should be connected to
    # And from then, use given data source 
    # Could come in with AJAX
    # Also could connect to which server


    datasets = []
    datasets.append({"data" : [clinton_tweets[0], trump_tweets[0], both_tweets[0]], 
                    "backgroundColor" : ["rgba(55,7,247,1)", "rgba(182,6,6,1)", "rgba(17, 130, 53, 1)"], 
                    "label": "All Tweets"})
                    

    sum_comparison_json = {
        "labels": ["Clinton", "Trump", "Both"],
        "datasets": datasets
    }

    return jsonify(sum_comparison_json)


################################################################################


@app.route("/map.json")
def load_maps_data():
    """Create json object for google maps API"""

    location_data = load_location_data("seed_data/location_data.txt")

    json_list = []


    for location in location_data:
        location_specs = {"coordinates": location[0],
                        "num_tweets": float(location[1]), 
                        "color": GOOGLE_MAPS_COLORS[location[2]][location[3]]}

        json_list.append(location_specs)

    test_json = {"location_data" : json_list}


    return jsonify(test_json)


################################################################################



if __name__ == "__main__":
    import doctest
    import sys

    print
    result = doctest.testmod()
    if not result.failed:
        print "ALL TESTS PASSED"
    print

    if sys.argv[-1] == "jstest":
        JS_TESTING_MODE = True
        

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.debug = False
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host='0.0.0.0')

