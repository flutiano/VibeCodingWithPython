"""
Prompts:
1. Create a Python program that receives texts from the user and convert the 
   texts received to audio file using text-to-speech technology.
2. Correct the playback prompt to accept both 'yes'/'y' and 'no'/'n'.
3. Detect the language of the input text and convert it to audio using the 
   correct language profile automatically.
"""

import os
from gtts import gTTS
from langdetect import detect, DetectorFactory
import platform
import subprocess

# Ensure consistent results for language detection
DetectorFactory.seed = 0

def text_to_speech():
    """
    Main function to get text from user and convert it to speech.
    """
    print("=== Text-to-Speech Converter ===")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        # Get text input from user
        text = input("Enter the text you want to convert to audio: ").strip()

        if text.lower() in ['exit', 'quit']:
            break
        
        if not text:
            print("Please enter some text.")
            continue

        # Get filename input from user (with a default)
        filename = input("Enter a filename for the MP3 (default: 'output.mp3'): ").strip()
        if not filename:
            filename = "output.mp3"
        
        # Ensure it has the .mp3 extension
        if not filename.endswith('.mp3'):
            filename += ".mp3"

        print(f"Converting text to audio...")

        try:
            # Detect language
            try:
                detected_lang = detect(text)
                print(f"Detected language: {detected_lang}")
            except Exception:
                print("Could not detect language, defaulting to English.")
                detected_lang = 'en'

            # Voice/Accent Selection for English
            tld = 'com'  # Default (US)
            if detected_lang == 'en':
                print("\nChoose an English Accent (Voice):")
                accents = {
                    '1': ('United States', 'com'),
                    '2': ('United Kingdom', 'co.uk'),
                    '3': ('Australia', 'com.au'),
                    '4': ('India', 'co.in'),
                    '5': ('Canada', 'ca'),
                    '6': ('Ireland', 'ie')
                }
                for key, val in accents.items():
                    print(f"{key}. {val[0]}")
                
                choice = input("Select an accent (1-6, default: 1): ").strip()
                if choice in accents:
                    tld = accents[choice][1]
                    print(f"Selected: {accents[choice][0]}")
                else:
                    print("Using default: United States")

            # Create the TTS object with the selected TLD
            tts = gTTS(text=text, lang=detected_lang, tld=tld)
            
            # Save the speech to a file
            tts.save(filename)
            
            print(f"Successfully saved to '{filename}'!")

            # Ask if the user wants to play the file
            play_choice = input("Would you like to play the audio now? (y/n): ").strip().lower()
            if play_choice in ['y', 'yes']:
                play_audio(filename)
            elif play_choice in ['n', 'no']:
                print("Skipping playback.")
            else:
                print("Invalid input, skipping playback.")

        except Exception as e:
            print(f"An error occurred: {e}")
        
        print("-" * 30)

def play_audio(filename):
    """
    Plays the audio file using the system's default player.
    """
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filename])
        elif platform.system() == "Windows":
            os.startfile(filename)
        else:  # Linux (usually 'xdg-open')
            subprocess.run(["xdg-open", filename])
    except Exception as e:
        print(f"Could not play the audio automatically: {e}")

if __name__ == "__main__":
    text_to_speech()
