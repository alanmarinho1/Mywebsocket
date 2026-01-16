# Documentação da API

Este documento descreve a REST API e a interface WebSocket para o conversor de PDF Bradesco para Excel.

## Índice

1. [URL Base](#url-base)
2. [Endpoints da REST API](#endpoints-da-rest-api)
3. [WebSocket API](#websocket-api)
4. [Tratamento de Erros](#tratamento-de-erros)
5. [Exemplos](#exemplos)

---

## URL Base

### Desenvolvimento
```
http://localhost:8000
```

### Produção
Substitua pelo seu domínio implantado:
```
https://your-domain.com
```

---

## Endpoints da REST API

### 1. Obter Interface de Upload

Serve a página HTML de upload.

**Endpoint**: `GET /`

**Descrição**: Retorna a interface web para fazer upload de arquivos PDF.

**Requisição**:
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Resposta**:
- **Status**: 200 OK
- **Content-Type**: text/html; charset=utf-8
- **Body**: Página HTML com formulário de upload

**Exemplo**:
```bash
curl http://localhost:8000/
```

---

### 2. Upload e Conversão de PDF

Converte um extrato bancário Bradesco em PDF para o formato Excel.

**Endpoint**: `POST /`

**Descrição**: Aceita um arquivo PDF, converte para Excel e retorna o arquivo Excel.

**Requisição**:

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

**Parâmetros**:

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| file | File | Sim | Arquivo PDF de extrato bancário Bradesco |

**Resposta (Sucesso)**:
- **Status**: 200 OK
- **Content-Type**: application/xlsx
- **Content-Disposition**: attachment; filename={original_name}.xlsx
- **Body**: Dados binários do arquivo Excel

**Resposta (Erro)**:
- **Status**: 400 Bad Request
- **Content-Type**: application/json
- **Body**:
```json
{
  "detail": "O arquivo statement.pdf não é PDF"
}
```

**Exemplo (cURL)**:
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

### Conexão

Fornece atualizações de progresso em tempo real durante a conversão do PDF.

**Endpoint**: `ws://localhost:8001/`

**Protocol**: WebSocket

**Descrição**: Conecta ao servidor WebSocket para receber atualizações de processamento página por página.

### Fluxo de Conexão

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

### Mensagens

**Direção**: Server → Client

**Formato**: String de texto simples

**Conteúdo**: Número da página atual sendo processada

**Exemplos**:
- `"1"` - Processando página 1
- `"2"` - Processando página 2
- `"15"` - Processando página 15

### Implementação do Cliente

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

## Tratamento de Erros

### Códigos de Erro HTTP

| Código de Status | Descrição | Causa Comum |
|------------------|-----------|-------------|
| 200 | Sucesso | Arquivo convertido com sucesso |
| 400 | Requisição Inválida | PDF inválido ou formato de arquivo incorreto |
| 422 | Entidade Não Processável | Parâmetro de arquivo ausente |
| 500 | Erro Interno do Servidor | Erro no servidor durante o processamento |

### Formato de Resposta de Erro

```json
{
  "detail": "Error description in Portuguese or English"
}
```

### Erros Comuns

#### 1. Parâmetro de Arquivo Ausente

**Requisição**:
```bash
curl -X POST http://localhost:8000/
```

**Resposta**:
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

#### 2. Arquivo PDF Inválido

**Resposta**:
```json
{
  "detail": "O arquivo invalid_file.txt não é PDF"
}
```

#### 3. Erro de Processamento

**Resposta**:
```json
{
  "detail": "Error processing PDF: [specific error message]"
}
```

### Erros do WebSocket

**Conexão Recusada**:
```
Error: WebSocket connection failed: Connection refused
```
- **Causa**: Servidor WebSocket não está em execução
- **Solução**: Iniciar o servidor `convert.py`

**Conexão Fechada**:
```
ConnectionClosedOK
```
- **Causa**: Fechamento normal após o processamento
- **Ação**: Nenhuma ação necessária, comportamento esperado

---

## Exemplos

### Exemplo de Fluxo de Trabalho Completo (Python)

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

### Exemplo de Processamento em Lote

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

### Integração com Aplicação Web (JavaScript)

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

## Limitação de Taxa

Atualmente, não há limitação de taxa implementada. Para uso em produção, considere:

- Implementar middleware de limitação de taxa
- Adicionar tokens de autenticação
- Definir limites de tamanho máximo de arquivo
- Sistema de fila para requisições simultâneas

---

## Considerações de Segurança

### Implementação Atual

- Nenhuma autenticação necessária
- Nenhuma validação de entrada além do tipo de arquivo
- Arquivos temporários armazenados no disco do servidor
- Nenhuma criptografia de arquivos enviados

### Recomendações para Produção

1. **Adicionar Autenticação**: Implementar chaves API ou OAuth
2. **Validar Entrada**: Verificar tamanho e conteúdo do arquivo
3. **Armazenamento Seguro**: Criptografar arquivos temporários
4. **HTTPS**: Usar certificados SSL/TLS
5. **Limitação de Taxa**: Prevenir abuso
6. **Registro de Logs**: Rastrear todas as chamadas da API
7. **CORS**: Configurar cabeçalhos CORS apropriados

---

## Versionamento

Versão atual: 1.0 (implícita)

Versões futuras devem incluir a versão na URL:
```
/api/v1/convert
/api/v2/convert
```

---

## Suporte

Para questões ou problemas com a API:
- Consulte [README.md](README.md) para documentação geral
- Veja [TECHNICAL.md](TECHNICAL.md) para detalhes de implementação
- Abra uma issue no GitHub com questões específicas sobre a API
