
function initSockets() {
	let socket = DA.socket = io("http://localhost:5000");  // Adjust if needed
	// === Socket Event Listeners ===
	socket.on("chat_message", data => {
		console.log('got message',data)
		const chatBox = document.getElementById("chatBox");
		const div = document.createElement("div");
		div.textContent = data;
		chatBox.appendChild(div);
		chatBox.scrollTop = chatBox.scrollHeight;
	});

	socket.on("games_list", games => {
		const sel = document.getElementById("gameSelect");
		sel.innerHTML = "";
		console.log(games)
		games.forEach(g => {
			const opt = document.createElement("option");
			opt.value = g;
			opt.textContent = g;
			sel.appendChild(opt);
		});
		if (games.length > 0) {
			sel.value = arrLast(games);
		}
	});

	socket.on("game_started", data => {
		console.log("Game started:", data);
		document.getElementById("gameIdInput").value = data.gameid;
		document.getElementById("stateGameId").value = data.gameid;
		updateGameState(data.state);
	});

	socket.on("game_update", updateGameState);
	socket.on("state", updateGameState);

	socket.on("error", err => {
		console.error("Error:", err.message);
		alert("Server error: " + err.message);
	});

}
function stringBetween(sFull, sStart, sEnd) {
	return stringBefore(stringAfter(sFull, sStart), isdef(sEnd) ? sEnd : sStart);
}
function stringBetweenLast(sFull, sStart, sEnd) {
	let s1 = stringBeforeLast(sFull, isdef(sEnd) ? sEnd : sStart);
	return stringAfterLast(s1, sStart);
}


