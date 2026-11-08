# Profile artwork and logos

## Typing introduction

`intro-typing.svg` types **Hey, I am electrifiedchan** in a nine-second loop, holds the completed line for over three seconds, then resets. It adapts its text color to light/dark mode and shows the complete line without a cursor when reduced motion is requested. The SVG is self-contained and uses no external typing service.

## Pixel solar system

- `solar-system.gif` — original 832 × 380 pixel-art scene, with a seamless 21.6-second loop.
- `solar-system-static.png` — still version selected for reduced-motion viewing.
- `linkedin.svg`, `github.svg`, `email.svg` — linked social badges with real brand icons.
- `stack-web.svg`, `stack-data.svg` — two locally cached rows of technology logos.

The existing monogram is the central sun. Six colorful planets represent Python, TypeScript, JavaScript, React, FastAPI, and Supabase. The scene includes a ringed planet, an asteroid belt, twinkling stars, and a comet. Planet sizes and orbits are artistic choices, not live GitHub statistics.

```sh
python -m pip install -r scripts/requirements.txt
python scripts/build_profile_art.py
```

The script reuses the saved avatar and icon strips. Add `--refresh-icons` to fetch new icon strips from Skill Icons. The scene is drawn at 416 × 190 and enlarged with nearest-neighbor scaling for crisp pixel edges.

The solar system is displayed at full width in the **Tech stack** section. The sun now has a filled, warm solar surface with flowing convection, a circular corona, and a transparent CH monogram. Disconnected ornamental specks are removed from the tiny monogram mask; no pointed rays or orbiting sparks are drawn. The “PIXEL ORBITS” label has been removed.

## Sunset cover and project aquarium

- `sunset-cover.gif` / `sunset-cover-static.png` — 832 × 288 extended sunset-lake cover; warm clouds, golden sunlight, soft glare, moving reflections, and silhouetted reeds.
- `project-aquarium.gif` / `project-aquarium-static.png` — 832 × 416 open-water reef for the footer, with four fish silhouettes, a sideways-walking crab, a weathered anchor and chain, red coral, purple tube sponges, kelp, starfish, shells, and a sunken hull.

The sunset loops in 14.4 seconds; the reef loops in 28.8 seconds. All three active scenes use 120 ms per frame for a slightly calmer pace. Both are generated locally:

```sh
python scripts/build_pixel_worlds.py
```

To rebuild only the reef:

```sh
python scripts/build_pixel_worlds.py --scene aquarium
```

The reef's project colors are:

| Project | Fish |
| --- | --- |
| G.U.A.R.D. | A large blue puffer. |
| GitReal | A tall-finned purple striped reef fish. |
| TeamTruth | A small school of slender mint tetras. |
| ExamHub | An orange clownfish with dark-edged white bands. |

The footer labels form a color legend, not fixed fish stations. Fish cross the whole scene with small vertical drift, pass completely beyond either edge, then re-enter. Changes of direction happen only after the entire sprite is outside the frame; visible fish do not rotate, compress, or bounce at the border. The central crab scuttles left and right with alternating legs and moving pincers. Scene and sprite code lives in `scripts/reef_scene.py`; the cover is in `scripts/sunset_scene.py`. The mapping is decorative, not a live activity visualization. Reference links are recorded in [the design notes](../docs/PROFILE_DESIGN.md).

### Icon sources

- Social logo paths: [Simple Icons v11.15.0](https://github.com/simple-icons/simple-icons/tree/11.15.0), distributed under [CC0](https://github.com/simple-icons/simple-icons/blob/11.15.0/LICENSE.md). Brand names and marks belong to their respective owners.
- Tech tiles: [Skill Icons](https://github.com/tandpfun/skill-icons), [MIT license](SKILL_ICONS_LICENSE.txt). Exact request URLs are in `scripts/build_profile_art.py`; these SVGs are stored locally so viewing the profile does not call the service.

## Original standalone logo

- `avatar-source.png` — snapshot of the existing public GitHub avatar, downloaded by the build script.
- `logo-animated.gif` — standalone 320 × 320 logo animation, retained for reuse.
- `logo-static.png` — still version for reduced-motion viewing and static use.

The original monogram stays still while two electric-blue highlights travel around its border. The animation loops every six seconds. Transparent corners and a dark circular backing work with both light and dark GitHub themes.

To rebuild from the saved source:

```sh
python -m pip install -r scripts/requirements.txt
python scripts/build_logo.py
```

To download a fresh copy of the account avatar before rebuilding:

```sh
python scripts/build_logo.py --refresh-avatar
```

The profile uses the sunset cover, solar-system skills scene, and underwater reef. Run all commands from the repository root. Python 3.10+ is required. Commit the generated images along with the README; visitors do not need Python or a running service.
