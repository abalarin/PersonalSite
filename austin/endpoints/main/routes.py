from flask import Blueprint, render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user

from dateutil import parser, tz
import datetime
import requests
import os
from urllib.parse import urlparse

from austin.endpoints.gallery.routes import *
from austin.models.site_models import Configuration
from austin import Config, db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', albums=get_albums(), changelog=github_feed(5), recently_played=spotify_feed(5))


@main.route('/changelog')
def change_log():
    return render_template('activity/github.html', changelog=github_feed(5))


@main.route('/music')
def music():
    return render_template('activity/spotify.html', recently_played=spotify_feed(50))

@main.route('/spotify')
@login_required
def spotify():
    payload = {
        'response_type': 'code',
        'client_id': Config.SPOTIFY_ID,
        'redirect_uri': Config.SPOTIFY_REDIRECT,
        'scope': 'user-read-recently-played'
    }
    url = 'https://accounts.spotify.com/authorize'
    response = requests.get(url, params=payload)

    return redirect(response.url)

# Spotify redirect callback
@main.route('/callback/')
def callback():

    code = urlparse(request.url).query[5:]
    authenticate_spotify(code)

    return render_template('index.html', albums=get_albums(), changelog=github_feed(5), recently_played=spotify_feed(5))


@main.app_errorhandler(401)
@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('404.html', e=error)


# Gets new spotify bearer token
def authenticate_spotify(SPOTIFY_CODE):

    # Build out spotify authentication POST
    code = "&code=" + SPOTIFY_CODE
    grant_type = "grant_type=authorization_code"
    redirect_uri = "&redirect_uri=" + Config.SPOTIFY_REDIRECT
    client_id = "&client_id=" + Config.SPOTIFY_ID
    client_secret = "&client_secret=" + Config.SPOTIFY_SECRET

    payload = grant_type + code + redirect_uri + client_id + client_secret

    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = 'https://accounts.spotify.com/api/token'

    # Once authenticated, Bearer Token will be returned for User data access
    response = requests.post(url, data=payload, headers=headers)
    access_token = json.loads(response.text)['access_token']

    # Update Site Configuration Table with Spotify Bearer Token
    config = Configuration.query.get(1)
    config.spotify_code = access_token
    db.session.commit()


# Return # of the most recent Spotify Songs Played
def spotify_feed(limit):
    url = "https://api.spotify.com/v1/me/player/recently-played"

    headers = {
        'Authorization': "Bearer " + Configuration.query.get(1).spotify_code
    }

    querystring = {"limit": str(limit)}
    music = requests.get(url, data="", headers=headers, params=querystring)
    print(('spotify: ', music))

    return(json.loads(music.text))


# Return # of the most recent Github Actions
def github_feed(limit):
    github_feed = requests.get(
        'https://api.github.com/users/abalarin/events/public?access_token=' + Config.GITHUB_TOKEN + '&per_page=' + str(limit)).json()

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
