from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required

from austin import client
from .utils import *


gallery = Blueprint('gallery', __name__)


@gallery.route('/buckets', methods=['GET'])
def get_buckets():
    try:
        results = list_albums(client)
        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@gallery.route('/create/album', methods=['GET'])
@login_required
def create_album():
    if request.method == "POST":
        return render_template('gallery/add_album.html')

    return render_template('gallery/add_album.html')


@gallery.route('/<album>/images', methods=['GET'])
def get_images2(album):
    try:
        results = list_images(client, album)
        links = []
        for result in results:
            url = get_URL(client, album, result)['url']
            links.append(url + '/' + result)

        return render_template('gallery/gallery.html', links=links)  # jsonify(links)

    except Exception as e:
        print(e)
        return abort(404)  # jsonify({"error": "There was a problem with the data you provided."})


def get_albums():
    try:
        albums = list_albums(client)
        images = []
        for album in albums:
            album = {
                'Name': album['Name'],
                'images': get_images(album['Name'])
            }
            images.append(album)

        return images

    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


def get_images(album):
    try:
        results = list_images(client, album)
        links = []
        for result in results:
            url = get_URL(client, album, result)['url']
            links.append(url + '/' + result)

        return(links)

    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})
