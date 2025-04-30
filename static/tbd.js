
async function DAInit(TESTING = false) {
	document.addEventListener("visibilitychange", handleVisibilityChange);
	DA.pollInterval = 3000;
	DA.pollCounter = 0;
	getBackendUrl();
	DA.gamelist = ['setgame', 'button96']; //'accuse aristo bluff ferro fishgame fritz huti lacuna nations setgame sheriff spotit wise'; if (DA.TEST0) gamelist += ' a_game'; gamelist = toWords(gamelist);
	DA.funcs = { setgame: setgame(), button96: button96() }; //implemented games!
	for (const gname in DA.gamelist) {
		if (isdef(DA.funcs[gname])) continue;
		DA.funcs[gname] = defaultGameFunc();
	}
	DA.evList = [];
	await loadAssetsStatic();
	M.tables = await MPollTables();
	let elems = mLayoutTM('dPage'); mStyle('dMain', { overy: 'auto', fg: 'inherit' }); mCenterFlex('dMain');
	mLayoutTopTestExtraMessageTitle('dTop');
	let username = localStorage.getItem('username') ?? 'hans';
	if (TESTING) {
		let names = ['amanda', 'felix', 'lauren', 'mimi', 'gul'];
		let d = mBy('dTestRight'); mClass(d, 'button_container'); //mFlex(d);
		for (const name of names) { let b = mDom(d, {}, { tag: 'button', html: name, onclick: async (ev) => await switchToUser(name) }); }
		username = rChoose(names);
	}
	await showMenuButtons();
	if (TESTING) await showTestButtons();
}
async function DASaveState(state) {
	if (isdef(state)) DA.gameState = state;
	let res = await fetch(`${getBackendUrl()}/save_state.php`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(DA.gameState)
	});
	let data = await res.json();
	if (VERBOSE) if (VERBOSE) console.log('Game state saved:', data, DA.gameState);
	return data;
}
