---
name: slotvfx-showcase-video
description: "Record requested SlotVFX clips or state-machine scenarios through MCP, verify true frame rate and loop behavior, save files reliably, and combine or deliver videos when requested. Supports named timelines and repeated cycles in 0.9.50."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Recording and delivering SlotVFX videos

Record only when requested. If the user wants to inspect effects directly in SlotVFX, leave the editable result ready there. Save only when requested. Preserve existing recordings and videos unless their deletion or replacement was requested. Use the current workspace for scratch files and its designated outputs folder for deliverables.

The installed 0.9.50 recorder schema was checked on 2026-09-26; limits marked 0.9.59 come from that build's recorder and scenario schemas. Read the current schema and `slotfx://authoring-guide/recording` when available, especially when a setting is refused. Version-specific observations from the supplied pack still need frame verification.

## Choose framing, frame rate and source

Use the requested FPS and dimensions. Infer established preferences from the current user's context; do not inherit another user's delivery defaults. Use freshly rendered frames at the requested FPS, and preserve the selected quality and audio.

Capture `x`/`y`/`captureWidth`/`captureHeight` describe a world-space rectangle. Output `renderWidth`/`renderHeight` describe encoded pixels. Preserve aspect ratio and frame the full intended effect with margin; for example, a 1920×1560 capture of a 1920×1638 board encodes at 1330×1080 rather than being stretched. Editor zoom is not an export crop. Add letterboxing, a blurred background or a 16:9 composite only when appropriate to the requested delivery.

`set_recorder` settings persist on the device, not in the project. Pass per-job settings to `start_recording` so a take does not depend on stale global recorder settings. Use prewarm (`prewarmSeconds`; about 2 s put ambient particles on frame zero on an earlier build) only when the scene needs an established first-frame population; check support, since the pack reports scenarios ignore it.

From 0.9.50, pass `timelineId` to record a named clip from a snapshot without switching the user's active editor clip, playback or settings. Each job captures a fixed project/settings snapshot at queue time (0.9.59), so later edits or clip switches do not change a queued take. Without `timelineId` and with no `stateScenarioId`, the recorder takes the active editing timeline, which was seen switching unexpectedly on an earlier build, most likely when a state was selected or previewed. For an ordinary clip, ensure no unintended state scenario is selected. Verify the returned source timeline/scenario (the `start_recording` reply includes `timelineId`/`stateScenarioId` from 0.9.47) and settings before trusting the take. On an older build requiring the active timeline, set it with `set_active_timeline`, capture, restore the original selection/playback and explain the visible limitation.

For a one-shot, derive frame count from duration and requested FPS, or use the supported matching option. Do not duplicate 30 fps frames and call that a newly rendered 60 fps animation.

## Loop cycles and scenarios

In 0.9.50, `matchTimeline: true` with `settings: { seamlessLoop: true, loopWithoutTimeline: false, repeatCycles: 3 }` requests three full clip cycles at the original speed, with keys and audio repeating each cycle; one take leaves no joins to crossfade. `repeatCycles` is 1–100, and values above one require those loop settings. With `seamlessLoop: false` the take is a one-shot that holds its keys at the end, even when the clip loops. Current limits still apply (`frameCount` ≤ 72,000 on 0.9.59). Check the actual recorded seam; schema support is not proof that a particular effect loops cleanly.

Scenarios run once and use `matchScenario`, not repeated clip cycles. A scenario defines an initial state, timed trigger steps and an end hold. On 0.9.59, `set_recorder_scenario` takes `initialStateId`, `steps` (each with `atSeconds` ≤ 600 or `afterStateComplete: true`, plus optional `params`; e.g. `[{ "atSeconds": 0, "trigger": "spin" }]`) and `endHoldSeconds` (default 1, max 600). Inspect the resolved duration and frame count through `get_recorder`, then record the intended `stateScenarioId` with `matchScenario: true`. Scenario definitions are project data, while selecting one is session-only; save the project if they are meant to persist.

The base timeline plays beneath state clips by design. Supply a neutral base `timelineId` (static scene only) rather than letting a selected effect contaminate a scenario; before 0.9.50, make it active before recording. For several spins, either use a supported complete scenario or separate scenarios whose starting/ending states match, e.g. *Idle → Spin → Win 1*, then *Win 1 → Spin 2 → Win 2*, so the grids match at every join. Crossfades (0.1 s worked) are a presentation choice, not a substitute for correct continuity.

Historical issues in the supplied pack:

- Before 0.9.48, particles in state clips used scenario time: with `spin` at 0.8 s, every burst fired 0.8 s early. An immediate trigger plus a separate editing-timeline take for any idle intro was a workaround.
- Before 0.9.49, a masked image layer visible at t = 0 of a scenario could render as a white rectangle on frame zero. Inspect the first frames; trim (`trim=start_frame=1`) only if the fault is present and timing is accounted for.
- Before 0.9.48, `render_layout` of late scenario frames timed out because each frame re-simulated the scenario from zero. Use the recorder for scenarios on those builds and spot-check stills from the MP4.

Recording after a clip ends may hold keys and continue some content: on an earlier build, keys held their last values while `duration: -1` layers, Spines and immortal particles kept running, giving a spin → win tail without a cut. Do not infer runtime instance lifetime from that. In the game runtime from 0.9.42 (source-checked on 0.9.59), a non-looping clip that reaches its end is held: keyed images, sprite sheets and Spine parts freeze on the last frame while particle layers keep simulating, and the copy is released once its layers have nothing left to show, so a `duration: -1` layer holds until the game stops it. `loop: true` replays keyed animation every lap; do not add it by habit, and never on a hold whose clip has a keyed entrance. Use the [hold skill](../slot-vfx-hold-loops/SKILL.md) and test the target runtime when shipping behavior matters.

## Retrieve the exact job safely

Queue captures sequentially unless current tools support independent parallel jobs and the task benefits from them. Keep a manifest of timeline/scenario, settings, expected duration/frames, job ID, exact output path and completion state. The 0.9.50 queue has six slots including completed jobs; when it is full, `start_recording` fails with "The queue holds six exports."

Poll `get_recording` with bounded waits and useful progress updates until `job.lifecycleState` is `completed`, and note its `byteLength`. `save_recording` opens the native Save As workflow; poll `job.saveState` until `saved`, `cancelled` or `failed`. A saved job can remain `state=ready` for retrieval. Use the dialog when that interaction is intended. For authorized direct retrieval into the workspace, use `read_recording` (0.9.59: base64 chunks, default 64 KiB, `length` up to 1 MiB), one call at a time:

1. Follow the exact job ID, offset and `nextOffset` from its responses until `nextOffset` is null.
2. Decode the exact returned data or tool-result file programmatically; depending on the client, a large chunk may arrive as a tool-result file rather than inline. Do not select the newest file by a wildcard and do not print base64.
3. Check contiguous offsets, decoded byte counts and final size against `totalBytes` and the job's `byteLength`, and the `sha256` when returned.
4. Write to a new task-owned partial file; promote it to the final path after validation. Never append blindly to an existing video on retry.

Do not delete tool-output files or other jobs as a side effect of decoding. After verifying a saved file, discard only this task's retrieved queue job (`cancel_recording { discard: true }`) if needed to free a slot. Older files and unrelated queue jobs remain untouched unless deletion was requested.

## Verify the video before combining

Use `ffprobe` (with `-count_frames`) and decode checks for actual frame count, dimensions, frame timestamps, FPS, audio tracks and duration. Inspect representative frames and motion: onset, peak, tail, frames zero through three, both sides of loop seams, state changes and joins. A contact sheet helps: `ffmpeg -i in.mp4 -vf "select='not(mod(n\,15))',scale=330:-1,tile=6x5" -frames:v 1 sheet.png` tiles every 15th frame. Counts alone cannot detect a frozen second lap.

For a visually changing loop, compare matching phases across cycles and different phases within each cycle. A still-looking hold can be intentional; assess against the authored effect. If a build cannot capture multiple cycles correctly, capture one verified lap and repeat it only when that satisfies the user's request, explaining the assembly.

To distinguish a Spine from its static substitute, compare a cropped cell at two times where its animation should differ (0.2 s apart worked). To verify a state transition, measure a property animated only by the next state, such as a frame pulse.

## Combine and deliver

Preserve requested ordering, FPS, dimensions and audio. Compatible silent H.264 clips can be concatenated without re-encoding. Use the bundled [logo recording helper](../slotvfx-logo-reveals/scripts/package_previews.py) when suitable; it requires Python 3, ffmpeg and ffprobe. It validates compatible silent clips and produces combined videos and optional ZIP/index reports. It deliberately rejects audio and incompatible inputs. Otherwise use a suitable local assembly workflow.

When normalization is necessary, explain material changes such as resizing or encoding; do not silently lower FPS or drop audio. Derive trim times and crossfade offsets from actual durations, put every input on a common frame rate and time base (`fps=<fps>,settb=1/<fps>`; `xfade` requires it), and validate the combined result. With crossfade length `d`, the first `xfade` offset is the first segment's length minus `d`; each later offset is the previous offset plus the length of the segment that previous `xfade` added, minus `d`. Do not copy hardcoded durations or remove frame zero from a healthy take.

Optional example for a 16:9 1080p delivery of a narrower take that is already 1080 px high, centred on a blurred copy of itself:

```bash
ffmpeg -i take.mp4 -filter_complex \
  "[0:v]split=2[fg][bgsrc];
   [bgsrc]scale=1920:-2,crop=1920:1080,gblur=sigma=36,eq=brightness=-0.05:saturation=1.15,vignette=PI/6[bg];
   [bg][fg]overlay=(W-w)/2:0,format=yuv420p[v]" \
  -map "[v]" -map "0:a?" -c:a copy -c:v libx264 -crf 16 -movflags +faststart composite.mp4
```

At brightness −0.05 with a light vignette, the background kept the scene's colour; darker settings read as black bars.

Use destination-specific limits only when they actually apply; file-transfer limits depend on the client. There is no universal 20 MB/30 MiB limit for desktop workspace files. Keep a good-quality master; produce a smaller delivery copy only when useful or requested. When a destination does impose a size limit, encode to it and check the size before delivering. In one ~30 s 1080p showcase, crf 17 produced 37 MB, while two-pass at about 4.9 Mb/s produced 18.4 MB with no visible loss:

```bash
ffmpeg -y -i composite.mp4 -c:v libx264 -preset slow -b:v 4900k -maxrate 7500k -bufsize 10000k -pass 1 -an -f mp4 /dev/null
ffmpeg -i composite.mp4 -c:v libx264 -preset slow -b:v 4900k -maxrate 7500k -bufsize 10000k -pass 2 -pix_fmt yuv420p -movflags +faststart delivery.mp4
```

Save under a new descriptive, versioned filename (e.g. `…_v4_1080p.mp4`) in the designated outputs folder; never overwrite a previous cut. Provide an absolute local Markdown link and, when supported and useful, an inline native preview. Include a combined download when requested and individual files/archive as appropriate. Do not assume cloud-only paths, upload tools or automatic external sharing. When checking a transferred still, compare decoded pixels rather than hashes: one client's file transfer re-encoded PNGs (bytes changed, pixels did not), while WebP files arrived byte-identical.

## Recover without losing work

For a lost capture context ("The capture context was lost"), isolate suspected layers/assets in a controlled preview. One lossless WebP was implicated in the supplied pack, and replacing it with a palette PNG fixed it; it is a troubleshooting lead, not a ban on that format. For a timeout, check recording/renderer state before retrying and avoid piling jobs onto a busy renderer; on an earlier build a render timeout kept the renderer busy, so wait about 60 s before the next call and keep render strips to 3–8 frames, one call at a time. After a crash, compare saved state (`get_editor_state.lastModified`) and available checkpoints before overwriting anything; before 0.9.48 a crash's Retry could reopen an older copy with Save enabled. Cloud revision checks apply only when that service is actually present.
