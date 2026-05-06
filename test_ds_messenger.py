"""
Tests for the DirectMessenger class and message retrieval functions.
"""

# pylint: disable=protected-access

from ds_messenger import DirectMessenger, DirectMessage


def test_send():
    """Test sending a direct message."""

    messenger = DirectMessenger(
        dsuserver="ics32.clotho.ics.uci.edu",
        username="haha",
        password="hh123"
    )

    result = messenger.send("hello", "ohhimark")

    assert isinstance(result, bool)


def test_retrieve_new():
    """Test retrieving new messages."""

    messenger = DirectMessenger(
        dsuserver="ics32.clotho.ics.uci.edu",
        username="haha",
        password="hh123"
    )

    result = messenger.retrieve_new()

    assert isinstance(result, list)

    if len(result) > 0:
        assert isinstance(result[0], DirectMessage)


def test_retrieve_all():
    """Test retrieving all messages."""

    messenger = DirectMessenger(
        dsuserver="ics32.clotho.ics.uci.edu",
        username="haha",
        password="hh123"
    )

    result = messenger.retrieve_all()

    assert isinstance(result, list)

    if len(result) > 0:
        assert isinstance(result[0], DirectMessage)


def test_parse_message_response_ok():
    """Test parsing a normal message response."""
    raw_response = (
        '{"response":{"type":"ok","messages":'
        '[{"from":"mark","message":"hello","timestamp":"123"}]}}'
    )

    result = DirectMessenger._parse_message_response(raw_response)

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], DirectMessage)
    assert result[0].recipient == "mark"
    assert result[0].message == "hello"
    assert result[0].timestamp == "123"


def test_parse_message_response_not_ok():
    """Test parsing a failed message response."""
    raw_response = '{"response":{"type":"error","message":"bad request"}}'

    result = DirectMessenger._parse_message_response(raw_response)

    assert not result


def test_send_bad_server():
    """Test sending a message to a bad server."""
    messenger = DirectMessenger(
        dsuserver="bad_server",
        username="haha",
        password="hh123"
    )

    result = messenger.send("hello", "mark")

    assert result is False
