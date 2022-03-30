
window.addEventListener("DOMContentLoaded", () => {

  // Open the WebSocket connection and register event handlers.
  const websocket = new WebSocket("ws://localhost:8001/");
  // receiveFile(websocket)
  // handleFileSelect(websocket);
});


var reader;
var progress = document.querySelector('.percent');

function SendFile() {
    // reader.abort();
    // alert("Xablau")
}

function errorHandler(evt) {
    switch(evt.target.error.code) {
    case evt.target.error.NOT_FOUND_ERR:
        alert('File Not Found!');
        break;
    case evt.target.error.NOT_READABLE_ERR:
        alert('File is not readable');
        break;
    case evt.target.error.ABORT_ERR:
        break; // noop
    default:
        alert('An error occurred reading this file.');
    };
}

function updateProgress(evt, websocket) {
    // evt is an ProgressEvent.
    if (evt.lengthComputable) {
    var percentLoaded = Math.round((evt.loaded / evt.total) * 100);
    // Increase the progress bar length.
    if (percentLoaded < 100) {
        progress.style.width = percentLoaded + '%';
        progress.textContent = percentLoaded + '%';
    }
    }
}

function handleFileSelect(evt, websocket) {
    // Reset progress indicator on new file selection.
    progress.style.width = '0%';
    progress.textContent = '0%';

    reader = new FileReader();
    reader.onerror = errorHandler;
    reader.onprogress = updateProgress;

    reader.onloadstart = function(e) {
    document.getElementById('progress_bar').className = 'loading';
    };
    reader.onload = function(e) {
    // Ensure that the progress bar displays 100% at the end.
    progress.style.width = '100%';
    progress.textContent = '100%';
    }
    websocket.send("xablau")
    // Read in the image file as a binary string.
    // websocket.send(reader.readAsBinaryString(evt.target.files[0]));
    // console.log(reader.)
    // console.log(reader.readAsBinaryString(evt.target.files[0]));
}

document.getElementById('files').addEventListener('change', handleFileSelect, false);