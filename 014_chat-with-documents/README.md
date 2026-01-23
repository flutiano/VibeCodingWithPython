# Chat with PDF (CLI & Web UI with RAG)

This task implements two versions of a PDF chat assistant powered by Google Gemini 3 (using the stable `gemini-2.5-flash` model for 2026).

## Versions

### 1. Simple CLI Version (`chat_pdf.py`)
- **Method**: Context Stuffing.
- **Best for**: Small to medium-sized PDFs (< 50 pages).
- **Usage**: `python 014_chat-with-documents/chat_pdf.py`

### 2. Pro Web UI Version (`chat_pdf_webui-RAG.py`)
- **Method**: **RAG (Retrieval-Augmented Generation)**.
- **UI**: Streamlit.
- **Vector Store**: FAISS.
- **Formats**: **PDF** and **EPUB**.
- **Best for**: Large documents, multiple files, and cross-format semantic search.
### 3. Redesigned Pro Web UI (`chat_docs_webui-rag-redesigned.py`)
- **Aesthetics**: Premium UI with glassmorphism, gradients, and custom CSS.
- **Modern UI**: Uses `st.chat_message` for bubbles and `st.chat_input` for a fixed input bar.
- **Fixed Code**: Uses modern LangChain `invoke` and `create_stuff_documents_chain` (no deprecation warnings).
- **Features**: Persistent session state history and a tabbed interface ("Chat" vs "Knowledge Base").
- **Usage**: `streamlit run 014_chat-with-documents/chat_docs_webui-rag-redesigned.py`

## Architecture & Core Logic
The project is refactored for modularity:
- **`doc_processor.py`**: The central engine. It handles PDF/EPUB extraction, chunking, FAISS indexing, and retrieval-augmented generation. 
- **Frontends**: All UI versions (CLI, Basic Web UI, and Redesigned Web UI) call this shared module for document processing.

### Key Logic
1. **Extraction**: `pypdf` (PDF) and `ebooklib` + `BeautifulSoup` (EPUB) extract raw text.
2. **Chunking**: `RecursiveCharacterTextSplitter` breaks text into chunks (5k-10k characters).
3. **Indexing**: `text-embedding-004` generates semantic vectors stored in local **FAISS** indices.
4. **Generation**: **Gemini 2.5 Flash** generates answers using `create_stuff_documents_chain` and the modern `.invoke()` pattern.

## Setup
1. Install dependencies: `pip install -r 014_chat-with-documents/requirements.txt`
2. Configure `.env`: Add `GOOGLE_API_KEY=your_key`
3. Launch: Use the streamlit command above.

## Example Output
```text
(User) > What is the secret code?
(Bot) > The secret code mentioned in the document is VIBE-2026.
```
