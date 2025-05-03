window.onload = () => {
	const socket = io("http://localhost:5000");  // Adjust to your actual backend URL

	fetchGamesList();
};

function startSelectedGame() {
	const game = document.getElementById("gameSelect").value;
	startGame(game, ["Alice", "Bob"]);
}

function makeSelectedMove() {
	const gameId = document.getElementById("gameIdInput").value;
	console.log(document.getElementById("moveInput").value);
	let move = document.getElementById("moveInput").value;
	console.log('move',move);
	move = JSON.parse(move);
	console.log('move',move);
	makeMove(gameId, move);
}

function fetchGameState() {
	const gameId = document.getElementById("stateGameId").value;
	getGameState(gameId);
}

function sendChat() {
	const msg = document.getElementById("chatInput").value;
	if (msg.trim()) {
		socket.emit("chat_message", msg);
		document.getElementById("chatInput").value = "";
	}
}

// Display chat messages
socket.on("chat_message", data => {
	const chatBox = document.getElementById("chatBox");
	const div = document.createElement("div");
	div.textContent = data;
	chatBox.appendChild(div);
	chatBox.scrollTop = chatBox.scrollHeight;
});

// Update dropdown with game modules
socket.on("games_list", games => {
	const sel = document.getElementById("gameSelect");
	sel.innerHTML = "";
	games.forEach(g => {
		const opt = document.createElement("option");
		opt.value = g;
		opt.textContent = g;
		sel.appendChild(opt);
	});
});

socket.on("game_started", data => {
	console.log("Game started: " + data.gameid);
	document.getElementById("gameIdInput").value = data.gameid;
	document.getElementById("stateGameId").value = data.gameid;
});

socket.on("game_update", data => {
	document.getElementById("gameState").textContent = JSON.stringify(data, null, 2);
});

socket.on("state", data => {
	document.getElementById("gameState").textContent = JSON.stringify(data, null, 2);
});