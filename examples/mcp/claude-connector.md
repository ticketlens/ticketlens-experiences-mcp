# Claude remote connector

Use the hosted TicketLens MCP server as a remote connector in Claude.

1. Open Claude and go to `Settings > Connectors`.
2. Choose the option to add a custom connector.
3. Set the connector URL to `https://mcp.ticketlens.com/`.
4. Save the connector, then enable the TicketLens tools in Claude.

Notes:

- Claude remote connectors are added from the Claude UI.
- `claude_desktop_config.json` is not the right place for remote MCP URLs.
- The public TicketLens MCP server currently does not require additional auth headers in the connector setup.
