onload = start;

function start(){ test0(); }

async function test0(){
	const username = prompt("Enter your username:") || "Guest";
	DA.username = username;
	initSockets(username);
	fetchGamesList();

	// Button event listeners
	document.getElementById("startGameBtn").onclick = startSelectedGame;
	document.getElementById("makeMoveBtn").onclick = makeSelectedMove;
	document.getElementById("fetchStateBtn").onclick = fetchGameState;
	document.getElementById("sendChatBtn").onclick = sendChat;
}

