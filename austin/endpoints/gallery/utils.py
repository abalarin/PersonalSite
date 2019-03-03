import boto3
import json


def createAlbum(client, name):
    client.create_bucket(Bucket=name)

def listAlbums(client):
    return client.list_buckets()['Buckets']

def listImages(client, album):
    objects = []
    for key in client.list_objects(Bucket=album)['Contents']:
        objects.append(key['Key'])
        
    return objects

def addImage(permisson, client, album, file, filename):
    client.put_object(ACL=permisson, Body=file, Bucket=album, Key=filename, ContentType='image/jpeg')

def getURL(client, album, file_name):
    return client.generate_presigned_post(Bucket=album, Key=file_name)
