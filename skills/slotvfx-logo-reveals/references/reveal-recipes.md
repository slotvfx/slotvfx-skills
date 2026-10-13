# Reveal recipes and independent logo motion

These concepts were built and visually reviewed in earlier local logo work on SlotVFX 0.9.49 (2026-09-26). Times describe those examples, not a required template. The source logo had an emblem and two lines of text; adapt the parts to the current artwork.

## Motion concepts

| Concept | Tested rhythm | Distinctive action |
| --- | --- | --- |
| Ricochet | Contacts near 0.58, 1.10, and 1.56 s; settle around 2.23 s; clip 4.6 s | The emblem rebounds along an angular path, strikes its final position, and transfers a small reaction into the lettering. Place sparks at contacts and trails along the actual trajectory. |
| Speedrun | Overshoot near 1.04 s; braking through 1.59 s; settle around 1.96 s; clip 4.7 s | Stagger lettering and emblem, overshoot, then brake and correct. Each piece gets a distinct curve. |
| Combo Hit | Impacts near 0.48, 0.96, and 1.44 s; clip 4.4 s | Give emblem, main text, and subtitle different entry directions. Escalate the last beat with a brief position/scale reaction. |
| Mechanical Snap | Locks near 0.52, 0.86, and 1.18 s; assembled emblem repositions around 2.20 s; clip 5.2 s | Three masked emblem pieces interlock, then move together into the final composition as text arrives. Retract construction rails. Accurate seams matter more than blur. |
| False Start | Imperfect landing near 0.67 s; correction near 1.85 s; subtitle correction through 2.94 s; clip 5.2 s | A brief crooked landing, pause, and decisive correction provide humor through timing. Finish precisely aligned. |
| Launch Button | Compress during 1.20–1.40 s; release around 1.51 s; settle by 2.48 s; clip 4.8 s | The emblem behaves like a pressed button, then releases stored energy into the wordmark. Connect the compression and release visibly. |

Use the remaining clip duration for a readable finish when appropriate. A readable final pose does not require a separate hold effect or timeline.

## Glitch and themed variants

- **Signal breach / cyberpunk:** brief misregistration, selective horizontal slices, interrupted motion, then a clean lock. Gate distortion off after recovery.
- **Industrial / forge:** weighted movement, restrained heat or contact sparks, and metal-like reflections where they support the finish.
- **Arcade / competitive:** bold spatial choreography, short streaks, sharp impacts, and playful rhythm. More glow alone does not create a stronger reveal.
- **Cosmic / arcane / relic:** appropriate when requested; match the selected style to the current logo identity.

Match intensity to the logo, frame size, and destination. Do not reproduce the same trailing shine as a default ending.

## Splitting a logo without destructive image edits

The tested workflow duplicated the original image into several image layers and assigned a closed polygon mask to each. The “cuts” were editable masks, not newly painted or physically cut PNGs.

1. Inspect the logo and identify meaningful components. Determine the mask coordinate system from the current schema and preview.
2. Duplicate the asset into separate image layers with identical baseline dimensions and alignment.
3. Apply component masks with appropriate feathering; hard assembly seams used zero feather.
4. Animate each part around its intended pivot. A full-image layer's center is usually not the center of a masked emblem or word.
5. Verify the final transforms reconstruct the source without seams, drift, or accidental cropping.

For a desired component pivot position `Q`, component pivot `p`, full-image center `c`, scale matrix `S`, and mathematical rotation `R(theta)`, place the full-image center at:

```text
C = Q - R(theta) S (p - c)
```

Express `p` and `c` in the same authored image coordinate system. Account for asset-to-image resizing first. In the tested SlotVFX image transform, the authored rotation was `-theta` in degrees; verify the sign with one part before keying the sequence.

For footage, masks rendered correctly in the editor. For game-runtime delivery, inspect actual target export behavior before relying on masked pieces; editor preview alone does not prove runtime parity. If separate image assets are needed, follow the available image-editing workflow and retain the original.

## Motion blur and finishing light

Use blur during fast travel and return it to zero at rest. The final tested native directional-blur setup animated both `strength` and `length` together. Setting only `strength` had left a default blur length active and produced ghosts. A restrained final example peaked around 2.64 for both, used 25 samples, and disabled blur on mechanically interlocking pieces. These values belong to that artwork and resolution, not every logo.

Two polished reveals used `realisticShine` as a localized reflection. Others worked better after shine was disabled. Inspect the current effect's parameters and dropdown meanings before adapting it; do not copy unexplained numeric enum values.
