"""Flask site for """

from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
from model import Tweet, Candidate, connect_to_db, db
from datetime import datetime
import sqlalchemy
from server_colors import POSITIVE_COLORS, NEGATIVE_COLORS, GOOGLE_MAPS_COLORS


app = Flask(__name__)
app.secret_key = "h65Tgx4RTzS21"


def load_sentiment_data(filename):
    """Load file with sentiment data for a given candidate"""

    dates = []
    pos_scores = []
    neg_scores = []

    for row in open(filename):
        row = row.rstrip()
        items = row.split("|")
        dates.append(items[0])
        neg_scores.append(items[1])
        pos_scores.append(items[2])


    return [dates, pos_scores, neg_scores]



################################################################################



def load_location_data(filename):
    """Load file with location based data"""

    location_data = []

    for row in open(filename):
        row = row.rstrip()
        lat, lng, tweets, candidate, sentiment = row.split("|")
        location_data.append(({"lat" : float(lat), "lng" : float(lng)}, float(tweets), candidate, sentiment))

    return location_data


################################################################################


def pos_line_chart(candidate):
    """Generate a json object for sentiment line chart"""

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
    """Generate a json object for sentiment line chart"""


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
    """Load in data from csv format"""


    options = {"clinton_data.txt" : {"pos_label": "Clinton - Positive", "neg_label": "Clinton - Negative", "candidate" : "Clinton"},
            "trump_data.txt" : {"pos_label": "Trump - Positive", "neg_label": "Trump - Negative", "candidate" : "Trump"},
            "both_data.txt" : {"pos_label" : "Both Referenced - Positive", "neg_label": "Both Referenced - Negative", "candidate" : "Both"}}

             

    datasets = []

    for option in options.keys():
        dates, pos_nums, neg_nums = load_sentiment_data(option)

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


@app.route("/donut_chart_clinton.json")
def load_clinton_donut():
    """Create donut chart representing total neg/pos of tweets about Clinton"""


    pos_clinton_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "pos") & (Tweet.referenced_candidate == "Clinton")).all()
    
    neg_clinton_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "neg") & (Tweet.referenced_candidate == "Clinton")).all()


    datasets = []
    datasets.append({"data" : [len(pos_clinton_tweets), len(neg_clinton_tweets)], "backgroundColor" : ["rgba(143, 211, 228,1)", "rgba(55,7,247,1)"]})
   

    clinton_json = {
        "labels": ["Clinton - Positive", "Clinton - Negative"],
        "datasets": datasets
    }

    return jsonify(clinton_json)



################################################################################

@app.route("/donut_chart_trump.json")
def load_trump_donut():
    """Create donut chart representing total neg/pos of tweets about Trump"""


    # Currently only queries on pos/neg not on associated candidate
    pos_trump_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "pos") & (Tweet.referenced_candidate == "Trump")).all()
    neg_trump_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "neg") & (Tweet.referenced_candidate == "Trump")).all()

    datasets = []
    datasets.append({"data" : [len(pos_trump_tweets), len(neg_trump_tweets)], "backgroundColor" : ["rgba(253, 175, 175,1)", "rgba(182,6,6,1)"]})
   

    trump_json = {
        "labels": ["Trump - Positive", "Trump - Negative"],
        "datasets": datasets
    }

    return jsonify(trump_json)


################################################################################



@app.route("/donut_chart_both.json")
def load_both_donut():
    """Create donut chart representing total neg/pos of tweets referencing both candidates"""


     # Currently only queries on pos/neg not on associated candidate
    pos_both_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "pos") & (Tweet.referenced_candidate == "Both")).all()
    neg_both_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "neg") & (Tweet.referenced_candidate == "Both")).all()
    datasets = []
    datasets.append({"data" : [len(pos_both_tweets), len(neg_both_tweets)], "backgroundColor" : ["rgba(199, 244, 213, 1)", "rgba(17, 130, 53, 1)"]})
   

    both_json = {
        "labels": ["Positive", "Negative"],
        "datasets": datasets
    }

    return jsonify(both_json)


################################################################################





@app.route("/sum_comparison.json")
def sum_comparison():
    """Create horizontal chart representing total neg/pos of tweets about Clinton"""

    clinton_tweets = db.session.query(Tweet).filter(Tweet.referenced_candidate == "Clinton").all()
    trump_tweets = db.session.query(Tweet).filter(Tweet.referenced_candidate == "Trump").all()
    both_tweets = db.session.query(Tweet).filter(Tweet.referenced_candidate == "Both").all()


    datasets = []
    datasets.append({"data" : [len(clinton_tweets), len(trump_tweets), len(both_tweets)], 
                    "backgroundColor" : ["rgba(55,7,247,1)", "rgba(182,6,6,1)", "rgba(17, 130, 53, 1)"], 
                    "label": "All Tweets"})
                    

    sum_comparison_json = {
        "labels": ["Clinton", "Trump", "Both"],
        "datasets": datasets
    }

    return jsonify(sum_comparison_json)


################################################################################





@app.route("/google.json")
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
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host='0.0.0.0')

