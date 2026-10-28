---
name: spine-vfx
description: Prepare and revise effects on existing Spine actors in SlotVFX, including bone or slot particle attachment, loop review, sprite plates and recorded or runtime delivery.
---

Start with app/bridge state and inspect the existing Spine actor and its owned skeleton, atlas and page assets. The current MCP imports assets but `create_entity` does not create a Spine actor. For a new rig, use the desktop Spine import workflow or ask for a project with the actor already imported. Do not claim asset import alone instantiated it.

Read the relevant registered schemas: `particle.spineAttachment` plus matching `particle.emissionShape`, `spine.timelineLoopBlendSeconds`, `spine.spineTextureFx`, `spine.imageFxStack`, `spine.spineSpriteAttachments`, `spine.interleaves`, `path.spineBinding` or `group.spineBinding`. Verify actual bone, slot, skin and attachment names. Derived alpha samples belong to the editor; do not fabricate them. World/local simulation and follow/release parameters change whether emitted particles remain attached: inspect current schemas and test poses before and after release.

Review loops, draw order, deformations and attachment motion through natural playback in SlotVFX. Activate the intended clip, focus the actor or effect and play it using the existing editor controls; inspect the returned editor state. Observe a visibly moving part through several wraps. Use `slotfx_render_layout` only for a specific pose/alignment comparison; three frames do not establish a smooth loop. Crossfade may soften a seam; it does not repair every skeleton animation. Requested green-screen output needs an actual solid green scene/backdrop and a recorded color check; transparent WebM is a different deliverable, while MP4 is opaque.

Read [workflow routes and Spine verification caveats](references/workflows.md) for preview, recovery and delivery. Do not infer random-seek or merged-sheet bake parity from the successful natural-playback fixture. Separate the outputs explicitly:

- Recorded media: MCP recorder with exact actor/clip and bounded settings.
- Game runtime data: `export_runtime`; read fileWrite and warnings. Current MCP writes JSON/diagnostic files, not the complete engine bundle.
- Complete Game Runtime Export: use the editor export UI for runtime scripts and external assets, then exercise that engine's output.
- Spine-file export, particle-to-Spine bake and FX plate export: these have editor bake/export paths; no dedicated MCP tool currently completes them. MCP can prepare supported properties. Finish through the existing UI when available and authorized, or report the exact manual step.

Keep source skeletons/atlases and original artwork intact. Confirm the user's right to use the assets and runtime license requirements when selecting a delivery. Do not infer general Spine runtime parity from one successful editor render.

## Add or edit Spine animations

These tools exist only in SlotVFX builds that ship them. If `slotfx_get_spine_rig` is not in the tool list, tell the user to update SlotVFX to the latest release. Do not hand-edit the skeleton JSON instead.

Read the `slotfx://authoring-guide/spine-animation` resource first (or `slotfx_get_authoring_guide` with section `spine-animation` when resources are unavailable), then:

1. `slotfx_get_spine_rig`: bones, slots, constraints, events, mesh attachments and the timeline types this rig's Spine version has.
2. `slotfx_get_spine_animation`: the keys of the animation you start from, usually the idle.
3. `slotfx_propose_spine_animation`: a new or edited animation as ops. They are checked against the rig; the proposal waits on the layer and changes nothing yet. A key's `curve` is `"linear"`, `"stepped"`, `{bezier:[cx1,cy1,cx2,cy2]}` (fractions of the segment's time and value change) or `{points:[cx1,cy1,cx2,cy2]}` (seconds and values, 4.x rigs; on 3.x only where a fraction is exact). Handles outside the segment's times are refused.
4. `slotfx_preview_spine_animation`: key frames posed by the layer's own Spine runtime. Fix what reads wrong and propose again. Sample times are clamped to the animation's duration, so it cannot show a second cycle: check a loop seam by comparing the poses at 0, just before the end and at the end.

The animator applies a proposal from the "AI animations" banner on the Spine layer (Preview, Apply, Discard); Apply is one undo step. No MCP tool applies it. A new proposal for the same animation does not replace an older one, and no MCP tool discards a Spine proposal (`slotfx_discard_proposal` clears only semantic change proposals): ask the animator to discard stale ones in the banner.

Keys you can write: bone, slot and constraint timelines; draw order (`moveSlot`, `setDrawOrder`, `resetDrawOrder`); deform on meshes (`displaceDeform` first, then `blendDeform`, `scaleDeform` or `copyKeys`, raw offsets last); sequence frames (Spine 4.1+); dark colour on slots set up with one; inherit modes (Spine 4.2+). A key type the rig's version lacks is refused.

Craft: start and end on the idle pose. Build an action as anticipation, strike, overshoot, recovery. To make an animation read differently, change the pose and silhouette, not small secondary parts.

To retarget an animation between rigs, `slotfx_propose_spine_mapping` proposes a bone mapping; the animator reviews and applies it in Retarget Animation.

SlotVFX does not include a Spine license. To export Spine animations or use the Spine Runtimes in their products, users need their own Spine license from Esoteric Software.
