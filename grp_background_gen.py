## Find out primary colors of each image, cluster based on the hsl value (WIP)

import os
import random
from PIL import Image
import numpy as np
import bisect
import pickle
import argparse
import re

# arguments given in the bash script, with a default that is absent from the default bash script
parser = argparse.ArgumentParser(description="Generate collage from images.")
parser.add_argument("images_file", type=str, help="Path to images_cluster_NUM.pkl file")
parser.add_argument("--output", type=str, default=None, help="Output file path (optional)")
args = parser.parse_args()

IMAGES_FILE = args.images_file
input_dir = os.path.dirname(IMAGES_FILE)

# If you don't have a specific file location in mind (you will need to then edit default input directory above) then you can specify output location in bash sctipt
if args.output:
    OUTPUT_FILE = args.output
else:
    match = re.search(r'images_cluster_(\d+)\.pkl$', os.path.basename(IMAGES_FILE))
    if match:
        num = match.group(1)
        OUTPUT_FILE = os.path.join(input_dir, f"collage_{num}.png")
    else:
        raise ValueError("Input file must be named like images_cluster_NUM.pkl or specify --output")

# Sets target canvas size (default to 4k which I prefer as I can fit more images then compress them for my meager 1k monitor)
CANVAS_SIZE = (3840, 2160)

with open(IMAGES_FILE, 'rb') as f:
    images = pickle.load(f)

def load_image(entry):
    # Lazy load image from path into entry dict (adds 'img' key).
    if 'img' not in entry:
        entry['img'] = Image.open(entry['path']).convert('RGB')
    return entry['img']

## 1. first pass placing central and corner images

central = random.choice(images)
cx, cy = CANVAS_SIZE[0] // 2, CANVAS_SIZE[1] // 2
cw, ch = central['w'], central['h']

# not necessarily required, but generates a modal background colour incase of gaps
arr = np.array(load_image(central))
pixels = arr.reshape(-1, 3)
modal_color = tuple(np.apply_along_axis(lambda x: np.bincount(x).argmax(), 0, pixels))
canvas = Image.new('RGB', CANVAS_SIZE, modal_color)

# placing central image
x0 = cx - cw // 2
y0 = cy - ch // 2
canvas.paste(load_image(central), (x0, y0))
images.remove(central)


def overlap_gen(w = 800, h = 800, fraction_cover = 0.2, max_overlap = 20):
    ## define this function to take the width and height and work out appropriate pixel overlaps
    # will need to take into account whether overlap is in x or y direction
    # this is a work in progress that got a bit forgotten about currently just random between an arbitrary bound
    return random.randint(0, max_overlap)

max_overlap = 50
placed = [(x0, y0, cw, ch)]

for i in range(-1,2):
    for j in range(-1,2):
        if i != 0 and j != 0:
            # first corners
            img = random.choice(images)
            while img['name'] == central['name']:
                img = random.choice(images)
            w, h = img['w'], img['h']

            last_x, last_y, lw, lh = placed[0]

            if i > 0: # to the right
                new_x = min(last_x + lw - i * overlap_gen(max_overlap = max_overlap), CANVAS_SIZE[0]-w)
            elif i < 0: # to the left
                new_x = max(last_x - w - i * overlap_gen(max_overlap = max_overlap), 0)
            if j > 0: # downwards
                new_y = min(last_y + lh - j * overlap_gen(max_overlap = max_overlap), CANVAS_SIZE[1]-h)
            elif j < 0: # upwards
                new_y = max(last_y - h - j * overlap_gen(max_overlap = max_overlap), 0)

            canvas.paste(load_image(img), (new_x, new_y))
            placed.append((new_x, new_y, w, h))
            images.remove(img)

central_x, central_y, central_w, central_h = placed[0]
top_left_x, top_left_y, top_left_w, top_left_h = placed[1]
bot_left_x, bot_left_y, bot_left_w, bot_left_h = placed[2]
top_right_x, top_right_y, top_right_w, top_right_h = placed[3]
bot_right_x, bot_right_y, bot_right_w, bot_right_h = placed[4]


## 2. Second pass filling gaps between corners, first time sorting images by height and width

images_sorted_w = sorted(images, key=lambda im: im['w'])
images_sorted_h = sorted(images, key=lambda im: im['h'])

# following algorithm needs fixing as it routinely fails giving the largest that is smaller than the target
def find_next_bigger(dx: int, measure: str):
    if measure == 'w':
        measures = [im['w'] for im in images_sorted_w]
        idx = bisect.bisect_left(measures, dx)  # first index where width >= dx
        if idx < len(images_sorted_w):
            print(f'i am width {images_sorted_w[idx]["w"]} >= {dx}')
            return images_sorted_w[idx]  # image with smallest w >= dx 
        else:
            print('im random xd')
            return random.choice(images_sorted_w) # no width bigger than dx

    elif measure == 'h':
        measures = [im['h'] for im in images_sorted_h]
        idx = bisect.bisect_left(measures, dx)  # first index where height >= dx
        if idx < len(images_sorted_h):
            print(f'i am height {images_sorted_h[idx]["h"]} >= {dx}')
            return images_sorted_h[idx]  # image with smallest h >= dx
        else:
            print('im random xd')
            return random.choice(images_sorted_h) # no height bigger than dx


# following two functions could probably easily be merged into one smaller function but, I dont really see how that would make it quicker just more readable
def width_fitter(dx: int, left_x, left_w, central_y, central_h, max_overlap, top: bool, CANVAS_SIZE):
    closest_img = find_next_bigger(dx = dx, measure = 'w')
    new_x = (dx // 2) + (left_x + left_w) - (closest_img['w'] // 2)
    if top:
        new_y = central_y - closest_img['h'] + overlap_gen(max_overlap = max_overlap)
    else:
        new_y = central_y + central_h - overlap_gen(max_overlap = max_overlap)
    canvas.paste(load_image(closest_img), (new_x, new_y))
    images_sorted_w.remove(closest_img)
    images_sorted_h.remove(closest_img)
    placed.append((new_x, new_y, closest_img['w'], closest_img['h']))

def height_fitter(dy: int, top_y, top_h, central_x, central_w, max_overlap, left: bool, CANVAS_SIZE):
    closest_img = find_next_bigger(dx = dy, measure = 'h')
    new_y = (dy // 2) + (top_y + top_h) - (closest_img['h'] // 2)
    if left:
        new_x = central_x - closest_img['w'] + overlap_gen(max_overlap = max_overlap)
    else:
        new_x = central_x + central_w - overlap_gen(max_overlap = max_overlap)
    canvas.paste(load_image(closest_img), (new_x, new_y))
    images_sorted_w.remove(closest_img)
    images_sorted_h.remove(closest_img)
    placed.append((new_x, new_y, closest_img['w'], closest_img['h']))

dx = top_right_x - (top_left_x + top_left_w)
if dx > 0:
    width_fitter(dx = dx, left_x = top_left_x, left_w = top_left_w, central_y = central_y, central_h = central_h, max_overlap = max_overlap, top = True, CANVAS_SIZE = CANVAS_SIZE)

dx = bot_right_x - (bot_left_x + bot_left_w)
if dx > 0:
    width_fitter(dx = dx, left_x = bot_left_x, left_w = bot_left_w, central_y = central_y, central_h = central_h, max_overlap = max_overlap, top = False, CANVAS_SIZE = CANVAS_SIZE)

dy = bot_right_y - (top_right_y + top_right_h)
if dy > 0:
    height_fitter(dy=dy, top_y = top_right_y, top_h = top_right_h, central_x = central_x, central_w = central_w, max_overlap = max_overlap, left = False, CANVAS_SIZE = CANVAS_SIZE)

dy = bot_left_y - (top_left_y + top_left_h)
if dy > 0:
    height_fitter(dy=dy, top_y = top_left_y, top_h = top_left_h, central_x = central_x, central_w = central_w, max_overlap = max_overlap, left = True, CANVAS_SIZE = CANVAS_SIZE)


## 3. Third pass, filling from each image edge a similar width or height up to the screen edge

def edge_addition(central_x: int, central_y: int, img_x: int, img_y: int, img_w: int, img_h: int, direction: str, canvas_size):
    centre_x = canvas_size[0] // 2
    centre_y = canvas_size[1] // 2

    if direction == 'top' and img_y < central_y and img_y > 0:
        closest_img = find_next_bigger(dx = img_w, measure = 'w')
        new_y = img_y - closest_img['h'] + overlap_gen(max_overlap = max_overlap)
        new_x = img_x + (img_w // 2) - (closest_img['w'] // 2)
        canvas.paste(load_image(closest_img), (new_x, new_y))
        placed.append((new_x, new_y, closest_img['w'], closest_img['h']))
        print(f'i am height {closest_img['h']} > {img_y - 0}, (top)')
        images_sorted_w.remove(closest_img)
        images_sorted_h.remove(closest_img)

    if direction == 'bottom' and img_y > centre_y and (img_y + img_h) < canvas_size[1]:
        closest_img = find_next_bigger(dx = img_w, measure = 'w')
        new_y = img_y + img_h - overlap_gen(max_overlap = max_overlap)
        new_x = img_x + (img_w // 2) - (closest_img['w'] // 2)
        canvas.paste(load_image(closest_img), (new_x, new_y))
        placed.append((new_x, new_y, closest_img['w'], closest_img['h']))
        print(f'i am height {closest_img['h']} > {canvas_size[1] - (img_y + img_h)}, (bottom)')
        images_sorted_w.remove(closest_img)
        images_sorted_h.remove(closest_img)

    if direction == 'left' and img_x < central_x and img_x > 0:
        closest_img = find_next_bigger(dx = img_h, measure = 'h')
        new_x = img_x - closest_img['w'] + overlap_gen(max_overlap = max_overlap)
        new_y = img_y + (img_h // 2) - (closest_img['h'] // 2)
        canvas.paste(load_image(closest_img), (new_x, new_y))
        placed.append((new_x, new_y, closest_img['w'], closest_img['h']))
        print(f'i am width {closest_img['w']} > {img_w - 0}, (left)')
        images_sorted_w.remove(closest_img)
        images_sorted_h.remove(closest_img)

    if direction == 'right' and img_x > centre_x and (img_x + img_w) < canvas_size[0]:
        closest_img = find_next_bigger(dx = img_h, measure = 'h')
        new_x = img_x + img_w - overlap_gen(max_overlap = max_overlap)
        new_y = img_y + (img_h // 2) - (closest_img['h'] // 2)
        canvas.paste(load_image(closest_img), (new_x, new_y))
        placed.append((new_x, new_y, closest_img['w'], closest_img['h']))
        print(f'i am width {closest_img['w']} > {canvas_size[0] - (img_x + img_w)}, (right)')
        images_sorted_w.remove(closest_img)
        images_sorted_h.remove(closest_img)

# running loop for third stage
for i in placed:
    img_x, img_y, img_w, img_h = i
    edge_addition(central_x = central_x, central_y = central_y, img_x = img_x, img_y = img_y, img_w = img_w, img_h = img_h, direction = 'top', canvas_size = CANVAS_SIZE)
    edge_addition(central_x = central_x, central_y = central_y, img_x = img_x, img_y = img_y, img_w = img_w, img_h = img_h, direction = 'bottom', canvas_size = CANVAS_SIZE)
    edge_addition(central_x = central_x, central_y = central_y, img_x = img_x, img_y = img_y, img_w = img_w, img_h = img_h, direction = 'left', canvas_size = CANVAS_SIZE)
    edge_addition(central_x = central_x, central_y = central_y, img_x = img_x, img_y = img_y, img_w = img_w, img_h = img_h, direction = 'right', canvas_size = CANVAS_SIZE)


# Save output
canvas.save(OUTPUT_FILE)
print(f'Collage saved as {OUTPUT_FILE}')