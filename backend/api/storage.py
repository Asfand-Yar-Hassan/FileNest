# Utility to store and retrieve objects from Minio
from .minio_init import client
from minio.error import S3Error
from .mongo_queries import *
from django.conf import settings


def upload_file(user_id: str, file_name: str, file_data):
    """Uploads file to MinIO under the unique bucket for the user and store metadata in MongoDB

    Args:
        user_id (str)
        file_name (str): source file path
        file_data (_type_)
    """
    try:
        user = get_user_by_id(user_id)
        if user:
            bucket_name = user.get("bucket_name")

            if not bucket_name:
                print(f"Error: No bucket found for user {user_id}")
                return None

        if not client.bucket_exist(bucket_name):
            client.make_bucket(bucket_name)

            print(f"Bucket: {bucket_name} created")

            client.fput_object(bucket_name, file_name,
                               file_data, len(file_data))
            file_url = f"{settings.MINIO_ENDPOINT/bucket_name/file_name}"

            upload_file_metadata(user_id, file_name, file_url, len(file_url))

            print(f"File successfully uploaded: {file_url}")
            return file_url
    except S3Error as e:
        print("Error uploading file: {e}")


def delete_file(user_id: str, file_name: str):
    """Delete a file for a user

    Args:
        user_id (str)
        file_name (str)
    """
    try:
        user = get_user_by_id(user_id)
        if user:
            bucket_name = user.get("bucket_name")
            if not bucket_name:
                print(f"No bucket found for user {user_id}")
                return
            try:
                delete_file_metadata(user_id, file_name)
                client.remove_object(bucket_name, file_name)
            except S3Error as e:
                print(f"Error removing object {e}")
    except Exception as e:
        print(f"Error deleting object {e}")
