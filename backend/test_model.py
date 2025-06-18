import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load your trained model
model = load_model('backend/model/color_classifier_improved.keras')

# Mapping of classes
color_map = {
    0: 'Red',
    1: 'Green',
    2: 'Blue',
    3: 'White',
    4: 'Yellow',
    5: 'Orange'
}

# Path to test images
TEST_IMAGES = {
    'White': 'test/white.jpg',
    'Yellow': 'test/yellow.jpg',
    'Blue': 'test/blue.jpg',
    'Green': 'test/green.jpg',
    'Red': 'test/red.jpg',
    'Orange': 'test/orange.jpg'
}

# Function to center-crop the image to a square
def center_crop(image):
    h, w, _ = image.shape
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    cropped = image[start_y:start_y + min_dim, start_x:start_x + min_dim]
    return cropped

# Loop through each test image
for label, path in TEST_IMAGES.items():
    img = cv2.imread(path)
    if img is None:
        print(f"❌ Image not found: {path}")
        continue

    img = center_crop(img)
    img = cv2.resize(img, (150, 150))  # Match model's input size
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img, verbose=0)
    predicted_class = np.argmax(prediction)
    predicted_label = color_map[predicted_class]
    confidence = np.max(prediction)

    print(f"✅ Image: {label} → Predicted: {predicted_label} (Confidence: {confidence:.2f})")

