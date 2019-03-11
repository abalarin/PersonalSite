import requests

from austin import Config


def github_feed(limit):
    """ Return # of the most recent Github Actions """

    url = 'https://api.github.com/users/abalarin/events/public'
    token = '?access_token=' + Config.GITHUB_TOKEN

    return requests.get(url + token + '&per_page=' + str(limit)).json()
