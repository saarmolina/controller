# Controller 

This control software allows extensive control over another computer, enabling the controlling side to fully monitor the activity of the controlled machine and perform various operations. The system consists of two parts: a server (running on the controlled computer) and a client (on the controlling computer). Developed using Python, this software currently works on macOS and requires a connection to a local area network (LAN).

## Features

- Connect to a remote server
- Display real-time screenshots from the server
- Send mouse and keyboard events
- Lock and unlock the server screen
- Shut down the server remotely

## Requirements

- Python 3 (recommended)
- wxPython
- Pillow (for image handling)
- pyautogui (for mouse actions)

## Configuration

- IP Address: In the client.py file, update the IP address in the connectServer method to match the server's address if it differs from 1.1.1.1.
- Files: Ensure the files are present in the same directory.

## Setup

1. **Install Dependencies**: Ensure you have the required Python packages installed. You can install them using pip:
   
   ```bash
   pip install wxPython Pillow pyautogui
   ```

3. **Run the Server**: Start the server.py application first to listen for incoming connections. You can run it from the terminal:
   
   ```bash
   python server.py
   ```
   
4. Run the Client: Start the client.py application to connect to the server:

   ```bash
   python client.py
   ```
   
## Usage Guide
1. Establish Connection: Click the CONNECT button on the client to establish a connection to the server.
2. Start Video Feed: Once connected, click Play to start receiving the server's screen as a video feed.
3. Control Server:
   - Use Lock to disable server input.
   - Use Unlock to re-enable server input.
   - The Shut Down button will power off the server remotely.
4. Exit: Click EXIT to close the connection gracefully.

## Important Notes
- Ensure that both the client and server are running on the same network for proper communication.
- Make sure to grant the required permissions for screen capturing and input control in macOS:
  - Go to System Preferences > Security & Privacy > Privacy tab.
  - Ensure that your Python interpreter or terminal has access to Screen Recording and Accessibility.
- If you encounter issues with permissions, restart your applications after granting access.

