"""Flask site for """

from flask import Flask, render_template, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
from model import Tweet, connect_to_db


app = Flask(__name__)
app.secret_key = "h65Tgx4RTzS21"


def load_data(filename):
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


def pos_line_chart():
    """Generate a json object for sentiment line chart"""

    chart_specs = {
                "label": "",
                "fill": False,
                "lineTension": 0.5,
                "backgroundColor": "rgba(220,220,220,0.2)",
                "borderColor": "rgba(220,220,220,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(220,220,220,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(220,220,220,1)",
                "pointHoverBorderWidth": 2,
                "pointRadius": 3,
                "pointHitRadius": 10,
                "data": [0], 
                "spanGaps": False}

    return chart_specs


def neg_line_chart():
    """Generate a json object for sentiment line chart"""

    chart_specs = {
                "label": "",
                "fill": False,
                "lineTension": 0.5,
                "backgroundColor": "rgba(151,187,205,0.2)",
                "borderColor": "rgba(151,187,205,1)",
                "borderCapStyle": 'butt',
                "borderDash": [],
                "borderDashOffset": 0.0,
                "borderJoinStyle": 'miter',
                "pointBorderColor": "rgba(151,187,205,1)",
                "pointBackgroundColor": "#fff",
                "pointBorderWidth": 1,
                "pointHoverRadius": 5,
                "pointHoverBackgroundColor": "#fff",
                "pointHoverBorderColor": "rgba(151,187,205,1)",
                "pointHoverBorderWidth": 2,
                "pointHitRadius": 10,
                "data": [0], 
                "spanGaps": False}

    return chart_specs



@app.route("/")
def homepage():
    """Data visualization page"""



    return render_template("homepage_charts.html")


@app.route("/sentiment_data.json")
def load_csv():
    """Load in data from csv format"""


    options = {"seed_data/clinton_data.txt" : {"pos_label": "Clinton - Positive", "neg_label": "Clinton - Negative"},
            "seed_data/trump_data.txt" : {"pos_label": "Trump - Positive", "neg_label": "Trump - Negative"}}

    datasets = []

    for option in options.keys():
        print option
        dates, pos_nums, neg_nums = load_data(option)

        pos_json_object = pos_line_chart()
        pos_json_object["label"] = options[option]["pos_label"]
        pos_json_object["data"] = pos_nums
        datasets.append(pos_json_object)

        neg_json_object = neg_line_chart()
        neg_json_object["label"] = options[option]["neg_label"]
        neg_json_object["data"] = neg_nums
        datasets.append(neg_json_object)
    print datasets

    json_test = {
        "labels": dates,
        "datasets": datasets
    }

    return jsonify(json_test)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host='0.0.0.0')