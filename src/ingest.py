import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

def ingest_pdf():
    """
    Lê o PDF, divide em chunks e salva no banco de dados PostgreSQL com pgVector.
    """
    print(f"Iniciando ingestão do PDF: {PDF_PATH}.")

    # 1. Carregar o PDF
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"PDF carregado com {len(documents)} páginas.")

    # 2. Dividir em chunks de 1000 caracteres com overlap de 150
    content_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False
    )
    chunks = content_splitter.split_documents(documents)
    print(f"Documento dividido em {len(chunks)} chunks.")

    # 3. Criar embeddings e salvar no banco
    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model=OPENAI_EMBEDDING_MODEL
    )

    print("Criando embeddings e salvando no banco de dados.")
    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True
    )

    print("Ingestão concluída com sucesso!")
    print(f"Total de {len(chunks)} chunks salvos no banco de dados.")


if __name__ == "__main__":
    ingest_pdf()
