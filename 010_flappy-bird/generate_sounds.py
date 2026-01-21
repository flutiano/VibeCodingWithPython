import wave
import struct
import math
import os

def generate_wave(filename, duration, volume=0.5, func=None):
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    with wave.open(filename, 'w') as f:
        f.setnchannels(1) # mono
        f.setsampwidth(2) # 16-bit
        f.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            sample = func(t, i) if func else 0
            
            # Simple envelope to avoid clicks at start/end
            envelope = 1.0
            if i < 1000:
                envelope = i / 1000.0
            elif i > num_samples - 1000:
                envelope = (num_samples - i) / 1000.0
                
            value = int(sample * volume * envelope * 32767)
            # Clip value to valid range
            value = max(-32768, min(32767, value))
            f.writeframesraw(struct.pack('<h', value))

def generate_beep(filename, frequency, duration, volume=0.5, type='sine'):
    def beep_func(t, i):
        if type == 'sine':
            return math.sin(2.0 * math.pi * frequency * t)
        elif type == 'square':
            return 1.0 if math.sin(2.0 * math.pi * frequency * t) > 0 else -1.0
        return 0
    generate_wave(filename, duration, volume, beep_func)

def generate_music(filename, duration=4.0, volume=0.2):
    def music_func(t, i):
        # A simple rhythmic loop
        # Base beat (every 0.5s)
        beat = (i % 22050) / 22050.0
        kick = math.exp(-beat * 10) * math.sin(2.0 * math.pi * 60 * t)
        
        # Melody (simple arpeggio)
        notes = [440, 554, 659, 880] # A major
        note_idx = int(t * 4) % len(notes)
        freq = notes[note_idx]
        melody = 0.5 * math.sin(2.0 * math.pi * freq * t)
        
        return kick + melody
    
    generate_wave(filename, duration, volume, music_func)

# Ensure directory exists
os.makedirs('010_flappy-bird/assets', exist_ok=True)

# Generate sounds
generate_beep('010_flappy-bird/assets/flap.wav', 440, 0.1, volume=0.3)
generate_beep('010_flappy-bird/assets/score.wav', 880, 0.15, volume=0.4)
generate_beep('010_flappy-bird/assets/crash.wav', 110, 0.4, volume=0.5, type='square')
generate_beep('010_flappy-bird/assets/select.wav', 660, 0.1, volume=0.3)
generate_music('010_flappy-bird/assets/music.wav', duration=4.0, volume=0.15)

print("Generated sounds and music in 010_flappy-bird/assets/")
