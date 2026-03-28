# TicketLens Experiences MCP

Official remote MCP server and REST API for discovering tours, tickets, attractions, and activities with TicketLens.

TicketLens provides a public hosted remote MCP server at `https://mcp.ticketlens.com/` and a versioned REST API at `https://api.ticketlens.com/v1` for AI travel planners, destination discovery flows, and custom integrations. The same hosted inventory covers guided tours, attraction tickets, hop-on hop-off buses, sports tickets, and other event tickets.

Main website: [www.ticketlens.com/en](https://www.ticketlens.com/en)

## What TicketLens is

- The official TicketLens remote MCP + REST surface for destination experiences.
- A developer-facing search surface for destination experiences.
- Available as both MCP and REST on the same hosted inventory.
- Designed for AI assistants, travel planning tools, destination discovery flows, and custom integrations.

## Why it fits AI agents

- Hosted remote MCP server with a public URL for quick connector setup and evaluation.
- Public REST fallback on the same inventory for clients that are not using MCP yet.
- Broad destination-experiences coverage across tours, attraction tickets, hop-on hop-off buses, sports tickets, and events.

## What the current API/MCP returns

The public `tour`-named tools and endpoints return a broader destination-experiences catalog, not just guided tours.

`search_tours` and `POST /v1/search/tours` can return:

- guided tours
- attraction and museum tickets
- hop-on hop-off bus products
- sports tickets
- event and admission products

Current public MCP tools:

- `search_tours`
- `search_pois`
- `get_tour`
- `health_check`

Current public REST endpoints:

- `POST /v1/search/tours`
- `GET /v1/tours/{tour_id}`
- `POST /v1/search/pois`
- `GET /v1/pois/{poi_id}`
- `GET /v1/livez`
- `GET /v1/readyz`
- `GET /v1/health`
- `GET /v1/openapi.json`
- `GET /v1/docs`
- `GET /v1/redoc`

## Hosted MCP quickstart

Hosted MCP URLs:

- Base URL: `https://mcp.ticketlens.com/`
- Canonical server card: `https://mcp.ticketlens.com/.well-known/mcp/server-card.json`
- Compatibility alias: `https://mcp.ticketlens.com/.well-known/mcp.json`

### Codex

Add the hosted server from the CLI:

```bash
codex mcp add ticketlens-experiences --url https://mcp.ticketlens.com/
```

If you manage Codex MCP servers through config files, start from [examples/mcp/codex-config.toml](examples/mcp/codex-config.toml).

### Cursor

Add the hosted MCP URL to your Cursor MCP config. A ready-to-copy example is in [examples/mcp/cursor-mcp.json](examples/mcp/cursor-mcp.json).

### Claude

Claude remote MCP connectors are added from the UI, not through `claude_desktop_config.json`. Use the hosted URL `https://mcp.ticketlens.com/` in `Settings > Connectors`, or follow the short guide in [examples/mcp/claude-connector.md](examples/mcp/claude-connector.md).

### OpenClaw

OpenClaw users can integrate TicketLens quickly by adding a workspace skill that calls the public TicketLens REST API. Start from [examples/openclaw/skills/ticketlens-api/SKILL.md](examples/openclaw/skills/ticketlens-api/SKILL.md).

See [examples/openclaw/README.md](examples/openclaw/README.md) for the recommended API path and notes about the more advanced MCP route.

## Hosted API quickstart

Hosted API URLs:

- Base URL: `https://api.ticketlens.com/v1`
- OpenAPI JSON: `https://api.ticketlens.com/v1/openapi.json`
- Swagger UI: `https://api.ticketlens.com/v1/docs`
- ReDoc: `https://api.ticketlens.com/v1/redoc`
- Committed artifact: [openapi/ticketlens-tour-search-api.v1.json](openapi/ticketlens-tour-search-api.v1.json)

The hosted examples below use the public HTTPS endpoints directly and do not require extra headers in the current public setup.

Step 1: resolve the Eiffel Tower to a canonical TicketLens POI:

```bash
curl -sS https://api.ticketlens.com/v1/search/pois \
  -H 'content-type: application/json' \
  -d '{
    "query": "Eiffel Tower",
    "city": "Paris",
    "language": "en",
    "limit": 5
  }'
```

Step 2: search for Eiffel Tower tickets using the POI from step 1:

```bash
curl -sS https://api.ticketlens.com/v1/search/tours \
  -H 'content-type: application/json' \
  -d '{
    "query": "ticket",
    "poi": {
      "id": "660851",
      "match_mode": "exact"
    },
    "city": "Paris",
    "languages": ["en"],
    "per_page": 5
  }'
```

For destination-specific ticketing flows like the Eiffel Tower, this is useful for agents because TicketLens can surface inventory from the official Eiffel Tower site, including hard-to-find high-season availability when it exists, alongside second-market ticket options in the same search flow.

To filter for travel dates, add a `dates` object with ISO `YYYY-MM-DD` values:

```bash
curl -sS https://api.ticketlens.com/v1/search/tours \
  -H 'content-type: application/json' \
  -d '{
    "query": "ticket",
    "poi": {
      "id": "660851",
      "match_mode": "exact"
    },
    "city": "Paris",
    "dates": {
      "from_date": "2026-05-15",
      "to_date": "2026-05-17"
    },
    "languages": ["en"],
    "per_page": 5
  }'
```

Date filtering notes:

- Use `dates.from_date` for a single-day search.
- Use both `dates.from_date` and `dates.to_date` for a date range.
- Dates must use ISO `YYYY-MM-DD`.
- `dates.flexible_days` exists in the schema but is not implemented in the current public version.

## MCP tool reference

| Tool | What it does |
| --- | --- |
| `search_tours` | Search destination experiences across tours, attraction tickets, hop-on hop-off buses, sports tickets, event tickets, and other activities. |
| `search_pois` | Resolve POIs and aliases before calling `search_tours`. |
| `get_tour` | Fetch detail for an experience returned by `search_tours`. |
| `health_check` | Return dependency-aware service health. |

## API endpoint reference

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/v1/search/tours` | Search destination experiences, including tours, attraction tickets, hop-on hop-off buses, sports tickets, event tickets, and other activities. |
| `GET` | `/v1/tours/{tour_id}` | Fetch detail for an experience returned by `/v1/search/tours`. |
| `POST` | `/v1/search/pois` | Resolve points of interest before filtering search. |
| `GET` | `/v1/pois/{poi_id}` | Fetch a canonical POI record by ID. |
| `GET` | `/v1/livez` | Process liveness check. |
| `GET` | `/v1/readyz` | Readiness check for infra and search dependencies. |
| `GET` | `/v1/health` | Richer human-facing diagnostic health. |

## Examples by experience type

Ready-to-run `curl` examples:

- Eiffel Tower ticket discovery
- hop-on hop-off bus discovery
- football ticket discovery
- classic guided tour discovery

- [examples/api/curl/eiffel-tower-ticket-search.sh](examples/api/curl/eiffel-tower-ticket-search.sh)
- [examples/api/curl/hop-on-hop-off-search.sh](examples/api/curl/hop-on-hop-off-search.sh)
- [examples/api/curl/football-ticket-search.sh](examples/api/curl/football-ticket-search.sh)
- [examples/api/curl/guided-tour-search.sh](examples/api/curl/guided-tour-search.sh)
- [examples/api/curl/poi-search.sh](examples/api/curl/poi-search.sh)

General API client examples:

- [examples/api/javascript/search_experiences.mjs](examples/api/javascript/search_experiences.mjs)
- [examples/api/python/search_experiences.py](examples/api/python/search_experiences.py)

## FAQ

### Why is the endpoint called tours if it returns tickets too?

The public `tour`-named tools and endpoints cover destination experiences more broadly, so `search_tours` and `POST /v1/search/tours` can return guided tours, attraction tickets, hop-on hop-off buses, sports tickets, event tickets, and other bookable activities.

## Access, limits, and support

- The hosted MCP and API are public and intended for developer evaluation and integration.
- Fair-use and abuse-protection limits may apply.
- Open a GitHub issue for broken examples, stale docs, or integration gaps.

## Maintenance

This repository is a curated public mirror of documentation, examples, and exported API artifacts. Runtime source remains internal and public-facing artifacts are refreshed from the private source of truth.
