# Implementation Plan - Task 012: Audio Transcriber

## Goal
Create a Python program that transcribes audio files and generates a concise summary (max 100 words) using online APIs.

## Requirements
- Support local audio files and remote URLs.
- Securely handle API keys for multiple providers (AssemblyAI and Google).
- Export transcription and summary to text files.
- Provide multiple implementation patterns:
    1.  Hybrid (AssemblyAI + Gemini)
    2.  Google SDK only (Gemini for both)
    3.  Structured Agent (Pydantic AI)

## Tech StackV
- **Python 3.12**
- **AssemblyAI SDK**: For high-accuracy transcription.
- **google-genai**: For Gemini 2.5 Flash transcription and summarization.
- **pydantic-ai**: For structured agent-based workflow.
- **python-dotenv**: For API key management.
- **requests**: For handling file downloads.

## Components
1.  **`transcriber.py`**: The original hybrid solution. Uses AssemblyAI's robust transcription model combined with Gemini's summarization.
2.  **`google_transcriber.py`**: A unified Google-only solution. Demonstrates Gemini's multimodal ability to transcribe files directly from the Cloud Files API.
3.  **`pydantic_transcriber.py`**: A modern, type-safe implementation using Pydantic AI. Enforces structured output via a Pydantic model.

## Final Steps
1.  **Dependency Alignment**: Consolidation of all libraries into `requirements.txt`.
2.  **Secret Management**: Single `.env` supporting both `ASSEMBLYAI_API_KEY` and `GEMINI_API_KEY`.
3.  **Documentation**: README updated with usage for all patterns.
