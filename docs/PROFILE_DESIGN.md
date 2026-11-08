# Profile design and animation notes

## Direction

One animated signature, a short introduction, four selected projects, and a compact text stack. The logo uses the existing avatar, with a six-second electric-blue orbit. The single-column project layout stays readable on narrow screens. Contact links appear near the top.

The README uses repository-hosted images, so its appearance does not depend on a badge or animation service. The `<picture>` element selects the still PNG for browsers that support the reduced-motion media preference; the GIF is the default. Use `assets/logo-static.png` directly if you want a completely still header.

This animates the logo **inside the profile README**. Your GitHub account's sidebar avatar is controlled separately in account settings; uploading this GIF there is not a reliable way to get an animated account avatar.

## Animation options researched

Reviewed on 8 November 2026 using the projects' own documentation.

| Option | What it adds | Fit for this profile |
| --- | --- | --- |
| **Custom avatar GIF — implemented** | Your existing logo with a restrained animated ring. Stored in this repository. | Best fit: personal branding, one focal point, no runtime setup. |
| [README Typing SVG](https://github.com/DenverCoder1/readme-typing-svg) | A typewriter line with configurable text, timing, and color. [Live editor](https://readme-typing-svg.demolab.com/demo/). | Good if you later want a changing role line. Keep it to one short line and consider reducing the logo motion. |
| [Platane/snk](https://github.com/Platane/snk) | An animated snake that follows your real contribution graph. Supports SVG, GIF, and theme palettes. | A playful footer option. Requires generation and publication of your own graph, usually through GitHub Actions. |
| [Capsule Render](https://github.com/kyechan99/capsule-render) | Configurable SVG headers, waves, gradients, and text animation. | Useful for a banner-led redesign. The custom logo already provides a stronger personal signature here. |

**Recommendation:** start with the logo alone. If you want another animation, add a contribution snake under a collapsed section at the bottom. Keep the visible header focused on your identity and work.

GitHub READMEs support images and a limited set of HTML elements. Treat animations as image assets rather than JavaScript widgets or page-level CSS. Lottie/interactive canvas effects need to be exported to a suitable image format before embedding.

### References

- [GitHub: managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [GitHub: basic formatting, images, and theme-specific pictures](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [GitHub: profile picture requirements](https://docs.github.com/en/account-and-profile/reference/profile-reference#profile-picture-requirements)
- The animation project documentation linked in the table above.

## Project selection

Descriptions were checked against the current public project READMEs, rather than relying only on repository descriptions, which can lag behind development. The order is an editorial recommendation based on current work and variety, not a popularity ranking.

1. **[G.U.A.R.D.](https://github.com/electrifiedchan/guard-edge-ai-proctoring)** — recent applied-AI work combining interview coaching, computer vision, and a full-stack interface. The current README describes a coach, while the repository name and short description still mention proctoring. The profile avoids claiming that every component operates offline.
2. **[GitReal](https://github.com/electrifiedchan/Git_real)** — AI resume verification against actual code. Corrects the old profile description that called it a version-control implementation.
3. **[TeamTruth](https://github.com/electrifiedchan/TeamTruth)** — AI memory and contradiction detection for team updates. Explicitly labeled an MVP; the profile does not describe planned GitHub webhook integration as an existing feature.
4. **[ExamHub](https://github.com/electrifiedchan/exam-hub-seating-system)** — a concrete data-processing and allocation application that balances the AI projects.

The expandable section keeps two additional projects discoverable:

- **[Namma Yatri](https://github.com/electrifiedchan/namma_yathri)** — its current scope includes React Native, Supabase, and ride-hailing logic, beyond the UI clone described in the old profile.
- **[VTU Performance Analyzer](https://github.com/electrifiedchan/vtu-performance-analyzer)** — its documented backend is Flask, correcting the previous Node.js label.

Suggested GitHub pinned repositories: these same six projects, with the four selected projects first. Pinning is a separate profile setting; editing this README does not change pinned repositories.

## Preview and publish

1. Open the root `README.md` in a Markdown preview to review the layout. Some editors do not support the `<picture>` element; open `assets/logo-animated.gif` in a browser to view the motion directly.
2. Publish the updated `README.md` **and the images in `assets/` together** to the `main` branch of `electrifiedchan/electrifiedchan`. The relative paths need those images in the repository.
3. Visit [your profile](https://github.com/electrifiedchan) to check the final GitHub rendering. Check both themes and a narrow window.
4. Use **Customize your pins** on your profile to select and order the suggested repositories.

No GitHub Actions workflow, personal access token, or hosted animation API is needed for the included logo.

For asset regeneration, see [assets/README.md](../assets/README.md). Edit `CYAN` / `BLUE` in `scripts/build_logo.py` for accent colors, or change `FRAMES` / `FRAME_MS` for animation speed, then rebuild.
