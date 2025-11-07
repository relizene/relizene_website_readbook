from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = 'static'
    file_overwrite = False
    signature_version = 's3v4'
    region_name = 'ru-central1'
    
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = 'relizene-website'
        kwargs['endpoint_url'] = 'https://storage.yandexcloud.net'
        super().__init__(*args, **kwargs)

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    signature_version = 's3v4'
    region_name = 'ru-central1'
    
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = 'relizene-website'
        kwargs['endpoint_url'] = 'https://storage.yandexcloud.net'
        super().__init__(*args, **kwargs)