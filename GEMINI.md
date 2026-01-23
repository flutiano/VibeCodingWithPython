# Project: VibeCodingWithPython

This repository is dedicated to "Vibe Coding" practice—using AI agents to quickly iterate on functional Python tools.

## AI Agent Context & Guidelines

### Environment
- **Python Version**: Python 3.12
- **Virtual Environment**: Located at `./venv`
- **Dependency Management**: Use `./venv/bin/python3 -m pip install` for installations.
- **Running Scripts**: Use the absolute path to the venv python: `/Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/venv/bin/python3`

### Governance Rules

#### Task Organization
1. **Directory Structure**: Every new task must have its own subdirectory.
2. **Naming Convention**: The task number must be prepended to the subdirectory name (e.g., `005_task-name`).

#### Source Code Standards
1. **Task Prompts**: The original prompt for each task must be added to the generated source code as a comment at the top of the main file.
2. **Example Outputs**: If the task produces outputs (e.g., console output, generated files), include an example of the output as a comment in the source code.
3. **Dependencies**: A `requirements.txt` file must be created in the task directory listing all specific Python dependencies for that task.

#### Documentation
1. **Implementation Plan**: Upon task completion, save the final implementation plan as `Plan.md` in the task directory.
2. **Walkthrough**: Upon task completion, save the final walkthrough as `README.md` in the task directory.

## Current Project Structure
- `000_hello-world`: Initial setup
- `001_youtube-downloader`: Video download tool
- `002_bitcoin-price`: Market data fetching
- `003_wikipedia_search`: Information retrieval
- `004_text-to-speech`: Audio generation
- `005_email-sender`: SMTP email automation
- `006_image-recognition`: AI-powered image classification
- `007_personal-website`: Personal website with Flask
- `008_personal-website-enhanced`: Improved website with Theme Switcher
- `009_pythonanywhere-deployment`: Cloud deployment to PythonAnywhere
- `010_flappy-bird`: Flappy Bird game with Pygame
- `011_flappy-bird-refactored`: Refactored Flappy Bird with base class extraction
- `012_audio-transcriber`: Audio transcription and summarization (AssemblyAI, Google, Pydantic AI)
- `013_stock-alert-bot`: Multi-platform market data alerts (Discord & Telegram)
- `014_chat-with-documents`: Advanced Chat with PDF/EPUB using RAG and shared core logic.
