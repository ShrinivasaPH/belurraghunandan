#!/usr/bin/env python3
"""Shrink the heavy pictures for the web. Run from the repo root:  python3 optimize_images.py
Resizes plays/, Books/, gallery/ (and sub-folders) to max 1100px on the long side and
saves them as progressive JPEG (quality 82). Already-light files are left alone,
so it is safe to run again after adding new pictures."""
import os, sys
from PIL import Image, ImageOps
ROOT = os.path.join(os.getcwd(), "images")
FOLDERS = ["plays", "Books", "gallery"]
MAX_SIDE, QUALITY, SKIP_BELOW = 1100, 82, 300 * 1024
saved = 0
for folder in FOLDERS:
    for dp, _, files in os.walk(os.path.join(ROOT, folder)):
        for f in files:
            p = os.path.join(dp, f)
            if not f.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            size = os.path.getsize(p)
            im = ImageOps.exif_transpose(Image.open(p))
            if size < SKIP_BELOW and max(im.size) <= MAX_SIDE:
                continue
            if max(im.size) > MAX_SIDE:
                im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA")
                bg = Image.new("RGB", im.size, "white")
                bg.paste(im, mask=im.split()[-1])
                im = bg
            else:
                im = im.convert("RGB")
            out = os.path.splitext(p)[0] + ".jpg"
            im.save(out + ".tmp", "JPEG", quality=QUALITY, optimize=True, progressive=True)
            os.replace(out + ".tmp", out)
            if out != p:
                os.remove(p)
            new = os.path.getsize(out)
            saved += size - new
            print(f"{os.path.relpath(p, ROOT)}: {size//1024} KB -> {new//1024} KB")
print(f"Saved {saved/1024/1024:.1f} MB")
