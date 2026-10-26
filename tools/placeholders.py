# -*- coding: utf-8 -*-
"""Erzeugt Platzhalterbilder, bis die Higgsfield-Bilder da sind. Vorhandene Dateien werden nicht überschrieben."""
import os, sys, shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from content import SERVICES, PROJECTS
IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site", "assets", "img")
PINK, INK, PAPER = (245, 189, 190), (10, 10, 11), (246, 245, 241)

def font(size, bold=True):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def typo(path, label, w=1200, h=1200, dark=False):
    bg, fg = (INK, PINK) if dark else (PINK, INK)
    im = Image.new("RGB", (w, h), bg); d = ImageDraw.Draw(im)
    f = font(int(w * .34)); d.text((w * .5, h * .48), "WOW", font=f, fill=fg, anchor="mm")
    d.text((w * .05, h * .93), label.upper(), font=font(int(w * .028), False), fill=fg, anchor="lm")
    im.save(path, quality=85)

def zoom(src, path, box=(.2, .15, .8, .85), flip=False):
    im = Image.open(src); W, H = im.size
    c = im.crop((int(W*box[0]), int(H*box[1]), int(W*box[2]), int(H*box[3])))
    if flip: c = ImageOps.mirror(c)
    if c.width < 1200:
        f = 1200 / c.width
        c = c.resize((int(c.width * f), int(c.height * f)), Image.LANCZOS)
    c.save(path, quality=85)

def out(n): return os.path.join(IMG, n)
def missing(n): return not os.path.exists(out(n))

proj = {p["cat"]: p["img"] for p in PROJECTS}
for s in SERVICES:
    base = out(s["img"])
    if missing(s["slug"] + "-2.jpg"): zoom(base, out(s["slug"] + "-2.jpg"), (.25, .1, .75, .9), flip=True)
    if missing(s["slug"] + "-3.jpg"): typo(out(s["slug"] + "-3.jpg"), "Platzhalter · " + s["slug"] + "-3.jpg", dark=s["num"] in ("02", "04", "06"))
    if missing(s["slug"] + "-4.jpg"):
        src = out(proj[s["key"]]) if s["key"] in proj and proj[s["key"]] != s["img"] else base
        zoom(src, out(s["slug"] + "-4.jpg"), (.05, 0, .95, 1))
for n in ("vehicle-after.jpg", "vehicle-before.jpg"):
    if missing(n): shutil.copy(out("hero-car.jpg"), out(n))
print("Platzhalter ok")
