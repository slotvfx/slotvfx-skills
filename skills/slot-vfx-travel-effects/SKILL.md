---
name: slot-vfx-travel-effects
description: "Create or revise SlotVFX travel effects such as zaps, pulses and orbs. Coordinate the moving head, riders, trails and impact, then verify instance IDs, coordinate spaces and arrival in the game runtime."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Travel effects

Use one movement driver for a projectile, pulse or moving emitter, and let its intended companions follow it. A normal path is sufficient for a fixed route. Preserve the requested look and existing versions; use multiple drivers only when the effect intentionally has separate or branching heads.

## Choose the travel driver

For particles or emitters travelling along a fixed route, straight or curved, prefer a normal path over many X/Y position keys. The path defines where travel goes; duration, speed and a progress curve define when it gets there.

Use A-to-B controls only when the game or caller must configure the launch and destination points, such as travel between changing board cells. In that case, put the configurable route on the head and make its companions follow the same driver. Reusing an effect does not by itself require configurable endpoints.

Choose what follows the route:

- **Travelling particle/head:** the particle moves along the route; a projectile, pulse or orb can carry riders and leave a trail.
- **Travelling emitter:** the source moves along the route and emits a wake. For particles meant to stay where born, choose world space and the intended follow-release behavior. Moving the source does not require old particles to follow it.

Inspect the installed path and `emitterFollowsPath` controls; assigning `pathId` alone does not prove which behavior is active. Use one travel driver rather than independently keying the same movement as well. Keep keys for emission/opacity and deliberate positional beats; retain velocity/forces for free ballistic motion, real weapon/bone attachments and existing approved trajectories. Do not convert approved effects solely to adopt a path. This choice controls movement, not the effect's visual construction, and does not establish performance or runtime parity.

## Connect the moving parts

| Companion | Starting arrangement |
| --- | --- |
| Traveling glow, orb or attached ribbon | Spawn-sync follower with Ride Driver and the intended lifetime synchronization (the pack turned Sync Lifetime on) |
| Impact, hit star or splash | Follower emitted on the driver's death (Follow On: death), so it fires where the travel actually ended |
| Launch puff or muzzle flash | Follower emitted on birth |
| Trail | TRAIL sub-emitter on the head or an appropriate rider, not a separate layer |

From 0.9.78 a path can also move by itself (Path Motion: the `pathMotion` option of `create_path_from_preset` or the `path.pathMotion` feature), with matching support in game runtime exports; read its schema before relying on it for a route. Avoid redundant paths or targets on followers that should share one route; each is a second source of truth and drifts when the head is re-aimed. Set lifespan variance explicitly for timing-critical heads and verify actual speed, bend and arrival. To key the head's ease exactly, see [motion craft](../slot-vfx-motion-craft/SKILL.md). For multiple heads, document which impact belongs to which driver.

The supplied pack reports one sub-emitter per layer and that a follower could not itself be a driver, so a trail that needed its own followers had to be flattened onto the moving layer; inspect current support before planning a hierarchy. It also reports:

- `subEmitterTrailSpacing` was in literal pixels. Without it, spacing was inferred as 0.5 × the child's largest size, which is why an old workaround set Start Size large and scaled the child down; when replacing that pattern, the spacing is 0.5 × the old Start Size.
- Path mode `stretch` needed Path Progress Speed above 0. At 0 the path only shaped emission and the Target Point never applied.
- On a path bent onto A-to-B, `targetBendSide` had no effect; the arc side was set by negating `targetScaleY` when the travel ran the other way in x.
- Group-level shared points were half-implemented, invisible in the UI and later removed; one A-to-B on the head did the same job with settings an artist can see.

Treat these as version-specific leads. Do not copy legacy size hacks or unsupported shared-point structures without checking the current schema.

## Re-aim the correct live instance

This section applies to effects with configurable endpoints. A fixed path does not require an A-to-B setup or a re-aiming API.

Read the installed runtime's public API, including `setTravelPoints` if present (the pack's runtime had `setTravelPoints(layerId, from, to, bendSide)`). Resolve the head's template ID from the authored group/manifest, then resolve the corresponding **instance** element ID; in the pack's runtime, `getGroupElementIds(instanceId)` listed them, and a copy's layer IDs carried a suffix such as `__manual_runtime__1`. Do not hardcode an ID from another game or invent suffix parsing when the runtime exposes a mapping.

A successful write to a template is not proof a live copy moved: in the pack's runtime a bare template ID wrote the template, returned `true`, and the copy on screen kept its old route. Confirm readback or visible movement on the intended instance.

Determine the point space required by the actual runtime. In the pack's tested implementation, points were relative to the layer's placement (`getEmitter(layerId).container.position`), because export rebased the authored pair that way; subtracting the start point instead put the arrival short. Subtracting its position is valid only when the incoming points are in the same parent space and the relevant transform is translation-only. For scaled, rotated or nested parents, use the supported world-to-local transform or matrix inversion for the required space. Do not subtract A from both points by habit.

Prefer a public bend/scale setter. The pack used a private `head.config.config.targetScaleY` write for one arc workaround; do not use that nested internal path without inspecting the exact runtime version and proving a public route is unavailable. Document any necessary workaround and retest after updates.

Do not move a head container to A as well as setting local travel points unless the current API calls for both; that can double the translation and displace followers. Older integrations moved the container; in the pack's runtime, riders and death followers were corrected against the driver's origin, so writing both points and leaving the container alone kept them attached.

## Verify several routes

Choose the motion check for the actual travel driver:

- **Moving emitter:** `get_timeline` with `motion: { targetIds, timesSeconds }` reports the emitter/source trajectory (`kind: "emitterHead"`), including supported emitter-follow-path motion. Inspect the returned `supported` flag and kind before using its positions, direction or speed.
- **Travelling particles:** that same probe still measures their emitter; it does not track individual simulated particles. Advance the particle simulation and inspect rendered frames or a known particle's positions at known ages to verify its route, speed and arrival. A stationary emitter sample is expected when the particles travel away from it; it does not mean the particles stopped.

Render early flight, mid-flight and impact; check the intended companions stay with the head and the released wake stays behind as designed. Verify the fixed path's shape, traversal speed and endpoint in the native runtime, including a late-started instance away from the template origin. Add transformed-parent tests if the game uses them.

For configurable A-to-B effects, also aim to a second destination and include left/right travel. `move_effect` shifts the head's A-to-B target and handles with it, so moving the whole effect keeps the route. A companion intended to ride the head should share its driver rather than retain an independent path or target.

Measure arrival against the path endpoint, or B for a configurable A-to-B effect, in a common coordinate space. Error within deliberate spawn spread (a few px in the pack's tests) may be correct; a large systematic offset (tens or hundreds of px) suggests an origin, instance-ID or follower-space problem. Check the full trail and impact remain attached, the flight duration is correct, and stopping/reusing the instance leaves no old particles behind.
