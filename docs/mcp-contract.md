# MCP contract guide

This guide describes the hosted TicketLens MCP contract **2.2.0** at `https://mcp.ticketlens.com/`. Use an MCP client with Streamable HTTP support. Connection examples are in the [README](../README.md#hosted-mcp-quickstart).

This version applies to MCP. The REST API has its own [OpenAPI contract](https://api.ticketlens.com/v1/openapi.json); MCP tool names, envelopes, status values, and `selection_ref` behavior must not be assumed to work as REST requests.

## Discover the current contract

After the MCP initialization handshake:

1. Call `tools/list` to discover tool inputs and available output schemas.
2. Call `resources/read` with `{"uri":"ticketlens://capabilities"}`.
3. Use the returned version, filters, limits, examples, and destination-resolution status when constructing requests.

The resource URI is read through MCP; it is not an HTTP URL. Its contract version is separate from the MCP protocol version and `initialize.serverInfo.version`. Discovery and resource reads do not perform experience searches.

All JSON tool-call examples in this repository's MCP guide are the `params` object of a `tools/call` request. Search, POI, detail, and feedback inputs are nested inside `arguments.payload`. `health_check` takes no arguments.

## Search experiences

Use `search_experiences` for new integrations. Supply at least one of `query`, `destination`, or `poi`. The [basic search example](../examples/mcp/search-experiences.json) searches museum tickets in Paris.

| Field | Supported behavior |
| --- | --- |
| `query` | Experience keywords, up to 500 characters; omit to browse a destination or POI. |
| `destination` | An object containing `destination_id`, or city/country/region context. Use full country and region names that match the content language. |
| `poi` | A landmark `id` from `search_pois`/`get_poi`, or a `name` to resolve. |
| `dates` | ISO `YYYY-MM-DD` values in `from_date` and/or `to_date`. One bound means that exact day; two bounds span at most 31 inclusive days. |
| `price` | Inclusive, nonnegative numeric `min` and/or `max` bounds in EUR. |
| `language` | Content language: `en`, `de`, or `it`; default `en`. This does not filter the language spoken by a tour guide. |
| `currency` | `EUR` only; no implicit currency conversion. |
| `sort` | `relevance` (default), `price_asc`, `price_desc`, or `rating_desc`; sorting is page-local. |
| `page` | Zero-based nonnegative integer; default `0`. |
| `page_size` | Integer from 1 to 50; default `20`. |

Omit unused filters. Empty filter objects, unsupported fields, invalid ranges, and unsupported language/currency values are rejected. This tool does not support tags, category filters, duration filters, group size, private-only filtering, flexible dates, or geographic-radius filtering. `search_pois` has a separate coordinate-based lookup contract.

New clients should use canonical field names. Supported aliases are listed in the capabilities resource and in the input schema's `x-input-aliases`; conflicting aliases are rejected.

For a date range, add this object inside the search payload, replacing the dates with the traveler's dates:

```json
{
  "dates": {"from_date": "2026-12-01", "to_date": "2026-12-03"},
  "price": {"max": 100},
  "sort": "price_asc"
}
```

Longer trips require separate searches with ranges of at most 31 inclusive days.

## Handle results and place ambiguity

`search_experiences` returns `status`, `request_id`, `applied_filters`, `results`, `pagination`, `candidates`, `suggestions`, and `warnings`. The preferred tools expose their result as `structuredContent` and the same JSON in text content.

| Status | Client action |
| --- | --- |
| `ok` | Read `results` and the normalized `applied_filters`. Use `pagination.has_more` to decide whether to request another page. |
| `needs_disambiguation` | Present the available candidate names and context. Once the intended place is selected, invoke its `retry.tool_name` with its complete `retry.arguments`. |
| `no_results` | Check `pagination` and `applied_filters` to distinguish an empty experience search from a place lookup with no match. Offer supplied suggestions without silently changing the traveler's location, dates, or budget. |
| `error` | Inspect `error.code`, `error.status`, `error.retryable`, safe details, and any recovery suggestions. Keep `request_id` when reporting the issue. |

Candidate retries contain a selected authoritative ID and reset pagination. Confidence labels are deterministic labels, not probabilities. Same-name candidates can refer to different IDs; do not choose the first candidate solely because it appears first. Use the available context and ask for clarification when it is insufficient.

If resolution stops before the experience search, `applied_filters` is empty and `pagination` is `null`. A failed location lookup is distinct from an experience search with zero matching offers.

Suggestions that relax filters are marked `verification: "not_tested"`. Other guidance can use `not_applicable`; inspect each suggestion's verification value. Suggested searches are not proof that a particular filter caused the empty result or that the suggested search has inventory.

Unknown optional result fields are omitted. A missing field means the value is unknown, rather than proving a feature or availability is absent. POI IDs identify landmarks; offer IDs identify experiences. Use [get_poi](../examples/mcp/get-poi.json) for a landmark and `get_tour` for an experience.

## Preserve the selected price

The price attached to an offer depends on the search context:

- **No dates:** the catalog's default price, which may differ from the price on the next available day.
- **Exact date:** the price for the requested day.
- **Date range:** the lowest eligible EUR price for that offer among matching records on the current page, after price bounds. This is not a guaranteed minimum across all pages or every date in the requested range.

Price selection happens before presentation sorting. Changing only the sort for the same page and filters does not select a different price record.

Inspect `price_context.basis`, `price_context.selection_scope`, and `price_context.matching_dates`. Matching dates are explicit known dates at the selected price; they do not imply continuous availability between those dates. `first_available` and `second_available` also refer to dates at that selected price, rather than the next dates for the tour at any price. Availability hints are not booking guarantees.

When a result includes `selection_ref`, pass it unchanged to `get_tour` with that result's `id` and the same language. Replace both placeholders below with values from the selected search result:

```json
{
  "name": "get_tour",
  "arguments": {
    "payload": {
      "tour_id": "<result.id>",
      "selection_ref": "<result.selection_ref>",
      "language": "en"
    }
  }
}
```

Without a reference, `get_tour` retrieves the catalog default. With a reference, a missing or changed price/date selection returns an error and requires a fresh search; the server does not silently substitute a default price. Treat the reference as opaque catalog context. It is not an authentication token, reservation, or locked quote. Confirm availability and final pricing at booking.

## Understand sorting and pagination

Price and rating sorts order only the results on the current page. Do not describe the first item of `price_asc` as the cheapest offer in the entire catalog.

The server deduplicates offer IDs within each page, so a page may contain fewer than `page_size` results. The same offer can occur on different pages. `total_hits` counts matching catalog records, rather than globally unique experiences. `total_exact: true` requires consistent pagination metadata and an explicitly exhaustive record count. `total_pages` describes accessible pages and can be capped independently of the count.

`pagination.page_status` can be `in_range`, `out_of_range`, `empty`, or `unknown`. Requesting a page beyond the accessible pages of a nonempty search returns:

- `status: "error"` and `error.code: "PAGE_OUT_OF_RANGE"`;
- the requested page and an empty `results` array, with known totals preserved;
- a recovery suggestion whose retry changes only the page to `0`.

Follow that supplied retry instead of repeating the same invalid page. The server does not silently return page-zero results, and an out-of-range page is not `no_results`.

For suspicious empty later pages, the service may verify counts with one first-page check using the same filters and page size. `counts_verified: true` means this additional check succeeded. Ordinary coherent responses need no additional check, so `false` alone is not a warning. Failed or inconsistent verification returns an error rather than claiming an exact zero.

## Error handling and usage limits

Check the MCP tool result's `isError` and then the applicable tool's response schema. An HTTP 200 response can still contain a tool error. For `search_experiences` and `get_poi`, inspect the typed `status` and structured error. Compatibility tools can return validation/execution errors in text content; do not assume every failure has `structuredContent`.

Use the supplied `retryable` value and any reset/retry timing to decide whether to repeat a request. A corrected request from a recovery suggestion is different from retrying the same request unchanged.

- `PAGE_OUT_OF_RANGE` is non-retryable as submitted; use its page-zero retry.
- `UPSTREAM_CONFIGURATION_ERROR` has semantic status 503 and `retryable: false`. It requires service-operator action. Asking the caller for another API key or repeatedly trying later will not fix the service configuration.
- Quota exhaustion has semantic status 429. Respect the returned reset time and retry delay.

Fair-use limits may change. A validated invocation of `search_experiences`, `get_poi`, `search_tours`, `search_pois`, or `get_tour` that reaches the search backend consumes at most one meaningful-operation quota unit. Internal resolution or count-verification work does not add units within that invocation. Repeating an invocation can consume another unit. Discovery, resource reads, passive health checks, feedback, and input validation rejected before search do not consume this semantic quota; other transport protections can still apply.

When reporting a failure, include its `request_id` and a concise reproduction. Use the [repository issue tracker](https://github.com/ticketlens/ticketlens-experiences-mcp/issues) or the documented `submit_feedback` tool.

## Existing integrations

`search_tours`, `search_pois`, `get_tour`, `health_check`, and `submit_feedback` remain available. No removal date is scheduled for `search_tours`; new integrations should prefer `search_experiences`.

The existing tools retain their own envelopes. For example, MCP `search_tours` uses `languages` and `hits_per_page`, while `search_experiences` uses `language` and `page_size`. Inspect `tools/list` for the tool you call. The public REST examples use a separate API contract, including `per_page`; do not substitute MCP request shapes into them.
