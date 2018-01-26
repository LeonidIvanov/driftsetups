from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticS3BotoStorage(S3Boto3Storage):
    location = 'static'


class MediaS3BotoStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False