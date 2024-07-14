# Remote Control Panel

This project implements a remote control panel using Python and wxPython, allowing real-time screen sharing and remote interaction between a client and server application.

## Features

- Connect to a remote server
- Display real-time screenshots from the server
- Send mouse and keyboard events
- Lock and unlock the server screen
- Shut down the server remotely

## Requirements

- Python 3.x
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
