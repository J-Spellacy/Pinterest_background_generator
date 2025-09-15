import os
import pickle
from PIL import Image

FOLDER = '/home/jude/Pictures/pint_pins'
OUTPUT_LIST = 'images.pkl'
OUTPUT_LIST_SORTED_W = 'images_sorted_w.pkl'
OUTPUT_LIST_SORTED_H = 'images_sorted_h.pkl'

images = []
for fname in os.listdir(FOLDER):
    if fname.lower().endswith('.png'):
        path = os.path.join(FOLDER, fname)
        with Image.open(path) as img:
            w, h = img.size
        images.append({'name': fname, 'path': path, 'w': w, 'h': h})

# Save to file (binary format)
with open(OUTPUT_LIST, 'wb') as f:
    pickle.dump(images, f)


images_sorted_w = sorted(images, key=lambda im: im['w'])
images_sorted_h = sorted(images, key=lambda im: im['h'])

with open(OUTPUT_LIST_SORTED_W, 'wb') as f:
    pickle.dump(images_sorted_w, f)

with open(OUTPUT_LIST_SORTED_H, 'wb') as f:
    pickle.dump(images_sorted_h, f)

print(f"Saved {len(images)} images to {OUTPUT_LIST}")
print(f"saved {OUTPUT_LIST_SORTED_W} and {OUTPUT_LIST_SORTED_H}")