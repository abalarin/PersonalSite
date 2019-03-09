from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required

from .utils import list_albums, list_images, get_URL


gallery = Blueprint('gallery', __name__)


@gallery.route('/albums', methods=['GET'])
def get_buckets():
    try:
        results = list_albums()
        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@gallery.route('/<album>/images', methods=['GET'])
def get_images(album):
    try:
        results = list_images(album)
        links = []
        for result in results:
            url = get_URL(album, result)['url']
            links.append(url + '/' + result)

        return render_template('gallery/gallery.html', links=links)

    except Exception as e:
        print(e)
        return abort(404)


@gallery.route('/create/album', methods=['GET'])
@login_required
def create_album():
    if request.method == "POST":
        return render_template('gallery/add_album.html')

    return render_template('gallery/add_album.html')
