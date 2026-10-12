# SlotVFX agent skills

SlotVFX is a 2D game effects editor for particles, shaders, effects, timelines and state machines.

Nineteen reusable skills for creating, revising, reviewing and delivering effects in SlotVFX Desktop. Each skill is a folder with `SKILL.md`; this repository snapshot includes its references, agent metadata and optional helper scripts.

**Skills are guidance, not a connection.** This distribution contains no SlotVFX application, MCP server, plugin manifest, account issuer, gateway, credentials or game projects. To run the tools, use a compatible SlotVFX Desktop build and connect your AI client to the app's existing local MCP adapter. Tool access, native asset grants, account licensing and your client's normal approval controls remain separate.

## Connect the existing local MCP

1. Install and open SlotVFX Desktop. In **Help → AI / MCP Bridge**, enable the local bridge and use its displayed MCP package or manual configuration for your chosen local MCP client. Keep its token and discovery path private; do not paste them into GitHub or a chat.
2. Connect the client to the local adapter supplied with that Desktop build. The exact client setup depends on the client and app version; these skills do not configure it for you.
3. Ask the client to call `slotfx_get_bridge_status` and then `slotfx_get_app_state` without edits. Confirm a compatible bridge and the intended project before authoring.

For Codex, install **all 19** `skills/<name>` folders into your Codex skills directory (typically `~/.codex/skills/<name>`) using its GitHub skill installer or a careful copy that does not overwrite existing folders. Install them together: some skills link to sibling skills. Restart or start a new client session so it discovers them. Other skill-capable clients may use a different installation location and may not support the same behavior; follow that client's documentation. The optional video helpers need their stated local dependencies only when used.

## Skills

| Skill | Purpose |
| --- | --- |
| [create-vfx](skills/create-vfx/SKILL.md) | Create, inspect or revise editable particles, artwork, logo reveals and game effects directly in SlotVFX Desktop. Show the result in the editor using its existing clip, focus and playback tools. |
| [deliver-vfx](skills/deliver-vfx/SKILL.md) | Export or record approved SlotVFX effects as runtime assets, editable projects or MP4/WebM, and verify the requested delivery. Use when the user asks for a SlotVFX export or recording. |
| [gdd-to-vfx](skills/gdd-to-vfx/SKILL.md) | Turn a game brief or GDD into a scoped SlotVFX effect pack and integration handoff with reusable effects, event contracts, anchors and target checks. |
| [motion-sequence](skills/motion-sequence/SKILL.md) | Author SlotVFX trailers, motion graphics and multi-stage sequences using clips, Scene Animator states, recorder scenarios, shaders, artwork and Spine animation. |
| [slot-vfx-effect-pack](skills/slot-vfx-effect-pack/SKILL.md) | Build a complete slot VFX pack in SlotVFX from a game brief, GDD and art: map the board, author effect groups and clips, verify in context, and prepare a practical game integration handoff. |
| [slot-vfx-hold-loops](skills/slot-vfx-hold-loops/SKILL.md) | Create or repair SlotVFX effects that sustain for variable durations, such as anticipation, win count-ups and cell highlights. Separate entry from sustain, verify loop seams and explicit stopping in the target runtime. |
| [slot-vfx-particle-recipes](skills/slot-vfx-particle-recipes/SKILL.md) | Particle looks that worked in SlotVFX (impacts, rain ripples, portals, flames, ambience, coin fountains, props with glows) and the parameter traps that silently break them. |
| [slot-vfx-per-cell-effects](skills/slot-vfx-per-cell-effects/SKILL.md) | Author SlotVFX effects used on many cells as spawnable templates, including win glows and lock rings, and verify instance placement, phase, lifetime and performance at realistic counts. |
| [slot-vfx-performance](skills/slot-vfx-performance/SKILL.md) | Investigate SlotVFX frame-rate or export-cost problems with controlled measurements in the actual target runtime. Compare realistic copy counts, simulation, draw calls, uploads, overdraw and baked alternatives. |
| [slot-vfx-port-effect](skills/slot-vfx-port-effect/SKILL.md) | Port an approved SlotVFX effect between game projects while preserving its motion and identity. Map source assets and geometry, scale positions and motion correctly, then verify on the target art and runtime. |
| [slot-vfx-slashes](skills/slot-vfx-slashes/SKILL.md) | Create or repair sword slashes, crescent cuts, attack swipes and directional energy strokes in SlotVFX, including textured breakup, dissolving flame tongues, streaks and particles released along the sweep. Establish shape and timing, then finish the reference's material and secondary motion. Excludes general portals, sustained vortex loops and logo reveals. |
| [slot-vfx-spin-showcase](skills/slot-vfx-spin-showcase/SKILL.md) | Build SlotVFX reel-spin, anticipation and multi-line win showcases using the actual game outcome, strip art, image or Spine symbols, timed highlights and optional state-machine flows. |
| [slot-vfx-travel-effects](skills/slot-vfx-travel-effects/SKILL.md) | Create re-aimable SlotVFX travel effects such as zaps, pulses and orbs. Coordinate the moving head, riders, trails and impact, then verify instance IDs, coordinate spaces and arrival in the game runtime. |
| [slotvfx-build-verification](skills/slotvfx-build-verification/SKILL.md) | Verify a SlotVFX update or reported fix against explicit reproduction cases. Check installed MCP compatibility, test editor and runtime behavior separately, run fair before/after comparisons and update authorized local findings. |
| [slotvfx-dev-reports](skills/slotvfx-dev-reports/SKILL.md) | Draft actionable SlotVFX bug reports and evaluate developer replies using minimal reproductions, versioned evidence and clear editor/runtime boundaries. Correct unsupported findings and track workarounds without sending reports unless authorized. |
| [slotvfx-logo-reveals](skills/slotvfx-logo-reveals/SKILL.md) | Create, refine, preview, and export logo reveal animations in SlotVFX through MCP, including independently moving logo parts, particles, image FX, and selective shaders. Use for SlotVFX logo animation work; ordinary gameplay particle effects are outside this skill's main scope. |
| [slotvfx-mcp-authoring](skills/slotvfx-mcp-authoring/SKILL.md) | Author and refine SlotVFX projects through MCP: discover effect parameters, preserve existing work, manage clip membership and keyframes, read back writes, and verify changes. Use alongside the relevant visual-design skill. |
| [slotvfx-showcase-video](skills/slotvfx-showcase-video/SKILL.md) | Record requested SlotVFX clips or state-machine scenarios through MCP, verify true frame rate and loop behavior, save files reliably, and combine or deliver videos when requested. Supports named timelines and repeated cycles in 0.9.50. |
| [spine-vfx](skills/spine-vfx/SKILL.md) | Prepare and revise effects on existing Spine actors in SlotVFX, including bone or slot particle attachment, loop review, sprite plates and recorded or runtime delivery. |

## Scope and provenance

This is a skills-only snapshot of the maintained SlotVFX guides. The skill text was kept intact except for portable links to a copied workflow guide and wording that no longer assumes plugin installation. The workflow guide is embedded with each skill that links to it, so individual folders retain that reference after installation. The two helper scripts remain inside their original skill folders.

External reference links are for study; their images, media and project files are not included. This bundle does not grant access to local files or authorize unrequested publishing, deletion or credentials. The original skills and helper scripts are available under the [MIT License](LICENSE); linked third-party work is not relicensed here. See [third-party notices](NOTICE.md). Contributions are welcome through reviewed pull requests; see [CONTRIBUTING.md](CONTRIBUTING.md).
