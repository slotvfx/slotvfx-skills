# Worked example: Fairy Spins choreography

This is a historical recipe from the supplied 0.9.50 pack, not a requirement for another game. Its project, build notes, assets and generator are not bundled. All numeric settings and visual preferences below belong to that example. Use current schemas and the actual game rules; preserve existing project work. Read the parent [spin showcase skill](../SKILL.md) for the current workflow.

**The worked example** is a fictional Fairy Spins showcase. Its original project-specific assets and generated keys are not installation dependencies. It has three spins:
- **Spin 1:** a V of five fairies.
- **Spin 2:** three lines through two wild keys.
- **Spin 3:** four lines, with the second key landing after a reel 5 anticipation.

Its numbers are quoted below.

## 0. Settle the result before any key

Use the outcome already provided by the user or game data. Clarify only if a missing outcome blocks meaningful work. For a fictional showcase, confirm that fictional outcomes are within the request. The result fixes everything downstream:
- which strip index lands in each row;
- which reel gets the anticipation;
- each payline's route, and the order the lines play in;
- which symbols have a Spine win animation.

In this fictional multi-line showcase, wild keys occupied shared cells, such as reel 3 row 2 and reel 4 row 3. Do not insert wilds or fabricate winning combinations in a real replay; use the actual outcome and game rules.

## 1. Measure the strip, and space copies by its content period

A reel is 2–3 copies of a tall strip image, leapfrogging.

**Space the copies by the strip's content period, not by the image height.** Spacing by height left a gap of about 200 px in the spinning reel.
- **Measure:** render one strip isolated and read its alpha profile, or its `contentBounds`, to find the symbol centres.
- **In Fairy Spins:** 6,065.40 px at scale 1.505, and 6,004.95 px at 1.49.

**Fit the landing.** Per reel, pick the strip index that puts the wanted symbols in their rows, and solve the reel's y by a weighted fit over the four visible cells. Weight card symbols 4× and fit every row: since reels show only images, every row must sit on a real symbol. Later reels take extra revolutions (0, 0, 1, 1, 2).

**Spins after the first** continue from the previous spin's end phase on each column, and keep the first spin's stop times so the flash and anticipation layers still line up.

## 2. Motion: generate the keys by script

Write one motion function per reel, sample it, and push linear keys.
- **Sampling:** 60 Hz for curved sections, 30 Hz for a long deceleration.
- **Pushing:** `timeMode: "exact"`, linear tangents, at most 200 keys per call (a hard cap). Omit tangents on bool and string keys.

| Phase | Settings |
| --- | --- |
| Start stagger | 0.06 s between reels |
| Lift (the "hold and up slightly") | 45 px up over 0.12 s (sine ease), then a 0.08 s hold |
| Accelerate | 0.25 s into the cruise |
| Stops, reels 1–4 | about 0.22 s apart (1.36 / 1.58 / 1.80 / 2.05 s) |
| Landing (the "slight shake") | 38 px overshoot, then a damped spring (period 0.13 s, decay 0.075 s, about 0.36 s), plus a small sideways shake |
| Teased reel | cruises at 6,000 px/s, then decelerates as (1 − u)² over 1.5 s. It lands about 2.2 s after reel 4, with a 22 px overshoot and a heavier spring (0.16 s / 0.085 s). |

**Wraps need a guard key before 0.9.48.** A copy wraps to the top with a **step** key. Before 0.9.48 a step key also eased the segment *arriving* at it, so a long linear run into a wrap stopped being linear. That left a copy 664 px ahead of its path and an empty cell. 0.9.48 fixed it: the arriving segment follows the chord.
- **On older builds:** add a linear key 1.2 ms before every step key, on the line.
- **Check:** measure `contentBounds` of the isolated strip mid-spin against the linear path.

## 3. Blur, and still strips

If the strip art carries spin blur as FX Stack keys (`directionalBlur`), **those keys run in every clip that includes the strip**, on that clip's time. `get_timeline` doesn't show them.
- **Fix:** duplicate the strips with an empty FX Stack. These still strips are used for Idle and Win.
- **First spin clip:** retime the blur windows to its start and stop times.
- **Later spins:** from each reel's landing time, set the moving copies to opacity 0 **and `visible: false`**. The still strip takes over, carrying the spring and the shake. Keep the still strip `visible: false` until then.

## 4. Symbols: images for spin and idle, Spines only on the win

**Preference in this example:** reels spin and idle as images, with a Spine visible only for its active payline. Other games may intentionally animate idle symbols; follow their design and performance constraints.

In an earlier build, Spines rode the reels and were parked off-screen when out of view. The user saw them "still behind reel" and dropping frames. Hide or stop content that should be inactive; use opacity zero only when continued simulation is intentional.

**A winning cell is shown by exactly one of these at a time:**
1. **The strip image**, dimmed while a win dim is on.
2. **A masked image copy** of the symbol, placed above the dims. This is the "bright" state.
3. **The symbol's Spine**, playing its win animation.

**Masked image copies:**
- **Making one:** duplicate a still strip and set `image.maskPath` to a rectangle around one symbol's span. The coordinates are **image pixels from the top-left** and scale with the layer.
- **Placing it:** put it at the strip's own position, and it shows only that cell.
- **Pop or pulse:** key x, y, scaleX and scaleY together about the card centre, so the card grows in place.
- **During the landing:** the copy rides the settle. y = rest + d(t) − D for the spring, plus the sideways shake on x. The landing pop can be folded into those samples.

**For an explicitly fictional showcase only:** Spin 1's V used fairies where the chosen strip landed a scroll or a basket. A real game/replay must instead use its correct symbol outcome. Use a masked copy of the strip's fairy card, offset so the card sits on the cell. It rides in with the reel from above the view, and rides out at the start of the next spin.

**Spines:**
- Keep x, y and scale at the cell's rest position, set by single keys.
- Set `visible` false at 0 s.
- At the line hit (2 ms early): `visible` true, the win `animation` key, and a scale pop (1 → 1.18 → 0.96 → 1 over 0.34 s).
- On 0.9.47 the recorder and `render_layout` draw a Spine that is revealed mid-clip.
- **Fading a Spine:** from 0.9.49 a Spine has an `opacity` track, so key it 1 → 0 over 0.1 s and then hide it. Export with 0.9.49 or later, because earlier runtimes reused a pooled Spine still faded out. On older builds, hide the Spine and show its image copy at the same time, then fade the copy. Either way, set `animation` back to `idle` while it is hidden, so the next show restarts the win animation.

## 5. Anticipation that reads

Run it from the second-to-last stop until the teased reel lands, about 2.2 s:
- **Frame:** a baked texture around the teased reel on an image layer, with opacity pulsing 1 ↔ 0.6 every 0.25 s.
- **Dim:** an image at α 0.42 over the other reels. The winners already landed stay lit as image copies above it, and pulse 1.0 → 1.05 every 0.6 s.
- **Inside the reel:** rising sparks and a glow, plus two runners on a rounded-rect path around it (`spacingOffset` 0 and 0.5).
- **Landing impact:** a ring and stars. The frame pops to 1.12 and fades out over 0.25 s.

## 6. The payline and the highlight

**For this payline presentation, use an open line through the winning cells, left to right.** A closed decorative path may fit another requested treatment, but must not misrepresent the actual winning route. A comet circling the specials was rejected as "moving in a closed path".
- **Head:** a head particle on an open custom path (corner handles, tension 0) draws the line.
- **Line pieces:** one image per segment.
  - The texture has a 200 px core in 256 px, so a segment of length L is L·256/200 wide.
  - Reveal it by keying scaleX from 0.002 to 1 while x/y move from the segment start to its midpoint.
  - **`image.rotation` is counter-clockwise positive,** so use −atan2(dy, dx) in y-down space. Unnegated angles mirrored every sloped piece.
- **Hit times** come from the fraction of path length at each cell. At each hit:
  - a ring and a spark burst;
  - the cell frame scales 1.3 → 1.0;
  - the symbol lights: a copy pops, or a Spine starts.
- **One ring layer and one spark layer can serve every hit in a spin.** List the burst times, and step-key the emitter x/y 6 ms before each burst.
- **What makes winners read:**
  - crisp per-cell frames, pulsing 1.0 ↔ 1.03 in the win loop;
  - a dim over the rest (α 0.55);
  - glow and rays behind each winner, in local simulation space so moving them to the next cell moves their live particles;
  - the Spine animations.

## 7. Several lines, one after another

**Draw time:** each line draws at about 2,900 px/s, then holds 0.55 s. In the win loop each line gets 1.2 s: a 0.32 s redraw, then a hold.

**Line change**, the part users notice:
- The previous line's pieces, frames and glows fade 0.12 s before the next line starts.
- Its cells drop back under the dim: Spines hidden, copies faded.
- The next line's cells light as its head reaches them.
- Cells on both lines, such as the wilds, stay lit and pop again.
- A previous line's symbols still animating after the switch is a bug report waiting to happen.

**Keep the seams consistent:**
- **End of the spin clip:** the last line fades before the clip ends. The win loop then starts from its own wrap state: only cells shared by the last and first lines are lit.
- **Start of the next spin:** begin from that same state. Only those lit cells ride out as image copies, and everything else starts dark. Starting with every copy lit caused a brightness pop.
- **Bright before line 1:** cells on the first line may stay bright from their landing through the dim fade-in. In an anticipation spin, all winners on the anticipating side stay bright. Other cells fade out with the dim.

**Build it as a cell-state model in a script.** For each cell over time, record off / image / Spine, and generate every key from that. Before uploading, print a state table at the line-change times (which ids are lit) and check it.

## 8. Clips and gating

- **Clips:**
  - Idle: 4 s, loop.
  - Each Spin: one-shot, as long as its sequence.
  - Each Win: a loop of 1.2 s × the number of lines, or 3.2 s for a single line.
- **Gate visual appearance with opacity keys when appropriate.** Particle `startTime` belongs to the layer, not the clip; opacity does not necessarily stop emission. Use membership or separate layers for independent birth timing.
- **Membership:**
  - A layer shown nowhere in a clip should not be a member of it.
  - Idle has only the still strips and ambience.
  - Remove Spines that never win from every clip.

## 9. State machine and a neutral base

- **States:** Idle →(`spin`) Spin →(`clipComplete`) Win →(`idle` / next spin trigger).
- **More spins:** add states with their own triggers (`spin2`, `spin3`) and `clipComplete` into their own Win. From 0.9.49 `update_transition` and `delete_transition` edit and remove transitions; on older builds, add new ones instead of retargeting.
- **Neutral base:** the base timeline plays underneath the state clips. Keep a neutral base timeline with the static scene only. From 0.9.50, pass it as `timelineId` on `start_recording`; on older builds keep it active.
- **Check before recording:** confirm the source in the `start_recording` reply before building on the take.
- **Verify transitions with a recorder scenario** (see the [video workflow](../../slotvfx-showcase-video/SKILL.md)). The editor's state preview doesn't take `clipComplete`.

## 10. MCP mechanics that bit

- **Per-call caps:**
  - `create_layers`: at most 25 `featureValues` per particle;
  - `reorder_layers`: 100 items per call;
  - `set_timeline_keyframes`: 200 keys per call.
- **Rewriting tracks:** delete the old keys by their exact times (`timeMode: "exact"`) before writing new ones. A set only replaces keys at matching times.
- **Thousands of keys:** use ordered, resumable batches and sequential uploads by default. Use agents only when delegation is authorized and writes are independent. Compare keyframe counts and representative values with the generator.
- **Saves:** checkpoint substantial edits and save completed stages. After a crash, compare reopened state with available saved data/checkpoints before overwriting anything. A cloud-revision comparison applies only if that service is available.

## 11. Verify

**Render the moments that matter:**
- the lift;
- mid-spin, checking for no empty cells;
- each landing;
- the anticipation;
- the teased landing;
- each line mid-draw;
- **both sides of every line change**, checking that only the new line's cells are lit.

Then record the scenarios and check the frames. If the device is offline, prototype with a 2D mock that composites strip crops at the computed y per frame, and print the cell-state table.
