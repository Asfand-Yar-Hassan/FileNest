from .mongo_init import client
import bcrypt
from bson.objectid import ObjectId
from datetime import datetime

client.list_database_names()
db = client["file_nest_db"]


def create_user(username: str, email: str, password: str):
    """
    Add a user record into users collection
    """
    # hash password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    bucket_name = f"user.{username}.bucket"
    # store user data
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "bucket_name": bucket_name
    }
    # Insert into the 'users' colllection
    user_id: str = db.users.insert_one(user_data).inserted_id
    return user_id


def get_user(user_id: str):
    "Get a user"
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return user


def get_user_by_username(username: str):
    user = db.users.find_one({"username": username})
    return user


def verify_user(username: str, password: str):
    """"
    Verifies if the username and pawweord match an existing user
    """
    user = get_user_by_username(username)

    # Check if user exists and the password matches
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user
    return None


def upload_file_metadata(user_id: str, file_name: str, file_url: str, file_size: int):
    """
    Store file metadata for a given use in the files collection
    """
    file_data = {
        "user": ObjectId(user_id),
        "file_name": file_name,
        "file_url": file_url,
        "file_size": file_size,
        "uploaded_at": datetime.now()
    }
    file_id = db.files.insert_one(file_data).inserted_id
    return str(file_id)


def get_files_by_user(user_id: str):
    """
    Get all files for a user
    """
    files = db.files.find({"user": ObjectId(user_id)})
    return [
        {**file, "_id": str(file["_id"]), "user": str(file["user"])}
        for file in files
    ]


def get_file_metadata_by_user_and_name(user_id: str, file_name: str):
    """
    Retrieve file metadata based on the user_id and file_name.

    :param user_id: User's unique ID.
    :param file_name: Name of the file to search for.
    :return: File metadata or None if not found.
    """
    return db.files.find_one({"user": ObjectId(user_id), "file_name": file_name})


def get_file_url(file_url: str):
    """Retrieve a file using file_id
    """
    return db.files.find_one({"file_url": file_url})


def delete_file_metadata(user_id: str, file_id: str):
    """
    Delete file metadata from MongoDB after file is deleted from MinIO
    """
    try:
        return db.files.delete_one({
            "_id": ObjectId(file_id),
            "user": ObjectId(user_id)
        })
    except Exception as e:
        print(
            f"Was unable to delete file {file_id} metadata from database.\n Error {e}")


def get_file_by_id(user_id: str, file_id: str):
    """
    Get file metadata by ID and user ID
    """
    return db.files.find_one({
        "_id": ObjectId(file_id),
        "user": ObjectId(user_id)
    })
