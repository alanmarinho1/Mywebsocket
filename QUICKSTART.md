# Guia de Início Rápido

Comece a usar o conversor de PDF Bradesco para Excel em 5 minutos.

## Pré-requisitos

- Python 3.7 ou superior
- Java Runtime Environment (JRE)
- Git (para clonar)

## Passos de Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/alanmarinho1/Mywebsocket.git
cd Mywebsocket
```

### 2. Instalar Dependências Python

```bash
pip install -r requirements.txt
```

Se encontrar problemas, tente usar um ambiente virtual:

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

### 3. Verificar Instalação do Java

```bash
java -version
```

A saída esperada deve mostrar a versão 8 do Java ou superior. Se o Java não estiver instalado:
- **Windows/Mac**: Baixe de [java.com](https://www.java.com/)
- **Linux**: `sudo apt-get install default-jre` (Ubuntu/Debian)

### 4. Iniciar o Servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Você deverá ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 5. Acessar a Aplicação

Abra seu navegador e vá para:
```
http://localhost:8000
```

### 6. Converter Seu Primeiro PDF

1. Clique em "Escolher arquivo"
2. Selecione um PDF de extrato bancário Bradesco
3. Clique em "Converter"
4. Aguarde o processamento
5. O arquivo Excel será baixado automaticamente

## Problemas Comuns e Soluções

### "Java not found"

**Problema**: tabula-py não consegue encontrar o Java

**Solução**:
```bash
# Verify Java is in PATH
echo $JAVA_HOME  # Linux/Mac
echo %JAVA_HOME%  # Windows

# If empty, install Java and add to PATH
```

### "Module not found"

**Problema**: Pacote Python ausente

**Solução**:
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### "Port already in use"

**Problema**: Porta 8000 está ocupada

**Solução**:
```bash
# Use a different port
uvicorn main:app --reload --port 8080
# Then access http://localhost:8080
```

### "File not processing"

**Problema**: PDF não converte

**Solução**:
- Verifique se é um PDF de extrato bancário Bradesco
- Certifique-se de que o PDF não está protegido por senha
- Verifique se o PDF não está corrompido
- Tente com um arquivo PDF diferente

## Usando a API

### Upload via Linha de Comando

```bash
# Upload and convert a PDF
curl -X POST http://localhost:8000/ \
  -F "file=@/path/to/statement.pdf" \
  -o output.xlsx
```

### Script Python

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

## Testando o Servidor WebSocket

### Iniciar Servidor WebSocket

```bash
python convert.py
```

### Testar com Cliente Python

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

### Testar com Console do Navegador

1. Abra o console do navegador (F12)
2. Cole e execute:

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

## Visão Geral da Estrutura do Projeto

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

## Próximos Passos

- Leia o [README.md](README.md) para documentação detalhada
- Confira o [TECHNICAL.md](TECHNICAL.md) para detalhes de arquitetura
- Revise o código para entender a lógica de conversão
- Personalize para suas necessidades

## Obtendo Ajuda

Se você encontrar problemas:

1. Verifique a saída do console para mensagens de erro
2. Revise a seção de solução de problemas acima
3. Verifique se todas as dependências estão instaladas corretamente
4. Certifique-se de estar usando um formato de PDF Bradesco válido
5. Abra uma issue no GitHub com detalhes do erro

## Implantação em Produção

Para uso em produção:

```bash
# Install production server
pip install gunicorn

# Run with gunicorn (more stable than uvicorn --reload)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Considere:
- Configurar um proxy reverso (nginx/Apache)
- Adicionar certificados HTTPS/SSL
- Implementar autenticação
- Adicionar limitação de taxa
- Configurar monitoramento e logging
- Usar variáveis de ambiente para configuração

## Modo de Desenvolvimento

Para desenvolvimento com auto-reload:

```bash
# Auto-reload on file changes
uvicorn main:app --reload --log-level debug
```

## Licença e Contribuição

Veja o [README.md](README.md) principal para informações de licença e diretrizes de contribuição.
