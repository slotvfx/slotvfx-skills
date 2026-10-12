---
name: slot-vfx-performance
description: "Investigate SlotVFX frame-rate or export-cost problems with controlled measurements in the actual target runtime. Compare realistic copy counts, simulation, draw calls, uploads, overdraw and baked alternatives."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Measuring SlotVFX performance

Use this skill for a requested performance investigation or a material shipping concern. Match the scope to the question; an isolated visual tweak does not require a full profiling harness. Preserve the accepted look and original versions while testing alternatives.

## Establish a representative baseline

Identify the actual scene, target engine/version, device class and likely bottleneck. Per-cell effects can multiply costs, but screen-wide overdraw, Spine work, shaders, uploads and texture memory can matter too.

Use the real exported data and runtime. A local harness is useful when there is no existing test page; no harness is bundled with this skill. Record runtime provenance and any local modifications. Measure the actual simultaneous instance count, including copies started at different times and offsets, and compare with a baseline under the same data, seed, frames and warm-up.

Collect only metrics relevant to the concern:

- CPU update time, including per-layer timing if available.
- Draw calls, buffer upload bytes and useful graphics call counts.
- Live particle counts per emitter and per instance.
- Approximate overdraw and actual baked texture dimensions/frame counts/memory.
- Frame-time distribution on representative hardware when claiming player-visible improvement.

Software rendering and headless environments may distort GPU timings. Use them to compare controlled CPU/structural metrics, label the environment, and avoid promising device FPS from those numbers.

## Test the expensive component

The supplied pack documented these historical cases; the numerical savings are examples, not expected results:

- A textured ribbon mesh per copy produced 31 draw calls for 15 cells. Later batching shared a mesh across copies, reducing the value of replacing it with a bake.
- Work proportional to the square of the number of layers grew sharply with copied groups. Profile the implementation before reducing visual density to compensate for an engine issue.
- A hold kept a large population alive long after an earlier one-shot would have ended.
- Large transparent glows increased overdraw. Small sprites, fewer layers or tighter bounds can help, depending on the scene.
- Reducing ribbon strands helped CPU cost in one case; measure the visual and runtime tradeoff in this build.

Change one meaningful factor at a time. For native versus baked versions, compare both current runtime cost and sheet memory, download size, visual fidelity and resolution. A prior claim of one-third CPU or one draw call is not a general guarantee.

The supplied 0.9.50 guide describes fitted bake frames and per-layer Bake FPS/Detail. Inspect the actual exported sheets and manifest before claiming those savings apply. Lower bake FPS only when the visual and game requirements permit; preview-video FPS is a separate setting.

Pixi versions and other engines can differ in batching and upload behavior. Test the engine the game actually ships. See [per-cell effects](../slot-vfx-per-cell-effects/SKILL.md) for copy phase/placement tests.

## Report the comparison

State the measured before/after, copy count, runtime version, device/environment and visual tradeoff. Retain the scenario and harness used so the comparison can be repeated. Distinguish measurement from a source-code hypothesis. Draft an engine report if useful, but do not send it externally without authorization or modify unrelated runtime code merely because profiling found a possible defect.
