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


def get_URL(file_name):
    return client.generate_presigned_post(Bucket='austin', Key=file_name)


def get_albums():
    try:

        result = client.list_objects(Bucket='austin', Prefix='albums/', Delimiter='/')
        album_names = []
        for object in result.get('CommonPrefixes'):
            album_names.append(object['Prefix'][6:].strip('/'))

        albums = []
        for album_name in album_names:
            album = {
                'Name': album_name,
                'images': get_images(album_name)
            }
            albums.append(album)

        return albums

    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})


def get_images(album):
    try:

        prefix = 'albums/' + str(album) + '/'
        result = client.list_objects(Bucket='austin', Prefix=prefix, Delimiter='/')

        image_urls = []
        skipthedir = 0  # becuase the directory itself is also retrived we want to skip it
        for object in result.get('Contents'):
            if skipthedir > 0:
                url = get_URL(object.get('Key'))
                image_urls.append(url.get('url') + '/' + url.get('fields')['key'])
            else:
                skipthedir += 1

        return image_urls


    except Exception as e:
        print(e)
        return jsonify({"error": "There was a problem with the data you provided."})
