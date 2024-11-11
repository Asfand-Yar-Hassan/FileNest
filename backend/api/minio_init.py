from minio import Minio
from django.conf import settings
client = Minio(settings.MINIO_ENDPOINT,
               settings.MINIO_ACCESS_KEY, settings.MINIO_SECRET_KEY)
