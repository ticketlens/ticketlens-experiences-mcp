# OpenClaw integration

TicketLens can be integrated into OpenClaw most easily as a workspace skill that calls the public TicketLens REST API.

## Option 1: workspace skill via the public API

This is the recommended OpenClaw path because it works across OpenClaw backends and follows OpenClaw's documented skill model directly.

Setup:

1. Copy `examples/openclaw/skills/ticketlens-api/` into your OpenClaw workspace under `skills/ticketlens-api/`, or into `~/.openclaw/skills/ticketlens-api/` for a shared local install.
2. Start a new OpenClaw session, or refresh skills if your setup watches the workspace skill directory.
3. Ask for destination experiences in natural language, for example:
   - `Find Eiffel Tower tickets in Paris this weekend`
   - `Search hop-on hop-off buses in Barcelona`
   - `Look up football tickets in London next Friday`

Notes:

- This skill assumes the agent can use a runtime shell tool such as `exec` or `bash`.
- The included skill uses the public TicketLens API with `curl`, so `curl` must be available on the OpenClaw host.
- If the user names a landmark or attraction, the skill resolves the POI first and then searches experiences against that POI.

## MCP note

OpenClaw's bundle docs currently describe MCP support around supported `stdio` servers launched as subprocesses. The public TicketLens MCP server is hosted remotely at `https://mcp.ticketlens.com/`, so the API skill above is the clearest "works today" integration path.

If you want MCP semantics inside OpenClaw, the more advanced path is to build either:

- a native OpenClaw plugin that exposes TicketLens tools directly, or
- a local `stdio` bridge that proxies to the hosted TicketLens MCP endpoint.

OpenClaw's ACP bridge docs also say per-session `mcpServers` are unsupported, so this is not a per-chat MCP setup path.

## Relevant OpenClaw docs

- [Creating Skills](https://docs.openclaw.ai/tools/creating-skills)
- [Skills](https://docs.openclaw.ai/skills)
- [Plugin Bundles](https://docs.openclaw.ai/plugins/bundles)
- [ACP bridge compatibility](https://docs.openclaw.ai/cli/acp)
