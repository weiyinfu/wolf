function rewriteUrl(url) {
    const appName = "/Wolf/"
    if (url.startsWith("/api/") && location.pathname.startsWith(appName)) {
        url = `${appName}${url.slice(1)}`
    }
    return url;
}
function get(url,...args) {
    return axios.get(rewriteUrl(url), ...args)
}
function post(url,...args) {
    return axios.post(rewriteUrl(url), ...args)
}
function createRoom(game) {
    return post('/api/create_room', {
        game,
    })
}

function fetch(room) {
    return get('/api/fetch', {
        params: {
            room,
        }
    })
}

function newGame(room) {
    return get("/api/newgame", {
        params: {
            room,
        }
    })
}