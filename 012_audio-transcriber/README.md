# Audio Transcriber & Summarizer

A suite of three Python tools to transcribe and summarize audio/video files using state-of-the-art APIs.

## Setup

1.  **API Keys**:
    *   **AssemblyAI**: [assemblyai.com](https://www.assemblyai.com/)
    *   **Google Gemini**: [aistudio.google.com](https://aistudio.google.com/)
    *   Create a `.env` file in this directory:
        ```bash
        ASSEMBLYAI_API_KEY=your_key_here
        GEMINI_API_KEY=your_key_here
        ```

2.  **Dependencies**:
    ```bash
    ../venv/bin/python3 -m pip install -r requirements.txt
    ```

## Usage

You can run any of the following implementation patterns. All patterns support both local file paths and remote URLs.

### 1. Hybrid Version (AssemblyAI + Gemini)
Uses AssemblyAI for transcription and Gemini 2.5 Flash for summarization.
```bash
../venv/bin/python3 transcriber.py [path_or_url]
```

### 2. Google Unified Version (Gemini Only)
Uses Gemini for both transcription and summarization via the `google-genai` SDK.
```bash
../venv/bin/python3 google_transcriber.py [path_or_url]
```

### 3. Structured Agent Version (Pydantic AI)
Uses the Pydantic AI framework to enforce structured, type-safe outputs.
```bash
../venv/bin/python3 pydantic_transcriber.py [path_or_url]
```

## Features
- **Accurate Transcription**: Multi-provider support.
- **Smart Summarization**: Always under 100 words with word count validation.
- **Multimodal Support**: Works with `.mp3`, `.wav`, `.mp4`, and more.
- **Structured Data**: Pydantic models ensure valid AI responses in the third version.

## Outputs
- `transcript.txt` / `google_transcript.txt`
- `summary.txt` / `google_summary.txt`
- `pydantic_output.txt`
