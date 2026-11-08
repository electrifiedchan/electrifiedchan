"""Generate original pixel solar-system artwork and cache the tech icon strips.

Run: python scripts/build_profile_art.py [--refresh-icons]
Requires Pillow; install scripts/requirements.txt first.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WIDTH, HEIGHT, SCALE = 416, 190, 2
FRAMES, FRAME_MS = 180, 120
CENTER = (208, 102)
BACKGROUND = (8, 13, 27)
FONT = {
    "A": "010/101/111/101/101", "B": "110/101/110/101/110",
    "C": "011/100/100/100/011", "D": "110/101/101/101/110",
    "E": "111/100/110/100/111", "F": "111/100/110/100/100",
    "G": "011/100/101/101/011", "H": "101/101/111/101/101",
    "I": "111/010/010/010/111", "J": "001/001/001/101/010",
    "K": "101/101/110/101/101", "L": "100/100/100/100/111",
    "M": "101/111/111/101/101", "N": "101/111/111/111/101",
    "O": "010/101/101/101/010", "P": "110/101/110/100/100",
    "Q": "010/101/101/111/011", "R": "110/101/110/101/101",
    "S": "011/100/010/001/110", "T": "111/010/010/010/010",
    "U": "101/101/101/101/111", "V": "101/101/101/101/010",
    "W": "101/101/111/111/101", "X": "101/101/010/101/101",
    "Y": "101/101/010/010/010", "Z": "111/001/010/100/111",
    "/": "001/001/010/100/100", ".": "000/000/000/000/010",
    "-": "000/000/111/000/000", " ": "000/000/000/000/000",
}
# name, orbital radii, planet size, palette, revolutions per seamless loop, phase
# These are creative stack symbols, not language percentages or live metrics.
WORLDS = [
    ("PYTHON", 46, 26, 5, ((247, 204, 104), (175, 115, 53), (255, 235, 169)), 3, 0.45),
    ("TYPESCRIPT", 70, 34, 6, ((95, 157, 245), (48, 77, 147), (163, 205, 255)), 2, 3.45),
    ("JAVASCRIPT", 96, 43, 5, ((247, 173, 98), (161, 77, 60), (255, 220, 151)), 2, 5.00),
    ("REACT", 121, 51, 7, ((90, 212, 226), (40, 111, 159), (178, 249, 242)), 1, 2.10),
    ("FASTAPI", 148, 60, 6, ((175, 148, 241), (96, 71, 154), (224, 199, 255)), 1, 5.65),
    ("SUPABASE", 177, 67, 7, ((101, 207, 155), (41, 116, 110), (180, 245, 182)), 1, 3.45),
]
ICON_URLS = {
    "stack-web.svg": "https://skillicons.dev/icons?i=python,ts,js,react,nextjs,nodejs&perline=6",
    "stack-data.svg": "https://skillicons.dev/icons?i=fastapi,flask,supabase,sqlite,mongodb,git&perline=6",
}


def text(draw: ImageDraw.ImageDraw, value: str, x: int, y: int, color, scale: int = 1) -> None:
    for char in value.upper():
        for row, pixels in enumerate(FONT[char].split("/")):
            for column, pixel in enumerate(pixels):
                if pixel == "1":
                    left, top = x + column * scale, y + row * scale
                    draw.rectangle((left, top, left + scale - 1, top + scale - 1), fill=color)
        x += 4 * scale


def planet(draw: ImageDraw.ImageDraw, x: int, y: int, radius: int, colors, ringed: bool) -> None:
    base, shadow, light = colors
    if ringed:
        draw.ellipse((x - radius - 6, y - 3, x + radius + 6, y + 3), outline=light)
    draw.ellipse((x - radius - 1, y - radius - 1, x + radius + 1, y + radius + 1), fill=(12, 22, 40))
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=shadow)
    draw.ellipse((x - radius, y - radius, x + radius - 2, y + radius - 2), fill=base)
    draw.line((x - radius + 2, y - 2, x + radius - 3, y - 2), fill=light)
    draw.point((x - 2, y - radius + 1), fill=light)
    draw.line((x + 1, y + 2, x + radius - 1, y + 2), fill=shadow)
    if ringed:
        draw.arc((x - radius - 6, y - 3, x + radius + 6, y + 3), 0, 180, fill=light)


def scene(logo: Image.Image, frame: int) -> Image.Image:
    phase = frame / FRAMES
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)

    # Quiet, fixed star field: brightness varies without shuffling the pixels.
    randomizer = random.Random(73)
    for index in range(100):
        x, y = randomizer.randrange(10, WIDTH - 10), randomizer.randrange(25, HEIGHT - 20)
        brightness = (math.sin(phase * math.tau + index * 1.71) + 1) / 2
        color = (43, 60, 91) if brightness < .75 else (94, 122, 163)
        draw.point((x, y), fill=color)
        if index % 19 == 0:
            draw.line((x - 1, y, x + 1, y), fill=color)
            draw.line((x, y - 1, x, y + 1), fill=color)

    cx, cy = CENTER
    for _, rx, ry, *_ in WORLDS:
        draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(24, 39, 61))

    # Sparse asteroid belt between the middle and outer worlds.
    for index in range(48):
        angle = index * math.tau / 48
        draw.point((round(cx + 133 * math.cos(angle)), round(cy + 55 * math.sin(angle))), fill=(54, 55, 78))

    # A passing comet stays in the upper part of the scene and fades before wrap.
    if .38 < phase < .58:
        travel = (phase - .38) / .20
        x, y = round(62 + travel * 113), round(31 + travel * 17)
        for step in range(17, -1, -1):
            draw.point((x - step, y - step // 4), fill=(60 + (17 - step) * 8, 90 + (17 - step) * 7, 133 + (17 - step) * 5))

    # A filled star with convection and a soft circular corona. No pointed rays
    # or orbiting sparks: the CH mark sits on the sun rather than in a black hole.
    pulse = (math.sin(phase * math.tau * 3) + 1) / 2
    for radius, base in ((28, (18, 19, 30)), (25, (33, 25, 32)), (23, (61, 35, 31)), (21, (125, 60, 31))):
        color = tuple(round(channel + pulse * (8 if index == 0 else 3)) for index, channel in enumerate(base))
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)
    sun_colors = [(211, 98, 36), (238, 139, 48), (252, 179, 70), (255, 208, 105), (255, 226, 146)]
    for dy in range(-19, 20):
        for dx in range(-19, 20):
            if dx * dx + dy * dy <= 19 * 19:
                radial = 1 - math.sqrt(dx * dx + dy * dy) / 19
                convection = math.sin(dx * .52 + phase * math.tau * 2) * math.cos(dy * .65 - phase * math.tau * 3)
                level = max(0, min(4, round(1 + radial * 2 + convection * .85)))
                draw.point((cx + dx, cy + dy), fill=sun_colors[level])
    image.paste((137, 61, 28), (cx - 13, cy - 13), logo)
    image.paste((255, 245, 205), (cx - 14, cy - 14), logo)

    # Paint far planets first, then the foreground planets.
    positions = []
    for index, (_, rx, ry, radius, colors, revolutions, offset) in enumerate(WORLDS):
        angle = phase * math.tau * revolutions + offset
        x, y = round(cx + rx * math.cos(angle)), round(cy + ry * math.sin(angle))
        positions.append((y, x, radius, colors, index == 4))
    for y, x, radius, colors, ringed in sorted(positions):
        planet(draw, x, y, radius, colors, ringed)

    # Terminal-inspired frame and a fixed, readable palette legend.
    draw.rounded_rectangle((0, 0, WIDTH - 1, HEIGHT - 1), radius=5, outline=(41, 56, 80))
    draw.line((1, 19, WIDTH - 2, 19), fill=(34, 48, 71))
    for x, color in ((11, (233, 122, 139)), (19, (236, 193, 114)), (27, (106, 210, 166))):
        draw.rectangle((x, 8, x + 3, 11), fill=color)
    text(draw, "ELECTRIFIEDCHAN / DEV UNIVERSE", 41, 8, (177, 198, 222))
    draw.line((12, 175, WIDTH - 13, 175), fill=(27, 41, 61))
    for index, (name, _, _, _, colors, *_rest) in enumerate(WORLDS):
        x = 16 + index * 66
        draw.rectangle((x, 181, x + 3, 184), fill=colors[0])
        text(draw, name, x + 7, 181, (144, 165, 190))

    return image.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.Resampling.NEAREST)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-icons", action="store_true")
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    source = ASSETS / "avatar-source.png"
    if not source.exists():
        parser.error("Run scripts/build_logo.py first to fetch your avatar.")
    with Image.open(source) as avatar:
        logo = ImageOps.fit(avatar.convert("L"), (28, 28), method=Image.Resampling.LANCZOS)
        logo = logo.point(lambda value: 255 if value > 155 else 0)
        # Remove disconnected decorative specks, retaining the main CH strokes.
        remaining = {(x, y) for y in range(28) for x in range(28) if logo.getpixel((x, y))}
        while remaining:
            pending = [remaining.pop()]
            component = set(pending)
            while pending:
                x, y = pending.pop()
                for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if neighbor in remaining:
                        remaining.remove(neighbor)
                        component.add(neighbor)
                        pending.append(neighbor)
            if len(component) < 7:
                for point in component:
                    logo.putpixel(point, 0)

    frames = [scene(logo, frame) for frame in range(FRAMES)]
    sample = Image.new("RGB", (WIDTH * SCALE * 4, HEIGHT * SCALE))
    for index in range(4):
        sample.paste(frames[index * (FRAMES // 4)], (index * WIDTH * SCALE, 0))
    palette = sample.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    output = ASSETS / "solar-system.gif"
    indexed[0].save(output, save_all=True, append_images=indexed[1:], duration=FRAME_MS,
                    loop=0, disposal=1, optimize=True)
    frames[0].save(ASSETS / "solar-system-static.png", optimize=True)
    print(f"Solar system: {WIDTH * SCALE}x{HEIGHT * SCALE}, {FRAMES} frames, {FRAMES * FRAME_MS / 1000:g}s loop, {output.stat().st_size / 1024:.0f} KiB")

    for name, url in ICON_URLS.items():
        output = ASSETS / name
        if args.refresh_icons or not output.exists():
            request = Request(url, headers={"User-Agent": "electrifiedchan-profile-assets"})
            with urlopen(request, timeout=30) as response:
                svg = response.read()
            svg = b"\n".join(line.rstrip() for line in svg.splitlines()).strip() + b"\n"
            if ElementTree.fromstring(svg).tag != "{http://www.w3.org/2000/svg}svg":
                raise ValueError(f"Expected an SVG for {name}")
            output.write_bytes(svg)
        print(f"Tech icons: {name}")


if __name__ == "__main__":
    main()
