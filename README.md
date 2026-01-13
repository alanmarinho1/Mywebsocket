# Bradesco Bank Statement PDF to Excel Converter

A Python-based web application that converts Bradesco bank statement PDFs into Excel spreadsheets (.xlsx) with real-time progress tracking via WebSocket.

## 🌟 Features

- **PDF to Excel Conversion**: Automatically extracts and processes Bradesco bank statement data from PDF files
- **Web Interface**: User-friendly HTML interface for file upload
- **Real-time Progress**: WebSocket-based progress tracking during conversion
- **Data Extraction**: Parses transaction details including:
  - Transaction dates
  - Descriptions
  - Document numbers
  - Credit/Debit amounts
  - Account balances
  - Company, agency, and account information
- **Multi-page Processing**: Handles bank statements with multiple pages
- **Data Cleaning**: Automatically cleans and formats extracted data

## 📋 Requirements

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)
- Pandas
- Tabula-py
- PyPDF2
- PyMuPDF (fitz)
- Websockets
- Java Runtime Environment (required by tabula-py)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/alanmarinho1/Mywebsocket.git
cd Mywebsocket
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Ensure Java is installed** (required for tabula-py)
```bash
java -version
```

If Java is not installed, download and install it from [java.com](https://www.java.com/).

## 💻 Usage

### Running the Web Application

1. **Start the FastAPI server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Access the web interface**
   - Open your browser and navigate to: `http://localhost:8000`
   - Upload a Bradesco bank statement PDF
   - Click "Converter" to start the conversion
   - Download the generated Excel file

### Running the WebSocket Server (Standalone)

For testing the WebSocket functionality separately:

```bash
python convert.py
```

The WebSocket server will start on `ws://localhost:8001`

### Simple WebSocket Example

```bash
python app.py
```

A basic WebSocket echo server for testing purposes.

## 🏗️ Architecture

### Components

1. **main.py** (FastAPI Application)
   - HTTP server for file upload and download
   - Serves the web interface
   - Handles PDF to Excel conversion requests

2. **convert.py** (Core Conversion Logic)
   - WebSocket server for real-time progress updates
   - PDF parsing and data extraction
   - Multi-page processing
   - Excel generation

3. **helpers.py** (Data Processing Functions)
   - `df_ajust_first_page()`: Processes the first page of the statement
   - `df_ajust_pages()`: Processes subsequent pages
   - `last_df_ajust()`: Final data cleanup and formatting

4. **keyword_position.py** (PDF Area Detection)
   - `keyword_first_page()`: Detects data area on first page
   - `keyword_last_page()`: Detects data area on last page

5. **Web Interface** (html/)
   - `index.html`: Upload form and progress bar
   - `main.js`: WebSocket client code
   - `estilo.css`: Styling

## 📡 API Endpoints

### GET /
Returns the HTML upload interface.

**Response**: HTML page

### POST /
Uploads and converts a Bradesco PDF statement to Excel.

**Request**:
- Content-Type: `multipart/form-data`
- Body: PDF file

**Response**:
- Content-Type: `application/xlsx`
- Body: Excel file download

## 🔌 WebSocket Protocol

The WebSocket server (port 8001) sends page processing progress:

**Connection**: `ws://localhost:8001/`

**Messages**: 
- Server sends the current page number being processed (e.g., "1", "2", "3"...)
- Client can track conversion progress in real-time

## 📊 Data Structure

The generated Excel file contains the following columns:

| Column | Description |
|--------|-------------|
| Empresa | Company name |
| Agencia | Bank agency number |
| Conta | Account number |
| Data | Transaction date |
| Lançamento | Transaction description |
| Dcto. | Document number |
| Crédito (R$) | Credit amount |
| Débito (R$) | Debit amount |
| Saldo (R$) | Account balance |

## 🔧 Configuration

### WebSocket Port
Default: 8001

To change, modify the port in:
- `convert.py`: Line 18 and 33
- `html/index.html`: Line 50 (if uncommented)

### FastAPI Port
Default: 8000

Set via uvicorn command:
```bash
uvicorn main:app --port <your_port>
```

## 🐛 Troubleshooting

### Java not found
**Error**: `Java is not installed or not in PATH`

**Solution**: Install Java Runtime Environment and ensure it's in your system PATH.

### PDF not processing
**Error**: File upload but no conversion

**Solution**: 
- Ensure the PDF is a valid Bradesco bank statement
- Check that the PDF is not password-protected
- Verify all dependencies are installed

### WebSocket connection failed
**Error**: Cannot connect to WebSocket

**Solution**: 
- Ensure convert.py server is running
- Check firewall settings for port 8001
- Verify the WebSocket URL matches your server address

## 📝 Notes

- This application is specifically designed for **Bradesco bank statements** and may not work with other bank formats
- The PDF structure must match the expected Bradesco format
- Large PDFs with many pages may take longer to process

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is available for use as-is. Please check with the repository owner for specific licensing terms.

## 👤 Author

Alan Marinho - [GitHub Profile](https://github.com/alanmarinho1)

## 🔗 Repository

[https://github.com/alanmarinho1/Mywebsocket](https://github.com/alanmarinho1/Mywebsocket)
