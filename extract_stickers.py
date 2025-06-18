import cv2
import os

# Paths
RAW_FOLDER = "raw_images"
SAVE_FOLDER = "dataset"
LABELS = ['red', 'green', 'blue', 'white', 'yellow', 'orange']

# Create label folders if they don't exist
for label in LABELS:
    os.makedirs(os.path.join(SAVE_FOLDER, label), exist_ok=True)

def crop_stickers(img):
    h, w, _ = img.shape
    grid_h, grid_w = h // 3, w // 3
    stickers = []

    for i in range(3):
        for j in range(3):
            y1 = i * grid_h
            y2 = (i + 1) * grid_h
            x1 = j * grid_w
            x2 = (j + 1) * grid_w
            sticker = img[y1:y2, x1:x2]
            stickers.append(sticker)
    return stickers

def label_and_save(stickers, image_index):
    for i, sticker in enumerate(stickers):
        resized = cv2.resize(sticker, (32, 32))
        cv2.imshow("Sticker", resized)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if key == 27:  # ESC to quit
            print("Aborted.")
            return

        # Convert key to label
        try:
            label = LABELS[int(chr(key))]  # Press 0–5 for labels
        except:
            print("Invalid key. Use 0=red, 1=green, 2=blue, 3=white, 4=yellow, 5=orange")
            continue

        save_path = os.path.join(SAVE_FOLDER, label, f"{image_index}_{i}.jpg")
        cv2.imwrite(save_path, resized)
        print(f"Saved to {save_path}")

def main():
    images = [f for f in os.listdir(RAW_FOLDER) if f.lower().endswith(('.jpg', '.png'))]

    print("\n⚠️ Use these keys to label colors:")
    print("0 = red, 1 = green, 2 = blue, 3 = white, 4 = yellow, 5 = orange")
    print("Press ESC to quit at any time.\n")

    for idx, file in enumerate(images):
        print(f"\nProcessing {file}...")
        img_path = os.path.join(RAW_FOLDER, file)
        img = cv2.imread(img_path)

        stickers = crop_stickers(img)
        label_and_save(stickers, idx)

if __name__ == "__main__":
    main()
