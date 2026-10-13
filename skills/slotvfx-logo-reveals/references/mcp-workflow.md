# SlotVFX MCP authoring notes

Original authoring tests used SlotVFX **0.9.49** on 2026-09-26. The installed **0.9.50** MCP schema was subsequently checked for named recording, repeated-cycle capture, imports and Image FX parameter references. Clip membership on duplicate/create and the import contract were re-checked on **0.9.59**. Distinguish those schema checks from visual/runtime tests. Prefer current tool descriptions before unfamiliar edits.

## Connection and inventory

Use the available SlotVFX MCP tools. If absent from tool discovery but the desktop app is installed, inspect its supported MCP integration and adapter shipped with that installed version. In this session, the bundled adapter exposed `createAutoDiscoveringSlotfxBridgeClient` and `callSlotfxTool`; an older source checkout exposed a stale interface. Use the local MCP adapter provided with a compatible SlotVFX Desktop build and the tools connected through your client. Do not copy another installation’s server, hardcode a former workspace path or print bridge credentials.

After resolving the current adapter module, its tested call pattern was:

```javascript
const client = createAutoDiscoveringSlotfxBridgeClient({ argv: [], env: process.env });
const result = await callSlotfxTool(client, toolName, args);
const data = result.structuredContent || result;
if (result.isError || data.ok === false) throw new Error(data.message || toolName);
```

Keep base64 payloads out of logs. For batches, save compact progress and artifact IDs so a restart does not duplicate successful work.

Useful reads:

- `slotfx_get_editor_state`: project ID, dimensions, playback, selection, counts.
- `slotfx_list_entities`: include hidden entities for preservation checks. Paginate or use an adequate supported limit; the tested default could omit layers beyond 200.
- `slotfx_get_entity`: `detail: "full"` returns all feature values/config; `fields` can retrieve named features.
- `slotfx_get_timeline`: returns the active/requested timeline plus timeline metadata. There was no `slotfx_list_timelines`. Fetch each relevant clip's full tracks when needed.
- `slotfx_get_assets` and `slotfx_export_asset`: inspect the actual logo or source sprite.
- `slotfx_find_features`: discover feature IDs/value schemas; the tested result limit was at most 50.
- `slotfx_get_feature_schema`: on 0.9.50, inspect `image.fxParams.<type>` for the relevant Image FX parameter defaults, ranges and named enums.
- `slotfx_import_asset`: accepts `sourcePath` (0.9.50+) with an optional `folderGrantId` from `slotfx_choose_asset_folder` for a user-approved folder; without a grant, paths resolve on the MCP server under its `SLOTFX_MCP_ASSET_ROOTS`. The 0.9.59 schema also takes a data URL, remote URL or inline data, and a programmatically encoded PNG data URL imported fine. Encode inline data programmatically; never transcribe base64 by hand.

Snapshot relevant original feature values, timeline memberships/tracks, and shared graphs before substantial batches. Avoid comparing transient geometry or visibility evaluated at different times.

## Timelines, groups, and bounded writes

- Give each new concept a unique group/timeline and explicitly include `group:<id>` rather than inheriting the scene.
- `slotfx_create_timeline` has `makeActive`; the default need not switch the editor. Pass the intended timeline ID to later animation calls.
- For layer duplication, set `clipIds` to destination clips. On 0.9.59 (source-checked): with `clipIds` omitted, the copy joins the clips its *original* plays in, not the open clip; `clipIds: []` removes direct membership, but a clip that includes the copy's parent group (`group:<id>`) still includes it. Read the reply's `duplicate.clipIds`, which lists every clip that effectively includes the copy. On 0.9.49, `clipIds: []` was rejected when the destination group was included whole in a clip; preserve existing membership while resolving the intended destination.
- `slotfx_create_entity` has no `clipIds` parameter. On 0.9.59, images created while a clip was active were added to that clip's `includedLayerIds`. Read the clip back after creating and correct it with `slotfx_update_timeline`, passing the full list.
- Group duplication copies the group's owned clips and rejects `clipIds` (0.9.59). Inspect returned IDs/memberships and shader bindings; do not assume a shallow copy or independent graph.
- Entity type is `effect`; shader-effect features use `vfxEffect.*`. Timeline targets use `vfx:<id>` for VFX effects. Check current schemas if uncertain.
- Tested write limits: 25 initial particle feature values, 100 property changes, and 200 timeline keys per batch.
- Use `timeMode: "exact"` for precise keys. Legacy time mode rounded to tenths.
- Recheck original timeline durations after clip creation/simulation. Main's reported duration changed during one workflow and was restored to its recorded baseline. Do not force a duration copied from this example.

## Image FX

The tested FX stack used `items`, each with an ID, type, enabled flag, and `params`. Animated scalar parameters used this form:

```json
{
  "id": "part-motion-blur",
  "type": "directionalBlur",
  "enabled": true,
  "params": {
    "angle": { "value": 0 },
    "strength": { "value": 0, "keyframes": [
      { "time": 0, "value": 0 }, { "time": 0.3, "value": 2 },
      { "time": 0.5, "value": 0 }
    ] },
    "length": { "value": 0, "keyframes": [
      { "time": 0, "value": 0 }, { "time": 0.3, "value": 2 },
      { "time": 0.5, "value": 0 }
    ] }
  }
}
```

Preserve unrelated stack items. In 0.9.50, first read `slotfx_get_feature_schema` for `image.fxParams.<type>`; use the current `slotfx://authoring-guide/image-fx` when available for interacting controls and parameter-animation rules. Read write warnings for unsupported names. Do not assume empty parameters produce a useful effect or that success proves visible behavior. Verify a frame; inspect UI labels or implementation only if the schema leaves a relevant gap. The `strength`/`length` pairing above is a 0.9.49 workaround, not a required 0.9.50 pattern.

## Particle and shader details

- Particle angle 90 moved **up**; positive gravity Y moved **down**. Early reveal scripts contained mistaken directional assumptions.
- `particle.faceDirection` controlled direction-facing rotation. Avoid guessed names such as `rotationIsDirection`.
- Particle colors used RGB 0–255 and alpha 0–1. `particle.ribbon.color` accepted RGB only and rejected an alpha member.
- `particle.separateSizeAxes` plus `startSizeX/Y` and `endSizeX/Y` worked for elongated glows. Small existing glow/soft-square textures supplied broad native light.
- Random texture flips and end-spin variance reduced repeated asymmetric silhouettes. They do not fix an overly detailed sprite.
- For independent shader variants, create independent graph IDs. Inspect bindings before graph edits/deletion.
- `uAbsoluteTime` in custom expressions provided seconds. Do not assume all time inputs share units. Derive looping phase explicitly, e.g. `2*pi*uAbsoluteTime/duration`.
- The custom expression accepted a GLSL body snippet with outputs such as `out_color` and `out_alpha`; node compilation before commit caught invalid code.
- Use `slotfx_set_shader_node_param` or an atomic graph patch. A side-only change should contain only side logic; renaming a layer does not narrow its coverage.

## Preview and save

`slotfx_simulate_and_capture` supported `timelineId`, `atTimeSeconds`, `fps`, `maxFrames`, `restorePlayback`, `imageOutput: "file"`, and capture options. Returned file path: `currentFrame.imageFile.path`. Diagnostics included renderer warnings and particle counts. Read the current schema rather than assuming all options persist.

`slotfx_focus_entity` used `paddingFactor`, not `padding`. Viewport framing is not an export crop. `slotfx_set_playback` used `playbackSpeed`, not `speed`.

When saving is requested, save with the live `projectId` and inspect the result. Leave the intended version selected for review; restore the user's active clip when appropriate for background recording.

## Earlier reports requiring fresh reproduction

The conversation included claims about multi-lap recorder freezes, white-tint/add behavior, particle morphing, radial-acceleration serialization, mask support, and normalized shader clocks. Do not present the entire list as verified current limitations. Reproduce a relevant issue in the installed version and distinguish editor behavior, exported data, and runtime behavior.
