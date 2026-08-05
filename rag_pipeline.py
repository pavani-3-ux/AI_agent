import os

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

PDF_PATH = "AI_Fundamentals.pdf"
CHROMA_PATH = "./chroma_db"

EMBEDDING_MODEL = "nomic-embed-text"


# ============================================================
# LOAD PDF
# ============================================================

def load_pdf():

    if not os.path.exists(PDF_PATH):

        raise FileNotFoundError(
            f"PDF not found: {PDF_PATH}"
        )

    reader = PdfReader(PDF_PATH)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.create_documents(
        [text]
    )


# ============================================================
# CREATE / LOAD VECTOR DATABASE
# ============================================================

def get_vector_database():

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    vector_db = Chroma(
        collection_name="ai_fundamentals",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )

    return vector_db


# ============================================================
# BUILD DATABASE IF EMPTY
# ============================================================

def build_database():

    vector_db = get_vector_database()

    existing_data = vector_db.get()

    if existing_data and existing_data.get("ids"):

        return vector_db

    print("Creating PDF knowledge database...")

    text = load_pdf()

    if not text.strip():

        raise ValueError(
            "No readable text found in the PDF."
        )

    documents = create_chunks(text)

    vector_db.add_documents(
        documents
    )

    print(
        f"PDF indexed successfully: "
        f"{len(documents)} chunks"
    )

    return vector_db


# ============================================================
# RAG TOOL
# ============================================================

@tool
def search_pdf(query: str) -> str:
    """
    Search the AI_Fundamentals.pdf knowledge base.

    Use this tool when the user asks a question that
    should be answered using information from the PDF.
    """

    try:

        vector_db = build_database()

        results = vector_db.similarity_search(
            query,
            k=4
        )

        if not results:

            return "No relevant information found in the PDF."

        formatted_results = []

        for index, document in enumerate(
            results,
            start=1
        ):

            formatted_results.append(
                f"Source {index}:\n"
                f"{document.page_content}"
            )

        return "\n\n---\n\n".join(
            formatted_results
        )

    except Exception as error:

        return (
            f"PDF search failed: {error}"
        )