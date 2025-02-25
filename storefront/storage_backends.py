
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = 'public-read'
    region_name = 'nyc3'
    endpoint_url = 'https://nyc3.digitaloceanspaces.com'
    signature_version = 's3v4'
    addressing_style = 'virtual'