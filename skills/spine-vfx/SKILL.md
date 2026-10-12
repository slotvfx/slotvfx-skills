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
