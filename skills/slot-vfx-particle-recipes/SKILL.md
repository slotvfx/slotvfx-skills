---
name: "slot-vfx-particle-recipes"
description: "Particle looks that worked in SlotVFX (impacts, rain ripples, portals, flames, ambience, coin fountains, props with glows) and the parameter traps that silently break them."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Particle recipes and traps

Use these as starting recipes, not mandatory stacks. They come from the supplied pack's observations across older SlotVFX builds, including 0.9.44–0.9.50; they have not all been reproduced in this installation. Read current feature schemas and verify important behavior in the intended runtime. Scale dimensions, rates and motion to the artwork and player view. Current user requests override these examples.

Preserve existing groups and layers unless editing or deletion of those targets was requested. Reuse suitable assets before generating more detail. For a complete pack, see [effect-pack workflow](../slot-vfx-effect-pack/SKILL.md); for A-to-B travel, [travel effects](../slot-vfx-travel-effects/SKILL.md); for sustained clips, [hold loops](../slot-vfx-hold-loops/SKILL.md).

## Traps: check these before you trust a render

These are historical failure cases. Inspect current tool warnings and defaults; a successful write alone does not prove the intended visual behavior.

| Trap | What happens | Do this |
| --- | --- | --- |
| The pack observed `lifeSpanVariance` defaulting to **0.4 s** (seconds, not a fraction). | A 0.25 s spark lives anywhere from 0 to 0.65 s, and a Target Point head arrives late. | Set it on every layer: 0 for anything that has to land on time. |
| The pack observed a wide default `angleVariance`. | A light column drifts sideways and a fan loses its shape. | Set it explicitly. `create_layers` warns about this; the warning is real. |
| Older tested builds accepted some `config.*` keys (emission rate, angle) without animating them; only opacity, x / y and image-transform keys drove anything there. | A keyed rate change renders byte-identical to no key. | Check the current animatable-property schema. If rate animation is unsupported, use separate emitters split by `startTime` / `duration` for surge and sustain. Verify other supported tracks rather than assuming all accepted keys animate. |
| A keyed emitter in world space (`simulationSpace` 1). | A long-lived glow stays where it was born while the prop it should follow moves away. | Anything that must stay on a moving prop goes in **local space (0)**, keyed with the same x / y times as the prop. |
| `startTime` belongs to the layer, not the clip. | A layer shared by two clips fires at the same time in both. | For visual gating, opacity keys can hide it until the beat; simulation may still run. Use clip membership or separate timed layers when actual births must be delayed. |
| An immortal burst at 0 s in a looping clip. | Missing on frame 0 and at every seam. | Try a small supported prewarm only if this fault reproduces (`prewarmDuration` 0.2 s fixed it on an earlier build); compare an immediate-birth setup and measure startup cost. |
| An orbit emitter (`emitterType` 1) with `angleVariance` 0. | Every particle is born at the same angle, so a "gather from all sides" arrives from one side. | Keep a full angle spread on orbit emitters. |
| A burst of 2 with `path.evenSpacing` on mortal path particles. | Both land in the same slot. | Use one layer per head, with `path.spacingOffset` 0 and 0.5. |
| A spawn-sync follower of a prewarmed immortal driver. | Never spawns. | Give it its own rider on the same path, speed and anchor. |
| A TRAIL child with distance fill (`subEmitterTrailSpacing`). | Works on a path head (0.9.45). On a Target Point head it drew nothing in 0.9.44. | If a trail draws nothing, give the child a rate (70–90/s) in its `subEmitterConfig`. |
| Ribbon length. | The line stops short of the path's end. | Segments × min distance must exceed the path length (128 × 8 for a ~900 px path). |
| `ribbonColorRamp` in the runtime. | It reads as a single colour. | Don't design a gradient along a drawn line. |

**Signs and directions:**
- Positive particle spin and positive `orbit.spinRate` both turn **counter-clockwise** on screen, while an ellipse path's nodes run **clockwise**. Negate the spins when things have to turn with a path.
- A positive `targetBend` bulges to the **right of the direction of travel**. Bend is strong: on a 960 px stage, −34 px is a natural arc and −96 px throws coins off the frame.

**Velocity stretch:** the sample sparks used 0.006, with 0.005–0.01 a starting range at that scale. Tune to the current speed, texture core and display size.

**Particle styling:** the pack used textures, ramps and layering because its particle layers had no Image FX stack. Check current support before relying on another mechanism.

## Recipes

### Impact or burst (one peak)

1. **Anticipation:** about 0.12 s of charge, streaks or specks pulled inward.
2. **The peak, stacked light:** a flash, a starburst, thin rays and two rings. All additive and short-lived.
3. **Sparks that behave physically:** velocity-stretched dots with drag and gravity.
4. **A slower second layer that lingers:** twinkling glitter (alpha pulsing in the ramp) and embers.

For a luminous warm look, a gold tail often reads more clearly than a dark brown tail; follow the requested material and palette. Hold back a kept effect with its own `startTime` to make a beat, so the build-up plays dark and the main effect arrives with the flash.

### Paired impacts: rain with ripples, drops with splashes

- **Drops:** short spawn-sync *drivers*. Each needs a speed and life that land it in the ground band (for example 0.08 s at 800 px/s).
  - Pivot each drop on its head (`pivotX` 0.9–0.95), so the head is where it dies.
- **Ripples and splash flecks:** followers with `emitOn: "death"`, and `syncVelocity`, `syncMotion`, `syncLifetime` and `syncSize` all false.
- **Result:** every ripple starts exactly where a visible drop landed.
- **Ripple texture:** two flattened ellipses with an even line width, drawn at 4:1.
- **Wind:** `windX` with a gust whose frequency matches the loop (0.2 Hz for 5 s), not keys.

### Portal or vortex

- **Spiral motion:** radius (orbit) emitter mode. `orbit.outerRadius` → `orbit.innerRadius` with `orbit.spinRate` spirals specks in; the reverse spirals them out. No force fields needed.
- **Aperture, swirl, counter-swirl and rim:** single particles with `startSize` 0 and `endSize` at full size, **all on one shared project curve** (`custom:…`). One curve keeps the hole, swirl and rim opening and closing together.
- **Depth without a mask:** a flat disc with normal blend under the additive layers keeps the centre darker than the rim.

### Flames

- **Tongues:**
  - Use a soft-edged flipbook, where alpha falls with height and the shape breaks up near the tip. Hard teardrops read as candles.
  - Set `pivotY` 1 so the base stays on the line, and a small speed (about 45 px/s).
  - Grow the height (100 → 175 px) so the fire licks upward instead of floating.
- **Behind the tongues:** a soft-glow body row fills the gaps.
- **Embers:** emit from the **tip line**. Embers born inside a bright flame only read once they are above it.

### Ambient loops

- **Light shafts:** an immortal or stable sprite with a verified first frame; the pack used 0.2 s of prewarm. Optional subtle opacity breathing (the pack kept it to 5% or less on the loop period) can use a different offset per shaft.
- **Pollen or motes:** keep the focal area clear when the composition calls for it. The pack used side thirds and about 3 s of prewarm; use only enough warm-up to establish the desired population, and measure startup cost.
- **One event per lap:** opacity keys give a steady loop a heartbeat.

Prewarm costs startup time on every play. Before reaching for it, try a burst at t=0, a burst start-age spread, or immortal particles with toroidal wrap.

### Coin fountain

- **Coins:** an 8-frame flip flipbook with **normal blend**, 820 ± 140 px/s, gravity about 900, angled 10° outward.
- **Rate change:** a surge emitter and a sustain emitter per side, with different `duration`s, so the rate halves on cue. Stop births well before the clip end.

### Props animated with images, and glows that stay on them

- **The prop:** a hammer, a box or a meter is animated with image `rotation`, `y`, `scaleX` / `scaleY` and `opacity` keys.
- **Its glows:** keyed on particle x / y at the same times, in **local space**.
- **Strike timing:** flat tangents on the wind-up and a linear tangent into the hit.

### Falling leaves

- **Path:** a hidden path with the sway built into the path, using stretch mode and `travelOverLifetime`.
- **Rocking:** `startSpin` +30 → `endSpin` −30, driven by a custom curve in phase with the sway, so the leaf tips its leading edge down on each swing.

### Smaller ones that worked

- **Anything electric:** an 8-frame arc flipbook at 50–60 fps.
- **Brighten a symbol without covering it:** an additive copy of the symbol as a particle texture, at α of about 0.3.
- **Shards:** one shaded grey-RGB texture tinted per layer, with damping so they stop within half a cell.
- **A halo behind an opaque symbol:** about **1.6×** the symbol, or it doesn't show.
- **Riders on a bright beam:** wider than the beam's glow, or spiky (a star4), or they vanish into its core.
- **One-shots repeated on a card or site:** consider a stable background or source marker (such as the source cell or a meter) if an empty gap looks accidental. A deliberate blackout can be part of the requested rhythm.

## Textures

- **Colour:** white RGB with the shape in alpha. Colour comes from the layer's ramp. Shaded solids (chips, leaves, shards) carry their shading in grey RGB.
- **Size a texture by its core, not its canvas.**
  - A line with a 1-texel core in a 16 px-tall texture vanishes at 3 px tall and reads cleanly at 11 px.
  - A dot whose bright core is 22% of its size needs 18–22 px to show as a 4–5 px speck.
- **Star generators:** inspect the actual generator and output. Parameter names such as `inner` are not standardized; in one earlier generator `inner` read backwards (low values gave a blob, and a six-point flare wanted 0.45). Use current native `create_texture` presets when suitable; this skill does not include a separate arbitrary-artwork generator.
- **Star cut-outs:** multiply them by a radial mask, or they go grey at partial alpha.
- **New shapes:** use the available image-generation or native asset workflow according to its instructions. Shapes that generators get wrong, such as a droplet or a rounded box with a smoothstep falloff, take about a dozen lines of procedural pixel code. Judge the result at actual display size before importing multiple variants.
- **Importing through MCP:** on 0.9.59 `import_asset` accepts a data URL, remote URL, inline data or `sourcePath`. With `sourcePath`, pass a `folderGrantId` from `choose_asset_folder` for a user-approved folder; without a grant, paths resolve under the server's `SLOTFX_MCP_ASSET_ROOTS`. `sourcePath` was the preferred route on 0.9.50. Encode any data URL programmatically (a programmatically encoded PNG data URL imported fine on 0.9.59); never manually transcribe base64, and no payload-size target is needed. Verify the imported dimensions and appearance and any returned byte/fingerprint fields against their documented meaning.
- **Format troubleshooting:** the pack reported one 210×670 lossless (VP8L) WebP making every render that included it fail with "capture context was lost", while a 64-colour palette PNG of the same image rendered fine. Isolate the asset and test a conversion if this reproduces; one file is not evidence that all lossless WebP is unsupported.

## Verify

- **Did it fire, and where:** `render_layout` with `includeImage: false`, reading `liveParticlesByEmitter` and `contentBounds` at the beats.
- **How it looks:** review entry, strongest beat and tail through natural playback in SlotVFX over the real background. Use captured frames only for a specific diagnostic or requested comparison.
- **One-shots:** verify zero live particles at the intended completion, including any deliberate tail. A held or overlapping effect has a different stop contract.
- **Loops:** inspect first frame and both sides of seams for visual continuity and expected population. Natural count variation or an intentional buildup is acceptable; a constant count alone does not prove a seamless loop.
