#will hold flask routes for project

from flask import Flask, render_template, session, request
from flask_debugtoolbar import DebugToolbarExtension
import jinja2


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "h65Tgx4RTzS21"

@app.route("/")
def index_page():
    """Data visualization page"""

    render_template(homepage.html)
