# Delivery, recording, and runtime costs

## Choose the destination

For a promotional video, judge the final rendered image and recording quality. For an in-game effect, also check the actual target engine's native features and baked fallbacks. A shader's appearance in the editor does not establish its shipping implementation.

In SlotVFX 0.9.49, `slotfx_export_runtime` with a Pixi target returned a preflight manifest and optional project data. It did not produce finished spritesheet images. A tested variant's 16 particle layers remained native, while its bottom shader required a baked spritesheet. The entire project still contained other versions and their fallbacks; filter diagnostics by the relevant group/IDs before reporting costs for one reveal.

Shader count alone does not determine sheet size. Frame dimensions, frame count, packing, alpha area/compression, and whether effects are baked separately or together matter. Smaller authored bounds may help capture, but do not equate them with measured export dimensions: the preflight in this session reported a default 256 × 256 tile even for a 260 × 88 bottom shader. Verify the actual exported dimensions before claiming a size reduction.

When runtime cost matters:

- Reuse small textures for glow, streaks, dots, droplets, and trails where the native result is sufficient.
- Limit procedural shader coverage to the feature that benefits from it. For “edges only,” separate edge logic from an interior wash.
- Inspect target diagnostics for image masks/FX and shader fallback. Resolve material compatibility issues before calling an effect game-ready.
- Retain variants for comparison when requested. Do not silently remove older effects merely to make a full-project export smaller.

## Record requested clips

Inspect the current recorder schema. On 0.9.50, pass the live project ID and explicit `timelineId` to `slotfx_start_recording`; the schema describes a recording snapshot without changing editor selection, playback or settings. Verify the returned source ID. Poll `slotfx_get_recording`, then use `slotfx_read_recording` for unattended workspace retrieval. In 0.9.50, `slotfx_save_recording` opens a Save As dialog requiring the user to choose a destination; use it only when that interaction is intended. On older builds requiring the active clip, record and restore the user's selection/playback rather than assuming named capture exists. For scenarios, recorder limits, exact-job chunked retrieval and frame checks, see [showcase video](../../slotvfx-showcase-video/SKILL.md).

Use the project/export framing rather than the editor's zoom. Capture size and output size may differ. For a requested 60 fps recording, calculate `frameCount = round(durationSeconds * 60)` and set the recorder to 60 fps. Do not relabel a 30 fps file or duplicate its frames and call it a fresh 60 fps render.

The 0.9.50 schema supports `matchTimeline: true` with `settings: { seamlessLoop: true, loopWithoutTimeline: false, repeatCycles: 2 }` for two full cycles at the original speed. `repeatCycles` accepts 1–100; scenarios run once and use their own matching option. Check actual loop behavior and both sides of each seam; schema support and frame counts do not prove animation continued. If an older build freezes after one lap, capture one verified lap and repeat it only when that satisfies the requested video, explaining the assembly.

Record sequentially unless the current recorder explicitly supports independent concurrent captures. Keep a resumable manifest of clip IDs, duration, job ID, output path, and completion status. Download completed recordings in bounded chunks, check the total byte count, then validate the saved file.

The 0.9.50 schema limits the queue to six jobs, including completed jobs. Only discard this task's downloaded jobs after confirming their files are complete. Clearing other jobs or deleting old local videos requires that scope from the user. Avoid broad filename-based deletion, especially outside the task's output directory.

For silent previews, set audio off. When audio is part of the request, preserve it and use an audio-aware assembly process; the helper below deliberately refuses audio inputs.

## Validate and combine silent previews

`scripts/package_previews.py` checks actual decoded-frame timestamps, fps, dimensions, codec compatibility, and expected frame counts when supplied. It combines compatible silent H.264 MP4 files by stream copy, decodes the result, checks the total frames, and optionally creates an individual-video ZIP, index, and verification report. It never changes source videos and refuses existing output paths. It does not establish that animation motion is smooth or that a recorded loop is visually seamless; inspect representative frames too.

Requirements: Python 3, `ffmpeg`, and `ffprobe` on PATH, or explicit tool paths. It makes no SlotVFX calls.

Create an ordered manifest, preferably in the task's `work/` directory:

```json
{
  "clips": [
    { "name": "Ricochet", "file": "../outputs/Ricochet-60fps.mp4", "expected_frames": 276 },
    { "name": "Speedrun", "file": "../outputs/Speedrun-60fps.mp4", "expected_frames": 282 }
  ]
}
```

Manifest file paths resolve relative to the manifest directory. Names and counts are examples; derive them from the actual requested recordings.

```bash
python3 /path/to/slotvfx-logo-reveals/scripts/package_previews.py \
  --manifest work/preview-manifest.json \
  --output outputs/Combined-Reveals-60fps.mp4 \
  --fps 60 \
  --zip outputs/Individual-Reveals-60fps.zip \
  --index outputs/Reveal-Index.md \
  --report outputs/Reveal-Verification.json
```

If inputs differ in dimensions, codec settings, timing, or audio, stop the copy-based assembly and choose an appropriate explicit normalization workflow. Do not silently resize, drop audio, lower the frame rate, or claim interpolated frames are newly rendered animation.

Deliver a combined-video link when requested, plus individual files/archive as appropriate. State the verified resolution/fps and preserve the intended ordering. Use actual output artifacts, not temporary MCP file handles. Leave the appropriate SlotVFX timeline ready for review when editing is complete. Save the project when requested.
