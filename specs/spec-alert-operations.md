# Alert operations

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

The 2026-09-30 [Kafka-first pipeline](spec-kafka-alert-pipeline.md) governs alert transport, gateway admission, UTC ordering, manual correlation, search reconciliation and cutover (REV-33). Unrelated product behavior remains unchanged.

Native v1/v2 inputs, logical identity, admission, lifecycle, history and alert APIs. Shared execution and storage are specified in [Alerts and history technical design](spec-alert-history-technical.md).

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
| `time_created` | Required | Optional | UTC `DD-MM-YYYY HH:mm:ss`; omitted v2 value defaults once to ingress receive time. |
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

Capture UTC when ingress receives the request, before reading its body. All members share that timestamp. Default omitted v2 `time_created` once from it, truncated to whole seconds. Preserve defaulting provenance and source-provided time separately. Processing order is Kafka append order per logical key, not timestamp sorting. Product timestamps are ISO 8601 UTC; display uses browser timezone and `DD-MM-YYYY HH:mm:ss`. Clock health and control ties follow Kafka pipeline section 5.

### 3. Managed field catalog

The following is the normative logical catalog; technical supplement 8–10 selects the alert/history physical record families, keys, partitions and indexes. A field's presence here does not make it customer-writable.

| Field | Meaning and exposure |
|---|---|
| `id`, `tenant_id`, `schema_version`, `key_field` | Immutable UUID alert ID, authoritative tenant, `v1`/`v2`, effective source-specific key. Searchable exact values. |
| `operator` | V2 immutable authenticated operator ID; v1 exact legacy operator string. Version and tenant distinguish these namespaces. Searchable. Alert detail, feed and preset preview display the current same-tenant managed operator name for v2, or the exact legacy string for v1, through read-time `operator_display_name` presentation metadata. The stored ID and CEL/sort meaning remain unchanged. If a v2 name cannot be resolved, the display metadata is null and the UI says Unknown operator rather than showing its ID. |
| `application`, `component`, `node_name`, `site`, `impact`, `runbook_url` | Source-derived values; v1 `object` maps to `component`. Absent v2 node and v1 fields without a counterpart are null. Searchable; do not invent empty-string defaults. |
| `message` | Latest successfully applied message, including messages on resolved deliveries. Searchable plain text. |
| `severity`, `status`, `suppressed` | Shared severity; firing/resolved lifecycle; effective suppression boolean. See decisions 4 and 16. Searchable. |
| `time_created`, `first_received_at`, `timestamp` | Current occurrence's agreed creation time; first applied source receipt; latest applied nonduplicate source receipt. `timestamp` is also exposed as `last_received_at`, not a second clock. Searchable instants. |
| `occurrence_id`, `occurrence_number`, `opened_at`, `resolved_at` | Current/latest occurrence identity, sequence and observed lifecycle times. No occurrence ID/opened time before any observed firing. Latest resolution time exists even for first-seen resolved. Searchable; count is zero before first firing. |
| `assignee_id` | Nullable eligible user UUID; the sole current ownership signal. Searchable exact value. |
| `display_status` | Derived current status: `firing`, `acknowledged`, or `resolved`, under section 17. Feed-only virtual enum; not a source field or independently writable state. |
| `acknowledged`, `acknowledged_by`, `acknowledged_at` | Deprecated compatibility evidence only. Retained old CEL predicates keep their previous boolean/actor/time meaning; omitted from current alert responses and editor discovery. Never used to derive current status. |
| `active_incident_id`, `incident_ids` | Current active ownership and retained incident links, including historical links. Searchable with incident policies unchanged. |
| `revision`, `projection_version`, `history_id` | Semantic concurrency revision, projection ordering version, latest applied source event UUID. Detail/API metadata; not expression inputs. |
| Source payloads, notes, occurrences, suppression causes and activity | Separate detail/history collections. Current undeleted note text is searchable through free-text search; note revisions and raw payloads are not CEL fields. |

CEL references searchable scalar fields directly by their catalog names, such as `application`, `severity` and `display_status`; the `alert.` prefix is not required. Existing expressions using `alert.field` remain accepted as a compatibility spelling and retain their original meaning. Bare identifiers are still restricted to the approved field catalog and each context's existing whitelist. The maintenance field whitelist is `id`, `tenant_id`, `schema_version`, `key_field`, `operator`, `application`, `component`, `node_name`, `site`, `impact`, `runbook_url`, `message`, `severity`, `status`, `time_created`, `acknowledged`, `acknowledged_by`, and `assignee_id`, subject to existing expression restrictions. These are typed strings/enums, nullable strings where applicable, the acknowledged boolean, and the time_created timestamp.

Correlation conditions and grouping exclude `assignee_id`; existing references are explicitly blocked during cutover until edited/reset. Correlation grouping may use only the supported scalar subset, so timestamps cannot be grouping keys. Receipt counters/times, occurrence bookkeeping, actor timestamps, incident memberships, revisions, histories and note text are excluded from rule expressions: transport traffic and derived relationships must not manufacture eligibility. Suppression is an outer eligibility policy, not a rule-expression input; maintenance must not depend on its own suppression output. Feeds may filter the full searchable catalog, including suppression, receipt/occurrence timestamps and occurrence_number as an integer.

No arbitrary labels or additional source fields are introduced by examples elsewhere.

### 4. Severity, exceptional clear and nulls

Preserve error→critical, major→high, warning→warning, and v2's unchanged severities. Clear is resolution and preserves an existing known severity. Represent the first-seen-clear exception as the literal managed value `severity = "clear"`, so the UI and CEL agree: `severity == "clear"` finds it. It is an unknown-prior-severity sentinel, not a fourth urgency level. Once a non-clear delivery supplies the first known severity, replace the sentinel. Manually reopening that exceptional row keeps clear until a valid source supplies a known severity; the firing lifecycle remains explicit.

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

Optional legacy request keys and member event_id values remain syntax-validated migration inputs. They do not deduplicate submissions. Each client resubmission is a new receipt. No sender identifier or receipt token is required. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 2 for the assistant-selected HTTP contract.

### 9. Internal event identity

Generate one internal delivery UUID before the first Kafka publish attempt and reuse its exact bytes/time on all three attempts. PostgreSQL source-result proof applies that UUID once, including duplicates at different Kafka offsets. Preserve permanent minimal replay fences. Logical alert identity remains sections 5–7.

## Ingestion and processing

### 10. Request shapes and gateway context

These are the strict native endpoint contracts. The later [operator supplement](spec-operator-operations.md), sections 7–8 and 17–19, adds an authenticated Grafana webhook transport adapter with a fixed conversion to native-equivalent v2 events. Its standard Grafana envelope and Bearer authentication are specific to that route; they do not add accepted fields or authentication alternatives to the native endpoints. All v2 transports share authoritative operator/credential checks and the existing identity, occurrence, history and durable-admission rules.

Use these distinct transport routes; the route selects the source schema and authentication contract:

| Route | Input | Authentication and destination |
|---|---|---|
| `POST /api/ingest/v1/alerts` | Native v1 object or wrapped batch | Unauthenticated ingestion into fixed Global. |
| `POST /api/ingest/v2/alerts` | Native v2 object or wrapped batch | Kong operator key; immutable operator-owned specific tenant. |
| `POST /api/ingest/v2/grafana` | Grafana webhook mapped by the operator adapter | Operator key through the dedicated Bearer adapter; same v2 tenant rules. |

Do not expose the version roots as alternate ingestion endpoints. Never infer or fall back to another schema from payload fields. A single request is the native v1 or v2 customer object. A batch is exactly `{"alerts":[{"event_id":"optional-sender-id","payload":{...native fields...}}]}`; omit `event_id` when unavailable. Only `alerts` is allowed at the batch root, and only `payload`/optional `event_id` are allowed per wrapper. No mixed schemas, tenant override or per-item credentials. If the top-level `alerts` member is present, validate as a batch and never reinterpret a bad batch as a single alert. JSON content type is required; initial ingestion accepts uncompressed UTF-8 request bodies only. Existing 1–100 batch size, 4 MiB whole-batch cap and 64 KiB customer-object cap remain unchanged; a single native object uses the 64 KiB cap.

Native v2 uses X-API-Key over HTTPS. Open-source Kong Key Auth plus the Appchi policy plugin checks active credential state, expiry, immutable owning tenant and policy generation. It strips client identity/credential headers and sends trusted context over private pinned mTLS. Ingress validates that context without PostgreSQL. Prepared credentials remain denied; all-node policy proof gates activation and revocation completion. V1 remains unauthenticated fixed Global. Keys never enter source/history/Kafka. See operator section 8 and Kafka pipeline section 7.

### 11. Partial batch acceptance

Validate members independently and publish valid members concurrently as separate Kafka records. Preserve result indices and item errors. Return 202 per item only after durable broker acknowledgement. Whole-response statuses are 202/207/422/503 as defined in [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 2; envelope errors fail before publishing.

### 12. HTTP acknowledgement and processing results

A 202 means ingress validation plus Kafka acceptance. It does not mean PostgreSQL application, search visibility or eventual processing before Kafka retention expiry. The receipt lookup API is removed; internal semantic rejections remain operational diagnostics. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) sections 2, 3 and 8.

### 13. Durable processing, failures and backpressure

Use self-contained alerts.received records and the transactional Kafka source consumer in [Kafka-first pipeline](spec-kafka-alert-pipeline.md) sections 1–3. PostgreSQL outages do not prevent healthy Kafka admission. Broker failure produces retryable per-item failure after three total attempts. There is no application backlog/lag gate. Transient processing failures retain offsets; terminal source business conflicts record post-202 rejection and advance. Kafka retention can lose unprocessed acknowledged inputs.

### 14. Source versus manual ordering and revisions

Manual commands commit directly to PostgreSQL with authorization, expected revision and command idempotency. Remove source_updates_pending. A queued source event can apply later and change the alert again. No-op commands retain their no-op behavior. Correlation ignores manual edits except a transition to resolved, which atomically removes evidence and records its UTC release boundary without unlinking or resolving incidents. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 4.

## Lifecycle, suppression and user actions

### 15. Occurrence representation

Assign each observed firing occurrence its own UUID and monotonically increasing number within the alert, starting at 1. Record opened_at from the source receipt or manual action time, separately from source-facing time_created. Close it with resolved_at and cause/actor. First-seen resolved has occurrence number 0 and no occurrence ID/opened_at; its row records time_created from that delivery and resolution observed at receipt time, with no invented firing duration. The next source or manual firing begins occurrence 1.

Preserve all agreed transitions: source firing after resolution changes current time_created to that delivery's supplied/defaulted value; manual reopening starts an occurrence but keeps time_created; repeated firing/resolved events and resolution keep it. New occurrences clear assignment exactly once and therefore display Firing. Resolution preserves assignment until a new occurrence, while displaying Resolved. Existing legacy acknowledgement storage also resets on a new occurrence for compatibility; it has no current ownership meaning. Historical occurrence summaries retain their creation/open/close times and recorded acknowledgement/assignment activity. Do not infer occurrence boundaries from equality/differences of source time_created. Incident links survive these transitions under the existing incident rules.

### 16. Legacy suspension and independent causes

**Current scope (REV-34):** Maintenance has no scheduler; after a window ends, its suppression clears on the alert's next source update, not at the end time; see [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler). Cause and re-evaluation rules below remain normative.

V2 firing means lifecycle firing and removes the source-suspension cause. Suspended means lifecycle firing with an active source-suspension cause; it creates/reopens an occurrence just as firing does. Resolved means lifecycle resolved and removes the source cause. A change firing↔suspended alone does not create an occurrence. Maintain source suppression separately from each maintenance-rule cause; effective suppression is their OR. Removing one cause never removes another.

V1 has no customer-supplied suppression field. Its native severity determines firing/resolved. The team-generated `to_show` is a compatibility projection: `return` while effectively suppressed, `suspend` otherwise; clear always determines resolution regardless of to_show. It is not accepted as an unauthenticated customer override. The initial system has no imported legacy snapshot/enriched-ingress interface; an adapter requiring historical to_show imports needs a separately designed trusted migration contract. This preserves the current literal meanings without inventing a third lifecycle status or permitting public v1 input to control maintenance.

Manual status changes do not directly clear source or maintenance suppression causes. Re-evaluate maintenance against the resulting before/after state: a condition that becomes false closes its maintenance cause under the maintenance contract; source suppression remains controlled by source deliveries. A manual reopening is a new firing transition and must be evaluated for maintenance before correlation, using action time. Maintenance changes and source-cause removal use effective before/after suppression; only final effective unsuppression of a firing alert can supply fresh correlation evidence. Keep existing no-backfill/overlap/late-arrival rules, scheduled effective end times, links and active ownership. Record each cause's activation/release and effective suppression intervals with origin identity. [Maintenance](spec-maintenance-operations.md) sections 4–11 define scheduler recovery, temporal proof and control races.

### 17. Assignment and derived acknowledgement

**Current scope (REV-34, REV-35):** Automatic `eligibility_lost` cleanup and five-minute LDAP propagation are deferred; known-ineligible assignees are masked at read time, not cleared; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Derived status and assignment rules below remain normative.

**User decision, 2026-09-27 (REV-27):** assignment acknowledges responsibility. Remove the independent acknowledgement field and acknowledge/unacknowledge actions from current product views. The source lifecycle remains `firing`/`resolved`; the user-visible Status is derived from lifecycle and current assignee:

| Lifecycle | Assignee | Visible status / `display_status` |
|---|---|---|
| Firing | None | Firing / `firing` |
| Firing | Eligible user | Acknowledged / `acknowledged` |
| Resolved | Any or none | Resolved / `resolved` |

Allow editors to assign/reassign/unassign firing, resolved or suppressed alerts. One Assign control on the detail page offers Assign to me, an eligible-user picker and Unassign when assigned. Feed and saved-preset rows offer Assign to me or Unassign, and Resolve or Reopen, in their ⋯ menu (REV-43). Assigning another user takes effect immediately without acceptance. Assigning or reassigning a firing alert displays Acknowledged; removing its assignee displays Firing. A repeated firing delivery preserves assignment. Resolution preserves the assignee, and the next occurrence clears it. Suppression remains a separate indicator and does not change this status table. Preserve acting user, target and action time in assignment history. Reassigning to the same user is a no-op.

**Assistant-selected compatibility:** retain old acknowledgement columns, physical search fields, immutable snapshots, activity and command receipts as historical/compatibility evidence. Never infer assignment from `acknowledged_by`, rewrite recorded history, or update the deprecated boolean when assigning. Current detail/feed/preview/linked-alert/affected-alert/command responses omit acknowledgement boolean/actor/time labels and expose `display_status` alongside the raw lifecycle `status`. Fresh and replayed supported command responses apply current assignee eligibility masking and derive visible status without changing stored receipts; the recorded lifecycle, revision and other command-result values remain those of the original command. The retired `set_acknowledged` command, including a retry of that kind, now returns 422. Existing CEL predicates and saved acknowledgement sorts retain their old independent-field meaning; they are removed from new editor suggestions. Use `display_status == "acknowledged"` for current ownership filters. This explicit compatibility boundary avoids silently changing saved rules or protected correlation/maintenance evidence.

Use the agreed effective-edit eligibility for user assignees. On writes, revalidate eligibility; when permission synchronization positively detects that the current assignee has lost all qualifying access, clear that still-current assignment atomically and record system cause eligibility_lost. Authoritative reads hide a known-ineligible assignee while cleanup is pending, deriving Firing for a firing alert; the search projection converges under its existing freshness contract. Losing one grant is insufficient if another grant still qualifies. A directory outage or unknown freshness alone is not evidence of lost access. Assignment grants no permissions and cleanup does not reset inactivity. Identity supplement 6–11 supplies the delegated identity/session configuration, including the five-minute normal-operation LDAP target, last-known-data outage fallback and eligibility-cleanup integration. Alert new-occurrence clearing remains different from incident reopening, which preserves an eligible incident assignee.

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

**Current scope (REV-34):** No sweep resolves inactive alerts; the activity anchors below are stored for compatibility and future automation; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation).

Use a fixed 30 elapsed days of source inactivity across tenants, without per-tenant override. Every successfully applied new source delivery, including an unchanged repeat, refreshes the alert's source-activity anchor to its original receipt time monotonically. Same-delivery Kafka duplicates, internal retries, rejected inputs and user assignment/notes do not refresh it. Manual reopening starts a new inactivity anchor at action time; the source may thereafter refresh it. Suppression does not pause expiry.

An hourly sweep resolves firing alerts whose activity deadline has passed. Under the coordinator, first ensure earlier admitted inputs for that alert have been processed, then recheck firing state, activity and deadline atomically. Resolve at execution time with system cause inactivity, preserve time_created and severity, and perform the normal linked-incident transition activity and correlation effects. A later accepted source firing opens a new occurrence normally. Resolved alerts are not repeatedly expired. This intentionally differs from incident inactivity: unchanged source repeats keep their alert current but never refresh the incident timer.

## Authority, propagation and retention

### 20. Authoritative history and storage

PostgreSQL is authoritative for applied current state/history, occurrences, user actions, note revisions, suppression/relationship proof and command results. Kafka holds validated receipts before application. On application preserve exact customer JSON, parsed values, trusted routing, ingress receive time, application order and defaulting provenance; never store authentication secrets. Validation failures have no alert history. Post-202 semantic rejections remain explicitly labelled diagnostics. Projection snapshots and immutable delivery results are proof, not polled dispatch queues.

### 21. Event coverage and projection recovery

Source state/history and immutable publication proof commit in PostgreSQL before a Kafka transaction publishes changed and commits the source offset. Manual/maintenance/relationship/retirement changes attempt best-effort notifications only after commit. Both paths cover all visible fields. Correlation uses tenant Kafka order and original receive UTC eligibility; unchanged repeats and manual reopening create no fresh evidence. Search uses version guards, bounded authority reconciliation and the fenced rebuild protocol in [Kafka-first pipeline](spec-kafka-alert-pipeline.md) sections 3–6. Redis/SSE hints retain durable view-state reconciliation.

### 22. Alert retention

**Current scope (REV-34):** Retention workers are not deployed, so resolved alerts are not retired at the 90-day deadline, which stays stored for future automation; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Deadline and fence rules below remain normative.

Retain a resolved alert and all its applied source history, occurrences, notes/revisions, activity, suppression history and successful command results for 90 elapsed days after its latest actual resolution, including a first-seen resolved row. Resolution repeats and resolved edits do not move this deadline. Reopening cancels the pending purge; later resolution starts a new 90-day period. No absolute creation-age cap and no manual Delete action. History remains available for the retained parent's lifetime; do not silently roll older occurrences out of a still-retained alert.

Source rejection detail is retained for 90 days. Minimal delivery UUID/digest/first-coordinate/result fences and retired logical-key boundaries remain through replay and restore risk; they contain no source bodies after cleanup. Unconfirmed immutable changed proof cannot be purged. There is no application-owned pending inbox retention guarantee: Kafka can expire accepted unprocessed inputs. Command receipt retention remains unchanged. See Kafka pipeline section 8.

### 23. Purge and replay protection

**Current scope (REV-34):** The hourly retention worker is not deployed; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Retirement fences, replay protection and the rules for references that survive a purge remain normative.

The hourly retention worker, under the coordinator, rechecks resolved state/latest resolution, applied-but-unconfirmed source results and protected dependencies before purge. **Assistant-selected Kafka retirement boundary:** retain a logical-key UTC fence at committed retirement. A delayed receipt at or before that boundary is terminally rejected as retired_receipt; a later firing receipt may create a new UUID alert with the same logical key and occurrence number 1. Kafka inputs not yet applied cannot be enumerated by a PostgreSQL pending-target check. It is not a continuation of purged history. Technical supplement 23–24 refines the physical mechanism: purge atomically retires the alert and makes all parent-owned content inaccessible, releases live uniqueness/ownership records and writes the deletion snapshot plus immutable old-UUID/final-version fence.

Large physical history removal is then resumable and chunked after independent fence protection; visibility never becomes partially purged. This preserves the eligibility, pending-source, new-incarnation and surviving-reference rules here. Keep minimal tombstones without source content or actor data indefinitely until a separately verified replay horizon permits compaction; do not guess a safe age.

Surviving incidents retain only unavailable counterpart identity/link provenance, with no expired alert payload, under the incident supplement. Purge does not resolve incidents or resurrect/change the lifecycle of other alerts. Unavailable alerts are not actionable and do not count as live members; the incident's historical linked-reference total still includes them, with its separate unavailable subset, as already selected. Existing deferred correlation evidence referencing the purged alert cannot claim it; protected journal/reset proof follows correlation retention rules until its consumers have advanced.

Propagate deletion to Elasticsearch, caches and live views. Product authorization/detail checks treat tombstoned IDs as unavailable immediately; until index deletion catches up, omit those IDs from returned pages and mark counts as updating. Retained Kafka/failed-event copies are internal transport data, never a source for reconstructing deleted product content. Old internal event IDs without a live admitted record cannot enter source processing. Backup restore must reconcile the authoritative purge ledger before serving traffic; reliability supplement 17–18 assigns backups to dedicated teams and requires application restoration fences and protected purge evidence through an agreed interface. Technical supplement 23–29 selects the physical cleanup target/protocol and restore checks; executed verification and supplied protection/capacity evidence remain R4/N4 work; this is not a claim of instant erasure from backups.

Technical supplement 13 selects an inline-or-immutable-reference wire encoding for the complete snapshots above, without changing their logical coverage. Decisions 15–21 select versioned indexing, refresh proof, PIT pagination and durable live reconciliation; D2/D5/U4 now track implementation and supplied capabilities for those alert mechanisms.

## Product API and screens

### 24. Reads, search and presentation

Alert detail, occurrence/history/notes and command responses read PostgreSQL and provide read-your-writes. The detail page offers a read-only View alert action that opens the currently loaded alert detail response as formatted JSON in an accessible modal; opening it performs no additional request or mutation. Feeds, full-text search and counts use Elasticsearch and may lag; return an indexing watermark/updating indication and never present a stale result as proof a command failed. Permissions and selected tenant apply to every detail/search/count request; knowing an ID grants no access. Keep raw received values under a source-details section alongside the shared fields, so v1 object/clear/to_show compatibility is understandable without replacing canonical lifecycle. Optional `q` is plain-text search, at most 256 code points, requiring all case-insensitive query tokens across message, impact and current undeleted notes; do not interpret it as CEL, regex or a query language. It combines with CEL, tenant and suppression filters. Search normalization never changes source storage or identity.

Default feed ordering is latest applied receipt timestamp descending, then alert ID ascending. Page size defaults to 50, maximum 200; opaque snapshot cursors last five minutes, bind tenant/filter/sort/visibility scope, and must be restarted after expiration or query changes. Revalidate access on every page; permission revocation overrides a snapshot. New arrivals appear on refresh rather than shifting pages mid-traversal. Sortable columns are application, component, node_name, site, operator, severity, status, time_created, first_received_at, timestamp/last_received_at, occurrence_number, opened_at, resolved_at and assignee_id; reject unsupported sorts. Assistant-selected compatibility retains existing `acknowledged` sorts for old definitions, labelled Legacy acknowledgement when editing. The new derived `display_status` is not sortable; label raw `status` sorting Lifecycle so it cannot imply the three visible-status order.

On the All alerts page, clicking a supported sortable column heading temporarily sorts the whole feed by that field ascending, then descending on a second click, then restores the default order on a third click. Clicking a different supported heading starts its ascending cycle. Each change starts a new result snapshot on page one and clears selection. Composite or derived headings without a supported sort field remain static.

The Feed can group results by one field under [preset section 4](spec-preset-operations.md#4-columns-and-sorting)'s grouping contract (REV-44). Feed grouping is transient view state like the temporary sort; Save as preset carries it into the new preset draft. Changing it starts a new snapshot and clears selection. `POST /api/tenants/{tenant_id}/alerts/groups` accepts the feed's `cel`, `q`, `include_suppressed`, `sort` and `direction` plus `group_by`, `group_limit`, `rows_per_group` and `group_cursor`, with the limits of preset section 16's grouped preview. The collection root accepts `group_by` with `group_key` or `group_empty=true` to page one group's rows.

Use exact Unicode scalar lexical order for strings, numeric/time order for integers/timestamps, false before true for booleans, the selected severity order and null-last behavior, and alert ID as the final tie-break. Ordered columns and sort remain preset settings and no preset time range is introduced. The activity timeline follows canonical change_order, while the source-events view follows PostgreSQL application order; both show source/effective time separately from processing time and support ascending/descending order.

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
| POST | `/{alert_id}/commands` | `command_id`, `expected_revision`, `kind` and `value`. Kinds: `set_status`, `set_assignee`. |
| POST | `/{alert_id}/notes` | Note text plus command ID and expected alert revision. |
| PATCH / DELETE | `/{alert_id}/notes/{note_id}` | Note update/removal with the same alert concurrency/idempotency metadata; DELETE carries command ID in `Idempotency-Key` and quoted revision in `If-Match`, without a JSON body. |
| POST | `/bulk-commands` | Atomic explicit selection under section 27. |

Command `value` is `firing` or `resolved` for lifecycle status, and an eligible principal UUID or null for assignment. `acknowledged` is a derived display value, never an accepted lifecycle write; `set_acknowledged` and boolean command values are rejected with 422. Note creation/update uses a `text` string. No alternate values or implicit field coercion are accepted. Incident linking/moving stays in the existing incident command contract. Use server-generated UUIDs for alert/occurrence/note/activity IDs and opaque command UUIDs from the caller.

Tenant view permits reads; edit or higher permits these mutations. Return 404 for inaccessible/cross-tenant resources, 403 for a visible resource without edit permission, 409 for stale revisions/reused command with different content, and 422 for invalid values/ineligible assignees. Return 201 for note creation and 200 with authoritative result/revision for commands and note changes, including no-ops. Revalidate permissions on replay before returning a stored result. Use a consistent error object with code, message, field errors and request ID; never expose another tenant's state. No source-content PATCH or alert Delete endpoint is offered.

### 27. Bulk alert actions

POST `/api/tenants/{tenant_id}/alerts/bulk-commands` accepts `{command_id, kind, value, items: [{alert_id, expected_revision}]}`. It supports up to 100 explicitly selected alert IDs for one lifecycle status or assignment command in one tenant. `kind` and `value` use section 26's contract. Repeated IDs must carry the same expected revision; conflicting duplicates return 422. Return 200 with each selected alert's authoritative result/revision, in first-selection order, including no-ops.

Deduplicate the selection before counting. Validate all permissions, pending-source checks, revisions and assignment eligibility, then apply atomically; on any failure change none and return indexed resource errors only for resources the caller may see. Use the existing sorted lock order. No unbounded Apply to all matching results operation, bulk note edits, or cross-tenant command in the initial API. This does not change the separate partial-acceptance policy for source batches or the complete-set policy for automatic correlation.

### 28. Acceptance

See [required alerts checks](../verification/verification-plan.md#alerts).
