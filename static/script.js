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

// // Example client-side code to decode and play audio
// socket.on('audio_update', function(data) {
//   // Decode Base64 audio data
//   var binaryString = window.atob(data.audio);
//   var bytes = new Uint8Array(binaryString.length);
//   for (var i = 0; i < binaryString.length; i++) {
//       bytes[i] = binaryString.charCodeAt(i);
//   }
  
//   // Create audio context and play the audio
//   var audioContext = new (window.AudioContext || window.webkitAudioContext)();
//   audioContext.decodeAudioData(bytes.buffer, function(buffer) {
//       var audioBuffer = audioContext.createBufferSource();
//       audioBuffer.buffer = buffer;
//       audioBuffer.connect(audioContext.destination);
//       audioBuffer.start(0);
//   });
// });

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

