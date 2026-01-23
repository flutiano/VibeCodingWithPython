import os
import streamlit as st
import doc_processor
from dotenv import load_dotenv

# --- CONFIG & INITIALIZATION ---
load_dotenv()
st.set_page_config(page_title="Document Chat Pro", layout="wide", page_icon="💎")

# CSS for Premium Aesthetics
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #e94560;
    }
    .stSidebar {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stButton>button {
        background: linear-gradient(90deg, #e94560 0%, #950740 100%);
        color: white;
        border: none;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);
    }
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    /* Chat Bubble Styling */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- HELPERS ---
def process_documents_ui(docs, api_key):
    pdf_files = [f for f in docs if f.name.lower().endswith('.pdf')]
    epub_files = [f for f in docs if f.name.lower().endswith('.epub')]
    
    raw_text = ""
    if pdf_files: raw_text += doc_processor.extract_text_from_pdf(pdf_files)
    if epub_files: raw_text += doc_processor.extract_text_from_epub(epub_files)
    
    if not raw_text.strip():
        return False, "No text found in documents."

    chunks = doc_processor.get_text_chunks(raw_text, chunk_size=5000, chunk_overlap=500)
    doc_processor.build_vector_store(chunks, api_key, index_name="faiss_index_pro")
    return True, f"Processed {len(chunks)} text segments."

# --- MAIN UI ---
def main():
    st.title("💎 Document Chat Pro")
    
    # Sidebar for API Key
    with st.sidebar:
        st.subheader("Settings")
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            api_key = st.text_input("Enter Gemini API Key", type="password")
            if api_key: os.environ["GOOGLE_API_KEY"] = api_key
        else:
            st.success("API Key loaded (Jan 2026 Tier)")
        
        st.divider()
        st.info("Supported formats: PDF, EPUB. Using RAG for massive documents.")

    # Tabs for Organization
    tab1, tab2 = st.tabs(["💬 Chat", "📚 Knowledge Base"])

    with tab2:
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader("Upload PDF or EPUB files", accept_multiple_files=True, type=["pdf", "epub"])
        if st.button("Process & Index"):
            if not api_key:
                st.error("Please set your API key in the sidebar.")
            elif not uploaded_files:
                st.error("Please upload at least one document.")
            else:
                with st.status("Preprocessing knowledge base...", expanded=True) as status:
                    st.write("Extracting text...")
                    success, msg = process_documents_ui(uploaded_files, api_key)
                    if success:
                        status.update(label="Processing Complete!", state="complete", expanded=False)
                        st.success(msg)
                    else:
                        status.update(label="Process Failed", state="error")
                        st.error(msg)

    with tab1:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input at the bottom
        if prompt := st.chat_input("Ask a question about your documents..."):
            if not api_key:
                st.error("Set API key in sidebar.")
            elif not os.path.exists("faiss_index_pro"):
                st.error("Please process documents in the 'Knowledge Base' tab first.")
            else:
                # Add user message to history
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Generate response
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing documents..."):
                        try:
                            full_response = doc_processor.query_documents(prompt, api_key, index_name="faiss_index_pro")
                            st.markdown(full_response)
                            # Add assistant response to history
                            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

    # Auto-scroll or Footer
    st.markdown("---")
    st.caption("Powered by Gemini 2.5 & FAISS | Task 014 Redesign")

if __name__ == "__main__":
    main()
