
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());
const server = http.createServer(app);
const io = new Server(server, {
	cors: {
		origin: "*",
		methods: ["GET", "POST"]
	}
});

// Serve index.html directly
app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, 'index.html'));
});

// Handle the socket namespace
const socketNamespace = io.of("/socket");

socketNamespace.on('connection', (socket) => {
	console.log('User connected to /socket');

	socket.on('chat message', (msg) => {
		console.log('message:', msg);
		socketNamespace.emit('chat message', msg);
	});

	socket.on('disconnect', () => {
		console.log('User disconnected');
	});
});

app.get('/routes', (req, res) => {
	const routes = [];

	app._router.stack.forEach((middleware) => {
		if (middleware.route) {
			// Direct route
			const path = middleware.route.path;
			const methods = Object.keys(middleware.route.methods).map(m => m.toUpperCase());
			routes.push({ path, methods });
		} else if (middleware.name === 'router' && middleware.handle.stack) {
			// Routes from a router (not needed here, but good practice)
			middleware.handle.stack.forEach((handler) => {
				if (handler.route) {
					const path = handler.route.path;
					const methods = Object.keys(handler.route.methods).map(m => m.toUpperCase());
					routes.push({ path, methods });
				}
			});
		}
	});

	res.json(routes);
});


const PORT = 3000;
server.listen(PORT, () => {
	console.log(`App listening on port ${PORT}`);
});
