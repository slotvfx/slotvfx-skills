---
name: spine-vfx
description: Prepare and revise effects on existing Spine actors in SlotVFX, including bone or slot particle attachment, loop review, sprite plates and recorded or runtime delivery.
---

For requested key cleanup, use the separate **Optimize animation** preview/apply workflow for eligible SlotVFX or Spine tracks, including independent bone tracks on physics/slider rigs in app 0.9.84 and newer. Read [supported optimization, error units and pose protection](../slot-vfx-motion-craft/references/animation-review.md#optimize-animation-preview-then-apply); preserve skipped data and locked poses, inspect savings/error before Apply, then verify playback with Undo available.

For native animation size and game budgets, read [animation review and budgets](../slot-vfx-motion-craft/references/animation-review.md). Run `slotfx_review_animation` for the clip and target; Spine Performance also reports key counts, animation/deform JSON, unique atlas memory and configurable page-side budgets. Bone/constraint curves can be cheaper than dense deform offsets when visually equivalent; sparse offset encoding and necessary deformation must be preserved. Whole Character FX is disabled in the 0.9.82 app profile; use supported attachment FX or explicitly requested rendered capture.

Start with app/bridge state and inspect the existing Spine actor and its owned skeleton, atlas and page assets. The current MCP imports assets but `create_entity` does not create a Spine actor. For a new rig, use the desktop Spine import workflow or ask for a project with the actor already imported. Do not claim asset import alone instantiated it. If no `slotfx_` tools are available at all, SlotVFX isn't connected to Claude Code yet; say so plainly instead of attempting the work, and help the user connect it with [Connect SlotVFX](../slotvfx-mcp-authoring/references/connect-slotvfx.md).

Read the relevant registered schemas: `particle.spineAttachment` plus matching `particle.emissionShape`, `spine.timelineLoopBlendSeconds`, `spine.spineTextureFx`, `spine.imageFxStack`, `spine.spineSpriteAttachments`, `spine.interleaves`, `path.spineBinding`, `group.spineBinding` or `path.maskSettings` (a path used as a Spine mask). Verify actual bone, slot, skin and attachment names. Derived alpha samples belong to the editor; do not fabricate them. World/local simulation and follow/release parameters change whether emitted particles remain attached: inspect current schemas and test poses before and after release.

Review loops, draw order, deformations and attachment motion through natural playback in SlotVFX. Activate the intended clip, focus the actor or effect and play it using the existing editor controls; inspect the returned editor state. Observe a visibly moving part through several wraps. Use `slotfx_render_layout` only for a specific pose/alignment comparison; three frames do not establish a smooth loop. Crossfade may soften a seam; it does not repair every skeleton animation. Requested green-screen output needs an actual solid green scene/backdrop and a recorded color check; transparent WebM is a different deliverable, while MP4 is opaque.

Read [workflow routes and Spine verification caveats](references/workflows.md) for preview, recovery and delivery. Do not infer random-seek or merged-sheet bake parity from the successful natural-playback fixture. Separate the outputs explicitly:

- Recorded media: MCP recorder with exact actor/clip and bounded settings.
- Game runtime data: `export_runtime`; read fileWrite and warnings. Current MCP writes JSON/diagnostic files, not the complete engine bundle.
- Complete Game Runtime Export: use the editor export UI for runtime scripts and external assets, then exercise that engine's output.
- Spine-file export, particle-to-Spine bake and FX plate export: these have editor bake/export paths; no dedicated MCP tool currently completes them. MCP can prepare supported properties. Finish through the existing UI when available and authorized, or report the exact manual step.

Before exporting a Spine layer for a game, run `slotfx_check_spine_export`; `slotfx_get_authoring_guide` topic `spine-performance` explains its rows. It plays every animation with the rig's own Spine runtime and reports peak draw calls a frame on Pixi 8, blend switches, atlas pages, vertices, meshes, bone weights, unused bones and textures stored twice; `settings.instances` checks several copies at once. From 0.9.79, `slotfx_remove_spine_atlas_duplicates` merges duplicate textures in the atlas without touching the skeleton. It is a dry run by default and compares every region before writing; nearly identical regions merge only with `includeNear` and `confirmNear`, after the artist agrees.

Keep source skeletons/atlases and original artwork intact. Confirm the user's right to use the assets and runtime license requirements when selecting a delivery. Do not infer general Spine runtime parity from one successful editor render.

## Add or edit Spine animations

These tools exist only in SlotVFX builds that ship them. If `slotfx_get_spine_rig` is not in the tool list, tell the user to update SlotVFX to the latest release. Do not hand-edit the skeleton JSON instead.

Read the `slotfx://authoring-guide/spine-animation` resource first (or `slotfx_get_authoring_guide` with section `spine-animation` when resources are unavailable), then:

1. `slotfx_get_spine_rig`: bones, slots, constraints, events, mesh attachments and the timeline types this rig's Spine version has.
2. `slotfx_get_spine_animation`: the keys of the animation you start from, usually the idle. It reads applied animations only, not a pending proposal.
3. `slotfx_propose_spine_animation`: a new or edited animation as ops. They are checked against the rig; the proposal waits on the layer and changes nothing yet. A key's `curve` is `"linear"`, `"stepped"`, `{bezier:[cx1,cy1,cx2,cy2]}` (fractions of the segment's time and value change) or `{points:[cx1,cy1,cx2,cy2]}` (seconds and values, 4.x rigs; on 3.x only where a fraction is exact). Handles outside the segment's times are refused.
4. `slotfx_preview_spine_animation`: key frames posed by the layer's own Spine runtime. Fix what reads wrong and propose again. Sample times are clamped to the animation's duration, so it cannot show a second cycle: check a loop seam by comparing the poses at 0, just before the end and at the end. Its bone angles are world angles in y-down screen space, sign flipped against the rig (measured in 0.9.69): a bone's rotate value = -(its angle - its parent's angle) - its setup rotation. Use them to check a proposal's keys.

5. `slotfx_check_spine_motion` on the proposal (`proposalId`): it poses the animation with the rig's own runtime and flags joints bent past straight, frozen hips, stiff blocks, sliding feet, loop seams and idles far quieter than the rig's own. Fix every FAIL, then compare preview strips with the idle by eye; `slotfx_get_authoring_guide` topic `spine-character-motion` explains the rows.

The animator applies a proposal from the "AI animations" banner on the Spine layer (Preview, Apply, Discard); Apply is one undo step. No MCP tool applies it. A new proposal for the same animation does not replace an older one, and no MCP tool discards a Spine proposal (`slotfx_discard_proposal` clears only semantic change proposals): ask the animator to discard stale ones in the banner. No MCP tool records a pending proposal: an MP4 needs the animator to Apply first; until then, show 12-frame preview strips.

Keys you can write: bone, slot and constraint timelines; draw order (`moveSlot`, `setDrawOrder`, `resetDrawOrder`); deform on meshes (`displaceDeform` first, then `blendDeform`, `scaleDeform` or `copyKeys`, raw offsets last); sequence frames (Spine 4.1+); dark colour on slots set up with one; inherit modes (Spine 4.2+). A key type the rig's version lacks is refused.

Craft: start and end on the idle pose. Build an action as anticipation, strike, overshoot, recovery. To make an animation read differently, change the pose and silhouette, not small secondary parts.

To retarget an animation between rigs, `slotfx_propose_spine_mapping` proposes a bone mapping; the animator reviews and applies it in Retarget Animation.

SlotVFX does not include a Spine license. To export Spine animations or use the Spine Runtimes in their products, users need their own Spine license from Esoteric Software.

## Coordinate effects with the performance

Identify release/contact and recovery in the existing animation, verify the attachment's position at those moments, and review the actor and FX together. Coordinate requested target/symbol reactions and sound from the same cue. Use supported layer order or `spine.interleaves` for near/far depth after reading its current schema. Read [visual critique](../create-vfx/references/visual-critique.md) for weak impact, flat depth or a timing mismatch. Preserve an approved performance during an FX-only revision; additional actor edits and host hit-stop must remain within the request and current tool capabilities.

## Protected poses, gaps and direct bone posing

For the 0.9.80 pose-plan workflow, read `localPoseGapWorkflow` and `localBonePosing` in `slotfx://authoring-guide/spine-animation`. Use the live schemas for `slotfx_get_spine_pose_plan`, `slotfx_edit_spine_pose_plan`, `slotfx_edit_spine_pose_gap` and `slotfx_set_spine_pose_preview`. This enrolled local-only Spine 4.2 profile requires fixed skin, isolated track 0 and no physics; it does not extend general animation proposals to every rig/version or cloud project. These pose-plan enrollment limits are separate from Optimize animation's support for independent tracks on physics/slider rigs.

Read the current layer/animation/skin, exact canonical times, approvals and project/revision/source/plan context tokens before edits. Gap candidates belong strictly between approved pose-and-timing-locked endpoints. Use deliberate `prepareBoundary` only when requested, then read fresh tokens. `propose` or `stageReturn` stages a candidate; preview it without applying source edits. Applying requires the artist's explicit Apply request, the exact candidate digest and fresh context tokens. Preserve protected endpoints and outside-gap data; respect refusal diagnostics instead of routing around them.

For a new marked pose, use the current pose-plan `savePose` operation with its fresh context tokens and exact time. It stores the edited pose in a marker without changing the original animation. Lock/approve the intended endpoints and use the AI gap workflow for in-betweens. Do not substitute source-animation key edits for saving a marker pose.

For direct Original corrections, use pose-plan `setBoneKeys` with exact `timeSeconds` and unique `boneEdits`. Translate/rotation values are native setup-relative animation offsets, not scene/world coordinates. The owner/profile, constrained-bone and approved-pose guards still apply; dry-run first and read back accepted values. Keep these changes separate from staged alternatives and general `slotfx_propose_spine_animation` proposals. Do not round close subframes to display frames.
