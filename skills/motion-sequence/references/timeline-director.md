# Timeline Director and Speed keys

This covers the 0.9.80 tool contract. Read connected schemas and `slotfx://authoring-guide/sequences`, `slotfx://authoring-guide/slow-motion` and `slotfx://authoring-guide/recording`. If they are missing, check app/MCP compatibility rather than inventing fields. Resolve actual clip, bar and asset IDs.

## Choose and arrange

Use a clip for one animation, Timeline Director for a fixed arrangement of clips, Scene Animator for event-driven states, or a recorder scenario to demonstrate those triggers. A scenario plays its state clips independently of the editing clip; no blank base clip is required.

A sequence has one row per source clip, with bars for its playbacks. Scene and Game object/Payline clips are supported; sequences cannot nest. `slotfx_edit_sequence` accepts `create:{name,sequenceId?,makeActive?}` or an existing `sequenceId`. Passing only `sequenceId` reads resolved rows, bars, markers, duration, overlaps, available clips and `exportBlocker`.

`addClips` puts each clip in its own row at the given `at`; it does not append them consecutively. Use `addBar` with explicit times for consecutive shots. `addBar` also repeats an existing row's clip. `removeBar` removes one playback, `removeClip` its row and bars, and `reorderRows` the row order.

Use sequence seconds for `at`, markers and `setEnd.endTime`; source clip seconds for `clipIn`/`clipOut`. `loopCount` repeats that trimmed range. Bar `speed` is a constant multiplier, and source Speed keys still affect duration. Re-read resolved start/end after changes. New same-clip overlapping bars are placed after existing playbacks; conflicting timing edits can refuse. `setEnd` with `null` restores the automatic end.

Replace example source IDs with real IDs, dry-run, inspect, then apply without `dryRun`:

```json
{
  "create": {"name": "Win chain", "sequenceId": "win-chain"},
  "operations": [
    {"op": "addBar", "timelineId": "intro-clip", "barId": "intro-bar", "at": 0, "clipIn": 0, "clipOut": 1},
    {"op": "addBar", "timelineId": "win-clip", "barId": "win-bar", "at": 1, "clipIn": 0, "clipOut": 1},
    {"op": "setMarkers", "markers": [{"id": "hit", "name": "Hit", "time": 1}]}
  ],
  "dryRun": true
}
```

One accepted call is one Undo step; a failing operation rejects the whole call. Submit collective moves or trim/speed corrections as consecutive `updateBar` operations so final geometry is checked together. Inspect overlaps between different source clips that may animate the same layer. Retain returned IDs for subsequent edits.

## Recorded showcases and export limits

Set `editorOnly:true` deliberately before using music, beat grids, titles, marker ties, media items or Blends. `crossfade` needs overlapping bars; `dip` uses bars before/after a cut. `setFade` affects a bar's layers or dips the frame to a colour. The editor calls these Blends; they are never live game transitions. Cleanup with `clearFades`, `untie` or `removeTitle` also works on game sequences; removing stored extras does not require enabling Editor only.

Titles use sequence `at`, duration, normalized vertical `y`, pixel `size`, fill and outline. `font` is a project font ID/name; `null` uses the built-in font. Use the returned `titleId` for edits; `setFade` accepts it in `barId` too.

`setMarkers` replaces the whole list, so preserve unrelated markers. `tieToMarker` binds a bar/title to a marker plus an offset; later marker moves move the tied item. Import sound into Assets before `setMusic {assetId,at}`. `assetId:null` removes music; `at` alone moves it. `setBeat` uses BPM and an offset in seconds into the music file of its first beat; `bpm:null` clears the grid. `findBeat` listens to assigned music through the desktop editor; read its result/diagnostics. The beat grid does not move bars automatically.

Explicitly Editor only clips/sequences are excluded from games; a game sequence referencing such a source is blocked. Resolve `exportBlocker` without silently clearing restrictions. Automatic filtering of unused Video edit content is a separate export rule.

## Media items and one blend model

Check the connected sequence guide for `media`, `blends` and `videoEdits` first; older builds don't have them, and then the operations above are the whole surface.

A trailer sequence can hold media items (loose video, images, text and sound) on media rows under its clip rows. Add them with `edit_trailer_document`, passing the sequence ID as `timelineId` (the Video edit `video`, `text` and `sound` operations; the media rows are made on the first edit). Read them back from `slotfx_edit_sequence` as `mediaItems`, with target IDs such as `image:<id>` and `audio:<id>`. Edit them with `editMedia`:

```json
{
  "sequenceId": "showcase",
  "operations": [
    {"op": "editMedia", "action": "move", "targetId": "image:gameplay", "startTime": 2},
    {"op": "editMedia", "action": "trim", "targetId": "image:gameplay", "startTime": 2, "endTime": 6},
    {"op": "editMedia", "action": "split", "targetId": "image:gameplay", "at": 4}
  ],
  "dryRun": true
}
```

A trim can reach into the source's handles. A video's own sound moves, trims and splits with its video. Split pieces stay on one row. `remove` takes the item off the sequence.

Every blend, on bars and media items, is read from `sequence.blends`. Use `setBlend {kind, from, to?, duration?, color?, curve?}` with `kind` `fade-in`, `fade-out`, `crossfade` or `dip`; `setBlendCurve {blendId, curve}`; and `removeBlend {blendId}`. The two kinds of item can look different: on bars a colour fade or `dip` covers the whole frame, while on media items a crossfade mixes the two images and a fade goes to a colour on that item only. Media items have no `dip`. `setFade`, `crossfade` and `dip` still work.

`tieToMarker` also accepts a media item (`barId: "image:<id>"`); the item then follows its marker. Moving a tied item keeps the tie with a new offset.

A Video edit opened in the editor becomes a trailer sequence with a copy of its media; its cues become markers, and items that start exactly on a cue are tied to it. The original stays until the artist chooses Keep or Go back. For one release, the Video edit commands also accept the converted Video edit's ID and act on its sequence.

## Speed keys

Use `slotfx_set_clip_slow_motion` for a whole source clip clock, not particle velocity or independent retiming of every layer. The preset takes `timelineId`, `slowSpeed`, `holdFrames`, `rampFrames` and `startFrame`; frame values use clip frame rate, not recorder FPS. Exact keys use source seconds or `frame`, one coordinate per key:

```json
{
  "timelineId": "intro-clip",
  "keys": [{"time": 0, "speed": 0.25}, {"time": 0.25, "speed": 0.25}, {"time": 0.5, "speed": 1}],
  "slowDownSound": false,
  "dryRun": true
}
```

This replaces the full Speed track and preserves other tracks. `remove:true` removes Speed keys. Speed is 0.05–4, with 1 normal; the slow-start preset requires below 1. A `curveId` shapes the next segment. The current limit is 64 keys; inspect the live schema for limits.

Read `clipDuration` versus `playedDuration`. Use played time for estimates and `matchTimeline:true` for a full take. Re-read sequence bar endpoints after source Speed edits. Recorder playback speed and bar speed are additional multipliers.

`slowDownSound:true` defaults to audio rate/pitch following the clip; `false` keeps normal-rate sound from its mapped cue. Omission preserves the previous choice. Sequence music uses its own clock. Do not promise pitch-preserving time stretching.

## Preview, record and deliver

Pass the returned `sequenceId` as `timelineId` to `slotfx_render_layout` or `slotfx_start_recording`. Use `matchTimeline:true` for a full take; repeated takes use `settings:{seamlessLoop:true,loopWithoutTimeline:false,repeatCycles:2}` within current limits. Bars and music repeat per cycle and clip at its End. Nonloop takes hold visuals while existing requested-window audio tails may continue. Check transitions, decoded audio and both sides of every loop seam.

Use per-job recorder settings, poll `lifecycleState` to `completed`, and verify/save the exact job when recording was requested. Save the editable project when persistence was requested. A successful preview or recording does not establish game-runtime parity.

Game sequences and clip Speed maps support Pixi, Phaser, Cocos and WebGL2. Test the exported target when claiming parity. Supplied runtime instances bind to their original spawn lifetime; sequence stop preserves newer game-owned playback. Test repeat/stop and destroyed/reused instances when relevant. Do not present parked native artwork rigs as shipped features, or media items and the merged editor as available in a build whose sequence guide does not list them.
