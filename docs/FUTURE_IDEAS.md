# Future profile ideas

## Interactive project CD player

A retro deck with four draggable project CDs: G.U.A.R.D., GitReal, TeamTruth, and ExamHub.

- Drop a disc onto the deck to load its short introduction, tech stack, and repository link.
- Animate disc insertion, spinning, and ejection.
- Support tapping a disc on phones and keyboard activation.
- Build with plain HTML, CSS, JavaScript, and local artwork, using relative paths.
- Host the interactive page on GitHub Pages and link it from an animated README preview. GitHub READMEs cannot execute the drag-and-drop JavaScript themselves.

The README now displays the supplied automatic `assets/record-rack.svg` animation. The drag-and-drop controls described here remain a future idea for a separate interactive page.

## Lossless animated WebP

Potentially reduce animation payload while retaining the GIF fallbacks.

Before enabling it in the profile:

1. Check `PIL.features.check("webp_anim")` in the build environment.
2. Generate lossless animated WebP alongside each GIF, then verify every decoded frame and duration.
3. Test a `<picture>` in a **scratch public GitHub repository**, in light mode, dark mode, and on mobile. Order sources as reduced-motion PNG, WebP, then the existing GIF `<img>` fallback.
4. Only adopt the WebP sources after confirming that animation actually plays on GitHub. If the test fails, retain the existing GIF/PNG setup.

WebP export and README sources are not enabled in the current build.
