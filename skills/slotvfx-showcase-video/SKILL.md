---
name: slotvfx-showcase-video
description: "Record requested SlotVFX clips or state-machine scenarios through MCP, verify true frame rate and loop behavior, save files reliably, and combine or deliver videos when requested. Supports named timelines and repeated cycles in 0.9.50."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Recording and delivering SlotVFX videos

Record only when requested. If the user wants to inspect effects directly in SlotVFX, leave the editable result ready there. Save only when requested. Preserve existing recordings and videos unless their deletion or replacement was requested. Use the current workspace for scratch files and its designated outputs folder for deliverables.

The installed 0.9.50 recorder schema was checked on 2026-09-26. Read the current schema and `slotfx://authoring-guide/recording` when available. Version-specific observations from the supplied pack still need frame verification.

## Choose framing, frame rate and source

Use the requested FPS and dimensions. Infer established preferences from the current user's context; do not inherit another user's delivery defaults. Use freshly rendered frames at the requested FPS, and preserve the selected quality and audio.

Capture x/y/width/height describe a world-space rectangle. Output width/height describe encoded pixels. Preserve aspect ratio and frame the full intended effect with margin; editor zoom is not an export crop. Add letterboxing, a blurred background or a 16:9 composite only when appropriate to the requested delivery.

Pass per-job settings to `start_recording` so a take does not depend on stale global recorder settings. Use prewarm only when the scene needs an established first-frame population; check support, since the pack reports scenarios ignore it.

From 0.9.50, pass `timelineId` to record a named clip from a snapshot without switching the user's active editor clip, playback or settings. For an ordinary clip, ensure no unintended state scenario is selected. Verify the returned source timeline/scenario and settings before trusting the take. On an older build requiring the active timeline, capture and restore the original selection/playback and explain the visible limitation.

For a one-shot, derive frame count from duration and requested FPS, or use the supported matching option. Do not duplicate 30 fps frames and call that a newly rendered 60 fps animation.

## Loop cycles and scenarios

In 0.9.50, `matchTimeline: true` with `settings: { seamlessLoop: true, loopWithoutTimeline: false, repeatCycles: 3 }` requests three full clip cycles. `repeatCycles` is 1–100, and values above one require those loop settings. Current duration/frame limits still apply. Check the actual recorded seam; schema support is not proof that a particular effect loops cleanly.

Scenarios run once and use `matchScenario`, not repeated clip cycles. A scenario defines an initial state, timed trigger steps and an end hold. Use `set_recorder_scenario`, inspect the resolved duration through `get_recorder`, and record the intended `stateScenarioId`. Scenario definitions are project data; save them if they are meant to persist.

The base timeline can play beneath state clips. Supply the intended neutral base `timelineId` where appropriate rather than letting a selected effect contaminate a scenario. For several spins, either use a supported complete scenario or separate scenarios whose starting/ending states match. Crossfades are a presentation choice, not a substitute for correct continuity.

Historical issues in the supplied pack:

- Before 0.9.48, particles in state clips reportedly used scenario time; an immediate trigger plus separate idle take was a workaround.
- Before 0.9.49, a visible masked image could produce a white rectangle on frame zero. Inspect the first frames; trim only if the fault is present and timing is accounted for.
- Late scenario still renders could be slow on older builds. Spot-check a recording if repeated simulation times out.

Recording after a clip ends may hold keys and continue some content. Do not infer runtime instance lifetime from that. The pack reports a lifetime change around 0.9.42; use the [hold skill](../slot-vfx-hold-loops/SKILL.md) and test the target runtime when shipping behavior matters.

## Retrieve the exact job safely

Queue captures sequentially unless current tools support independent parallel jobs and the task benefits from them. Keep a manifest of timeline/scenario, settings, expected duration/frames, job ID, exact output path and completion state. The 0.9.50 queue has six slots including completed jobs.

Poll `get_recording` with bounded waits and useful progress updates until `job.lifecycleState` is `completed`. `save_recording` opens the native Save As workflow; poll `job.saveState` until `saved`, `cancelled` or `failed`. A saved job can remain `state=ready` for retrieval. Use the dialog when that interaction is intended. For authorized direct retrieval into the workspace, use `read_recording` in supported chunks:

1. Follow the exact job ID, offset and `nextOffset` from its responses.
2. Decode the exact returned data or tool-result file programmatically. Do not select the newest file by a wildcard and do not print base64.
3. Check contiguous offsets, decoded byte counts and final size against the job's `byteLength`.
4. Write to a new task-owned partial file; promote it to the final path after validation. Never append blindly to an existing video on retry.

Do not delete tool-output files or other jobs as a side effect of decoding. After verifying a saved file, discard only this task's retrieved queue job if needed to free a slot. Older files and unrelated queue jobs remain untouched unless deletion was requested.

## Verify the video before combining

Use `ffprobe` and decode checks for actual frame count, dimensions, frame timestamps, FPS, audio tracks and duration. Inspect representative frames and motion: onset, peak, tail, frames zero through three, both sides of loop seams, state changes and joins. Counts alone cannot detect a frozen second lap.

For a visually changing loop, compare matching phases across cycles and different phases within each cycle. A still-looking hold can be intentional; assess against the authored effect. If a build cannot capture multiple cycles correctly, capture one verified lap and repeat it only when that satisfies the user's request, explaining the assembly.

To distinguish a Spine from its static substitute, compare a cropped cell at two times where its animation should differ. To verify a state transition, inspect a property animated specifically by the next state.

## Combine and deliver

Preserve requested ordering, FPS, dimensions and audio. Compatible silent H.264 clips can be concatenated without re-encoding. Use the bundled [logo recording helper](../slotvfx-logo-reveals/scripts/package_previews.py) when suitable; it requires Python 3, ffmpeg and ffprobe. The helper it validates compatible silent clips and produces combined videos and optional ZIP/index reports. It deliberately rejects audio and incompatible inputs. Otherwise use a suitable local assembly workflow.

When normalization is necessary, explain material changes such as resizing or encoding; do not silently lower FPS or drop audio. Derive trim times and crossfade offsets from actual durations, use a common time base, and validate the combined result. Do not copy hardcoded durations or remove frame zero from a healthy take.

Use destination-specific limits only when they actually apply. There is no universal 20 MB/30 MiB limit for desktop workspace files. Keep a good-quality master; produce a smaller delivery copy only when useful or requested.

Save under a new descriptive filename in the designated outputs folder. Provide an absolute local Markdown link and, when supported and useful, an inline native preview. Include a combined download when requested and individual files/archive as appropriate. Do not assume cloud-only paths, upload tools or automatic external sharing.

## Recover without losing work

For a lost capture context, isolate suspected layers/assets in a controlled preview. One lossless WebP was implicated in the supplied pack; it is a troubleshooting lead, not a ban on that format. For a timeout, check recording/renderer state before retrying and avoid piling jobs onto a busy renderer. After a crash, compare saved state and available checkpoints before overwriting anything; cloud revision checks apply only when that service is actually present.
