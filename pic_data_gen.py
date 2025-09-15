import os
import re
import pandas as pd

FOLDER = "/home/jude/Pictures/pint_pins"
pattern = re.compile(r"^pin_(\d{4})_(\d+)_(\d+)\.png$")

rows = []

for filename in os.listdir(FOLDER):
    match = pattern.match(filename)
    if match:
        pin_number, width, height = match.groups()
        rows.append({
            "pin_number": int(pin_number),
            "width": int(width),
            "height": int(height)
        })

# Make DataFrame
df = pd.DataFrame(rows).sort_values("pin_number").reset_index(drop=True)

print(df.head())  # preview
print(f"Total pins: {len(df)}")

# Save to CSV if you want
df.to_csv("pins_metadata.csv", index=False)