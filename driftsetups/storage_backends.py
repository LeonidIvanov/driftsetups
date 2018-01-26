from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION

    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        print(name)
        if not name.endswith('/'):
            name += "/"

        name += self.location
        return name


class MediaStorage(S3Boto3Storage):
    location = settings.AWS_MEDIA_LOCATION
    file_overwrite = False

    def _clean_name(self, name):
        return name

    def _normalize_name(self, name):
        if not name.endswith('/'):
            print(name)
            name += "/"

        name += self.location
        return name
