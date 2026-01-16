# Exemplos

Este documento fornece exemplos práticos de uso do conversor de PDF para Excel do Bradesco em vários cenários.

## Índice

1. [Exemplos de Uso Básico](#exemplos-de-uso-básico)
2. [Exemplos de Integração](#exemplos-de-integração)
3. [Cenários Avançados](#cenários-avançados)
4. [Exemplos de Testes](#exemplos-de-testes)

---

## Exemplos de Uso Básico

### Exemplo 1: Upload Simples via Linha de Comando

A maneira mais simples de converter um PDF:

```bash
curl -X POST http://localhost:8000/ \
  -F "file=@my_statement.pdf" \
  -o converted.xlsx
```

### Exemplo 2: Script Python

```python
#!/usr/bin/env python3
import requests
import sys

def convert_pdf(pdf_path, output_path):
    """Convert a PDF to Excel using the API"""
    url = "http://localhost:8000/"
    
    try:
        with open(pdf_path, 'rb') as pdf_file:
            files = {'file': pdf_file}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as output:
                output.write(response.content)
            print(f"✓ Successfully converted {pdf_path} to {output_path}")
            return True
        else:
            print(f"✗ Error {response.status_code}: {response.json()}")
            return False
    except FileNotFoundError:
        print(f"✗ File not found: {pdf_path}")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_script.py <input.pdf> <output.xlsx>")
        sys.exit(1)
    
    convert_pdf(sys.argv[1], sys.argv[2])
```

Usage:
```bash
python convert_script.py statement.pdf result.xlsx
```

### Exemplo 3: Script Node.js

```javascript
const fs = require('fs');
const axios = require('axios');
const FormData = require('form-data');

async function convertPDF(pdfPath, outputPath) {
    try {
        const form = new FormData();
        form.append('file', fs.createReadStream(pdfPath));

        const response = await axios.post('http://localhost:8000/', form, {
            headers: {
                ...form.getHeaders(),
            },
            responseType: 'arraybuffer'
        });

        fs.writeFileSync(outputPath, response.data);
        console.log(`✓ Successfully converted ${pdfPath} to ${outputPath}`);
        return true;
    } catch (error) {
        console.error(`✗ Error: ${error.message}`);
        return false;
    }
}

// Usage
const [,, inputFile, outputFile] = process.argv;

if (!inputFile || !outputFile) {
    console.log('Usage: node convert.js <input.pdf> <output.xlsx>');
    process.exit(1);
}

convertPDF(inputFile, outputFile);
```

---

## Exemplos de Integração

### Exemplo 4: Aplicação Web Flask

Integre o conversor em uma aplicação Flask:

```python
from flask import Flask, render_template, request, send_file
import requests
import io

app = Flask(__name__)

CONVERTER_API = "http://localhost:8000/"

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
    
    file = request.files['file']
    
    if file.filename == '':
        return {'error': 'No file selected'}, 400
    
    # Forward to converter API
    files = {'file': (file.filename, file.stream, file.content_type)}
    response = requests.post(CONVERTER_API, files=files)
    
    if response.status_code == 200:
        # Return Excel file
        return send_file(
            io.BytesIO(response.content),
            mimetype='application/xlsx',
            as_attachment=True,
            download_name=file.filename.replace('.pdf', '.xlsx')
        )
    else:
        return {'error': 'Conversion failed'}, 500

if __name__ == '__main__':
    app.run(port=5000)
```

### Exemplo 5: Integração com Django

```python
# views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests

def convert_pdf(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Send to converter API
        files = {'file': uploaded_file}
        response = requests.post('http://localhost:8000/', files=files)
        
        if response.status_code == 200:
            # Return Excel file
            excel_response = HttpResponse(
                response.content,
                content_type='application/xlsx'
            )
            excel_response['Content-Disposition'] = \
                f'attachment; filename="{uploaded_file.name.replace(".pdf", ".xlsx")}"'
            return excel_response
        else:
            return JsonResponse({'error': 'Conversion failed'}, status=500)
    
    return render(request, 'upload.html')
```

### Exemplo 6: Frontend React

```javascript
import React, { useState } from 'react';
import axios from 'axios';

function PDFConverter() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!file) {
            alert('Please select a file');
            return;
        }

        setLoading(true);
        setProgress(0);

        // Connect to WebSocket for progress
        const ws = new WebSocket('ws://localhost:8001/');
        ws.onmessage = (event) => {
            setProgress(parseInt(event.data));
        };

        // Upload file
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(
                'http://localhost:8000/',
                formData,
                {
                    responseType: 'blob',
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            );

            // Download the file
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', file.name.replace('.pdf', '.xlsx'));
            document.body.appendChild(link);
            link.click();
            link.remove();

            ws.close();
            setLoading(false);
            setProgress(0);
        } catch (error) {
            console.error('Error:', error);
            alert('Conversion failed');
            setLoading(false);
            ws.close();
        }
    };

    return (
        <div>
            <h2>PDF to Excel Converter</h2>
            <form onSubmit={handleSubmit}>
                <input 
                    type="file" 
                    accept=".pdf" 
                    onChange={handleFileChange}
                    disabled={loading}
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Converting...' : 'Convert'}
                </button>
            </form>
            {loading && (
                <div>
                    <p>Processing page: {progress}</p>
                    <progress value={progress} max="100" />
                </div>
            )}
        </div>
    );
}

export default PDFConverter;
```

---

## Cenários Avançados

### Exemplo 7: Processamento em Lote com Rastreamento de Progresso

```python
import requests
import asyncio
import websockets
from pathlib import Path
import json

class BatchConverter:
    def __init__(self, api_url="http://localhost:8000/", ws_url="ws://localhost:8001/"):
        self.api_url = api_url
        self.ws_url = ws_url
        self.results = []

    async def monitor_websocket(self, filename):
        """Monitor conversion progress for a file"""
        try:
            async with websockets.connect(self.ws_url) as ws:
                pages = []
                while True:
                    try:
                        page = await asyncio.wait_for(ws.recv(), timeout=60.0)
                        pages.append(page)
                        print(f"  [{filename}] Page {page}")
                    except asyncio.TimeoutError:
                        break
                    except websockets.exceptions.ConnectionClosed:
                        break
                return pages
        except Exception as e:
            print(f"  [{filename}] WebSocket error: {e}")
            return []

    def convert_file(self, pdf_path, output_dir):
        """Convert a single PDF file"""
        pdf_path = Path(pdf_path)
        output_path = Path(output_dir) / pdf_path.name.replace('.pdf', '.xlsx')
        
        print(f"\n📄 Converting: {pdf_path.name}")
        
        try:
            with open(pdf_path, 'rb') as f:
                response = requests.post(
                    self.api_url,
                    files={'file': f},
                    timeout=300  # 5 minutes timeout
                )
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Success: {output_path.name}")
                return {'file': pdf_path.name, 'status': 'success', 'output': str(output_path)}
            else:
                print(f"✗ Failed: {response.status_code}")
                return {'file': pdf_path.name, 'status': 'failed', 'error': response.status_code}
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return {'file': pdf_path.name, 'status': 'error', 'error': str(e)}

    def batch_convert(self, input_dir, output_dir):
        """Convert all PDFs in a directory"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        pdf_files = list(input_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {input_dir}")
            return
        
        print(f"Found {len(pdf_files)} PDF files to convert\n")
        
        for pdf_file in pdf_files:
            result = self.convert_file(pdf_file, output_dir)
            self.results.append(result)
        
        # Print summary
        print("\n" + "="*50)
        print("CONVERSION SUMMARY")
        print("="*50)
        
        success = sum(1 for r in self.results if r['status'] == 'success')
        failed = len(self.results) - success
        
        print(f"Total files: {len(self.results)}")
        print(f"Successful: {success}")
        print(f"Failed: {failed}")
        
        # Save results to JSON
        with open(output_path / 'results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return self.results

# Usage
if __name__ == "__main__":
    converter = BatchConverter()
    converter.batch_convert("./input_pdfs", "./output_excel")
```

### Exemplo 8: Tratamento de Erros e Lógica de Retentativa

```python
import requests
import time
from functools import wraps

def retry(max_attempts=3, delay=2, backoff=2):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    
                    print(f"Attempt {attempts} failed: {e}")
                    print(f"Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator

class RobustConverter:
    def __init__(self, api_url="http://localhost:8000/"):
        self.api_url = api_url
    
    @retry(max_attempts=3, delay=2, backoff=2)
    def convert_with_retry(self, pdf_path, output_path):
        """Convert PDF with automatic retry on failure"""
        
        # Validate file exists and is PDF
        if not pdf_path.endswith('.pdf'):
            raise ValueError(f"File must be a PDF: {pdf_path}")
        
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"File not found: {pdf_path}")
        
        # Check file size (example: max 50MB)
        file_size = Path(pdf_path).stat().st_size
        if file_size > 50 * 1024 * 1024:
            raise ValueError(f"File too large: {file_size / 1024 / 1024:.2f}MB")
        
        print(f"Converting: {pdf_path}")
        
        with open(pdf_path, 'rb') as f:
            response = requests.post(
                self.api_url,
                files={'file': f},
                timeout=300
            )
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✓ Saved: {output_path}")
            return True
        else:
            error_msg = f"HTTP {response.status_code}"
            try:
                error_detail = response.json().get('detail', error_msg)
            except:
                error_detail = error_msg
            raise Exception(f"Conversion failed: {error_detail}")

# Usage
converter = RobustConverter()

try:
    converter.convert_with_retry("statement.pdf", "output.xlsx")
except Exception as e:
    print(f"Failed after all retries: {e}")
```

### Exemplo 9: Processamento em Lote Agendado

```python
import schedule
import time
from pathlib import Path
from datetime import datetime
import shutil

class ScheduledConverter:
    def __init__(self, input_dir, output_dir, processed_dir):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.processed_dir = Path(processed_dir)
        
        # Create directories
        self.output_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
    
    def process_new_files(self):
        """Process all new PDF files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n[{timestamp}] Checking for new files...")
        
        pdf_files = list(self.input_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("No new files to process")
            return
        
        print(f"Found {len(pdf_files)} files to process")
        
        for pdf_file in pdf_files:
            try:
                # Convert
                output_file = self.output_dir / pdf_file.name.replace('.pdf', '.xlsx')
                
                with open(pdf_file, 'rb') as f:
                    response = requests.post(
                        'http://localhost:8000/',
                        files={'file': f}
                    )
                
                if response.status_code == 200:
                    # Save Excel
                    with open(output_file, 'wb') as f:
                        f.write(response.content)
                    
                    # Move processed PDF
                    shutil.move(str(pdf_file), str(self.processed_dir / pdf_file.name))
                    
                    print(f"✓ Processed: {pdf_file.name}")
                else:
                    print(f"✗ Failed: {pdf_file.name}")
                    
            except Exception as e:
                print(f"✗ Error processing {pdf_file.name}: {e}")
    
    def start_scheduler(self, interval_minutes=30):
        """Start scheduled processing"""
        print(f"Starting scheduler (checking every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop")
        
        # Run immediately on start
        self.process_new_files()
        
        # Schedule recurring runs
        schedule.every(interval_minutes).minutes.do(self.process_new_files)
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Usage
if __name__ == "__main__":
    converter = ScheduledConverter(
        input_dir="./incoming",
        output_dir="./converted",
        processed_dir="./processed"
    )
    
    # Check every 30 minutes
    converter.start_scheduler(interval_minutes=30)
```

---

## Exemplos de Testes

### Exemplo 10: Teste Unitário para Cliente do Conversor

```python
import unittest
from unittest.mock import patch, Mock
import io

class TestConverter(unittest.TestCase):
    def setUp(self):
        self.api_url = "http://localhost:8000/"
        self.test_pdf = b"%PDF-1.4 fake pdf content"
    
    @patch('requests.post')
    def test_successful_conversion(self, mock_post):
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake excel content"
        mock_post.return_value = mock_response
        
        # Test conversion
        files = {'file': io.BytesIO(self.test_pdf)}
        response = mock_post(self.api_url, files=files)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
    
    @patch('requests.post')
    def test_failed_conversion(self, mock_post):
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'detail': 'Invalid PDF'}
        mock_post.return_value = mock_response
        
        # Test conversion
        files = {'file': io.BytesIO(self.test_pdf)}
        response = mock_post(self.api_url, files=files)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'Invalid PDF')

if __name__ == '__main__':
    unittest.main()
```

### Exemplo 11: Teste de Integração

```python
import pytest
import requests
from pathlib import Path

class TestConverterAPI:
    API_URL = "http://localhost:8000/"
    
    def test_upload_valid_pdf(self, sample_pdf):
        """Test uploading a valid PDF file"""
        with open(sample_pdf, 'rb') as f:
            response = requests.post(
                self.API_URL,
                files={'file': f}
            )
        
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/xlsx'
        assert len(response.content) > 0
    
    def test_upload_invalid_file(self, sample_text_file):
        """Test uploading a non-PDF file"""
        with open(sample_text_file, 'rb') as f:
            response = requests.post(
                self.API_URL,
                files={'file': f}
            )
        
        assert response.status_code == 400
    
    def test_no_file_upload(self):
        """Test request without file"""
        response = requests.post(self.API_URL)
        assert response.status_code == 422

@pytest.fixture
def sample_pdf(tmp_path):
    """Create a sample PDF file for testing"""
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 test content")
    return pdf_file

@pytest.fixture
def sample_text_file(tmp_path):
    """Create a sample text file"""
    text_file = tmp_path / "test.txt"
    text_file.write_text("Not a PDF file")
    return text_file
```

---

## Mais Exemplos

Consulte os arquivos de documentação individuais para mais exemplos:
- [README.md](README.md) - Uso básico
- [QUICKSTART.md](QUICKSTART.md) - Exemplos de início rápido
- [API.md](API.md) - Exemplos de uso da API
- [TECHNICAL.md](TECHNICAL.md) - Exemplos de implementação técnica
