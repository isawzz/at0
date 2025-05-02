
onload = start; VERBOSE=true;
function start() { test0(); }

async function test0() {
	getBackendUrl(); console.log(DA)

	//document.getElementById('fetch-state-button').addEventListener('click', fetchAndDisplayGameState);
	document.title = stringBetween(window.location.href,'//','/');/// DA.sessionType; //getBackendUrl() + DA.sessionType == 'live'?'(live)':'';

}




