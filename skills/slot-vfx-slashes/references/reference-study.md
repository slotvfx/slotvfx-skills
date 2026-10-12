# Reference study and evidence

## Roman Rait — Sword Slash VFX Pack | Hero Wars

[Artist's project](https://www.behance.net/gallery/251397299/Sword-Slash-VFX-Pack-Hero-Wars), published June 21, 2026. Inspected October 8, 2026. The gallery presents mobile-game attack variants; it does not establish their runtime implementation.

Four served GIFs were inspected as frames. Each downloaded sample was 600×600, 30 frames, with 30 ms encoded per frame: a 900 ms GIF cycle. These are encoded playback measurements, not measured game timing or proof of the author's source frame rate.

| Sample | Observed family | Peak bright-area frame / time | Last frame above the analysis threshold |
|---|---|---|---|
| [81d144…](https://mir-s3-cdn-cf.behance.net/project_modules/max_1200_webp/81d144251397299.6a3557c5d6e44.gif) | Clean curved stroke | 4 / 120 ms | 300 ms |
| [acd458…](https://mir-s3-cdn-cf.behance.net/project_modules/max_1200_webp/acd458251397299.6a3658a2f3747.gif) | Torn flame crescent | 3 / 90 ms | 540 ms |
| [45573c…](https://mir-s3-cdn-cf.behance.net/project_modules/max_1200_webp/45573c251397299.6a3668b7cdcad.gif) | Broad leading energy fan | 2 / 60 ms | 450 ms |
| [1517ff…](https://mir-s3-cdn-cf.behance.net/project_modules/max_1200_webp/1517ff251397299.6a36703d9c542.gif) | Straight bright cut | 4 / 120 ms | 510 ms |

Threshold: resize to 128×128, count pixels with max(R,G,B)>110, and retain frames above 3% of peak count. Dim residual glow can last longer. Some GIFs begin with visible action, so their first frame is not necessarily the attack's true onset.

Visual interpretation: the clean arc changes angular extent; the flame variant sheds irregular fragments; the fan concentrates light at its front; the straight cut loses its body before residual sparks disappear. These are useful distinctions, not a claim about how the artist constructed them. Reference media are not bundled as reusable production assets.

## Supporting first-person technical sources

- [Cyanilux — Sword Slash Shader Breakdown](https://www.cyanilux.com/tutorials/sword-slash-shader-breakdown/): describes an unlit ring-mesh effect driven by a moving shape texture and separate panning noise. Its masking prevents texture repeats and visible mesh boundaries. This supports separating geometry, stroke window and texture detail. The article explicitly leaves animation setup outside its scope; it does not validate SlotVFX parameters.
- [Geri — Venom Slash breakdown](https://realtimevfx.com/t/venom-slash-breakdown-of-the-effect-included/18903): the author uses a static ring mesh, multiplied texture detail, scrolling noise, a color ramp and separately dissolving splash sprites. It demonstrates that material motion can carry a stroke without spinning the entire mesh.
- [NotSoLittleChris / Tayko — WIP Sword Attack](https://realtimevfx.com/t/wip-sword-attack-thoughts/5730): creator feedback and revision emphasize shorter visible duration, closer alignment to weapon motion and contrast beyond additive glow. Treat its proposed duration reduction as feedback on that example, not a universal percentage.

## What the failed local study taught

The rejected SlotVFX attempts used prolonged whole-crescent sprites, repeated decorative arcs, increasingly wide filament trails and many secondary layers. Tool success and attractive isolated textures did not make their motion into a convincing attack. Analytic contour noise also produced regular scallops instead of intentional torn edges.

These observations justify a core-only motion pass and earlier construction changes. They do not establish that particles, trails, shaders or colored sprites are inherently unsuitable. The user rejected the visual result; do not carry those attempts forward as approved presets.
