from storages.backends.s3boto3 import S3Boto3Storage

class CustomS3Boto3Storage(S3Boto3Storage):
    def url(self, name):
        # Get the base URL without query parameters
        base_url = super().url(name).split('?')[0]
        return base_url

