---
name: slotvfx-mcp-authoring
description: "Author and refine SlotVFX projects through MCP: discover effect parameters, preserve existing work, manage clip membership and keyframes, read back writes, and verify changes. Use alongside the relevant visual-design skill."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Authoring in SlotVFX through MCP

Inspect the current project, relevant entities and timelines before editing. Current user instructions define the scope. New alternatives normally get new named groups and clips; revisions change the specified version. Preserve unrelated work. Creating an effect does not authorize deleting existing layers, recordings or shared assets, posting reports, or exporting video.

This skill adapts the supplied 0.9.50 pack. The installed 0.9.50 MCP schema was checked on 2026-09-26; older behavioral observations below came from the pack and require reproduction when material. Prefer current schemas and actual frames over historical assumptions.

To add or edit Spine animations, use `slotfx_get_spine_rig`, `slotfx_get_spine_animation`, `slotfx_propose_spine_animation` and `slotfx_preview_spine_animation` with `slotfx://authoring-guide/spine-animation`; the [Spine skill](../spine-vfx/SKILL.md) covers the flow. If those tools are missing, ask the user to update SlotVFX rather than editing skeleton JSON.

## Discover features and read back writes

Use `find_features` (a plain-language query works) for a feature ID, then `get_feature_schema` for its shape. Registry IDs can differ from stored paths: `particle.subEmitter.trailSpacing` writes `config.subEmitterTrailSpacing`. A rejected patch's error lists every valid ID; search that list rather than guessing. Inspect tool warnings as well as success flags.

From 0.9.50, Image FX references such as `get_feature_schema { featureId: "image.fxParams.shineSweep" }` expose parameter defaults, ranges and named enums. Read the relevant schema before editing the FX stack. Consult `slotfx://authoring-guide/image-fx` when available for interacting controls and animation format; for example, Shine Sweep's intensity also scales its halo. Preserve unrelated stack items. Unknown parameter names may be stored without visible effect; from 0.9.50, single, batch and patch writes (dry runs included) return a warning naming them, so read `warnings` rather than trusting `ok`, and verify a frame. For Color Tint, verify both `amount` and `add` return to their intended final values; the pack reports independent additive strength, so key `add` back to zero to end a flash.

Read back any nested config object after writing it (`get_entity`) and check a field omitted from the patch. Older builds replaced `particle.subEmitterConfig`, an open map rather than a declared settings group, on partial writes: writing seven size keys to a trail child dropped eighteen others, including texture, gravity, color ramp, emission rate, lifespan, speed and blend mode, while the reply's `changedKeys` listed every key of the object and so looked like a normal write. The pack reports merging from 0.9.47, but the reply still does not show which behavior you got. Keep the original full object so a mistaken replacement can be repaired by writing the whole object back with the change folded in.

If an authorized target is locked, remember its lock state, unlock, edit and relock. A patch naming a locked layer fails, and the message includes the unlock call. Older builds required separate calls: unlock and relock in the same patch was refused as a duplicate edit. Do not broaden the edit to other locked layers.

## Clip membership and animation

- Pass explicit `clipIds` where the creating tool accepts them. On an earlier build, `create_layers` into a brand-new group put the layers in whichever clip was open. `create_entity` has no `clipIds` parameter: on 0.9.59, two images created while a clip was active were added to that clip's `includedLayerIds`.
- `duplicate_entity` (source-checked on 0.9.59): with `clipIds` omitted, the copy joins the clips its original plays in, not the open clip. `clipIds: []` gives no direct membership, but **whole-parent-group inclusion still applies**: a clip that includes the copy's parent group (`group:<id>`) still includes it. Read the reply's `duplicate.clipIds`, which lists the clips that effectively include the copy, and inspect the destination group's membership too.
- Duplicating a group rejects `clipIds`; the group copy duplicates its owned clips. Inspect returned IDs and shared shader bindings before further writes.
- After creation, read affected timelines with `get_timeline` and correct them with `update_timeline`. `includedLayerIds` replaces the full list; send it whole and preserve original entries outside the requested change.
- Remove a layer from a clip only when it should never appear there; non-members are hidden while the clip plays, so membership is the cheapest way to keep such a layer off. `hiddenBy: ["timeline"]` means absent from the active clip, not unused everywhere.
- Inspect animatable properties before generating tracks. The pack observed Spine `visible`, `x`, `y`, `scale`, `rotation`, `animation`, `loop`, `skin` and `opacity` (opacity from 0.9.49; before that a Spine could not fade, so an image of the same symbol was swapped in and faded); image `opacity`, `visible`, `x`, `y`, `scaleX`, `scaleY` and `rotation`; particle `x`, `y` and `opacity`. It also observed `config.*` keys being accepted without animation. Recheck current support rather than promising arbitrary config animation.
- On 0.9.59, `set_timeline_keyframes` keys with `tangents {mode:"free", out:{dt,dv}, in:{dt,dv}}` evaluate exactly as a CSS cubic-bezier; the sibling skill [motion craft](../slot-vfx-motion-craft/SKILL.md) turns named eases and springs into such keys. Use `timeMode: "exact"` for handle-carrying keys (the default `legacy` snaps to tenths of a second).
- Image FX parameter keys are stored in the FX stack and may not appear in `get_timeline`. Inspect both when diagnosing motion.

Tested schema limits: 25 initial feature values (`featureValues`) per particle in `create_layers`, 100 entries per `reorder_layers` call, 200 timeline keys per `set_timeline_keyframes` call (still 200 on 0.9.59), and six recording jobs including completed ones. On an earlier build, `cancel_recording { discard: true }` freed a slot; use it only on a task-owned job. Check current tool limits before a large batch.

## Large key edits

1. Snapshot the full affected tracks, membership and duration; retain a task-owned undo/snapshot or an authorized local saved copy for substantial changes. Cloud history checkpoints are not generic local backups.
2. Generate exact-time keys locally, by script. To replace a track, delete the old keys by their exact times (`delete_timeline_keyframes` with `timeMode: "exact"`) before setting the intended keys. A set only updates keys at matching times, so old keys at other times survive and mix with the new ones.
3. Upload ordered, resumable batches below the current limit, for example 180 keys, with deletes before sets. Pass each generated array unchanged and stop on any error. Default to sequential uploads. Use separate agents only when delegation is authorized and their writes do not overlap.
4. "Not connected to the bridge" means the call never reached SlotVFX: retry once, unchanged. After any other timeout or uncertain result, inspect state, read back the attempted edit and check `list_audit_log` before retrying a mutation. Avoid duplicate creates.
5. Compare readback keyframe counts **and representative values/times** with the generated plan. `get_timeline` with `includeKeyframes: false` returns each timeline's `keyframeCount`, which should match the generator exactly. Each `set_timeline_keyframes` reply reports how many keys changed and how many already matched (from 0.9.50; on 0.9.59, for example, "Updated 7 timeline keyframes; 0 already matched"), so a rewrite that reports every key as already matched changed nothing. Counts alone do not prove correctness.
6. If interrupted, do not save a half-applied state. Resume, or restore the task's recorded changes from its snapshot through local undo or an authorized saved copy; `create_checkpoint`/`restore_checkpoint` need cloud Main History. Do not close the editor without saving or discard unrelated user work as a recovery shortcut.

## Coordinate and playback observations

- The pack and logo workflow observed counter-clockwise positive `image.rotation`; a y-down `atan2` angle needed negating, and unnegated angles mirrored every sloped segment. Verify one sloped segment.
- `image.maskPath` points are image pixels from the top-left, not the center, and scale with the layer, so a masked copy of a strip placed at the strip's own position shows exactly one cell. Test the actual exported runtime if masks matter to delivery.
- Before 0.9.48, a step key also eased the segment arriving at it. A linear guard key 1–2 ms before the step key (just before a wrap, or at the end of a long linear run) was a workaround; from 0.9.48 the arriving segment follows the chord, so do not add it to newer builds without a reproduced need.
- Hidden or finished content can still cost work. Set `visible: false` for sustained hidden periods and stop finished clips when the design permits. Opacity zero or off-screen placement is not evidence that simulation stopped: on an earlier build, Spines parked off-screen kept animating behind the reels and dropped frames. Hidden scene Spines skip their updates, but a hidden Spine owned by a clip that is still playing kept advancing (measured on 0.9.49). On 0.9.47 the recorder and `render_layout` drew a Spine that starts hidden and is shown by a mid-clip `visible` key.
- From 0.9.49, `update_transition` and `delete_transition` support existing state-machine edges. `update_transition` keeps omitted fields, the edge's ID and its matching order; both take `dryRun`, are one Undo step and accept the Any-state (`*`) source. Read their current schemas and use `dryRun` when useful before a substantial flow edit. On older builds no tool edited or deleted a transition: plan triggers first, and change a flow by adding new triggers and transitions (`spin2`, `spin3`) rather than retargeting old ones.

## Measure and preserve

Keep verification claims separate:

- **Configuration checked:** readback confirms intended values, clip membership and layer relationships. Tool success or particle counts alone do not establish appearance.
- **Editor visually checked:** observed natural playback over the real art at the intended display size. Name any visible issue or phase not inspected; a screenshot cannot verify a loop seam or continuous travel by itself.
- **Runtime tested:** exercised the actual exported target and the relevant instance count, aiming, stop/skip or cleanup behavior. Editor FPS and an export receipt do not establish this.

Use these distinctions in a concise handoff when material; do not create a separate report for every tweak. Report unverified claims as untested. If a requested check is blocked, say what remains instead of substituting a successful property write as evidence.

Review representative times through natural playback in SlotVFX. Use bounded `render_layout` captures for a particular diagnostic or an explicitly requested comparison. For diagnostics, `includeImage: false` provides particle counts and bounds (`liveParticlesByEmitter` and `contentBounds` per strip cell). Bounds need a transparent render, because a painted `background` fills the frame; use the real layout separately to judge placement and readability. Frame generously before concluding nothing drew: a dot outside a too-small frame has caused a false bug report.

Counts and bounds diagnose activity and clipping. To verify unchanged appearance, compare decoded pixels or actual images under matching seed/time/settings; compressed image byte length is not an equality test. Check entry, peak, tail and any loop seam. To tell an animating Spine from a still image in a recording, crop its cell on frames 0.2 s apart: the Spine's pixels change and the still image's don't.

`get_bridge_status` returns `compatibility {compatible, level, warnings, errors}` plus contract fingerprints and versions for both sides (0.9.59). A bridge fingerprint mismatch is a compatibility signal, not proof that every tool works or fails. Inspect installed versions and current schemas, perform read-only checks, and use a supported dry run to assess the intended write. Resolve a relevant incompatibility before mutation, and mention any remaining mismatch in the handoff. Do not restart the user's app without considering unsaved work.

Only clean up clearly task-owned disposable objects after checking references and clip membership; delete a task-owned throwaway group with `deleteChildren: true`, then confirm the clips are back to their original membership. Preserve pre-existing objects unless their deletion was requested. Save the accepted result when requested; restore temporary selection/playback when appropriate. Update existing build notes for material behavior changes or handoff requirements: what changed, the measured before and after, and why. When removing a workaround, say what replaced it so nobody puts it back. A small visual tweak does not require creating a new documentation system.
