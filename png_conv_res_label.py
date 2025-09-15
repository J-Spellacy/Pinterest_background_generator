import os
from PIL import Image
import re

FOLDER = "/home/jude/Pictures/pint_pins"  # your folder with jpgs

for filename in os.listdir(FOLDER):
    if filename.lower().endswith(".jpg"):
        jpg_path = os.path.join(FOLDER, filename)

        with Image.open(jpg_path) as img:
            width, height = img.size

            # new filename: keep prefix (e.g., pin_0001) and add dimensions
            base = os.path.splitext(filename)[0]  # "pin_0001"
            new_name = f"{base}_{width}_{height}.png"
            new_path = os.path.join(FOLDER, new_name)

            img.save(new_path, "PNG")
            print(f"Converted {filename} → {new_name}")

        # delete original JPG
        os.remove(jpg_path)

# pattern = re.compile(r"^pin_(\d+)_([0-9]+)_([0-9]+)\.png$")

# for filename in os.listdir(FOLDER):
#     match = pattern.match(filename)
#     if match:
#         num, w, h = match.groups()
#         num_padded = f"{int(num):04d}"  # pad to 4 digits
#         new_name = f"pin_{num_padded}_{w}_{h}.png"
        
#         old_path = os.path.join(FOLDER, filename)
#         new_path = os.path.join(FOLDER, new_name)
        
#         # only rename if different
#         if old_path != new_path:
#             os.rename(old_path, new_path)
#             print(f"Renamed {filename} → {new_name}")