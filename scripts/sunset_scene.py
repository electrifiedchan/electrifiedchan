"""Wide original sunset-lake pixel scene inspired by the supplied GIPHY link."""

from functools import lru_cache
import math
import random

from PIL import Image, ImageDraw


WIDTH, HEIGHT, SCALE = 416, 144, 2
COVER_FRAMES = 120


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


@lru_cache(maxsize=12)
def cloud(width, height, seed, colors):
    rng = random.Random(seed)
    mask = Image.new('L', (width, height), 0)
    d = ImageDraw.Draw(mask)
    for index in range(15):
        x = round(height / 2 + index * (width - height) / 14)
        radius = rng.randrange(max(4, height // 5), max(6, height // 2))
        y = round(height * .55 + math.sin(index * .65) * height * .17)
        d.ellipse((x - radius, y - radius, x + radius, y + radius // 2), fill=255)
    sprite = Image.new('RGBA', mask.size)
    for y in range(height):
        for x in range(width):
            if not mask.getpixel((x, y)):
                continue
            above = y > 1 and mask.getpixel((x, y - 2))
            noise = (x * 19 + y * 31 + seed * 7) % 29
            shade = colors[0] if y > height * .58 else colors[1]
            if not above:
                shade = colors[2]
            elif noise < 4 and y < height * .7:
                shade = colors[2] if (x + y) % 2 else colors[1]
            sprite.putpixel((x, y), (*shade, 255))
    return sprite


def sunset(frame):
    phase = (frame % COVER_FRAMES) / COVER_FRAMES
    image = Image.new('RGB', (WIDTH, HEIGHT))
    d = ImageDraw.Draw(image)
    for y in range(98):
        d.line((0, y, WIDTH, y), fill=mix((224, 66, 41), (255, 146, 70), y / 98))
    # Small dithering patches keep the sky painterly at this pixel scale.
    for y in range(0, 91, 2):
        for x in range(0, WIDTH, 2):
            if math.sin(x * .041 + y * .065) + math.cos(x * .023 - y * .11) > 1.55:
                if (x + y) % 4 == 0:
                    d.point((x, y), fill=mix((235, 91, 49), (255, 168, 85), y / 98))

    # Golden corona and warm horizontal glare, followed by the solar disc.
    sx, sy = 214, 48
    glow = .5 + .5 * math.sin(phase * math.tau)
    corona_pulse = round(.5 + .5 * math.sin(phase * math.tau * 2))
    for radius, color in ((35, (246, 137, 70)), (31, (252, 158, 81)), (27, (255, 190, 106))):
        radius += corona_pulse
        d.ellipse((sx - radius, sy - radius, sx + radius, sy + radius), fill=color)
    glare_extent = round(62 + glow * 8)
    d.line((sx - glare_extent, sy, sx + glare_extent, sy), fill=(255, 205, 116))
    d.line((sx - 37, sy - 1, sx + 37, sy - 1), fill=(255, 205, 116))
    vertical_glare = 27 + round(glow * 3)
    d.line((sx, sy - vertical_glare, sx, sy + vertical_glare), fill=(255, 212, 128))
    d.ellipse((sx - 22, sy - 22, sx + 22, sy + 22), fill=(255, 232, 149))
    d.ellipse((sx - 19, sy - 20, sx + 19, sy + 17), fill=(255, 238, 165))

    # Broad clouds are independently redrawn, extended beyond both frame edges.
    formations = (
        (-29, 0, 224, 34, 3, ((226, 76, 43), (245, 121, 61), (255, 175, 90))),
        (202, -8, 243, 39, 8, ((228, 81, 44), (247, 132, 64), (255, 188, 105))),
        (-49, 32, 206, 42, 12, ((232, 94, 50), (250, 154, 78), (255, 209, 123))),
        (277, 28, 189, 44, 20, ((239, 116, 60), (254, 169, 87), (255, 219, 133))),
        (117, 63, 123, 25, 27, ((245, 129, 62), (255, 181, 91), (255, 221, 137))),
    )
    for index, (x, y, width, height, seed, colors) in enumerate(formations):
        drift = round(math.sin(phase * math.tau + index * .8) * (3, 3, 6, 6, 8)[index])
        sprite = cloud(width, height, seed, colors)
        image.paste(sprite, (x + drift, y), sprite)

    # Distant shore and jagged treetops across the horizon.
    rng = random.Random(208)
    d.rectangle((0, 96, WIDTH, 103), fill=(85, 62, 76))
    for x in range(0, WIDTH, 3):
        height = rng.randrange(1, 5)
        d.line((x, 97, x, 97 - height), fill=(92, 65, 75))
    for y in range(104, HEIGHT):
        d.line((0, y, WIDTH, y), fill=mix((245, 145, 73), (234, 106, 61), (y - 104) / 40))

    # The reflection breaks into gently moving horizontal gold ripples.
    for y in range(104, 144):
        width = 29 + (y - 104) * 1.7
        offset = math.sin(y * .78 + phase * math.tau * 6) * 5
        left, right = round(sx - width + offset), round(sx + width + offset)
        color = (255, 223, 132) if y % 4 < 2 else (255, 194, 106)
        d.line((left, y, right, y), fill=color)
        if y % 3 == 0:
            gap = round(sx + math.sin(y * .9 - phase * math.tau * 5) * width)
            d.line((gap, y, gap + 12, y), fill=(248, 159, 80))
    for index in range(21):
        x = (index * 37 + 11) % WIDTH
        y = 107 + index % 6 * 5
        shift = round(math.sin(phase * math.tau + index) * 4)
        d.line((x + shift, y, x + shift + 7 + index % 8, y), fill=(247, 178, 91))

    # A restrained lens-glare accent, kept in the same warm pixel palette.
    for x, y, radius in ((251, 72, 3), (268, 89, 5)):
        color = mix((249, 160, 81), (255, 225, 154), .55 + glow * .25)
        d.ellipse((x - radius, y - radius, x + radius, y + radius), outline=color)
    glint = round(3 + glow * 3)
    d.line((sx - glint, 116, sx + glint, 116), fill=(255, 241, 174))
    d.line((sx, 115, sx, 117), fill=(255, 241, 174))

    # Low silhouetted banks frame the water; reeds have gentle cyclical sway.
    ink = (66, 49, 67)
    d.polygon(((0, 119), (32, 120), (57, 128), (89, 126), (113, 137), (155, 144), (0, 144)), fill=ink)
    d.polygon(((416, 117), (385, 120), (363, 126), (343, 127), (319, 136), (280, 144), (416, 144)), fill=ink)
    for index, (x, base, height) in enumerate(((23, 126, 45), (50, 132, 27), (85, 137, 33), (332, 141, 66), (355, 134, 48), (391, 127, 36))):
        lean = (-12 if index > 2 else 6) + math.sin(phase * math.tau * 3 + index) * 2.5
        stem = [(round(x + lean * t / height), base - t) for t in range(height)]
        d.line(stem, fill=ink)
        for step in range(7, height - 3, 8):
            px, py = stem[step]
            direction = -1 if step % 16 else 1
            d.line((px, py, px + direction * 5, py - 5), fill=ink)
            d.line((px + direction * 4, py - 4, px + direction * 7, py - 5), fill=ink)
    for index in range(50):
        x = rng.randrange(WIDTH)
        y = 141 if 120 < x < 290 else 128 + rng.randrange(12)
        d.line((x, 144, x - 2, y), fill=ink)

    # One crossing per loop; all three birds are outside the frame at wraparound.
    lead_x = round(-20 + ((phase + .18) % 1) * (WIDTH + 40))
    lead_y = 41 + round(math.sin(phase * math.tau) * 3)
    flap_up = math.sin(phase * math.tau * 30) > 1e-9
    for dx, dy in ((0, 0), (-9, -6), (-17, 2)):
        x, y = lead_x + dx, lead_y + dy
        wing_y = y if flap_up else y + 2
        d.line((x - 3, wing_y, x, y + 1, x + 3, wing_y), fill=ink)
    return image.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.Resampling.NEAREST)
