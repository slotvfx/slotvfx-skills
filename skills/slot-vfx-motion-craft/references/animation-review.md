# Animation review and delivery budgets

Use this for game animation generation or delivery, large key edits, Spine animation and Bend / Warp. A focused visual inspection does not authorize exporting, simplifying or changing approved motion.

## Review the intended delivery

Read `slotfx://authoring-guide/game-animation` and `slotfx://authoring-guide/animation-review`, then call the read-only tool with the actual clip ID, runtime and simultaneous copy count:

```json
{"timelineId":"win-clip-id","runtimeTarget":"pixi","profile":"mobile","instances":15}
```

Pass that object to `slotfx_review_animation`. The editor exposes the same check in Timeline > Review animation. Use `scope: "project"` to include all named clips. Mobile/desktop profiles are starting budgets, not device guarantees; inspect the returned settings and override them for the game. If this tool is absent, read `get_timeline.gameAnimation`, use available runtime/performance diagnostics and state the missing check; do not claim a completed review.

- Read artist keys separately from validated derived media sampling. Dense-key warnings are advice, not proof that the motion is wrong. Sampled imports, solved IK/retargeting and necessary deformation may need dense data. Video recording FPS does not require one authored key per output frame.
- Prefer a few intentional extremes/breakdowns and curves for ordinary movement. Named eases can use two keys; fitted springs use an explicit approximation tolerance. Do not promise that the fewest keys is always the best result.
- Read `gameDenseArtistKeys` and other `gameAnimation` warnings. Exact-linear candidates are only candidates: preserve locked marker poses, event/contact times, holds, intentional steps, rotation turns, loop values and seam velocities. The review does not simplify keys; change artist motion only within scope and after an error comparison.
- Generated graph curves with exactly equal normalized shapes share a runtime curve at export. Do not replace them with hundreds of sampled keys to avoid lookup tables. Named artist curves retain their identities, including IDs starting `graph-`. A prefix is not permission to delete a curve; generated export IDs must avoid existing identities and collisions.

## Interpret size and cost

Review reports compact UTF-8 tracks plus referenced runtime curves and measured gzip when available. These are animation-data costs, not the full download bundle. Artwork, native Spine JSON and other resources need their own budgets. Compare the actual exported artifact before promising a file size.

Base texture memory is width × height × 4 per unique RGBA page, plus mipmaps and runtime buffers. A 2048² page is 16 MiB before those extras even when its PNG compresses well. Shared pages and skeleton data count once; simulation, vertices and draw calls can grow with copies. Unknown dimensions remain unknown: obtain real source/atlas sizes instead of using scene display width as texture resolution. Check performance on the target runtime/device before claiming FPS.

For Spine, also run `slotfx_check_spine_motion` for motion and `slotfx_check_spine_export` for delivery. Spine Performance now reports key count, compact animation/skeleton JSON, deform-key JSON and stored offsets, unique base atlas memory and a configurable page-side budget. Existing draw-call, blend, mesh, weight, bone, clipping and physics thresholds remain configurable by team, user and call. An advisory threshold is not a universal Spine format limit.

Deform data can contain x/y offsets per affected vertex or bone influence. The writer keeps the first-to-last nonzero offset run; it does not always store the whole mesh. Prefer bone/constraint curves when they reproduce the intended shape, but retain necessary deforms and check actual bytes. Internal IK/retarget helpers already reduce some solved samples; the separate Optimize animation workflow handles eligible linear artist tracks; Animation review itself remains read-only.

## Bend / Warp and Spine shape changes

Choose the representation for the actual consumer. Image Bend / Warp is a live lattice in supported web-runtime combinations; native Spine deformation is a separate skeleton feature. Inspect the current feature schemas and runtime warnings, then use the fewest controls/subdivisions that preserve the silhouette, with sparse pose keys and curves where they fit.

Live image deformation eligibility depends on the source and runtime. Static centred images can use it; local masks, non-centred pivots, Image FX, animated media or path placement can require capture. Do not assume that every warped image is live, or bake every bend by default. Keep editable source layers and verify the delivered live or baked version at game size, including its start, peak and seam. For a bake, check frame count/FPS, trim/pivots, atlas page dimensions and memory, and reuse one packed animated image instead of one layer per frame.

Whole Character FX is disabled in the 0.9.82 app profile. Do not promise it in a native Spine bundle: use supported attachment FX or an explicitly requested rendered capture. Inspect the connected build before relying on a newer capability.

## Optimize animation: preview, then apply

Use Timeline > Optimize animation, or `slotfx_preview_animation_optimization` followed by `slotfx_apply_animation_optimization`. Both SlotVFX clips and native Spine animations use the same bounded reduction/fitting core. Read the live tool schema; older builds may only offer Animation review.

```json
{"target":"slotvfx","mode":"fitCurves","tolerances":{"position":0.25,"rotation":0.1,"scale":0.001,"opacity":0.001},"protectedTimes":[0.4,0.8]}
```

For Spine use `target: "spine"`, `layer` (ID) and `animation`. Modes are `reduceKeys` and `fitCurves`. Preview changes no project data. Inspect `canApply`, keys/bytes before and after, each track's error/tolerance, skipped reasons and protected times. Apply with exactly the returned `proposalId` within the authorized scope. Only an acknowledged editor publication creates the one undo step; Undo restores keys, skeleton assets and pose-plan bindings. A refused publication with unchanged source keeps the preview for retry and creates no Undo entry. A preview expires after 15 minutes and rejects changed source, animation or locks. Discard/re-preview after any relevant edit. Do not rebuild keys manually to bypass a refusal.

Close or Escape cancels the dialog's read-only preparation, including asset checks before Apply, without changing keys or creating Undo history. Late asset responses cannot publish the abandoned edit. Once editor publication starts, the dialog waits for its acknowledgement. URL asset reads have a timeout; retry a failed read after the source is available.

- Reduce keys retains endpoints and their neighbours, extrema and hold boundaries. It never deletes an entire static timeline, because setup/mixing and duration semantics matter.
- Fit curves fits value against time, with fixed endpoint times/values. Continuous error against the original piecewise linear channels is checked at source breakpoints and interior extrema of the difference. SlotVFX also checks its exported 256-entry LUT playback. Spine reads the result through the rig version's native runtime and refines or preserves the track when its curve-table/Float32 error exceeds tolerance.
- Tolerances are per numeric channel: position in scene/native skeleton units, rotation/shear in degrees, scale/opacity as ratios. They are not a bound on final skin/world positions after constraints. Review natural playback, contacts and silhouettes after Apply; Undo if the result is unsuitable.
- Retain contact/beat times using `protectedTimes`. Automatic cue/event/discrete-key times and locked marker neighbourhoods cannot be disabled. Approved full Spine poses must also pass the existing project guard before Apply is enabled. A changed lock/source requires a fresh preview.
- Current SlotVFX scope: linear numeric x/y/z, width/height, rotation/angle, scale/scaleX/scaleY and opacity/alpha tracks in one clip. Derived media keys, authored curves, step/discrete tracks, unknown key metadata and locked layers are preserved. Lock checks resolve canonical target identity, including legacy raw IDs and force-field/morph-zone targets; missing or ambiguous targets are retained. Locks and parent bindings are checked again through the preview source signature before Apply. Other continuous FX/warp/deform properties are not yet eligible; inspect skipped reasons.
- Spine JSON versions 3.7–3.8 and 4.0–4.3: linear bone rotate/translate/scale/shear channels. Legacy vector Fit curves is preserved because 3.x shares one curve across channels. Deform, attachment, event, draw-order and constraint data are preserved. Continuous slot color/alpha keys stay unchanged without pinning all bone samples; attachment/sequence times and both sides of stepped slot transitions remain protected. This is not binary `.skel` optimization.
- From app 0.9.84, physics/slider rigs can optimize independent bone tracks. Inputs and outputs of those constraints retain their original keys, including dependencies through parents, IK/transform/path constraints, weighted path attachments and slider-reference animations across skins. A visually separate bone is not necessarily independent: use the preview's per-track skipped reasons. Unresolved dependency data can preserve all bone tracks; do not remove constraints, change skin or hand-edit source JSON to force eligibility. Skipped tracks are expected when safe tracks still save bytes.
- Locked marker poses remain protected on these rigs. Inspect `canApply`, protected times and any `Apply blocked` note; physics/slider presence does not relax the approved-pose guard. Review the rendered skin, contacts and silhouettes after Apply and use Undo if needed. Optimization of a shared skeleton JSON affects every layer using that asset; inspect the shared-layer note and review those uses.
- SlotVFX byte comparison includes exported tracks and referenced curves/LUTs; Spine compares compact skeleton JSON. Apply is disabled if the proposal does not save payload bytes, even if it removes keys. These are not gzip/full-bundle sizes or device FPS. Named ease/spring authoring can already be sparse; do not optimize it without a measured reason.

Graph previews are bounded samples of numeric curves, not rendered skin comparisons. Error checks cover every optimized track. Run the motion/delivery checks above and inspect the final target-runtime animation before accepting quality or FPS claims.
