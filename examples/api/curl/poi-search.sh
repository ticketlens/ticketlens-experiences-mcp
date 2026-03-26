#!/usr/bin/env bash
set -euo pipefail

curl -sS https://api.ticketlens.com/v1/search/pois \
  -H 'content-type: application/json' \
  -d '{
    "query": "Eiffel Tower",
    "city": "Paris",
    "language": "en",
    "limit": 5
  }'
