"""Flask site for """

from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
from model import Tweet, Candidate, connect_to_db, db
from datetime import datetime
import sqlalchemy


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
        pos_scores.append(items[1])
        neg_scores.append(items[2])

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

    colors = {"Trump" : {"backgroundColor" : "rgba(253, 175, 175, 0.2)",
                        "borderColor" : "rgba(253, 175, 175,1)",
                        "pointBorderColor" : "rgba(253, 175, 175,1)",
                        "pointHoverBorderColor" : "rgba(253, 175, 175,1)"},
            "Clinton" : {"backgroundColor" : "rgba(143, 211, 228, 0.2)",
                        "borderColor" : "rgba(143, 211, 228,1)",
                        "pointBorderColor" : "rgba(143, 211, 228,1)",
                        "pointHoverBorderColor" : "rgba(143, 211, 228,1)"}}

    chart_specs = {
                "label": "",
                "fill": False,
                "lineTension": 0.5,
                "backgroundColor": colors[candidate]["backgroundColor"],
                "borderColor": colors[candidate]["borderColor"],
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": colors[candidate]["pointBorderColor"],
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": colors[candidate]["pointHoverBorderColor"],
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": [0], 
                "spanGaps": False}

    return chart_specs




################################################################################




def neg_line_chart(candidate):
    """Generate a json object for sentiment line chart"""

    colors = {"Trump" : {"backgroundColor" : "rgba(182,6,6,0.2)",
                        "borderColor" : "rgba(182,6,6,1)",
                        "pointBorderColor" : "rgba(182,6,6,1)",
                        "pointHoverBorderColor" : "rgba(182,6,6,1)"},
            "Clinton" : {"backgroundColor" : "rgba(55,7,247,0.2)",
                        "borderColor" : "rgba(55,7,247,1)",
                        "pointBorderColor" : "rgba(55,7,247,1)",
                        "pointHoverBorderColor" : "rgba(55,7,247,1)"}}

    chart_specs = {
                "label": "",
                "fill": False,
                "lineTension": 0.5,
                "backgroundColor": colors[candidate]["backgroundColor"],
                "borderColor": colors[candidate]["borderColor"],
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": colors[candidate]["pointBorderColor"],
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": colors[candidate]["pointHoverBorderColor"],
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


    options = {"seed_data/clinton_data.txt" : {"pos_label": "Clinton - Positive", "neg_label": "Clinton - Negative", "candidate" : "Clinton"},
            "seed_data/trump_data.txt" : {"pos_label": "Trump - Positive", "neg_label": "Trump - Negative", "candidate" : "Trump"}}

             # "seed_data/both_data.txt" : {"pos_label" : "Both Referenced - Positive", "pos_label": "Both Referenced - Negative", "candidate" : "Both"}

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


    #currently only queries on pos/neg not on associated candidate
    pos_clinton_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "pos")).all()
    neg_clinton_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "neg")).all()

    # test_clinton_pos = db.session.query(Tweet).filter((Tweet.name == "Clinton")).all()
    # print test_clinton_pos

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


    #currently only queries on pos/neg not on associated candidate
    pos_trump_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "pos")).all()
    neg_trump_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "neg")).all()

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


     #currently only queries on pos/neg not on associated candidate
    pos_both_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "pos")).all()
    neg_both_tweets = db.session.query(Tweet).filter((Tweet.naive_bayes == "neg")).all()
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

    clinton_tweets = db.session.query(Candidate).filter((Candidate.name == "Clinton")).one()
    trump_tweets = db.session.query(Candidate).filter((Candidate.name == "Trump")).one()
    both_tweets = db.session.query(Candidate).filter((Candidate.name == "Both")).one()


    datasets = []
    datasets.append({"data" : [len(clinton_tweets.tweets), len(trump_tweets.tweets), len(both_tweets.tweets)], "backgroundColor" : ["rgba(55,7,247,1)", "rgba(182,6,6,1)", "rgba(17, 130, 53, 1)"], "label": "All Tweets"})
    # datasets.append({"data" : [len(clinton_tweets.tweets)], "backgroundColor": ["rgba(55,7,247,1)"], "label" : "Clinton"})
    # datasets.append({"data" : [len(trump_tweets.tweets)], "backgroundColor": ["rgba(182,6,6,1)"], "label" : "Trump"}) 
    # datasets.append({"data" : [len(both_tweets.tweets)], "backgroundColor": ["rgba(17, 130, 53, 1)"], "label" : "Both"})
                    

    sum_comparison_json = {
        "labels": ["Clinton", "Trump", "Both"],
        "datasets": datasets
    }

    return jsonify(sum_comparison_json)


################################################################################





@app.route("/google.json")
def load_maps_data():
    """Create json object for google maps API"""

    location_data = load_location_data("location_data.txt")

    sentiment_color = {"Trump" : {"neg" : "rgba(253,0,0,1)", "pos" : "rgba(255,199,199,1)"},
                        "Clinton" : {"neg" : "rgba(55,7,247,1)", "pos" : "rgba(143, 211, 228,1)"},
                        "Both" : {"neg" : "rgba(20, 163, 27, 1)", "pos" : "rgba(128, 239, 133, 1)"}}

    json_list = []

    for location in location_data:
        location_specs = {"coordinates": location[0],
                        "num_tweets": float(location[1]), 
                        "color": sentiment_color[location[2]][location[3]]}

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

