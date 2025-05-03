# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Initialize Flask app
app = Flask(__name__)
# Set a secret key for Flask sessions (required by Flask-SocketIO)
# In a real application, use a strong, randomly generated key
app.config['SECRET_KEY'] = 'mysecretkey'
# Initialize Flask-SocketIO
# `cors_allowed_origins="*"` is used here for simplicity to allow connections
# from any origin. In production, you should restrict this to your client's origin.
socketio = SocketIO(app, cors_allowed_origins="*")

# Define a route for the root URL
@app.route('/')
def index():
    # Render the HTML template
    return render_template('index.html')

# SocketIO event handler for client connections
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Emit a message back to the connected client
    emit('status', {'msg': 'Connected to server'})

# SocketIO event handler for client disconnections
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# SocketIO event handler for a custom 'message' event
# This event is triggered when a client sends a message with the event name 'message'
@socketio.on('message')
def handle_message(data):
    print('Received message: ' + str(data))
    # Emit the received message to all connected clients (broadcast=True)
    # This simulates a simple chat application
    emit('message', data, broadcast=True)

# SocketIO event handler for a custom 'my_event'
@socketio.on('my_event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    # You can emit back to the sender or broadcast to others
    # emit('my_response', json) # Emit back to the sender
    emit('my_response', json, broadcast=True) # Broadcast to all

# Main entry point to run the application
# Use eventlet or gevent for production deployment with SocketIO
# For development, the default Werkzeug server is sufficient but not performant
if __name__ == '__main__':
    # Use socketio.run() instead of app.run() when using Flask-SocketIO
    # debug=True enables debug mode, which is useful during development
    # For production, set debug=False
    socketio.run(app, debug=True)

