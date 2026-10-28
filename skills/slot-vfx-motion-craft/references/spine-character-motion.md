# Spine character motion

How to key a Spine character so it moves like an animator made it: intent first, then poses, then timing, then the overlap that makes it feel alive. The rest of motion-craft covers eases, springs and staggers for layers; this file applies the same ideas to bones.

Nothing here has been measured in SlotVFX yet. Every number is a starting point from animation practice (the 12 principles, pose-to-pose workflow, game frame data); keep it only if it looks right on the real rig at gameplay size, and say which numbers you judged by eye. Where the rig's existing animations already set a tempo or pose range, match them.

## 1. Read the rig before keying

Read the skeleton and its existing animations first (with the Spine read tools, such as `slotfx_get_spine_rig` and `slotfx_get_spine_animation`, when the running app has them; check their schemas). Note:

- **Chains**: root → hip → torso → chest → neck → head; shoulder → upper arm → forearm → hand; tails, ears, hair, capes, wires. Overlap lives here.
- **Pivots**: a bone rotates and scales around its own origin. Know where each origin sits before planning squash or a swing; a squash keyed on a hip whose origin is mid-body lifts the feet off the ground.
- **What is already driven**: physics, IK and transform constraints move bones you shouldn't also key. Keying a physics-driven bone fights the constraint; lower its mix for the beat instead, and only if it must read differently.
- **Inheritance**: children inherit the parent's rotation and scale. Non-uniform scale on a parent shears rotated children; squash on a leaf bone, or on a bone whose children don't inherit scale.
- **The existing tempo and pose range**: idle cycle length, how far the win or attack rotates. A new animation that ignores them looks pasted in.
- **Values**: rotate timeline values are added to the setup pose, so 0 means "setup angle". Translate is in the parent's space, so rotating a parent changes where a child's translate points. Rotation values interpolate numerically: going from 170 to -170 swings 340° the long way; keep neighbouring keys within 180° unless a full spin is the point.
- **Prefer bone keys over mesh deform keys.** Deform keys are heavy and break when the mesh changes; use them only for a shape bones can't make.

## 2. State the action, then block it

1. **One sentence first**: who moves, what they intend, how much force, where they end, and the feeling. "The raccoon winds up and slams a lightning punch at the reels, heavy and smug." If the sentence is vague, the animation will be too.
2. **Rank the motion**: one primary action (the punch), then secondary actions beneath it (tail whip, ear flick, wires). Secondary never leads and never competes.
3. **Name the beats** with verbs, as in the main skill's beat sheet: CROUCHES, LUNGES, STRIKES, RECOILS, SETTLES. Typical event poses: rest, anticipation, commit, passing, apex or hold, contact, overshoot, settle.
4. **Key poses**: one pose per beat on the main bones only (root, hip, torso, head, the acting limb), held with stepped keys. Play it: the story must read from the poses alone, and from a few still frames.
5. **Phase table**: for each move between poses write the duration, which bones move, rotation and travel, ease, which bone leads, which follow and by how much, and any contact that must stay put. Prefer this table to one ease applied to everything.
6. **Breakdowns**: add the in-between pose that sets the arc (a hand swings down and through, not straight across).
7. **Curves, then overlap**: only now set eases (section 2 of the main skill) and add follow-through (section 4 below).

**Every bone gets its own curve.** Driving the whole body from one shared progress value or one ease makes the rig move as one stiff piece.

**Primary motion first, effects last.** The animation must read with no particles, flashes or shaders on. VFX that hides a weak pose is a reason to fix the pose, not to add more VFX.

## 3. Timing, spacing and silhouette

- **Silhouette sells it.** A new animation must read differently from the rig's other animations in silhouette at tile size: a different lean, a wind-up in the opposite direction, a full-body line of action. Small parts (wires, a few degrees of hand angle) barely show, especially under VFX flashes. Learned on the Rocket raccoon attack: the first version read as "the win animation again" until the body pose changed.
- **No twins.** Left and right limbs that mirror each other, at the same time, look dead. Offset them in angle and by a frame or two.
- **Weight is timing.** Starting points: snappy, light characters 0.1–0.2 s per move; normal 0.2–0.35 s; heavy 0.35–0.55 s. Big characters take longer to start and stop.
- **Uneven timing.** Up and down, out and back must not take the same time. Fast commit, slow recovery. A jump launches fast, hangs near the apex, falls faster than it rose and lands in a few frames. Example phase ratios for a 1.5 s jump at 30 fps (starting point): rest 4 frames, crouch 6, crouch hold 2, launch 9, hang 12, fall 6, landing squash 2, recover 4.
- **Attack frame data** (games, at 60 fps; starting points): light attack startup 3–6 frames, active 2–4, recovery 8–12; heavy attack startup 12–20, active 4–8, recovery 16–24. Startup is the anticipation.
- **Anticipation** runs opposite the action, about 20–30% of the action's time (main skill, section 6), and about 10–20% of its size for small moves, more for big hits. A short preparation followed by a big change in spacing reads as force.
- **Spacing**: wide spacing reads as speed, close spacing near a pose reads as weight and emphasis. Ease into the extremes and holds; don't ease into every key.
- **Don't stop at passing keys.** An ease-in-out on every segment makes the body stop at every key. Only extremes (direction changes), contacts and holds get zero speed. Through a breakdown or passing pose, keep the speed continuous: give the segments on both sides handles that agree in slope.
- **Impact**: reach contact fast, hold or nearly hold for 2–5 frames at 60 fps (hit-stop), then recover more slowly than you struck. Put a Spine event key (for example `hit`) on the contact frame so the game and the VFX sync to it.
- **Exaggeration**: games read at small size and speed, so push key poses 20–30% past realistic. Pick the one channel that tells the idea (pose, hold, spacing, squash) and push that, not every channel at once.
- **Personality** (starting points): *heavy* — long anticipation, little overshoot, slow settle; *snappy / energetic* — short anticipation, fast action, crisp rotation overshoot of 5–15°; *playful* — bouncy settles, squash on impacts, overshoot 10–20% (past about 25% it looks broken); *floaty* — sine eases, long holds at the top, gentle overlap.

## 4. Overlap and follow-through down a chain

This is what separates animation from moving a puppet.

- **Successive breaking of joints**: the parent leads, each child starts later and settles later. Start with 2–4 frames of lag per level at 30 fps (about 0.07–0.13 s); loose things (tails, hair, capes) take the long end.
- **Children swing further**: each level a little more rotation than its parent, about 1.1–1.3× for loose parts, about 1.0 for stiff ones.
- **Follow-through**: when the parent stops, loose children carry on past the end pose and settle back, the overshoot growing down the chain.
- **Drag**: when the parent starts suddenly, the child first trails behind before catching up. The delay alone gives this.
- **Secondary action** (an ear flick, a blink, a weight shift) is smaller and later than the primary: about 30–50% of its size, starting 2–6 frames after it, with a different ease. Quiet it near the primary's key pose.

`scripts/motion_keys.py chain` writes this from the lead bone's keys: each level samples its parent `--lag` seconds later and swings `--gain` times as far. Example: a tail of 4 bones following a hip swing, 3 frames lag at 30 fps, each child 1.2× its parent, overshooting 15% per level at the end:

```
python3 scripts/motion_keys.py chain --bones hip,tail1,tail2,tail3 \
    --keys "0:0,0.25:-12,0.6:25:power2.out,1.0:0" --ease power2.inOut \
    --lag 0.1 --gain 1.2 --overshoot 0.15
```

- Each key is `time:value`, optionally `:ease` for the segment that starts at that key (otherwise `--ease`).
- With `--overshoot`, don't also give the last segment an overshooting ease such as `back.out`: it double-bounces.
- The followers end later than the lead (here 0.35 s for the first follower and 0.1 s more for each one after), so the animation gets longer. Check its duration, and that the end pose matches what the next animation expects. In SlotVFX a `setDuration` op shorter than the last follower key is refused ("Keys run to … past the duration"); without one the duration is the last key. If you start from `copyFrom`, check the duration the proposal returns.
- `--loop L` for cycles: the lead keys must run from 0 to L and end on the starting value. Delayed keys wrap round the seam, and the segment that crosses it is split exactly, so the cycle stays seamless. No overshoot in loops.
- Output is Spine-style rotate keys per bone: `time`, `value`, and `curve` as absolute bezier handles `[cx1, cy1, cx2, cy2]` (the Spine 4.x JSON form). For `slotfx_propose_spine_animation` on a 4.x rig, keep `time` and `value` and wrap the curve as `curve: {points: [cx1, cy1, cx2, cy2]}`, in a `setKeys` op with target `{type: "bone", name, timeline: "rotate"}`. On a 3.x rig convert each curve to fractions of its segment, `{bezier: [(cx1 - t0) / dt, (cy1 - v0) / dv, (cx2 - t0) / dt, (cy2 - v0) / dv]}`; where the two keys have the same value (dv = 0) a curve that swings out and back cannot be written, so add a key at the swing. For other tools, check their schema rather than guessing field names.
- It writes rotation only. For translate or scale on followers, apply the same idea by hand: delay and soften.

## 5. Arcs

- Organic motion travels on arcs. Get them from **rotation down the chain**, not from translating the end bone in a straight line.
- When a translate is needed (root bounce, a lunge), add a little rotation on the same beat so the path curves, and lift the midpoint of a straight move slightly.
- Graceful characters move on flowing arcs; aggressive ones change direction sharply. Arcs are part of personality.
- Check an arc by sampling the end bone (hand, head, tail tip) at a few times: the points should lie on a smooth curve with spacing that matches the intended ease. A kink means a missing breakdown or handles that disagree.

## 6. Squash, stretch and contact

- Concentrate squash and stretch around acceleration and contact; don't run it continuously. Starting point for an impact: squash about scaleX 1.2 / scaleY 0.8 for 2–4 frames at 60 fps, recover over 4–8.
- Keep volume: when scaleY drops, scaleX rises so the product stays near 1.
- Scale around the contact: squash a bone whose origin is at the contact point (feet for a landing), or the character lifts off as it squashes.
- **Planted contacts stay planted.** A foot on the ground or a hand on a prop must not slide while the body squashes or turns. Use IK if the rig has it; otherwise counter-rotate the child so the contact point stays still, and check it by sampling.
- Size the reaction to the force: a landing from a high jump squashes more than a hop.

## 7. Holds, loops and hand-offs

- **No dead holds.** A held pose keeps a tiny drift (a moving hold): 1–3° of breathing on the torso, a small settle on loose parts. Hold the pose, not every channel.
- **Idles**: breathing on the torso, head following 2–4 frames later, loose parts later still. Cycle length a whole divisor of the clip; give different parts whole-number cycle counts (1, 2, 3) with phase offsets, as in the main skill's section 7. Slots replay idles thousands of times: keep them subtle enough to stay pleasant on the hundredth viewing.
- **Walk and run cycles**: block contact → down → passing → up for each step, two steps per cycle. The hip is lowest on the down pose and highest on the up pose; arms swing opposite the legs; the head bobs with the hip and lags slightly. Feet stay planted during contact (section 6).
- **Loop seam**: the first and last keys of every bone must match in value *and* slope. `chain --loop` handles the wrap for followers; check the lead bone's own seam too.
- **Hand-offs between animations**: key every bone this animation touches at its first and last frame, so mixing from or to another animation doesn't pop. An attack or win that returns to idle should end on (or ease into) the idle's first pose.

## 8. Review

Play it at normal speed and at gameplay size, at least two cycles, then ask:

- Can you tell the action from a few still frames and from the silhouette alone?
- Is there one clear lead, and do the other bones follow it in order, starting later and settling later?
- Does the anticipation point opposite the action, and is it sized to the payoff?
- Are timings uneven where they should be (fast strike, slow recovery)?
- Does anything stop dead at a passing key, or freeze in a dead hold?
- Do loose parts overlap and settle, or stop with the parent?
- Do arcs stay smooth, and do planted contacts stay put?
- Does it still read with the VFX off, and does it look different from the rig's other animations?
- Does it start and end cleanly against the animations it mixes with?
- Try the whole thing 50% faster and 50% slower. If either looks better, the timing was wrong.

Then show it in SlotVFX through the Spine animation proposal and preview. The preview samples only within the animation's duration, so check a loop's seam there by comparing the poses at 0, just before the end and at the end, and play two cycles in the editor's banner Preview. The user applies it from the editor's own review banner; don't look for a tool to apply it.
