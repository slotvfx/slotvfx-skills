---
name: slot-vfx-motion-craft
description: Write how a SlotVFX effect or Spine character moves — eases, springs, scale pops, staggers, beats, win escalation, loops, overlap down bone chains — as exact keys. Use with the build skills whenever something animates.
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Motion craft for slot VFX

The build skills say what to make. This one says how it moves, and how to write that motion into SlotVFX keys exactly instead of eyeballing handles.

Lines marked **(tested)** were measured in SlotVFX 0.9.59 through the MCP. Everything else is a starting point taken from motion-design practice (HyperFrames, GSAP, Remotion and the 12 principles); keep it only if it looks right on the real art at player scale. Where an approved number already exists in another SlotVFX skill, that number wins.

## 1. How SlotVFX evaluates a key

**A key pair with `free` tangents is a CSS / After Effects cubic-bezier (tested).** Sampled positions matched `cubic-bezier(0.25, 1, 0.5, 1)` and `back.out` to 0.01 px. So for a segment from key A (time t0, value v0) to key B (t1, v1) and a named ease `(x1, y1, x2, y2)`:

```
A.tangents = { mode: "free", out: { dt: x1·(t1−t0), dv: y1·(v1−v0) } }
B.tangents = { mode: "free", in:  { dt: (x2−1)·(t1−t0), dv: (y2−1)·(v1−v0) } }
```

- A named ease is therefore two keys, not a sampled run. `scripts/motion_keys.py ease` writes them.
- Overshoot eases work: a handle can carry the value past the next key. `back.out` went about 10% past the target and settled (tested).
- Use `timeMode: "exact"`. The default `legacy` snaps to tenths of a second and moves every handle-carrying key.
- Image layers key `x`, `y`, `scaleX`, `scaleY`, `rotation`, `opacity`. Particles key only `x`, `y`, `opacity`, so a particle's own scale or ease lives in its size and alpha curves (`set_project_curve`).
- Keep overshoot off `opacity`: it cannot go past 1. Put opacity on its own keys with a plain `.out` ease at the same times as the transform.
- The authoring guide says export bakes graph segments into runtime easing curves. Exact runtime parity of free handles was not measured here. Before promising frame-exact timing to a game dev, check one clip in the headless harness from [slotvfx-build-verification](../slotvfx-build-verification/SKILL.md).
- Measure, don't eyeball: `get_timeline` with `motion: { targetIds, timesSeconds }` returns evaluated positions and speeds. A speed jump between two neighbouring samples means a handle that doesn't match its neighbour. For scale, `render_layout` with `includeImage: false` returns `contentBounds` per strip cell; its precision is one world pixel per output pixel, so render at a 1:1 or 1:2 ratio.

## 2. Pick the ease by what the motion means

| Moment | Ease | Notes |
| --- | --- | --- |
| Something arrives: banner, symbol pop, logo part, badge | `power3.out` default; `expo.out` for punch | Starts fast, settles. Never `.in` for an arrival — it feels sluggish. |
| Something leaves | `power2.in` / `power3.in` | Exits are shorter than entrances: about 60–70% of the entrance duration. |
| Moves between two rest positions | `power2.inOut`; `sine.inOut` when calm | Camera pushes, panels sliding. |
| A head that strikes something | `power2.in` or linear into the hit | Accelerating into contact reads as force. The impact layers then start at the contact time. |
| Breathing, hovering, glow pulse | `sine.inOut`, there and back | See section 7. |
| Counter ticks, flicker, mechanical steps | `step` tangents | Discrete jumps. |
| Physical settle (landing, pop that wobbles) | a spring | Section 3. |

- **Vary on purpose.** In one beat, no more than two independent moves share both ease and duration. Make the slowest move in a sequence about 3× as long as the fastest, rather than running everything at 0.4 s.
- **Speed carries weight:** 0.15–0.3 s punchy, 0.3–0.5 s standard, 0.5–0.8 s heavy, 0.8–2 s cinematic.
- **Game-triggered clips react on the first frame.** A win clip that starts with an empty 0.2 s feels laggy. A wind-up is fine, but it must show something from frame one. Offsetting the first move by 0.1–0.3 s is for trailer edits, not gameplay triggers.

The full ease table is in the script. These beziers are the usual approximations, within about 1% of GSAP's own curves. The common ones, as `(x1, y1, x2, y2)`:

| Ease | Bezier | Ease | Bezier |
| --- | --- | --- | --- |
| power2.out | 0.33, 1, 0.68, 1 | power2.in | 0.32, 0, 0.67, 0 |
| power3.out | 0.25, 1, 0.5, 1 | power3.in | 0.5, 0, 0.75, 0 |
| power4.out | 0.22, 1, 0.36, 1 | power2.inOut | 0.65, 0, 0.35, 1 |
| expo.out | 0.16, 1, 0.3, 1 | sine.inOut | 0.37, 0, 0.63, 1 |
| circ.out | 0, 0.55, 0.45, 1 | back.out (1.7) | 0.34, 1.56, 0.64, 1 |

## 3. Springs: pick the register, then generate the keys

Describe a spring by **response** (seconds per undamped oscillation) and **damping ratio ζ**. The [spin-showcase skill](../slot-vfx-spin-showcase/SKILL.md) describes its landing as a visible wobble period and a decay time; convert with ζ = (1/decay) / √((2π/period)² + (1/decay)²).

For a spring that starts at rest, the first overshoot is exp(−ζπ / √(1−ζ²)) of the travel:

| ζ | Overshoot | Reads as |
| --- | --- | --- |
| 1.0 | none | premium settle; a logo lockup, UI |
| 0.85 | 0.6% | alive but not bouncy |
| 0.8 | 1.5% | |
| 0.7 | 4.6% | physical, a little playful |
| 0.6 | 9.5% | playful |
| 0.5 | 16% | very bouncy |
| 0.27 | 41% | the spin-showcase reel landing (period 0.13 s, decay 0.075 s) |

**Slots are not brand video.** HyperFrames' rule "smooth beats bouncy" is right for a logo lockup and wrong for a reel stop or a win pop. The approved reel landing sits at ζ ≈ 0.27 on purpose; keep it. Starting points, to be judged on the art:

- Reel landing: the spin-showcase values, unchanged.
- Win symbol pop, big-win banner slam: ζ 0.5–0.65, response 0.35–0.5 s.
- Logo lockup, final settle of a reveal, UI: ζ 0.85–1.0, response 0.4–0.6 s.

**Write springs as keys with the script (tested).** `scripts/motion_keys.py spring` places keys at the start, every peak, every crossing of the target and the end, fits bezier handles, and splits any segment that misses by more than 0.25% of the travel. ζ 0.65, response 0.4 s over 1,000 px became 7 keys. SlotVFX's evaluated positions stayed within 0.4 px of the closed-form spring, and within 1.7 px in the last 0.1 s, where the script hands over to the exact target. `--sampled` writes linear keys at 60 fps instead (the spin-showcase method); use it when keys must be dense anyway.

- `--v0` starts the spring with a velocity (value units per second), for something that arrives moving, like a reel.
- Don't hand-key a mid-state such as scale 1.1 on top of a spring or `back.out`. The curve already overshoots; an extra key double-bounces.

## 4. Scale in log space

A size change is seen as a ratio. With the same ease, scale interpolated linearly from 0.2 to 1 grows fastest, in relative terms, at the very start and seems to stall near the end. Interpolate in log space instead: equal ratios for equal steps of the ease.

**Tested**, `expo.out` 0.2 → 1 over 0.5 s on a 400 px square:

| Time | Linear-space scale | Log-space scale |
| --- | --- | --- |
| 0.02 s | 0.39 (×1.95 already) | 0.29 (×1.45) |
| 0.05 s | 0.60 | 0.45 |
| 0.12 s | 0.85 | 0.74 |
| 0.25 s | 0.98 | 0.96 |

The log version needs 4 fitted keys (`scripts/motion_keys.py ease ... --log`); the linear one needs 2. Use log space for pops from small, slams from big (3 → 1), zoom pushes and scaled springs (`spring --log`). Write `scaleX` and `scaleY` with the same keys, unless squashing.

**Squash on contact** (starting point): for 1–2 frames at impact, scaleX up and scaleY down with their product near 1, then release into the settle.

## 5. Choreography: order, overlap, stagger

- **What moves first reads as most important.** The win amount or banner leads; frame, glow and particles follow.
- **Follow-through:** each level lags its parent by 2–4 frames at 24 fps (about 80–170 ms) and settles after it. Banner, then frame, then glow, then debris.
- **Overlap, don't queue.** Start the next element while the previous one decelerates, with 30–50% overlap. Queued, finish-then-start sequences feel slow.
- **A group reads as one beat** when its whole stagger is short. Starting point: a 5×3 board spread over 0.2–0.4 s.

Grid staggers are computed, not hand-typed. `scripts/motion_keys.py stagger --rows 3 --cols 5 --origin center --amount 0.3` gives:

```
0.300  0.190  0.134  0.190  0.300
0.268  0.134  0.000  0.134  0.268
0.300  0.190  0.134  0.190  0.300
```

The script also takes `--origin edges`, `start`, `end`, `random`, `reels` (column order, like reel stops) and `line:1,0,0,0,1` (a payline, one row per column). `--ease` shapes the spread; `--each` gives seconds per cell of distance instead of a total.

**Where the delays live:**
- **Per-cell templates** ([slot-vfx-per-cell-effects](../slot-vfx-per-cell-effects/SKILL.md)) are spawned by the game. The template has no stagger; hand the dev the delay table with the integration notes.
- **Scene clips:** offset each cell layer's keys by its delay. `stagger_layers` shifts layers by one fixed interval in the order you give (the first stays put), so it can't express cells that share a distance. Use it for reel order, and per-layer key offsets for centre or edge spreads.

## 6. Beats, rhythm and win escalation

1. **Write a beat sheet before keys.** Each element gets a verb: SLAMS, COUNTS UP, BREATHES, SHATTERS, LOCKS IN. If you can't name the verb, the element isn't designed yet. Name the rhythm too: for example fast-fast-HOLD-fast.
2. **Build, breathe, resolve.** Entrances take about the first 30%. One ambient motion keeps the hold alive. The exit is quicker than the entrance. In slots the breathe usually lasts for a game-controlled time, so build it as a hold loop ([slot-vfx-hold-loops](../slot-vfx-hold-loops/SKILL.md)).
3. **Anticipation** runs at about 20–30% of the action it precedes. Size it to the payoff: a bigger wind-up for a bigger hit, and the anticipation's size roughly matches the settle's.
4. **Win tiers (BIG → MEGA → EPIC)** escalate by adding beats on one shared tempo, not by making one beat louder. Each tier lands on the same pulse with a different axis: scale slam, side snap, rise. The top tier gets the longest wind-up and a hold that runs longer than expected before it lands.
5. **Impact punctuation** (starting point): hold the moving element still for 2–5 frames at 60 fps at contact, as two equal-value keys, then release. It sells weight.
6. **Count-ups:** the number ticks in the game. SlotVFX supplies the banner's growth over the same duration and ease, so give the dev the ease name and its bezier. A multiplier or suffix lands after the count, on its own beat.

## 7. Loops that don't look like loops

A looping clip repeats at its length L, so every key-driven cycle has to divide L. Cycles of 3, 5 and 7 s never line up, and so are only usable for things the clip doesn't key: particle emission, Spine idles.

For keyed layers, give each layer a different whole number of cycles per clip, such as 1, 2, 3 and 5, and offset their phases. They line up only at the loop point. Starting point for breathing: `sine.inOut` there and back, scale change ≤5%, cycles of 2–4 s.

## 8. Cuts and hand-offs (trailers, base game → feature)

- **Velocity-matched cut:** exit with an `.in` ease and enter with the `.out` of the same family. Both pass through the cut at the same speed when distance divided by duration is equal on each side. For `power2` the speed at the cut is about 3× the average speed.
- **A transition** that overlaps two scenes shortens the total by the overlap. **An overlay** (light leak, flash) sits centred on the cut and adds no time.

## 9. Judge it as motion

- Play at normal speed, at gameplay size, through at least two cycles. A strong peak frame proves nothing about the motion.
- **Diagnose timing** by trying 50% faster and 50% slower. If either looks better, the timing was wrong.
- Read back keys with `get_timeline` and compare their count with what the script generated, as [slotvfx-mcp-authoring](../slotvfx-mcp-authoring/SKILL.md) describes.
- Report which numbers you measured and which you judged by eye.

## 10. Spine characters

Keying bones on a Spine character follows the same eases and beats, plus character rules: state the action in one sentence, block poses before curves, make it read before any VFX, give every bone its own curve, change the silhouette so a new animation doesn't read as an existing one, uneven timing, overlap and follow-through down bone chains, arcs from rotation, planted contacts, moving holds and clean cycles. Read [Spine character motion](references/spine-character-motion.md) before writing keys for a Spine animation; `scripts/motion_keys.py chain` writes the overlap down a chain.

## Script

[`scripts/motion_keys.py`](scripts/motion_keys.py) (Python 3, standard library only) writes the keys and tables used above; run `python3 scripts/motion_keys.py -h`. Each key subcommand prints JSON batches of up to 180 keys for `slotfx_set_timeline_keyframes`; pass each batch unchanged and read the track back. `stagger` prints a delay grid and a JSON list. `chain` prints Spine-style rotate keys per bone. The ease beziers are the common easings.net approximations under GSAP's names; the springs are the closed-form damped-oscillator solution, so the same arguments always give the same keys.
