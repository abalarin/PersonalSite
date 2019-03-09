import json
import requests

from austin.models.site_models import Configuration
from austin import Config, db


def authenticate_spotify():
    """ Gets new spotify bearer token """

    config = Configuration.query.get(1)

    # Build out spotify authentication POST
    grant_type = "grant_type=authorization_code"
    code = "&code=" + config.spotify_code
    redirect_uri = "&redirect_uri=" + Config.SPOTIFY_REDIRECT
    client_id = "&client_id=" + Config.SPOTIFY_ID
    client_secret = "&client_secret=" + Config.SPOTIFY_SECRET

    payload = grant_type + code + redirect_uri + client_id + client_secret

    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = 'https://accounts.spotify.com/api/token'

    # Once authenticated, Bearer Token will be returned for User data access
    response = requests.post(url, data=payload, headers=headers)
    access_token = json.loads(response.text)['access_token']
    refresh_token = json.loads(response.text)['refresh_token']

    # Update Site Configuration Table with Spotify Bearer Token
    config.spotify_access_token = access_token
    config.spotify_refresh_token = refresh_token
    db.session.commit()


def reauth_spotify():
    """ Get a new  Spotify access token with the Refresh token """

    config = Configuration.query.get(1)

    # Build out spotify authentication POST
    grant_type = "grant_type=refresh_token"
    refresh_token = "&refresh_token=" + config.spotify_refresh_token
    client_id = "&client_id=" + Config.SPOTIFY_ID
    client_secret = "&client_secret=" + Config.SPOTIFY_SECRET

    payload = grant_type + refresh_token + client_id + client_secret

    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    url = 'https://accounts.spotify.com/api/token'

    # Once authenticated, Bearer Token will be returned for User data access
    response = requests.post(url, data=payload, headers=headers)
    access_token = json.loads(response.text)['access_token']

    # Update Site Configuration Table with Spotify Bearer Token
    config.spotify_access_token = access_token
    db.session.commit()
    return access_token


def spotify_feed(limit):
    """ Return # of the most recent Spotify Songs Played """

    url = "https://api.spotify.com/v1/me/player/recently-played"
    querystring = {"limit": str(limit)}

    headers = {
        'Authorization': "Bearer " + Configuration.query.get(1).spotify_access_token
    }

    response = requests.get(url, data="", headers=headers, params=querystring)
    response = json.loads(response.text)

    # Check if the Access Token is not expired, if not KeyError will be thrown
    try:
        if response['error']:
            headers = {
                'Authorization': "Bearer " + reauth_spotify()
            }

            response = requests.get(
                url, data="", headers=headers, params=querystring)
            response = json.loads(response.text)
            return response

    # If Key Error is thrown then there was no error in get request, return original response
    except KeyError:
        return response

    return response


def github_feed(limit):
    """ Return # of the most recent Github Actions """

    url = 'https://api.github.com/users/abalarin/events/public'
    token = '?access_token=' + Config.GITHUB_TOKEN

    return requests.get(url + token + '&per_page=' + str(limit)).json()
