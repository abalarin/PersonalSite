def createBucket(client, name):
    client.create_bucket(Bucket=name)


def addObject(client, bucket, file, filename):
    client.put_object(ACL="public-read", Body=file,
                      Bucket=bucket, Key=filename, ContentType='image/jpeg')


def downloadObject(client, bucket, object_key, local_file):
    returned_object = client.download_file(bucket, object_key, local_file)
    return returned_object


def getObject(client, bucket, object_key):
    returned_object = client.get_object(Bucket=bucket, Key=object_key)
    return returned_object


def listObjects(client, bucket):
    objects = []
    for key in client.list_objects(Bucket=bucket)['Contents']:
        objects.append(key['Key'])
    return objects


def listBuckets(client):
    return client.list_buckets()


def objectPermissions(client, bucket, object_key):
    return client.get_object_acl(Bucket=bucket, Key=object_key)


def changeObjectPerm(client, bucket, object_key):

    ACP = {
        'Grants': [{
            'Grantee': {
                'DisplayName': 'Everyone',
                'Type': 'Group',
            },
            'Permission': 'READ',
        }]
    }

    # Convert the policy to a JSON string
    # policy = json.dumps(ACP)

    client.put_object_acl(ACL='public-read', AccessControlPolicy=ACP, Bucket=bucket, Key=object_key)


def bucketPermissions(client, bucket):
    return client.get_bucket_acl(Bucket=bucket)


def changeBucketPermissions(resource, bucket):
    bucket_acl = resource.BucketAcl(bucket)
    bucket_acl.put(ACL="public-read")


def getURL(client, bucket, obj_key):
    return client.generate_presigned_post(Bucket=bucket, Key=obj_key)


def getBucketLocation(client, bucket):
    return client.get_bucket_location(Bucket=bucket)


def createURL(client, bucket):
    # Create the configuration for the website
    website_configuration = {
        'ErrorDocument': {'Key': 'error.html'},
        'IndexDocument': {'Suffix': 'index.html'},
        'RedirectAllRequestsTo': {
            'HostName': 'austinbalarin.com',
            'Protocol': 'http'
        }
    }

    # Set the new policy on the selected bucket
    client.put_bucket_website(
        Bucket=bucket,
        WebsiteConfiguration=website_configuration
    )
