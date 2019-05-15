from flask import jsonify
from dateutil import parser, tz
import datetime
import requests

from austin import Config


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

    return dict(date_convert)


def github_feed(limit):
    """ Return # of the most recent Github Actions """

    url = 'https://api.github.com/users/abalarin/events/public'
    token = '?access_token=' + Config.GITHUB_TOKEN

    github_resp = requests.get(url + token + '&per_page=' + str(limit)).json()

    # print(github_resp)
    for event in github_resp:
        if event['type'] == 'WatchEvent':
            event['type'] = ' is watching'
        if event['type'] == 'ForkEvent':
            event['type'] = ' forked'
        if event['type'] == 'PushEvent':
            event['type'] = ' pushed to'
        if event['type'] == 'PullRequestEvent':
            event['type'] = ' pulled from'
        if event['type'] == 'CreateEvent':
            event['type'] = ' created repo'
        if event['type'] == 'DeleteEvent':
            event['type'] = ' deleted repo'
        if event['type'] == 'IssueCommentEvent':
            event['type'] = ' commented on'
        if event['type'] == 'IssuesEvent':
            if event['payload']['action'] == 'closed':
                event['type'] = 'closed out an issue on'
            elif event['payload']['action'] == 'opened':
                event['type'] = 'opened an issue on '

        event['created_at'] = date_convert(event['created_at'])

    return github_resp
