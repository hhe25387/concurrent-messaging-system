"""
Tests for ds_protocol message building and JSON extraction functions.
"""

import json

from ds_protocol import (
    build_join,
    build_direct_message,
    build_direct_message_new,
    build_direct_message_all,
    extract_json
)


def test_build_join():
    """Test building a join message."""
    msg = build_join("haha", "psw123")
    msg_dict = json.loads(msg)

    assert isinstance(msg, str)
    assert "join" in msg
    assert "haha" in msg
    assert msg_dict["join"]["username"] == "haha"
    assert msg_dict["join"]["password"] == "psw123"
    assert msg_dict["join"]["token"] == ""


def test_build_direct_message():
    """Test building a direct message."""
    msg = build_direct_message("mytoken", "hello", "mark")
    msg_dict = json.loads(msg)

    assert isinstance(msg, str)
    assert "directmessage" in msg
    assert "hello" in msg
    assert "mark" in msg
    assert msg_dict["token"] == "mytoken"
    assert msg_dict["directmessage"]["entry"] == "hello"
    assert msg_dict["directmessage"]["recipient"] == "mark"


def test_build_direct_message_new():
    """Test requesting new direct messages."""
    msg = build_direct_message_new("mytoken")
    msg_dict = json.loads(msg)

    assert isinstance(msg, str)
    assert "new" in msg
    assert msg_dict["token"] == "mytoken"
    assert msg_dict["directmessage"] == "new"


def test_build_direct_message_all():
    """Test requesting all direct messages."""
    msg = build_direct_message_all("mytoken")
    msg_dict = json.loads(msg)

    assert isinstance(msg, str)
    assert "all" in msg
    assert msg_dict["token"] == "mytoken"
    assert msg_dict["directmessage"] == "all"


def test_extract_json():
    """Test extracting JSON response from server message."""
    server_response = '{"response":{"type":"ok","message":"welcome"}}'

    result = extract_json(server_response)

    assert result.type == "ok"
    assert result.message == "welcome"
    assert result.token is None


def test_extract_json_with_token():
    """Test extracting JSON when a token is included."""
    server_response = (
        '{"response":{"type":"ok","message":"welcome back",'
        '"token":"token789"}}'
    )

    result = extract_json(server_response)

    assert result.type == "ok"
    assert result.message == "welcome back"
    assert result.token == "token789"


def test_extract_json_invalid():
    """Test extracting invalid JSON."""
    result = extract_json("not json")

    assert result.type == "error"
    assert result.message == "Invalid JSON"
    assert result.token is None
