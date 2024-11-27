from minio import Minio
from django.conf import settings
minio_client = Minio(settings.MINIO_ENDPOINT,
               settings.MINIO_ACCESS_KEY, settings.MINIO_SECRET_KEY, secure=False)
try:
    minio_client.list_buckets()
    print("Connected to MinIO Client successfully")
except Exception as e:
    print(f"Error: {e}")
