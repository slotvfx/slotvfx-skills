---
name: slotvfx-mcp-authoring
description: "Author and refine SlotVFX projects through MCP: discover effect parameters, preserve existing work, manage clip membership and keyframes, read back writes, and verify changes. Use alongside the relevant visual-design skill."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Authoring in SlotVFX through MCP

Inspect the current project, relevant entities and timelines before editing. Current user instructions define the scope. New alternatives normally get new named groups and clips; revisions change the specified version. Preserve unrelated work. Creating an effect does not authorize deleting existing layers, recordings or shared assets, posting reports, or exporting video.

This skill adapts the supplied 0.9.50 pack. The installed 0.9.50 MCP schema was checked on 2026-09-26; older behavioral observations below came from the pack and require reproduction when material. Prefer current schemas and actual frames over historical assumptions.

## Discover features and read back writes

Use `find_features` for a feature ID, then `get_feature_schema` for its shape. Registry IDs can differ from stored paths: `particle.subEmitter.trailSpacing` writes `config.subEmitterTrailSpacing`. Inspect tool warnings as well as success flags.

From 0.9.50, Image FX references such as `get_feature_schema { featureId: "image.fxParams.shineSweep" }` expose parameter defaults, ranges and named enums. Read the relevant schema before editing the FX stack. Consult `slotfx://authoring-guide/image-fx` when available for interacting controls and animation format. Preserve unrelated stack items. Unknown parameter names may be stored without visible effect; inspect warnings and verify a frame. For Color Tint, verify both `amount` and `add` return to their intended final values; the pack reports independent additive strength.

Read back any nested config object after writing it and check a field omitted from the patch. Older builds replaced `particle.subEmitterConfig` on partial writes; the pack reports merging from 0.9.47. Keep the original full object so a mistaken replacement can be repaired without losing other fields.

If an authorized target is locked, remember its lock state, unlock, edit and relock. Older builds required separate calls. Do not broaden the edit to other locked layers.

## Clip membership and animation

- Pass explicit `clipIds` when creating or duplicating layers. In 0.9.50, `[]` excludes a copied layer from direct clip membership, but **whole-parent-group inclusion still applies**. Inspect the destination group's membership too.
- Group duplication can also duplicate clips. Inspect returned IDs and shared shader bindings before further writes.
- After creation, read affected timelines. `includedLayerIds` replaces the full list; preserve original entries outside the requested change.
- Remove a layer from a clip only when it should never appear there. `hiddenBy: ["timeline"]` means absent from the active clip, not unused everywhere.
- Inspect animatable properties before generating tracks. The pack observed Spine transforms, visibility, animation, skin and opacity (opacity from 0.9.49); image transforms and visibility; particle x/y/opacity. It also observed `config.*` keys being accepted without animation. Recheck current support rather than promising arbitrary config animation.
- Image FX parameter keys are stored in the FX stack and may not appear in `get_timeline`. Inspect both when diagnosing motion.

Tested schema limits: 25 initial feature values per particle, 100 entries per layer reorder, 200 timeline keys per call, and six recording jobs including completed ones. Check current tool limits before a large batch.

## Large key edits

1. Snapshot the full affected tracks, membership and duration; retain a task-owned undo/snapshot or an authorized local saved copy for substantial changes. Cloud history checkpoints are not generic local backups.
2. Generate exact-time keys locally. To replace a track, delete the old keys by their exact times before setting the intended keys. A set does not remove keys at other times.
3. Upload ordered, resumable batches below the current limit, for example 180 keys. Default to sequential uploads. Use separate agents only when delegation is authorized and their writes do not overlap.
4. On connection errors, inspect state and read back the attempted edit before retrying a mutation whose completion is uncertain. Avoid duplicate creates.
5. Compare readback keyframe counts **and representative values/times** with the generated plan. Counts alone do not prove correctness.
6. If interrupted, resume or restore the task's recorded changes from the checkpoint. Do not close the editor without saving or discard unrelated user work as a recovery shortcut.

## Coordinate and playback observations

- The pack and logo workflow observed counter-clockwise positive `image.rotation`; a y-down `atan2` angle needed negating. Verify one sloped segment.
- `image.maskPath` points are image pixels from the top-left and scale with the layer. Test the actual exported runtime if masks matter to delivery.
- Before 0.9.48, a step key could affect the incoming segment. A linear guard key just before a wrap was a workaround; do not add it to newer builds without a reproduced need.
- Hidden or finished content can still cost work. Set `visible: false` for sustained hidden periods and stop finished clips when the design permits. Opacity zero or off-screen placement is not evidence that simulation stopped.
- From 0.9.49, `update_transition` and `delete_transition` support existing state-machine edges. Read their current schemas and use `dryRun` when useful before a substantial flow edit.

## Measure and preserve

Review representative times through natural playback in SlotVFX. Use bounded `render_layout` captures for a particular diagnostic or an explicitly requested comparison. For diagnostics, `includeImage: false` provides particle counts and bounds. Bounds need a transparent render; use the real layout separately to judge placement and readability. Frame generously before concluding nothing drew.

Counts and bounds diagnose activity and clipping. To verify unchanged appearance, compare decoded pixels or actual images under matching seed/time/settings; compressed image byte length is not an equality test. Check entry, peak, tail and any loop seam.

A bridge fingerprint mismatch is a compatibility signal, not proof that every tool works or fails. Inspect installed versions and current schemas, perform read-only checks, and use a supported dry run to assess the intended write. Resolve a relevant incompatibility before mutation. Do not restart the user's app without considering unsaved work.

Only clean up clearly task-owned disposable objects after checking references and clip membership. Preserve pre-existing objects unless their deletion was requested. Save the accepted result when requested; restore temporary selection/playback when appropriate. Update existing build notes for material behavior changes or handoff requirements. A small visual tweak does not require creating a new documentation system.
