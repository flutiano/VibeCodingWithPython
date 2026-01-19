"""
Task: create a Python program that can recognize what an image is

Example Output:
$ /Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/venv/bin/python3 006_image-recognition/recognizer.py 006_image-recognition/sample_image.png
Loading ResNet-50 model...
Loading image: 006_image-recognition/sample_image.png
Preprocessing image...
Running prediction...
Predictions:
1. golden retriever: 39.40%
2. flat-coated retriever: 1.24%
3. soccer ball: 0.80%
4. Greater Swiss Mountain dog: 0.78%
5. tennis ball: 0.72%
"""

import sys
import os
import torch
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import urllib.request
import json

def get_labels():
    # Download ImageNet labels
    labels_url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
    try:
        with urllib.request.urlopen(labels_url) as f:
            labels = [line.decode("utf-8").strip() for line in f.readlines()]
        return labels
    except Exception as e:
        print(f"Error downloading labels: {e}")
        return None

def recognize_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return

    print("Loading ResNet-50 model...")
    # Use ResNet-50 with default weights
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.eval()

    print(f"Loading image: {image_path}")
    img = Image.open(image_path).convert("RGB")

    print("Preprocessing image...")
    # Standard ImageNet transforms
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    input_tensor = preprocess(img)
    input_batch = input_tensor.unsqueeze(0) # Add batch dimension

    print("Running prediction...")
    with torch.no_grad():
        output = model(input_batch)

    # Convert output to probabilities
    probabilities = F.softmax(output[0], dim=0)
    
    # Get top 5
    top5_prob, top5_catid = torch.topk(probabilities, 5)

    labels = get_labels()
    if not labels:
        print("Could not load labels. Printing raw category IDs.")
        for i in range(5):
            print(f"{i+1}. Category {top5_catid[i].item()}: {top5_prob[i].item() * 100:.2f}%")
        return

    print("Predictions:")
    for i in range(5):
        category_name = labels[top5_catid[i]]
        print(f"{i+1}. {category_name}: {top5_prob[i].item() * 100:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recognizer.py <path_to_image>")
    else:
        recognize_image(sys.argv[1])
