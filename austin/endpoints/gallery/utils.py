from flask import jsonify

from austin import client


def create_album(name):
    client.create_bucket(Bucket=name)


def list_albums():
    return client.list_buckets()['Buckets']


def list_images(album):
    objects = []
    for key in client.list_objects(Bucket=album)['Contents']:
        objects.append(key['Key'])

    return objects


def add_image(permisson, album, file_object, filename):
    client.put_object(ACL=permisson, Body=file_object, Bucket=album, Key=filename, ContentType='image/jpeg')


def get_URL(album, file_name):
    return client.generate_presigned_post(Bucket=album, Key=file_name)


def get_albums():
    try:
        albums = list_albums()
        images = []
        for album in albums:
            if album['Name'] != 'linodestuff':
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
        results = list_images(album)
        links = []
        for result in results:
            url = get_URL(album, result)['url']
            links.append(url + '/' + result)

        return(links)

    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})
