import pyttsx3
import os
import time

def test_save():
    engine = pyttsx3.init()
    text = "This is a test to see if saving works correctly on this system."
    filename = "test_output.aiff"
    
    if os.path.exists(filename):
        os.remove(filename)
        
    print(f"Saving to {filename}...")
    engine.save_to_file(text, filename)
    engine.runAndWait()
    
    time.sleep(1) # Wait for flush
    
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"File created. Size: {size} bytes")
    else:
        print("File NOT created.")

if __name__ == "__main__":
    test_save()
