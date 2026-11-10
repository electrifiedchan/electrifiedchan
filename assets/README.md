# Profile artwork and logos

## Typing introduction

`intro-typing.svg` types **Hey, I am electrifiedchan** in a 7.5-second loop and holds the completed line for 2.7 seconds. The text, reveal boundary, and cursor share a fixed 20-pixel character grid. The cursor stays visible during typing/deletion and blinks only during the pause. The SVG adapts to light/dark mode, shows the complete line for reduced motion, and uses no external service.

## Record-rack footer

`record-rack.svg` is the supplied 832 × 500 animated turntable illustration used at the bottom of the README. A hand plays four project records in a 72-second sequence, with a typed introduction for each project. Its own reduced-motion styles show a static presentation. The SVG is used directly.

## Raster scene assets

Each GIF has a matching `<name>-static.png` for reduced-motion viewing. These raster scenes use **120 ms per frame**, two-times nearest-neighbor enlargement, and integer animation cycles. The reef assets below are archived; the README footer now displays the record rack.

| Asset | Dimensions | Frames | Loop | Palette samples / colors | GIF KiB | Static PNG KiB |
| --- | --- | ---: | ---: | --- | ---: | ---: |
| `sunset-cover.gif` | 832 × 288 | 120 | 14.4 s | 4 / 128 | 380.26 | 10.33 |
| `solar-system.gif` | 832 × 380 | 180 | 21.6 s | 4 / 128 | 692.47 | 8.28 |
| `project-aquarium.gif` | 832 × 416 | 240 | 28.8 s | 16 / 192 | 2031.69 | 23.67 |

Sizes use 1 KiB = 1024 bytes. All GIFs fit the 2 MiB / 2048 KiB per-file budget; the reef has 16.31 KiB of headroom. Rebuilding after future art edits may change these sizes.

### Sunset cover

Orange clouds with depth-dependent drift, six-cycle reflection ripples, five-cycle opposing gaps, three-cycle reeds, a two-cycle corona pulse, warm glare, and a three-bird flock. The birds cross once per loop and flap at 30 cycles per loop.

### Solar-system skills scene

The CH mark is rendered from the checked-in `avatar-source.png`, which remains a required build input. The two innermost planets complete two revolutions per loop (10.8 seconds each); the outer four complete one (21.6 seconds). An irregular, seeded asteroid belt rotates once per loop. The comet has a gently twinkling four-point glare, completing eight sparkle cycles per loop, and a growing/shrinking trail. Near/far planets change size and highlight tint. Sun convection uses four/six cycles, the corona uses six, and stars use one/two/three. The scene title is drawn at scale 2.

### Project reef (archived)

| Project | Fish | Fin cycles per loop |
| --- | --- | ---: |
| G.U.A.R.D. | Blue puffer | 32 |
| GitReal | Purple striped reef fish | 40 |
| TeamTruth | Mint tetra school | 48 |
| ExamHub | Orange clownfish | 40 |

Fish enter and exit beyond either edge. Background kelp uses three cycles at amplitude 4; foreground kelp uses four at amplitude 6. Crab steps settle at turnarounds. Eight bubbles originate at the anchor, hull, or sponges; twelve follow ambient paths. The chain extends from the top edge to the anchor ring.

The puffer inflates by up to four source pixels for ten frames when the school first passes it, centered on frame 58. Twelve subtle caustic flecks use existing sand colors and complete four cycles. A real-text legend below the image complements the scale-2 title and the image's small color key.

## Rebuilding

Run from the repository root with Python 3.10+ and **Pillow==12.3.0**:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/build_pixel_worlds.py --scene cover
python scripts/build_pixel_worlds.py --scene aquarium
python scripts/build_profile_art.py
```

The normal build reuses local avatar and icon inputs. `--refresh-icons` is an optional manual refresh of the cached Skill Icons strips. Visitors need no Python runtime or animation service.

## Social and technology icons

- `linkedin.svg`, `github.svg`, `email.svg` — local branded social buttons.
- `stack-web.svg`, `stack-data.svg` — locally cached technology-logo strips.
- Social paths: [Simple Icons v11.15.0](https://github.com/simple-icons/simple-icons/tree/11.15.0), distributed under [CC0](https://github.com/simple-icons/simple-icons/blob/11.15.0/LICENSE.md).
- Tech tiles: [Skill Icons](https://github.com/tandpfun/skill-icons), with the included [MIT license](SKILL_ICONS_LICENSE.txt).

## WebP and future work

The published README uses GIFs and static PNGs. Animated WebP is not generated or selected: it must first pass a scratch public GitHub repository test in light mode, dark mode, and on mobile. The interactive project CD player is also deferred. See [future ideas](../docs/FUTURE_IDEAS.md).

See [the design notes](../docs/PROFILE_DESIGN.md) for reference links and validation measurements.
