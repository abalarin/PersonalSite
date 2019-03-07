from flask import Blueprint, render_template, redirect, url_for
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


@main.route('/changelog1')
def github_feed():

    github_feed = requests.get(
        'https://api.github.com/users/abalarin/events/public?access_token=' + Config.GITHUB_TOKEN).json()

    return github_feed


@main.route('/callback/')
def callback():

    code = urlparse(request.url).query[5:]
    print("code=" + code)
    recently_played = get_recently_played(code)
    # return(recently_played)
    return render_template('index.html', albums=get_albums(), changelog=github_feed(), recently_played=recently_played)


@main.route('/spotify')
def spotify():
    payload = {
        'response_type': 'code',
        'client_id': Config.SPOTIFY_ID,
        'redirect_uri': 'http://127.0.0.1:5000/callback/',
        'scope': 'user-read-recently-played'
    }
    response = requests.get(
        'https://accounts.spotify.com/authorize', params=payload)
    print(response.text)
    return redirect(response.url)


def get_recently_played(SPOTIFY_CODE):

    code = "&code=" + SPOTIFY_CODE
    grant_type = "grant_type=authorization_code"
    redirect_uri = "&redirect_uri=http://127.0.0.1:5000/callback/"
    client_id = "&client_id=" + Config.SPOTIFY_ID
    client_secret = "&client_secret=" + Config.SPOTIFY_SECRET

    payload = grant_type + code + redirect_uri + client_id + client_secret

    headers = { 'Content-Type': "application/x-www-form-urlencoded" }
    response = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)
    print(response)

    print("------------------SPOTIFY-------------------------")
    url = "https://api.spotify.com/v1/me/player/recently-played"

    headers = {
        'Authorization': "Bearer " + json.loads(response.text)['access_token']
        }

    music = requests.get(url, data="", headers=headers)
    # print(music.text)
    return json.loads(music.text)


@main.app_errorhandler(401)
@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('404.html', e=error)
