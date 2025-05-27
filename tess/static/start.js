
onload = start;
function start() { test0(); }

async function test0() {
	document.getElementById('tess-form').addEventListener('submit', async function (e) {
		e.preventDefault();
		const u = document.getElementById('u-num').value;
		const v = document.getElementById('v-num').value;

		const response = await fetch(`http://localhost:5000/tessellate?u=${u}&v=${v}`);
		console.log(response)
		const svgText = await response.text();
		console.log(svgText)

		document.getElementById('svg2').innerHTML = svgText;
	});
	const svg = document.getElementById('svg');
	const svgDoc = svg.contentDocument;
	const gElement = svgDoc.querySelector('g');
	const centers = getPolygonCentersFromG(gElement);
	console.log(centers);
}

function getPolygonCentersFromG(gElement) {
	// If input is a string, parse it to a DOM element
	if (typeof gElement === 'string') {
		const parser = new DOMParser();
		const doc = parser.parseFromString(`<svg>${gElement}</svg>`, 'image/svg+xml');
		gElement = doc.querySelector('g');
	}

	const polygons = gElement.querySelectorAll('polygon');
	const centers = [];

	polygons.forEach(polygon => {
		const pointsStr = polygon.getAttribute('points').trim();
		// Parse points into array of {x, y}
		const points = pointsStr.split(/\s+/).map(pair => {
			const [x, y] = pair.split(',').map(Number);
			return { x, y };
		});

		// Calculate centroid
		let area = 0;
		let cx = 0;
		let cy = 0;
		for (let i = 0; i < points.length; i++) {
			const { x: x0, y: y0 } = points[i];
			const { x: x1, y: y1 } = points[(i + 1) % points.length];
			const cross = x0 * y1 - x1 * y0;
			area += cross;
			cx += (x0 + x1) * cross;
			cy += (y0 + y1) * cross;
		}
		area /= 2;
		cx /= (6 * area);
		cy /= (6 * area);

		centers.push({ x: cx, y: cy });
	});

	return centers;
}
