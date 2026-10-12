---
name: gdd-to-vfx
description: Turn a game brief or GDD into a scoped SlotVFX effect pack and integration handoff with reusable effects, event contracts, anchors and target checks.
---

Read the actual GDD, game art and current project. Extract a small effect inventory: trigger, visual role, anchor, lifetime (one-shot or held), stop behavior, layering and intended engine. Start with one representative effect and verify it at gameplay size. This workflow produces VFX and an integration handoff; it does not promise a complete game from a document.

Use [workflow routes and specialist checks](references/workflows.md) for the current tool surface. Reuse the bundled effect-pack, hold-loop, per-cell, travel or porting skill for the relevant part of the brief when available. Create named groups/clips with explicit membership. For reused per-cell or travel effects, inspect game-object origins, instance APIs, mount coordinates and driver/follower lifetime in the actual runtime. A loop or duration:-1 may intentionally sustain until a game event stops it. Preserve that contract.

Reuse approved assets. If new artwork improves the result, use an available image-generation capability under its instructions, or create supported procedural textures with `slotfx_create_texture`. Image generation is an optional external capability, not bundled into SlotVFX. Stop only that step if it needs a key or new grant; continue with existing or procedural art. Keep source assets and relevant usage rights/provenance. Import through scoped asset roots or the native folder grant.

Prepare the representative editable effect directly in SlotVFX and use the guide's active-clip/focus/playback handoff so the user can inspect it there. Do not make a chat render or recording the default deliverable. Deliver requested exports plus a concrete integration note: effect/group/clip IDs, triggers, origin/pivot, anchor coordinates, who starts/stops instances, and target/version tested. Current `export_runtime` writes data and diagnostics only; a complete engine bundle still uses Game Runtime Export in the editor. Inspect actual files and test realistic simultaneous instances before claiming integration or performance.

Edit a user's game repository only when that repository and change are in scope. Use an isolated branch or reversible patch, preserve existing integration, and derive API calls from its actual runtime. Do not install dependencies, generate credentials, publish, or broaden filesystem grants as an implied consequence of a GDD.
