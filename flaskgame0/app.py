
import eventlet
eventlet.monkey_patch()  # Ensures that socketio works with eventlet

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os, sys, json, uuid, random, string
from itertools import product
from importlib import import_module

GAMES_DIR = "games"
SAVED_GAMES_DIR = "saved_games"
os.makedirs(SAVED_GAMES_DIR, exist_ok=True)

app = Flask(__name__, static_folder="templates")
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

# region --- Helper functions ---

def cartesian_per_row(data):
    results = []
    for row in data:
        keys = list(row.keys())
        values = list(row.values())
        results.append([keys, values])
    return results

def cartesian_contract(dict_list):
    """
    Given a list of dictionaries with identical keys, return:
    (keys, list of value lists for each key)
    """
    if not dict_list:
        return [], []

    keys = list(dict_list[0].keys())
    values_lists = [[] for _ in keys]

    for d in dict_list:
        for i, key in enumerate(keys):
            if d[key] not in values_lists[i]:
                values_lists[i].append(d[key])

    return keys, values_lists

def cartesian_expand(keys, values_lists):
    product_list = [dict(zip(keys, combo)) for combo in product(*values_lists)]
    return product_list

def delete_all_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def generate_id(s: str, n: int) -> str:
  if not isinstance(n, int) or n <= 0:
    raise ValueError("Number of digits 'n' must be a positive integer.")
  return f"{s}_{''.join(random.choices(string.digits, k=n))}"

def get_game_path(game_id):
    return os.path.join(SAVED_GAMES_DIR, f"{game_id}.json")

def save_game_state(game_id, data):
    with open(get_game_path(game_id), "w") as f:
        json.dump(data, f)

def load_game_state(game_id):
    with open(get_game_path(game_id)) as f:
        return json.load(f)

# endregion

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
    return "game server running!"; #render_template("index.html")

@app.route("/save_game/<game_id>", methods=["POST"])
def save_game(game_id):
    data = request.get_json()
    save_game_state(game_id, data)
    return jsonify({"status": "saved"})


@app.route("/load_game/<game_id>", methods=["GET"])
def load_game(game_id):
    try:
        return jsonify(load_game_state(game_id))
    except FileNotFoundError:
        return jsonify({"error": "Game not found"}), 404


@app.route("/delete_game/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    try:
        os.remove(get_game_path(game_id))
        return jsonify({"status": "deleted"})
    except FileNotFoundError:
        return jsonify({"error": "Game not found"}), 404

@app.route("/delete_games", methods=["DELETE"])
def delete_games():
    delete_all_files(SAVED_GAMES_DIR)
    return jsonify({"status": "deleted"})

@app.route("/get_tables", methods=["GET"])
def get_tables():
    """Return all saved game data."""
    tables = {}
    for filename in os.listdir(SAVED_GAMES_DIR):
        if filename.endswith(".json"):
            game_id = filename.rsplit(".", 1)[0]
            try:
                tables[game_id] = load_game_state(game_id)
            except Exception as e:
                tables[game_id] = {"error": str(e)}
    return jsonify(tables)


@app.route("/get_table_names", methods=["GET"])
def get_table_names():
    """Return a list of all saved game IDs (filenames without extension)."""
    names = [
        filename.rsplit(".", 1)[0]
        for filename in os.listdir(SAVED_GAMES_DIR)
        if filename.endswith(".json")
    ]
    return jsonify(names)


if __name__ == "__main__":
    try:
        socketio.run(app, debug=True)
        # socketio.run(app)     #this uses eventlet
        # app.run(debug=True)   #runs flask server werkzeug?!?!?
    except KeyboardInterrupt:
        print("Server stopped by user.")

