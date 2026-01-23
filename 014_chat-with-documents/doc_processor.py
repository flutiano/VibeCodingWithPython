import os
from pypdf import PdfReader
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

def extract_text_from_pdf(pdf_files):
    """Extracts text from a list of PDF file-like objects."""
    text = ""
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_epub(epub_files):
    """Extracts text from a list of EPUB file-like objects."""
    text = ""
    for epub_file in epub_files:
        book = epub.read_epub(epub_file)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text += soup.get_text() + "\n"
    return text

def get_text_chunks(text, chunk_size=10000, chunk_overlap=1000):
    """Splits text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)

def build_vector_store(chunks, api_key, index_name="faiss_index"):
    """Creates and saves a FAISS vector store from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local(index_name)
    return True

def query_documents(question, api_key, index_name="faiss_index"):
    """Retrieves relevant chunks and generates an answer using Gemini."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
    
    # Load vector store
    if not os.path.exists(index_name):
        raise FileNotFoundError("Vector index not found. Please process documents first.")
        
    vector_db = FAISS.load_local(index_name, embeddings, allow_dangerous_deserialization=True)
    docs = vector_db.similarity_search(question, k=4)

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.3)
    
    # Modern Prompt & Chain
    prompt = ChatPromptTemplate.from_template("""
    Answer the question as detailed as possible from the provided context. 
    If the answer is not in the context, just say: "The answer is not available in the context." 
    Do not provide incorrect information.

    Context:
    {context}

    Question: 
    {input}
    """)

    document_chain = create_stuff_documents_chain(llm, prompt)
    response = document_chain.invoke({
        "input": question,
        "context": docs
    })
    
    return response
