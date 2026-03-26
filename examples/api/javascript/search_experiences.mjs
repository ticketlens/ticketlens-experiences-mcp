#!/usr/bin/env node

const apiBaseUrl = process.env.TICKETLENS_API_BASE_URL || "https://api.ticketlens.com/v1";

const searchExamples = [
  {
    name: "attraction-ticket",
    payload: {
      query: "museum ticket",
      city: "Paris",
      languages: ["en"],
      per_page: 5
    }
  },
  {
    name: "hop-on-hop-off",
    payload: {
      query: "hop on hop off bus",
      city: "London",
      languages: ["en"],
      per_page: 5
    }
  },
  {
    name: "football-ticket-search",
    payload: {
      query: "Arsenal",
      city: "London",
      languages: ["en"],
      per_page: 5
    }
  },
  {
    name: "guided-tour",
    payload: {
      query: "guided walking tour",
      city: "Rome",
      languages: ["en"],
      per_page: 5
    }
  }
];

async function postJson(path, payload) {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    method: "POST",
    headers: {
      "content-type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();
  return { status: response.status, data };
}

for (const example of searchExamples) {
  const { status, data } = await postJson("/search/tours", example.payload);
  const firstTitle = data.items && data.items.length > 0 ? data.items[0].title : "(no results)";
  console.log(`\n[${example.name}] status=${status}`);
  console.log(firstTitle);
}

const poiLookup = await postJson("/search/pois", {
  query: "Eiffel Tower",
  city: "Paris",
  language: "en",
  limit: 5
});

console.log(`\n[poi-search] status=${poiLookup.status}`);
console.log(JSON.stringify(poiLookup.data, null, 2));
