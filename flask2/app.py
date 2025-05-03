
import eventlet
eventlet.monkey_patch()  # Ensures that socketio works with eventlet

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os, json, uuid
from importlib import import_module

GAMES_DIR = "games"
SAVED_GAMES_DIR = "saved_games"
os.makedirs(SAVED_GAMES_DIR, exist_ok=True)

app = Flask(__name__, static_folder="templates")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")


def get_game_path(game_id):
    return os.path.join(SAVED_GAMES_DIR, f"{game_id}.json")


def save_game_state(game_id, data):
    with open(get_game_path(game_id), "w") as f:
        json.dump(data, f)


def load_game_state(game_id):
    with open(get_game_path(game_id)) as f:
        return json.load(f)

connected_users = {}  # sid → username

@socketio.on("connect")
def handle_connect():
    sid = request.sid
    ip = request.remote_addr
    print(f":::client connected: IP = {ip}, SID = {sid}")
    # Wait for registration from client

@socketio.on("register")
def handle_register(data):
    sid = request.sid
    username = data.get("username", f"User-{sid[:5]}")
    connected_users[sid] = username
    print(f":::user registered: {username} (SID = {sid})")
    emit("user_joined", f"{username} joined.", broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    username = connected_users.pop(sid, f"Unknown-{sid[:5]}")
    print(f":::client disconnected: {username}")
    emit("user_left", f"{username} left.", broadcast=True)

@socketio.on("chat_message")
def handle_chat_message(data):
    username = data.get('username', 'Unknown')  # Default to 'Unknown' if username is not sent
    message = data.get('message', '')
    print(f":::{username}: {message}")
    emit('chat_message', {'username': username, 'message': message}, broadcast=True)
    # print(f":::chat_message",data)
    # emit('chat_message', data, broadcast=True)

@socketio.on("start_game")
def start_game(data):
    game_name = data["gamename"]
    players = data["players"]
    options = data.get("options", {})
    print(f":::start_game")

    game_module = import_module(f"{GAMES_DIR}.{game_name}")
    game = game_module.Game(players, options)
    game_id = str(uuid.uuid4())

    save_game_state(
        game_id,
        {
            "gamename": game_name,
            "players": players,
            "options": options,
            "state": game.serialize(),
        },
    )

    emit("game_started", {"gameid": game_id, "state": game.get_state()}, broadcast=True)


@socketio.on("make_move")
def make_move(data):
    game_id = data["gameid"]
    move = data["move"]
    print(f":::make_move")
    try:
        info = load_game_state(game_id)
        game_module = import_module(f"{GAMES_DIR}.{info['gamename']}")
        game = game_module.Game(info["players"], info["options"])
        game.deserialize(info["state"])
        result = game.make_move(move)
        info["state"] = game.serialize()
        save_game_state(game_id, info)

        emit(
            "game_update",
            {"gameid": game_id, "result": result, "state": game.get_state()},
            broadcast=True,
        )
    except FileNotFoundError:
        emit("error", {"message": "Game not found"})


@socketio.on("get_state")
def get_state(data):
    game_id = data["gameid"]
    try:
        info = load_game_state(game_id)
        game_module = import_module(f"{GAMES_DIR}.{info['gamename']}")
        game = game_module.Game(info["players"], info["options"])
        game.deserialize(info["state"])
        emit("state", {"gameid": game_id, "state": game.get_state()})
    except FileNotFoundError:
        emit("error", {"message": "Game not found"})


@socketio.on("games_list")
def games_list():
    print(":::game_list")
    emit(
        "games_list",
        [
            f.replace(".py", "")
            for f in os.listdir(GAMES_DIR)
            if f.endswith(".py") and not f.startswith("__")
        ],
    )


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    try:
        socketio.run(app, debug=True)
        # socketio.run(app)     #this uses eventlet
        # app.run(debug=True)   #runs flask server werkzeug?!?!?
    except KeyboardInterrupt:
        print("Server stopped by user.")

