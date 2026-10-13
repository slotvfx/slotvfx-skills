---
name: slot-vfx-performance
description: "Investigate SlotVFX frame-rate or export-cost problems with controlled measurements in the actual target runtime. Compare realistic copy counts, simulation, draw calls, uploads, overdraw and baked alternatives."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Measuring SlotVFX performance

Use this skill for a requested performance investigation or a material shipping concern. Match the scope to the question; an isolated visual tweak does not require a full profiling harness. Preserve the accepted look and original versions while testing alternatives.

## Establish a representative baseline

Identify the actual scene, target engine/version, device class and likely bottleneck. Per-cell effects can multiply costs, but screen-wide overdraw, Spine work, shaders, uploads and texture memory can matter too.

Use the real exported data (`project_data.json`) and runtime. A local harness is useful when there is no existing test page; no harness is bundled with this skill. Record runtime provenance and any local modifications. Measure the actual simultaneous instance count, including copies started at different times and offsets, and compare with a baseline under the same data, seed, frames and warm-up.

Collect only metrics relevant to the concern:

- CPU update time, including per-layer timing if available.
- Draw calls, buffer upload bytes and useful graphics call counts. Upload bytes have caught whole classes of runtime bug.
- Live particle counts per emitter and per instance.
- Approximate overdraw (clipped sprite area over screen area) and actual baked texture dimensions/frame counts/memory.
- Frame-time distribution on representative hardware when claiming player-visible improvement.

Software rendering and headless environments may distort GPU timings; on an earlier build the same scene's render time measured both 19 ms and 2.5 ms on a software GPU. Use them to compare controlled CPU/structural metrics, label the environment, and avoid promising device FPS from those numbers.

## Test the expensive component

The supplied pack documented these historical cases; the numerical savings are examples, not expected results:

- A textured ribbon mesh per copy produced 31 draw calls for 15 cells, where the rest of the scene was 1. Later batching shared a mesh across copies of a layer, reducing the value of replacing it with a bake; check that the build in use shares it and that sharing is on.
- Work proportional to the square of the number of layers grew sharply with copied groups: one scene went from 3,552 to 64,032 spawn-sync normalisations a frame just by adding copies. Profile the implementation before reducing visual density to compensate for an engine issue.
- A hold kept a large population alive long after an earlier one-shot would have ended. Record the steady count per effect and name the heaviest layer.
- Large transparent glows increased overdraw; a full-screen bloom cost more than hundreds of small sparks. Small sprites, fewer layers or tighter bounds can help, depending on the scene.
- Reducing ribbon strands helped CPU cost in one case (3 strands cost about 2.5× the CPU of 1); measure the visual and runtime tradeoff in this build.

Change one meaningful factor at a time. For native versus baked versions, compare both current runtime cost and sheet memory, download size, visual fidelity and resolution. One per-cell case replaced a 3-strand ribbon trail with a baked energy beam around the cell frame (one sprite sheet plus a couple of small particle layers for crackle) and measured roughly a third of the update time and 1 draw call against 31, before ribbons shared a mesh. A prior claim of one-third CPU or one draw call is not a general guarantee. Check that the exported sheet's `spritesheet.originalWidth` (field observed on an earlier build) is close to the effect's real size; an oversized bake draws a large see-through quad per copy.

The supplied 0.9.50 guide describes fitted bake frames and per-layer Bake FPS/Detail: from 0.9.50 the Export Bundle fitted each sheet's frames to its effect plus about 4% slack for peaks between sampled frames, where older bundles used one shared box, and a sheet's frame count came from its layer's Bake FPS. Inspect the actual exported sheets and manifest before claiming those savings apply. Lower bake FPS only when the visual and game requirements permit; preview-video FPS is a separate setting.

Pixi versions and other engines can differ in batching and upload behavior; on an earlier build the runtime built a `ParticleContainer` per layer under Pixi 7 but not under Pixi 8, and upload behavior differed sharply between them. Test the engine the game actually ships. See [per-cell effects](../slot-vfx-per-cell-effects/SKILL.md) for copy phase/placement tests.

## Report the comparison

State the measured before/after, copy count, runtime version, device/environment and visual tradeoff. "Update time 8.17 ms to 5.49 ms, draw calls 31 to 3, p95 frame 17.4 ms to 11.9 ms" is a finding; "it feels smoother" is not. Retain the scenario and harness used so the comparison can be repeated. Distinguish measurement from a source-code hypothesis. Draft an engine report if useful, but do not send it externally without authorization or modify unrelated runtime code merely because profiling found a possible defect.
