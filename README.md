# Conversor de Extratos Bancários Bradesco PDF para Excel

Uma aplicação web baseada em Python que converte extratos bancários Bradesco em PDF para planilhas Excel (.xlsx) com acompanhamento de progresso em tempo real via WebSocket.

## 📚 Documentação

- **[Guia de Início Rápido](QUICKSTART.md)** - Comece em 5 minutos
- **[Documentação da API](API.md)** - Referência REST API e WebSocket
- **[Documentação Técnica](TECHNICAL.md)** - Arquitetura e detalhes de implementação
- **[Exemplos](EXAMPLES.md)** - Exemplos de código e padrões de integração
- **[Como Contribuir](CONTRIBUTING.md)** - Como contribuir para o projeto

## 🌟 Funcionalidades

- **Conversão PDF para Excel**: Extrai e processa automaticamente dados de extratos bancários Bradesco de arquivos PDF
- **Interface Web**: Interface HTML amigável para upload de arquivos
- **Progresso em Tempo Real**: Acompanhamento de progresso baseado em WebSocket durante a conversão
- **Extração de Dados**: Analisa detalhes de transações incluindo:
  - Datas das transações
  - Descrições
  - Números de documento
  - Valores de crédito/débito
  - Saldos da conta
  - Informações de empresa, agência e conta
- **Processamento Multi-páginas**: Processa extratos bancários com múltiplas páginas
- **Limpeza de Dados**: Limpa e formata automaticamente os dados extraídos

## 📋 Requisitos

- Python 3.7+
- FastAPI
- Uvicorn (servidor ASGI)
- Pandas
- Tabula-py
- PyPDF2
- PyMuPDF (fitz)
- Websockets
- Java Runtime Environment (necessário para tabula-py)

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/alanmarinho1/Mywebsocket.git
cd Mywebsocket
```

2. **Instale as dependências Python**
```bash
pip install -r requirements.txt
```

3. **Certifique-se de que o Java está instalado** (necessário para tabula-py)
```bash
java -version
```

Se o Java não estiver instalado, baixe e instale a partir de [java.com](https://www.java.com/).

## 💻 Uso

### Executando a Aplicação Web

1. **Inicie o servidor FastAPI**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Acesse a interface web**
   - Abra seu navegador e navegue para: `http://localhost:8000`
   - Faça upload de um extrato bancário Bradesco em PDF
   - Clique em "Converter" para iniciar a conversão
   - Baixe o arquivo Excel gerado

### Executando o Servidor WebSocket (Standalone)

Para testar a funcionalidade WebSocket separadamente:

```bash
python convert.py
```

O servidor WebSocket iniciará em `ws://localhost:8001`

### Exemplo Simples de WebSocket

```bash
python app.py
```

Um servidor WebSocket echo básico para fins de teste.

## 🏗️ Arquitetura

### Componentes

1. **main.py** (Aplicação FastAPI)
   - Servidor HTTP para upload e download de arquivos
   - Serve a interface web
   - Gerencia requisições de conversão PDF para Excel

2. **convert.py** (Lógica Principal de Conversão)
   - Servidor WebSocket para atualizações de progresso em tempo real
   - Análise e extração de dados do PDF
   - Processamento multi-páginas
   - Geração de Excel

3. **helpers.py** (Funções de Processamento de Dados)
   - `df_ajust_first_page()`: Processa a primeira página do extrato
   - `df_ajust_pages()`: Processa páginas subsequentes
   - `last_df_ajust()`: Limpeza e formatação final dos dados

4. **keyword_position.py** (Detecção de Área do PDF)
   - `keyword_first_page()`: Detecta área de dados na primeira página
   - `keyword_last_page()`: Detecta área de dados na última página

5. **Interface Web** (html/)
   - `index.html`: Formulário de upload e barra de progresso
   - `main.js`: Código cliente WebSocket
   - `estilo.css`: Estilização

## 📡 Endpoints da API

### GET /
Retorna a interface HTML de upload.

**Resposta**: Página HTML

### POST /
Faz upload e converte um extrato Bradesco em PDF para Excel.

**Requisição**:
- Content-Type: `multipart/form-data`
- Body: Arquivo PDF

**Resposta**:
- Content-Type: `application/xlsx`
- Body: Download do arquivo Excel

## 🔌 Protocolo WebSocket

O servidor WebSocket (porta 8001) envia o progresso do processamento de páginas:

**Conexão**: `ws://localhost:8001/`

**Mensagens**: 
- O servidor envia o número da página atual sendo processada (ex: "1", "2", "3"...)
- O cliente pode acompanhar o progresso da conversão em tempo real

## 📊 Estrutura de Dados

O arquivo Excel gerado contém as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| Empresa | Nome da empresa |
| Agencia | Número da agência bancária |
| Conta | Número da conta |
| Data | Data da transação |
| Lançamento | Descrição da transação |
| Dcto. | Número do documento |
| Crédito (R$) | Valor do crédito |
| Débito (R$) | Valor do débito |
| Saldo (R$) | Saldo da conta |

## 🔧 Configuração

### Porta WebSocket
Padrão: 8001

Para alterar, modifique a porta em:
- `convert.py`: Linhas 18 e 33
- `html/index.html`: Linha 50 (se descomentado)

### Porta FastAPI
Padrão: 8000

Configure via comando uvicorn:
```bash
uvicorn main:app --port <sua_porta>
```

## 🐛 Solução de Problemas

### Java não encontrado
**Erro**: `Java is not installed or not in PATH`

**Solução**: Instale o Java Runtime Environment e certifique-se de que está no PATH do sistema.

### PDF não está processando
**Erro**: Upload de arquivo mas sem conversão

**Solução**: 
- Certifique-se de que o PDF é um extrato bancário Bradesco válido
- Verifique se o PDF não está protegido por senha
- Verifique se todas as dependências estão instaladas

### Falha na conexão WebSocket
**Erro**: Não é possível conectar ao WebSocket

**Solução**: 
- Certifique-se de que o servidor convert.py está rodando
- Verifique as configurações de firewall para a porta 8001
- Verifique se a URL do WebSocket corresponde ao endereço do seu servidor

## 📝 Notas

- Esta aplicação é especificamente projetada para **extratos bancários Bradesco** e pode não funcionar com outros formatos de banco
- A estrutura do PDF deve corresponder ao formato esperado do Bradesco
- PDFs grandes com muitas páginas podem levar mais tempo para processar

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

## 📄 Licença

Este projeto está disponível para uso no estado em que se encontra. Verifique com o proprietário do repositório os termos específicos de licenciamento.

## 👤 Autor

Alan Marinho - [Perfil no GitHub](https://github.com/alanmarinho1)

## 🔗 Repositório

[https://github.com/alanmarinho1/Mywebsocket](https://github.com/alanmarinho1/Mywebsocket)
