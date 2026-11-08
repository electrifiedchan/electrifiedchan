"""Build the wide sunset-lake cover and original project reef.

Run from the repository root: python scripts/build_pixel_worlds.py
Visual references and asset credits are recorded in docs/PROFILE_DESIGN.md.
"""

from __future__ import annotations

import argparse
from PIL import Image

from build_profile_art import ASSETS
from reef_scene import REEF_FRAMES, aquarium
from sunset_scene import COVER_FRAMES, sunset


FRAMES, FRAME_MS = 120, 120


def export(name: str, renderer, count: int = FRAMES) -> None:
    frames = [renderer(frame) for frame in range(count)]
    width, height = frames[0].size
    samples = Image.new("RGB", (width * 4, height))
    for index in range(4):
        samples.paste(frames[index * count // 4], (index * width, 0))
    palette = samples.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    output = ASSETS / f"{name}.gif"
    indexed[0].save(output, save_all=True, append_images=indexed[1:], duration=FRAME_MS,
                    loop=0, disposal=1, optimize=True)
    frames[0].save(ASSETS / f"{name}-static.png", optimize=True)
    print(f"{name}: {width}x{height}, {count} frames, {count * FRAME_MS / 1000:g}s, {output.stat().st_size / 1024:.0f} KiB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", choices=("all", "cover", "aquarium"), default="all")
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    if args.scene in ("all", "cover"):
        export("sunset-cover", sunset, COVER_FRAMES)
    if args.scene in ("all", "aquarium"):
        export("project-aquarium", aquarium, REEF_FRAMES)
