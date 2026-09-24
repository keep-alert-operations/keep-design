# Alert operations

Native v1/v2 inputs, logical identity, admission, lifecycle, history and alert APIs. Shared execution and storage are specified in [Alerts and history technical design](./spec-alert-history-technical.md).

## Input and normalized fields

### Native field inventory

Only the fields in this table are accepted in customer alert objects. Every supplied value is a nonblank string. “Required” means the field must occur in every delivery; “optional” permits omission, not null. Generated fields are never accepted as source input.

| Field | V1 | V2 | Meaning / accepted values |
|---|---|---|---|
| `application` | Required | Required | Application identifier. |
| `object` | Required | Rejected | V1 component; maps to managed `component`. |
| `component` | Rejected | Required | Component identifier. |
| `node_name` | Required | Optional | Node identifier; omitted v2 node has one canonical null representation. |
| `message` | Required | Required | Diagnostic plain text; mutable source content. |
| `operator` | Required | Rejected | Exact legacy v1 string. V2 operator identity comes from authentication. |
| `time_created` | Required | Optional | UTC `DD-MM-YYYY HH:mm:ss`; omitted v2 value defaults once to PostgreSQL receipt time. |
| `severity` | Required | Required | V1: `error`, `major`, `warning`, `clear`. V2: `critical`, `high`, `warning`. |
| `status` | Rejected | Required | V2: `firing`, `suspended`, `resolved`. V1 resolves through severity `clear`. |
| `site` | Rejected | Required | Site identifier. |
| `impact` | Rejected | Required | Free-text description of client impact; no categories or numeric scale. |
| `runbook_url` | Rejected | Required | Absolute HTTP(S) URL; ingestion does not fetch it. |
| `key_field` | Optional | Rejected | Exact explicit v1 identity; omission uses section 6's length-prefixed encoding. V2 identity is generated under section 5. |

The system generates `history_id`, `timestamp`, tenant identity and other managed fields. It generates v1 `to_show` from effective suppression; senders cannot provide it. V2 `suspended` means firing with a source-suppression cause, not a third managed lifecycle status. Source details retain native names and values. V1-to-v2 migration creates new logical alerts; versions never merge.

### 1. Validation and compatibility

All customer fields in either source schema are strings; reject numbers, booleans, arrays, objects and null rather than coercing them. V1 requires every listed customer field except `key_field`. V2 requires every listed customer field except `node_name` and `time_created`. An optional value may be omitted, but, if supplied, must be a nonblank string satisfying its field rules. Reject unknown customer fields in both versions, duplicate JSON object keys, malformed UTF-8, unpaired Unicode surrogates, and invalid enum values. Validation errors identify item index, field, code and reason without echoing the full rejected payload.

Preserve valid string content exactly: no trimming, case folding or Unicode normalization of source values. Whitespace-only strings are invalid; leading/trailing whitespace in otherwise valid strings remains significant. Identifier fields (`application`, `object`, `component`, `node_name`, `site`, legacy `operator`, explicit v1 `key_field`) cannot contain control characters. Message and impact accept ordinary multiline plain text but reject NUL. `runbook_url` must be an absolute HTTP or HTTPS URL with a host, without whitespace, control characters or embedded credentials; store its exact spelling and do not fetch it during ingestion. The UI treats it as a link and renders source text without interpreting HTML.

Decoded-code-point limits are: identifiers 256, explicit v1 key 1,024, message 8,192, impact 4,096, URL 2,048, with the separately selected enums and timestamp format. Each raw customer JSON object is at most 65,536 uncompressed UTF-8 bytes before enrichment. No truncation. Rejected legacy inputs must be corrected or adapted before admission; there is no silent coercion or fallback to another version.

### 2. Time capture and presentation

Source `time_created` uses the agreed exact UTC `DD-MM-YYYY HH:mm:ss` format, valid calendar dates in years 0001–9999, without a timezone suffix or leap-second value. Reject invalid supplied values. Do not reject an otherwise valid timestamp merely because it is old or in the future: it describes source occurrence time and never controls ordering, expiry or maintenance coverage.

Capture authoritative UTC receipt time from PostgreSQL when admitting an item. Default omitted v2 `time_created` to that receipt time truncated to whole seconds, once only. Batch members share the request's admission instant and receive distinct increasing tenant order tokens. Preserve supplied/defaulted origin in history. Store timestamps as UTC instants; Product API timestamps use ISO 8601 UTC strings and the UI displays dates as `DD-MM-YYYY HH:mm:ss` in the browser timezone, labelled with that timezone. This does not change the maintenance editor's selected IANA timezone behavior. Preserve each received source timestamp separately even when the current occurrence keeps its existing `time_created`.

### 3. Managed field catalog

The following is the normative logical catalog; technical supplement 8–10 selects the alert/history physical record families, keys, partitions and indexes. A field's presence here does not make it customer-writable.

| Field | Meaning and exposure |
|---|---|
| `id`, `tenant_id`, `schema_version`, `key_field` | Immutable UUID alert ID, authoritative tenant, `v1`/`v2`, effective source-specific key. Searchable exact values. |
| `operator` | V2 immutable authenticated operator ID; v1 exact legacy operator string. Version and tenant distinguish these namespaces. Searchable. Display name is separate presentation metadata. |
| `application`, `component`, `node_name`, `site`, `impact`, `runbook_url` | Source-derived values; v1 `object` maps to `component`. Absent v2 node and v1 fields without a counterpart are null. Searchable; do not invent empty-string defaults. |
| `message` | Latest successfully applied message, including messages on resolved deliveries. Searchable plain text. |
| `severity`, `status`, `suppressed` | Shared severity; firing/resolved lifecycle; effective suppression boolean. See decisions 4 and 16. Searchable. |
| `time_created`, `first_received_at`, `timestamp` | Current occurrence's agreed creation time; first applied source receipt; latest applied nonduplicate source receipt. `timestamp` is also exposed as `last_received_at`, not a second clock. Searchable instants. |
| `occurrence_id`, `occurrence_number`, `opened_at`, `resolved_at` | Current/latest occurrence identity, sequence and observed lifecycle times. No occurrence ID/opened time before any observed firing. Latest resolution time exists even for first-seen resolved. Searchable; count is zero before first firing. |
| `acknowledged`, `acknowledged_by`, `acknowledged_at`, `assignee_id` | Managed acknowledgement and assignment; nullable actor/time and assignee. Searchable exact values. |
| `active_incident_id`, `incident_ids` | Current active ownership and retained incident links, including historical links. Searchable with incident policies unchanged. |
| `revision`, `projection_version`, `history_id` | Semantic concurrency revision, projection ordering version, latest applied source event UUID. Detail/API metadata; not expression inputs. |
| Source payloads, notes, occurrences, suppression causes and activity | Separate detail/history collections. Current undeleted note text is searchable through free-text search; note revisions and raw payloads are not CEL fields. |

CEL uses the `alert.` prefix for searchable scalar fields above. The maintenance/correlation field whitelist is `id`, `tenant_id`, `schema_version`, `key_field`, `operator`, `application`, `component`, `node_name`, `site`, `impact`, `runbook_url`, `message`, `severity`, `status`, `time_created`, `acknowledged`, `acknowledged_by`, and `assignee_id`, subject to existing expression restrictions. These are typed strings/enums, nullable strings where applicable, the acknowledged boolean, and the time_created timestamp.

Correlation grouping may use only the supported scalar subset, so timestamps cannot be grouping keys. Receipt counters/times, occurrence bookkeeping, actor timestamps, incident memberships, revisions, histories and note text are excluded from rule expressions: transport traffic and derived relationships must not manufacture eligibility. Suppression is an outer eligibility policy, not a rule-expression input; maintenance must not depend on its own suppression output. Feeds may filter the full searchable catalog, including suppression, receipt/occurrence timestamps and occurrence_number as an integer.

No arbitrary labels or additional source fields are introduced by examples elsewhere.

### 4. Severity, exceptional clear and nulls

Preserve error→critical, major→high, warning→warning, and v2's unchanged severities. Clear is resolution and preserves an existing known severity. Represent the first-seen-clear exception as the literal managed value `severity = "clear"`, so the UI and CEL agree: `alert.severity == "clear"` finds it. It is an unknown-prior-severity sentinel, not a fourth urgency level. Once a non-clear delivery supplies the first known severity, replace the sentinel. Manually reopening that exceptional row keeps clear until a valid source supplies a known severity; the firing lifecycle remains explicit.

Urgency sorts critical, high, warning, with clear last in either direction. Nullable fields compare equal to null when absent; string matching requires a non-null string and yields false on null in the supported query translation. Missing values sort last in either direction. The shared CEL validator/evaluator must implement these contracts consistently; technical supplement 2–7 now selects the complete initial operator/function profile, compiler, clock and equivalence contract. Incident severity values are unaffected.

## Logical identity and delivery identity

### 5. V2 identity encoding

Use lowercase hexadecimal SHA-256 of the UTF-8 identity encoding below as `key_field`. Its fixed input is the array `[2, operator_id, application, component, node_name_or_null, severity, site, impact, runbook_url]`, prefixed by the literal text `alerts:v2:identity:1` and one LF. Encode the array as compact JSON, with no spaces between elements; escape quote, backslash and U+0000–U+001F using standard JSON escapes (controls use lowercase `\u00xx`), and emit all other Unicode scalar values as literal UTF-8, including `/`. Null is the JSON literal `null`; 2 is the literal integer `2`. No string normalization occurs before hashing. All components are length-delimited by JSON syntax and position, not concatenated ambiguously.

This supplies the previously missing new-system algorithm; it does not assert byte compatibility with the old system's unspecified hashing implementation. It includes the immutable authenticated operator, not its editable name or API key. Exclude status, message, time_created and all other generated/managed data, as already agreed. Missing node has one canonical null representation; explicit null input is still invalid. Persist identity format version and canonical identity material alongside the key. A future hash-format change requires an explicit migration design, not an automatic reinterpretation of stored keys.

### 6. V1 identity encoding and collision protection

An explicit v1 `key_field` is used verbatim. If omitted, encode the agreed combination of application, object and node_name as `v1:` followed by each string's decimal UTF-8 byte length, `:`, and exact string, in that order without extra separators. For example application `a`, object `b`, node `c` yields `v1:1:a1:b1:c`. This selects an unambiguous new-system encoding of the previously agreed combination; the old system's exact delimiter format was not supplied and is not assumed. Producers needing an existing key's exact spelling must send that key explicitly, including on clear deliveries. Explicit and derived keys share the same v1 key namespace.

Logical uniqueness is `(tenant_id, schema_version, key_field)`. V1 operator is not added to the agreed fallback combination. Persist and compare immutable source identity/content when an existing key is found. Different v1 fixed content under the same explicit/derived key, or different v2 canonical identity material under the same digest, is a terminal `identity_conflict`; never merge, silently overwrite, or append a synthetic suffix. V1→v2 always creates a separate logical alert as agreed.

### 7. Mutable source fields and identity changes

For an existing logical alert, source updates may change message, source lifecycle/suppression indicators, receipt metadata, and occurrence timestamps only under the agreed lifecycle rules. V1 application, object, node_name and operator are fixed; its first known non-clear severity is fixed, with clear as the resolution indication rather than a severity mutation. A differing non-clear severity for the same v1 key is a conflict; a producer must use a different explicit key for a different severity identity. First-seen clear may initialize its first known severity later.

V2 changes to any hash input identify a different alert, including changes to severity, impact or runbook URL. The old alert remains in its current state until explicitly resolved or expired; the new delivery does not resolve or merge it. Resolving an old v2 alert therefore requires its original identity fields. A message change updates the same alert. Identity and fixed-field rules apply across recurrences, not just within one occurrence. Users cannot directly edit source fields, keys, severity, operator or time_created through the Product API.

### 8. External retry identifiers

Support optional `Idempotency-Key` on either ingestion endpoint for a whole request, and optional `event_id` on each wrapped batch item. Both are case-sensitive opaque ASCII strings of 1–128 characters from letters, digits, `.`, `_`, `:`, `-`; UUID strings are recommended. These are transport metadata, not additional source fields and not hash inputs. Scope request keys and item IDs to endpoint version plus authoritative tenant and, for v2, immutable operator ID. V1's namespace is the global v1 endpoint; caller-supplied operator does not authenticate retry ownership.

Compare retry content using a deterministic canonical encoding of the parsed request/item before enrichment and time defaults: ignore JSON property order and insignificant JSON formatting, but preserve array order, omissions and exact string content. Reject reuse with different content with `409 idempotency_conflict`. An identical replay returns the original receipt/defaults/results and performs no second admission, state change, history append or timer refresh. Duplicate item IDs inside a batch use the same rule, with the first occurrence winning. A request key deduplicates the whole batch; per-item IDs allow safe retry in a different batch.

Retain request-key results and receipt lookup tokens for 90 elapsed days after admission. Retain per-item event-ID associations while their alert is retained and for 90 days after alert purge; unattached rejected-event associations last 90 days. After the relevant retry window, identifier reuse may be treated as a new submission; publish this limit in the API. Requests without identifiers are new deliveries even if their contents are identical. The logical key and system-generated UUID cannot prove an external retry. These guarantees require no new mandatory customer source field.

### 9. Internal event identity

Assign one UUID `history_id` to each newly admitted item and use it as its internal event ID through inbox, Kafka, processing and source history. Deduplicated items return the original ID. User actions and scheduler actions have separate activity/command IDs. Internal retries always load the existing admitted record and preserve receipt time, order, defaulted fields, identity and provenance; a Kafka record alone may never create a new admission or resurrect deleted data. Source processing records terminal outcomes exactly once in the same transaction as any canonical mutation.

## Ingestion and processing

### 10. Request shapes and gateway context

These are the strict native endpoint contracts. The later [operator supplement](./spec-operator-operations.md), sections 7–8 and 17–19, adds an authenticated Grafana webhook transport adapter with a fixed conversion to native-equivalent v2 events. Its standard Grafana envelope and Bearer authentication are specific to that route; they do not add accepted fields or authentication alternatives to the native endpoints. All v2 transports share authoritative operator/credential checks and the existing identity, occurrence, history and durable-admission rules.

Use these distinct transport routes; the route selects the source schema and authentication contract:

| Route | Input | Authentication and destination |
|---|---|---|
| `POST /api/ingest/v1/alerts` | Native v1 object or wrapped batch | Unauthenticated ingestion into fixed Global. |
| `POST /api/ingest/v2/alerts` | Native v2 object or wrapped batch | Kong operator key; immutable operator-owned specific tenant. |
| `POST /api/ingest/v2/grafana` | Grafana webhook mapped by the operator adapter | Operator key through the dedicated Bearer adapter; same v2 tenant rules. |

Do not expose the version roots as alternate ingestion endpoints. Never infer or fall back to another schema from payload fields. A single request is the native v1 or v2 customer object. A batch is exactly `{"alerts":[{"event_id":"optional-sender-id","payload":{...native fields...}}]}`; omit `event_id` when unavailable. Only `alerts` is allowed at the batch root, and only `payload`/optional `event_id` are allowed per wrapper. No mixed schemas, tenant override or per-item credentials. If the top-level `alerts` member is present, validate as a batch and never reinterpret a bad batch as a single alert. JSON content type is required; initial ingestion accepts uncompressed UTF-8 request bodies only. Existing 1–100 batch size, 4 MiB whole-batch cap and 64 KiB customer-object cap remain unchanged; a single native object uses the 64 KiB cap.

Native v2 sends its API key in `X-API-Key` over HTTPS. Kong validates it, strips any client-supplied trusted-context headers, and supplies authenticated Consumer/operator and Kong credential identifiers over the private mutually authenticated Kong-to-ingestion connection. The Ingestion API accepts v2 context only on that connection, maps those bindings to its operator/key records and resolves operator→tenant from authoritative configuration; no direct external ingress can bypass it. Recheck credential validity in the PostgreSQL admission transaction as selected in operator supplement 8, including expiry/revocation despite stale gateway state. Never place the API key in messages, logs, receipts, source payload history or Kafka. Operator supplement 1–28 completes key rotation/provisioning/storage policy. V1 remains unauthenticated; unrelated supplied headers cannot route it elsewhere, and its public payload rejects team-generated fields such as to_show/history_id/timestamp.

### 11. Partial batch acceptance

Reject the entire request before admission for bad JSON/root envelope (including a non-array alerts value), unknown root fields, invalid v2 authentication/context, empty/over-count batch or excessive total size. Once the root envelope is valid, validate each member independently: accept valid members and return errors for invalid members. A malformed member wrapper, missing/non-object payload, unknown wrapper field, per-item oversize, bad source fields, bad item ID or ID/content conflict affects that item only. Preserve original zero-based indexes, and admission order among newly accepted items; do not collapse repeated logical keys.

Commit all newly accepted members of the request, their tenant order allocation, receipt result and received-event outbox records in one PostgreSQL transaction. Partial acceptance is a validation policy, not permission to acknowledge half a database transaction. A transaction failure admits none of that transaction; a lost response after commit is recovered with the request key. Rejected items have no alert mutation and no fabricated alert history event. Correcting an item requires a new request key and, if its previous event ID was durably associated with different admitted content, a new event ID.

### 12. HTTP acknowledgement and processing results

Return `202 Accepted` after durable PostgreSQL admission, without waiting for Kafka, the alert processor, Elasticsearch or correlation. Return a request ID, receipt URL/token, and ordered item results containing index, accepted/duplicate/rejected disposition, event ID when admitted, receipt time and structured error when rejected. Replays of a request key return the original response even if processing has advanced; receipt lookup gives current processing results. A valid batch with zero admitted/duplicate items returns 422; a single validation failure returns 422, and a single retry conflict returns 409.

Malformed envelope/JSON is 400, unsupported media/content encoding 415, whole-body/count limit 413, missing/invalid v2 key 401, and unauthorized operator context 403. Operator disable/re-enable is outside the initial release; there is no disabled-operator response. Capacity rejection is 429 with Retry-After; unavailable durable admission is 503. Never report 202 for memory-only or Kafka-only acceptance.

Expose `GET /api/ingest/v{1|2}/receipts/{request_id}` using an unguessable 256-bit receipt token in `X-Receipt-Token`, and additionally the same operator authentication for v2. This v1 token protects receipt access without requiring authentication to send alerts. It reveals only submitted-item IDs, dispositions/errors and pending/applied/rejected processing status, not payloads, tenant data or alert details. Store a token hash for verification; encrypt the original response retained for request-key replay so replay can return the same token without plaintext secret storage. Return 404 for inaccessible/expired receipts. Authenticated tenant readers can inspect associated receipt outcomes in product diagnostics. An applied result includes the alert ID and occurrence ID, if any. A terminal fixed-field conflict can appear here after initial 202; admission is explicitly different from successful state application. Use the secret protection and rotation contract in shared system section 21.

### 13. Durable processing, failures and backpressure

PostgreSQL owns a durable ingestion inbox. A relay publishes `alerts.received` from its admission outbox; Kafka is the transport/wakeup path and a periodic database scan recovers pending work after lost hints. The canonical processor applies newly admitted source items in tenant admission order, taking the existing tenant coordinator lock and prescribed downstream lock order. State, occurrence changes, source history, suppression consequences, correlation before/after journal, terminal outcome and change outbox commit atomically. A validated unchanged repeat still records one received event and updates last receipt/alert inactivity; it does not manufacture a semantic transition.

Keep original `admission_order` separate from canonical `change_order`. Allocate change_order from the common tenant coordinator at the state transaction, in committed mutation order; it is the correlation journal cursor order. Preserve original admission_order/time as source proof for rule activation/reset fences and source FIFO. A source admitted before a rule reset but processed later therefore has a later change_order and earlier admission proof: the worker sees it but cannot treat it as post-reset activity. Never append a late source journal row behind an already advanced cursor. Manual/control commands use their coordinated action order; scheduled transitions also retain their original effective time. These are internal bookkeeping fields, not new customer input.

Terminal content/identity conflicts are recorded as rejected and the tenant advances to the next input. Retry transient processing/relay/index failures with exponential backoff starting at one second and capped at 30 seconds with full jitter, as selected in the technical baseline. After 10 consecutive processing failures on the same head item, mark the tenant's processing blocked for investigation; retain pending inputs and resume from the same order on an audited explicit retry by a global super-admin after repair.

Never skip a failing item whose outcome is unknown. Different tenants continue independently. Duplicate/corrupt Kafka hints do not override the database; quarantine bad hints and recover from the inbox. Accept further inputs only within configured durable backlog budgets; return 429 before admission when a budget is exceeded, or 503 if durability cannot be established. System completion 23 selects measured application budget/concurrency qualification; the Kafka team supplies retention/service contracts; never silently discard admitted events.

### 14. Source versus manual ordering and revisions

Manual alert changes use expected `revision`, a command idempotency key scoped to tenant/actor/operation, and the existing tenant coordinator/lock order. The command fingerprint includes target IDs, revisions and values; reuse with different content is a conflict. If an earlier admitted source input for any targeted alert is still pending, reject the manual mutation with `409 source_updates_pending`; the UI refreshes and lets the user retry once it is applied. Check this atomically with command ordering. This prevents already-received work from later overwriting a manual choice. A source item admitted after a successful manual command can change lifecycle again, as already agreed. Other incident/correlation control ordering and reset barriers remain as specified in their supplements.

Increment semantic `revision` for actual changes to user-visible semantic state/content, notes or relationships. Unchanged source repeats only increment `projection_version` for receipt/history metadata; they do not stale a user's semantic revision or supply fresh correlation evidence. Every committed indexed change increments projection_version, including semantic changes and purge. Correlation observes the semantic revision and before/after proof, with receipt bookkeeping excluded from its expression catalog. A stale manual revision returns 409; identical command replay returns its original result. Retain successful alert command results for the alert lifetime, as for incidents. A no-op command makes no new occurrence or activity and preserves acknowledgement/assignment timestamps.

## Lifecycle, suppression and user actions

### 15. Occurrence representation

Assign each observed firing occurrence its own UUID and monotonically increasing number within the alert, starting at 1. Record opened_at from the source receipt or manual action time, separately from source-facing time_created. Close it with resolved_at and cause/actor. First-seen resolved has occurrence number 0 and no occurrence ID/opened_at; its row records time_created from that delivery and resolution observed at receipt time, with no invented firing duration. The next source or manual firing begins occurrence 1.

Preserve all agreed transitions: source firing after resolution changes current time_created to that delivery's supplied/defaulted value; manual reopening starts an occurrence but keeps time_created; repeated firing/resolved events and resolution keep it. New occurrences clear acknowledgement and assignment exactly once. Resolution itself preserves them until a new occurrence. Historical occurrence summaries retain their creation/open/close times and acknowledgement/assignment activity. Do not infer occurrence boundaries from equality/differences of source time_created. Incident links survive these transitions under the existing incident rules.

### 16. Legacy suspension and independent causes

V2 firing means lifecycle firing and removes the source-suspension cause. Suspended means lifecycle firing with an active source-suspension cause; it creates/reopens an occurrence just as firing does. Resolved means lifecycle resolved and removes the source cause. A change firing↔suspended alone does not create an occurrence. Maintain source suppression separately from each maintenance-rule cause; effective suppression is their OR. Removing one cause never removes another.

V1 has no customer-supplied suppression field. Its native severity determines firing/resolved. The team-generated `to_show` is a compatibility projection: `return` while effectively suppressed, `suspend` otherwise; clear always determines resolution regardless of to_show. It is not accepted as an unauthenticated customer override. The initial system has no imported legacy snapshot/enriched-ingress interface; an adapter requiring historical to_show imports needs a separately designed trusted migration contract. This preserves the current literal meanings without inventing a third lifecycle status or permitting public v1 input to control maintenance.

Manual status changes do not directly clear source or maintenance suppression causes. Re-evaluate maintenance against the resulting before/after state: a condition that becomes false closes its maintenance cause under the maintenance contract; source suppression remains controlled by source deliveries. A manual reopening is a new firing transition and must be evaluated for maintenance before correlation, using action time. Maintenance changes and source-cause removal use effective before/after suppression; only final effective unsuppression of a firing alert can supply fresh correlation evidence. Keep existing no-backfill/overlap/late-arrival rules, scheduled effective end times, links and active ownership. Record each cause's activation/release and effective suppression intervals with origin identity. [Maintenance](./spec-maintenance-operations.md) sections 4–11 define scheduler recovery, temporal proof and control races.

### 17. Acknowledgement and assignment

Allow editors to acknowledge/unacknowledge and assign/reassign/unassign firing, resolved or suppressed alerts. Acknowledging records the acting LDAP user and action time; acknowledging an already acknowledged alert is a no-op and does not replace the actor. Unacknowledging clears the current actor/time and preserves their history. Neither action changes assignee or status; there is no implicit assignment on acknowledgement. Include Assign to me.

Use the agreed effective-edit eligibility for user assignees. On writes, revalidate eligibility; when permission synchronization positively detects that the current assignee has lost all qualifying access, clear that still-current assignment atomically and record system cause eligibility_lost. Losing one grant is insufficient if another grant still qualifies. A directory outage or unknown freshness alone is not evidence of lost access. Assignment grants no permissions and cleanup does not reset inactivity. Identity supplement 6–11 supplies the delegated identity/session configuration, including the five-minute normal-operation LDAP target, last-known-data outage fallback and eligibility-cleanup integration. Alert new-occurrence clearing remains different from incident reopening, which preserves an eligible incident assignee.

### 18. Notes and actors

Any tenant editor may add, edit or delete any note on a retained alert, including resolved/suppressed alerts. Notes are nonblank plain text up to 10,000 Unicode code points; trim outer whitespace for validation/storage of notes only, not source content. Keep immutable revisions/deletion activity visible to tenant readers; show current undeleted notes in the primary notes list and search only those current texts. Notes belong to the logical alert and remain after reopening, with the occurrence ID at creation retained as context. They are not automatically copied as new notes into every occurrence.

Assistant-selected implementation clarification: the notes collection accepts
`include_deleted=true` for retained-note discovery; its default remains false.
Deleted entries expose their identity and deletion marker with current text null.
Readers open the existing note-history route for retained revision text. The
selector is bound into pagination and does not change retention or search.
Other alert history collections reject this note-only selector. Source-event
lists omit raw payloads; opening an event retrieves the existing detail route and
renders received JSON as plain text without interpreting or fetching its content.

Record stable LDAP actor IDs plus display-name snapshots; source events identify the authenticated v2 operator or explicitly unauthenticated v1 legacy operator; automated events identify their system cause. Preserve authorship after user/name changes. Never impersonate a user for automatic work. Note changes do not reset alert or linked-incident inactivity and cannot change correlation eligibility.

### 19. Alert inactivity

Use a fixed 30 elapsed days of source inactivity across tenants, without per-tenant override. Every successfully applied new source delivery, including an unchanged repeat, refreshes the alert's source-activity anchor to its original receipt time monotonically. External duplicates recognized by identifiers, internal retries, rejected inputs and user acknowledgement/assignment/notes do not refresh it. Manual reopening starts a new inactivity anchor at action time; the source may thereafter refresh it. Suppression does not pause expiry.

An hourly sweep resolves firing alerts whose activity deadline has passed. Under the coordinator, first ensure earlier admitted inputs for that alert have been processed, then recheck firing state, activity and deadline atomically. Resolve at execution time with system cause inactivity, preserve time_created and severity, and perform the normal linked-incident transition activity and correlation effects. A later accepted source firing opens a new occurrence normally. Resolved alerts are not repeatedly expired. This intentionally differs from incident inactivity: unchanged source repeats keep their alert current but never refresh the incident timer.

## Authority, propagation and retention

### 20. Authoritative history and storage

PostgreSQL is the authority for current alerts, admitted source payloads/results, occurrence summaries, user actions, note revisions, suppression intervals, relationship history and command results. Store the exact customer-object JSON bytes and parsed values for successfully admitted events, together with source version, trusted routing provenance, receipt order/time, identity format and supplied/defaulted time provenance. Store no authentication secrets. Admission-invalid payloads are not persisted as alert history; retain their structured receipt errors only. Semantically rejected admitted payloads are diagnostic records, not applied alert activity.

Elasticsearch is a rebuildable projection of retained current alerts and current undeleted note text. The alert timeline/received-event detail comes from PostgreSQL; a second full-history Elasticsearch index is not required initially. Index field mappings come from this catalog, with exact values for equality/identity and appropriate text fields for free-text search. Technical supplement 8–10 selects alert/history table families, partitions and indexes. Include full source history in measured capacity. Dedicated teams own infrastructure backup policy and tooling.

### 21. Event coverage and projection recovery

Use versioned internal envelopes independent of customer schema: event UUID, kind, tenant/alert IDs, source version when applicable, original admission order when source-driven, canonical change_order after application, cause/actor, effective time, commit time, semantic revision, projection_version and relevant history IDs. `alerts.received` references the authoritative inbox item; `alerts.changed` carries the complete current searchable snapshot (or deletion marker), not an ambiguous patch. Consumers reject unsupported internal versions visibly and preserve pending work for repair. Do not confuse internal envelope version with v1/v2.

Publish change snapshots for creation, source message/lifecycle changes, repeat receipt metadata, acknowledgement, assignment/cleanup, note changes, suppression transitions, incident relationship changes and purge. Every semantic revision also commits the separate canonical before/after correlation journal, so even a note/relationship-only revision advances current-state proof without inventing a false-to-true match or refreshing membership. Mere receipt traffic and no-op user commands do not create fresh evidence. Consumers are idempotent by event ID and apply snapshots only when projection_version is newer. Source application and correlation arbitration continue to use PostgreSQL order/proof, not Elasticsearch/Kafka ordering.

Rebuild search from a consistent PostgreSQL snapshot plus committed outbox changes after its boundary, then catch up and switch the serving index. Rebuild does not replay source events into lifecycle processing, create occurrences, run correlation actions or reopen alerts. Reconcile missing/deleted IDs, respect tombstones, and keep the previous serving index until the replacement is validated. Kafka loss can delay propagation but cannot erase authoritative alert history. The Kafka team supplies capacity/retention and supported settings; Appchi integrates partition-key/replay/rollout contracts through D2/D5/N1.

### 22. Alert retention

Retain a resolved alert and all its applied source history, occurrences, notes/revisions, activity, suppression history and successful command results for 90 elapsed days after its latest actual resolution, including a first-seen resolved row. Resolution repeats and resolved edits do not move this deadline. Reopening cancels the pending purge; later resolution starts a new 90-day period. No absolute creation-age cap and no manual Delete action. History remains available for the retained parent's lifetime; do not silently roll older occurrences out of a still-retained alert.

Unattached semantically rejected admission diagnostics expire 90 days after admission, as do standalone receipts/request results. Accepted pending inputs have no age-based deletion: process or explicitly repair them first. A retained alert's per-item dedup associations follow decision 8. Source history growth for continuously active alerts is an explicit sizing concern; changing to a rolling raw-history window would be a new product decision, not an implementation shortcut.

### 23. Purge and replay protection

The hourly retention worker, under the coordinator, rechecks resolved state/latest resolution and pending source inputs before purge. A source admitted before purge must be processed first; a firing source admitted after completed purge may create a new UUID alert with the same logical key and occurrence number 1. It is not a continuation of purged history. Technical supplement 23–24 refines the physical mechanism: purge atomically retires the alert and makes all parent-owned content inaccessible, releases live uniqueness/ownership records and writes the deletion snapshot plus immutable old-UUID/final-version fence.

Large physical history removal is then resumable and chunked after independent fence protection; visibility never becomes partially purged. This preserves the eligibility, pending-source, new-incarnation and surviving-reference rules here. Keep minimal tombstones without source content or actor data indefinitely until a separately verified replay horizon permits compaction; do not guess a safe age.

Surviving incidents retain only unavailable counterpart identity/link provenance, with no expired alert payload, under the incident supplement. Purge does not resolve incidents or resurrect/change the lifecycle of other alerts. Unavailable alerts are not actionable and do not count as live members; the incident's historical linked-reference total still includes them, with its separate unavailable subset, as already selected. Existing deferred correlation evidence referencing the purged alert cannot claim it; protected journal/reset proof follows correlation retention rules until its consumers have advanced.

Propagate deletion to Elasticsearch, caches and live views. Product authorization/detail checks treat tombstoned IDs as unavailable immediately; until index deletion catches up, omit those IDs from returned pages and mark counts as updating. Retained Kafka/failed-event copies are internal transport data, never a source for reconstructing deleted product content. Old internal event IDs without a live admitted record cannot enter source processing. Backup restore must reconcile the authoritative purge ledger before serving traffic; reliability supplement 17–18 assigns backups to dedicated teams and requires application restoration fences and protected purge evidence through an agreed interface. Technical supplement 23–29 selects the physical cleanup target/protocol and restore checks; executed verification and supplied protection/capacity evidence remain R4/N4 work; this is not a claim of instant erasure from backups.

Technical supplement 13 selects an inline-or-immutable-reference wire encoding for the complete snapshots above, without changing their logical coverage. Decisions 15–21 select versioned indexing, refresh proof, PIT pagination and durable live reconciliation; D2/D5/U4 now track implementation and supplied capabilities for those alert mechanisms.

## Product API and screens

### 24. Reads, search and presentation

Alert detail, occurrence/history/notes and command responses read PostgreSQL and provide read-your-writes. Feeds, full-text search and counts use Elasticsearch and may lag; return an indexing watermark/updating indication and never present a stale result as proof a command failed. Permissions and selected tenant apply to every detail/search/count request; knowing an ID grants no access. Keep raw received values under a source-details section alongside the shared fields, so v1 object/clear/to_show compatibility is understandable without replacing canonical lifecycle. Optional `q` is plain-text search, at most 256 code points, requiring all case-insensitive query tokens across message, impact and current undeleted notes; do not interpret it as CEL, regex or a query language. It combines with CEL, tenant and suppression filters. Search normalization never changes source storage or identity.

Default feed ordering is latest applied receipt timestamp descending, then alert ID ascending. Page size defaults to 50, maximum 200; opaque snapshot cursors last five minutes, bind tenant/filter/sort/visibility scope, and must be restarted after expiration or query changes. Revalidate access on every page; permission revocation overrides a snapshot. New arrivals appear on refresh rather than shifting pages mid-traversal. Sortable columns are application, component, node_name, site, operator, severity, status, time_created, first_received_at, timestamp/last_received_at, occurrence_number, opened_at, resolved_at, acknowledged and assignee_id; reject unsupported sorts.

Use exact Unicode scalar lexical order for strings, numeric/time order for integers/timestamps, false before true for booleans, the selected severity order and null-last behavior, and alert ID as the final tie-break. Ordered columns and sort remain preset settings and no preset time range is introduced. The activity timeline follows canonical change_order, while the source-events view follows original receipt/admission order; both show source/effective time separately from processing time and support ascending/descending order.

Their page size is 50/max 200 with stable order/ID cursors. This keeps delayed processing explicit without backdating actual state mutations.

### 25. Suppression controls and counts

Ordinary feeds and count requests use `include_suppressed=false` by default, as already agreed. Provide an explicit Include suppressed view/request switch outside CEL; with it enabled the caller's CEL determines which suppressed/unsuppressed rows match. A CEL expression alone cannot silently bypass the default exclusion. The same effective filter applies to page results and their total count, and counts always count logical rows, never events/occurrences.

The switch is transient view/request state, not an added preset field; reopening a preset uses the ordinary default. Dashboard section 6 defines ordinary counts without a dashboard suppression switch. Incident details continue to show linked suppressed alerts with their suppression indicators. Do not exclude resolved alerts implicitly: lifecycle filtering comes from CEL/the selected view. Suppression does not conceal data from authorized explicit searches.

### 26. Commands, endpoints and errors

All routes below are relative to `/api/tenants/{tenant_id}/alerts`:

| Method | Route | Contract |
|---|---|---|
| GET | collection root | Filtered feed under section 24. |
| GET | `/{alert_id}` | Authoritative alert detail. |
| GET | `/{alert_id}/history`, `/{alert_id}/occurrences`, `/{alert_id}/notes`, `/{alert_id}/source-events` | Alert-owned collections, never tenant-wide shorthand. |
| POST | `/{alert_id}/commands` | `command_id`, `expected_revision`, `kind` and `value`. Kinds: `set_status`, `set_acknowledged`, `set_assignee`. |
| POST | `/{alert_id}/notes` | Note text plus command ID and expected alert revision. |
| PATCH / DELETE | `/{alert_id}/notes/{note_id}` | Note update/removal with the same alert concurrency/idempotency metadata; DELETE carries command ID in `Idempotency-Key` and quoted revision in `If-Match`, without a JSON body. |
| POST | `/bulk-commands` | Atomic explicit selection under section 27. |

Command `value` is `firing` or `resolved` for status, a JSON boolean for acknowledgement, and an eligible principal UUID or null for assignment. Note creation/update uses a `text` string. No alternate values or implicit field coercion are accepted. Incident linking/moving stays in the existing incident command contract. Use server-generated UUIDs for alert/occurrence/note/activity IDs and opaque command UUIDs from the caller.

Tenant view permits reads; edit or higher permits these mutations. Return 404 for inaccessible/cross-tenant resources, 403 for a visible resource without edit permission, 409 for stale revisions/pending source/reused command with different content, and 422 for invalid values/ineligible assignees. Return 201 for note creation and 200 with authoritative result/revision for commands and note changes, including no-ops. Revalidate permissions on replay before returning a stored result. Use a consistent error object with code, message, field errors and request ID; never expose another tenant's state. No source-content PATCH or alert Delete endpoint is offered.

### 27. Bulk alert actions

POST `/api/tenants/{tenant_id}/alerts/bulk-commands` accepts `{command_id, kind, value, items: [{alert_id, expected_revision}]}`. It supports up to 100 explicitly selected alert IDs for one status, acknowledgement or assignment command in one tenant. `kind` and `value` use section 26's contract. Repeated IDs must carry the same expected revision; conflicting duplicates return 422. Return 200 with each selected alert's authoritative result/revision, in first-selection order, including no-ops.

Deduplicate the selection before counting. Validate all permissions, pending-source checks, revisions and assignment eligibility, then apply atomically; on any failure change none and return indexed resource errors only for resources the caller may see. Use the existing sorted lock order. No unbounded Apply to all matching results operation, bulk note edits, or cross-tenant command in the initial API. This does not change the separate partial-acceptance policy for source batches or the complete-set policy for automatic correlation.

### 28. Acceptance

See [required alerts checks](./verification-plan.md#alerts).
