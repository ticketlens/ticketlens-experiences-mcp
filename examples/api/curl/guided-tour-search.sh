#!/usr/bin/env bash
set -euo pipefail

curl -sS https://api.ticketlens.com/v1/search/tours \
  -H 'content-type: application/json' \
  -d '{
    "query": "guided walking tour",
    "city": "Rome",
    "languages": ["en"],
    "per_page": 5
  }'
