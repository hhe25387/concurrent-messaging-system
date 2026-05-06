# He He
# heh15@uci.edu
# 82678258

"""
ds_messenger.py

Provides classes for sending and retrieving direct messages
using the DSP server.
"""

# pylint: disable=too-few-public-methods

import json
import socket

from ds_protocol import (
    build_join,
    build_direct_message,
    build_direct_message_new,
    build_direct_message_all,
    extract_json
)


class DirectMessage:
    """
    Represents a direct message retrieved from the server.
    """

    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """
    Handles communication with the DSP server
    for sending and retrieving direct messages.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None
        self.last_error = ""

    @staticmethod
    def _parse_message_response(raw_response: str) -> list:
        """
        Parse a direct-message retrieval response into DirectMessage objects.
        """
        parsed = json.loads(raw_response)
        response = parsed.get("response", {})

        if response.get("type") != "ok":
            return []

        messages = response.get("messages", [])
        parsed_messages = []

        for server_message in messages:
            dm = DirectMessage()
            dm.recipient = (
                server_message.get("from")
                or server_message.get("sender")
            )
            dm.message = (
                server_message.get("message")
                or server_message.get("entry")
            )
            dm.timestamp = server_message.get("timestamp")
            parsed_messages.append(dm)

        return parsed_messages

    def send(self, message: str, recipient: str) -> bool:
        """
        Send a direct message to the specified recipient.
        """
        self.last_error = ""

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(8)
                client.connect((self.dsuserver, 2021))

                send_m = client.makefile('w')
                recv_m = client.makefile('r')

                join_msg = build_join(self.username, self.password)
                send_m.write(join_msg + '\r\n')
                send_m.flush()

                resp = recv_m.readline().strip()
                join_response = extract_json(resp)

                if join_response.type != 'ok':
                    self.last_error = f"Join failed: {join_response.message}"
                    return False

                self.token = join_response.token

                dm_msg = build_direct_message(self.token, message, recipient)
                send_m.write(dm_msg + '\r\n')
                send_m.flush()

                resp = recv_m.readline().strip()
                dm_response = extract_json(resp)

                if dm_response.type != 'ok':
                    self.last_error = (
                        f"Send failed: {dm_response.message}"
                    )
                    return False

                return True

        except socket.gaierror:
            self.last_error = (
                f"Cannot resolve server address: {self.dsuserver}"
            )
            return False
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.last_error = f"Network error: {e}"
            return False

    def retrieve_new(self) -> list:
        """
        Retrieve new direct messages from the server.
        """
        new_messages = []

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(8)
                client.connect((self.dsuserver, 2021))

                send_m = client.makefile('w')
                recv_m = client.makefile('r')

                join_msg = build_join(self.username, self.password)
                send_m.write(join_msg + '\r\n')
                send_m.flush()

                resp = recv_m.readline().strip()
                join_response = extract_json(resp)

                if join_response.type != 'ok':
                    return []

                self.token = join_response.token

                new_msg = build_direct_message_new(self.token)
                send_m.write(new_msg + '\r\n')
                send_m.flush()

                resp = recv_m.readline().strip()
                new_messages.extend(self._parse_message_response(resp))

            return new_messages

        except Exception:  # pylint: disable=broad-exception-caught
            return []

    def retrieve_all(self) -> list:
        """
        Retrieve all direct messages from the server.
        """
        all_messages = []

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(8)
                client.connect((self.dsuserver, 2021))

                send_m = client.makefile('w')
                recv_m = client.makefile('r')

                join_msg = build_join(self.username, self.password)
                send_m.write(join_msg + '\r\n')
                send_m.flush()

                resp = recv_m.readline().strip()
                join_response = extract_json(resp)

                if join_response.type != 'ok':
                    return []

                self.token = join_response.token

                all_msg = build_direct_message_all(self.token)
                send_m.write(all_msg + '\r\n')
                send_m.flush()

                resp = recv_m.readline().strip()
                all_messages.extend(self._parse_message_response(resp))

            return all_messages

        except Exception:  # pylint: disable=broad-exception-caught
            return []
