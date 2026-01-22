"""
Task Prompt: Create a Python program that transcribe an audio file using an online API. 
Add a summary of max 100 words of the transcript.

Recommended APIs: 
- AssemblyAI (Transcription)
- Google Gemini 2.5 Flash (Summarization)

Example Output:
-------------
Transcribing file: sample_audio.mp3
Status: completed
Transcript: Welcome to this audio transcription example...

Generating summary with Gemini (max 100 words)...
--- Summary ---
This audio discusses the history of lunar landing training...
-------------
"""

import os
import sys
import assemblyai as aai
from google import genai
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
ASSEMBLY_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not ASSEMBLY_KEY or ASSEMBLY_KEY == "your_assemblyai_key":
    print("\n[!] ERROR: AssemblyAI API Key not found in .env")
    sys.exit(1)

# Configure AssemblyAI
aai.settings.api_key = ASSEMBLY_KEY

# Configure Gemini Client
client = None
if GEMINI_KEY:
    try:
        client = genai.Client(api_key=GEMINI_KEY)
    except Exception as e:
        print(f"\n[!] ERROR configuring Gemini client: {e}")
else:
    print("\n[!] WARNING: GEMINI_API_KEY not found. Summary will be skipped.")

def transcribe_audio(audio_source):
    """
    Transcribes audio and generates a summary using Gemini.
    """
    print(f"\n--- Transcribing: {audio_source} ---")
    
    transcriber = aai.Transcriber()
    
    try:
        transcript = transcriber.transcribe(audio_source)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription failed: {transcript.error}")
            return
        
        print(f"Status: {transcript.status}")
        print("\n--- Transcript ---")
        print(transcript.text)
        print("------------------\n")
        
        with open("transcript.txt", "w") as f:
            f.write(transcript.text)
        print("Saved transcript to transcript.txt")

        # --- Summarization Logic with Gemini ---
        if not client:
            return

        print("\nGenerating summary with Gemini (at most 100 words)...")
        try:
            # Stricter prompt to ensure summary stays well under the 100-word limit
            prompt = (
                "Provide a concise summary of the following transcript. "
                "CRITICAL: The summary MUST be less than 100 words total. "
                "Aim for around 70-80 words to be safe.\n\n"
                f"Transcript:\n{transcript.text}"
            )
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            summary_text = response.text.strip()
            
            # Count words to show the user it respects the limit
            word_count = len(summary_text.split())
            
            print("\n--- Summary ---")
            print(summary_text)
            print(f"\n[Word Count: {word_count}]")
            print("------------------\n")
            
            with open("summary.txt", "w") as f:
                f.write(summary_text)
            print("Saved summary to summary.txt")

        except Exception as e:
            print(f"Could not generate summary: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Check if a file path was provided as a command line argument
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        # Default sample URL provided by AssemblyAI for testing if no local file is given
        source = "https://assembly.ai/news.mp4"
        print("No file provided. Using default sample URL...")

    transcribe_audio(source)
