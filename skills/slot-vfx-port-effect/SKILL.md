---
name: slot-vfx-port-effect
description: "Port an approved SlotVFX effect between game projects while preserving its motion and identity. Map source assets and geometry, scale positions and motion correctly, then verify on the target art and runtime."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Porting an approved effect

Start from the approved source project and its latest relevant notes. Compare notes with current layer values and previews; neither stale documentation nor an abandoned experiment defines the target. Record rejected treatments only when they explain what must be preserved. Resolve all asset/group IDs from the actual projects.

Create a new target group and clip unless the user requested a direct replacement. Keep the source and unrelated target layers intact. Read only the necessary source data and preserve any sharing restrictions.

## Map geometry while preserving timing

Choose reference dimensions appropriate to the effect: cell pitch, symbol size, reel window or travel distance. Use a uniform scale when maintaining proportions matters. If the target genuinely needs different horizontal and vertical scales, map each component deliberately:

- Positions, emitter extents and path points use their respective x/y scale factors.
- Sprite width and height may need separate scaling; preserve aspect ratio when required by the approved texture.
- Velocity and acceleration vectors scale per axis when time stays the same. With anisotropic scaling, direction angles can change; do not blindly keep angles and scale every speed by the vertical factor.
- Circular radii become elliptical under anisotropic mapping, unless retaining circles is a deliberate design choice.
- Keep lifetimes and choreography initially. Rates, caps and variance are starting values to compare, not invariants when clipping, coverage or runtime constraints change.

Set timing-critical defaults explicitly. The supplied pack observed a 0.4 s lifespan variance default in older builds; read the current default and carry the source's actual value. Compare live counts and motion to the source under equivalent times/seeds, allowing natural randomness rather than imposing an arbitrary percentage as proof of correctness.

## Carry assets and color carefully

A texture swap changes visible core, padding, alpha shape and orientation. Prefer the approved asset where reuse is allowed. Inspect substitutions in isolation on transparent/dark backgrounds and then over the actual game art. For directional streaks, verify face-direction behavior and which size axis is the length.

Choose color for contrast and requested identity. White-hot cores fading to theme color can work; do not impose white on every steady frame or ban a requested theme color. If overlapping glows band, consider the stable-sprite approach in [hold loops](../slot-vfx-hold-loops/SKILL.md).

## Verify and hand off

Preview full-board placement and the effect at normal player size. Check entry, peak, tail, loop/hold behavior, second-cell placement and any runtime-specific features. Use temporary render overrides where supported before committing exploratory changes.

For a substantive port, update existing notes with source/target dimensions, transformed settings, asset substitutions and intentional deviations. Supply the actual trigger/play/stop integration and runtime version when game delivery is part of the task. Do not claim engine compatibility solely from an editor preview.
