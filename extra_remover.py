import os
import re

FOLDER = "/home/jude/Pictures/pint_pins"  
LIMIT = 1136 # enter the number of pins in your html file or look in the folder to see where the adverts begin

for filename in os.listdir(FOLDER):
    match = re.match(r"pin_(\d{4})\.jpg$", filename)
    if match:
        num = int(match.group(1))
        if num > LIMIT:
            filepath = os.path.join(FOLDER, filename)
            os.remove(filepath)
            print(f"Deleted {filename}")