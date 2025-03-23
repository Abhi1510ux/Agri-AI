import os
from PIL import Image
import numpy as np

# Define dataset paths
dataset_path = "dataset"
healthy_path = os.path.join(dataset_path, "Healthy")
pests_path = os.path.join(dataset_path, "Pests")

# Create folders
os.makedirs(healthy_path, exist_ok=True)
os.makedirs(pests_path, exist_ok=True)

def generate_image(file_path, color):
    """ Generate a dummy image with a solid color. """
    image = Image.new("RGB", (128, 128), color)
    image.save(file_path)

# Generate dummy images
for i in range(10):
    generate_image(os.path.join(healthy_path, f"healthy_{i}.jpg"), (0, 255, 0))  # Green for healthy
    generate_image(os.path.join(pests_path, f"pest_{i}.jpg"), (255, 0, 0))  # Red for infected

print("✅ Dummy images generated successfully!")
