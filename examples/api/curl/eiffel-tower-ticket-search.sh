#!/usr/bin/env bash
set -euo pipefail

# Step 1: resolve the Eiffel Tower to a canonical TicketLens POI.
curl -sS https://api.ticketlens.com/v1/search/pois \
  -H 'content-type: application/json' \
  -d '{
    "query": "Eiffel Tower",
    "city": "Paris",
    "language": "en",
    "limit": 5
  }'

# Step 2: search for Eiffel Tower tickets using the POI id from the first response.
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
