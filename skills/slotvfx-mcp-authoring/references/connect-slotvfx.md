# Connect SlotVFX to Claude Code

The SlotVFX skills need the SlotVFX editor tools (named `slotfx_...`). Those tools come from SlotVFX Desktop 0.9.64 or newer, running on the same computer with **Connect AI** turned on. The full SlotVFX plugin starts the connection itself. The skills-only SlotVFX plugin from Anthropic's plugin directory has no connection, so it is added once with one command (step 4).

If no `slotfx_` tools are available at all, say plainly that SlotVFX isn't connected yet, and don't attempt the work. Then help the user step by step. Ask before running any command, and never ask the user to paste tokens or keys into the chat.

1. Check that SlotVFX Desktop 0.9.64 or newer is installed and open, with Connect AI turned on. If it isn't installed, it is at https://slotvfx.com.
2. Ask the user to run `/mcp` in Claude Code and say whether a server named SlotVFX is listed.
3. **SlotVFX is listed but failed:** ask for the error it shows. With the full plugin on macOS, a missing `node` is the usual cause: install the LTS version from https://nodejs.org, then restart Claude Code.
4. **SlotVFX is not listed:** the connection isn't installed (usually the skills-only plugin from Anthropic's directory). Add it with one terminal command for SlotVFX in its default folder:
   - macOS, if `/Applications/SlotVFX.app/Contents/Resources/mcp/slotvfx-mcp` exists:
     `claude mcp add --scope user SlotVFX /Applications/SlotVFX.app/Contents/Resources/mcp/slotvfx-mcp`
   - macOS, older SlotVFX without that file:
     `claude mcp add --scope user --env=ELECTRON_RUN_AS_NODE=1 SlotVFX /Applications/SlotVFX.app/Contents/MacOS/SlotVFX /Applications/SlotVFX.app/Contents/Resources/mcp/adapter/server/slotfxMcpServer.mjs`
   - Windows, in PowerShell:
     `claude mcp add --scope user --env=ELECTRON_RUN_AS_NODE=1 SlotVFX "$env:LOCALAPPDATA\Programs\SlotVFX\SlotVFX.exe" "$env:LOCALAPPDATA\Programs\SlotVFX\resources\mcp\adapter\server\slotfxMcpServer.mjs"`
   - Windows, in Command Prompt: the same command with `%LOCALAPPDATA%` in place of `$env:LOCALAPPDATA`.

   Keep `--env=...` before the name `SlotVFX` exactly as written. For SlotVFX in another folder, replace the paths with that folder. These commands only point Claude Code at the MCP server that ships inside SlotVFX; nothing is downloaded.

   Then check with `claude mcp get SlotVFX` while SlotVFX is open: it should say Connected. If it doesn't, remove it with `claude mcp remove SlotVFX -s user` and try the other macOS command. Restart Claude Code and run `slotfx_get_app_state` to confirm.

   If the `claude` command isn't found (for example in the Claude desktop app's Code tab), create a `.mcp.json` file in the project folder instead, with the same command and arguments, and approve it when Claude Code asks. For the first macOS case: `{"mcpServers": {"SlotVFX": {"command": "/Applications/SlotVFX.app/Contents/Resources/mcp/slotvfx-mcp", "args": []}}}`. For the other cases, put the paths in `command` and `args` and add `"env": {"ELECTRON_RUN_AS_NODE": "1"}`.
5. Use only one SlotVFX connection at a time. If the SlotVFX tools show up twice (for example from the SlotVFX extension in the Claude desktop app as well), remove one of them.
