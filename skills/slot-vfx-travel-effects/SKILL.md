---
name: slot-vfx-travel-effects
description: "Create re-aimable SlotVFX travel effects such as zaps, pulses and orbs. Coordinate the moving head, riders, trails and impact, then verify instance IDs, coordinate spaces and arrival in the game runtime."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Travel effects

For a single projectile or pulse, put A-to-B motion on one head and let companions follow it. This is a useful synchronization pattern, not a restriction against intentionally separate or branching heads. Preserve the requested look and existing versions.

## Connect the moving parts

| Companion | Starting arrangement |
| --- | --- |
| Traveling glow, orb or attached ribbon | Spawn-sync follower with Ride Driver and the intended lifetime synchronization |
| Impact, hit star or splash | Follower emitted on the driver's death |
| Launch puff or muzzle flash | Follower emitted on birth |
| Trail | TRAIL sub-emitter on the head or an appropriate rider |

Avoid redundant paths or targets on followers that should share one route. Set lifespan variance explicitly for timing-critical heads and verify actual speed, bend and arrival. For multiple heads, document which impact belongs to which driver.

The supplied pack reports one sub-emitter per layer and limits on followers also acting as drivers; inspect current support before planning a hierarchy. It also reports literal-pixel `subEmitterTrailSpacing`, a positive Path Progress Speed requirement for path stretch travel, and path arc cases where `targetBendSide` was ineffective. Treat these as version-specific leads. Do not copy legacy size hacks or unsupported shared-point structures without checking the current schema.

## Re-aim the correct live instance

Read the installed runtime's public API, including `setTravelPoints` if present. Resolve the head's template ID from the authored group/manifest, then resolve the corresponding **instance** element ID. Do not hardcode an ID from another game or invent suffix parsing when the runtime exposes a mapping.

A successful write to a template is not proof a live copy moved. Confirm readback or visible movement on the intended instance.

Determine the point space required by the actual runtime. In the pack's tested implementation, points were relative to the layer's placement. Subtracting its position is valid only when the incoming points are in the same parent space and the relevant transform is translation-only. For scaled, rotated or nested parents, use the supported world-to-local transform or matrix inversion for the required space. Do not subtract A from both points by habit.

Prefer a public bend/scale setter. The pack used a private `head.config.config.targetScaleY` write for one arc workaround; do not use that nested internal path without inspecting the exact runtime version and proving a public route is unavailable. Document any necessary workaround and retest after updates.

Do not move a head container to A as well as setting local travel points unless the current API calls for both; that can double the translation and displace followers.

## Verify several routes

Render early flight, mid-flight and impact, then aim to a second destination. In the runtime, include left/right travel and a late-started instance away from the template origin. Add transformed-parent tests if the game uses them.

Measure the arrival against B in a common coordinate space. Error within deliberate spawn spread may be correct; a large systematic offset suggests an origin, instance-ID or follower-space problem. Check the full trail and impact remain attached, the flight duration is correct, and stopping/reusing the instance leaves no old particles behind.
