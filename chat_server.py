from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Inline HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Chat</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f4f4f4; }
        h2 { color: #333; }
        #chat { width: 100%; height: 300px; margin-bottom: 10px; }
        input, button { padding: 10px; margin-top: 5px; }
    </style>
</head>
<body>
    <h2>Simple Real-Time Chat</h2>
    <input id="username" placeholder="Enter your name" /><br>
    <textarea id="chat" readonly></textarea><br>
    <input id="message" placeholder="Type your message..." />
    <button onclick="sendMessage()">Send</button>

    <script>
        var socket = io();
        var chat = document.getElementById("chat");

        socket.on("message", function(msg) {
            chat.value += msg + "\\n";
        });

        function sendMessage() {
            var user = document.getElementById("username").value || "Anonymous";
            var text = document.getElementById("message").value;
            if (text.trim() !== "") {
                socket.send(user + ": " + text);
                document.getElementById("message").value = "";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@socketio.on('message')
def handle_message(msg):
    print("Received message:", msg)
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)

