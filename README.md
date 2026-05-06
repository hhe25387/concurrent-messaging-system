# ICS 32: Direct Messaging Chat Application

**Author:** He He  
**Email:** heh15@uci.edu

---

## 📝 Project Overview
This project is a Direct Messaging Chat application developed for **ICS 32**. It allows users to send and receive direct messages through the **DSP server** using a custom messaging protocol.

## ✨ Key Features
* **DirectMessenger Module**: Handles server communication (sending, receiving, and history).
* **Interactive GUI**: Built with `Tkinter` for easy contact management and messaging.
* **Local Persistence**: Stores messages and contacts locally using a profile system.
* **Real-time Updates**: Automatically retrieves new messages while the app is running.

## 🛠 Tech Stack
* **Python 3**
* **Tkinter** (GUI)
* **Socket Programming**

## 🛠️ Known Issues & Future Architecture Improvements

As this project was initially developed as a foundational course project (ICS 32), the current architecture prioritizes basic functionality and exception resistance over high-concurrency performance. If this were to be scaled for production, I would implement the following improvements:

1. **Asynchronous I/O to Prevent GUI Blocking:** Currently, socket operations in `ds_messenger.py` are synchronous. Under heavy network latency, the Tkinter `mainloop()` might experience blocking (UI freezing). Future iterations would move network requests to a background thread or utilize Python's `asyncio` framework.
2. **Refining Exception Handling:** To guarantee system stability and prevent crash loops, broad exception blocks (`except Exception:`) are currently used. Moving forward, I plan to design more granular exception classes to handle specific socket timeouts and JSON decode errors separately.
3. **Security Enhancements:** The current DSP protocol transmits data via unencrypted JSON strings over TCP sockets as a proof-of-concept. For real-world deployment, TLS/SSL wrappers would be necessary to ensure data privacy.
