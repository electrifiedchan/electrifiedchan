"""An original open-water pixel reef with free-swimming project puffer fish.

Inspiration: the user's blue puffer GIF and red-coral/tube-sponge Pinterest pin.
All sprites, scenery, and paths are drawn here; no reference image is embedded.
"""

from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw

from build_profile_art import text


WIDTH, HEIGHT, SCALE = 416, 208, 2
REEF_FRAMES = 240
FISH_PALETTES = (
    ((22, 190, 205), (12, 122, 160), (102, 236, 227), (29, 75, 182)),
    ((172, 112, 223), (98, 65, 157), (230, 177, 242), (54, 104, 190)),
    ((59, 198, 159), (24, 125, 117), (148, 239, 194), (20, 107, 128)),
    ((239, 182, 80), (178, 109, 48), (255, 225, 154), (209, 104, 56)),
)


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def puffer(colors, beat: float, blink: bool = False) -> Image.Image:
    """Fuller 64x52 silhouette, shaded belly, blue fan tail, big eye, pink lips."""
    body, shadow, light, fin = colors
    ink = mix(shadow, (4, 29, 57), .55)
    sprite = Image.new("RGBA", (64, 52))
    d = ImageDraw.Draw(sprite)
    flap = round(math.sin(beat) * 3)

    # Stepped fan tail with overlapping blue scales rather than a flat rectangle.
    d.polygon(((20, 21), (8, 13 + flap), (3, 15 + flap), (0, 20), (0, 35), (4, 41 - flap), (9, 42 - flap), (22, 33)), fill=ink)
    d.polygon(((20, 23), (8, 16 + flap), (4, 18 + flap), (2, 22), (2, 34), (6, 38 - flap), (10, 38 - flap), (22, 32)), fill=fin)
    for y in (20, 26, 32):
        d.rectangle((3, y, 8, y + 3), fill=mix(fin, light, .32))
    d.line((12, 22, 12, 35), fill=shadow, width=3)
    d.line((17, 24, 17, 32), fill=body, width=2)
    d.polygon(((26, 12), (22, 3), (31, 3), (38, 9), (42, 5 + flap), (46, 14)), fill=fin)
    d.line((26, 5, 33, 7), fill=mix(fin, light, .45), width=2)
    d.polygon(((21, 38), (22, 47), (28, 46), (32, 39)), fill=fin)

    d.ellipse((15, 9, 61, 49), fill=ink)
    d.ellipse((17, 10, 60, 47), fill=shadow)
    d.ellipse((19, 10, 58, 43), fill=body)
    d.ellipse((27, 11, 55, 38), fill=light)
    # Broken highlights follow the curve of the back.
    d.line((25, 14, 31, 12, 42, 12), fill=mix(light, (238, 255, 248), .45), width=2)
    d.line((20, 19, 24, 15), fill=mix(body, light, .6), width=2)
    d.polygon(((18, 34), (23, 37), (30, 36), (37, 39), (47, 37), (58, 33), (57, 41), (49, 47), (36, 49), (25, 45), (20, 41)), fill=(228, 240, 229))
    d.polygon(((23, 42), (32, 45), (46, 45), (55, 40), (50, 46), (36, 48), (26, 45)), fill=(176, 200, 198))
    for x, y, width in ((27, 36, 3), (38, 39, 2), (47, 36, 3), (54, 34, 2)):
        d.rectangle((x, y, x + width, y + 2), fill=body)
    for x, y in ((20, 26), (25, 22), (46, 17), (50, 21)):
        d.point((x, y), fill=shadow)

    # One expressive eye with a bright catchlight and colored lower reflection.
    d.ellipse((33, 17, 50, 36), fill=mix(shadow, body, .3))
    d.ellipse((34, 17, 50, 35), fill=(237, 255, 242))
    if blink:
        d.ellipse((34, 17, 50, 35), fill=body)
        d.line((36, 27, 48, 27), fill=ink, width=2)
    else:
        d.ellipse((37, 19, 49, 33), fill=(6, 24, 37))
        d.rectangle((44, 20, 47, 23), fill=(255, 255, 249))
        d.rectangle((39, 29, 43, 32), fill=shadow)
        d.point((41, 28), fill=body)
    d.rectangle((56, 29, 63, 36), fill=(187, 53, 91))
    d.rectangle((56, 28, 62, 34), fill=(250, 117, 148))
    d.line((58, 29, 62, 29), fill=(255, 207, 204))
    d.line((60, 33, 63, 33), fill=(255, 173, 180))
    d.polygon(((23, 27), (15, 24 + flap), (16, 32), (25, 33)), fill=fin)
    d.line((18, 28, 22, 30), fill=body, width=2)
    return sprite


def striped_fish(beat: float) -> Image.Image:
    """Tall-finned purple reef fish: a different silhouette from the puffer."""
    sprite = Image.new('RGBA', (62, 56))
    d = ImageDraw.Draw(sprite)
    flap = round(math.sin(beat) * 2)
    d.polygon(((22, 24), (6, 15 + flap), (2, 18), (2, 38), (7, 41 - flap), (23, 31)), fill=(85, 66, 157))
    d.line((7, 21, 7, 35), fill=(181, 139, 230), width=2)
    d.polygon(((22, 23), (33, 1), (43, 19), (49, 27), (42, 39), (32, 54), (24, 35)), fill=(72, 50, 119))
    d.polygon(((24, 23), (33, 5), (40, 21), (53, 27), (42, 37), (33, 49), (27, 33)), fill=(152, 113, 207))
    d.ellipse((19, 16, 56, 40), fill=(187, 150, 230))
    d.ellipse((24, 18, 55, 37), fill=(220, 194, 241))
    for x in (28, 38):
        d.polygon(((x, 17), (x + 4, 18), (x + 1, 39), (x - 3, 38)), fill=(100, 77, 161))
    d.line((31, 10, 29, 19), fill=(245, 210, 129))
    d.line((32, 41, 32, 47), fill=(236, 190, 119))
    d.ellipse((45, 22, 52, 29), fill=(239, 245, 229))
    d.ellipse((47, 23, 52, 28), fill=(11, 28, 42))
    d.point((50, 23), fill=(255, 255, 244))
    d.line((55, 29, 59, 29), fill=(241, 169, 174), width=2)
    d.polygon(((37, 30), (31, 35 + flap), (41, 34)), fill=(130, 109, 186))
    return sprite


def tetra(beat: float) -> Image.Image:
    """Slender mint schooling fish with a bright lateral stripe."""
    sprite = Image.new('RGBA', (42, 22))
    d = ImageDraw.Draw(sprite)
    flap = round(math.sin(beat) * 2)
    d.polygon(((14, 10), (2, 3 + flap), (5, 10), (2, 19 - flap), (15, 13)), fill=(45, 129, 142))
    d.polygon(((13, 9), (23, 2), (26, 9), (34, 10), (28, 15), (23, 21), (18, 15)), fill=(47, 139, 136))
    d.ellipse((11, 7, 39, 16), fill=(58, 179, 157))
    d.line((15, 9, 34, 9), fill=(159, 245, 214), width=2)
    d.line((16, 14, 33, 14), fill=(215, 231, 176))
    d.rectangle((33, 9, 35, 11), fill=(8, 31, 43))
    d.point((34, 9), fill=(237, 255, 234))
    return sprite


def clownfish(beat: float) -> Image.Image:
    """Orange reef fish with black-edged white bands and a rounded fan tail."""
    sprite = Image.new('RGBA', (64, 38))
    d = ImageDraw.Draw(sprite)
    flap = round(math.sin(beat) * 2)
    d.polygon(((21, 16), (8, 6 + flap), (3, 8), (2, 28), (8, 31 - flap), (23, 24)), fill=(81, 53, 53))
    d.polygon(((20, 17), (8, 9 + flap), (5, 10), (5, 27), (9, 28 - flap), (22, 22)), fill=(234, 140, 58))
    d.polygon(((23, 12), (30, 3), (40, 4), (49, 13)), fill=(126, 72, 42))
    d.polygon(((27, 27), (33, 36), (43, 31), (48, 25)), fill=(185, 99, 45))
    d.ellipse((16, 9, 60, 31), fill=(70, 47, 48))
    d.ellipse((18, 10, 59, 30), fill=(237, 145, 54))
    d.ellipse((22, 12, 56, 27), fill=(255, 182, 79))
    for x in (25, 40):
        d.polygon(((x, 11), (x + 7, 10), (x + 4, 30), (x - 2, 29)), fill=(74, 56, 53))
        d.polygon(((x + 1, 12), (x + 5, 11), (x + 2, 29), (x, 28)), fill=(246, 235, 204))
    d.ellipse((49, 15, 56, 22), fill=(251, 231, 184))
    d.ellipse((51, 16, 56, 21), fill=(13, 31, 42))
    d.point((54, 16), fill=(255, 255, 238))
    d.line((57, 24, 62, 24), fill=(217, 98, 58), width=2)
    d.polygon(((35, 22), (30, 29 + flap), (42, 26)), fill=(212, 109, 45))
    return sprite


def swimmer_pose(index: int, phase: float):
    """Two straight crossings per loop; all direction changes occur off-screen."""
    offset = (.15, .21, .365, .13)[index]
    journey = ((phase + offset) % 1) * 2
    leg = int(journey)
    progress = journey - leg
    direction = (1 if index % 2 == 0 else -1) * (1 if leg == 0 else -1)
    margin = 84
    span = WIDTH + margin * 2
    x = -margin + progress * span if direction > 0 else WIDTH + margin - progress * span
    y = (69, 102, 43, 127)[index] + 6 * math.sin(phase * math.tau * 2 + index)
    return x, y, direction


def draw_swimmer(image, index: int, phase: float, offset=(0, 0), size=.84):
    x, y, direction = swimmer_pose(index, phase)
    x, y = x + offset[0], y + offset[1]
    blink = (phase + .13 + index * .21) % 1 < .009
    beat = phase * math.tau * 14
    sprite = (puffer(FISH_PALETTES[0], beat, blink) if index == 0 else
              striped_fish(beat) if index == 1 else
              tetra(beat) if index == 2 else clownfish(beat))
    if direction < 0:
        sprite = sprite.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    sprite = sprite.resize((round(sprite.width * size), round(sprite.height * size)), Image.Resampling.NEAREST)
    image.paste(sprite, (round(x - sprite.width / 2), round(y - sprite.height / 2)), sprite)


def kelp(draw, x, base, height, phase, palette, seed=0):
    dark, middle, light = palette
    sway = math.sin(phase * math.tau + seed) * 4
    stem = []
    for step in range(height):
        px = x + round(math.sin(step * .11 + seed) * sway * step / height)
        stem.append((px, base - step))
    draw.line(stem, fill=dark, width=3)
    for step in range(7, height - 3, 9):
        px, py = stem[step]
        side = 1 if step % 18 < 9 else -1
        length = 7 + step // 12
        draw.polygon(((px, py + 3), (px + side * length, py - 5), (px + side * (length + 2), py - 11), (px + side * 3, py - 3)), fill=middle)
        draw.line((px, py, px + side * length, py - 7), fill=light)


def coral(draw, x, base, scale=1.0, blue=False):
    colors = ((14, 74, 103), (21, 143, 166), (93, 218, 211)) if blue else ((103, 27, 57), (210, 63, 91), (255, 131, 120))
    # Hand-shaped branches with short forks, matching the reference's silhouette.
    branches = [
        [(0, 0), (-5, -18), (-12, -38), (-10, -59), (-16, -74)],
        [(-5, -18), (9, -32), (17, -52), (15, -66)],
        [(-12, -38), (-26, -46), (-30, -60)],
        [(-10, -55), (-1, -65), (0, -76)],
        [(9, -32), (30, -40), (36, -55)],
        [(0, -12), (-27, -27), (-36, -28)],
        [(-26, -46), (-39, -44)],
        [(17, -48), (30, -57), (32, -66)],
        [(25, -39), (43, -39)],
        [(-13, -67), (-26, -67), (-29, -74)],
        [(-22, -25), (-23, -38)],
    ]
    for branch in branches:
        points = [(x + round(px * scale), base + round(py * scale)) for px, py in branch]
        draw.line(points, fill=colors[0], width=max(3, round(7 * scale)))
        draw.line([(px - 1, py - 1) for px, py in points], fill=colors[1], width=max(2, round(4 * scale)))
        draw.line([(px - 2, py - 2) for px, py in points], fill=colors[2], width=1)


def sponges(draw, x, y, scale=1.0):
    for dx, dy, height, radius in ((-12, 0, 14, 5), (0, 0, 20, 7), (13, 1, 12, 5), (-5, 8, 12, 6), (8, 9, 10, 5)):
        px, py = x + round(dx * scale), y + round(dy * scale)
        h, r = round(height * scale), max(3, round(radius * scale))
        draw.ellipse((px - r, py - h, px + r, py + 3), fill=(77, 44, 117))
        draw.line((px - r + 2, py - h + 5, px - r + 2, py), fill=(161, 78, 181), width=2)
        draw.ellipse((px - r, py - h, px + r, py - h + r + 1), fill=(205, 100, 210))
        draw.ellipse((px - r + 2, py - h + 2, px + r - 2, py - h + r - 1), fill=(17, 51, 85))
        draw.point((px - r + 1, py - h + 1), fill=(255, 166, 230))


def anchor(image, x, y):
    sprite = Image.new("RGBA", (70, 78))
    d = ImageDraw.Draw(sprite)
    ink, steel, shine = (23, 54, 68), (87, 136, 143), (160, 202, 194)
    d.ellipse((27, 2, 43, 18), outline=ink, width=5)
    d.ellipse((29, 3, 41, 16), outline=steel, width=3)
    d.arc((29, 3, 41, 16), 165, 280, fill=shine, width=1)
    paths = [((35, 16), (35, 65)), ((17, 26), (53, 26)), ((11, 43), (14, 54), (24, 64), (35, 69), (46, 64), (56, 54), (59, 43))]
    for points in paths:
        d.line(points, fill=ink, width=7)
        d.line(points, fill=steel, width=4)
        d.line([(px - 1, py - 1) for px, py in points], fill=shine, width=1)
    for side in (-1, 1):
        px = 35 + side * 24
        d.polygon(((px, 40), (px - side * 10, 49), (px + side * 4, 51)), fill=steel)
        d.line((px, 40, px - side * 8, 48), fill=shine)
    for px, py in ((34, 34), (38, 57), (19, 56), (48, 63)):
        d.rectangle((px, py, px + 2, py + 2), fill=(139, 99, 70))
    sprite = sprite.rotate(-17, Image.Resampling.NEAREST, expand=True)
    image.paste(sprite, (x - sprite.width // 2, y - sprite.height), sprite)


def starfish(draw, x, y, radius=9):
    points = []
    for index in range(10):
        angle = -math.pi / 2 + index * math.pi / 5
        r = radius if index % 2 == 0 else radius * .38
        points.append((round(x + r * math.cos(angle)), round(y + r * math.sin(angle))))
    draw.polygon(points, fill=(213, 125, 58))
    for index in range(0, 10, 2):
        px, py = points[index]
        draw.line((x, y, px, py), fill=(255, 200, 102))


def crab_pose(phase):
    return 211 + 35 * math.sin(phase * math.tau), 183


def walking_crab(draw, phase):
    """Sideways crab with alternating feet and independently opening pincers."""
    x, y = crab_pose(phase)
    x = round(x)
    beat = phase * math.tau * 18
    dark, red, light = (113, 48, 51), (219, 91, 64), (255, 156, 101)
    draw.ellipse((x - 16, y - 1, x + 16, y + 4), fill=(106, 103, 84))
    for side in (-1, 1):
        for index in range(3):
            step = round(math.sin(beat + index * math.pi * .7 + side) * 2)
            root = (x + side * 7, y - 5 + index)
            knee = (x + side * (13 + index), y - 4 + index + step)
            foot = (x + side * (16 + index), y + 1 + step)
            draw.line((root, knee, foot), fill=dark, width=2)
            draw.line((root, knee), fill=red)
        claw_y = y - 15 + round(math.sin(beat / 3 + side) * 1)
        draw.line((x + side * 8, y - 8, x + side * 14, claw_y + 3), fill=red, width=3)
        cx = x + side * 17
        draw.ellipse((cx - 4, claw_y - 4, cx + 4, claw_y + 4), fill=red)
        opening = 1 + round((math.sin(beat / 3 + side) + 1) * 1.5)
        draw.polygon(((cx, claw_y), (cx - opening, claw_y - 5), (cx + opening, claw_y - 5)), fill=(15, 45, 56))
        draw.point((cx - 2, claw_y + 1), fill=light)
    draw.ellipse((x - 11, y - 13, x + 11, y - 2), fill=dark)
    draw.ellipse((x - 10, y - 13, x + 10, y - 4), fill=red)
    draw.line((x - 6, y - 12, x + 5, y - 12), fill=light)
    for eye_x in (x - 5, x + 5):
        draw.line((eye_x, y - 12, eye_x, y - 17), fill=red, width=2)
        draw.rectangle((eye_x - 1, y - 19, eye_x + 1, y - 16), fill=(248, 236, 206))
        draw.point((eye_x, y - 18), fill=(14, 27, 38))


def aquarium(frame: int) -> Image.Image:
    phase = frame / REEF_FRAMES
    image = Image.new("RGB", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(image)
    # Open water: depth gradient and slanted sunbeams, no glass walls/waterline.
    for y in range(HEIGHT):
        d.line((0, y, WIDTH, y), fill=mix((12, 67, 88), (5, 22, 44), min(1, y / 180)))
    for index, x in enumerate((-25, 75, 189, 327)):
        shift = round(math.sin(phase * math.tau + index) * 6)
        d.polygon(((x, 0), (x + 22, 0), (x + 90 + shift, 166), (x + 53 + shift, 166)), fill=(14, 53, 75))
        d.polygon(((x + 2, 0), (x + 6, 0), (x + 60 + shift, 143), (x + 54 + shift, 143)), fill=(17, 62, 81))
    # A distant reef ridge and small silhouettes establish depth behind the fish.
    d.polygon(((0, 151), (36, 139), (62, 148), (111, 135), (154, 144), (211, 129), (251, 141), (310, 134), (363, 141), (416, 129), (416, 186), (0, 186)), fill=(12, 48, 64))
    for index, x in enumerate((15, 60, 157, 214, 283, 370, 410)):
        kelp(d, x, 164, 39 + index % 3 * 9, phase, ((15, 55, 69), (20, 76, 82), (26, 91, 91)), index)
    for index in range(8):
        x = (index * 56 + phase * (WIDTH + 20)) % (WIDTH + 20) - 10
        y = 43 + index % 3 * 13 + math.sin(phase * math.tau + index) * 3
        d.ellipse((round(x), round(y), round(x + 6), round(y + 2)), fill=(36, 102, 118))
        d.polygon(((round(x), round(y + 1)), (round(x - 3), round(y - 1)), (round(x - 3), round(y + 3))), fill=(36, 102, 118))

    # Fish cross the whole frame, disappear beyond it, and re-enter from either
    # side. Margin is larger than every sprite, including school offsets.
    inhabitants = [(swimmer_pose(i, phase)[1], i) for i in (0, 1, 3)]
    inhabitants.append((swimmer_pose(2, phase)[1], 2))
    for _, index in sorted(inhabitants):
        if index == 2:
            for lag, offset, size in ((-.013, (-12, 12), .73), (-.006, (-4, -9), .8), (0, (14, 4), .87)):
                draw_swimmer(image, index, (phase + lag) % 1, offset, size)
        else:
            draw_swimmer(image, index, phase, size=(.88, .86, .8, .94)[index])

    # Warm rippled sand forms a curved clearing around the nautical objects.
    d.polygon(((0, 177), (45, 166), (98, 174), (146, 163), (207, 170), (256, 161), (321, 171), (378, 163), (416, 170), (416, 194), (0, 194)), fill=(88, 92, 83))
    d.polygon(((0, 184), (70, 175), (137, 180), (200, 174), (254, 168), (319, 176), (387, 170), (416, 177), (416, 194), (0, 194)), fill=(136, 126, 98))
    rng = random.Random(684)
    for index in range(230):
        x, y = rng.randrange(WIDTH), rng.randrange(179, 194)
        d.point((x, y), fill=rng.choice(((176, 158, 115), (111, 108, 88), (156, 142, 107))))
    for x, y, length in ((71, 185, 21), (179, 178, 30), (242, 184, 35), (316, 183, 24)):
        d.line((x, y, x + length, y - 1), fill=(189, 168, 123))
        d.line((x + 2, y + 2, x + length - 3, y + 1), fill=(102, 105, 87))

    # Foreground props overlap passing fish: coral thickets, sponges, and a
    # weathered anchor/chain, instead of four isolated project display stands.
    coral(d, 34, 180, .95)
    coral(d, 373, 179, .74)
    coral(d, 325, 187, .47, blue=True)
    for index in range(6):
        px, py = 105 + index * 4, 82 + index * 4
        d.ellipse((px - 2, py, px + 3, py + 7), outline=(79, 119, 129), width=2)
        d.point((px - 1, py + 1), fill=(129, 164, 165))
    anchor(image, 118, 185)
    # Broken hull planks partially buried in the middle of the reef.
    d.polygon(((179, 169), (196, 178), (235, 177), (249, 166), (242, 184), (194, 187)), fill=(49, 59, 65))
    for index in range(6):
        x = 190 + index * 9
        d.line((x, 174, x + 3, 184), fill=(91, 91, 81), width=2)
    d.line((187, 176, 240, 180), fill=(117, 112, 88))
    starfish(d, 270, 180, 10)
    starfish(d, 75, 186, 6)
    sponges(d, 45, 179, 1.15)
    sponges(d, 353, 179, .9)
    for index, (x, height) in enumerate(((4, 72), (15, 57), (149, 35), (287, 32), (400, 67), (414, 78))):
        kelp(d, x, 188, height, phase, ((10, 78, 84), (22, 140, 134), (94, 200, 167)), index + 2)
    # Two small shells with pearl highlights.
    for x, y in ((162, 184), (303, 186)):
        d.pieslice((x - 7, y - 8, x + 7, y + 2), 180, 360, fill=(200, 157, 136))
        for offset in (-4, 0, 4):
            d.line((x, y, x + offset, y - 6), fill=(242, 201, 172))

    walking_crab(d, phase)

    # Current-borne particles and bubbles at different depths.
    for index in range(20):
        travel = (phase * 2 + index / 20) % 1
        x = 16 + index * 47 % 390 + round(math.sin(travel * math.tau + index) * 5)
        y = round(190 - travel * 180)
        if 25 < y < 167:
            r = 1 if index % 4 else 2
            d.ellipse((x - r, y - r, x + r, y + r), outline=(68, 139, 157))
    text(d, "THE PROJECT REEF", 12, 9, (167, 205, 216))
    d.rectangle((0, 195, WIDTH, HEIGHT), fill=(7, 26, 43))
    for index, name in enumerate(("G.U.A.R.D.", "GITREAL", "TEAMTRUTH", "EXAMHUB")):
        x = 14 + index * 103
        d.rectangle((x, 201, x + 3, 204), fill=FISH_PALETTES[index][0])
        text(d, name, x + 8, 201, (143, 177, 191))
    return image.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.Resampling.NEAREST)
