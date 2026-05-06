# He He
# heh15@uci.edu
# 82678258

"""
ds_protocol.py

Builds and parses DSP protocol messages for server communication.
"""

import json
from collections import namedtuple
import time

# Namedtuple used to store values retrieved from JSON messages.
Response = namedtuple('Response', ['type', 'message', 'token'])


def build_join(username: str, password: str):
    """
    Build a JSON string for a join request.
    """
    join_dict = {
        "join": {
            "username": username,
            "password": password,
            "token": ""
        }
    }
    return json.dumps(join_dict)


def build_post(token: str, message: str, timestamp: float = None):
    """
    Build a JSON string for a post request.
    """
    if timestamp is None:
        timestamp = time.time()

    post_dict = {
        "token": token,
        "post": {
            "entry": message,
            "timestamp": str(timestamp)
        }
    }
    return json.dumps(post_dict)


def build_bio(token: str, bio: str, timestamp: float = None):
    """
    Build a JSON string for a bio request.
    """
    if timestamp is None:
        timestamp = time.time()

    bio_dict = {
        "token": token,
        "bio": {
            "entry": bio,
            "timestamp": str(timestamp)
        }
    }
    return json.dumps(bio_dict)


def extract_json(json_msg: str):
    """
    Call json.loads on a JSON string and convert it
    to a Response object.
    """
    try:
        json_obj = json.loads(json_msg)
        response = json_obj.get("response", {})
    except json.JSONDecodeError:
        return Response("error", "Invalid JSON", None)

    return Response(
        response.get("type", "error"),
        response.get("message", ""),
        response.get("token", None)
    )


def build_direct_message(token: str, message: str,
                         recipient: str, timestamp: float = None) -> str:
    """
    Build a JSON string for sending a direct message.
    """

    if timestamp is None:
        timestamp = time.time()

    direct_message_dict = {
        "token": token,
        "directmessage": {
            "entry": message,
            "recipient": recipient,
            "timestamp": str(timestamp)
        }
    }

    return json.dumps(direct_message_dict)


def build_direct_message_new(token: str) -> str:
    """
    Build a JSON string requesting new direct messages
    from the server for the authenticated user.
    """
    direct_message_new = {
        "token": token,
        "directmessage": "new"
    }
    return json.dumps(direct_message_new)


def build_direct_message_all(token: str) -> str:
    """
    Build a JSON string requesting all direct messages
    from the server for the authenticated user.
    """
    direct_message_all = {
        "token": token,
        "directmessage": "all"
    }
    return json.dumps(direct_message_all)
