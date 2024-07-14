# Remote Control Panel

This control software allows extensive control over another computer, enabling the controlling side to fully monitor the activity of the controlled machine and perform various operations. The system consists of two parts: a server (running on the controlled computer) and a client (on the controlling computer). Developed using Python, this software currently works on macOS and requires a connection to a local area network (LAN).

## Features

- Connect to a remote server
- Display real-time screenshots from the server
- Send mouse and keyboard events
- Lock and unlock the server screen
- Shut down the server remotely

## Requirements

- Python 2
- wxPython
- Pillow (for image handling)
- `pywin32` (for Windows-specific functionalities, not required on macOS)

## Setup
 - Run the Server: Start the server.py application first to listen for incoming connections.
- Run the Client: Start the project.py application to connect to the server.

## Usage
- Click the CONNECT button on the client to establish a connection to the server.
- Once connected, click Play to start receiving the server's screen as a video feed.
- Use Lock to disable server input and Unlock to re-enable it.
- The Shut Down button will power off the server remotely.
- Click EXIT to close the connection gracefully.

## Notes
- Ensure that both the client and server are running on the same network.
- Update the IP address in the client code to match the server's address if necessary.
- Make sure the required permissions for screen capturing and input control are granted.
