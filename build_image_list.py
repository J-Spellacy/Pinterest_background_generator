import os
import pickle
import argparse
from PIL import Image

# Inputs from bash script with a default added incase I switch to using jpeg or something
parser = argparse.ArgumentParser(description="Generate pickle file with image metadata from a folder.")
parser.add_argument("folder", type=str, help="Path to folder containing images")
parser.add_argument("--ext", type=str, default=".png", help="Image extension to include (default: .png)")
args = parser.parse_args()

# file names of pickle files to reflect cluster
FOLDER = os.path.abspath(args.folder)
folder_name = os.path.basename(os.path.normpath(FOLDER))
OUTPUT_LIST = f"images_{folder_name}.pkl"

images = []
for fname in os.listdir(FOLDER):
    if fname.lower().endswith(args.ext.lower()):
        path = os.path.join(FOLDER, fname)
        with Image.open(path) as img:
            w, h = img.size
        images.append({'name': fname, 'path': path, 'w': w, 'h': h})


with open(OUTPUT_LIST, 'wb') as f:
    pickle.dump(images, f)

print(f"Saved {len(images)} images to {OUTPUT_LIST}")
