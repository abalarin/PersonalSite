from flask import Blueprint, render_template
import requests

from austin.endpoints.gallery.routes import *
from austin import Config

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', albums=get_albums(), changelog=github_feed())


@main.route('/changelog')
def change_log():
    github_feed = requests.get('https://api.github.com/users/abalarin/events/public?access_token=' + Config.GITHUB_TOKEN).json()
    return render_template('changelog/github.html', changelog=github_feed)


@main.route('/changelog1')
def github_feed():

    github_feed = requests.get('https://api.github.com/users/abalarin/events/public?access_token=' + Config.GITHUB_TOKEN).json()
    
    return github_feed


@main.app_errorhandler(401)
@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('404.html', e=error)
