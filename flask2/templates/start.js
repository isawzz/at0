onload = start;

function start(){ test0(); }

async function test0(){
	initSockets();
	fetchGamesList();

	// Button event listeners
	document.getElementById("startGameBtn").onclick = startSelectedGame;
	document.getElementById("makeMoveBtn").onclick = makeSelectedMove;
	document.getElementById("fetchStateBtn").onclick = fetchGameState;
	document.getElementById("sendChatBtn").onclick = sendChat;
}

// === Game Actions ===
function startGame(gameName, players = ["Player1"], options = {}) {
	DA.socket.emit("start_game", {
		gamename: gameName,
		players: players,
		options: options
	});
}

function makeMove(gameId, move) {
	DA.socket.emit("make_move", {
		gameid: gameId,
		move: move
	});
}

function getGameState(gameId) {
	DA.socket.emit("get_state", {
		gameid: gameId
	});
}

function fetchGamesList() {
	DA.socket.emit("games_list");
}

// === UI Handlers ===
function startSelectedGame() {
	const game = document.getElementById("gameSelect").value;
	startGame(game, ["Alice", "Bob"]);
}

function makeSelectedMove() {
	const gameId = document.getElementById("gameIdInput").value;
	let moveText = document.getElementById("moveInput").value;
	try {
		const move = JSON.parse(moveText);
		makeMove(gameId, move);
	} catch (err) {
		alert("Invalid move JSON");
	}
}

function fetchGameState() {
	const gameId = document.getElementById("stateGameId").value;
	getGameState(gameId);
}

function sendChat() {
	const input = document.getElementById("chatInput");
	const msg = input.value.trim();
	if (msg) {
		DA.socket.emit("chat_message", msg);
		input.value = "";
	}
}


// === Utility ===
function updateGameState(state) {
	document.getElementById("gameState").textContent = JSON.stringify(state, null, 2);
}
