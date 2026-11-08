# Profile logo assets

- `avatar-source.png` — snapshot of the existing public GitHub avatar, downloaded by the build script.
- `logo-animated.gif` — 320 × 320 animation, displayed at 152 × 152 in the profile README.
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

Run these commands from the repository root. Python 3.10+ is required. Commit the generated images along with the README; visitors do not need Python or a running service.
