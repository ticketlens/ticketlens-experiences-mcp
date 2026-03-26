#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import urllib.request

API_BASE_URL = os.environ.get("TICKETLENS_API_BASE_URL", "https://api.ticketlens.com/v1")

SEARCH_EXAMPLES = [
    {
        "name": "attraction-ticket",
        "payload": {
            "query": "museum ticket",
            "city": "Paris",
            "languages": ["en"],
            "per_page": 5,
        },
    },
    {
        "name": "hop-on-hop-off",
        "payload": {
            "query": "hop on hop off bus",
            "city": "London",
            "languages": ["en"],
            "per_page": 5,
        },
    },
    {
        "name": "football-ticket-search",
        "payload": {
            "query": "Arsenal",
            "city": "London",
            "languages": ["en"],
            "per_page": 5,
        },
    },
    {
        "name": "guided-tour",
        "payload": {
            "query": "guided walking tour",
            "city": "Rome",
            "languages": ["en"],
            "per_page": 5,
        },
    },
]


def post_json(path: str, payload: dict) -> tuple[int, dict]:
    request = urllib.request.Request(
        f"{API_BASE_URL}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body)


for example in SEARCH_EXAMPLES:
    status, data = post_json("/search/tours", example["payload"])
    items = data.get("items", [])
    first_title = items[0]["title"] if items else "(no results)"
    print(f"\n[{example['name']}] status={status}")
    print(first_title)


poi_status, poi_data = post_json(
    "/search/pois",
    {
        "query": "Eiffel Tower",
        "city": "Paris",
        "language": "en",
        "limit": 5,
    },
)

print(f"\n[poi-search] status={poi_status}")
print(json.dumps(poi_data, indent=2))
