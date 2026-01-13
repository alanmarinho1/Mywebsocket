# API Documentation

This document describes the REST API and WebSocket interface for the Bradesco PDF to Excel converter.

## Table of Contents

1. [Base URL](#base-url)
2. [REST API Endpoints](#rest-api-endpoints)
3. [WebSocket API](#websocket-api)
4. [Error Handling](#error-handling)
5. [Examples](#examples)

---

## Base URL

### Development
```
http://localhost:8000
```

### Production
Replace with your deployed domain:
```
https://your-domain.com
```

---

## REST API Endpoints

### 1. Get Upload Interface

Serves the HTML upload page.

**Endpoint**: `GET /`

**Description**: Returns the web interface for uploading PDF files.

**Request**:
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response**:
- **Status**: 200 OK
- **Content-Type**: text/html; charset=utf-8
- **Body**: HTML page with upload form

**Example**:
```bash
curl http://localhost:8000/
```

---

### 2. Upload and Convert PDF

Converts a Bradesco bank statement PDF to Excel format.

**Endpoint**: `POST /`

**Description**: Accepts a PDF file, converts it to Excel, and returns the Excel file.

**Request**:

```http
POST / HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data; boundary=----FormBoundary
Content-Length: [file_size]

------FormBoundary
Content-Disposition: form-data; name="file"; filename="statement.pdf"
Content-Type: application/pdf

[PDF binary data]
------FormBoundary--
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | Bradesco bank statement PDF file |

**Response (Success)**:
- **Status**: 200 OK
- **Content-Type**: application/xlsx
- **Content-Disposition**: attachment; filename={original_name}.xlsx
- **Body**: Excel file binary data

**Response (Error)**:
- **Status**: 400 Bad Request
- **Content-Type**: application/json
- **Body**:
```json
{
  "detail": "O arquivo statement.pdf não é PDF"
}
```

**Example (cURL)**:
```bash
curl -X POST http://localhost:8000/ \
  -F "file=@statement.pdf" \
  -o converted.xlsx
```

**Example (Python)**:
```python
import requests

url = "http://localhost:8000/"
files = {'file': open('statement.pdf', 'rb')}
response = requests.post(url, files=files)

if response.status_code == 200:
    with open('converted.xlsx', 'wb') as f:
        f.write(response.content)
```

**Example (JavaScript/Fetch)**:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'converted.xlsx';
    a.click();
});
```

---

## WebSocket API

### Connection

Provides real-time progress updates during PDF conversion.

**Endpoint**: `ws://localhost:8001/`

**Protocol**: WebSocket

**Description**: Connects to the WebSocket server to receive page-by-page processing updates.

### Connection Flow

```
Client                          Server
  |                               |
  |-------- Connect ------------->|
  |<------- Accept ---------------|
  |                               |
  |                         [Processing starts]
  |                               |
  |<------ Message: "1" ----------|  (Page 1)
  |<------ Message: "2" ----------|  (Page 2)
  |<------ Message: "3" ----------|  (Page 3)
  |           ...                 |
  |<------ Message: "N" ----------|  (Page N)
  |                               |
  |                         [Processing complete]
  |<------- Close ----------------|
```

### Messages

**Direction**: Server → Client

**Format**: Plain text string

**Content**: Current page number being processed

**Examples**:
- `"1"` - Processing page 1
- `"2"` - Processing page 2
- `"15"` - Processing page 15

### Client Implementation

**JavaScript/Browser**:
```javascript
const socket = new WebSocket('ws://localhost:8001/');

socket.onopen = (event) => {
    console.log('Connected to WebSocket server');
};

socket.onmessage = (event) => {
    const pageNumber = event.data;
    console.log(`Processing page ${pageNumber}`);
    // Update UI progress bar
    updateProgressBar(pageNumber);
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};

socket.onclose = (event) => {
    console.log('Connection closed');
};
```

**Python**:
```python
import asyncio
import websockets

async def receive_updates():
    uri = "ws://localhost:8001/"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                print(f"Processing page: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

asyncio.run(receive_updates())
```

**Node.js**:
```javascript
const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8001/');

ws.on('open', () => {
    console.log('Connected to WebSocket server');
});

ws.on('message', (data) => {
    console.log(`Processing page: ${data}`);
});

ws.on('close', () => {
    console.log('Connection closed');
});

ws.on('error', (error) => {
    console.error('WebSocket error:', error);
});
```

---

## Error Handling

### HTTP Error Codes

| Status Code | Description | Common Cause |
|-------------|-------------|--------------|
| 200 | Success | File converted successfully |
| 400 | Bad Request | Invalid PDF or file format |
| 422 | Unprocessable Entity | Missing file parameter |
| 500 | Internal Server Error | Server error during processing |

### Error Response Format

```json
{
  "detail": "Error description in Portuguese or English"
}
```

### Common Errors

#### 1. Missing File Parameter

**Request**:
```bash
curl -X POST http://localhost:8000/
```

**Response**:
```json
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 2. Invalid PDF File

**Response**:
```json
{
  "detail": "O arquivo invalid_file.txt não é PDF"
}
```

#### 3. Processing Error

**Response**:
```json
{
  "detail": "Error processing PDF: [specific error message]"
}
```

### WebSocket Errors

**Connection Refused**:
```
Error: WebSocket connection failed: Connection refused
```
- **Cause**: WebSocket server not running
- **Solution**: Start `convert.py` server

**Connection Closed**:
```
ConnectionClosedOK
```
- **Cause**: Normal closure after processing
- **Action**: No action needed, expected behavior

---

## Examples

### Complete Workflow Example (Python)

```python
import requests
import asyncio
import websockets
import threading

def upload_file(filename):
    """Upload PDF and download Excel"""
    url = "http://localhost:8000/"
    
    print(f"Uploading {filename}...")
    with open(filename, 'rb') as f:
        response = requests.post(url, files={'file': f})
    
    if response.status_code == 200:
        output_filename = filename.replace('.pdf', '.xlsx')
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        print(f"Saved to {output_filename}")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return False

async def monitor_progress():
    """Monitor conversion progress via WebSocket"""
    uri = "ws://localhost:8001/"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Monitoring progress...")
            while True:
                message = await websocket.recv()
                print(f"📄 Processing page {message}")
    except websockets.exceptions.ConnectionClosed:
        print("✓ Processing complete")

def run_async_monitor():
    """Run async monitor in separate thread"""
    asyncio.run(monitor_progress())

# Example usage
if __name__ == "__main__":
    # Start monitoring in background
    monitor_thread = threading.Thread(target=run_async_monitor)
    monitor_thread.start()
    
    # Upload file
    success = upload_file("statement.pdf")
    
    # Wait for monitoring to complete
    monitor_thread.join()
    
    if success:
        print("✓ Conversion successful!")
```

### Batch Processing Example

```python
import requests
import os
from pathlib import Path

def batch_convert(input_dir, output_dir):
    """Convert all PDFs in a directory"""
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Find all PDF files
    pdf_files = list(Path(input_dir).glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        
        # Upload and convert
        with open(pdf_file, 'rb') as f:
            response = requests.post(
                'http://localhost:8000/',
                files={'file': f}
            )
        
        if response.status_code == 200:
            # Save Excel file
            output_file = Path(output_dir) / pdf_file.name.replace('.pdf', '.xlsx')
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"✓ Saved: {output_file.name}")
        else:
            print(f"✗ Failed: {response.status_code}")

# Usage
batch_convert("./pdfs", "./excel_outputs")
```

### Web Application Integration (JavaScript)

```javascript
// Complete upload with progress tracking

class PDFConverter {
    constructor() {
        this.apiUrl = 'http://localhost:8000/';
        this.wsUrl = 'ws://localhost:8001/';
        this.websocket = null;
    }

    async convert(file, onProgress, onComplete, onError) {
        // Connect to WebSocket for progress
        this.websocket = new WebSocket(this.wsUrl);
        
        this.websocket.onmessage = (event) => {
            if (onProgress) {
                onProgress(parseInt(event.data));
            }
        };

        this.websocket.onclose = () => {
            console.log('WebSocket closed');
        };

        // Upload file via HTTP
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                if (onComplete) {
                    onComplete(blob);
                }
                this.websocket.close();
            } else {
                const error = await response.json();
                if (onError) {
                    onError(error);
                }
            }
        } catch (error) {
            if (onError) {
                onError(error);
            }
        }
    }

    downloadBlob(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
}

// Usage
const converter = new PDFConverter();
const fileInput = document.getElementById('file-input');

fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    
    converter.convert(
        file,
        // Progress callback
        (pageNumber) => {
            console.log(`Processing page ${pageNumber}`);
            updateProgressBar(pageNumber);
        },
        // Complete callback
        (blob) => {
            console.log('Conversion complete!');
            converter.downloadBlob(blob, file.name.replace('.pdf', '.xlsx'));
        },
        // Error callback
        (error) => {
            console.error('Conversion failed:', error);
            alert('Error converting file');
        }
    );
});
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider:

- Implementing rate limiting middleware
- Adding authentication tokens
- Setting maximum file size limits
- Queue system for concurrent requests

---

## Security Considerations

### Current Implementation

- No authentication required
- No input validation beyond file type
- Temporary files stored on server disk
- No encryption of uploaded files

### Recommendations for Production

1. **Add Authentication**: Implement API keys or OAuth
2. **Validate Input**: Check file size and content
3. **Secure Storage**: Encrypt temporary files
4. **HTTPS**: Use SSL/TLS certificates
5. **Rate Limiting**: Prevent abuse
6. **Logging**: Track all API calls
7. **CORS**: Configure appropriate CORS headers

---

## Versioning

Current version: 1.0 (implicit)

Future versions should include version in URL:
```
/api/v1/convert
/api/v2/convert
```

---

## Support

For API questions or issues:
- Check [README.md](README.md) for general documentation
- See [TECHNICAL.md](TECHNICAL.md) for implementation details
- Open an issue on GitHub with API-specific questions
