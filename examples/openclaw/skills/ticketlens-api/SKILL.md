---
name: ticketlens_api
description: Search TicketLens destination experiences and resolve POIs via the public TicketLens REST API.
homepage: https://www.ticketlens.com/en
metadata: {"openclaw":{"requires":{"bins":["curl"]}}}
---

# TicketLens API

Use this skill when the user wants tours, attraction tickets, hop-on hop-off buses, sports tickets, event tickets, or other destination experiences from TicketLens.

## Behavior

- Prefer the public TicketLens REST API:
  - `POST https://api.ticketlens.com/v1/search/pois`
  - `POST https://api.ticketlens.com/v1/search/tours`
  - `GET https://api.ticketlens.com/v1/tours/{tour_id}`
- If the user mentions a landmark, museum, stadium, or attraction, resolve the POI first with `search/pois`, then use the returned POI ID in `search/tours`.
- For date-specific requests, include a `dates` object with ISO `YYYY-MM-DD` values.
- Default to `per_page: 5` unless the user asks for more results.
- Summarize the best matches with title, city, price, rating, first availability, and booking URL when available.
- If the request is too ambiguous, ask one short follow-up question.

## Execution

- Use a runtime shell tool such as `exec` or `bash`.
- Use `curl -sS` and set `content-type: application/json`.
- Keep requests focused and avoid broad unbounded searches when the user gives enough context to filter by city, POI, or dates.
- If runtime shell tools are not available in the current OpenClaw agent profile, tell the user that this skill needs `exec` or `bash`, or suggest a native OpenClaw plugin or local `stdio` bridge when the deployment needs MCP-style tools instead.

## Example POI resolution

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

## Example experience search

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
