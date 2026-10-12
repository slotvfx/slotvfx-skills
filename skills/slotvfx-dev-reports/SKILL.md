---
name: slotvfx-dev-reports
description: "Draft actionable SlotVFX bug reports and evaluate developer replies using minimal reproductions, versioned evidence and clear editor/runtime boundaries. Correct unsupported findings and track workarounds without sending reports unless authorized."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Reporting SlotVFX issues

Prepare a local report unless the user explicitly asked to send it or update an external tracker. Reading a developer reply or discovering a defect does not authorize messages, issue creation or publication. Use the existing authorized backlog when one exists; do not create a new reporting system for every small edit.

## Make each finding reproducible

Include:

1. A concrete trigger, expected result and actual result, with measurements where useful.
2. Exact app/MCP/runtime versions, engine target and relevant environment.
3. A small reproduction: necessary settings, timeline times, instance setup and assets or IDs resolved from the project. Exclude secrets and unrelated data.
4. Evidence scope: schema checked, source inspected, editor measured, recorder measured or target runtime measured.
5. A likely cause only when supported. Separate hypotheses from demonstrated causes.
6. A suggested fix or investigation, plus any workaround already used and how to remove it when fixed.

Reference source against a known commit or artifact and note local modifications. Prefer a clean baseline for upstream claims, but do not discard the user's work to obtain one. Generated data and runtime outputs can be overwritten on export, so prefer changes in their authoring source; explicit authorized patches remain legitimate and should be documented.

## Exclude test mistakes

Frame captures generously before concluding nothing drew. Check clip membership, visibility, current selection, actual instance IDs and coordinate spaces. Read current recorder and lifetime rules before calling behavior a parity bug. A field name used differently by two engines is only a lead; run the relevant cases before claiming divergence.

Compare the same data, times and seeds where possible. Reproduce a second way when the initial measurement is indirect. If a test cannot be run, state that limit rather than filling the gap with certainty.

## Handle replies with evidence

Retest claimed fixes within the authorized scope. Distinguish confirmed fixes, source changes that miss the failing case, and partial fixes. Check stale-connector explanations before repeating them. Incorporate corrections to the original report, including wrong engine attribution or overbroad claims.

Review related workarounds in the affected project's notes. Do not automatically edit other projects or handoffs beyond the current authorization. If a lifetime or API change alters the game integration, explain the practical consequence and update the relevant authorized documentation.

When a finding was incorrect, correct or withdraw it in the local report with what was actually observed. If an external correction is needed but sending is not authorized, prepare it for the user. A non-reproduction under different conditions is not enough to erase a previously demonstrated issue.

Answer a developer's technical question with a bounded test when possible. Provide the useful measured fields or a small log excerpt, not full raw dumps containing credentials, base64 or unrelated project data. Name any testing limitation explicitly.
