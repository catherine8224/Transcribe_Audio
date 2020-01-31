// set up basic variables for app

const record = document.querySelector('.record');
//const pause = document.querySelector('.pause');
//const pauseButton = document.getElementById("pauseButton")
const pauseButton = document.querySelector(".pause")
const stop = document.querySelector('.stop');
const soundClips = document.querySelector('.sound-clips');
const canvas = document.querySelector('.visualizer');
const mainSection = document.querySelector('.main-controls');
var rec;

const upload = document.querySelector('.upload');
var mediaRecorder = null;
var source = null;
var ignoreAutoPlay = false;

//pauseButton.addEventListener("click", pauseRecording);

// disable stop button while not recording
//disable upload button while not recording
//disable pause button while not recording
stop.disabled = true;
upload.disabled = false;
pauseButton.disabled = true; 

// visualiser setup - create web audio api context and canvas

let audioCtx;
const canvasCtx = canvas.getContext("2d");

//main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.');
  let constraints = { audio: true }; //ask for permission to access microphone
  let chunks = [];

  /*let onSuccess = function(stream) {
    mediaRecorder = new MediaRecorder(stream);
    mediaStreamSource = audioCtx.createMediaStreamSource(stream);
    record.onclick = function() {
      visualize(stream);

      // Display a countdown before recording starts.
      var progress = document.querySelector('.progress-display');
      progress.innerText = "3";
      document.querySelector('.info-display').innerText = "";
      setTimeout(function() {
        progress.innerText = "2";
	    setTimeout(function() {
	      progress.innerText = "1";
	      setTimeout(function() {
		  progress.innerText = "";
		  startRecording();
	      }, 1000);
	  }, 1000);
      }, 1000);
      stop.disabled = false;
      record.disabled = true;
    }*/

  // Create a MediaStreamAudioSourceNode
  // Feed the HTMLMediaElement into it
  let onSuccess = function(stream) {
    const mediaRecorder = new MediaRecorder(stream);
    var audioCtx = new AudioContext();
    mediaStreamSource = audioCtx.createMediaStreamSource(stream);
    visualize(stream);

    record.onclick = function() {
      mediaRecorder.start();
      console.log(mediaRecorder.state);
      console.log("recorder started");
      record.style.background = "red";
      stop.disabled = false;
      record.disabled = true;
      pauseButton.disabled= false;
    } 

    //pauses the recording
    pauseButton.onclick = function() {
      if(mediaRecorder.state === "recording") {
        mediaRecorder.pause();
        stop.disabled = false;
        record.disabled = false;
        pauseButton.disabled= false;
        // recording paused
      } else if(mediaRecorder.state === "paused") {
        mediaRecorder.resume();
        stop.disabled = false;
        record.disabled = true;
        pauseButton.disabled= false;
        // resume recording
      }
    }
  
    mediaRecorder.onpause = function() {
      // do something in response to
      // recording being paused
      pauseButton.innerHTML = 'Resume'
    }
  
    mediaRecorder.onresume = function() {
      // do something in response to
      // recording being resumed
      pauseButton.innerHTML = 'Pause'
    }

    stop.onclick = function() {
      mediaRecorder.stop();
      console.log(mediaRecorder.state);
      console.log("recorder stopped");
      record.style.background = "";
      record.style.color = "";
      // mediaRecorder.requestData();
      stop.disabled = true;
      record.disabled = false;
      pauseButton.disabled= false;  
      upload.disabled=false; 
      promptToSave();
    }

    upload.onclick = function() {
      saveRecordings();
    }
  
    mediaRecorder.onstop = function(e) {
      console.log("data available after MediaRecorder.stop() called.");

      const clipName = prompt('Enter a name for your sound clip?','My unnamed clip');
      console.log(clipName);
      const clipContainer = document.createElement('article'); //<article class="clip">
      const clipLabel = document.createElement('p'); //<p>My unnamed clip</p>
      const audio = document.createElement('audio'); //<audio controls src="a;slkf;asf"></audio>
      const link = document.createElement('a');
      const deleteButton = document.createElement('button');

      clipContainer.classList.add('clip'); //<article class="clip">
      audio.setAttribute('controls', '');//<audio controls...>
      deleteButton.textContent = 'Delete';
      deleteButton.className = 'delete';

      //clipLabel.onclick = function() {
        //const existingName = clipLabel.textContent;
        //const newClipName = prompt('Enter a new name for your sound clip?');
      if(clipName === null) {
        clipLabel.textContent = 'My unnamed clip';
      } else {
        clipLabel.textContent = clipName;
      }
     
      /*fileNumber=0;
      if(clipName === null) {
        allClips = document.querySelectorAll('.clip');
        clipLabel.textContent = 'Unnamedclip_' + fileNumber;
        //allClips.length
        if(clipLabel.textContent.exists()) {
          clipLabel.textContent = 'Unnamedclip_' + (fileNumber++);
        }

      } else {
        clipLabel.textContent = clipName;
      }*/

      clipContainer.appendChild(audio);
      clipContainer.appendChild(clipLabel);
      clipContainer.appendChild(deleteButton);
      clipContainer.appendChild(link)
      soundClips.appendChild(clipContainer);

      audio.controls = true;
      const blob = new Blob(chunks, { 'type' : 'audio/ogg; codecs=opus' });
      chunks = [];
      const audioURL = window.URL.createObjectURL(blob);
      audio.src = audioURL;
      link.href = audioURL;
      link.download = clipName + ".mp3";
      link.innerHTML= "Save to disk";
      console.log("recorder stopped");

      deleteButton.onclick = function(e) {
        evtTgt = e.target;
        evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
      }

      clipLabel.onclick = function() {
        const existingName = clipLabel.textContent;
        const newClipName = prompt('Enter a new name for your sound clip?');
        if(newClipName === null) {
          clipLabel.textContent = existingName;
        } else {
          clipLabel.textContent = newClipName;
        }
      }
    }

    mediaRecorder.ondataavailable = function(e) {
      chunks.push(e.data);
    }
  }

  let onError = function(err) {
    console.log('The following error occured: ' + err);
  }

  navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);

} else {
   console.log('getUserMedia not supported on your browser!');
}

function visualize(stream) {
  if(!audioCtx) {
    audioCtx = new AudioContext();
  }

  const source = audioCtx.createMediaStreamSource(stream);

  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 2048;
  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  source.connect(analyser);
  //analyser.connect(audioCtx.destination);

  draw()

  function draw() {
    WIDTH = canvas.width
    HEIGHT = canvas.height;

    requestAnimationFrame(draw);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(200, 200, 200)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

    canvasCtx.beginPath();

    let sliceWidth = WIDTH * 1.0 / bufferLength;
    let x = 0;


    for(let i = 0; i < bufferLength; i++) {

      let v = dataArray[i] / 128.0;
      let y = v * HEIGHT/2;

      if(i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height/2);
    canvasCtx.stroke();

  }
}

window.onresize = function() {
  canvas.width = mainSection.offsetWidth;
}

window.onresize();

function promptToSave() {
  if (confirm('Are you ready to upload your words?\nIf not, press cancel now,' + 
	      ' and then press Upload once you are ready.')) {
    saveRecordings();
  }
  upload.disabled = false;
}

var allClips;
var clipIndex;

/*var encodingTypeSelect = document.getElementById("encodingTypeSelect");*/

/* LOOK AT THIS TOMORROW 
recorder.setOptions({
  timeLimit: 120,
  encodeAfterRecord: encodeAfterRecord,
  ogg: {
      quality: 0.5
  },
  mp3: {
      bitRate: 160
  }
}); */

function saveRecordings() {
  mediaStreamSource.disconnect();
  allClips = document.querySelectorAll('.clip');
  console.log('allClips: ', allClips)
  clipIndex=0;
  uploadNextClip();
}

function uploadNextClip() {
  document.querySelector('.progress-display').innerText = 'Uploading clip ' + clipIndex; //+ '/' + unrollWordCounts(getAllWantedWords()).length;
  let clip = allClips[clipIndex];
  clip.style.display = 'None';
  var audioBlobUrl = clip.querySelector('audio').src;
  var word = clip.querySelector('p').innerText;
  var xhr = new XMLHttpRequest();
  xhr.open('GET', audioBlobUrl, true);
  xhr.responseType = 'blob';
  xhr.onload = function(e) {
    if (this.status == 200) {
      var blob = this.response;
      var ajaxRequest = new XMLHttpRequest();
      var uploadUrl = '/record_form?word=' + word; //+ '&_csrf_token=' + csrf_token;
      ajaxRequest.open('POST', uploadUrl, true);
      ajaxRequest.setRequestHeader('Content-Type', 'application/json');    
      ajaxRequest.onreadystatechange = function() {
        if (ajaxRequest.readyState == 4) {
    if (ajaxRequest.status === 200) {
            clipIndex += 1;
            if (clipIndex < allClips.length) {
        uploadNextClip();
      } else {
        allDone();
      }
          } else {
            alert('Uploading failed with error code ' + ajaxRequest.status);
          }
  }
      };
      ajaxRequest.send(blob);
    }
  };
  xhr.send();
}

function allDone() {
  document.cookie = 'all_done=true; path=/';
  location.reload(true);
}

document.getElementById("timer").onclick = function() {revealMessage()};

function revealMessage() {
  document.getElementById("timer").style.display = 'block';
}

(function(){
  "use strict";
  var $start_button = document.getElementById("recordButton");
  var $stop_button = document.getElementById("stopButton");
  var $pause_button = document.getElementById("pauseButton");
  var $timer = document.getElementById("timer");
  var second = 0;
  function zf(x) { return (x > 9 ? "" : "0") + x; }

  function updateSecond(x) {
    second = x;
    $timer.textContent = zf(second / 60 | 0) + ":" + zf(second % 60);
  }

  function nextSecond() {
    updateSecond(second + 1);
  }
  var timer_handle = -1;
  $start_button.addEventListener("click", function(ev) {
    timer_handle = setInterval(nextSecond, 1000);
  }, false);
  $stop_button.addEventListener("click", function(ev) {
    if (timer_handle != -1) {
      clearInterval(timer_handle);
      timer_handle = -1;
      updateSecond(0);
    }
  }, false);
  $pause_button.addEventListener("click", function(ev) {
    if (timer_handle != -1) {
    clearInterval(timer_handle);
    timer_handle = -1;
  }
  else {
    timer_handle = setInterval(nextSecond, 1000);
  }
}, false);
})();
