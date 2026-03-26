#!/usr/bin/env bash
set -euo pipefail

curl -sS https://api.ticketlens.com/v1/search/tours \
  -H 'content-type: application/json' \
  -d '{
    "query": "hop on hop off bus",
    "city": "London",
    "languages": ["en"],
    "per_page": 5
  }'
