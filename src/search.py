import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
OPENAI_SEARCHING_MODEL = os.getenv("OPENAI_SEARCHING_MODEL")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    """
    Cria uma chain de busca semântica com LangChain.
    Retorna uma chain que pode ser invocada com uma pergunta.
    """
    # Cria embeddings da pergunta
    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model=OPENAI_EMBEDDING_MODEL
    )

    # Conecta ao vector_store
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )

    # Inicia o modelo de LLM
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_SEARCHING_MODEL,
        temperature=0
    )

    # Cria o prompt template
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # Função para realizar busca com score e formatar documentos
    def retrieve_and_format(query):
        docs_with_scores = vector_store.similarity_search_with_score(query, k=10)
        return "\n\n".join([doc.page_content for doc, _ in docs_with_scores])

    # Cria a que vai fazer a busca na base de dados e responder a pergunta
    chain = (
        {
            "contexto": retrieve_and_format,
            "pergunta": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
