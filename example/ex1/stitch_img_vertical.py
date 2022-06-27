import numpy as np
from PIL import Image
import glob

list_im = glob.glob("*.png")
total_width = 0
total_height = 0
max_width = 0
max_height = 0
min_width = 2000
min_height = 0
pre_w = 0
pre_h = 0
ix = []

"""
Input: A bunch of images with names that have iterating number (0.png, 1.png, ...)

list_im = ['8.png', '9.png', '14.png', '15.png', '17.png', '16.png', '12.png', '13.png',
 '11.png', '10.png', '20.png', '18.png', 'new.png', '19.png', '4.png', '5.png'
, '7.png', '6.png', '2.png', '3.png', '1.png', '0.png']

Output: Image stitched/combined vertically in that order.

- The problem:
    Currrently, the image combine the images in a random order. I want to change that.


Constraints:
    I have to split the strings inside list_im and convert them from string to int.
    The names have to be numbers, if else, ignore.

- I need to access the name of the image files. I cannot use the exif data/metadata since the screenshots I take with shareX does not store them.
- This is an array problem.


- Naive Approach:
    Just use sort.
    Make a list that is sorted by names.
    Iterate through the new list and combine the images.
    
- Hashmap / hashset:
    Iterate through list_im and store the key as the file name and value as the integer in the name. ( {"0.png": 0, "1.png": 1, ...} ) 
    Sort by values in the hashmap.

"""

d = {}

# print(list_im)
for img in list_im:

    if "_" in img:
        img_num = img.split("_")[0]
    else:
        img_num = img.split(".")[0]

    if img_num.isnumeric():
        d[img] = int(img_num)


for img in sorted(d, key=d.get, reverse=False):
    im = Image.open(img)
    size = im.size
    w = size[0]
    h = size[1]
    total_width += w
    total_height += h

    if h > max_height:
        max_height = h
    if w > max_width:
        max_width = w
    if h < min_height:
        min_height = h
    if w < min_width:
        min_width = w
    ix.append(im)


target_vertical = Image.new("RGB", (max_width, total_height))

for img in ix:
    target_vertical.paste(img, (pre_w, pre_h, pre_w + img.size[0], pre_h + img.size[1]))
    pre_h += img.size[1]


tw, th = target_vertical.size
target_vertical.crop((0, 0, tw - (max_width - min_width), th)).save(
    "result_sorted_combined.png", quality=100
)
