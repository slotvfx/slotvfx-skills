---
name: slot-vfx-hold-loops
description: "Create or repair SlotVFX effects that sustain for variable durations, such as anticipation, win count-ups and cell highlights. Separate entry from sustain, verify loop seams and explicit stopping in the target runtime."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Sustained highlights, anticipation and celebrations

Determine what starts the effect, what ends it, whether the entry should repeat, and whether stopping should fade or cut. Preserve the current approved design while changing its lifetime. Use existing notes when present; `duration: -1` can be intentional.

## Separate entry from sustain

Entry layers are usually short bursts with zero continuous emission (`emissionRate: 0` with `emissionBursts` and a short `duration` such as 0.1–0.4 s): crown bursts, shards, shock rings, centre blooms. Sustain layers use continuous emission, a stable sprite, or a deliberate repeating animation. On builds supporting it, `duration: -1` keeps sustain emission open-ended. Change only the intended sustain layers. An anticipation is usually all sustain.

Do not assume a burst list repeats at every kind of loop seam. The supplied pack observed entry bursts not replaying on a clip's own loop, while base-timeline wraps reset them: on a 4.5 s tier clip, 60 crown-burst particles at 0.2 s, then 0 at 4.7 s and again at 9.2 s past two seams, while the body held at about 960. The 0.9.59 runtime source agrees: a clip's own loop wrap does not reset the particle layers it owns. Verify the actual playback route and version. Keep bursts off sustain layers, because a rhythm built from a burst list beats once and then goes silent. An emission rate at the beat's own rate (1 / gap) gives the same cadence indefinitely; more structured rhythm may need a timeline or explicit loop logic.

One clip may be enough. Separate entry/hold/exit clips or a state machine can be appropriate when the game already uses them or needs independent transitions. Choose the simplest structure that satisfies the actual integration, not a universal ban on either approach.

## Runtime lifetime is version-specific

Before 0.9.42 the runtime released a non-looping instance at the clip duration while the editor kept simulating. Historical measurement, same group with a 3.2 s clip in headless Pixi (live particles):

| played with | 1 s | 3 s | 3.5 s | 6 s | 12 s |
| --- | --- | --- | --- | --- | --- |
| `loop: true` | 145 | 165 | 168 | 168 | 166 |
| `loop: false` | 145 | 165 | **0** | **0** | **0** |

From 0.9.42 (source-checked on 0.9.59) a non-looping clip that reaches its end is held. Everything its clock drives (keyed images, sprite sheets, Spine parts) freezes on the last frame, while its particle layers keep simulating. The copy is released once its layers have nothing left to show, so a `duration: -1` layer holds until the game stops it; an open-ended emitter needs an explicit game stop. A looping clip samples its keys modulo the clip length, so `loop: true` replays keyed animation every lap.

Do not pass `loop: true` by habit or without checking whether it repeats an intro or changes keyed animation. Never use it on a hold whose clip has a keyed entrance. For a particle-only hold without bursts it changes nothing visible and keeps pre-0.9.42 builds holding. A sustain carried by keys, a sprite sheet or Spine stops moving at the clip end unless the clip loops; when such a sustain follows a keyed entrance, give the sustain its own looping clip (inferred from the same 0.9.59 source, not yet run). On an earlier build the clip's own loop flag was the editor default and the fallback when the game passed nothing; keep it off for a keyed entrance, and when the clip opens with bursts (that build's editor preview replayed them every lap).

Test the exported engine the game ships, even on a recent build. Confirm the intended `loop` argument, clip default, entry repetition, final-key behavior and stop/tail behavior. Editor preview, recording and runtime playback are distinct tests.

## A continuous body can be one sprite

A single textured sprite can give a cleaner held shaft, frame or tint than many overlapping glows, which break into blobs or bands where they overlap. A starting recipe from the pack is one stationary particle (speed 0) with `lifeSpan: 60`, rate 0.833, Emit On Start enabled and `maxParticles: 1`; a lifetime ramp reaching full alpha at 0.006 gives about a 0.36 s fade-in, then holds to 0.99. Emit On Start is not a default: without it the first sprite arrived at 1.2 s. Do not make the sprite a burst; burst layers are reset on base-timeline wraps, where it would fade in again every lap.

That recipe is finite: it may fade, die and respawn around 60 seconds. Test beyond the intended maximum hold, including replacement if applicable. For indefinite holds, choose a supported stable sprite or lifetime arrangement with a verified entry fade. Immortal particles may sample a fixed ramp point; a normal lifetime fade is not guaranteed to animate. Confirm the first particle is present immediately.

Prewarm is optional and measured; it costs startup time on every play. Use it only if needed for the first frame or an established ambient population, after trying a burst at t=0, a burst start-age spread, or immortal particles with toroidal wrap. If an immortal t=0 burst in a looping clip goes missing on frame 0 or at a seam and the fault reproduces, `prewarmDuration` 0.2 s fixed it on an earlier build. Do not add it to every hold or forbid it globally.

## Verify both staying and stopping

Preview before and after the clip boundary, at two and four clip lengths, and at the expected longest hold. Use `includeImage: false` renders for counts and frames or natural playback for appearance. Inspect:

- Entry particles end once and do not unexpectedly repeat.
- Sustain remains visually continuous; count variation may be natural, but there is no unexplained thinning or seam spike.
- Intended emitters are active; investigate unexpected `silentEmitters` entries rather than requiring every entry emitter to remain live.
- A game stop ends emission and produces the specified tail or fade, with no leaked instance.

Set editor preview duration longer than the clip; otherwise playback stops at the clip end and the seam is never seen. For runtime delivery, test these same cases in the actual runtime even on a recent build. Report sustained particle count and the heaviest layer, since the cost persists for the full hold.
