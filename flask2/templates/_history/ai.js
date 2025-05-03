
// Start a new game
function startGame(gameName, players = ["Player1"], options = {}) {
	socket.emit("start_game", {
		gamename: gameName,
		players: players,
		options: options
	});
}

// Make a move in a game
function makeMove(gameId, move) {
	socket.emit("make_move", {
		gameid: gameId,
		move: move
	});
}

// Get current state of a game
function getGameState(gameId) {
	socket.emit("get_state", {
		gameid: gameId
	});
}

// Get list of available games (modules)
function fetchGamesList() {
	socket.emit("games_list");
}

// Event listeners
socket.on("game_started", data => {
	console.log("Game started:", data);
	// e.g. update UI with data.gameid and data.state
});

socket.on("game_update", data => {
	console.log("Game updated:", data);
	// e.g. update game board
});

socket.on("state", data => {
	console.log("Current game state:", data);
});

socket.on("games_list", games => {
	console.log("Available games:", games);
	// e.g. populate game dropdown
});

socket.on("error", err => {
	console.error("Error:", err.message);
});
