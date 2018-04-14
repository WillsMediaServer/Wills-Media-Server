// Get Elements
var player = document.getElementById('player');
var timeline = document.getElementById('timeline');
var playButton = document.getElementById('play');
var loopButton = document.getElementById('loop');
var displayCurrentTime = document.getElementById('timeCurrent');
var displayTotalTime = document.getElementById('timeTotal');

var isPlaying = false;
var isLoop = false;
var length = 0;
var currentPosition = 0;

timeline.addEventListener("click", function(event) {
  timelineSeek(event);
});

playButton.addEventListener("click", function() {
  audioPlay();
});

loopButton.addEventListener("click", function() {
  audioLoop();
});

function audioPlayerPosition() {
  currentPosition = player.currentTime;
  length = player.duration;
  var timelineValue = (Math.round(currentPosition) / length);
  timeline.value = timelineValue;
  displayCurrentTime.innerHTML = prettyTime(Math.round(currentPosition));
  displayTotalTime.innerHTML = prettyTime(Math.round(length));
  if (player.ended) {
    if (isLoop){
      audioPlay();
    } else {
      playButton.innerHTML = "Play";
    }
  }
}

function timelineSeek(event) {
  var percent = event.offsetX / timeline.offsetWidth;
  var playerTime = Math.round(percent * length);
  var timelinePosition = Math.round(percent / 100);
  timeline.value = timelinePosition;
  player.currentTime = playerTime;
}

function audioPlay() {
  if (player.paused === false) {
    player.pause()
    isPlaying = false;
    playButton.innerHTML = "Play";
    playButton.setAttribute("title", "Play");
  } else {
    player.play()
    isPlaying = true;
    playButton.innerHTML = "Pause";
    playButton.setAttribute("title", "Pause");
  }
}

function audioLoop() {
  if (isLoop) {
    isLoop = false;
    loopButton.innerHTML = "Not Looping";
  } else {
    isLoop = true;
    loopButton.innerHTML = "Looping";
  }
}

function prettyTime(sec) {
  var hours = Math.floor(sec / 3600);
  var minutes = Math.floor((sec - (hours * 3600)) / 60);
  var seconds = Math.round((sec - (hours * 3600) - (minutes * 60)) * 100) / 100;

  var result = "";
  if (hours != 0) {
    result += (hours < 10 ? "0" + hours : hours) + ":";
  }

  result += (minutes < 10 ? "0" + minutes : minutes) + ":";
  result += (seconds  < 10 ? "0" + seconds : seconds);
  return result;
}
