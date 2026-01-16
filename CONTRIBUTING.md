# Contribuindo para o Bradesco PDF to Excel Converter

Obrigado por considerar contribuir com este projeto! Este documento fornece diretrizes para contribuição.

## Índice

1. [Código de Conduta](#código-de-conduta)
2. [Como Posso Contribuir?](#como-posso-contribuir)
3. [Configuração do Ambiente de Desenvolvimento](#configuração-do-ambiente-de-desenvolvimento)
4. [Padrões de Código](#padrões-de-código)
5. [Enviando Alterações](#enviando-alterações)
6. [Reportando Bugs](#reportando-bugs)
7. [Sugerindo Melhorias](#sugerindo-melhorias)

---

## Código de Conduta

Este projeto tem como objetivo ser acolhedor e inclusivo. Por favor, seja respeitoso e atencioso ao interagir com outras pessoas.

### Nossos Padrões

- Usar linguagem acolhedora e inclusiva
- Ser respeitoso com diferentes pontos de vista e experiências
- Aceitar críticas construtivas com elegância
- Focar no que é melhor para a comunidade
- Demonstrar empatia com outros membros da comunidade

---

## Como Posso Contribuir?

### Reportando Bugs

Se você encontrar um bug, por favor crie uma issue com:

1. **Título claro**: Descreva o problema brevemente
2. **Descrição**: Explicação detalhada do bug
3. **Passos para reproduzir**: Como reproduzir o problema
4. **Comportamento esperado**: O que deveria acontecer
5. **Comportamento atual**: O que realmente acontece
6. **Ambiente**: SO, versão do Python, etc.
7. **Capturas de tela**: Se aplicável

**Exemplo**:
```
Título: PDF com caracteres especiais falha ao converter

Descrição:
Ao fazer upload de um PDF que contém caracteres especiais (ç, ã, õ),
a conversão falha com um erro de codificação.

Passos para Reproduzir:
1. Iniciar o servidor
2. Fazer upload de PDF com caracteres especiais
3. Clicar em converter

Esperado: PDF converte com sucesso
Atual: Erro 500 com exceção de codificação

Ambiente:
- SO: Ubuntu 22.04
- Python: 3.10.5
- Navegador: Chrome 120
```

### Sugerindo Melhorias

Sugestões de melhorias são bem-vindas! Por favor, crie uma issue com:

1. **Caso de uso**: Por que esta melhoria é necessária?
2. **Solução proposta**: Como deveria funcionar?
3. **Alternativas**: Alguma abordagem alternativa?
4. **Contexto adicional**: Capturas de tela, mockups, etc.

### Pull Requests

Pull requests são sempre bem-vindos! Veja [Enviando Alterações](#enviando-alterações) abaixo.

---

## Configuração do Ambiente de Desenvolvimento

### 1. Fork e Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/Mywebsocket.git
cd Mywebsocket
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv

# Activate
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt

# Install development dependencies (if added)
pip install pytest black flake8 mypy
```

### 4. Criar um Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 5. Fazer Suas Alterações

Edite o código, adicione testes, atualize a documentação.

### 6. Testar Suas Alterações

```bash
# Run the server
uvicorn main:app --reload

# Test manually or with scripts
python -m pytest  # If tests exist
```

---

## Padrões de Código

### Estilo Python

- Siga o guia de estilo [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 espaços para indentação (sem tabs)
- Comprimento máximo de linha: 88 caracteres (padrão do Black)
- Use nomes de variáveis descritivos

### Formatação de Código

Use Black para formatação:

```bash
pip install black
black .
```

### Linting

Use flake8 para linting:

```bash
pip install flake8
flake8 . --max-line-length=88 --extend-ignore=E203
```

### Type Hints

Adicione type hints sempre que possível:

```python
def convert_pdf(filename: str) -> bytes:
    """Convert PDF to Excel"""
    pass
```

### Documentação

- Adicione docstrings às funções e classes
- Atualize o README.md ao adicionar recursos
- Adicione exemplos ao EXAMPLES.md se aplicável
- Atualize o TECHNICAL.md para mudanças de arquitetura

**Exemplo de Docstring**:
```python
def process_page(df: pd.DataFrame, page_num: int) -> pd.DataFrame:
    """
    Process a single page of the bank statement.
    
    Args:
        df: DataFrame containing extracted table data
        page_num: Page number (1-indexed)
    
    Returns:
        Cleaned and formatted DataFrame
    
    Raises:
        ValueError: If DataFrame is empty or invalid
    """
    pass
```

### Comentários

- Escreva comentários para lógica complexa
- Evite comentários óbvios
- Use português para termos específicos do domínio quando apropriado
- Use inglês para termos técnicos

---

## Enviando Alterações

### Antes de Enviar

1. **Teste suas alterações**: Garanta que tudo funciona
2. **Atualize a documentação**: Se você alterou funcionalidades
3. **Adicione exemplos**: Se você adicionou novos recursos
4. **Formate o código**: Execute Black e flake8
5. **Mensagem de commit**: Escreva mensagens de commit claras

### Mensagens de Commit

Siga o formato de commits convencionais:

```
type(scope): brief description

Longer description if needed

Fixes #123
```

**Tipos**:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Alterações de estilo de código (formatação)
- `refactor`: Refatoração de código
- `test`: Adição ou atualização de testes
- `chore`: Tarefas de manutenção

**Exemplos**:
```
feat(converter): adiciona suporte para extratos multi-coluna

fix(helpers): trata linhas vazias corretamente

docs(readme): atualiza instruções de instalação

refactor(convert): simplifica lógica de detecção de página
```

### Processo de Pull Request

1. **Envie para seu fork**:
```bash
git push origin feature/your-feature-name
```

2. **Crie um Pull Request no GitHub**:
   - Vá para o repositório original
   - Clique em "New Pull Request"
   - Selecione seu fork e branch
   - Preencha o template

3. **Descrição do PR** deve incluir:
   - Quais alterações foram feitas
   - Por que as alterações eram necessárias
   - Como testar as alterações
   - Issues relacionadas (se houver)

**Exemplo de Descrição de PR**:
```markdown
## Descrição
Adicionado suporte para extratos bancários com múltiplas contas no mesmo PDF.

## Alterações
- Modificado `convert.py` para detectar mudanças de conta
- Atualizado `helpers.py` para lidar com dados de múltiplas contas
- Adicionada nova função `split_by_account()`

## Testes
1. Fazer upload do arquivo de teste `multi_account_statement.pdf`
2. Verificar se a saída tem planilhas separadas para cada conta
3. Verificar a integridade dos dados para cada conta

## Issues Relacionadas
Fixes #42
```

4. **Aguarde Revisão**:
   - Responda a qualquer feedback
   - Faça as alterações solicitadas
   - Atualize o PR

5. **Merge**:
   - Uma vez aprovado, o mantenedor fará o merge
   - Delete seu branch após o merge

---

## Reportando Bugs

### Problemas de Segurança

**Não** abra issues públicas para vulnerabilidades de segurança. Em vez disso:
- Envie um email diretamente ao mantenedor
- Forneça informações detalhadas
- Aguarde resposta antes de divulgar

### Relatórios de Bug

Use o template de issue:

```markdown
**Descreva o bug**
Uma descrição clara do que é o bug.

**Para Reproduzir**
Passos para reproduzir:
1. Vá para '...'
2. Clique em '...'
3. Veja o erro

**Comportamento esperado**
O que você esperava que acontecesse.

**Capturas de tela**
Se aplicável, adicione capturas de tela.

**Ambiente:**
 - SO: [ex: Ubuntu 22.04]
 - Versão do Python: [ex: 3.10.5]
 - Navegador: [ex: Chrome 120]

**Contexto adicional**
Qualquer outro contexto sobre o problema.
```

---

## Sugerindo Melhorias

### Solicitações de Recursos

Use este template:

```markdown
**Sua solicitação de recurso está relacionada a um problema?**
Uma descrição clara do problema.

**Descreva a solução que você gostaria**
Uma descrição clara do que você quer que aconteça.

**Descreva alternativas que você considerou**
Soluções ou recursos alternativos que você considerou.

**Contexto adicional**
Capturas de tela, mockups, exemplos, etc.
```

### Ideias de Melhorias

Algumas áreas onde contribuições seriam valiosas:

1. **Suporte Multi-Banco**: Adicionar suporte para outros bancos brasileiros
2. **Tratamento de Erros Melhorado**: Mensagens de erro melhores e recuperação
3. **Barra de Progresso**: Implementar rastreamento de progresso no cliente
4. **Autenticação**: Adicionar autenticação de usuário
5. **Banco de Dados**: Armazenar histórico de conversões
6. **Testes**: Adicionar conjunto abrangente de testes
7. **Docker**: Criar imagem Docker
8. **Documentação da API**: Adicionar documentação Swagger/OpenAPI
9. **Internacionalização**: Adicionar traduções em inglês
10. **Performance**: Otimizar para PDFs grandes

---

## Diretrizes de Desenvolvimento

### Adicionando Novos Recursos

1. **Discuta primeiro**: Crie uma issue para discutir o recurso
2. **Mantenha o foco**: Um recurso por PR
3. **Mantenha compatibilidade**: Não quebre funcionalidades existentes
4. **Adicione testes**: Se adicionar infraestrutura de testes
5. **Documente**: Atualize toda a documentação relevante

### Corrigindo Bugs

1. **Reproduza primeiro**: Garanta que você consegue reproduzir o bug
2. **Correção mínima**: Faça a menor alteração que o corrija
3. **Adicione teste**: Previna regressão
4. **Documente**: Atualize a documentação se o comportamento mudou

### Melhorando a Documentação

1. **Clareza**: Torne fácil de entender
2. **Exemplos**: Adicione exemplos práticos
3. **Completude**: Cubra todos os aspectos
4. **Precisão**: Garanta que a informação está correta
5. **Formatação**: Siga as melhores práticas de markdown

---

## Dúvidas?

Se você tiver dúvidas sobre como contribuir:

1. Verifique a documentação existente
2. Pesquise issues existentes
3. Crie uma nova issue com a label "question"
4. Seja específico e forneça contexto

---

## Reconhecimento

Contribuidores serão reconhecidos em:
- Página de contribuidores do GitHub
- Notas de lançamento (para contribuições significativas)
- Menções especiais para recursos importantes

Obrigado por contribuir! 🎉
