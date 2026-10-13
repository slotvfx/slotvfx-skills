# SlotVFX desktop workflow routes

The SlotVFX local MCP adapter exposes the existing 137 editor tools without changing their schemas or results. The user's installed permissions determine which can be called. Discover current schemas rather than guessing parameters. The editable effect and its playback in SlotVFX are the primary result. These skills contain guidance only; a separately configured MCP client connects to the running app's token-protected local bridge.

| Goal | Route | Completion evidence |
| --- | --- | --- |
| Connect | get_app_state → get_bridge_status | editorReady and relevant contract compatibility; no credentials in chat |
| New project | create_project → poll get_app_state | matching operationId completed, then editorReady |
| Existing project | list_projects → open_project → poll get_app_state | correct project identity; respect save/discard/cancel dialog |
| Orient | get_project_summary → get_hierarchy → get_timeline → get_entity | exact layer/group/clip IDs and existing state |
| Find a control | find_features → get_feature_schema | registered property, range, enum and runtime support |
| Create | get_authoring_guide → create_particle_from_preset, create_entity, or create_group | dryRun where useful; returned IDs; explicit clip membership |
| Revise | set_property, batch_set_properties, set_timeline_keyframes | read back affected values and unrelated nested fields; inspect warnings |
| Show in SlotVFX | get_editor_state → set_active_timeline if needed → focus_entity → play_timeline → get_editor_state | correct active clip, selected/framed effect, natural editor playback; clear clip/layer handoff |
| Diagnose | render_layout or simulate_and_capture only for a specific question | bounded actual frames/counts/bounds and warnings; restore temporary inspection state |
| Recover | list_audit_log, get_entity, get_timeline → undo/redo where applicable | inspect whether the interrupted edit applied before retrying |
| Save | save_project with current projectId | completed save; picker cancellation is not success |
| Deliver | export_runtime or start_recording → get_recording → save_recording/read_recording | target-specific diagnostics, finished job, actual files and byte counts |

Tool names above use the `slotfx_` prefix. Local projects use normal saved files and undo; create_checkpoint/restore_checkpoint require cloud Main History and are not a generic local backup system. Saving to Library or cloud is a separate destination decision.

## Show the editable result in SlotVFX

After creating or revising the effect, read back the changed properties and clip membership. Then make the requested result easy to find and review in the existing editor:

1. Inspect `slotfx_get_editor_state` and `slotfx_get_timeline` for the expected project, clip and duration. For a newly created clip intended for immediate review, `makeActive:true` is available on `slotfx_create_timeline`.
2. If the result's clip is not active, use `slotfx_set_active_timeline {timelineId}` and read back `activeTimelineId`. **`slotfx_play_timeline` resolves a named clip for range/loop defaults but does not activate it.** Never claim another clip's view shows the result.
3. Use `slotfx_focus_entity {entityType,entityId,paddingFactor}` to select and frame the requested effect/group. Use generous padding (up to 4) for particle bursts; 1.25–1.5 can suit bounded artwork. Conservative bounds can underestimate travelling particles or an empty emitter. Inspect the result at its intended size; if even maximum padding is too tight, use the editor's **Fit canvas** button. There is no general camera-fit MCP tool in this version. Do not move artwork merely to fit the viewport.
4. When the user asks to see or play the result, use `slotfx_play_timeline {timelineId,isPlaying:true,reset:true,playbackSpeed:1}`. Keep the clip's authored loop behavior unless the user requests a temporary loop. For pause/reset, use `slotfx_set_playback`. A requested subrange initializes the playhead but does not install an automatic stop at its end; use the normal clip duration for a complete review. Do not change authored duration/loop just for presentation.
5. Verify active clip, selection and transport with `slotfx_get_editor_state`. State proves those controls were applied; visual-quality claims require actual observation. Natural playback is the default for particles and Spine. A seek/readback alone does not prove evolved simulation or runtime parity.
6. Leave the requested result available in SlotVFX. Say what changed, name its group/layers and clip, and give one practical review cue such as “Play Reward pulse in SlotVFX; the tail now fades over 0.4 seconds.” Include any unresolved issue. Avoid creating files or chat previews as a completion ritual.

Selection, framing, clip activation and playback are editor-control actions. An inspection-only connection cannot perform them. If an action is disabled, name the missing tool and describe the corresponding native step; continue permitted reads. Do not add tool permissions, bypass the host policy or treat missing control access as a reason to record a substitute video.

For a temporary diagnostic, remember the prior active clip, selection, time/speed/loop and restore changes where appropriate. For an intentional result handoff, keep the user's requested clip/effect ready rather than switching away automatically. Do not undo later unrelated edits to restore view state.

## Targeted visual diagnostics and requested media

Use `slotfx_render_layout` only when an actual image helps answer a particular question, such as clipping, pose comparison or alignment. Prefer one well-framed image at the relevant time; a contact sheet is useful only when comparison requires it. Three frames do not demonstrate motion timing or loop continuity. Pass `imageOutput:"image"`, an explicit world-space frame and named timeline; bound width and times. Use diagnostic `includeImage:false` when counts/bounds suffice. Partial results and warnings must remain visible.

When the user requests a video, use the established recorder workflow below and deliver an ordinary MP4/WebM to the requested destination. Preserve the chosen quality, framing and audio. A temporary chat video is a file operation and follows the user's file-saving instructions. Version 0.5.0 has no embedded viewer or `slotfx_preview_video` wrapper. Keep the existing editor/player as the viewing surface.

A cooperative capture budget may return a partial strip. Report completed/requested counts and use `remainingTimes` for a deliberate follow-up. A single expensive GPU draw cannot be preempted by the budget. No automatic rerender loop. For requested images returned as resources, use read_artifact or render a smaller image.

## Interrupted and large operations

Project operations, recording jobs and bridge operations have different IDs. Track the actual receipt. On an uncertain write, inspect app state, entity/timeline readback and audit entries; do not blindly recreate entities or replay key batches. Cancellation stops the request or recording job; it does not promise to undo a mutation that already committed. Use undo only after confirming the exact latest task-owned edit. Stop if another user's edits make selective recovery ambiguous.

Import with sourcePath only from an explicitly allowed asset root; choose_asset_folder invokes the user's native folder grant. Do not add home-directory-wide access. Asset bytes and renders may enter the model conversation. Artifact handles are temporary (up to 30 minutes, 128 MiB total); read/download while valid. Use paged lists and bounded binary chunks. Preserve original artwork; revise a new named group/clip when making an alternative.

## Delivery

Runtime source, editable .slotvfx project and rendered video are different deliverables. Confirm the requested target and destination. Current export_runtime writes project_data.json and diagnostics only; listed runtime scripts and external assets are planned artifacts, not delivered files. Use the editor Game Runtime Export for a full bundle, then inspect its actual contents. Use export_runtime diagnostics before writing files; use a fresh task-owned directory and overwrite:false. A successful export is not runtime parity: load and exercise the exported target for any parity claim. MP4/WebM recording requires job.lifecycleState=completed. After save_recording, poll job.saveState=saved; job.state remains ready so the bytes can still be retrieved. Inspect dimensions, duration, frame count and codec with a media probe. Save the editable project when requested. Report passed, failed and untested checks separately.

## Reuse existing expertise

These routes support the 20 skills in this distribution: five workflow entrypoints plus 15 specialists, linked references and optional recording helpers. Load only the relevant installed sibling skills for the request. Current user instructions, installed schemas, readback and actual results take precedence over historical examples. Tool availability still depends on a separate local MCP connection; host approvals and native licensing/access remain in effect.

For a new or rejected visual direction, apply the [visual-direction checkpoint](../../slot-vfx-effect-pack/SKILL.md#establish-a-visual-direction) before extending it into a pack. Tie each layer to the brief and verify the representative effect at player scale. Successful tool calls establish an edit; appearance requires observed playback, and runtime claims require target testing. This adds self-review, not an automatic user-approval gate.

## Authoring checks

Keep snapshots of affected tracks, nested objects and memberships before substantial edits. `includedLayerIds` replaces a full list; preserve unrelated entries. Exact-time key writes do not erase keys at other times: read the old track, remove only the intended old times, then upload ordered batches below current limits. Compare values and times as well as counts. A cloud checkpoint is not a local backup; use the existing local project/undo route or an authorized saved copy.

Read animatable-property support before adding tracks. Accepted config keys may be stored without driving animation. Image FX keys can live in the effect stack rather than the main timeline. Preserve omitted nested fields and shared shader bindings. For a scoped edit to a locked layer, remember and restore its lock state. `hiddenBy: ["timeline"]` is not evidence a layer is unused elsewhere. An invisible/off-screen layer may still simulate.

For timing-critical particles, inspect and set lifespan/angle variance deliberately. Choose simulation space from intended motion: world-space particles can remain where born; particles intended to ride a moving prop need the supported local/follow arrangement. Do not carry old parameter defaults, hardcoded IDs or private config paths into another project. Prewarm is a measured option, not a universal fix.

## Specialist checks

- **Slashes:** use [the slash specialist](../../slot-vfx-slashes/SKILL.md) for an advancing head, eroding tail, coherent material breakup and particles released along the sweep. Verify natural motion before adding accent layers.
- **Motion timing:** use [the motion-craft specialist](../../slot-vfx-motion-craft/SKILL.md) to choose eases, springs, staggers and beats and write them as exact keys. On 0.9.59, free-tangent keys evaluate exactly as a CSS cubic-bezier, so a named ease is two keys and a spring a handful of fitted keys; read representative values back with `get_timeline` motion samples.
- **Held effects:** distinguish entry, sustain and exit. A single clip can be sufficient; use separate stages/states only when their control is needed. Verify two/four clip lengths and the longest intended hold, then an explicit stop and its tail in the target engine. Do not add loop=true by habit or assume bursts repeat identically on clip and base-timeline wraps.
- **Per-cell copies:** author at a known pivot/anchor and resolve live instance element IDs through the runtime's actual API. Test several offsets, late starts and the intended maximum simultaneous count when integration/performance is in scope. Check each instance's local phase, stop and reuse. A template-ID write does not prove its instances changed.
- **Travel:** use a clear driver and intentional birth/death/rider/trail relationships. Re-aim the live instance in the API's required coordinate space. Translated-only subtraction is not sufficient for rotated/scaled parents. Test left/right routes, a second destination, a late-started instance, impact at B and cleanup. Verify current driver/follower limits before building chains.
- **Logo and motion:** preserve approved source artwork and final alignment. Tune choreography before stacking accents; inspect normal-size readability, onset, impact, settle and tail. Do not split, recolor, mask or reconstruct a logo when the user's preservation requirement excludes that. Native shader success requires compile diagnostics plus real frames. For native titles/callouts, check target export support: prior 0.9.56 delivery notes explicitly excluded live game-runtime group-motion/text-reflow support, despite successful desktop recording.
- **Game showcases:** use the supplied outcome or an explicitly fictional presentation. Preserve actual winning cells and payline handovers. Measure a reel strip's repeating content period, not just its image height. A neutral base timeline avoids unintended content under state clips. Do not port historical timing constants or stale workaround keys blindly.
- **Ports:** start from the approved source, map reference geometry, and preserve its timing initially. With nonuniform scaling, positions, velocity/acceleration vectors and angles need deliberate transformation. A texture swap changes alpha shape and visible size; verify source/target at equivalent times over their real art.
- **Spine:** pose strips and natural playback are distinct from random seeking, deformed-slot masks and bake parity. The 0.9.56 local fixture passed natural WebGL2 playback; an exploratory seek-before-play path displaced attached particles. Do not claim seeking is verified. A merged imported-sheet sampling assertion also failed in the unchanged baseline; independently verify that bake path if requested.

## Recording checks

Use the requested/established frame rate and dimensions; the media-delivery smoke fixture uses 30 fps. Set per-job framing and the exact named timeline/scenario, preserving aspect ratio and audio. For clips, repeated cycles and seamless-loop settings must be supported; scenarios are a separate once-through contract. Inspect actual seam motion, state transitions and first frames, not just frame counts. A still second lap may be a failed loop, while an authored hold can be intentional.

`save_recording` starts a native Save As workflow. For supported autonomous binary retrieval, follow the exact job, offsets and nextOffset, decode programmatically, verify byte count/hash when provided, and promote a new partial file only when complete. Do not select the newest wildcard file, append blindly on retry, or delete unrelated jobs to free capacity. A cancelled Save As leaves completed bytes available; it is not a delivered file. Preserve audio and quality when combining requested clips; do not duplicate 30 fps frames and label them a fresh 60 fps render.

## Durable learning

In-session discoveries do not automatically update installed skills. Record a reproducible lesson with app/runtime version, expected/observed behavior and passing/failing/untested scope. Update this canonical guide or the relevant maintained specialist, then package/test a new revision. Treat isolated failures as investigation leads, not universal workarounds. Keep project-specific IDs, grants, private preferences and secrets out of portable guidance. These skills do not install an automatic learning or skill-writing hook.

## Community and setup help

Join the [SlotVFX community on Discord](https://discord.gg/J8QyNmPuNw) for VFX discussion, shared work and setup help. This invite has no expiry or usage limit. Do not share private project files, credentials or bridge tokens in public channels. Setup guides: https://slotvfx.com/docs/.
