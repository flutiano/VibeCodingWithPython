from PIL import Image
import os

def process_bird_image(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    img = Image.open(filepath).convert("RGBA")
    
    # 1. Flip horizontally
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    # 2. Make white background transparent
    datas = img.getdata()
    newData = []
    
    for item in datas:
        # If the pixel is white or very close to white, make it transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
            
    img.putdata(newData)
    
    # Save back
    img.save(filepath, "PNG")
    print(f"Processed and saved: {filepath}")

if __name__ == "__main__":
    process_bird_image("010_flappy-bird/assets/bird.png")
