#!/usr/bin/env python3
"""Cover art: a night sky over pack ice, a small sledge on the horizon, the title. 1600x1600 JPG.

    <studio venv python> tools/cover.py   # needs Pillow
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W = H = 1600
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def main():
    random.seed(17)
    img = Image.new("RGB", (W, H))
    px = img.load()
    horizon = int(H * 0.62)
    for y in range(H):
        if y < horizon:  # sky: near-black to deep blue at the horizon
            t = y / horizon
            c = (int(8 + 22 * t), int(12 + 34 * t), int(24 + 58 * t))
        else:  # ice: grey-blue, darker towards the viewer
            t = (y - horizon) / (H - horizon)
            c = (int(150 - 95 * t), int(170 - 100 * t), int(190 - 100 * t))
        for x in range(W):
            px[x, y] = c
    d = ImageDraw.Draw(img)
    for _ in range(260):  # stars
        x, y = random.randrange(W), random.randrange(int(horizon * 0.9))
        r = random.choice([1, 1, 1, 2])
        b = random.randint(150, 255)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(b, b, min(255, b + 10)))
    for _ in range(40):  # pressure ridges in the ice
        x = random.randrange(-200, W)
        y = random.randrange(horizon + 10, H - 220)
        w = random.randrange(120, 520)
        d.line([(x, y), (x + w, y + random.randrange(-12, 12))], fill=(205, 220, 232), width=random.choice([1, 2, 3]))
    img = img.filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(img)
    # the sledge and its driver, small, far off, heading right (north)
    sx, sy = int(W * 0.68), horizon - 2
    d.rectangle([sx, sy - 10, sx + 46, sy], fill=(10, 12, 18))
    d.rectangle([sx + 30, sy - 40, sx + 42, sy - 10], fill=(10, 12, 18))
    d.ellipse([sx + 29, sy - 54, sx + 43, sy - 40], fill=(10, 12, 18))
    for i in range(5):
        dx = sx + 60 + i * 22
        d.ellipse([dx, sy - 9, dx + 16, sy], fill=(10, 12, 18))
    d.line([(sx + 46, sy - 5), (sx + 165, sy - 5)], fill=(10, 12, 18), width=2)

    title = ImageFont.truetype(SERIF_B, 132)
    sub = ImageFont.truetype(SERIF, 52)
    small = ImageFont.truetype(SERIF, 40)
    def centre(text, font, y, fill):
        w = d.textlength(text, font=font)
        d.text(((W - w) / 2, y), text, font=font, fill=fill)
    centre("DARKNESS", title, 230, (232, 236, 240))
    centre("AND DISTANCE", title, 380, (232, 236, 240))
    centre("a true-crime podcast", sub, 560, (170, 190, 210))
    centre("The Frankenstein Letters  ·  Season One", small, H - 170, (228, 234, 242))
    centre("after Mary Shelley, 1818", small, H - 110, (228, 234, 242))
    for out in (ROOT / "voice/darkness-and-distance/cover.jpg", ROOT / "site/static/cover.jpg"):
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, quality=90)
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
