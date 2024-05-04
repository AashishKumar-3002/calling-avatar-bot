var socket = io.connect(
  "http://" + window.location.hostname + ":" + location.port
);

var isTranscribing = false;

document.getElementById("record").addEventListener("change", function () {
  if (this.checked) {
    // Start transcription
    isTranscribing = true;
    socket.emit("toggle_transcription", { action: "start" });
  } else {
    // Stop transcription
    isTranscribing = false;
    socket.emit("toggle_transcription", { action: "stop" });
  }
});

socket.on("transcription_update", function (data) {
  document.getElementById("captions").innerHTML = data.transcription;
});

// Emit the 'start_steve_intro' event after 5 seconds of page load
setTimeout(function() {
  socket.emit("start_steve_intro");
}, 5000);

socket.on('audio_update', function(data) {
  // Add the 'glow' class to the audio-response div
  document.getElementById('audio-response').classList.add('glow');

  // Decode Base64 audio data
  var binaryString = window.atob(data.audio);
  var bytes = new Uint8Array(binaryString.length);
  for (var i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
  }

  // Create audio context and play the audio
  var audioContext = new (window.AudioContext || window.webkitAudioContext)();
  audioContext.decodeAudioData(bytes.buffer, function(buffer) {
      var audioBuffer = audioContext.createBufferSource();
      audioBuffer.buffer = buffer;
      audioBuffer.connect(audioContext.destination);
      audioBuffer.start(0);

      // Remove the 'glow' class after the audio finishes playing
      audioBuffer.onended = function() {
          document.getElementById('audio-response').classList.remove('glow');
      };
  });
});

document.addEventListener('DOMContentLoaded', function() {
  const countdownElement = document.getElementById('countdown');
  const startCountdownValue = countdownElement.textContent.trim();
  console.log('startCountdownValue:', startCountdownValue);

  // Function to start the timer
  function startTimer() {
      let seconds = 0;
      const timerElement = document.getElementById('countdown');

      // Update timer display every second
      const timerInterval = setInterval(() => {
          seconds++;
          timerElement.textContent = formatTime(seconds);
      }, 1000);

      // Clear the interval when the page is closed or navigated away
      window.addEventListener('beforeunload', function() {
          clearInterval(timerInterval);
      });
  }

  // Function to format time (hh:mm:ss)
  function formatTime(seconds) {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const remainingSeconds = seconds % 60;
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  }

  // Start the timer if startCountdownValue is 'true'
  if (startCountdownValue === 'Ringing...') {
    setTimeout(startTimer, 5000); 
  }
});

window.onload = function() {
  var audio = document.getElementById("myAudio");
  audio.play();

  setTimeout(function() {
    audio.pause();
    audio.currentTime = 0;
  }, 5000);  // Stop playing after 5 seconds
};

