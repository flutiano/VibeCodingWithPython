"""
Prompts:
1. Create a Python program that receives texts from the user and convert the 
   texts received to audio file using text-to-speech technology.
2. Correct the playback prompt to accept both 'yes'/'y' and 'no'/'n'.
3. Detect the language of the input text and convert it to audio using the 
   correct language profile automatically.
4. The user should be able to choose a voice (accent) for the audio file.
5. Use pyttsx3 library to offer more choices for the voice (Siri, system voices).
6. Please save the converted audio file to mp3, not wav.
"""

import pyttsx3
import os
import subprocess
import time

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

        # Save to file or just speak
        if filename:
            if not filename.endswith('.mp3'):
                filename += ".mp3"
            
            temp_audio = "temp_output.aiff" # Native format for macOS
            if os.path.exists(temp_audio):
                os.remove(temp_audio)

            print(f"Generating audio file...")
            engine.save_to_file(text, temp_audio)
            engine.runAndWait()

            # Wait a moment for the file to be fully written
            time.sleep(1.0)

            if os.path.exists(temp_audio) and os.path.getsize(temp_audio) > 1000:
                print(f"Converting to MP3 via ffmpeg...")
                try:
                    # Use ffmpeg to convert aiff to mp3
                    subprocess.run([
                        "ffmpeg", "-y", "-i", temp_audio, 
                        "-codec:a", "libmp3lame", "-qscale:a", "2", 
                        filename
                    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    print(f"Successfully saved to '{filename}'!")
                    os.remove(temp_audio)
                except Exception as e:
                    print(f"Conversion failed: {e}")
            else:
                print("Error: Audio generation failed or file too small.")
        else:
            # Just speak if no filename provided
            print("Speaking...")
            engine.say(text)
            engine.runAndWait()

        print("\n" + "-"*30)

if __name__ == "__main__":
    advanced_tts()
