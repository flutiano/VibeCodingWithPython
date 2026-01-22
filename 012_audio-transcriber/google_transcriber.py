"""
Task Prompt: Create a Python program that transcribe an audio file using an online API. 
Add a summary of max 100 words of the transcript.
Use only Google APIs for both.

Example Output:
-------------
Uploading file to Google AI...
Processing...
Status: COMPLETED

--- Transcript ---
[Transcript text here...]

Generating summary (at most 100 words)...
--- Summary ---
[Summary text here...]
[Word Count: xx]
-------------
"""

import os
import sys
import time
import requests
from google import genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_KEY:
    print("\n[!] ERROR: GEMINI_API_KEY not found in .env")
    sys.exit(1)

# Configure Gemini Client
client = genai.Client(api_key=GEMINI_KEY)

def download_file(url):
    """Downloads a file from a URL to a local temporary file."""
    print(f"Downloading sample file: {url}")
    local_filename = "temp_audio.mp4"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def transcribe_with_google(source):
    """
    Transcribes and summarizes an audio/video file using Google Gemini 2.5 Flash.
    """
    is_temp = False
    
    # Handle URLs by downloading first
    if source.startswith("http"):
        source = download_file(source)
        is_temp = True

    if not os.path.exists(source):
        print(f"[!] ERROR: File not found: {source}")
        return

    try:
        print(f"Uploading {source} to Google AI...")
        # Upload the file - the argument is 'file', not 'path'
        uploaded_file = client.files.upload(file=source)
        
        # Wait for processing to complete
        print("Processing file", end="", flush=True)
        while uploaded_file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)
        
        if uploaded_file.state.name == "FAILED":
            print(f"\n[!] File processing failed: {uploaded_file.state}")
            return
        
        print("\nTranscription & Summarization in progress...")

        # Step 1: Transcription
        # We ask Gemini to transcribe the uploaded file
        trans_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                uploaded_file,
                "Transcribe the audio in this file exactly. Just provide the transcript text."
            ]
        )
        
        transcript_text = trans_response.text.strip()
        print("\n--- Transcript ---")
        print(transcript_text)
        print("------------------\n")
        
        with open("google_transcript.txt", "w") as f:
            f.write(transcript_text)
        print("Saved transcript to google_transcript.txt")

        # Step 2: Summarization (using the generated transcript for precision)
        print("\nGenerating summary (at most 100 words)...")
        summary_prompt = (
            "Summarize the following transcript in at most 100 words. "
            "Stay well under the limit (target 70-80 words).\n\n"
            f"Transcript:\n{transcript_text}"
        )
        
        sum_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=summary_prompt
        )
        
        summary_text = sum_response.text.strip()
        word_count = len(summary_text.split())
        
        print("\n--- Summary ---")
        print(summary_text)
        print(f"\n[Word Count: {word_count}]")
        print("------------------\n")
        
        with open("google_summary.txt", "w") as f:
            f.write(summary_text)
        print("Saved summary to google_summary.txt")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Cleanup temp file if we downloaded it
        if is_temp and os.path.exists("temp_audio.mp4"):
            os.remove("temp_audio.mp4")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        source = "https://assembly.ai/news.mp4"
        print("No file provided. Using default sample URL...")

    transcribe_with_google(source)
