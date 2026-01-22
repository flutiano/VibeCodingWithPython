"""
Task Prompt: Create a Python program that transcribe an audio file using an online API. 
Add a summary of max 100 words of the transcript.
Use Pydantic AI framework with Google Gemini.

Example Output:
-------------
Processing with Pydantic AI Agent...
--- Result ---
Transcript: [Text...]
Summary: [Summary...]
Word Count: 75
-------------
"""

import os
import sys
import time
import requests
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from google import genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
# Check for both possible names
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not GEMINI_KEY:
    print("\n[!] ERROR: API Key (GEMINI_API_KEY or GOOGLE_API_KEY) not found in .env")
    sys.exit(1)

# Pydantic AI prefers GOOGLE_API_KEY. Set it and clear the other to avoid the SDK warning.
os.environ["GOOGLE_API_KEY"] = GEMINI_KEY
os.environ.pop("GEMINI_API_KEY", None)

# 1. Define the Structured Response Model
class TranscriptionResult(BaseModel):
    """Structured response from the transcription agent."""
    transcript: str = Field(description="The full verbatim transcript of the audio.")
    summary: str = Field(description="A concise summary of the content in at most 100 words.")
    word_count: int = Field(description="The number of words in the summary.")

# 2. Setup the Model and Agent
# Using the updated GoogleModel class
model = GoogleModel('gemini-2.5-flash')
agent = Agent(
    model,
    output_type=TranscriptionResult,
    system_prompt=(
        "You are an expert transcription and summarization assistant. "
        "Your task is to transcribe content from the provided media file and summarize it. "
        "The summary MUST be under 100 words. Be concise and accurate."
    ),
)

def download_file(url):
    print(f"Downloading sample: {url}")
    local_filename = "pydantic_temp.mp4"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

async def run_transcription(source):
    # We still need the genai client for file management (Pydantic AI handles the LLM part)
    genai_client = genai.Client(api_key=GEMINI_KEY)
    
    is_temp = False
    if source.startswith("http"):
        source = download_file(source)
        is_temp = True

    try:
        print(f"Uploading {source} to Google AI...")
        uploaded_file = genai_client.files.upload(file=source)
        
        while uploaded_file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(2)
            uploaded_file = genai_client.files.get(name=uploaded_file.name)
        
        from pydantic_ai.messages import VideoUrl
        
        print("\nAgent is transcribing and summarizing...")
        
        # 3. Call the Agent with Multimodal Input
        result = await agent.run(
            [
                "Please transcribe and summarize this file verbatim.",
                VideoUrl(url=uploaded_file.uri, media_type="video/mp4")
            ]
        )

        # The result.output is an instance of TranscriptionResult!
        data = result.output
        
        print("\n--- Transcription Result (Structured) ---")
        print(f"Status: SUCCESS")
        print(f"\n--- Transcript ---\n{data.transcript[:200]}...") # Print first 200 chars
        print(f"\n--- Summary ---\n{data.summary}")
        print(f"\n[Word Count: {data.word_count}]")
        print("------------------------------------------\n")

        # Save results
        with open("pydantic_output.txt", "w") as f:
            f.write(f"TRANSCRIPT:\n{data.transcript}\n\nSUMMARY:\n{data.summary}\nWORD COUNT: {data.word_count}")
        print("Saved detailed results to pydantic_output.txt")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if is_temp and os.path.exists("pydantic_temp.mp4"):
            os.remove("pydantic_temp.mp4")

if __name__ == "__main__":
    import asyncio
    
    source = sys.argv[1] if len(sys.argv) > 1 else "https://assembly.ai/news.mp4"
    if len(sys.argv) == 1:
        print("No file provided. Using default sample URL...")
        
    asyncio.run(run_transcription(source))
