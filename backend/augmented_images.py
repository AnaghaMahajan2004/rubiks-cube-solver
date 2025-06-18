import os
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Color labels and folders
LABELS = ['red', 'green', 'blue', 'white', 'yellow', 'orange']
INPUT_DIR = 'dataset'  # Manually labeled original dataset
AUG_DIR = 'augmented_dataset'  # Save augmented images here

# HSV hue ranges (OpenCV hue is 0–180)
COLOR_HUE_RANGES = {
    'red': [(0, 10), (160, 180)],
    'yellow': [(20, 35)],
    'green': [(35, 85)],
    'blue': [(100, 130)],
    'orange': [(15, 25)],
    'white': [(0, 180)]  # white: hue doesn't matter
}

# Augmentation settings
datagen = ImageDataGenerator(
    brightness_range=[0.7, 1.3],
    zoom_range=0.1,
    width_shift_range=0.05,
    height_shift_range=0.05,
    fill_mode='nearest'
)

# Function to check if hue matches color
def is_color_valid(hsv_img, label):
    h = hsv_img[:, :, 0]
    ranges = COLOR_HUE_RANGES[label]
    for low, high in ranges:
        if np.mean((h >= low) & (h <= high)) > 0.5:
            return True
    return False

# Augment images safely
for label in LABELS:
    src_folder = os.path.join(INPUT_DIR, label)
    dest_folder = os.path.join(AUG_DIR, label)
    os.makedirs(dest_folder, exist_ok=True)

    print(f"\n▶ Augmenting {label} images...")

    for fname in os.listdir(src_folder):
        if not fname.lower().endswith(('.jpg', '.png')):
            continue

        img_path = os.path.join(src_folder, fname)
        img = cv2.imread(img_path)
        if img is None:
            print(f"⚠️ Skipping invalid image: {fname}")
            continue

        img = cv2.resize(img, (32, 32))
        img = np.expand_dims(img, 0)  # (1, 32, 32, 3)

        saved = 0
        tries = 0
        generator = datagen.flow(img, batch_size=1)

        while saved < 10 and tries < 100:
            batch = next(generator)
            augmented = batch[0].astype(np.uint8)
            hsv = cv2.cvtColor(augmented, cv2.COLOR_BGR2HSV)

            if is_color_valid(hsv, label):
                save_path = os.path.join(dest_folder, f"{os.path.splitext(fname)[0]}_aug{saved}.jpg")
                cv2.imwrite(save_path, augmented)
                saved += 1

            tries += 1

        print(f"✅ {label}/{fname}: {saved} saved (from {tries} tries)")
