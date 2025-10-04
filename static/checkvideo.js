const scriptTag = document.currentScript;
const url = scriptTag.getAttribute("src");
const video_ids = url.split("video_ids=")[1].split(",");

window.onYouTubeIframeAPIReady = function() {
    for(const id of video_ids){
        new YT.Player(id, {
            events: {
                'onReady': (event) => onPlayerReady(id, event)
            }
        });
    }
};

function onPlayerReady(id, event) {
    const state = event.target.getPlayerState();
    updateStatus(id, state);
}

function updateStatus(id, state) {
    const stateMap = {
        '-1': 'unstarted',
        '0': 'ended',
        '1': 'playing',
        '2': 'paused',
        '3': 'buffering',
        '5': 'video cued'
    };
    const stateName = stateMap[state] || state;
    if (stateName == "unstarted") {
        document.querySelector(`#${id}`).remove();
    }
}

