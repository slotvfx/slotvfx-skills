# Spine character motion

How to key a Spine character so it moves like an animator made it: poses first, then timing, then the overlap that makes it feel alive. The rest of motion-craft covers eases, springs and staggers for layers; this file applies the same ideas to bones.

Nothing here has been measured in SlotVFX yet. Every number is a starting point from animation practice (the 12 principles, pose-to-pose workflow); keep it only if it looks right on the real rig at gameplay size, and note what you judged by eye. Where the rig's existing animations already set a tempo or pose range, match them.

## 1. Read the rig before keying

Read the skeleton and the existing animations first (with the Spine read tools, such as `slotfx_get_spine_rig` and `slotfx_get_spine_animation`, when the running app has them; check their schemas). Note:

- **Chains**: root → hip → torso → chest → neck → head; shoulder → upper arm → forearm → hand; tails, ears, hair, capes, wires. These are where overlap lives.
- **What is already driven**: physics constraints, IK and transform constraints move bones you shouldn't also key. Keying a physics-driven bone fights the constraint; lower its mix for the beat instead, and only if it must read differently.
- **The existing tempo**: how long the idle cycle is, how far the character rotates in its win or attack. A new animation that ignores them looks pasted in.
- **Rotation values in a Spine rotate timeline are added to the setup pose**, so 0 means "setup angle", not "pointing right".

## 2. Pose to pose: block before you ease

Work in this order and don't skip to curves:

1. **Name the beats.** Write one line per beat with a verb, as in the main skill's beat sheet: CROUCHES, LUNGES, STRIKES, RECOILS, SETTLES.
2. **Key poses.** One pose per beat on the main bones only (root, hip, torso, head, the limb doing the action), held with stepped keys. Play it: the story must read from the poses alone.
3. **Phase table.** For every move between two poses, write: duration, which bones move, rotation and travel, ease, which bone leads, and which bones follow and by how much. Prefer this table over one ease applied to everything.
4. **Breakdowns.** Add the in-between pose that sets the arc (a hand that swings down and through, not straight across). This is where arcs come from.
5. **Curves, then overlap.** Only now set eases (section 2 of the main skill) and add the follow-through (section 4 below).

**Every bone gets its own curve.** Don't drive the whole body from one shared progress value or one ease; that makes the rig move as a single stiff piece.

## 3. Timing and silhouette

- **Silhouette sells it.** A new animation must read differently from the rig's other animations in silhouette at tile size: a different lean, a wind-up in the opposite direction, a full-body line of action. Changing small parts (wires, a few degrees of hand angle) barely shows, especially under VFX flashes. Learned on the Rocket raccoon attack: the first version read as "the win animation again" until the body pose changed.
- **Weight comes from timing.** Starting points at 30 fps: snappy, light characters 3–6 frames per move; normal 6–10; heavy 10–16. Big characters take longer to start and stop.
- **Uneven timing.** Up and down, out and back must not take equal time; a symmetric move looks mechanical. A jump rises fast and hangs at the top; a strike winds up slowly and hits in a few frames.
- **Anticipation** is about 20–30% of the action, in the opposite direction, sized to the payoff (main skill, section 6).
- **Spacing**: wide spacing reads as speed, close spacing near a pose reads as weight and emphasis. Ease into the key poses and fly between them.
- **Impact**: hit the contact pose fast, hold or nearly hold it 2–4 frames, then recover more slowly than you struck.
- **Personality presets** (starting points): *heavy* — long anticipation, small overshoot, slow settle; *snappy* — short anticipation, fast action, a crisp overshoot of 5–10°; *floaty* — sine eases, long holds at the top, gentle overlap.

## 4. Overlap and follow-through down a chain

This is what separates animation from moving a puppet.

- **Successive breaking of joints**: the parent leads, each child starts later and settles later. Start with 2–4 frames of lag per level at 30 fps (about 0.07–0.13 s); loose things (tails, hair, capes) take the long end.
- **Children swing further**: each level a little more rotation than its parent, about 1.1–1.3× for loose parts, about 1.0 for stiff ones.
- **Follow-through**: when the parent stops, loose children overshoot past the end pose and settle back, with the overshoot growing down the chain.
- **Drag**: when the parent starts suddenly, the child first lags behind (holds or moves slightly backwards) before catching up.
- **Secondary action** supports the main action and never competes with it: smaller, later, softer.

`scripts/motion_keys.py chain` writes this for you from the parent's keys. Example: a tail of 4 bones following a hip swing, 3 frames lag at 30 fps, each child swinging 1.2× its parent, overshooting 15% at the end:

```
python3 scripts/motion_keys.py chain --bones hip,tail1,tail2,tail3 \
    --keys "0:0,0.25:-12,0.6:25:power2.out,1.0:0" --ease power2.inOut \
    --lag 0.1 --gain 1.2 --overshoot 0.15
```

Each key is `time:value`, optionally `:ease` for the segment that starts at that key (otherwise `--ease`). With `--overshoot`, don't also give the last segment an overshooting ease such as `back.out`: it double-bounces. Add `--loop 1.0` for a cycle (no overshoot in loops): shifted keys wrap around the loop length so the cycle stays seamless. Output is Spine-style rotate keys per bone (`time`, `value`, and `curve` as absolute bezier handles `[cx1, cy1, cx2, cy2]`, the Spine 4.x JSON form). Convert them to the schema of the Spine animation tool you are using; don't guess its field names.

## 5. Arcs

- Organic motion travels on arcs. Get arcs from **rotation down the chain**, not from translating the end bone in a straight line.
- When a translate is needed (root bounce, a lunge), add a little rotation on the same beat so the path curves.
- Check an arc by sampling the end bone (hand, head, tail tip) at a few times: the points should lie on a smooth curve with spacing that matches the intended ease. A kink means a breakdown is missing or a key's handle doesn't match its neighbour.

## 6. Squash, stretch and contact

- Concentrate squash and stretch around acceleration and contact; don't run it continuously.
- Keep volume: when scaleY drops, scaleX rises so the product stays near 1.
- **Planted contacts stay planted.** A foot on the ground or a hand on a prop must not slide while the body squashes or turns. Use IK if the rig has it; otherwise counter-rotate the child so the contact point stays still, and check it by sampling.

## 7. Holds and loops

- **Never a dead hold.** A held pose keeps a tiny drift (a moving hold): 1–3° of breathing on the torso, a small settle on loose parts. A perfectly frozen frame looks broken.
- **Idles**: breathing on the torso, head following 2–4 frames later, loose parts later still. Cycle length a whole divisor of the clip; give the different parts whole-number cycle counts (1, 2, 3) with phase offsets, as in the main skill's section 7.
- **Walk and run cycles**: block contact → down → passing → up for each step, two steps per cycle. The hip is lowest on the down pose and highest on the up pose; arms swing opposite to legs; the head bobs with the hip and lags slightly. Feet stay planted during contact (section 6).
- **Loop seam**: the first and last keys of every bone must match in value *and* tangent. `chain --loop` handles the wrap for followers; check the parent's own seam too.

## 8. Review

Play it at normal speed and at gameplay size, at least two cycles, then ask:

- Does the action read from the silhouette alone?
- Is there a clear lead bone, and do the others follow it in order?
- Are timings uneven where they should be (fast strike, slow recovery)?
- Do loose parts overlap and settle, or stop dead with the parent?
- Do arcs stay smooth, and do planted contacts stay put?
- Is anything in a dead hold?
- Try the whole thing 50% faster and 50% slower. If either looks better, the timing was wrong.

Then show it in SlotVFX through the Spine animation proposal and preview. The user applies it from the editor's own review banner; don't look for a tool to apply it.
