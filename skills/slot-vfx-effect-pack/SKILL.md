---
name: slot-vfx-effect-pack
description: "Build a complete slot VFX pack in SlotVFX from a game brief, GDD and art: map the board, author effect groups and clips, verify in context, and prepare a practical game integration handoff."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Building a slot VFX effect pack

Use this workflow for a requested collection of gameplay effects. For an isolated effect, use only the relevant steps. For logo choreography, use the logo-reveal skill if available. Current user instructions override example designs and historical preferences. Preserve existing work; new alternatives get new named groups and clips unless direct edits were requested.

## Establish the brief and layout

Read the brief, source art, existing project and any build notes available. Notes explain deliberate oddities, but compare them with the current project. An open-ended `duration: -1` layer and a clip shorter than its content may intentionally sustain through a variable win count-up; do not convert it to a one-shot without understanding its trigger and stop contract.

Map cell centres, pitch, reel window, logo, badges and event anchors. Check placement over the real shipping background with `render_layout` and `background: "layout"`. Use transparent renders separately for isolated bounds. Where supported, bind to real layout anchors and grid cells rather than hardcoding every placement.

Agree only missing decisions that materially affect the result. Infer reasonable styling and timing from the existing project; do not require an approval at every stage.

## Establish a visual direction

Before authoring, connect the effect's gameplay purpose to its silhouette/coverage, material and motion, contrast over the real art, and entry/peak/sustain/exit timing. A brief sentence per effect is enough; use existing task notes rather than creating a separate design document. Give each layer a visible job, and add support only when it improves that job.

For a new pack or a rejected visual direction, finish and inspect one representative effect at player scale before expanding that treatment across the pack. Resolve weak visibility, muddy shape or unsuitable motion there first. This is a self-review checkpoint, not a new user-approval requirement; follow any review boundary the user explicitly requested.

Reusable shapes can support different mechanics when their silhouettes, motion, timing and placement differ meaningfully. Recoloring the same burst is insufficient when the mechanics need distinct feedback. Preserve intentional continuity between connected events, such as a projectile and its arrival or a transition and the ambience it reveals. Use approved references when available; a named preset alone does not establish a visual direction.

## Assets and editable structure

Reuse suitable project assets first. Generate a new texture only when it improves the requested look, using the available image workflow and its instructions. Simple readable cores often work better than detailed sprites at player scale.

- Light textures such as glows, rings, streaks and dots can use white RGB with shape in alpha and color from the layer ramp.
- Painted solids can retain their RGB shading with a neutral ramp that fades alpha. Do not wash out approved artwork to follow a universal white-texture rule.
- Size by visible core and intended display size. A 32–128 px texture is a useful starting point for small marks, not a universal limit. Crop excess transparent padding before import/packing while retaining needed antialiasing, filter bleed and consistent frame pivots.
- Preserve editable source or generation settings when actually used. A texture's alpha shape changes the mark; compare substitutions instead of treating them as brightness adjustments.

On 0.9.50, prefer `import_asset` with `sourcePath` and, when needed, a granted `folderGrantId`. Without a grant, paths resolve on the MCP server under its allowed asset roots. If inline data is necessary, encode and transfer it programmatically; never transcribe base64 by hand or impose an arbitrary 2 KB payload target.

Use one clearly named group and clip per independently triggered effect. Include a GDD number when one exists. Name layers by visual role; avoid redundant UI labels that make follower badges confusing. Check hierarchy stacking and explicit clip membership through the [MCP authoring workflow](../slotvfx-mcp-authoring/SKILL.md).

## Design for the actual game

Start with one strong readable element, then add supporting accents. For an outline treatment, preserve symbol readability; for a requested full-column highlight, provide the intended interior coverage. Do not turn every effect into a frame because an earlier project preferred frames.

Use small moving marks for rhythm and a restrained larger sprite for a continuous body where appropriate. Either can bleach bright art if additive intensity is excessive. Choose blending by material: solid foam or fragments may need normal blending to remain visible over bright art; supporting light can use additive blending. A wash intended to conceal a scene change needs actual coverage, not just brightness. Verify the choice over the real art. Set particle caps deliberately, especially for effects repeated on many cells; include supporting layers and followers in the total.

Even coverage usually depends on spawn geometry. Extend a spawn band beyond the visible area when that keeps falloff outside it; increasing speed can instead create unwanted sideways drift. For static or nearly static shapes, a textured sprite may be cheaper and cleaner than dozens of particles.

Use prewarm selectively. Prefer an immediate burst, start-age spread or another supported initialization when it gives the required first frame cheaply. Prewarm can be appropriate for a populated ambient field or an otherwise missing initial particle; measure its startup cost. Immortal particles may not advance ordinary lifetime ramps, so verify the actual fade mechanism.

Color for contrast over the real art. White-hot cores followed by theme color are one useful impact treatment; themed, white or contrasting steady frames can all work. Compare on a bright symbol, a theme-colored symbol and a dark symbol. If a rim disappears, adjust line width and geometry before blindly increasing brightness.

For specific mechanics, read only the relevant companion skill: [recipes](../slot-vfx-particle-recipes/SKILL.md), [holds](../slot-vfx-hold-loops/SKILL.md), [travel](../slot-vfx-travel-effects/SKILL.md), or [per-cell copies](../slot-vfx-per-cell-effects/SKILL.md).

## Verify the authored result

Inspect natural playback of onset, peak, sustain where present, and exit at player scale on the actual board. For mobile game effects, include a phone-sized view; a zoomed-in editor view is insufficient. Check clear silhouette, intended coverage, readable symbols/amounts, correct layer order, clipping, and the intended distinction from adjacent effects. If any of these fail, revise the composition before expanding the pack or calling the look ready. Use bounded captures or render offsets/overrides for specific placement questions; still frames alone do not establish motion timing or loop continuity.

Estimate lifetime from timing settings, then measure beyond the expected end. Driver-death followers and variance can invalidate a simple sum. Read live counts and inspect frames until a one-shot finishes, or until a hold reaches its expected sustained behavior. Recheck after changing supposedly vestigial fields too.

For shipping performance, test the requested engine and realistic simultaneous copy count. Editor appearance does not verify masks, baked fallbacks or runtime lifetime. Use the [performance skill](../slot-vfx-performance/SKILL.md) for a real performance investigation, not automatically for every small visual edit.

## Save and hand off

Preserve old variants unless replacement/deletion was requested. Only remove task-owned disposable scratch objects after reference checks. A layer absent from the currently open clip may be used by another clip.

If exporting, inspect the current editor's Bake and Export settings. The supplied 0.9.50 guide describes per-layer FPS/Detail, grouping of overlapping baked layers, and fitted frame sizes; confirm these in the actual exported manifest and sheets before claiming size savings. Check `warnings.txt` and any `[Max Size]` reductions. A preview MP4's FPS is separate from a baked runtime sheet's FPS.

For a full pack, update existing build notes and a developer handoff with:

- Effect names, event triggers, group/clip IDs resolved from this project, origin/pivot and layering.
- Meaningful settings and deliberate exceptions, including who stops held effects and how tails end.
- Travel aiming and per-cell instance examples using the project's actual runtime API.
- Verified SlotVFX/runtime versions, relevant measurements, unresolved limitations and removed workarounds.

Treat exported data as generated output: prefer changing the authoring source and re-exporting. If the user explicitly asks for runtime or export fixes, work in the authorized source and record the patch so it is reproducible. Do not tell the owner they cannot edit their files. Draft any bug report locally; sending it or posting backlog items requires explicit authorization.
