"""
Task: 014_chat-with-documents
Goal: CLI version of the PDF Chat bot using shared RAG logic.
"""

import os
import doc_processor
from dotenv import load_dotenv

load_dotenv()

def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in environment.")
        return

    print("--- 📄 PDF/EPUB CLI Chat Pro ---")
    file_path = input("Enter the path to your document (PDF or EPUB): ").strip()
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    # Process based on extension
    print("Processing document...")
    raw_text = ""
    if file_path.lower().endswith('.pdf'):
        with open(file_path, "rb") as f:
            raw_text = doc_processor.extract_text_from_pdf([f])
    elif file_path.lower().endswith('.epub'):
        with open(file_path, "rb") as f:
            raw_text = doc_processor.extract_text_from_epub([f])
    else:
        print("Error: Unsupported file format. Please use PDF or EPUB.")
        return

    if not raw_text.strip():
        print("Error: Could not extract text from document.")
        return

    # Build vector store
    chunks = doc_processor.get_text_chunks(raw_text)
    doc_processor.build_vector_store(chunks, api_key, index_name="faiss_index_cli")
    print(f"Index built with {len(chunks)} chunks.")

    print("\n--- Chat Started (Type 'quit' to exit) ---")
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ['quit', 'exit', 'q']:
            break
        
        try:
            response = doc_processor.query_documents(user_query, api_key, index_name="faiss_index_cli")
            print(f"Bot: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
