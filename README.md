<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remote Control Panel</title>
</head>
<body>
    <h1>Remote Control Panel</h1>
    <p>This project implements a remote control panel using Python and wxPython, allowing real-time screen sharing and remote interaction between a client and server application.</p>

    <h2>Features</h2>
    <ul>
        <li>Connect to a remote server</li>
        <li>Display real-time screenshots from the server</li>
        <li>Send mouse and keyboard events</li>
        <li>Lock and unlock the server screen</li>
        <li>Shut down the server remotely</li>
    </ul>

    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li>wxPython</li>
        <li>Pillow (for image handling)</li>
        <li><code>pywin32</code> (for Windows-specific functionalities, not required on macOS)</li>
    </ul>
    <p>You can install the required packages using pip:</p>
    <pre><code>pip install wxPython Pillow pywin32</code></pre>
    <p>For macOS users, you may also need to install <code>pyobjc</code>:</p>
    <pre><code>pip install pyobjc</code></pre>

    <h2>Setup</h2>
    <ol>
        <li><strong>Clone the Repository</strong>:
            <pre><code>git clone https://github.com/yourusername/remote-control-panel.git
cd remote-control-panel</code></pre>
        </li>
        <li><strong>Run the Server</strong>:
            <pre><code>python server.py</code></pre>
        </li>
        <li><strong>Run the Client</strong>:
            <pre><code>python project.py</code></pre>
        </li>
    </ol>

    <h2>Usage</h2>
    <ul>
        <li>Click the <strong>CONNECT</strong> button on the client to establish a connection to the server.</li>
        <li>Once connected, click <strong>Play</strong> to start receiving the server's screen as a video feed.</li>
        <li>Use <strong>Lock</strong> to disable server input and <strong>Unlock</strong> to re-enable it.</li>
        <li>The <strong>Shut Down</strong> button will power off the server remotely.</li>
        <li>Click <strong>EXIT</strong> to close the connection gracefully.</li>
    </ul>

    <h2>Notes</h2>
    <ul>
        <li>Ensure that both the client and server are running on the same network.</li>
        <li>Update the IP address in the client code to match the server's address if necessary.</li>
        <li>Make sure the required permissions for screen capturing and input control are granted.</li>
    </ul>

    <h2>License</h2>
    <p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>
</body>
</html>
