
const output = document.getElementById("output");

async function api(method, url, body = null) {
	console.log('Request body:', body);
	url = getBackendUrl() + url;

	const options = {
		method,
		headers: {},
	};

	if (body) {
		options.headers['Content-Type'] = 'application/json';
		options.body = JSON.stringify(body);
	}

	const res = await fetch(url, options);

	let data;
	try {
		data = await res.json();
	} catch (e) {
		data = { error: 'Invalid JSON response or empty body', status: res.status };
	}

	output.textContent = JSON.stringify(data, null, 2);
	return data;
}

async function startGame() {
	const gamename = valf(document.getElementById("gamename").value,'setgame');
	const players = valf(JSON.parse(document.getElementById("players").value),['felix','amanda']);
	const options = valf(JSON.parse(document.getElementById("options").value),{});
	const data = await api("POST", "/start_game", { gamename, players, options });
	if (data.gameid) document.getElementById("gameid").value = data.gameid;
}

async function makeMove() {
	const id = document.getElementById("gameid").value;
	const move = JSON.parse(document.getElementById("move").value);
	await api("POST", `/make_move/${id}`, { move });
}

async function getGameState() {
	const id = document.getElementById("gameid").value;
	await api("GET", `/game_state/${id}`);
}

async function saveGame() {
	const id = document.getElementById("gameid").value;
	const state = await api("GET", `/game_state/${id}`);
	await api("POST", `/save_game/${id}`, state);
}

async function loadGame() {
	const id = document.getElementById("gameid").value;
	await api("GET", `/load_game/${id}`);
}

async function deleteGame() {
	const id = document.getElementById("gameid").value;
	await api("DELETE", `/delete_game/${id}`);
}

