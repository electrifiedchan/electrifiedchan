"""Build a slow, seamless animated ring around the existing GitHub avatar.

Usage: python scripts/build_logo.py [--refresh-avatar]
Requires: python -m pip install -r scripts/requirements.txt
"""

from __future__ import annotations

import argparse
import math
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
AVATAR_URL = "https://avatars.githubusercontent.com/u/174957966?s=400&v=4"
SIZE = 320
SCALE = 3
FRAMES = 75
FRAME_MS = 80  # One quiet, six-second revolution.
CYAN = (90, 211, 255)
BLUE = (65, 135, 230)
TRACK = (29, 55, 77)
TRANSPARENT = (255, 0, 255)


def build_frame(avatar: Image.Image, phase: float) -> Image.Image:
    # Downsample against the backing color, not the GIF transparency key, to
    # prevent a magenta fringe around the circular edge.
    canvas = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), (10, 17, 26))
    draw = ImageDraw.Draw(canvas)
    center = SIZE * SCALE / 2

    def ring(radius: float, color: tuple[int, int, int], width: float) -> None:
        r = radius * SCALE
        draw.ellipse(
            (center - r, center - r, center + r, center + r),
            outline=color,
            width=round(width * SCALE),
        )

    # A dark circular backing keeps the logo readable on either GitHub theme.
    draw.ellipse((10 * SCALE, 10 * SCALE, 310 * SCALE, 310 * SCALE), fill=(10, 17, 26))
    ring(149, (30, 48, 65), 1)
    ring(137, TRACK, 2)
    ring(125, (27, 39, 53), 1)

    # Two restrained, opposing trails orbit; the monogram itself stays still.
    radius = 137 * SCALE
    for offset, color in ((0, CYAN), (math.pi, BLUE)):
        angle = phase * math.tau + offset
        for step in range(90):
            strength = (step + 1) / 90
            start = angle - math.radians(90 - step)
            end = start + math.radians(1.6)
            shade = tuple(round(a + (b - a) * strength**1.6) for a, b in zip(TRACK, color))
            draw.line(
                (
                    center + radius * math.cos(start),
                    center + radius * math.sin(start),
                    center + radius * math.cos(end),
                    center + radius * math.sin(end),
                ),
                fill=shade,
                width=4 * SCALE,
            )
        x = center + radius * math.cos(angle)
        y = center + radius * math.sin(angle)
        r = 2.8 * SCALE
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

    diameter = 234 * SCALE
    logo = ImageOps.fit(avatar, (diameter, diameter), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", logo.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter - 1, diameter - 1), fill=255)
    inset = (SIZE * SCALE - diameter) // 2
    canvas.paste(logo, (inset, inset), mask)

    # GIF has binary transparency. An exact circular mask avoids colored edges.
    canvas = canvas.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    visible = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(visible).ellipse((10, 10, 310, 310), fill=255)
    result = Image.new("RGB", (SIZE, SIZE), TRANSPARENT)
    result.paste(canvas, mask=visible)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-avatar", action="store_true", help="Download the current public avatar")
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    source = ASSETS / "avatar-source.png"

    if args.refresh_avatar or not source.exists():
        request = Request(AVATAR_URL, headers={"User-Agent": "electrifiedchan-profile-assets"})
        with urlopen(request, timeout=30) as response:
            with Image.open(BytesIO(response.read())) as image:
                image.convert("RGB").save(source, optimize=True)

    with Image.open(source) as image:
        avatar = image.convert("RGB")
    frames = [build_frame(avatar, index / FRAMES) for index in range(FRAMES)]

    # Share one palette across all frames so the stationary avatar never flickers.
    sheet = Image.new("RGB", (SIZE * 5, SIZE))
    for index in range(5):
        sheet.paste(frames[index * (FRAMES // 5)], (SIZE * index, 0))
    palette = sheet.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    colors = palette.getpalette()[: 255 * 3] + list(TRANSPARENT)
    palette.putpalette(colors)

    indexed = []
    for frame in frames:
        output = frame.quantize(palette=palette, dither=Image.Dither.NONE)
        background = Image.new("L", frame.size)
        background.putdata([255 if pixel == TRANSPARENT else 0 for pixel in frame.get_flattened_data()])
        output.paste(255, mask=background)
        indexed.append(output)

    animation = ASSETS / "logo-animated.gif"
    indexed[0].save(
        animation,
        save_all=True,
        append_images=indexed[1:],
        duration=FRAME_MS,
        loop=0,
        disposal=1,
        transparency=255,
        background=255,
        optimize=True,
    )
    still = frames[0].convert("RGBA")
    still.putalpha(Image.eval(background, lambda value: 255 - value))
    still.save(ASSETS / "logo-static.png", optimize=True)
    print(f"Built {animation.relative_to(ROOT)}: {FRAMES} frames, {FRAMES * FRAME_MS / 1000:g}s loop, {animation.stat().st_size / 1024:.0f} KiB")


if __name__ == "__main__":
    main()
