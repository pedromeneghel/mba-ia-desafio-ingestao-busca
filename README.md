# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de ingestão e busca semântica com LangChain e PostgreSQL + pgVector.

## Descrição

Este projeto implementa um sistema RAG (Retrieval-Augmented Generation) que permite:
- **Ingestão**: Processar arquivos PDF e armazená-los em um banco de dados vetorial
- **Busca Semântica**: Fazer perguntas sobre o conteúdo do PDF e receber respostas baseadas apenas nas informações contidas no documento

## Tecnologias utilizadas

- **Python 3.12**
- **LangChain**: Framework para aplicações com LLM
- **PostgreSQL + pgVector**: Banco de dados vetorial
- **OpenAI**: Embeddings (text-embedding-3-small) e LLM (gpt-4o-mini)
- **Docker & Docker Compose**: Para execução do banco de dados

## Pré-requisitos

1. Python 3.12 ou superior
2. Docker e Docker Compose
3. Chave de API da OpenAI

## Instalação

### 1. Clone o repositório e acesse a pasta

```bash
cd mba-ia-desafio-ingestao-busca
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip3 install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e adicione sua chave da OpenAI:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave:

```
OPENAI_API_KEY=sk-sua-chave-aqui
```

No arquivo existe também a seguinte variável no arquivo:

```
PDF_PATH=document.pdf
```

Ela indica onde está armazenado o PDF que será processado, quebrado em chunks e salvo no banco vetorial. Por padrão o projeto conta com um PDF exemplo e disponível no caminho indicado pela variável. Caso queira utilizar outro arquivo ou um caminho diferente, edite o valor dessa variável.

As outras variáveis já estão pré-configuradas:
- `DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag`
- `PG_VECTOR_COLLECTION_NAME=documents`
- `OPENAI_EMBEDDING_MODEL='text-embedding-3-small'`
- `OPENAI_SEARCHING_MODEL='gpt-5-nano'`

## Como Executar

### 1. Inicie o banco de dados PostgreSQL

```bash
docker compose up -d
```

Aguarde alguns segundos para o banco inicializar completamente.

### 2. Execute a ingestão do PDF

Este passo processa o PDF, divide em chunks e salva no banco vetorial:

```bash
python3 src/ingest.py
```

Você verá mensagens indicando:
- Número de páginas do PDF;
- Número de chunks criados;
- Confirmação de salvamento no banco;

### 3. Inicie o chat interativo

```bash
python3 src/chat.py
```

Agora você pode fazer perguntas sobre o conteúdo do PDF!

## Exemplos de Uso

```
Faça sua pergunta: Qual o faturamento da Empresa Alfa Energia S.A.?
RESPOSTA: O faturamento foi de R$ 227.237,24.

---

Faça sua pergunta: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Para sair do chat, digite: `sair`, `exit`, `quit` ou `q`

## Estrutura do Projeto

```
├── src/
│   ├── chat.py              # Interface CLI para interação
│   ├── ingest.py            # Script de ingestão do PDF
│   └── search.py            # Lógica de busca semântica
├── .env                     # Variáveis de ambiente (criar a partir do .env.example)
├── .env.example             # Template de variáveis de ambiente
├── .gitignore               # Arquivos e/ou pastas que não devem ser versionados
├── docker-compose.yml       # Configuração do PostgreSQL + pgVector
├── document.pdf             # PDF a ser processado
├── README.md                # Detalhamento do projeto e como utilizá-lo (este arquivo)
└── requirements.txt         # Dependências Python necessárias para executar o projeto
```

## Como Funciona

### Ingestão (ingest.py)
1. Carrega o PDF usando `PyPDFLoader`
2. Divide o texto em chunks de 1000 caracteres com overlap de 150
3. Converte cada chunk em embedding usando OpenAI (text-embedding-3-small)
4. Armazena os vetores no PostgreSQL com pgVector

### Busca (search.py)
1. Converte a pergunta do usuário em embedding
2. Busca os 10 chunks mais relevantes no banco vetorial
3. Monta um prompt com o contexto recuperado
4. Envia para o LLM (gpt-5-nano) com regras estritas
5. Retorna a resposta baseada apenas no contexto

### Chat (chat.py)
Interface CLI que permite interação com o sistema de busca.

## Troubleshooting

### Erro ao conectar ao banco de dados
- Verifique se o Docker está rodando: `docker ps`
- Reinicie o container: `docker compose restart`

### Erro de API Key
- Confirme que a chave da OpenAI está correta no arquivo `.env`
- Verifique se há créditos disponíveis na sua conta OpenAI

### Erro "collection not found"
- Execute novamente a ingestão: `python3 src/ingest.py`

## Limpeza

Para remover o banco de dados e volumes:

```bash
docker compose down -v
```
