---
name: slot-vfx-hold-loops
description: "Create or repair SlotVFX effects that sustain for variable durations, such as anticipation, win count-ups and cell highlights. Separate entry from sustain, verify loop seams and explicit stopping in the target runtime."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Sustained highlights, anticipation and celebrations

Determine what starts the effect, what ends it, whether the entry should repeat, and whether stopping should fade or cut. Preserve the current approved design while changing its lifetime. Use existing notes when present; `duration: -1` can be intentional.

## Separate entry from sustain

Entry layers are usually short bursts with zero continuous emission. Sustain layers use continuous emission, a stable sprite, or a deliberate repeating animation. On builds supporting it, `duration: -1` keeps sustain emission open-ended. Change only the intended sustain layers.

Do not assume a burst list repeats at every kind of loop seam. The supplied pack observed entry bursts not replaying on a clip's own loop, while base-timeline wraps reset them. Verify the actual playback route and version. A steady emission rate can produce simple repeating beats; more structured rhythm may need a timeline or explicit loop logic.

One clip may be enough. Separate entry/hold/exit clips or a state machine can be appropriate when the game already uses them or needs independent transitions. Choose the simplest structure that satisfies the actual integration, not a universal ban on either approach.

## Runtime lifetime is version-specific

The supplied pack reports that before 0.9.42 a non-looping instance was released at clip end, whereas later builds hold final keys and allow particle layers to continue until exhausted; an open-ended emitter therefore needs an explicit game stop. These are historical reports, not verification of every later engine.

Test the exported engine the game ships. Confirm the intended `loop` argument, clip default, entry repetition, final-key behavior and stop/tail behavior. Do not automatically pass `loop: true` without checking whether it repeats an intro or changes keyed animation. Editor preview, recording and runtime playback are distinct tests.

## A continuous body can be one sprite

A single textured sprite can give a cleaner held shaft, frame or tint than many overlapping glows. A starting recipe from the pack is one stationary particle with `lifeSpan: 60`, rate 0.833, Emit On Start enabled and `maxParticles: 1`; a lifetime ramp reaching full alpha at 0.006 gives about a 0.36 s fade-in.

That recipe is finite: it may fade, die and respawn around 60 seconds. Test beyond the intended maximum hold, including replacement if applicable. For indefinite holds, choose a supported stable sprite or lifetime arrangement with a verified entry fade. Immortal particles may sample a fixed ramp point; a normal lifetime fade is not guaranteed to animate. Confirm the first particle is present immediately.

Prewarm is optional and measured. Use it only if needed for the first frame or an established ambient population; do not add it to every hold or forbid it globally.

## Verify both staying and stopping

Preview before and after the clip boundary, at two and four clip lengths, and at the expected longest hold. Inspect:

- Entry particles end once and do not unexpectedly repeat.
- Sustain remains visually continuous; count variation may be natural, but there is no unexplained thinning or seam spike.
- Intended emitters are active; investigate unexpected silent emitters rather than requiring every entry emitter to remain live.
- A game stop ends emission and produces the specified tail or fade, with no leaked instance.

Set editor preview duration long enough to see the boundary. For runtime delivery, test these same cases in the actual runtime even on a recent build. Report sustained particle count and the heaviest layer, since the cost persists for the full hold.
