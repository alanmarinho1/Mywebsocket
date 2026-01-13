# Technical Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Data Flow](#data-flow)
3. [Module Descriptions](#module-descriptions)
4. [PDF Processing Algorithm](#pdf-processing-algorithm)
5. [WebSocket Implementation](#websocket-implementation)
6. [API Reference](#api-reference)

---

## Architecture Overview

This application follows a client-server architecture with two main components:

```
┌─────────────────┐         ┌──────────────────┐
│   Web Browser   │ ◄─────► │  FastAPI Server  │
│  (index.html)   │  HTTP   │   (main.py)      │
└─────────────────┘         └──────────────────┘
        │                            │
        │ WebSocket                  │ Function Call
        ▼                            ▼
┌─────────────────┐         ┌──────────────────┐
│  WebSocket      │         │  PDF Converter   │
│  Client (JS)    │ ◄─────► │  (convert.py)    │
└─────────────────┘  WS     └──────────────────┘
                                     │
                            ┌────────┴────────┐
                            ▼                 ▼
                    ┌──────────────┐  ┌──────────────┐
                    │   helpers.py │  │keyword_pos.py│
                    └──────────────┘  └──────────────┘
```

---

## Data Flow

### 1. File Upload Flow (HTTP)

```
User → [Select PDF] → [Submit Form] → FastAPI POST / endpoint
                                            │
                                            ▼
                                    Save file temporarily
                                            │
                                            ▼
                                    Call convert() function
                                            │
                                            ▼
                                    Process PDF pages
                                            │
                                            ▼
                                    Generate Excel (BytesIO)
                                            │
                                            ▼
                                    Delete temporary file
                                            │
                                            ▼
                                    Return Excel as download
```

### 2. WebSocket Progress Flow

```
convert.py starts processing → For each page:
                                    │
                                    ▼
                            Send page number via WebSocket
                                    │
                                    ▼
                            Browser receives update
                                    │
                                    ▼
                            Update progress bar (if implemented)
```

---

## Module Descriptions

### main.py - FastAPI Application

**Purpose**: HTTP server for file handling

**Key Components**:
- `app`: FastAPI instance
- `templates`: Jinja2 template renderer
- `home()`: GET endpoint serving the upload page
- `upload_file()`: POST endpoint handling PDF upload and conversion

**Dependencies**: FastAPI, Jinja2, convert module

**Workflow**:
1. Receives uploaded PDF file
2. Saves file to disk temporarily
3. Calls `convert()` function
4. Removes temporary file
5. Returns Excel file as streaming response

---

### convert.py - PDF Processing Core

**Purpose**: Main conversion logic with WebSocket support

**Key Functions**:

#### `convert(websocket)`
- **Parameters**: WebSocket connection object
- **Returns**: BytesIO object containing Excel file
- **Process**:
  1. Opens PDF file using PyPDF2
  2. Iterates through each page
  3. Sends progress updates via WebSocket
  4. Extracts text and identifies page type
  5. Determines extraction area based on page content
  6. Uses tabula to extract table data
  7. Processes and cleans data using helper functions
  8. Concatenates all pages into final DataFrame
  9. Exports to Excel in memory

#### `main()`
- Starts WebSocket server on port 8001
- Runs forever waiting for connections

#### `server()`
- Alternative server with SIGTERM handling for graceful shutdown

---

### helpers.py - Data Processing Functions

**Purpose**: DataFrame cleaning and formatting

#### `df_ajust_first_page(df, listadrop, empresa, ag, conta)`

Processes the first page of the statement:
- Renames columns if needed
- Extracts transaction dates from combined text
- Handles multi-line transactions
- Adds company, agency, and account columns
- Identifies incomplete last row

**Parameters**:
- `df`: pandas DataFrame from tabula
- `listadrop`: List to track rows to delete
- `empresa`: Company name
- `ag`: Agency number
- `conta`: Account number

**Returns**: Tuple (processed DataFrame, boolean indicating incomplete last row)

#### `df_ajust_pages(df, listadrop, lastrow)`

Processes subsequent pages:
- Handles different column configurations
- Standardizes column names
- Manages page continuation (from incomplete previous page)
- Consolidates multi-line transactions
- Removes "SALDO ANTERIOR" (previous balance) rows

**Parameters**:
- `df`: pandas DataFrame from tabula
- `listadrop`: List to track rows to delete
- `lastrow`: Boolean indicating if previous page ended incomplete

**Returns**: Tuple (processed DataFrame, boolean indicating incomplete last row)

#### `last_df_ajust(df, listadrop)`

Final cleanup of complete DataFrame:
- Consolidates remaining multi-line transactions
- Propagates date, company, agency, and account information
- Removes "Total" rows
- Resets index

**Parameters**:
- `df`: Complete concatenated DataFrame
- `listadrop`: List to track rows to delete

**Returns**: Cleaned and formatted DataFrame

---

### keyword_position.py - Area Detection

**Purpose**: Dynamically calculate PDF extraction areas based on text positions

#### `keyword_first_page(file, x)`

Calculates extraction area for first page:
- Searches for "Os dados acima" (data disclaimer)
- Searches for "Data" (date column header)
- Returns coordinates for tabula area parameter

**Returns**: Tuple (top, left, bottom, right) in points

#### `keyword_last_page(file, x)`

Calculates extraction area for last page:
- Searches for "Total" keyword
- Returns coordinates excluding summary sections

**Returns**: Tuple (top, left, bottom, right) in points

---

## PDF Processing Algorithm

### Page Classification

The algorithm classifies each page into one of several types:

1. **First Page** (`Folha 1/`)
   - Contains account metadata (empresa, agencia, conta)
   - May have special footer text
   - Uses dynamic or static area extraction

2. **Empty/Summary Page**
   - Contains only disclaimers or "no transactions" message
   - Skipped during processing

3. **Last Page with Total**
   - Contains "Total" and transaction data
   - Uses `keyword_last_page()` for area detection

4. **Regular Transaction Page**
   - Contains only transaction data
   - Uses static area coordinates

### Multi-line Transaction Handling

Bank statements often split transaction descriptions across multiple rows. The algorithm detects this by:

1. Checking if a row has a balance value but the adjacent rows don't
2. Concatenating text from adjacent rows into single transaction
3. Marking adjacent rows for deletion
4. Maintaining proper data alignment

### Date Propagation

Transaction dates may not repeat for every transaction. The algorithm:
1. Detects when a date exists
2. Propagates it forward to subsequent transactions
3. Stops when a new date is encountered

---

## WebSocket Implementation

### Server Side (convert.py)

```python
async def convert(websocket):
    # ... initialization ...
    for x in range(1, xreader.numPages + 1):
        # ... processing ...
        while True:
            try:
                await websocket.send(str(x))  # Send page number
                break
            except websockets.ConnectionClosedOK:
                break
```

The server:
- Accepts WebSocket connections
- Sends page numbers as strings
- Handles connection closures gracefully

### Client Side (index.html)

Currently commented out in the HTML, but the structure is:

```javascript
const websocket = new WebSocket("ws://localhost:8001/");
// Handle incoming messages to update progress bar
```

---

## API Reference

### FastAPI Endpoints

#### GET /

**Description**: Serves the web upload interface

**Response**:
- Content-Type: `text/html`
- Body: Rendered index.html template

**Example**:
```bash
curl http://localhost:8000/
```

---

#### POST /

**Description**: Uploads PDF and returns converted Excel file

**Request**:
- Method: POST
- Content-Type: `multipart/form-data`
- Body Parameter: `file` (PDF file)

**Response**:
- Content-Type: `application/xlsx`
- Content-Disposition: `attachment; filename={original_name}.xlsx`
- Body: Excel file binary

**Error Response**:
- Status: 400
- Detail: "O arquivo {filename} não é PDF"

**Example**:
```bash
curl -X POST http://localhost:8000/ \
  -F "file=@statement.pdf" \
  -o output.xlsx
```

---

### WebSocket Protocol

#### Connection

**URL**: `ws://localhost:8001/`

**Protocol**: WebSocket

#### Messages

**Direction**: Server → Client

**Format**: Plain text string representing page number

**Example Messages**:
- `"1"` - Processing page 1
- `"2"` - Processing page 2
- `"3"` - Processing page 3

**Connection Lifecycle**:
1. Client connects
2. Server begins processing
3. Server sends page updates
4. Processing completes
5. Connection closes

---

## Development Notes

### Adding Support for New Bank Formats

To adapt this for other banks:

1. **Analyze PDF Structure**: 
   - Use PyMuPDF to examine text layout
   - Identify table areas and keywords

2. **Update Extraction Areas**:
   - Modify area coordinates in `convert.py`
   - Update keyword detection in `keyword_position.py`

3. **Adjust Column Mapping**:
   - Update column names in `helpers.py`
   - Modify regex patterns for data extraction

4. **Test Thoroughly**:
   - Test with multiple statement formats
   - Validate all data types (dates, amounts, etc.)

### Performance Considerations

- **Memory Usage**: Large PDFs are processed entirely in memory
- **Processing Time**: Proportional to number of pages (≈1-2 seconds per page)
- **Concurrent Requests**: FastAPI supports async, but file I/O is synchronous
- **WebSocket Overhead**: Minimal, only sends page numbers

### Known Limitations

1. **Single Format**: Only supports Bradesco bank statement format
2. **No Authentication**: No user authentication or file encryption
3. **Temporary Files**: Uploaded files briefly stored on disk
4. **Error Handling**: Limited validation of PDF content
5. **No Persistence**: No database or file storage

---

## Testing

### Manual Testing Steps

1. **Start the server**:
```bash
uvicorn main:app --reload
```

2. **Access interface**: http://localhost:8000

3. **Upload test PDF**: Use a sample Bradesco statement

4. **Verify output**: 
   - Check Excel file downloads
   - Verify data accuracy
   - Test with multi-page statements

### Integration Testing

Test the complete flow:
```python
import requests

# Upload file
with open('test_statement.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/',
        files={'file': f}
    )

# Save result
with open('output.xlsx', 'wb') as f:
    f.write(response.content)
```

### WebSocket Testing

Test WebSocket separately:
```python
import asyncio
import websockets

async def test():
    uri = "ws://localhost:8001"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

asyncio.run(test())
```

---

## Debugging Tips

### Enable Debug Logging

Add logging to convert.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect DataFrame at Each Stage

Add print statements:
```python
print(df.head())
print(df.columns)
print(df.dtypes)
```

### Check PDF Extraction

Test tabula extraction manually:
```python
import tabula
df = tabula.read_pdf('test.pdf', pages='1')
print(df)
```

### Monitor WebSocket Traffic

Use browser developer tools:
1. Open DevTools (F12)
2. Go to Network tab
3. Filter by WS (WebSocket)
4. Watch message exchange

---

## Future Enhancements

Potential improvements:
- [ ] Add authentication and user sessions
- [ ] Support multiple bank formats
- [ ] Implement client-side progress bar with WebSocket
- [ ] Add file validation before processing
- [ ] Store conversion history
- [ ] Batch processing of multiple files
- [ ] Docker containerization
- [ ] Add unit tests and CI/CD
- [ ] Improve error messages and user feedback
- [ ] Add API documentation with Swagger UI
