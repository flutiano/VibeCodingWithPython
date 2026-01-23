# Document Chat Architecture (Task 014)

## Goal Description
Build a multi-format document chat system (PDF/EPUB) using a shared RAG (Retrieval-Augmented Generation) engine and multiple UI frontends (CLI, Basic Web UI, Premium Web UI).

## System Architecture
The project follows a modular design to separate logic from presentation:

### Core Engine (`doc_processor.py`)
- **Extraction**: Handles `pypdf` for PDFs and `ebooklib` + `BeautifulSoup` for EPUBs.
- **RAG Pipeline**: Manages text chunking, FAISS vector store creation, and semantic retrieval.
- **LLM Integration**: Uses Google's `text-embedding-004` and `gemini-2.5-flash` with modern LangChain `invoke` patterns.

### Frontends
- **CLI (`chat_pdf.py`)**: Quick command-line interface for local file interaction.
- **Premium Web UI (`chat_docs_webui-rag-redesigned.py`)**: High-aesthetic Streamlit interface with chat bubbles and tabbed workspace.

## Final Components
1. `doc_processor.py`: Shared core logic.
2. `chat_pdf.py`: CLI frontend.
3. `chat_docs_webui-rag-redesigned.py`: Premium Web frontend.
4. `requirements.txt`: Unified dependencies.
5. `README.md`: Project-wide documentation.
