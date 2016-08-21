"""Flask site for """

from flask import Flask, render_template, session, request
from flask_debugtoolbar import DebugToolbarExtension
import jinja2
from model import Tweet, connect_to_db


app = Flask(__name__)
app.secret_key = "h65Tgx4RTzS21"

@app.route("/")
def homepage():
    """Data visualization page"""

    tweets = {}
    for tweet in Tweet.query.all():
        tweets[tweet.tweet_id] = {
            
        }


    return render_template("homepage.html", data=data)



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host='0.0.0.0')