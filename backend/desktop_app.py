"""
IntelliAudit Desktop App
-------------------------
Runs the FastAPI backend in the background and opens the app
in its own plain window (no browser bar, no tabs).
"""

import threading
import time

import uvicorn
import webview


def start_server():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level="warning")


if __name__ == "__main__":
    # Start the FastAPI server in a background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Give the server a moment to start up before opening the window
    time.sleep(1.5)

    # Open the app in its own desktop window
    webview.create_window(
        "IntelliAudit | Enterprise Risk & Fraud Detection",
        "http://127.0.0.1:8000/",
        width=1400,
        height=900,
        min_size=(900, 600),
    )
    webview.start()
