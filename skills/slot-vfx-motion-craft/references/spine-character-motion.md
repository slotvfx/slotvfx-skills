# Spine character motion

Key a body that has weight, not a set of separate bones. The full guide, with tested amounts, timing tables and the review checklist, is served by SlotVFX: read `slotfx_get_authoring_guide` topic `spine-character-motion` before writing keys for a Spine character, and run `slotfx_check_spine_motion` on every new or edited animation before proposing it. If those tools are missing, ask the user to update SlotVFX, follow the rules below, and judge the result from preview strips next to the rig's idle.

Two clips an animator rejected show what goes wrong:

- **A breathing idle** made of one rotation on the torso bone. The upper body leaned as one block around frozen hips, the face moved most and the loop hitched. Later redone with the right parts but far smaller than the rig's own idle, it read as almost static.
- **A fist pump** that bent the elbow past straight and threw the arm up the back, while the body stood still.

Matching seam values and keys that read back exactly did not catch either. Work in this order:

1. Read the rig and its own animations (`slotfx_get_spine_rig`, `slotfx_get_spine_animation`): roles, contacts, which way each elbow and knee bends, what the constraints drive, and how much the idle moves.
2. State the action and the cause of every motion in one sentence; plan the key poses and which part leads.
3. Key from the hips outward, starting from the idle's keys.
4. Run `slotfx_check_spine_motion` and fix every FAIL.
5. Look at preview strips next to the idle, at game size, and only then propose.

Core rules:

- **Start from the idle and end on it.** Key every body bone the idle keys, so nothing snaps to the setup pose and the idle's own life keeps going.
- **The hips lead.** Motion travels out through the spine, shoulders, arms and head, each part a frame or two (at 30 fps) after its parent. Loose parts (hair, tails, capes) lag a little more and settle later.
- **Hinges stay on their own side of straight.** Learn each elbow's and knee's bend direction from the idle; never key it straight or past straight.
- **The weight stays over planted feet.** When the upper body leans or reaches, the hips shift the other way; planted feet do not slide.
- **The head stays steady.** Spread a bend over the spine segments and counter-rotate the neck and head so the gaze holds.
- **A breath is a wave of small offsets, not a lean**: the chest rises, the shoulders lift after it, the arms drag, the hips bob, the feet stay planted.
- **Idles move about as much as the rig's own idle.** Subtle is fine; invisible is not.
- **Arms**: shoulder leads, then upper arm, elbow, wrist; the elbow stays bent; the hand travels on an arc; the body sells the move.
- **Uneven timing**: fast commit, slower recovery; holds keep moving slightly.
- Keep neighbouring rotate keys within 180° unless a full spin is the point.

`scripts/motion_keys.py wave` writes looping breath and sway layers (each channel with its own amount, delay and period, wrapped exactly at the seam); `scripts/motion_keys.py chain` writes overlap down loose chains only (tails, hair, capes), never a spine or an acting arm. Pass `--base` with the idle's first-pose values.
