---
name: slot-vfx-per-cell-effects
description: "Author SlotVFX effects used on many cells as spawnable templates, including win glows and lock rings, and verify instance placement, phase, lifetime and performance at realistic counts."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Effects repeated per cell

Author one reusable effect at a reference cell and record its centre, pivot and intended dimensions. Preserve existing work; a requested alternative gets its own named group/clip. Use the project's actual spawnable group type and runtime API.

## Distinguish templates from displayed copies

For spawnable/GameObject template groups, the rendered objects are runtime instances; ordinary scene groups may render directly. Resolve the instance's element IDs through the supported runtime API, such as `getGroupElementIds(instanceId)`, rather than writing to a bare template ID and assuming every live copy changed.

The supplied pack observed suffixed instance IDs. Discover them live and record the relationship to the template; never reuse an example project's ID. Use `render_layout`'s supported `previewInstance` mode to inspect a template at its intended mount point.

## Verify placement and phase

One copy is a useful visual check, but it does not establish behavior at the game's maximum simultaneous count. For integration checks, spawn representative copies at different offsets and different times. Compare each with its own expected local phase and position.

Look for effects reading scene time instead of instance time, followers using the template's position, and baked animation restarting when unrelated ambience loops. Check birth, steady state, stop/tail and reuse of pooled copies where applicable.

For a performance task, measure realistic counts in the actual runtime: update time, draw calls, upload cost, particle counts and sheet memory as relevant. Do not build a large headless benchmark for every small visual revision; use [performance](../slot-vfx-performance/SKILL.md) when needed.

## Keep the repeated cost deliberate

- Start with a clear shape and a few accents; choose coverage from the current request rather than assuming every highlight must be a thin frame.
- Cap particles per layer and account for the number of copies.
- Check ribbon strands, segments and current batching support before deciding they are too expensive.
- Consider a textured sprite for a static frame or a baked animated beam for suitable motion, but measure current native/baked cost and texture memory. Historical one-third-CPU and single-draw-call examples are not universal.
- Inspect exported frame dimensions, pivot and `originalWidth`/height where present. A large transparent quad still costs overdraw even if the visible mark is small. The pack's 0.9.50 fitted-frame claim needs confirmation in the exported artifact.

Offer a second version when there is a meaningful visual or performance tradeoff. Build it when within the authorized alternatives or optimization scope; do not automatically double the work or replace the approved effect. Save the selected result and give the game developer the correct origin, instance API, stop behavior and measured limits.
