---
name: slotvfx-dev-reports
description: "Draft actionable SlotVFX bug reports and evaluate developer replies using minimal reproductions, versioned evidence and clear editor/runtime boundaries. Correct unsupported findings and track workarounds without sending reports unless authorized."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Reporting SlotVFX issues

Prepare a local report unless the user explicitly asked to send it or update an external tracker. Reading a developer reply or discovering a defect does not authorize messages, issue creation or publication. Use the existing authorized backlog when one exists; do not create a new reporting system for every small edit.

Located defects with evidence get fixed; in one round such a backlog had 18 items fixed in a day. A confident wrong item costs the developer more than a missing one and devalues every true item beside it.

## Make each finding reproducible

Include:

1. A concrete trigger, expected result and actual result, with measurements where useful: "the hit landed 409 px from B" beats "impacts are off".
2. Exact app/MCP/runtime versions, engine target and relevant environment.
3. A small reproduction: necessary settings, timeline times, instance setup and assets or IDs resolved from the project. Exclude secrets and unrelated data.
4. Evidence scope: schema checked, source inspected, editor measured, recorder measured or target runtime measured. Developers sort their replies by this distinction.
5. A likely cause only when supported. Separate hypotheses from demonstrated causes. With source available, naming the line does more than description, for example an early return before the branch that handles the case, or a lookup against a store that is empty in ordinary exports.
6. A suggested fix or investigation, plus any workaround already used and how to remove it when fixed. Say when the data the fix needs is already present: "the pool slot already maps the template id to the running copy's id" turns a report into a patch.

Reference source against a known commit or artifact and note local modifications; check `git status` before quoting line numbers. A line reference only helps against the tree the developer opens, so say when the runtime was patched locally or exported data was hand-edited. Prefer a clean baseline for upstream claims, but do not discard the user's work to obtain one. Generated data and runtime outputs can be overwritten on export, so prefer changes in their authoring source; explicit authorized patches remain legitimate and should be documented.

## Exclude test mistakes

Frame captures generously before concluding nothing drew. Check clip membership, visibility, current selection, actual instance IDs and coordinate spaces. Read current recorder and lifetime rules before calling behavior a parity bug. A field name used differently by two engines is only a lead; run the relevant cases before claiming divergence.

Testing errors that were filed as defects: a render frame too small to contain the effect, reported as "not drawn anywhere"; a recorder asked to simulate past a clip's end, reported as a parity bug; and a divergence read off field names. In that last case one runtime's `p.vx` was its direction vector, updated from real movement like the editor's, so the divergence did not exist and the runtime that really had the bug went unnamed. Before filing, ask whether the tool is doing what it documents and the question was wrong; that accounted for two withdrawn items in one day.

Compare the same data, times and seeds where possible. Reproduce a second way when the initial measurement is indirect. If a test cannot be run, state that limit rather than filling the gap with certainty.

## Handle replies with evidence

Retest claimed fixes within the authorized scope. Distinguish confirmed fixes (with the numbers), source changes that miss the failing case (with the reason) and partial fixes (say which half: one item had `duplicate_entity` fixed while `create_layers` was still broken). Check stale-connector explanations before repeating them; in one case the connector had already restarted itself. Incorporate corrections to the original report, including wrong engine attribution or overbroad claims.

Review related workarounds in the affected project's notes. Do not automatically edit other projects or handoffs beyond the current authorization. If a lifetime or API change alters the game integration, explain the practical consequence and update the relevant authorized documentation.

When a finding was incorrect, correct or withdraw it in the local report with what was actually observed and why the original reading was wrong. Withdraw a finding when it no longer reproduces under its original conditions on the build in question. A non-reproduction under different conditions is not enough to erase a previously demonstrated issue. A marginal item can come off the developer's fix list while its measurement stays in your own build notes. If an external correction is needed but sending is not authorized, prepare it for the user.

Answer a developer's technical question with a bounded test rather than reasoning, when possible. Provide the useful measured fields or a small log excerpt, such as the relevant `get_entity_values` fields, the count at the time they named or the asset fields, not full raw dumps containing credentials, base64 or unrelated project data. Name any testing limitation explicitly.
