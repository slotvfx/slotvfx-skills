# Layered slash craft

Use after the core direction and timing read correctly, especially for flame, energy and textured fantasy swipes. This is a construction guide; visual comparison remains necessary.

## Choose one reference family

Roman Rait's [Hero Wars pack](https://www.behance.net/gallery/251397299/Sword-Slash-VFX-Pack-Hero-Wars) includes visibly different families. Do not average them into a generic effect. The golden torn crescent sample has broad irregular bands, interior gaps, a brighter narrow edge, uneven ends and particles along its circumference. The energy fan instead keeps a broad leading face with long streamers behind it. These are visual observations, not access to the artist's project.

When the core movement reads well but the effect still looks too basic, preserve that movement and focus the next pass on material breakup and secondary motion. A smooth gold gradient on a perfect crescent is only the blockout for the torn variant.

## Material breakup that changes shape

Separate the broad silhouette, directional detail and erosion field. Use anisotropic noise or painted streak masks in arc UV space: u follows the sweep, v spans the width. Align holes and tongues with travel. Prefer a few large features plus smaller detail over uniform speckle or regular sinusoidal scallops.

Animate a threshold through the field, for example `coverage = smoothstep(cut, cut + feather, density)`. Increase cut with local age so gaps widen, bridges break and isolated pieces disappear. Multiplying the entire image by a falling opacity only dims it. Retain a restrained opacity finish after erosion to avoid hard terminal pops. If using a hot dissolve edge, keep it narrow and subordinate to the leading blade.

Let the brighter edge and the rougher body have different breakup schedules. Keep some dark/transparent openings at peak. A fully white sheet loses the internal structure; a thin bright outline with no body becomes another wire.

## Followers and released particles

Use the slash's same arc, direction, center, aspect and motion schedule. Distinguish a source following the stroke from already emitted particles following it. World-space sparks should remain where born, then travel independently; attaching every spark to the moving head creates a rigid clump.

For an analytical arc, derive a release point `P(u)` and tangent from the same curve used by the shader. Assign release times from the head's inverse progress curve, or use a matching animated path driver. Give departing fragments predominantly tangential velocity with a smaller outward component. Use modest drag and size/lifetime variation. A small delay can suggest material peeling off, but large delays visually detach the systems.

For a fixed one-shot, a few staggered burst sources sampled along that curve are a practical alternative to a continuous moving emitter. Label this honestly; it is not a path-follow system. Check enough sampling density that births do not appear as isolated unrelated explosions. Keep the curve/schedule in one task-owned recipe so both layers can be regenerated together.

Use two scales when the reference supports them: a handful of larger slivers that preserve direction, and more tiny embers that survive briefly after the bright body. Vary opacity as well as size so the wake does not resemble confetti. Do not fill the whole bounding box with ambient dots and call it a slash wake.

## Streaks and residual motion

Two or three unequal streaks can trail the main body: offset radius, angular extent, birth time and decay slightly, while retaining the same sweep. Avoid equal concentric rings and equally bright parallel wires. Streaks can be broken alpha shapes; they need not be particle trails. A short residual strand can carry follow-through after most of the body has eroded.

An example phase plan for a fast fantasy cut (adapt to the source): formation 0–80 ms; strongest body 80–180 ms; material separates 180–360 ms; short embers/strands 360–650 ms. The encoded Hero Wars GIF timing is documented separately; this plan is an authoring starting point, not exact reproduction data.

## Readback and visual checks

Compare formation, peak, breakup and late remnants. At breakup, verify actual holes and detached shapes, not just dimmer opacity. During playback, verify particle births sit on the moving sweep and released particles do not orbit forever. Review multiple full cycles for accumulation and leftover heads. Preserve the simple core as an alternative when making a substantial style change.

Use real particle layers when editable emitter behavior is requested. A shader can also render deterministic moving fragments, but report those as shader fragments and do not claim native particle simulation. Native shader compilation, frame inspection and user aesthetic approval are different checks.

## First-person technical evidence

- [Torbach, Power Slashing, posts 16–17](https://realtimevfx.com/t/sketchbook-torbach/19480): demonstrates a sharper subtractive dissolve with increased contrast, compared with a multiplicative fade. This informs the threshold-based breakup distinction.
- [Hazel Stagner, Stylized Sword Slashes](https://glairedaggers.artstation.com/projects/GaGnLQ): breaks a slash into textured discs, contrast layers, cascading sparks, flames and distinct hit sprays. Layer count is not a quality rule; the useful principle is a separate visual role and timing for each layer.
- [Tova Wesström, Slash VFX](https://www.tovawesstrom.com/worksamples): uses multiple ribbon materials, age-driven strength, shared masks and faster secondary streaks. This supports coherent registration with varied internal motion.
- [Cyanilux, Sword Slash Shader Breakdown](https://www.cyanilux.com/tutorials/sword-slash-shader-breakdown/): describes separately panning shape/detail masks and world-space particles emitted along weapon motion. The tutorial does not establish SlotVFX controls.

No reference media are included as production assets.
