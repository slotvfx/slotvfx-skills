---
name: slot-vfx-effect-pack
description: "Build a complete slot VFX pack in SlotVFX from a game brief, GDD and art: map the board, author effect groups and clips, verify in context, and prepare a practical game integration handoff."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Building a slot VFX effect pack

Use this workflow for a requested collection of gameplay effects. For an isolated effect, use only the relevant steps. For logo choreography, use the logo-reveal skill if available. Current user instructions override example designs and historical preferences. Preserve existing work; new alternatives get new named groups and clips unless direct edits were requested.

## Establish the brief and layout

Read the brief, source art, existing project and any build notes available. Notes explain deliberate oddities, but compare them with the current project. An open-ended `duration: -1` layer, a very long lifespan and a clip shorter than its content may intentionally sustain through a variable win count-up; do not convert it to a one-shot without understanding its trigger and stop contract. Such a hold measures like a bug (live counts flat at hundreds long past the clip end, a dim holding the board dark for half a minute); one Max Win hold was nearly reverted three versions after it was deliberately introduced and documented.

Map cell centres, pitch, reel window, logo, badges and event anchors, and record them as a layout table in the build notes. Check placement over the real shipping background with `render_layout` and `background: "layout"`; a grid read from a mock-up was once 24 px off the shipping art, and every board effect had to be moved. Use transparent renders separately for isolated bounds; they hide that kind of offset. Where supported, bind to real layout anchors and grid cells rather than hardcoding every placement, so one recipe serves every cell (earlier builds used `layoutAnchorId` plus `layoutAnchorGridCell`).

Agree only missing decisions that materially affect the result. Infer reasonable styling and timing from the existing project; do not require an approval at every stage.

## Establish a visual direction

Before authoring, connect the effect's gameplay purpose to its silhouette/coverage, material and motion, contrast over the real art, and entry/peak/sustain/exit timing. A brief sentence per effect is enough; use existing task notes rather than creating a separate design document. Give each layer a visible job, and add support only when it improves that job.

For a new pack or a rejected visual direction, finish and inspect one representative effect at player scale before expanding that treatment across the pack. Resolve weak visibility, muddy shape or unsuitable motion there first. This is a self-review checkpoint, not a new user-approval requirement; follow any review boundary the user explicitly requested.

Reusable shapes can support different mechanics when their silhouettes, motion, timing and placement differ meaningfully. Recoloring the same burst is insufficient when the mechanics need distinct feedback. Preserve intentional continuity between connected events, such as a projectile and its arrival or a transition and the ambience it reveals. Use approved references when available; a named preset alone does not establish a visual direction.

## Assets and editable structure

Reuse suitable project assets first. Generate a new texture only when it improves the requested look, using the available image workflow and its instructions. Simple readable cores often work better than detailed sprites at player scale.

- Light textures such as glows, rings, streaks and dots can use white RGB with shape in alpha and color from the layer ramp, so one texture serves many effects and palettes.
- Painted solids can retain their RGB shading with a neutral ramp that fades alpha. Do not wash out approved artwork to follow a universal white-texture rule.
- Size by visible core and intended display size. A 32–128 px texture is a useful starting point for small marks, not a universal limit. Crop excess transparent padding before import/packing while retaining needed antialiasing, filter bleed and consistent frame pivots.
- Preserve editable source or generation settings when actually used; for a procedural texture, keep its generator script with the project and name it in the build notes. A texture's alpha shape changes the mark: a radial that fills its square draws a mark several times heavier than a thin line inside a mostly transparent square of the same size. Compare substitutions instead of treating them as brightness adjustments; to make an approved layer read more strongly, change its count, rate or ramp first, because a texture swap is a redesign.

On 0.9.50 and 0.9.59, prefer `import_asset` with `sourcePath` and, when needed, a `folderGrantId` from `choose_asset_folder` for a user-approved folder. Without a grant, paths resolve on the MCP server under its allowed asset roots (`SLOTFX_MCP_ASSET_ROOTS`). The 0.9.59 schema also accepts a data URL, a remote URL or inline data. If inline data is necessary, encode and transfer it programmatically (a programmatically encoded PNG data URL imported cleanly on 0.9.59); never transcribe base64 by hand or impose an arbitrary 2 KB payload target.

Use one clearly named group and clip per independently triggered effect. Include a GDD number when one exists (`FK 07 Village Snowfall`, `RR 20 Win Cell Glow`); it keeps the GDD, the project and the handoff in step. Name layers by visual role; avoid role words and other redundant UI labels that make follower badges confusing. The Layers panel echoes a driver's name onto each follower badge, so a layer named "Surge Head (driver)" made a thirteen-layer group look like thirteen drivers. Check hierarchy stacking and explicit clip membership through the [MCP authoring workflow](../slotvfx-mcp-authoring/SKILL.md). On earlier builds the first group in the hierarchy drew on top; celebrations usually sit above the board and ambience below it.

One-shot clips keep their loop flag off; an ambient loop keeps it on. Do not set or pass `loop: true` on a hold by habit. On 0.9.42 and later (source-checked on 0.9.59) a non-looping clip that reaches its end is held: keyed images, sprite sheets and Spine parts freeze on their last frame, particle layers keep simulating, and a `duration: -1` layer holds until the game stops it. `loop: true` replays keyed animation every lap, so never use it on a hold whose clip has a keyed entrance; for a particle-only hold without bursts it changes nothing visible and keeps pre-0.9.42 builds holding. The [holds](../slot-vfx-hold-loops/SKILL.md) skill covers the rest.

## Design for the actual game

Start with one strong readable element, then add supporting accents. For an outline treatment, preserve symbol readability; for a requested full-column highlight, provide the intended interior coverage. Do not turn every effect into a frame because an earlier project preferred frames.

Use small moving marks for rhythm and a restrained larger sprite for a continuous body where appropriate. Either can bleach bright art if additive intensity is excessive. Choose blending by material: solid foam or fragments may need normal blending to remain visible over bright art; supporting light can use additive blending. A wash intended to conceal a scene change needs actual coverage, not just brightness. Verify the choice over the real art. Set particle caps deliberately, especially for effects repeated on many cells; include supporting layers and followers in the total.

Even coverage usually depends on spawn geometry. Uniform spawn of sizeable sprites over a finite band is centre-weighted, because the middle collects from both ends; extend the spawn band beyond the visible area when that keeps falloff outside it. Increasing speed can instead turn `angleVariance` into unwanted sideways drift and push particles out of the shape they should fill. For static or nearly static shapes, a textured sprite may be cheaper and cleaner than dozens of particles. A border highlight that travels round a cell at over a second a lap is always caught mid-lap when the display ends, which reads as clipping; a continuous edge emitter holds the border but spends dozens of sprites per cell to draw something that does not move. One sprite on a baked frame texture solves both.

Use prewarm selectively; it costs startup time on every play. Prefer an immediate burst at t=0, a burst start-age spread, immortal particles with toroidal wrap for an ambient field, or another supported initialization when it gives the required first frame cheaply. Prewarm can be appropriate for a populated ambient field or an otherwise missing initial particle; measure its startup cost. If an immortal t=0 burst in a looping clip goes missing on frame 0 or at a seam and the fault reproduces, `prewarmDuration` 0.2 s fixed it on an earlier build. Immortal particles may not advance ordinary lifetime ramps (on earlier builds they read a single ramp point, so give them a flat ramp); verify the actual fade mechanism.

Color for contrast over the real art; an additive mark adds nothing where the art is already bright in the same hue. White-hot cores followed by theme color are one useful impact treatment: the core separates from any symbol and the theme color arrives on the way out. Themed, white or contrasting steady frames can all work, but a static marker has no fade in which to separate from the art. A frame painted in the game's own key color vanished on WILD and bonus symbols of that color and read as a flat colored box, while white or a contrasting color read. Compare on a bright symbol, a symbol in the game's key color and a dark symbol; a mid-tone symbol proves nothing. If a rim disappears, adjust line width and geometry before blindly increasing brightness, in whichever direction makes it a line: on calm art a too-thin rim vanishes into bright symbols and needs widening; on busy art a too-wide rim reads as haze and needs narrowing.

Write motion as exact keys rather than dragged handles. Give each element a verb and a beat first (slams, counts up, breathes), then key its eases, springs and staggers with the [motion craft](../slot-vfx-motion-craft/SKILL.md) skill. Free-tangent keys evaluate as a CSS cubic-bezier, so a named ease is two keys and a spring is about 4–10. Per-cell staggers go into the handoff as a delay table, because the game spawns those copies.

For specific mechanics, read only the relevant companion skill: [recipes](../slot-vfx-particle-recipes/SKILL.md), [holds](../slot-vfx-hold-loops/SKILL.md), [travel](../slot-vfx-travel-effects/SKILL.md), [per-cell copies](../slot-vfx-per-cell-effects/SKILL.md), or [motion craft](../slot-vfx-motion-craft/SKILL.md).

## Verify the authored result

Inspect natural playback of onset, peak, sustain where present, and exit at player scale on the actual board. For mobile game effects, include a phone-sized view; a zoomed-in editor view is insufficient. Check clear silhouette, intended coverage, readable symbols/amounts, correct layer order, clipping, and the intended distinction from adjacent effects. If any of these fail, revise the composition before expanding the pack or calling the look ready. Use bounded captures or render offsets/overrides for specific placement questions; still frames alone do not establish motion timing or loop continuity. `render_layout` `times` gives a cheap strip of how an effect evolves (for example at 0.2 s, mid-life and near the end). `offset` with an explicit `entities` list moves a per-cell effect onto the cell it will play on for one render, and `overrides` tries a value, both without editing the project. `includeImage: false` with `contentBounds` and `liveParticlesByEmitter` answers whether it fired and where.

Estimate lifetime from timing settings, then measure beyond the expected end. Driver-death followers and variance can invalidate a simple sum: a death follower's clock starts when its driver dies, so `startTime + duration + lifeSpan + variance` can over-count by most of a second. One clip was lengthened to 1.75 s on that arithmetic before a render showed the effect was over at 0.98 s. Read live counts (`totalLiveParticles` down to zero) and inspect frames until a one-shot finishes, or until a hold reaches its expected sustained behavior; set the clip length from the measured end plus a margin for lifespan variance. Recheck after changing supposedly vestigial fields too.

For shipping performance, test the requested engine and realistic simultaneous copy count. Editor appearance does not verify masks, baked fallbacks or runtime lifetime. Use the [performance skill](../slot-vfx-performance/SKILL.md) for a real performance investigation, not automatically for every small visual edit.

## Save and hand off

Preserve old variants unless replacement/deletion was requested. Only remove task-owned disposable scratch objects after reference checks: a path or asset that looks orphaned may be the one a driver's `pathId` points at, which the Layers panel does not show, so dry-run the delete. A layer absent from the currently open clip may be used by another clip; `hiddenBy: ["timeline"]` only means it is not in the open clip, while `hiddenBy: ["self"]` means the layer itself is switched off.

If exporting, inspect the current editor's Bake and Export settings. The supplied 0.9.50 guide describes per-layer FPS/Detail, grouping of overlapping baked layers, and fitted frame sizes; confirm these in the actual exported manifest and sheets before claiming size savings. As described for 0.9.50:

- Export Bundle reads FPS and Detail from each baked layer's own Bake panel. They are saved with the layer and set in the editor; the MCP had no feature for them then, so check `find_features` on the current build.
- Overlapping layers in the same clips share one sheet at the highest FPS and Detail among them, and a sheet runs for the longest clip its layers play in.
- A loop tied to its clip's length (a baked timeline loop or an Image FX) gets its own sheet in each clip when those clips differ in length; the runtime switches sheets with the clip.
- Frames follow each effect's shape up to the dialog's Frame size.

Check `warnings.txt`: a `[Max Size]` line means a sheet was squeezed below its Detail to fit the texture limit. A preview MP4's FPS is separate from a baked runtime sheet's FPS.

For a full pack, update existing build notes and a developer handoff with:

- Effect names, event triggers, group/clip IDs resolved from this project, origin/pivot, layering and container order.
- Meaningful settings and deliberate exceptions, including who stops held effects and how tails end. Give each workaround and deliberate oddity its reason, so nobody removes it because it looks wrong or keeps it after the underlying bug is fixed.
- Travel aiming and per-cell instance examples using the project's actual runtime API.
- Per-cell stagger delay tables, and the ease and duration a game-side count-up must share with its banner.
- Verified SlotVFX/runtime versions, relevant measurements, unresolved limitations and removed workarounds.
- A first-build checklist. When an engine build changes behavior, a short post-export check: which effect to play, what fixed and broken look like, and which cases prove nothing (a symmetric sprite, or a fan whose art already points the right way, says nothing about a facing fix).

Keep the build notes current in the same session as the work, with a changes section per version and open items. Re-read the handoff whenever the build changes and delete what the new build has made unnecessary; a handoff that still lists solved problems is worse than none (five of seven open items in one were already done).

Treat exported data as generated output: prefer changing the authoring source and re-exporting. If the user explicitly asks for runtime or export fixes, work in the authorized source and record the patch so it is reproducible. Do not tell the owner they cannot edit their files. Do explain the costs in the handoff: a hand edit to exported data is overwritten by the next export and until then makes editor and game disagree, which looks like an engine bug; a locally patched runtime is reverted by SlotVFX updates and makes bug reports against it unreliable, because line numbers no longer match the stock runtime. Recommend fixing a wrong effect in SlotVFX and re-exporting, using the runtime API for per-play differences, and reporting engine bugs. Draft any bug report locally; sending it or posting backlog items requires explicit authorization.
