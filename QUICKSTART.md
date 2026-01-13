# Quick Start Guide

Get up and running with the Bradesco PDF to Excel converter in 5 minutes.

## Prerequisites

- Python 3.7 or higher
- Java Runtime Environment (JRE)
- Git (for cloning)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/alanmarinho1/Mywebsocket.git
cd Mywebsocket
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues, try using a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Java Installation

```bash
java -version
```

Expected output should show Java version 8 or higher. If Java is not installed:
- **Windows/Mac**: Download from [java.com](https://www.java.com/)
- **Linux**: `sudo apt-get install default-jre` (Ubuntu/Debian)

### 4. Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5. Access the Application

Open your browser and go to:
```
http://localhost:8000
```

### 6. Convert Your First PDF

1. Click "Escolher arquivo" (Choose file)
2. Select a Bradesco bank statement PDF
3. Click "Converter" (Convert)
4. Wait for processing
5. The Excel file will automatically download

## Common Issues and Solutions

### "Java not found"

**Problem**: tabula-py can't find Java

**Solution**:
```bash
# Verify Java is in PATH
echo $JAVA_HOME  # Linux/Mac
echo %JAVA_HOME%  # Windows

# If empty, install Java and add to PATH
```

### "Module not found"

**Problem**: Missing Python package

**Solution**:
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### "Port already in use"

**Problem**: Port 8000 is occupied

**Solution**:
```bash
# Use a different port
uvicorn main:app --reload --port 8080
# Then access http://localhost:8080
```

### "File not processing"

**Problem**: PDF doesn't convert

**Solution**:
- Verify it's a Bradesco bank statement PDF
- Ensure PDF is not password-protected
- Check PDF is not corrupted
- Try with a different PDF file

## Using the API

### Command Line Upload

```bash
# Upload and convert a PDF
curl -X POST http://localhost:8000/ \
  -F "file=@/path/to/statement.pdf" \
  -o output.xlsx
```

### Python Script

```python
import requests

# Upload file
with open('statement.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/',
        files={'file': ('statement.pdf', f, 'application/pdf')}
    )

# Save Excel file
if response.status_code == 200:
    with open('converted.xlsx', 'wb') as output:
        output.write(response.content)
    print("Conversion successful!")
else:
    print(f"Error: {response.status_code}")
```

### JavaScript/Node.js

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('statement.pdf'));

axios.post('http://localhost:8000/', form, {
    headers: form.getHeaders(),
    responseType: 'arraybuffer'
})
.then(response => {
    fs.writeFileSync('converted.xlsx', response.data);
    console.log('Conversion successful!');
})
.catch(error => {
    console.error('Error:', error.message);
});
```

## Testing the WebSocket Server

### Start WebSocket Server

```bash
python convert.py
```

### Test with Python Client

```python
import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8001"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server")
            # Listen for messages
            while True:
                message = await websocket.recv()
                print(f"Received page: {message}")
    except KeyboardInterrupt:
        print("Disconnected")

asyncio.run(test_websocket())
```

### Test with Browser Console

1. Open browser console (F12)
2. Paste and run:

```javascript
const ws = new WebSocket('ws://localhost:8001');

ws.onopen = () => {
    console.log('Connected to WebSocket');
};

ws.onmessage = (event) => {
    console.log('Received:', event.data);
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};

ws.onclose = () => {
    console.log('Disconnected from WebSocket');
};
```

## Project Structure Overview

```
Mywebsocket/
├── main.py                 # FastAPI web server
├── convert.py              # PDF conversion + WebSocket
├── helpers.py              # Data processing functions
├── keyword_position.py     # PDF area detection
├── app.py                  # Simple WebSocket example
├── requirements.txt        # Python dependencies
├── README.md              # Main documentation
├── TECHNICAL.md           # Technical documentation
├── QUICKSTART.md          # This file
└── html/
    ├── index.html         # Upload interface
    ├── main.js            # WebSocket client
    └── estilo.css         # Styles
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [TECHNICAL.md](TECHNICAL.md) for architecture details
- Review the code to understand the conversion logic
- Customize for your needs

## Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Review the troubleshooting section above
3. Verify all dependencies are installed correctly
4. Ensure you're using a valid Bradesco PDF format
5. Open an issue on GitHub with error details

## Production Deployment

For production use:

```bash
# Install production server
pip install gunicorn

# Run with gunicorn (more stable than uvicorn --reload)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Consider:
- Setting up a reverse proxy (nginx/Apache)
- Adding HTTPS/SSL certificates
- Implementing authentication
- Adding rate limiting
- Setting up monitoring and logging
- Using environment variables for configuration

## Development Mode

For development with auto-reload:

```bash
# Auto-reload on file changes
uvicorn main:app --reload --log-level debug
```

## License and Contributing

See the main [README.md](README.md) for license information and contribution guidelines.
