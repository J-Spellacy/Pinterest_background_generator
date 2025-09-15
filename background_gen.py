## Find out primary colors of each image, work out if this is possible
## Start from corners working the way inwards to a full background

import os
import random
from PIL import Image
import numpy as np
import bisect
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_FILE = os.path.join(BASE_DIR, 'images.pkl')

# Settings
CANVAS_SIZE = (3840, 2160)  # target resolution
OUTPUT_FILE = os.path.join(BASE_DIR, 'collage.png')

with open(IMAGES_FILE, 'rb') as f:
    images = pickle.load(f)

def load_image(entry):
    '''Lazy load image from path into entry dict (adds 'img' key).'''
    if 'img' not in entry:
        entry['img'] = Image.open(entry['path']).convert('RGB')
    return entry['img']

# Step 2. Pick central image
central = random.choice(images)
cx, cy = CANVAS_SIZE[0] // 2, CANVAS_SIZE[1] // 2
cw, ch = central['w'], central['h']

# Step 3. Get modal color of central image
arr = np.array(load_image(central))
pixels = arr.reshape(-1, 3)
modal_color = tuple(np.apply_along_axis(lambda x: np.bincount(x).argmax(), 0, pixels))

# Step 4. Create canvas filled with modal color
canvas = Image.new('RGB', CANVAS_SIZE, modal_color)

## need to start with corners then fill the gaps then work out second layer algorithm
# Step 5. Paste central image in the middle
x0 = cx - cw // 2
y0 = cy - ch // 2
canvas.paste(load_image(central), (x0, y0))

'''
Conditions for algorithm:

# first pass
- select random corner images
- fill gaps in y direction with random images when x is > or < 0 and in x when y is > or < 0
- allow either a set overlap (flat rate) or a percentage of parent image

# second pass
- for each image check what the central x and y is relative to centre of first image
- use this to determine which corner to fill first
- from corners fill either side

Optional/later additions:
- match modal colour of background with modal colour of images in some range of complementary colours
(see if there is an easy way to do this with rgb or something)
- Make central/first image from a subset of large images

'''

def overlap_gen(w = 800, h = 800, fraction_cover = 0.2, max_overlap = 20):
    ## define this function to take the width and height and work out appropriate pixel overlaps
    # will need to take into account whether overlap is in x or y direction
    return random.randint(0, max_overlap)

# Step 6. Naive greedy placement of others (demo version)
# Idea: expand outward from center, try to fill quadrants
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
            # 10 px overlap
            ## minimise these with the edge of the screen
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

central_x, central_y, central_w, central_h = placed[0]
top_left_x, top_left_y, top_left_w, top_left_h = placed[1]
bot_left_x, bot_left_y, bot_left_w, bot_left_h = placed[2]
top_right_x, top_right_y, top_right_w, top_right_h = placed[3]
bot_right_x, bot_right_y, bot_right_w, bot_right_h = placed[4]

images_sorted_w = sorted(images, key=lambda im: im['w'])
images_sorted_h = sorted(images, key=lambda im: im['h'])

# with open('images_sorted_w.pkl', 'rb') as f:
#     images_sorted_w = pickle.load(f)

# with open('images_sorted_h.pkl', 'rb') as f:
#     images_sorted_h = pickle.load(f)

images_sorted_w = sorted(images, key=lambda im: im['w'])
images_sorted_h = sorted(images, key=lambda im: im['h'])

def find_next_bigger(dx: int, measure: str):
    if measure == 'w':
        measures = [im['w'] for im in images_sorted_w]
    if measure == 'h':
        measures = [im['h'] for im in images_sorted_h]
    idx = bisect.bisect_right(measures, dx)  # first index where width > dx
    if (idx) < len(images_sorted_w) and measure =='w':
        print(f'i am width {images_sorted_w[idx]['w']} > {dx}')
        return images_sorted_w[idx]  # image with smallest w > dx
        
    if (idx) < len(images_sorted_h) and measure =='h':
        print(f'i am height {images_sorted_w[idx]['h']} > {dx}')
        return images_sorted_h[idx]  # image with smallest h > dx

    else:
        print('im random xd')
        return random.choice(images) # no width bigger than dx

def width_fitter(dx: int, left_x, left_w, central_y, central_h, max_overlap, top: bool, CANVAS_SIZE):
    closest_img = find_next_bigger(dx = dx, measure = 'w')
    new_x = (dx // 2) + (left_x + left_w) - (closest_img['w'] // 2)
    if top:
        new_y = central_y - closest_img['h'] + overlap_gen(max_overlap = max_overlap)
        # new_y = max(central_y - closest_img['h'] + overlap_gen(max_overlap = max_overlap), 0)
    else:
        new_y = central_y + central_h - overlap_gen(max_overlap = max_overlap)
        # new_y = min(central_y + central_h - overlap_gen(max_overlap = max_overlap), CANVAS_SIZE[1] - closest_img['h'])
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
    # needs to find the central values of the central image so central x and y + central_w // 2 or central_h // 2
    # all images to for example the left have images added in that direction using the closest image to the gap between that image and the end of the screen
    # one function for all directions called for each direction


def complementary_cols_finder():
    # uses central image and only includes images in list with mostly complementary colors
    # to be used before algorithm
    return

for i in placed:
    img_x, img_y, img_w, img_h = i
    edge_addition(central_x = central_x, central_y = central_y, img_x = img_x, img_y = img_y, img_w = img_w, img_h = img_h, direction = 'top', canvas_size = CANVAS_SIZE)
    edge_addition(central_x = central_x, central_y = central_y, img_x = img_x, img_y = img_y, img_w = img_w, img_h = img_h, direction = 'bottom', canvas_size = CANVAS_SIZE)
    edge_addition(central_x = central_x, central_y = central_y, img_x = img_x, img_y = img_y, img_w = img_w, img_h = img_h, direction = 'left', canvas_size = CANVAS_SIZE)
    edge_addition(central_x = central_x, central_y = central_y, img_x = img_x, img_y = img_y, img_w = img_w, img_h = img_h, direction = 'right', canvas_size = CANVAS_SIZE)


# Save output
canvas.save(OUTPUT_FILE)
print(f'Collage saved as {OUTPUT_FILE}')