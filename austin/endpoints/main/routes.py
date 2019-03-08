from flask import Blueprint, render_template
from dateutil import parser, tz
import datetime

import requests
import json
from urllib.parse import urlparse

from austin.endpoints.gallery.routes import *
from austin import Config

main = Blueprint('main', __name__)


@main.route('/')
def index():
    # return render_template('index.html', albums=get_albums(), changelog=github_feed())
    return redirect(url_for('main.spotify'))


@main.route('/changelog')
def change_log():
    github_feed = requests.get(
        'https://api.github.com/users/abalarin/events/public?access_token=' + Config.GITHUB_TOKEN).json()
    return render_template('changelog/github.html', changelog=github_feed)



@main.app_errorhandler(401)
@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('404.html', e=error)


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

# Date-Time Parser
@main.context_processor
def jinja_time_parger():
    def date_convert(date_time):

        # This assumes datetime is coming from Zulu/UTC zone & convert to EST
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')

        # Get Current Time
        time_now = datetime.datetime.now()

        # Parse given time into datetime type, convert to EST time
        old_time = parser.parse(date_time)
        old_time = old_time.replace(tzinfo=from_zone).astimezone(to_zone)

        # Remove the timezone awareness to calculate time difference
        old_time = old_time.replace(tzinfo=None)
        time_difference = (time_now - old_time).total_seconds()

        if time_difference < 60:
            return(str(int(time_difference)) + " seconds ago")

        elif time_difference < 3600:
            if time_difference < 120:
                return(str(int(time_difference / 60)) + " minute ago")
            else:
                return(str(int(time_difference / 60)) + " minutes ago")

        elif time_difference < 86400:
            if time_difference < 7200:
                return(str(int((time_difference / 60) / 60)) + " hour ago")
            else:
                return(str(int((time_difference / 60) / 60)) + " hours ago")
        else:
            if time_difference < 172800:
                return(str(int(((time_difference / 60) / 60) / 24)) + " day ago")
            else:
                return(str(int(((time_difference / 60) / 60) / 24)) + " days ago")

    return dict(date_convert=date_convert)
