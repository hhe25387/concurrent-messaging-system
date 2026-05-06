"""
GUI module for the ICS 32 Distributed Social Messenger application.
"""

# pylint: disable=too-many-instance-attributes

import tkinter as tk
from tkinter import messagebox, ttk

import ds_messenger
from Profile import Profile


class Body(tk.Frame):
    """Main body area containing contacts and message editors."""

    def __init__(self, root, recipient_selected_callback=None):
        """Initialize the Body frame."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    @property
    def contacts(self):
        """Return the contact list."""
        return self._contacts

    def node_select(self, _event):
        """Handle contact selection from the tree view."""

        selection = self.posts_tree.selection()

        if not selection:
            return

        index = int(selection[0])
        entry = self._contacts[index]

        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """Insert a contact into the contact list."""
        self._contacts.append(contact)
        contact_id = len(self._contacts) - 1
        self._insert_contact_tree(contact_id, contact)

    def refresh_contacts(self):
        """Rebuild the contact tree from current contact data."""
        self.posts_tree.delete(*self.posts_tree.get_children())
        for idx, contact in enumerate(self._contacts):
            self._insert_contact_tree(idx, contact)

    def _insert_contact_tree(self, contact_id, contact: str):
        """Insert a contact into the tree widget."""
        if len(contact) > 25:
            contact = contact[:24] + "..."
        self.posts_tree.insert('', tk.END, iid=str(contact_id), text=contact)

    def insert_user_message(self, message: str):
        """Insert a message sent by the user."""
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        """Insert a message received from a contact."""
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')

    def get_text_entry(self) -> str:
        """Return the current text from the message editor."""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        """Set the text in the message editor."""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """Create and pack widgets for the Body frame."""
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(
            master=scroll_frame,
            command=self.entry_editor.yview
        )
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """Footer area containing controls and status text."""

    def __init__(self, root, send_callback=None):
        """Initialize the Footer frame."""
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """Handle clicking the send button."""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """Create and pack widgets for the Footer frame."""
        save_button = tk.Button(
            master=self,
            text="Send",
            width=20,
            command=self.send_click
        )
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


# pylint: disable=too-many-instance-attributes
class NewContactDialog(tk.simpledialog.Dialog):
    """Dialog for configuring DS server account information."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """Initialize the dialog."""
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, master):
        """Create the dialog body widgets."""
        self.server_label = tk.Label(master, width=30,
                                     text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(master, width=30)
        if self.server:
            self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(master, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master, width=30)
        if self.user:
            self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(master, width=30, text="Password")
        self.password_label.pack()

        self.password_entry = tk.Entry(master, width=30)
        self.password_entry['show'] = '*'
        if self.pwd:
            self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

        # You need to implement also the region for the user to enter
        # the Password. The code is similar to the Username you see above
        # but you will want to add self.password_entry['show'] = '*'
        # such that when the user types, the only thing that appears are
        # * symbols.
        # self.password...

    def apply(self):
        """Store dialog input values."""
        self.user = self.username_entry.get().strip()
        self.pwd = self.password_entry.get().strip()
        self.server = self.server_entry.get().strip()


class MainApp(tk.Frame):
    """Main application frame for the messenger GUI."""

    def __init__(self, root):
        """Initialize the main application."""
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.direct_messenger = None
        self.profile = Profile()
        self.profile_path = None
        self.checking_new = False
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        # self.direct_messenger = ... continue!

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_profile_path(self):
        """Return the profile file path."""
        if self.username:
            return f"{self.username}.dsu"
        return None

    def save_current_profile(self):
        """Save the current profile to disk."""
        if self.profile_path:
            try:
                self.profile.save_profile(self.profile_path)
            except OSError:
                pass

    def send_message(self):
        """Send the current message."""
        if self.direct_messenger is None:
            messagebox.showerror("Error", "Server not configured.")
            return

        if self.recipient is None:
            messagebox.showwarning("Warning", "Please select a contact.")
            return

        message = self.body.get_text_entry()
        if not message:
            return
        success = self.publish(message)
        if success:
            self.body.set_text_entry("")

    def add_contact(self):
        """Prompt the user to add a contact."""
        contact = tk.simpledialog.askstring(
            "Add Contact",
            "Enter username:"
        )

        if not contact:
            return

        if contact in self.body.contacts:
            confirm = messagebox.askyesno(
                "Contact Exists",
                "This contact already exists.\nDo you still want to add?"
            )
            if not confirm:
                return
        self.body.insert_contact(contact)
        self.profile.add_contact(contact)
        self.save_current_profile()

    def delete_contact(self):
        """Delete the currently selected contact."""
        if self.recipient is None:
            messagebox.showwarning("Warning", "Please select a contact.")
            return

        contact = self.recipient
        confirm = messagebox.askyesno(
            "Delete Contact",
            f"Delete contact '{contact}'?"
        )
        if not confirm:
            return

        if contact in self.body.contacts:
            self.body.contacts.remove(contact)
            self.body.refresh_contacts()

        if contact in self.profile.contacts:
            self.profile.contacts.remove(contact)

        self.profile.messages = [
            msg for msg in self.profile.messages
            if not (
                (msg.get("from") == contact and msg.get("to") == "me")
                or (msg.get("from") == "me" and msg.get("to") == contact)
            )
        ]

        self.recipient = None
        self.body.entry_editor.delete('1.0', tk.END)
        self.save_current_profile()

    def recipient_selected(self, recipient):
        """Set the currently selected recipient."""

        self.recipient = recipient
        self.body.entry_editor.delete('1.0', tk.END)

        for msg in self.profile.messages:

            if msg["from"] == recipient and msg["to"] == "me":
                self.body.insert_contact_message(
                    f"{recipient}: {msg['message']}"
                )

            elif msg["from"] == "me" and msg["to"] == recipient:
                self.body.insert_user_message(
                    f"me: {msg['message']}"
                )

    def configure_server(self):
        """Open the server configuration dialog."""
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)

        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server

        if not (self.username and self.password and self.server):
            return

        self.profile_path = self.get_profile_path()

        self.profile = Profile()

        try:
            self.profile.load_profile(self.profile_path)
        except (OSError, ValueError):
            self.profile.username = self.username
            self.profile.password = self.password
            self.profile.dsuserver = self.server

        self.profile.username = self.username
        self.profile.password = self.password
        self.profile.dsuserver = self.server

        self.direct_messenger = ds_messenger.DirectMessenger(
            dsuserver=self.server,
            username=self.username,
            password=self.password
        )

        self.body.posts_tree.delete(*self.body.posts_tree.get_children())
        self.body.contacts.clear()

        for contact in self.profile.contacts:
            self.body.insert_contact(contact)

        messages = self.direct_messenger.retrieve_all()

        for msg in messages:
            sender = msg.recipient
            message = msg.message
            timestamp = msg.timestamp

            exists = False
            for m in self.profile.messages:
                if (
                        m["from"] == sender
                        and m["to"] == "me"
                        and m["message"] == message
                        and m["timestamp"] == timestamp
                ):
                    exists = True
                    break

            if not exists:
                self.profile.add_message(sender, "me", message, timestamp)

            if sender not in self.profile.contacts:
                self.profile.add_contact(sender)
                if sender not in self.body.contacts:
                    self.body.insert_contact(sender)

        self.save_current_profile()

        if not self.checking_new:
            self.checking_new = True
            self.root.after(2000, self.check_new)
        # You must implement this!
        # You must configure and instantiate your
        # DirectMessenger instance after this line.

    def publish(self, message: str):
        """Send message to the server."""
        if self.direct_messenger is None:
            messagebox.showerror("Error", "Server not configured.")
            return False

        if self.recipient is None:
            messagebox.showwarning("Warning", "Please select a contact.")
            return False

        success = self.direct_messenger.send(message, self.recipient)

        if success:
            self.body.insert_user_message(f"me: {message}")
            self.profile.add_message(
                "me",
                self.recipient,
                message,
                "local"
            )
            self.save_current_profile()
            return True

        if self.direct_messenger.last_error:
            messagebox.showerror("Error", self.direct_messenger.last_error)
        else:
            messagebox.showerror("Error", "Message failed to send.")
        return False

    def check_new(self):
        """Check and retrieve new messages from server."""
        if self.direct_messenger is None:
            return

        new_messages = self.direct_messenger.retrieve_new()
        for msg in new_messages:

            sender = msg.recipient
            message = msg.message
            timestamp = msg.timestamp

            exists = False
            for m in self.profile.messages:
                if (
                        m["from"] == sender
                        and m["to"] == "me"
                        and m["message"] == message
                        and m["timestamp"] == timestamp
                ):
                    exists = True
                    break

            if not exists:
                self.profile.add_message(
                    sender,
                    "me",
                    message,
                    timestamp
                )

            if sender not in self.profile.contacts:
                self.profile.add_contact(sender)
                if sender not in self.body.contacts:
                    self.body.insert_contact(sender)

            if self.recipient == sender:
                self.body.insert_contact_message(f"{sender}: {message}")

        self.save_current_profile()

        self.root.after(2000, self.check_new)

    def on_close(self):
        """Save the profile and close the application."""
        try:
            self.save_current_profile()
        except OSError:  # pylint: disable=broad-exception-caught
            pass

        self.root.destroy()

    def _draw(self):
        """Create and pack widgets for the main application."""
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New')
        menu_file.add_command(label='Open...')
        menu_file.add_command(label='Close')

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Delete Contact',
                                  command=self.delete_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(
            self.root,
            recipient_selected_callback=self.recipient_selected
        )
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
