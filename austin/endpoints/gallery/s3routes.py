#
#  Not in use: These are some sample endpoints for CRUD functions of object Storage
#

from flask import Blueprint, jsonify, request

from austin import client, resource

# BOTO STUFF
from austin.botoConfig.objects import *


boto3s = Blueprint('boto3s', __name__)


@boto3s.route('/buckets', methods=['GET'])
def get_buckets():
    try:
        results = listBuckets(client)
        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/buckets', methods=['POST'])
def POST_make_bucket():
    try:
        post_values = request.get_json()

        name = post_values['bucket_name']
        createBucket(client, name)
        return jsonify({"result": "Bucket created!"})
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/objects/<bucket>', methods=['GET'])
def GET_list_objects(bucket):
    results = listObjects(client, bucket)
    return jsonify(results)


@boto3s.route('/objects/<bucket>/<object_file>', methods=['POST'])
def POST_add_object(bucket, object_file):
    try:
        files = request.files['file']
        print(files)
        addObject(client, bucket, files, object_file)
        return jsonify({"result": "Object added!"})
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/download/objects/<bucket>/<object_key>', methods=['GET'])
def Download_Object(bucket, object_key):
    try:
        object = downloadObject(
            client, bucket, object_key, Config.APP_ROOT + "/static/images/test.png")
        return jsonify({"result": "Object Downloaded!"})
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/objects/<bucket>/<object_key>', methods=['GET'])
def Get_Object(bucket, object_key):
    try:
        object = getObject(client, bucket, object_key)
        print(object)
        return jsonify(object['Body'].read())
        # file = object['Body'].read()
        # file = open(bytes)
        # return render_template('index.html', file=file)
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/objects/<bucket>/<object_key>', methods=['POST'])
def change_perms(bucket, object_key):
    try:
        # print("WORK" + ACP['Grants'][0]['Permission'])
        changeObjectPerm(client, bucket, object_key)
        return jsonify({"result": "Object Updated!"})
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/url/<bucket>/<object_id>', methods=['GET'])
def geturl(bucket, object_id):
    try:
        object = getURL(client, bucket, object_id)
        return jsonify(object)
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/location/<bucket>', methods=['GET'])
def getloco(bucket):
    try:
        object = getBucketLocation(client, bucket)
        return jsonify(object)
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/curl/<bucket>', methods=['GET'])
def createurl(bucket):
    try:
        createURL(client, bucket)
        return jsonify({"result": "URL Created!"})
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/bucketperm/<bucket>', methods=['GET'])
def getBucketPerms(bucket):
    try:
        return jsonify(bucketPermissions(client, bucket))
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


@boto3s.route('/bucketperm/<bucket>', methods=['PUT'])
def chgBucketPerms(bucket):
    try:
        changeBucketPermissions(resource, bucket)
        return jsonify(bucketPermissions(client, bucket))
    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})
