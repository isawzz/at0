from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, uuid
from importlib import import_module

# Directories
GAMES_DIR = "games"
SAVED_GAMES_DIR = "saved_games"
os.makedirs(SAVED_GAMES_DIR, exist_ok=True)

# Flask setup
app = Flask(__name__)
CORS(app)  # Allow access from external frontend (e.g., public_html)

#region --- Helper functions ---

from itertools import product

def unfold_cartesian_product(dicts):
    if not dicts:
        return tuple()
    keys = dicts[0].keys()
    result = {key: set() for key in keys}
    for d in dicts:
        for key in keys:
            result[key].add(d[key])
    return tuple([sorted(result[key]) for key in keys])

def fold_cartesian_product(keys, values_lists):
    return [dict(zip(keys, values)) for values in product(*values_lists)]

def get_game_path(game_id):
    return os.path.join(SAVED_GAMES_DIR, f"{game_id}.json")


def save_game_state(game_id, data):
    with open(get_game_path(game_id), "w") as f:
        json.dump(data, f)


def load_game_state(game_id):
    with open(get_game_path(game_id)) as f:
        return json.load(f)
#endregion

#region --- API Routes ---
@app.route("/", methods=["GET"])
def testapp():
    print('testing...')
    return jsonify({"gameid": "Hello!"})

@app.route("/help", methods=["GET"])
def helpme():
    print('hello! you have arrived! the game is: select_a_game')
    return jsonify({"possible_moves": "Hello!"})

@app.route("/test_folding", methods=["GET"])
def test_folding():
    data = [{'x': 'a', 'y': 1}, {'x': 'a', 'y': 2}, {'x': 'b', 'y': 1}, {'x': 'b', 'y': 2}]
    keys = ['x', 'y']

    # Unfold:
    unfolded = unfold_cartesian_product(data)  # (['a', 'b'], [1, 2])

    # Fold:
    folded = fold_cartesian_product(keys, unfolded)
    return jsonify({"possible_moves": {"fold":folded,"unfold":unfolded}})

@app.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()
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

    return jsonify({"gameid": game_id})


@app.route("/game_state/<game_id>", methods=["GET"])
def game_state(game_id):
    try:
        data = load_game_state(game_id)
        game_module = import_module(f'{GAMES_DIR}.{data["gamename"]}')
        game = game_module.Game(data["players"], data["options"])
        game.deserialize(data["state"])
        return jsonify(game.get_state())
    except FileNotFoundError:
        return jsonify({"error": "Game not found"}), 404


@app.route("/make_move/<game_id>", methods=["POST"])
def make_move(game_id):
    try:
        move = request.get_json()["move"]
        data = load_game_state(game_id)

        game_module = import_module(f'{GAMES_DIR}.{data["gamename"]}')
        game = game_module.Game(data["players"], data["options"])
        game.deserialize(data["state"])

        result = game.make_move(move)
        data["state"] = game.serialize()
        save_game_state(game_id, data)

        return jsonify(result)
    except FileNotFoundError:
        return jsonify({"error": "Game not found"}), 404


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


# --- Main ---

if __name__ == "__main__":
    app.run(debug=True)
