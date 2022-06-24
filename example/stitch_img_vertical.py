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

for img in list_im:
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
    "new.png", quality=100
)
