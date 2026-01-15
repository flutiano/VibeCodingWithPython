"""
Prompts:
1. Create a Python program that receives texts from the user and convert the 
   texts received to audio file using text-to-speech technology.
2. Correct the playback prompt to accept both 'yes'/'y' and 'no'/'n'.
3. Detect the language of the input text and convert it to audio using the 
   correct language profile automatically.
4. The user should be able to choose a voice (accent) for the audio file.
5. Use pyttsx3 library to offer more choices for the voice (Siri, system voices).
"""

import pyttsx3
import os

def list_voices(engine):
    """
    Returns a list of available system voices.
    """
    return engine.getProperty('voices')

def advanced_tts():
    """
    Main loop for selection of voices and text conversion using pyttsx3.
    """
    engine = pyttsx3.init()
    voices = list_voices(engine)

    print("=== Advanced Text-to-Speech (System Voices) ===")
    print(f"Detected {len(voices)} voices on your system.\n")

    # List all available voices
    print("Available Voices:")
    for i, voice in enumerate(voices): 
        print(f"{i + 1}. {voice.name} ({voice.languages[0] if voice.languages else 'Unknown'})")

    # Select Voice
    try:
        voice_choice = int(input(f"\nSelect a voice number (1-{len(voices)}): ")) - 1
        if 0 <= voice_choice < len(voices):
            selected_voice = voices[voice_choice]
            engine.setProperty('voice', selected_voice.id)
            print(f"Selected: {selected_voice.name}")
        else:
            print("Invalid choice, using default voice.")
    except ValueError:
        print("Invalid input, using default voice.")

    while True:
        text = input("\nEnter the text to speak: ").strip()
        
        if text.lower() in ['exit', 'quit']:
            break
        
        if not text:
            continue

        filename = input("Enter filename to save (e.g., 'speech.wav', leave blank to skip saving): ").strip()

        # Speak immediately
        print("Speaking...")
        engine.say(text)
        engine.runAndWait()

        # Save to file if requested
        if filename:
            if not (filename.endswith('.wav') or filename.endswith('.aiff') or filename.endswith('.mp3')):
                filename += ".wav"
            
            print(f"Saving to {filename}...")
            engine.save_to_file(text, filename)
            engine.runAndWait()
            print("Successfully saved!")

        print("\n" + "-"*30)

if __name__ == "__main__":
    advanced_tts()
