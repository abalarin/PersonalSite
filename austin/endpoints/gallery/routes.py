from flask import Blueprint, render_template, jsonify, request, abort
from flask_login import login_required

from .utils import list_albums, get_images


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
def get_album(album):
    try:
        return render_template('gallery/gallery.html', links=get_images(album))

    except Exception as e:
        print(e)
        return abort(404)


# @gallery.route('/create/album', methods=['GET'])
# @login_required
# def create_album():
#     if request.method == "POST":
#         return render_template('gallery/add_album.html')
#
#     return render_template('gallery/add_album.html')
#
