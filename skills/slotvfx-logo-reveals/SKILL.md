---
name: slotvfx-logo-reveals
description: Create, refine, preview, and export logo reveal animations in SlotVFX through MCP, including independently moving logo parts, particles, image FX, and selective shaders. Use for SlotVFX logo animation work; ordinary gameplay particle effects are outside this skill's main scope.
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# SlotVFX Logo Reveals

Build an editable reveal in the user's current SlotVFX project. Preserve the logo's identity and use motion, timing, and accents to make the chosen concept readable. Current user instructions override these defaults and earlier examples.

## Establish the task

Connect to the available SlotVFX MCP and inspect the current project, logo assets, active timeline, and relevant groups before editing. Resolve project and asset IDs live; examples in this skill contain no reusable project IDs.

Distinguish a promotional video from an effect intended to run inside a game. This changes the choice between shader/image FX and native particles. Infer the destination from the conversation when possible; ask only if the distinction materially affects an otherwise unclear request.

New concepts normally get a new named group and timeline. A revision normally updates the specified version. Preserve unrelated work, and interpret requests such as “only the edges” or “keep the bottom” as exact boundaries. Deletion, recording, and replacement requests apply to their stated targets; creating a reveal does not itself authorize clearing old recordings or effects.

Read [MCP workflow](references/mcp-workflow.md) when connecting, authoring masks/keyframes/FX, or diagnosing surprising tool behavior. Check the current schema. The original authoring observations were tested against 0.9.49; named recording, repeated-cycle capture options and Image FX schema availability were checked in the installed 0.9.50 MCP on 2026-09-26. Schema checks do not establish every runtime behavior.

## Choose the visual idea

Start with a clear action: assemble, ricochet, brake, strike, correct, launch, or recover from a glitch. Distinguish variants through choreography and rhythm as well as color. Use [reveal recipes](references/reveal-recipes.md) for the motion concepts and splitting/pivot technique tested in this session.

Design checks:

- Match motion style to the requested identity: playful, mechanical, elegant, cinematic or magical as appropriate.
- Vary choreography and rhythm; use a material-aware reflection selectively, or omit it, rather than repeating the same shine sweep.
- Move components independently only when requested or useful, and preserve correct final alignment and source identity.
- Judge generated particles at their actual display size; simple silhouettes can communicate better than intricate sprites.
- Match shader coverage and glow to the target: compact gameplay effects and cinematic videos have different needs.

These are design checks, not inherited personal preferences. Do not add generated images merely because generation is available.

## Build and revise

Establish the logo's entrance, strongest beat, settling motion, and readable finish. Tune those before adding a dense effects stack. Use [motion craft](../slot-vfx-motion-craft/SKILL.md) to key those eases, springs and beats exactly. Keep particles tied to contacts, acceleration, discharge, or another visible cause. Parameterize dimensions, colors, pivots, timing, and intensity for the current logo.

Keep components independently editable and name layers by their role, for example “Mechanical Snap · Emblem Left Piece” or “Speedrun · Brake Sparks.” For a localized revision, change the named component and visually verify the untouched components instead of redesigning the whole effect.

Preview representative moments at normal viewing size: onset, fastest movement, impact, and settled logo. Look for clipped parts, incorrect pivots, repeated sprite silhouettes, persistent tint, blur ghosts, unreadable text, and activity continuing beyond its intended beat. Check a loop boundary when the effect is intended to loop.

For additive work, compare original entity feature values, group membership, timeline membership/keyframes, and any shared shader graphs against the starting snapshot. Exclude transient selection, playback time, and evaluated bounds from preservation comparisons. For existing-work edits, compare against the authorized change set.

## Finish in the requested form

Save to the current project and leave the intended group/timeline selected for review. Report its exact name and what changed.

When the user wants to inspect SlotVFX directly, finish there. For requested recording, combined downloads, or game-engine delivery, read [delivery and runtime](references/delivery-and-runtime.md). That reference includes a helper for validating and combining compatible silent recordings.

Keep the entrypoint small as the skill evolves. Add verified techniques to the relevant reference, date version-specific behavior, and update recipes after real feedback. Do not turn unverified bug reports into permanent workarounds.
