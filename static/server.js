
function getBackendUrl(isScript = null) {
	if (nundef(DA.backendUrl)) {
		let loc = window.location.href;
		if (VERBOSE) console.log('href', loc);
		let sessionType = DA.sessionType =
			loc.includes('moxito.online/at0') ? 'at0' :
				loc.includes('moxito.online') ? 'fastcomet' :
					loc.includes('vidulus') ? 'vps' :
						loc.includes('telecave') ? 'telecave' : loc.includes('8080') ? 'php'
							: loc.includes(':40') ? 'nodejs'
								: loc.includes(':60') ? 'flask' : 'live';
		if (VERBOSE) console.log('sessionType', sessionType);
		let backendUrl = DA.backendUrl = sessionType == 'live' ? 'http://localhost:5000' : 'at0' ? 'https://moxito.online/at0' : 'fastcomet' ? 'https://moxito.online' : isScript || sessionType == 'php' ? 'http://localhost:8080/mox' : '..';
		if (VERBOSE) console.log('backendUrl', backendUrl);
	}
	return DA.backendUrl;
}


async function fetchAndDisplayGameState() {
	const gameInfoDiv = document.getElementById('game-info');
	const statusMessage = document.getElementById('status-message');
	const movesAreaDiv = document.getElementById('moves-area');

	movesAreaDiv.innerHTML = '';
	statusMessage.textContent = 'Fetching game state...';
	statusMessage.className = '';

	let url = `${getBackendUrl()}/game_state`; console.log('url', url);
	try {
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const gameState = await response.json();

		if (gameState.game_over) {
			statusMessage.classList.add('game-over-message');
			if (gameState.winner === 1) {
				statusMessage.textContent = 'Game Over! Player X wins!';
				statusMessage.classList.add('winner-message');
			} else if (gameState.winner === 2) {
				statusMessage.textContent = 'Game Over! Player O wins!';
				statusMessage.classList.add('winner-message');
			} else if (gameState.winner === 0) {
				statusMessage.textContent = 'Game Over! It\'s a Draw!';
				statusMessage.classList.add('draw-message');
			} else {
				statusMessage.textContent = 'Game Over!';
			}
			movesAreaDiv.innerHTML = '';

		} else {
			const currentPlayer = gameState.current_player === 1 ? 'X' : 'O';
			statusMessage.textContent = `Current Player: ${currentPlayer}`;

			const possibleMoves = gameState.possible_moves;

			if (possibleMoves.length > 0) {
				const movesList = document.createElement('ul');
				movesList.id = 'possible-moves-list';

				const movesTitle = document.createElement('h3');
				movesTitle.textContent = 'Possible Moves (Row, Col):';
				movesAreaDiv.appendChild(movesTitle);

				possibleMoves.forEach(move => {
					const listItem = document.createElement('li');
					listItem.textContent = `(${move[0]}, ${move[1]})`;
					listItem.addEventListener('click', () => {
						console.log(`User selected move: (${move[0]}, ${move[1]})`);
						alert(`You selected move: (${move[0]}, ${move[1]})`);
					});
					movesList.appendChild(listItem);
				});

				movesAreaDiv.appendChild(movesList);
			} else {
				movesAreaDiv.innerHTML = '<p>No possible moves available.</p>';
			}
		}
	} catch (error) {
		console.error('Error fetching game state:', error);
		statusMessage.textContent = `Error: Could not fetch game state. ${error.message}`;
		statusMessage.style.color = 'red';
		movesAreaDiv.innerHTML = '';
	}
}
async function sendMoveToServer(row, col) {
	let url = `${getBackendUrl()}/make_move`; console.log('url', url);
	try {
		const response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ row, col }),
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		// Re-fetch and update UI with the new game state
		await fetchAndDisplayGameState();
	} catch (error) {
		console.error('Error sending move:', error);
		alert(`Error: Could not send move. ${error.message}`);
	}
}

