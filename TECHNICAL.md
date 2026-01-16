# Documentação Técnica

## Índice
1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Fluxo de Dados](#fluxo-de-dados)
3. [Descrição dos Módulos](#descrição-dos-módulos)
4. [Algoritmo de Processamento de PDF](#algoritmo-de-processamento-de-pdf)
5. [Implementação WebSocket](#implementação-websocket)
6. [Referência da API](#referência-da-api)

---

## Visão Geral da Arquitetura

Esta aplicação segue uma arquitetura cliente-servidor com dois componentes principais:

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

## Fluxo de Dados

### 1. Fluxo de Upload de Arquivo (HTTP)

```
Usuário → [Selecionar PDF] → [Enviar Formulário] → FastAPI POST / endpoint
                                            │
                                            ▼
                                    Salvar arquivo temporariamente
                                            │
                                            ▼
                                    Chamar função convert()
                                            │
                                            ▼
                                    Processar páginas do PDF
                                            │
                                            ▼
                                    Gerar Excel (BytesIO)
                                            │
                                            ▼
                                    Deletar arquivo temporário
                                            │
                                            ▼
                                    Retornar Excel como download
```

### 2. Fluxo de Progresso via WebSocket

```
convert.py inicia processamento → Para cada página:
                                    │
                                    ▼
                            Enviar número da página via WebSocket
                                    │
                                    ▼
                            Navegador recebe atualização
                                    │
                                    ▼
                            Atualizar barra de progresso (se implementada)
```

---

## Descrição dos Módulos

### main.py - Aplicação FastAPI

**Propósito**: Servidor HTTP para manipulação de arquivos

**Componentes Principais**:
- `app`: Instância do FastAPI
- `templates`: Renderizador de templates Jinja2
- `home()`: Endpoint GET servindo a página de upload
- `upload_file()`: Endpoint POST lidando com upload e conversão de PDF

**Dependências**: FastAPI, Jinja2, módulo convert

**Fluxo de Trabalho**:
1. Recebe arquivo PDF enviado
2. Salva arquivo no disco temporariamente
3. Chama função `convert()`
4. Remove arquivo temporário
5. Retorna arquivo Excel como resposta em streaming

---

### convert.py - Núcleo de Processamento de PDF

**Propósito**: Lógica principal de conversão com suporte WebSocket

**Funções Principais**:

#### `convert(websocket)`
- **Parâmetros**: Objeto de conexão WebSocket
- **Retorna**: Objeto BytesIO contendo arquivo Excel
- **Processo**:
  1. Abre arquivo PDF usando PyPDF2
  2. Itera através de cada página
  3. Envia atualizações de progresso via WebSocket
  4. Extrai texto e identifica tipo de página
  5. Determina área de extração baseada no conteúdo da página
  6. Usa tabula para extrair dados da tabela
  7. Processa e limpa dados usando funções auxiliares
  8. Concatena todas as páginas no DataFrame final
  9. Exporta para Excel em memória

#### `main()`
- Inicia servidor WebSocket na porta 8001
- Executa indefinidamente aguardando conexões

#### `server()`
- Servidor alternativo com manipulação de SIGTERM para desligamento gracioso

---

### helpers.py - Funções de Processamento de Dados

**Propósito**: Limpeza e formatação de DataFrame

#### `df_ajust_first_page(df, listadrop, empresa, ag, conta)`

Processa a primeira página do extrato:
- Renomeia colunas se necessário
- Extrai datas de transação do texto combinado
- Lida com transações multi-linha
- Adiciona colunas de empresa, agência e conta
- Identifica última linha incompleta

**Parâmetros**:
- `df`: pandas DataFrame do tabula
- `listadrop`: Lista para rastrear linhas a deletar
- `empresa`: Nome da empresa
- `ag`: Número da agência
- `conta`: Número da conta

**Retorna**: Tupla (DataFrame processado, booleano indicando última linha incompleta)

#### `df_ajust_pages(df, listadrop, lastrow)`

Processa páginas subsequentes:
- Lida com diferentes configurações de colunas
- Padroniza nomes de colunas
- Gerencia continuação de página (de página anterior incompleta)
- Consolida transações multi-linha
- Remove linhas de "SALDO ANTERIOR"

**Parâmetros**:
- `df`: pandas DataFrame do tabula
- `listadrop`: Lista para rastrear linhas a deletar
- `lastrow`: Booleano indicando se página anterior terminou incompleta

**Retorna**: Tupla (DataFrame processado, booleano indicando última linha incompleta)

#### `last_df_ajust(df, listadrop)`

Limpeza final do DataFrame completo:
- Consolida transações multi-linha restantes
- Propaga informações de data, empresa, agência e conta
- Remove linhas de "Total"
- Redefine índice

**Parâmetros**:
- `df`: DataFrame concatenado completo
- `listadrop`: Lista para rastrear linhas a deletar

**Retorna**: DataFrame limpo e formatado

---

### keyword_position.py - Detecção de Área

**Propósito**: Calcular dinamicamente áreas de extração de PDF baseadas em posições de texto

#### `keyword_first_page(file, x)`

Calcula área de extração para primeira página:
- Busca por "Os dados acima" (aviso de dados)
- Busca por "Data" (cabeçalho da coluna de data)
- Retorna coordenadas para parâmetro de área do tabula

**Retorna**: Tupla (topo, esquerda, baixo, direita) em pontos

#### `keyword_last_page(file, x)`

Calcula área de extração para última página:
- Busca pela palavra-chave "Total"
- Retorna coordenadas excluindo seções de resumo

**Retorna**: Tupla (topo, esquerda, baixo, direita) em pontos

---

## Algoritmo de Processamento de PDF

### Classificação de Páginas

O algoritmo classifica cada página em um dos vários tipos:

1. **Primeira Página** (`Folha 1/`)
   - Contém metadados da conta (empresa, agencia, conta)
   - Pode ter texto de rodapé especial
   - Usa extração de área dinâmica ou estática

2. **Página Vazia/Resumo**
   - Contém apenas avisos ou mensagem de "sem transações"
   - Ignorada durante processamento

3. **Última Página com Total**
   - Contém "Total" e dados de transações
   - Usa `keyword_last_page()` para detecção de área

4. **Página Regular de Transações**
   - Contém apenas dados de transações
   - Usa coordenadas de área estática

### Manipulação de Transações Multi-linha

Extratos bancários frequentemente dividem descrições de transações em múltiplas linhas. O algoritmo detecta isso por:

1. Verificar se uma linha tem um valor de saldo mas as linhas adjacentes não
2. Concatenar texto das linhas adjacentes em transação única
3. Marcar linhas adjacentes para deleção
4. Manter alinhamento adequado dos dados

### Propagação de Datas

Datas de transações podem não se repetir para cada transação. O algoritmo:
1. Detecta quando uma data existe
2. Propaga-a para transações subsequentes
3. Para quando uma nova data é encontrada

---

## Implementação WebSocket

### Lado do Servidor (convert.py)

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

O servidor:
- Aceita conexões WebSocket
- Envia números de página como strings
- Lida com fechamentos de conexão graciosamente

### Lado do Cliente (index.html)

Atualmente comentado no HTML, mas a estrutura é:

```javascript
const websocket = new WebSocket("ws://localhost:8001/");
// Handle incoming messages to update progress bar
```

---

## Referência da API

### Endpoints FastAPI

#### GET /

**Descrição**: Serve a interface web de upload

**Resposta**:
- Content-Type: `text/html`
- Body: Template index.html renderizado

**Exemplo**:
```bash
curl http://localhost:8000/
```

---

#### POST /

**Descrição**: Faz upload de PDF e retorna arquivo Excel convertido

**Requisição**:
- Method: POST
- Content-Type: `multipart/form-data`
- Body Parameter: `file` (arquivo PDF)

**Resposta**:
- Content-Type: `application/xlsx`
- Content-Disposition: `attachment; filename={original_name}.xlsx`
- Body: Binário do arquivo Excel

**Resposta de Erro**:
- Status: 400
- Detail: "O arquivo {filename} não é PDF"

**Exemplo**:
```bash
curl -X POST http://localhost:8000/ \
  -F "file=@statement.pdf" \
  -o output.xlsx
```

---

### Protocolo WebSocket

#### Conexão

**URL**: `ws://localhost:8001/`

**Protocolo**: WebSocket

#### Mensagens

**Direção**: Servidor → Cliente

**Formato**: String de texto puro representando número da página

**Exemplos de Mensagens**:
- `"1"` - Processando página 1
- `"2"` - Processando página 2
- `"3"` - Processando página 3

**Ciclo de Vida da Conexão**:
1. Cliente conecta
2. Servidor inicia processamento
3. Servidor envia atualizações de página
4. Processamento completa
5. Conexão fecha

---

## Notas de Desenvolvimento

### Adicionando Suporte para Novos Formatos de Banco

Para adaptar isso para outros bancos:

1. **Analisar Estrutura do PDF**: 
   - Use PyMuPDF para examinar layout do texto
   - Identifique áreas de tabela e palavras-chave

2. **Atualizar Áreas de Extração**:
   - Modifique coordenadas de área em `convert.py`
   - Atualize detecção de palavras-chave em `keyword_position.py`

3. **Ajustar Mapeamento de Colunas**:
   - Atualize nomes de colunas em `helpers.py`
   - Modifique padrões regex para extração de dados

4. **Testar Minuciosamente**:
   - Teste com múltiplos formatos de extrato
   - Valide todos os tipos de dados (datas, valores, etc.)

### Considerações de Performance

- **Uso de Memória**: PDFs grandes são processados inteiramente em memória
- **Tempo de Processamento**: Proporcional ao número de páginas (≈1-2 segundos por página)
- **Requisições Concorrentes**: FastAPI suporta async, mas I/O de arquivo é síncrono
- **Overhead de WebSocket**: Mínimo, envia apenas números de página

### Limitações Conhecidas

1. **Formato Único**: Suporta apenas formato de extrato do banco Bradesco
2. **Sem Autenticação**: Sem autenticação de usuário ou criptografia de arquivo
3. **Arquivos Temporários**: Arquivos enviados brevemente armazenados em disco
4. **Tratamento de Erros**: Validação limitada do conteúdo do PDF
5. **Sem Persistência**: Sem banco de dados ou armazenamento de arquivo

---

## Testes

### Passos de Teste Manual

1. **Iniciar o servidor**:
```bash
uvicorn main:app --reload
```

2. **Acessar interface**: http://localhost:8000

3. **Fazer upload de PDF de teste**: Use um extrato Bradesco de exemplo

4. **Verificar saída**: 
   - Verificar se arquivo Excel baixa
   - Verificar precisão dos dados
   - Testar com extratos multi-página

### Teste de Integração

Testar o fluxo completo:
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

### Teste de WebSocket

Testar WebSocket separadamente:
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

## Dicas de Depuração

### Habilitar Log de Debug

Adicionar logging a convert.py:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspecionar DataFrame em Cada Estágio

Adicionar declarações print:
```python
print(df.head())
print(df.columns)
print(df.dtypes)
```

### Verificar Extração de PDF

Testar extração tabula manualmente:
```python
import tabula
df = tabula.read_pdf('test.pdf', pages='1')
print(df)
```

### Monitorar Tráfego WebSocket

Usar ferramentas de desenvolvedor do navegador:
1. Abrir DevTools (F12)
2. Ir para aba Network
3. Filtrar por WS (WebSocket)
4. Observar troca de mensagens

---

## Melhorias Futuras

Potenciais melhorias:
- [ ] Adicionar autenticação e sessões de usuário
- [ ] Suportar múltiplos formatos de banco
- [ ] Implementar barra de progresso do lado do cliente com WebSocket
- [ ] Adicionar validação de arquivo antes do processamento
- [ ] Armazenar histórico de conversões
- [ ] Processamento em lote de múltiplos arquivos
- [ ] Containerização Docker
- [ ] Adicionar testes unitários e CI/CD
- [ ] Melhorar mensagens de erro e feedback do usuário
- [ ] Adicionar documentação da API com Swagger UI
