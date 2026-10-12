---
name: slot-vfx-slashes
description: Create or repair sword slashes, crescent cuts, attack swipes and directional energy strokes in SlotVFX, including textured breakup, dissolving flame tongues, streaks and particles released along the sweep. Establish shape and timing, then finish the reference's material and secondary motion. Excludes general portals, sustained vortex loops and logo reveals.
---

# SlotVFX slashes

A slash is a short directional event. Establish its changing silhouette and timing before making a decorated composition. A bright curved image rotating and fading as a whole can be useful, but does not by itself reproduce a stroke that grows from a moving head and vanishes from its tail.

Use the user's reference and requested style. Do not silently replace a slash with a persistent ring, multi-turn spiral, flame column or shower of particles. Preserve existing project work; make an alternative in a named group and clip.

## Read the reference as motion

Identify the attack family: **sweeping crescent**, **straight cut**, **projectile/fan**, or **lingering magical arc**. Record its plane, direction, pivot, head shape, widest region, tail shape, peak and disappearance. Distinguish multiple strikes from multiple layers of one strike.

For animation references, inspect the actual motion and representative frames. Separate source facts, measured encoded timing and interpretation. A still image cannot establish speed. For the Hero Wars examples and timing method, read [the reference study](references/reference-study.md). Use `scripts/analyze_gif.py` when a locally available GIF needs frame/timing inspection; its brightness thresholds are an analysis aid, not a visibility or quality verdict.

## Choose a construction that fits

| Need | Suitable starting point | Check before committing |
|---|---|---|
| Follow a real weapon or known moving head | Textured ribbon/trail | Stable width, sparse smooth path, no folded corners; short history |
| Fixed camera, controllable crescent sweep | Curved strip or polar shader with a moving visibility window | UV direction, moving head **and** tail, seam outside the stroke |
| Hand-drawn tongues, changing contour or breakup that defines the style | Authored image sequence/flipbook | Registered frames, stable pivot, no ghost hold on the last frame |
| Brief accent with little contour change | Single sprite particle | A short cue; do not describe whole-image rotation/fade as frame animation |
| View-dependent 3D sword sweep | Curved mesh with coherent strip UVs | Actual SlotVFX mesh/material support and camera orientation |

A shader or flipbook is a normal authoring choice, not a last resort after stacking unsuccessful particles. Missing MCP tools do not establish that the app lacks the feature. Inspect available schemas and use supported native controls where needed.

## Build the core in isolation

Start with one stroke in white or a restrained two-tone palette. Hide optional glow, sparks, smoke, debris, rings and stars during core review. Work at intended gameplay size, including a small thumbnail view.

The core should communicate direction without those accents:

- A coherent arc or cut with a deliberate broad region and taper; sufficient empty space inside a crescent.
- A fast advancing front and a following, shortening/eroding tail. Keep stroke extent separate from opacity.
- A clear bright region and lower-value body; avoid flattening all detail into white.
- Edge detail aligned with travel. Random sinusoidal wobble across the contour creates a scalloped tube; many equal filaments create wires.

For a fast attack with no supplied timing, start around **0.3–0.6 seconds of visible action**, then adjust to the animation. Make the strongest shape appear early; give dissolution a little more time than formation. This is a starting range, not a requirement for charged attacks or lingering spells. The blank pause in a review loop is separate from effect lifetime.

Do not lengthen the stroke into several seconds just to make it easy to inspect. Use slow playback for inspection and return to normal speed for judgment. Do not add secondary layers to conceal a failing core. If successive changes only add noise, return to the plain silhouette and reconsider the construction.

## Texture and material discipline

Use a **straight strip texture** on a curved ribbon/mesh. A pre-curved crescent belongs on a flat sprite unless its UV mapping was designed otherwise. Curving both shape and texture can distort the silhouette twice.

Keep shape, directional streak detail and erosion independently controllable where practical. Prefer sparse stretched marks following travel to isotropic speckle. For stylized color, a tintable grayscale mask plus a color ramp is often easier to control than a fully lit illustration.

Inspect real alpha, padding and bright/dark fringes. A black preview is not proof of transparency. Opaque pixels inside a clean painted silhouette are legitimate; an opaque rectangular matte is different. An alpha-blended body can preserve readable color, with restrained additive glow over it. Check on a representative background before committing to additive-only rendering.

Read [SlotVFX implementation notes](references/slotvfx-implementation.md) for controls, UV/window logic, clock probes and observed traps. Treat untested routes as proposals until the actual editor result passes review.

## Add only what serves the strike

The plain core is an intermediate study, not the final deliverable when the reference has rich material breakup and secondary motion. Once the motion works, complete the requested style. Read [layered slash craft](references/layered-slash-craft.md) for erosion, particle release and streak choreography.

Add layers by role: a broad textured body, a brighter moving edge, a few unequal filaments, detached fragments and residual embers. A contact flash or smoke belongs only where the reference/attack needs it. Keep the dominant motion, brightness and timing with the slash. Reusing one static crescent three times is not a substitute for three distinct attack phases.

## Verify and hand off

Read back properties, clip membership, frame order and shader diagnostics as applicable. Play the named clip naturally through at least two complete cycles and check entry, peak, tail and reset. Watch for birth pops, a stationary horseshoe, a full-ring seam, crossed trail triangles, a rectangular texture edge or a held final frame.

Review with accents disabled, at normal speed and intended size, then with accents restored. A good peak screenshot does not establish good motion. Keep the result selected/framed in SlotVFX and name the clip. Report whether it is a textured trail, shader, animated sequence or static sprite. Saving, recording, exporting and runtime parity remain separate tasks unless requested. Do not label the result approved or validated merely because the tools accepted the writes.
