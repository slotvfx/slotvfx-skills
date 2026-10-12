---
name: slot-vfx-spin-showcase
description: "Build SlotVFX reel-spin, anticipation and multi-line win showcases using the actual game outcome, strip art, image or Spine symbols, timed highlights and optional state-machine flows."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Spin, anticipation and win showcases

Use the supplied game outcome or an explicitly authorized fictional presentation. Do not invent wins or change symbol results in an actual game replay. Infer choices already established in the conversation; clarify only missing decisions that materially affect the sequence.

Inspect reel-strip assets, layout anchors, existing clips, symbol animations and current runtime constraints. Preserve existing groups/layers unless their direct revision was requested. New showcase variants get new named groups and clips with explicit membership.

## Build the motion and cell states

Measure the strip's repeating **content period**, including intended symbol spacing, rather than assuming image height is the wrap interval. Fit every visible row at landing. For later spins, preserve the previous end phase unless an intentional cut resets the scene.

Author lift, acceleration, cruise, staggered stops, overshoot and settle with timing that matches the current game. Derive key sampling from motion and output needs; batch exact-time keys under the current schema limits. A guard key before step wraps was an older-build workaround, not a universal requirement.

Model each cell's state over time: ordinary strip, bright image substitute or animated symbol. Generate visibility, transforms and highlight keys from that model so shared cells remain consistent across payline changes. Static images for spin/idle and Spines for wins can save work, but an established animated idle is legitimate. Hide/stop inactive content rather than merely parking it off-screen.

Image FX keys may live in the asset/layer stack and run in every clip containing that layer. Inspect them when blur appears in idle/win. A separate still strip with no blur stack may be useful; preserve the moving version's requested behavior.

## Anticipation and wins

Make the teased reel readable at normal scale: a clear edge or interior highlight, restrained supporting particles and a distinct landing beat. Choose coverage and intensity from the current request; do not automatically add heavy shaders, detailed sprites or a dim across every reel.

Draw the correct winning route and light symbols at the intended hit times. On a multi-line change, fade the previous line and stop its exclusive symbol animations while keeping shared winning cells consistent. Inspect both sides of every change; stale visible winners are easy to miss in a midpoint still.

For a detailed recipe with historical timings, masks, strip fitting and a cell-state generator approach, read the [Fairy Spins worked example](references/fairy-spins-example.md). Its numbers and preferences are examples, not project defaults.

## Clips, states and verification

Use separate idle, spin and win clips when appropriate. Define actual trigger names from the existing game integration. Inspect the base timeline that may play under state clips and keep it neutral when needed. Use current transition editing tools rather than duplicating obsolete edges.

Follow the [MCP authoring workflow](../slotvfx-mcp-authoring/SKILL.md) for bounded key replacement, readback, locks and membership. Save substantial completed stages and preserve recovery snapshots.

Preview lift, mid-spin for gaps, each landing, anticipation, strongest impact and every payline handover. Check matching start/end brightness at loop seams and the next spin. A mock or calculated state table can help when the app is unavailable, but does not verify SlotVFX behavior.

Only record when requested. Use the [video workflow](../slotvfx-showcase-video/SKILL.md) to test a requested state-machine scenario and named neutral base timeline. Runtime delivery additionally requires the relevant exported-engine checks; an editor preview alone is insufficient.
