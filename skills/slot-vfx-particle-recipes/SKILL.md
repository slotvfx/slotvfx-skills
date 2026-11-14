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
| Older tested builds accepted some `config.*` keys (emission rate, angle) without animating them. On 0.9.79 the timeline plays particle `visible`, `opacity`, `emissionRate`, `x`, `y` and `motionRelease`; angle, size, colour and spin keys are still not played, even where the feature schema calls them keyable. | A keyed change renders byte-identical to no key. | On 0.9.79 key `emissionRate` directly and check a frame. For other settings, or on older builds, use separate emitters split by `startTime` / `duration` for surge and sustain. |
| A keyed emitter in world space (`simulationSpace` 1). | A long-lived glow stays where it was born while the prop it should follow moves away. | Anything that must stay on a moving prop goes in **local space (0)**, keyed with the same x / y times as the prop. |
| `startTime` belongs to the layer, not the clip. | A layer shared by two clips fires at the same time in both. | For visual gating, opacity keys can hide it until the beat; simulation may still run. Use clip membership or separate timed layers when actual births must be delayed. |
| An immortal burst at 0 s in a looping clip. | Missing on frame 0 and at every seam. | Try a small supported prewarm only if this fault reproduces (`prewarmDuration` 0.2 s fixed it on an earlier build); compare an immediate-birth setup and measure startup cost. |
| An orbit emitter (`emitterType` 1) with `angleVariance` 0. | Every particle is born at the same angle, so a "gather from all sides" arrives from one side. | Keep a full angle spread on orbit emitters. |
| A burst of 2 with `path.evenSpacing` on mortal path particles. | Both land in the same slot. | Use one layer per head, with `path.spacingOffset` 0 and 0.5. |
| A spawn-sync follower of a prewarmed immortal driver. | Never spawns. | Give it its own rider on the same path, speed and anchor. |
| A TRAIL child with distance fill (`subEmitterTrailSpacing`). | Works on a path head (0.9.45). On a Target Point head it drew nothing in 0.9.44. | If a trail draws nothing, give the child a rate (70–90/s) in its `subEmitterConfig`. |
| Ribbon length. | The line stops short of the path's end. | Segments × min distance must exceed the path length (128 × 8 for a ~900 px path). |
| `ribbonColorRamp` in the runtime. | It reads as a single colour. | Don't design a gradient along a drawn line. |
| `particle.angle` direction (observed on 0.9.80). | Angle 90 points **up** on screen. Rising layers built with −90 launch downward and only gravity turns them round: a flame stays squat and the checker still reports clean. | Use 90 for anything that rises. Check direction on the first rendered frame before tuning speed. |
| `alphaCurve` with a `colorRamp`. | The schema says the alpha curve is ignored when the ramp has stops, so a flicker or blink curve does nothing. | Put the flicker in the ramp's alpha stops. For a curve, use start/end colour with start alpha 0 and end alpha at the peak, so the curve value maps to alpha. |
| Radial / tangential acceleration origin. | Each particle accelerates around its own spawn point, so a vortex or gather does nothing visible. | Set `radialAccelerationOrigin` to the emitter and give an initial speed. |
| Flipbook frame mode `animated` on a burst. | Frames play by particle age, so every particle shows the same frame together. | Use `randomStatic` for most bursts. |
| `emissionScaleX/Y` on a circle emitter at ground level. | Particles still spawn below the ground line. | Use a rectangle emitter. |
| `create_layers` / `create_particle` with many settings. | Creation takes at most 25 feature values per layer. | Set the rest with `batch_set_properties`. |
| A hidden path collider. | Particles fall through the ground. | Keep the collider visible (it doesn't export) on the ground line. |
| Spark or streak textures with a lot of empty canvas. | The checker's texture row warns (at about 27% core) and the mark reads thin. | Crop the texture to its core. |
| A spawn-sync follower with `emitOn: "death"` from a short-lived driver. | Builds up to 0.9.80 counted its births in the checker but did not draw them; newer builds draw them (0.9.82 drew them in `capture_viewport` and `render_layout`). | If unsure on the connected build, confirm with a viewport capture while the followers should be alive. On 0.9.82 they are the usual choice for an impact where a flight ends; an independent emitter at the height where the drivers die is the fallback for older builds. A follower's `rideOffsetX/Y` was ignored on a death spawn (0.9.82): it appears on the landing point, so centre death-spawned hits on it. Followers with `emitOn: "birth"` and `ride: true` draw on every build tested: use them for a lit cap or shade offset on each smoke ball (`rideOffsetX/Y`), a glow on each coin, or a lagging sparkle trail (`rideLag` about 0.05 s). |
| A prop that should hang and then fly to a target. | One particle cannot switch from physics to target flight. | Use two layers: a hanging layer whose lifespans end in the fly rhythm, and a target-point layer (`targetPosition`, easeIn, `targetBend`, `lifeSpanVariance` 0) with one burst per item at the stagger times. |

**Signs and directions:**
- Positive particle spin and positive `orbit.spinRate` both turn **counter-clockwise** on screen, while an ellipse path's nodes run **clockwise**. Negate the spins when things have to turn with a path.
- A positive `targetBend` bulges to the **right of the direction of travel**. Bend is strong: on a 960 px stage, −34 px is a natural arc and −96 px throws coins off the frame.

**Velocity stretch:** the sample sparks used 0.006, with 0.005–0.01 a starting range at that scale. Tune to the current speed, texture core and display size.

**Particle styling:** the pack used textures, ramps and layering because its particle layers had no Image FX stack. Check current support before relying on another mechanism.

## Build from particle kinds and light

Give each material its own layer and behaviour instead of one generic emitter. Prefer 10–40 varied particles with uneven births over hundreds of identical ones, and give each layer its own wobble (turbulence or curl noise) rather than a shared sine.

| Kind | Behaviour (starting point) |
| --- | --- |
| Spark | Falls at about half the debris gravity, damping 2–3 /s, velocity-stretched with a bright head, cools down the ramp, bounces once on a path collider (restitution about 0.45). Make every third or so 1.5–2× bigger. |
| Ember | Rises slowly, wanders (turbulence or curl noise), cools and shrinks, flickers out in its last third. |
| Smoke | Soft, translucent, normal blend; rises and sways, damping 1.2–1.6, swells about 1.5× while it thins, drifts toward grey. A denser low core and a lit cap while young help it read as volume. |
| Fire puff | Rises fast (negative gravity), brakes hard (damping 3–5), shrinks to about half and cools down the fire ramp; hand off to smoke with a separate smoke emitter at the height puffs die. |
| Flake / petal | Drifts down with sway and slow spin. |
| Debris | Tumbles under heavy gravity, bounces, settles and fades at the end. |
| Twinkle | Thrown fast on curving paths (tangential acceleration), damping about 4, hangs, then blinks out (stepped alpha over the last 30%, in the ramp). |

- **Many small events beat one big one.** A flash, rings, sparks, a puff and glints, timed differently, with varied size, speed, delay and life.
- **Colour is not light.** Build the readable shape in normal-blend colour; put brightness in separate additive light layers on top.
- **Ramps:** 7–8 steps from dark to bright, hue-shifted (shadows cooler and deeper, highlights warmer, only the last step white). Particles cool down the ramp as they age instead of only fading. Starting ramps: fire `1f0b10 4a1118 8c1d1c cc3a1a f2701f ffae35 ffe27a fff8d6`; gold `1e1206 4a2c08 86520c c48412 f0b424 ffe066 fff6c4 ffffff`; ice `0c1430 162c5c 1f4f94 2f7fcc 58b4ec 9bdcff d8f4ff ffffff`; poison `0d1a0c 173a14 265e18 3f8a1e 6cb82a a8e04a e0ff8a`.
- **Two lights per peak:** a tight white light dying in 0.08–0.14 s and a wider theme light dying in 0.3–0.55 s, alpha falling with remaining life squared, 1.3–2× the burst size; a small glow per spark or glint.
- **Light pools:** a low, soft light (about 15%, breathing) on the surface under anything that really emits light.
- **Rings:** a thin bright ring fast (about 0.3 s, expo.out, white for its first third), then a thicker softer ring 0.04 s later and slower (about 0.5 s, power3.out). A ring on the board is a flat ellipse (height about 0.2 of the width), with its far half behind the target and its near half in front.
- **Pop, hold, shrink away:** a project size curve that overshoots past 1, holds, then drops to 0 (start size 0, end size at full) makes cartoon puffs go out ball by ball instead of fading, and opens and folds a HUD plate (one square particle with separate size axes) without keys.
- **Residue:** something stays and cools for 1–2 s (scorch, frost, embers, settling dust), and it still ends on a one-shot. Per-cell residue counts toward the particle budget.

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
- **Aperture, swirl, counter-swirl and rim:** single particles with `startSize` 0 and `endSize` at full size, **all on one shared project curve** (`custom:…`, made with `slotfx_set_project_curve`). One curve keeps the hole, swirl and rim opening and closing together.
- **Depth without a mask:** a flat disc with normal blend under the additive layers keeps the centre darker than the rim.

### Flames

- **Tongues:**
  - Use a soft-edged flipbook, where alpha falls with height and the shape breaks up near the tip. Hard teardrops read as candles.
  - Set `pivotY` 1 so the base stays on the line, and a small speed (about 45 px/s).
  - Grow the height (100 → 175 px) so the fire licks upward instead of floating.
- **Behind the tongues:** a soft-glow body row fills the gaps.
- **Embers:** emit from the **tip line**. Embers born inside a bright flame only read once they are above it.

### Live-particle fire (no flipbook)

Tested on 0.9.80 as a 3 s looping campfire, checker clean. Starting values are in art pixels; at 4× scale multiply accelerations and speeds by 4.

- **Tongues:** four layers of a plain square, hot to cool from front to back: white heart, yellow, orange, red rim. Each is wider, longer-lived and one palette step cooler at death than the one in front of it. Lift about 380 px/s², damping 5; a start speed of about 380–400 px/s gives a flame of about 170 px at that damping. Turbulence X 60–90 with a time scale of about 1.6 makes them lean and lick.
- **Puffs** shed at the tips (damping 3.2), cooling to the darkest step, with smoke from its own emitter at that height.
- **Licks:** thin direction-facing rectangles, short-lived.
- **Embers:** lift about 120, damping 1.6, flicker in the ramp. **Pops:** a short flash plus sparks with gravity about 1708, damping 2.2, on a ground collider; time the last pop so its sparks finish before the loop wraps.
- **Smoke plume:** lift 64–80, damping 1.2, sideways draught +20–44.
- **Light:** additive hot heart, room glow and floor pool with a jagged alpha curve for flicker.

### Ambient loops

- **Light shafts:** an immortal or stable sprite with a verified first frame; the pack used 0.2 s of prewarm. Optional subtle opacity breathing (the pack kept it to 5% or less on the loop period) can use a different offset per shaft.
- **Pollen or motes:** keep the focal area clear when the composition calls for it. The pack used side thirds and about 3 s of prewarm; use only enough warm-up to establish the desired population, and measure startup cost.
- **One event per lap:** opacity keys give a steady loop a heartbeat.

Prewarm costs startup time on every play. Before reaching for it, try a burst at t=0, a burst start-age spread, or immortal particles with toroidal wrap.

### Coin fountain

- **Coins:** an 8-frame flip flipbook with **normal blend**, 820 ± 140 px/s, gravity about 900, angled 10° outward.
- **Rate change:** a surge emitter and a sustain emitter per side, with different `duration`s, so the rate halves on cue. On 0.9.79 an `emissionRate` key can do it on one emitter; check a frame. Stop births well before the clip end.

### Props animated with images, and glows that stay on them

- **The prop:** a hammer, a box or a meter is animated with image `rotation`, `y`, `scaleX` / `scaleY` and `opacity` keys.
- **Its glows:** keyed on particle x / y at the same times, in **local space**.
- **Strike timing:** flat tangents on the wind-up and a linear tangent into the hit.

### Falling leaves

- **Path:** a hidden path with the sway built into the path, using stretch mode and `travelOverLifetime`.
- **Rocking:** `startSpin` +30 → `endSpin` −30, driven by a custom curve in phase with the sway, so the leaf tips its leading edge down on each swing.

### Tested recipes (0.9.80, checker clean)

Target squashes, flashes and HUD bumps below are optional integration examples. Edit actor, symbol or UI animation only within the request; for FX-only work, align to existing cues and describe proposed host reactions.

- **Portal without orbit mode:** a dark normal-blend void disc, a dim additive swirl glow, a rim ring, rim wisps outward with short life, swirl streaks from the rim inward (radial acceleration about −1100, tangential about 1500, origin at the emitter), inflow motes from twice the radius, debris lifted by `targetPosition` to the centre (easeIn), a wide theme light and a ground light pool.
- **Steady glow in a loop:** a crossfade pair (rate 0.5/s, life 4 s, prewarm 4 s), alpha 0 → peak → 0 for additive or a plateau 0 → 1 at 25% → 1 at 75% → 0 for normal blend, size variance about ±5%.
- **Rain:** three depth layers (near 5 px at 2400 px/s α 0.5, mid 4 px at 1800 α 0.3, far 2 px at 1200 α 0.18), additive, `faceDirection`, angle about 278; ground splash droplets (280 ± 130 px/s up, gravity 2600, life 0.22), splash crowns (flat rings to 46×12 in 0.3 s), puddle ripples and a faint ground mist; about 360 live.
- **Confetti:** two low cannons (62° and 118° ± 20, 1900 ± 850 px/s, damping 2.5, turbulence X about 230, large spin variance, life 3.4 ± 1), white paper tinted by a random-colour palette, normal blend, streamers, a muzzle peak (white light, warm light, spark fan, grey puff) and glints above.
- **Gather → peak → rise (heal, level up):** charge 0–0.4 s with motes inward, a growing body glow and a rune ring; peak with a white light (about 0.12 s), a theme light (about 0.9 s), a narrowing light pillar, two ground rings 0.08 s apart, sparks and rising streaks. The target squashes 0.91/1.06, stretches 1.12/0.92 and settles (key y too, to keep the feet down). Over a character cap the lights: white ≤ 0.45, theme ≤ 0.4, body glow ≤ 0.3.
- **Pickup to HUD:** the item pops up, then flies on an arc with a riding sparkle stream (`targetPosition`, `targetSpread`, `targetBend`, `lifeSpanVariance` 0). On arrival: a flash, a ring, a star burst and a HUD bump 1 → 1.4 → 0.9 → 1 over 0.25 s. Keep the HUD point about 150 px inside the frame. Several coins hang after the throw (damping about 7), then fly one by one about 0.075 s apart, speeding into the target; each arrival gets a 0.07 s white flash, a 0.14 s counter bump and 2–3 glints. One option for the arrival hits (flash, ring, glints, counter bump, landing glow): make them Spawn Sync followers of the flying coins with Follow On `death` (`syncVelocity`, `syncMotion`, `syncLifetime`, `syncSize` off). They then fire where each flight ends, stay in step if the timing changes, and follow the Target Point when it moves; hand-timed bursts at a fixed point do neither. The counter itself (plate, rim, coin, shine) is on screen before the first arrival, so it stays as its own layers placed at B; `slotfx_move_effect` on the group shifts A, B and the counter together. For the flight to the counter (A to B), [travel effects](../slot-vfx-travel-effects/SKILL.md) covers the head, rider and impact pattern; the pop, fountain and counter are ordinary particle work.
- **Heavy gas:** positive gravity about 140 on a visible ground collider, a wide fast spread (480 ± 200 px/s, angle 90 ± 100), alpha about 0.4, growing 170 → 360 px from rectangle emitters; a glowing puddle residue uses a glow texture in additive.

### Smaller ones that worked

- **Anything electric:** an 8-frame arc flipbook at 50–60 fps.
- **Brighten a symbol without covering it:** an additive copy of the symbol as a particle texture, at α of about 0.3.
- **Shards:** one shaded grey-RGB texture tinted per layer, with damping so they stop within half a cell.
- **A halo behind an opaque symbol:** about **1.6×** the symbol, or it doesn't show.
- **Riders on a bright beam:** wider than the beam's glow, or spiky (a star4), or they vanish into its core.
- **One-shots repeated on a card or site:** consider a stable background or source marker (such as the source cell or a meter) if an empty gap looks accidental. A deliberate blackout can be part of the requested rhythm.

## Textures

- **Create what the effect needs:** reuse suitable project assets, built-in shapes, procedural textures or custom-drawn image assets. Use `slotfx_create_texture` and supported image imports for missing artwork. Match the requested art style and the texture's appearance at its final on-screen size.
- **Shared library is manual UI only:** do not browse or import from it, and do not stop effect creation to ask the user to choose textures. Author the effect autonomously using the normal texture workflow.
- **Use the right texture role:** visible particle sprites, LUTs, noise maps and emission masks serve different jobs. A LUT or noise map is not a substitute for a smoke sprite. A still depicting a swirl does not create flowing motion by itself; animate or deform an appropriate shape.
- **Preserve accepted art:** keep suitable existing textures when improving motion, timing or lighting. If creating replacement artwork is needed, change one material/layer at a time and compare in the effect. Keep fire, smoke and dust visually distinct and coordinate them with the scene.
- **Colour:** intentionally tintable masks use white RGB with the shape in alpha, so the layer's ramp supplies colour. Other textures retain their authored material colours, intentional dark smoke and RGB shading. Shaded solids (chips, leaves, shards) can keep grey RGB shading for tinting; do not whiten them into flat silhouettes.
- **Size a texture by its core, not its canvas.**
  - A line with a 1-texel core in a 16 px-tall texture vanishes at 3 px tall and reads cleanly at 11 px.
  - A dot whose bright core is 22% of its size needs 18–22 px to show as a 4–5 px speck.
- **Star generators:** inspect the actual generator and output. Parameter names such as `inner` are not standardized; in one earlier generator `inner` read backwards (low values gave a blob, and a six-point flare wanted 0.45). Use current native `create_texture` presets when suitable; this skill does not include a separate arbitrary-artwork generator.
- **Star cut-outs:** multiply them by a radial mask, or they go grey at partial alpha.
- **New shapes:** use the available image-generation or native asset workflow according to its instructions. Shapes that generators get wrong, such as a droplet or a rounded box with a smoothstep falloff, take about a dozen lines of procedural pixel code. Judge the result at actual display size before importing multiple variants.
- **Importing through MCP:** on 0.9.59 `import_asset` accepts a data URL, remote URL, inline data or `sourcePath`. With `sourcePath`, pass a `folderGrantId` from `choose_asset_folder` for a user-approved folder; without a grant, paths resolve under the server's `SLOTFX_MCP_ASSET_ROOTS`. `sourcePath` was the preferred route on 0.9.50. Encode any data URL programmatically (a programmatically encoded PNG data URL imported fine on 0.9.59); never manually transcribe base64, and no payload-size target is needed. Verify the imported dimensions and appearance and any returned byte/fingerprint fields against their documented meaning.
- **Format troubleshooting:** the pack reported one 210×670 lossless (VP8L) WebP making every render that included it fail with "capture context was lost", while a 64-colour palette PNG of the same image rendered fine. Isolate the asset and test a conversion if this reproduces; one file is not evidence that all lossless WebP is unsupported.

## Verify

- **Check first:** `slotfx_check_particle_effect` on the layer, group or clip (pass `role` burst, fountain, hold or ambient when the names don't say) flags pops over budget, tails after the stop, holds that creep, loop seams, empty first frames, clipping, a symbol covered too long, uniform spreads, additive solids, flashing and several traps above (a trail child with rate 0, a death burst on an immortal parent). Fix every FAIL and WARN, run it again, then look.
- **Did it fire, and where:** `render_layout` with `includeImage: false`, reading `liveParticlesByEmitter` and `contentBounds` at the beats.
- **Does it draw in the editor:** `slotfx_capture_viewport` during playback. `render_layout` can stack layers differently from the editor; an opaque preview backdrop in the clip hid every particle in the editor while renders looked right.
- **Check the authored clip:** Pass its id or name as `clip` to `slotfx_check_particle_effect` so its keys and loop period are applied. If narrowing to a member group or layer, also pass the intended `clip` and inspect the returned layer scope. Clip mode can fail with "No particle layers in clip" on a clip that does hold particle layers, whether or not that clip is active (seen on 0.9.80 and 0.9.82); check the clip selector and membership first, and if they are right, use the fallback below. For unexpected zero births, inspect emission timing and keys as well as clip selection. Verify expected births before accepting the result.
- **Standalone fallback:** If clip checking still fails, `group` (with `loop: true` for an intended sustain) can screen the layers in isolation. On 0.9.82 a `loop: true` group check counts births even when that group's clip is not the active clip; a one-shot group check (`loop: false`) samples the active clip and can count nothing while another clip is open, so activate the intended clip first. Either way it but it omits clip keys and the clip wrap period, so a clean result does not verify the authored clip. Inspect that clip through natural playback across entry, keyed changes, stopping and wraps; use `render_layout` frames around specific transitions as additional evidence. Report automated clip checks as unverified while the failure remains.
- **First frames in `render_layout` (seen on 0.9.80 and 0.9.82):** the first strip cell in which a texture appears can draw it as a solid square the size of the sprite; later cells and `capture_viewport` show it correctly. Put a throwaway time first in the strip, or judge the first frame in the editor. (A capture or seek can still show a stale simulation on a heavy effect while the editor shows "Updating particle preview" (0.9.82): wait until it clears and capture again during natural playback.)
- **Many copies:** no MCP tool runs N copies on a runtime. As a cheap projection, run the checker with its `budget` divided by N (for 10 copies: particles 40, fill 0.3). Large light quads dominate fill; share room or floor lights per scene instead of per copy.
- **How it looks:** review entry, strongest beat and tail through natural playback in SlotVFX over the real background. Use captured frames only for a specific diagnostic or requested comparison.
- **One-shots:** verify zero live particles at the intended completion, including any deliberate tail. A held or overlapping effect has a different stop contract.
- **Loops:** inspect first frame and both sides of seams for visual continuity and expected population. Natural count variation or an intentional buildup is acceptable; a constant count alone does not prove a seamless loop.
