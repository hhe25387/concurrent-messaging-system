# He He
# heh15@uci.edu
# 82678258

"""
Profile module.

Provides classes used to manage DSU user profiles and posts.
"""

# pylint: disable=invalid-name, redefined-outer-name

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """Exception raised when DSU file operations fail."""


class DsuProfileError(Exception):
    """Exception raised when DSU profile deserialization fails."""


class Post(dict):
    """
    Represents a single user post.

    Stores the entry text and timestamp.
    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        """Initialize post."""
        self._timestamp = timestamp
        self.set_entry(entry)

        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        """Set entry text."""
        self._entry = entry
        dict.__setitem__(self, "entry", entry)

        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        """Get entry text."""
        return self._entry

    def set_time(self, timestamp: float):
        """Set timestamp."""
        self._timestamp = timestamp
        dict.__setitem__(self, "timestamp", timestamp)

    def get_time(self):
        """Get timestamp."""
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    Represents a DSU user profile.

    Stores username, password, server, bio, and posts.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        """Initialize profile."""
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ""
        self._posts = []
        self.contacts = []
        self.messages = []

    def add_post(self, post: Post) -> None:
        """Add post."""
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """Delete post."""
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:
        """Return posts."""
        return self._posts

    def save_profile(self, path: str) -> None:
        """Save profile to DSU file."""
        p = Path(path)

        if p.suffix == ".dsu":
            try:
                with open(p, "w", encoding="utf-8") as f:
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError(
                    "Error while attempting to process the DSU file."
                ) from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """Load profile from DSU file."""
        p = Path(path)

        if p.exists() and p.suffix == ".dsu":
            try:
                with open(p, "r", encoding="utf-8") as f:
                    obj = json.load(f)

                self.username = obj.get("username")
                self.password = obj.get("password")
                self.dsuserver = obj.get("dsuserver")
                self.bio = obj.get("bio", "")
                self.contacts = obj.get("contacts", [])
                self.messages = obj.get("messages", [])

                self._posts = []
                for post_obj in obj.get("_posts", []):
                    post = Post(
                        post_obj["entry"],
                        post_obj["timestamp"]
                    )
                    self._posts.append(post)

            except Exception as ex:
                raise DsuProfileError(ex) from ex
        else:
            raise DsuFileError()

    def add_contact(self, username: str):
        """Add a new contact."""
        if username not in self.contacts:
            self.contacts.append(username)

    def add_message(self, sender, recipient, message, timestamp):
        """Store a message locally."""

        msg = {
            "from": sender,
            "to": recipient,
            "message": message,
            "timestamp": timestamp
        }
        self.messages.append(msg)
