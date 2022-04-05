window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI.
    // Open the WebSocket connection and register event handlers.
    const websocket = new WebSocket("ws://localhost:8001/");
    // receiveText(websocket);
    websocket.onmessage = function (event) {
        console.log(event.data);
      }
    
  });

  async function receiveText(websocket) {
    message = await websocket.

    console.log(message)
  }