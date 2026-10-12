# SlotVFX slash implementation notes

## Establish the live contract

Use the installed SlotVFX authoring workflow and registered schemas. Inspect project, clips, assets and selected entities before writing. These notes were compiled with Desktop 0.9.57 and MCP 0.9.56; recheck current behavior instead of copying old project identifiers.

Useful current resources include `slotfx://authoring-guide/particles`, `slotfx://authoring-guide/particle-textures`, `slotfx://authoring-guide/image-fx`, `slotfx://authoring-guide/animation`, and `slotfx://features/<featureId>`. Read only the route needed. A truncated large resource is not complete schema evidence.

## Sweeping mask or shader

Parameterize a strip with **u along travel**, **v across width**. Keep a head position and a tail position. A conceptual window is:

```text
window(u,t) = smoothstep(tail(t), tail(t)+feather, u)
            * (1 - smoothstep(head(t)-feather, head(t), u))
alpha       = window * cross_section * shape_detail * erosion
```

This is conceptual math, not a drop-in SlotVFX shader. Give a forming stroke an increasing span, then advance the tail to contract it. Permit the window to leave the finite strip completely. Clamp/mask samples outside the texture domain; wrapping can accidentally make another slash.

For a 2D polar implementation, inverse-rotate and ellipse-scale the fragment position, then derive radius and angle. Unwrap the angle across the intended arc and place its discontinuity outside visible travel. Convert angle to u and radial distance to v. Keep the body width envelope separate from the detail texture. Use stretched detail flowing along u and modest erosion; do not move the whole outer contour with high-frequency sine waves.

Expose or name controls for direction, arc span, width envelope, sweep progress, tail length, erosion, palette and glow. An angular reveal with a stationary tail creates a held crescent; a uniform opacity fade cannot correct that motion.

### Clock probe before choreography

Confirm the input's units and restart behavior with a small visible test at two known times. Check again after changing clip duration. SlotVFX documents that the default expression `p_time` can represent normalized loop phase in some modes, while explicit time wiring changes the clock. Do not assume `p_time`, `uTime`, `uAbsoluteTime` or `uLoopLocalTime` are interchangeable seconds.

A prior six-second study appeared to work after multiplying its phase by six. That is **not a reusable clock solution**. Use a verified duration mapping or explicitly verified seconds input. Test normal playback, reset and repeat; a seek alone is insufficient for evolved particle state.

### Texture-slot probe before a shader build

Verify UV orientation, color channels, alpha and clamp behavior with a small diagnostic input before connecting artwork. A slot named `mask` is not a general color texture slot. In the local study, assigning painted artwork to a standalone effect mask and sampling `uTexture` produced clipped/white striped output and also cut the surrounding effect. The precise pipeline cause was not established. Do not repeat that unverified technique or generalize it to all custom shaders.

The observed graph route supports `custom/expression`, inputs such as `p_uv`, `p_time`, `p_speed`, `p_scale`, `p_intensity`, and outputs `out_color` / `out_alpha`; compile and inspect the live contract. Use shader graph tools for edits and check real frames after compilation. Creating/selecting a blank effect showed an editor graph before it was committed to project data in this session; do not reuse a transient UI graph ID without readback.

## Textured ribbon route

Use a short smooth arc and a clear driver. Check whether the path moves particles or moves the emitter; group membership does not attach a path. Choose world/local simulation intentionally.

Use a straight grayscale streak strip with quiet transparent borders and longitudinal detail. Tune width and visible length together. Large width over a tight bend can fold a ribbon; multiplying width cannot repair path geometry. Judge with a plain texture first, then restore detail. Do not stack many equal bright strands to imitate the body of a broad blade.

After motion/path edits, let the old trail history clear and review a full fresh cycle. An immediate mid-cycle capture can contain prior trajectory history. Inspect birth, hard turns, termination and reset at normal speed.

## Animated image / flipbook route

Author actual contour changes: onset, advancing head, widest smear, shortening tail, broken remnants, clear frame. A sequence of independently generated unrelated crescents will wobble; preserve camera, registration, pivot and direction across frames. If generation is used, inspect consistency and repair deliberately with the image-generation workflow.

Plan the visible frame count from duration and playback rate. For example, a roughly half-second stroke at 30 fps needs about 15 timed frames, not a long hold of one still. Do not impose that count on an existing reference with different cadence.

Use the supported Image Sequence import and inspect frame order, trim offsets, atlas padding, playback rate, loop flag and terminal behavior. A pure slash should clear after its last visible frame; a repeated review clip should restart it. Check first/last frames at actual playback speed. Current runtime/export parity is a separate verification task.

## Short sprite particle route

For a quick static-shaped accent, a single burst is sufficient. Set lifespan variance, speed variance, spin variance and emission duration intentionally. The following registry names were observed in this version:

- `particle.emissionRate`, `emissionBursts`, `maxParticles`, `duration`, `lifeSpan`, `lifeSpanVariance`.
- `particle.separateSizeAxes`, `startSizeX/Y`, `endSizeX/Y`, `startSpin`, `endSpin`, `colorRamp`.
- `particle.blendMode` accepts presets including `normal`, `add_soft` and `screen`; `particle.blendPreset` was rejected.

Color ramps use RGB 0–255 and alpha 0–1 in the observed schema. Inspect the current schema before reusing values. The creation route observed a limit of 25 initial particle features; bulk edits had a 100-change limit. Pass explicit clip membership and read it back.

Whole-sprite growth, rotation and alpha fading are simple particle animation. They do not create an advancing stroke window or independent tail erosion. Use a different route when those define the reference.

## Useful acceptance probes

1. Core only, normal speed: can direction and attack moment be read immediately?
2. Paused phases: does extent change, or is the same horseshoe simply fading?
3. Small view: is one shape dominant, with a clear opening and a readable bright region?
4. Dark and representative lighter background: do alpha edges, saturation and contrast survive?
5. Two cycles: do both cycles animate, with no held final frame or old trail history?

These notes contain verified tool observations and research-based construction guidance. They are not a certified successful slash preset. Do not claim a route has passed visual or runtime verification until it has been exercised in the target setup.
