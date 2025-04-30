from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
import uuid
import os
import json
from importlib import import_module

GAMES_DIR = 'games'
SAVED_GAMES_DIR = 'saved_games'

os.makedirs(SAVED_GAMES_DIR, exist_ok=True)

# Create an instance of the Flask class
app = Flask(__name__, static_folder='static')
CORS(app)

# --- Flask Routes ---

@app.route('/sim/')
def rootsim():
	return send_from_directory('templates', 'index.html')

@app.route('/')
def index():
	return send_from_directory('templates', 'index.html')
    # return 'hello, you are right here!'

@app.route('/<path:path>')
def rootsimPath(path):
	res = send_from_directory('', path)
	return send_from_directory('', path)

from ttt import (
    board,
    current_player,
    game_over,
    winner,
    initialize_board,
    get_possible_moves,
    make_move,
    check_win,
    check_draw
)

@app.route('/restart', methods=['POST'])
def restart_game():
    """Restarts the game."""
    # Use the imported initialize_board function
    initialize_board()
    # Access updated game state directly from the imported variables
    state = {
        'board': board.tolist(),
        'current_player': current_player,
        'possible_moves': get_possible_moves(board),
        'game_over': game_over,
        'winner': winner
    }
    return jsonify(state)

# --- Helper Functions ---
def get_game_path(game_id):
    return os.path.join(SAVED_GAMES_DIR, f'{game_id}.json')

def save_game_state(game_id, data):
    with open(get_game_path(game_id), 'w') as f:
        json.dump(data, f)

def load_game_state(game_id):
    with open(get_game_path(game_id)) as f:
        return json.load(f)

# --- Routes ---

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.json
    game_name = data['gamename']
    players = data['players']
    options = data.get('options', {})

    game_module = import_module(f'{GAMES_DIR}.{game_name}')
    game = game_module.Game(players, options)
    game_id = str(uuid.uuid4())

    state = game.serialize()
    save_game_state(game_id, {
        'gamename': game_name,
        'players': players,
        'options': options,
        'state': state
    })

    return jsonify({'gameid': game_id})

@app.route('/load_game/<game_id>', methods=['GET'])
def load_game(game_id):
    try:
        return jsonify(load_game_state(game_id))
    except FileNotFoundError:
        return jsonify({'error': 'Game not found'}), 404

@app.route('/save_game/<game_id>', methods=['POST'])
def save_game(game_id):
    data = request.json
    save_game_state(game_id, data)
    return jsonify({'status': 'saved'})

@app.route('/delete_game/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    try:
        os.remove(get_game_path(game_id))
        return jsonify({'status': 'deleted'})
    except FileNotFoundError:
        return jsonify({'error': 'Game not found'}), 404

@app.route('/game_state/<game_id>', methods=['GET'])
def game_state(game_id):
    try:
        data = load_game_state(game_id)
        game_module = import_module(f'{GAMES_DIR}.{data["gamename"]}')
        game = game_module.Game(data['players'], data['options'])
        game.deserialize(data['state'])

        return jsonify(game.get_state())
    except FileNotFoundError:
        return jsonify({'error': 'Game not found'}), 404

@app.route('/make_move/<game_id>', methods=['POST'])
def make_move(game_id):
    try:
        move = request.json['move']
        data = load_game_state(game_id)
        game_module = import_module(f'{GAMES_DIR}.{data["gamename"]}')
        game = game_module.Game(data['players'], data['options'])
        game.deserialize(data['state'])

        result = game.make_move(move)

        data['state'] = game.serialize()
        save_game_state(game_id, data)

        return jsonify(result)
    except FileNotFoundError:
        return jsonify({'error': 'Game not found'}), 404

# This block ensures the development server runs only when the script is executed directly
# It will not run when imported into another script (like passenger_wsgi.py)
if __name__ == '__main__':
    # Run the Flask development server
    # debug=True is useful for development but should be False in production
    app.run(debug=True)
