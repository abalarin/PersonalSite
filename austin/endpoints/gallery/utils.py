def create_album(client, name):
    client.create_bucket(Bucket=name)


def list_albums(client):
    return client.list_buckets()['Buckets']


def list_images(client, album):
    objects = []
    for key in client.list_objects(Bucket=album)['Contents']:
        objects.append(key['Key'])

    return objects


def add_image(permisson, client, album, file_object, filename):
    client.put_object(ACL=permisson, Body=file_object, Bucket=album, Key=filename, ContentType='image/jpeg')


def get_URL(client, album, file_name):
    return client.generate_presigned_post(Bucket=album, Key=file_name)
