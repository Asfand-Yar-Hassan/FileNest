# Utility to store and retrieve objects from Minio
from .minio_init import minio_client
from minio.error import S3Error
from .mongo_queries import *
from django.conf import settings
from pathlib import Path
from io import BytesIO


def upload_file(username: str, file_name: str, file_data: bytes):
    """
    Uploads a file to MinIO under the unique bucket for the user and stores metadata in MongoDB.

    Args:
        username (str): The username of the user.
        file_name (str): The name of the file to be uploaded.
        file_data (bytes): The content of the file to be uploaded.
    """
    try:
        # Verify user and bucket
        user = get_user(username)
        if not user:
            print(f"Error: User {username} not found.")
            return None

        user_id = user["_id"]
        bucket_name: str = user.get("bucket_name")

        if not bucket_name:
            print(f"Error: No bucket found for user {user_id}")
            return None

        # Check if bucket exists, create if not
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket: {bucket_name} created")

        # Wrap file_data (bytes) in BytesIO to make it file-like
        file_data_stream = BytesIO(file_data)

        # Upload file to MinIO
        minio_client.put_object(bucket_name, file_name,
                                data=file_data_stream, length=len(file_data))

        # Construct file URL
        file_url = f"{settings.MINIO_ENDPOINT}/{bucket_name}/{file_name}"

        # Store file metadata in MongoDB
        upload_file_metadata(user_id, file_name, file_url, len(file_data))
        print(f"File successfully uploaded: {file_url}")

        return file_url

    except S3Error as e:
        print(f"Error uploading file to MinIO: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def delete_file(username: str, file_name: str):
    """Delete a file for a user

    Args:
        user_id (str)
        file_name (str)
    """
    try:
        user = get_user(username)
        user_id = user["_id"]
        if user:
            bucket_name = user.get("bucket_name")
            if not bucket_name:
                print(f"No bucket found for user {user_id}")
                return
            try:
                delete_file_metadata(user["_id"], file_name)
                minio_client.remove_object(bucket_name, file_name)
            except S3Error as e:
                print(f"Error removing object {e}")
    except Exception as e:
        print(f"Error deleting object {e}")
