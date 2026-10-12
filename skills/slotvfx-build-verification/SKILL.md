---
name: slotvfx-build-verification
description: "Verify a SlotVFX update or reported fix against explicit reproduction cases. Check installed MCP compatibility, test editor and runtime behavior separately, run fair before/after comparisons and update authorized local findings."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Verifying a SlotVFX build

Use this skill when asked to assess an update or reproduce specific issues. Confirming an installed version, reading a fix and demonstrating that fix are different results. Do not expand an ordinary visual task into a complete engine audit.

## Check the environment

Inspect `get_bridge_status`, installed app/server versions and contract fingerprints. A mismatch signals possible incompatibility, not certainty that every write is unsafe or every tool works. Recheck current schemas and read-only calls; use a supported dry run to assess an intended write without committing it. Resolve relevant incompatibilities before mutation. Consider unsaved work before any restart.

“Renderer bridge is not ready” can indicate no open project, startup or a disconnected renderer. Inspect available state before diagnosing it. Registry tools may work while project tools do not.

## Identify the exact claim and code

Read the authorized backlog/release notes or supplied developer reply. If a source repository is available, inspect relevant commits and diffs against a known baseline. Do not assume access to source, invent a release ref or upload a source tree to another environment.

Record app/runtime version, commit or artifact hash, target engine and local modifications. A dirty tree does not invalidate every observation, but a fair stock comparison needs a clean baseline or an explicit patch record. Never reset the user's changes to obtain one.

Use an exported runtime from the matching installed build when possible. If source-based extraction is necessary, inspect its actual exports and use a compatible local toolchain. The supplied pack's `PIXI_RUNTIME_TEMPLATE` location is a historical clue, not a guaranteed path. Do not copy macOS dependencies into Linux or assume a cloud container is required. Confirm the extracted artifact contains the intended change before testing it.

## Run a bounded reproduction

Keep before/after runtimes separate. Use identical project data, seed, scene, frame count, warm-up and copy counts. Test the case that originally failed, including ordinary branches that an early return or empty store could bypass.

Use an existing harness or create a small local one if necessary; this pack supplies no harness. Manage any local server through its own process/session ID and stop only that task-owned process. Never use broad `pkill` patterns to clear servers.

Label hardware/browser/rendering mode. Software-GPU timings may not predict device rendering cost. CPU updates, draw calls, uploads and counts still need controlled conditions; player FPS claims need representative hardware.

## Test MCP and runtime independently

MCP writes, defaults and membership can be checked in an editor project. Runtime facing, lifetime, pooling and engine integration require the actual exported runtime. Editor captures do not establish engine parity.

Use an isolated test project or explicitly task-owned temporary groups within the authorized audit. Snapshot original membership/state first. Avoid adding test objects to the user's active production work when an isolated reproduction suffices. Remove only disposable objects created for this test, check references and restore the original project state where appropriate.

For each item, classify evidence clearly:

- Version/schema checked.
- Source inspected; behavioral hypothesis remains.
- Reproduced in the editor or recorder.
- Reproduced in a named runtime/environment.
- Fixed or partly fixed under the stated test.

## Update findings responsibly

Update authorized local notes with measured results, unresolved cases and obsolete workarounds. If a previous finding was wrong, correct it plainly and retain enough history to explain the change. Do not silently turn a failed reproduction into proof the bug never existed.

Use the [developer report skill](../slotvfx-dev-reports/SKILL.md) for a concise evidence-based report. Draft locally unless the user explicitly authorized sending it or posting a backlog update. Testing authority does not by itself authorize publishing or altering unrelated game projects.
