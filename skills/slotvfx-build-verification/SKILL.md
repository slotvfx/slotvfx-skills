---
name: slotvfx-build-verification
description: "Verify a SlotVFX update or reported fix against explicit reproduction cases. Check installed MCP compatibility, test editor and runtime behavior separately, run fair before/after comparisons and update authorized local findings."
---

Use the bundled [current workflow guide](references/workflows.md) for SlotVFX desktop review, tool routes, recovery and delivery contract. Older version-specific observations below are historical leads; inspect the running app’s schemas before relying on them. Review editable results in SlotVFX by activating the intended clip, framing/selecting the effect and playing it naturally. Save, record, export, publish or send reports only within the user’s request.

# Verifying a SlotVFX build

Use this skill when asked to assess an update or reproduce specific issues. Confirming an installed version, reading a fix and demonstrating that fix are different results; say which one you did. A commit or release note saying an item is fixed is a claim to test: in one round, two claimed fixes did not reach the case that mattered. Do not expand an ordinary visual task into a complete engine audit.

## Check the environment

Inspect `get_bridge_status`, installed app/server versions and contract fingerprints. On 0.9.59 it returns `compatibility: {compatible, level, warnings, errors}` plus contract fingerprints and versions for both sides (an earlier build exposed them as `contractFingerprint` on the bridge and on `mcpServer`, and `mcpServer.version`). The reported server version is the cheapest check that a claimed build is installed. A mismatch signals possible incompatibility, not certainty that every write is unsafe or every tool works. Recheck current schemas and read-only calls; use a supported dry run to assess an intended write without committing it. Resolve relevant incompatibilities before mutation. Consider unsaved work before any restart; on an earlier build the connector picked up a new version when the desktop app reloaded, so re-check status before asking for a restart.

“Renderer bridge is not ready” can indicate no open project, startup or a disconnected renderer. Inspect available state before diagnosing it. Registry tools (`find_features`, `list_features`) may work while project tools do not. On an earlier build `get_project_summary` returned it whenever no project was open, so check for an open project before reporting a broken connector.

## Identify the exact claim and code

Read the authorized backlog/release notes or supplied developer reply. If a source repository is available, inspect relevant commits and diffs against a known baseline (for example `git log --oneline <baseline>..HEAD`, `git show --stat`, then the diff of each relevant file) and map each commit to the backlog items it claims. Do not assume access to source, invent a release ref or upload a source tree to another environment.

Record app/runtime version, commit or artifact hash, target engine and local modifications. A dirty tree does not invalidate every observation, but a fair stock comparison needs a clean baseline or an explicit patch record. Never reset the user's changes to obtain one.

Use an exported runtime from the matching installed build when possible. If source-based extraction is necessary, inspect its actual exports and use a compatible local toolchain. In a SlotVFX source checkout (0.9.59) the Pixi runtime is the exported const `PIXI_RUNTIME_TEMPLATE` in `utils/pixi/pixiRuntimeTemplate.ts`; verify the path in your checkout. Import that module with a TypeScript runner and write the const to a versioned file. On an earlier build it could not be recovered from `dist/assets/*.js`: it is stitched from several chunks and is larger than any one bundle file. Do not copy macOS dependencies into Linux (native packages such as esbuild fail with a platform mismatch) or assume a cloud container is required. Confirm the extracted artifact contains the intended change before testing it, for example by comparing `grep -c` counts of a symbol the new build introduced against the previous runtime.

## Run a bounded reproduction

Keep before/after runtimes separate, as files, and swap the one the harness page loads. Use identical project data, seed, scene, frame count, warm-up and copy counts; changing warm-up alone changes particle populations. Test the case that originally failed, including ordinary branches that an early return or empty store could bypass.

Use an existing harness or create a small local one if necessary; this pack supplies no harness. Manage any local server through its own process/session ID and stop only that task-owned process, by its own PID. Where background processes do not survive between tool calls, start the server in the same call as the test run. Never use broad `pkill` patterns to clear servers: `pkill -f "http.server"` also matches the calling shell's own command line and kills it.

Label hardware/browser/rendering mode. Software-GPU render timings are unreliable and may not predict device rendering cost (the same scene measured 19 ms vs 2.5 ms on an earlier build). Update ms, draw calls, buffer uploads, GL call counts and particle counts are steadier but still need controlled conditions; player FPS claims need representative hardware.

## Test MCP and runtime independently

MCP writes, defaults and membership can be checked in an editor project. Runtime facing, spin direction, lifetime, pooling and engine integration require the actual exported runtime. Editor captures do not establish engine parity. A round done entirely through the MCP has verified the project, not the engine; state that boundary in the report, and lead with it when asked whether something is verified.

Use an isolated test project or explicitly task-owned temporary groups within the authorized audit, named with an obvious prefix. Snapshot original membership/state first. Avoid adding test objects to the user's active production work when an isolated reproduction suffices. Remove only disposable objects created for this test, check references, confirm clip membership matches the snapshot before saving and restore the original project state where appropriate.

For each item, classify evidence clearly:

- Version/schema checked.
- Source inspected; behavioral hypothesis remains.
- Reproduced in the editor or recorder.
- Reproduced in a named runtime/environment.
- Fixed or partly fixed under the stated test.

Measured claims carry numbers; mark source-only items, for example `(code)`.

## Update findings responsibly

Update authorized local notes with measured results, unresolved cases and obsolete workarounds. If a previous finding was wrong, correct it plainly and retain enough history to explain the change. Do not silently turn a failed reproduction into proof the bug never existed.

Project audits follow the same rule. An audit built on a formula rather than a measurement produces confident wrong numbers, and changes made on them. Check the formula against one rendered case before acting on it; a formula that only errs in one direction can give the right conclusion for the wrong reason, which is not verification.

Use the [developer report skill](../slotvfx-dev-reports/SKILL.md) for a concise evidence-based report. Draft locally unless the user explicitly authorized sending it or posting a backlog update. Testing authority does not by itself authorize publishing or altering unrelated game projects.
