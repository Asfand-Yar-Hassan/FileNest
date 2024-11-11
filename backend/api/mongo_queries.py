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

    # store user data
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    # Insert into the 'users' colllection
    user_id: str = db.users.insert_one(user_data).inserted_id
    return user_id


def get_user_by_username(username: str):
    """
    Get user by username
    """
    return db.users.find_one({"username": username})


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
    return list(db.files.find({"user": ObjectId(user_id)}))


def get_file(file_id: str):
    """Retrieve a file using file_id
    """
    return db.files.find_one({"_id": ObjectId(file_id)})
