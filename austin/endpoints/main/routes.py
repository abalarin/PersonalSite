from flask import Blueprint, render_template
import requests
import datetime
from dateutil import parser

from austin.endpoints.gallery.routes import *
from austin import Config

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', albums=get_albums(), changelog=github_feed())


@main.route('/changelog')
def change_log():
    github_feed = requests.get(
        'https://api.github.com/users/abalarin/events/public?access_token=' + Config.GITHUB_TOKEN).json()
    return render_template('changelog/github.html', changelog=github_feed)

# Return 5 of the most recent Github Actions


def github_feed():
    github_feed = requests.get(
        'https://api.github.com/users/abalarin/events/public?access_token=' + Config.GITHUB_TOKEN + '&per_page=5').json()

    return github_feed

# This is too slow - optimize
@main.context_processor
def jinja_api_caller():
    def get_json_from(url):
        return requests.get(url + '?access_token=' + Config.GITHUB_TOKEN).json()
    return dict(get_json_from=get_json_from)


@main.app_errorhandler(401)
@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('404.html', e=error)
