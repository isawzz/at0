from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os, json, uuid
from importlib import import_module

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

GAMES_DIR = "games"
SAVED_GAMES_DIR = "saved_games"
os.makedirs(SAVED_GAMES_DIR, exist_ok=True)


def get_game_path(game_id):
    return os.path.join(SAVED_GAMES_DIR, f"{game_id}.json")


def save_game_state(game_id, data):
    with open(get_game_path(game_id), "w") as f:
        json.dump(data, f)


def load_game_state(game_id):
    with open(get_game_path(game_id)) as f:
        return json.load(f)


@socketio.on("start_game")
def start_game(data):
    game_name = data["gamename"]
    players = data["players"]
    options = data.get("options", {})

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
    socketio.run(app, debug=True)
