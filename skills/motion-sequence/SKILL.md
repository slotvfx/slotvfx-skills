---
name: motion-sequence
description: Author SlotVFX trailers, motion graphics and multi-stage sequences using clips, Scene Animator states, recorder scenarios, shaders, artwork and Spine animation.
---

Inspect the scene, existing clips, state machine and trailer document. Use the structure that fits the request: a clip for one continuous animation, a Scene Animator for event-driven states, a recorder scenario for a timed demonstration of those events, or trailer document tools for editorial/media work. Do not convert every sequence into a logo reveal or rebuild the editor externally.

Use `get_trailer_document`, `prepare_trailer_media` and `edit_trailer_document` only after reading their current action schemas, revision requirements and asset support. Preserve existing transitions, clips, audio and track membership. Time units differ between seconds, frame-grid keys and recorder frames; use explicit exact-time or frame semantics and read representative values back.

For states, inspect trigger declarations and parameter schemas. A recorder scenario can play over its base timeline; choose a neutral base when overlapping content would contaminate the take. `matchScenario` resolves scenario timing; it is not the same as repeating a looping clip. Distinguish entry, hold and exit behavior for variable durations; a single clip can suffice, with separate stages only when their control is needed.

Read [workflow routes, motion and recording checks](references/workflows.md); use relevant bundled logo-reveal, spin-showcase or showcase-video detail when available, and [motion craft](../slot-vfx-motion-craft/SKILL.md) to choose eases, springs, staggers and beats and write them as exact keys. Review entry, turning points, transitions and tail in SlotVFX itself. Activate the intended clip before playing it, focus the relevant result, and inspect editor state. For recording requested by the user, pass the exact timeline/scenario and per-job fps, dimensions and frame count. Poll lifecycleState rather than assuming a queued take completed. Preserve sound and validate its sync. Native title/callout recording does not establish game-runtime text/group-motion support. Return the editable sequence ready in SlotVFX and any explicitly requested verified media; expose editor-only bake/export steps clearly.

Use natural playback in the existing editor for motion review. Chat frame strips and recorded files are separate requested outputs or targeted diagnostics. Keep authored loop/duration and existing recorder settings intact when merely showing the sequence. Never expand an inspection-only tool policy.
