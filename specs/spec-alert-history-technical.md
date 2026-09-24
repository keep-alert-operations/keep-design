# Alerts and history technical design

Shared CEL, PostgreSQL records, ordered processing, search, live updates and protected deletion. Product behavior is defined in [Alert operations](./spec-alert-operations.md).

## 1. Authority and implementation boundary

Keep the Python backend, PostgreSQL authority, Elasticsearch current-alert projection, Kafka delivery and Redis/SSE live hints. No new independently operated query service, full-history search index or event-sourcing authority is introduced. PostgreSQL remains sufficient to recover accepted application work when transport messages disappear.

Use separately deployable application workload roles for ingress, Product API, outbox relay, source processing, correlation, search projection and scheduling/cleanup, sharing versioned Python packages/images with role-specific entrypoints. Keep network publication/indexing out of the ingress request process. Replica counts, resource placement and allocations follow the OpenShift team's supported model and measured profile.

Appchi owns its schemas, query/compiler code, transactions, worker protocol, migrations and client behavior. Dedicated teams supply service versions, supported capabilities, credentials, capacity, durability and recovery interfaces; they retain infrastructure retention, backups, HA and topology. The user's team-owned Keycloak remains the already-selected identity-service ownership exception. All numerical application settings below are selected defaults or qualification requirements, not measured throughput or imposed infrastructure settings.

## 2. CEL compiler and runtime

Select `cel-expr-python`, the CEL project's Python wrapper around its C++ implementation, embedded in the Python application. Pin a tested package/native-runtime/protobuf combination in the application lock/build manifest. Use its parsed/checked protobuf expressions to build a small Appchi typed intermediate representation (IR). The wrapper supplies compile/type-check/evaluate operations; its serialized expression is a protobuf `Any` carrying a parsed or checked expression. These integration facts are documented in the [project](https://github.com/cel-expr/cel-python) and [expression implementation](https://github.com/cel-expr/cel-python/blob/main/cel_expr_python/py_cel_expression.cc).

The pipeline is source parsing, Appchi field/operator/type/size validation, null/presence lowering, checked compilation of the lowered program, and either native evaluation or Elasticsearch translation from the same IR. Parse-only output may be inspected but is never executed. Lower catalog fields to statically declared internal variables and explicit presence bits; users cannot address those internal variables. Require a boolean checked result. Do not accept client-supplied compiled expressions, disable checking on executable programs, use Python eval/exec, or load arbitrary CEL extensions.

Compile on save/preview and cache immutable programs by environment/catalog/translator versions and source digest. Saved resource revision and tenant remain part of the authorized cache lookup. Cache native programs only within the owning process and bound their memory by the application's qualified allocation. Package upgrades require the equivalence suite and supported OpenShift image/ABI check; no package version is claimed installed or qualified.

## 3. Complete initial searchable language

Select this initial subset, used consistently wherever the resource permits the referenced fields:

| Construct | Contract |
|---|---|
| `true`, `false`, parentheses, `&&`, `\|\|`, `!` | Ordinary boolean composition; no implicit truthiness. |
| `==`, `!=` | A catalog scalar compared with a compatible literal, including null; constant comparisons may fold. No field-to-field comparisons. |
| `<`, `<=`, `>`, `>=` | Integers or timestamps compared with compatible constants/time bounds. String/enum/boolean ordered predicates are excluded; table sorting keeps its separately selected order. |
| `in` | Scalar membership in a homogeneous literal list; nullable lists may additionally contain null. Feed-only literal UUID membership in `alert.incident_ids` is also supported. |
| `startsWith`, `endsWith`, `contains` | Case-sensitive literal string operations on approved string fields; arguments must be literal strings. |
| `has(alert.field)` | True exactly when an approved scalar field has a non-null value. Unknown fields are compile errors. |
| `timestamp`, `duration`, `now` | Only the bounded forms in decision 4. |

Reject regex/matches, comprehensions/macros other than the selected presence form, arbitrary maps/objects, collection transforms/indexing, ternaries, numeric arithmetic/conversions, floating-point/unsigned literals, string concatenation and all unlisted functions. No arbitrary source labels are added. Correlation/maintenance keep their existing field whitelist; feed-only occurrence/receipt/suppression/relationship fields stay unavailable to those rules. `incident_ids` supports membership only, not list equality or grouping.

Compare strings as exact Unicode scalar sequences without case folding or normalization. Boolean catalog fields may stand alone in boolean expressions. Enums validate against their published values and support equality/inequality/membership, not string methods or ordered predicates. Integers are signed 64-bit with overflow rejected. Missing approved nullable fields are null: null equals null; null differs from a non-null literal; ordered/string predicates on null are false. Consequently negation of such a false predicate is true. Implement these rules with presence guards in both execution paths rather than inheriting accidental missing-field behavior from either engine. Empty string predicates follow literal string semantics for present values; they remain false on null.

## 4. Dates, durations and the query clock

Use RFC 3339 timestamp literals with an explicit `Z` or numeric offset, valid years 0001–9999, no leap seconds and at most six fractional-second digits. Normalize the literal to a UTC instant without altering stored source text. Native source `time_created` retains its previously selected `DD-MM-YYYY HH:mm:ss` input format; query literals do not change ingestion.

Allow nonnegative duration literals composed of integer hours, minutes and seconds, with optional microsecond-precision fractional seconds, such as `24h` or `1h30m0.5s`; maximum 3,652,500 days. Permit a timestamp literal or feed-only `now()` plus/minus one literal duration. Reject an out-of-range resulting instant. No field arithmetic or nested arithmetic is supported. Constant time expressions may be used in rules; `now()` and any moving clock are forbidden in maintenance/correlation conditions so time passing cannot manufacture an unjournaled condition transition.

For a new feed/count snapshot, capture one PostgreSQL UTC time and bind every `now()` to it. Reuse that instant across rows, exact total and every page of the snapshot. Return `evaluated_at`; a refresh starts a new snapshot/time. Foreground live first pages and count views with a relative expression schedule a fresh query at least once per second when no request is in flight, coalescing pending ticks. Historical pagination retains its captured time and shows that newer results may exist. This chooses a moving live view and a fixed pagination snapshot, without introducing a saved preset time-range field or dashboard time picker. A confirmed untrusted authoritative clock makes relative queries unavailable until clock health recovers; fixed-time queries may continue with the degraded-clock indication. Never substitute the browser clock.

## 5. Limits, cost and failure handling

Bound each expression to 16 KiB UTF-8, 256 AST nodes after macro expansion, depth 32, and 100 members per literal list. Validate the source-size bound before parsing and reject unsupported syntax before execution/translation. Literal text is additionally constrained by that source envelope, not silently truncated. Bound compiler jobs to one second in a replaceable worker process; exhausting that wall-time guard is a visible validation-service failure, not proof that a valid expression is false.

Define deterministic cost accounting as AST visits plus scalar comparisons, with string comparison/matching charged by conservative operand-byte work and list membership by its comparison work. Use catalog maximum lengths to compute an upper bound for rule inputs. Record a versioned cost-model ID. The per-expression and aggregate rule/group/evidence capacity budgets must be supplied by the already-required measured N1 profile; do not fabricate a qualified numerical budget or reinterpret the 50/100-rule test scenarios as product caps. Missing qualified budgets gate automatic-query readiness, while durable ingestion retains its independent backlog contract.

A user query failure returns diagnostics or unavailable results, never a broader filter or false zero. Correlation deterministic evaluation/cost failures retain the selected blocked-rule/fresh-restart behavior. If maintenance suppression cannot be established, retain pending affected work and block its unsafe state transition rather than treating the condition as false or clearing existing suppression. Process crashes roll back and retry from authoritative state. No expression performs network, filesystem or database calls.

## 6. Elasticsearch translation and mappings

Use explicit strict mappings and stored `_source`; do not depend on dynamic keyword defaults or synthetic source to preserve original values. Translate typed IR to parameterized bool/term/terms/range/exists queries, escaped literal prefix/suffix/substring patterns and constant filters. No user query-string DSL, Elasticsearch scripts, runtime fields or application-wide post-filter scan is permitted. Wrap the compiled query in mandatory tenant, live-document and suppression filters.

IDs/enums and bounded identifiers use keyword fields; booleans use boolean and counts/versions use long. Give sortable nullable fields an explicit missing flag, ascending in either sort direction. Severity uses a clear/missing-last flag followed by the selected urgency rank. Store a dedicated keyword alert ID for the final tie-break; do not sort on Elasticsearch `_id`.

Map timestamp search/sort values to signed epoch-microsecond longs, with the original ISO UTC string retained for presentation. This preserves both microseconds and the admitted years 0001–9999; Elasticsearch's `date_nanos` has a narrower range and ordinary `date` has millisecond precision. See [Elastic's date documentation](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/date_nanos).

Use wildcard representations for literal string matching, including the message's possible 8,192 four-byte characters. Bounded sortable identifiers fit exact keyword/doc-value fields under the existing source limits. Set mapping length limits explicitly so every accepted value is indexed; never silently ignore a valid long message. Equality on a wildcard representation is an exact-value query, and wildcard metacharacters in user string literals are escaped. Elastic documents the [keyword byte limit and wildcard representation](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/keyword).

For plain-text `q`, tokenize Unicode letter/mark/number/underscore runs, apply default Unicode full case folding without source normalization, discard separators and require every distinct token across message, impact and current undeleted note text. Version the Unicode/tokenizer profile. Persist searchable tokens as a derived keyword projection; words from deleted/old note revisions do not remain searchable. Derive the maximum possible normalized query-token size from the pinned Unicode profile and the existing 256-code-point q bound. Omit only larger source tokens that no valid q token can equal; this avoids keyword limits without changing a supported match or truncating source text. An all-separator nonblank query is invalid, not match-all. CEL remains case-sensitive and has no note-text input.

## 7. Query versions and migration

Name the first application profile `appchi-cel-v1`; its version covers field types/null semantics, allowed syntax, time rules, cost model, text tokenizer and Elasticsearch translator/mapping compatibility. Preserve source and environment version in each saved definition. Keep source-span mapping through lowering for useful diagnostics. Ship a common conformance corpus for feed search, preset preview, rule testing and rule execution.

Before changing the profile, compile every active saved expression and compare old/new results over the boundary corpus and a retained-data sample. Block activation of incompatible resources until a reviewed migration or supported old execution profile exists. An equivalent compiler/index optimization does not reset correlation evidence; a genuine rule-logic/profile semantic change uses its existing revision/reset boundaries and no backfill. Never re-evaluate history as new source events. Keep old compiler/mapping readers while protected active work needs them; retire them only after all references are cleared.

## 8. PostgreSQL physical record families

Use ordinary relational columns for identities, scope, state, order, revisions and timestamps; JSONB only for versioned snapshots/configuration/provenance and bytea for exact admitted customer bytes. PostgreSQL timestamptz stores instants; checks reject infinity and out-of-contract years. The alert catalog remains the complete current-state column contract, with internal lifecycle/job fields kept out of customer inputs.

| Record family | Selected keys and purpose |
|---|---|
| `alert_identities` | UUID primary key; tenant, retirement state/final version and minimal purge evidence. Stable target for surviving references. Unique `(tenant_id,id)` supports scoped foreign keys. |
| `alerts` | UUID primary/foreign key to identity; typed current catalog, occurrence pointer, semantic/projection versions, last source activity and retention deadline. |
| `alert_key_claims` | Primary key `(tenant_id,schema_version,key_digest)`; exact key/canonical identity material and unique live alert ID. Compare full material after digest lookup; a digest collision is a conflict, never a merge. |
| `ingest_requests`, `ingest_items`, `ingest_retry_keys` | Request/event UUID identities, exact retry scope/content digest, receipt protection, tenant admission order, pending payload and terminal outcome. Event UUID is globally unique at admission. |
| `alert_source_events`, `alert_occurrences`, `alert_activity` | Parent UUID plus event/occurrence/activity UUID keys; source receipt order versus canonical activity order, exact admitted bytes/parsed values and required provenance. |
| `alert_notes`, `alert_note_revisions`, `alert_suppression_history` | Parent-scoped current notes and immutable note/suppression changes. |
| `alert_active_ownership` | Unique `(tenant_id,alert_id)` active claim; incident/context uniqueness remains the existing incident/correlation contract. |
| `alert_command_results` | Actor/tenant/alert/command identity, request digest and committed result; selected parent lifetime. |
| `tenant_work_state`, `application_outbox`, `consumer_progress` | Coordinator/order counters, ready state/leases, immutable events/full snapshots and required consumer acknowledgements. |
| `tenant_view_state`, `projection_progress` | Separate live generations and per-index-epoch search progress. Updating these rows never requires taking a coordinator after a domain row lock. |
| `alert_purge_jobs`, `recovery_evidence` | Eligibility/version checks, protected intent/final fence references, chunk progress and sanitized outcomes. |

Successful application moves exact payload/provenance into applied source history and releases the redundant pending payload in the same transaction. Rejected admitted payloads remain separately labeled diagnostics, with their existing 90-day retention. Requests, item retry associations and alert commands keep their distinct existing lifetimes; do not extend external idempotency indefinitely or expire pending work to match a receipt deadline. Immutable surviving references point to `alert_identities`, not a parent row that physical cleanup must retain forever.

## 9. Partitioning and indexes

Keep current alerts, identity/key registries, active claims, ready work and command lookup tables unpartitioned initially. Hash-partition the large source-event, activity, note-revision, suppression and occurrence histories into 32 partitions by alert UUID; partitioned primary/unique keys include that UUID. This distributes even a single busy tenant's many alerts and prunes parent-history reads. Do not drop time partitions to enforce retention: an old event can belong to a still-retained alert. PostgreSQL requires partition keys in partitioned uniqueness constraints; see [partitioning documentation](https://www.postgresql.org/docs/current/ddl-partitioning.html).

Add B-tree indexes for `(tenant_id,alert_id,admission_order,event_id)` source pages; `(tenant_id,alert_id,change_order,activity_id)` activity pages; parent/note/revision lookups; pending `(tenant_id,admission_order)`; pending target-key lookup; ready job `(next_attempt_at,id)`; outbox `(tenant_id,stream,stream_order)`; and live operator/assignee/ownership lookups. Use partial due indexes for active inactivity checks and resolved retention deadlines. Use the exact tenant/version/key digest uniqueness above, rather than indexing potentially large canonical identity material. Query note/source payload JSON through explicit detail reads, not a blanket JSONB GIN index.

Partition count and indexes are an application-schema baseline to measure, not a service replica/shard allocation. Expand partitions through a checked application migration when justified; service teams own physical resource allocation, vacuum/backup operation and capacity.

## 10. Transactions, locks and tenant isolation

Use READ COMMITTED with explicit row locks for mutations. Preserve the common domain order: tenant coordinator, sorted rule IDs, full context keys, incident IDs, then alert IDs. Source admission, source application, ownership/reset decisions and logical purge take the same coordinator. Never acquire it after a domain row lock. Validate mutation authorization under the existing access-version guard; avoid holding transactions across external service calls.

Use `FOR UPDATE SKIP LOCKED` to claim ready tenants/jobs, never to skip an earlier source item within one tenant. Persist ten-second leases, renew every three seconds and require matching lease generation/deployment epoch at commit. Leases schedule work; PostgreSQL locks and predicates establish correctness. Read a consistent parent/history page in a short transaction and release it before returning a browser cursor.

Enable and force tenant row-level security on human-facing tenant tables, in addition to Product API authorization. The Product API role is neither table owner nor BYPASSRLS; set transaction-local tenant context only after authenticated route authorization and clear it with the transaction. Use composite tenant foreign keys and trusted scope on every join. System workers use a separate limited role/claim path, never the human request connection role. RLS is defense against omitted predicates, not a substitute for the LDAP/access policy or a defense against a compromised trusted backend. PostgreSQL documents [owner/bypass behavior](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

## 11. History reads and detail contracts

Use keyset history pagination, default 50/max 200, with opaque authenticated 15-minute cursors fixing an upper committed order watermark. Bind cursors to tenant, alert, collection, sort direction, filters and current deployment epoch. Reauthorize and recheck retained parent/content on each page. New events appear on refresh; expired parents/history cannot be recovered through an old cursor. No long-lived PostgreSQL transaction is held for pagination.

Activity defaults newest first by canonical change order and UUID; source events default newest first by original admission order and event UUID. Support existing ascending mode, optional occurrence ID, activity-kind filters and an explicit inclusive `from`/exclusive `to` UTC interval. Label activity filtering by recording time and source filtering by receipt time; display effective/source time separately. No default short date window conceals older retained history.

Collection pages contain metadata/summaries, not 200 embedded raw payloads. Add `GET /api/tenants/{tenant_id}/alerts/{alert_id}/source-events/{event_id}` for a retained applied event's exact UTF-8 `raw_json` string, parsed values and provenance. It uses current tenant read permission and the retained-parent guard. Unattached rejected admissions remain receipt/diagnostic records and never masquerade as applied alert history. No bulk raw-history export is introduced.

## 12. Durable processing and fairness

Continue acknowledging ingress only after atomic PostgreSQL admission. A worker takes the next pending tenant admission, applies it once and commits outcome/current state/history/occurrence/correlation journal/outbox together. Event IDs, admission time/defaults and source order never change on retries. Unchanged valid repeats keep source history and receipt/inactivity effects without becoming semantic transitions.

Recover ready work with the existing one-second scan, independent of Kafka wakeups. Yield between complete atomic units after 100 events or 100 milliseconds, as already selected. One blocked tenant does not block another. Pending manual-target inputs continue to cause the selected conflict; a manual write cannot leap over them. Correlation reads its ordered PostgreSQL before/after journal, not an Elasticsearch result or a presumed Kafka order. Maintenance producers must establish current suppression and original effective-transition proof before correlation acts; unproven maintenance boundaries block unsafe work rather than create eligibility.

## 13. Kafka topics and event encoding

Select environment-scoped topics `appchi.{environment}.alerts.received` and `appchi.{environment}.alerts.changed`, keyed by immutable tenant UUID bytes. Use separate processor, projection and correlation-wakeup consumer groups. Partition count, retention and broker settings come from the Kafka team; changing partition allocation requires draining/fencing Appchi writers and reconciling PostgreSQL progress, never assuming old/new broker ordering is sufficient.

Use a versioned UTF-8 JSON envelope with internal schema version, event/kind/tenant IDs, original admission proof where relevant, change order, projection sequence/version, actor/cause, effective/recorded times and immutable payload digest/reference. Serialize once and persist those exact bytes; retransmissions reuse them. Native v1/v2 source versions are separate fields, not internal envelope versions. Transport order/version counters use decimal strings to preserve full 64-bit values in consumers.

`alerts.received` references its authoritative admitted record. `alerts.changed` represents a complete immutable searchable snapshot or retired-ID marker, never an ambiguous patch. Inline snapshots up to 256 KiB when the supplied broker limit permits; otherwise use an envelope under 8 KiB referencing the immutable PostgreSQL snapshot plus digest. This is a wire-encoding refinement of the existing full-snapshot contract, not permission to fetch whatever state happens to exist later. Required consumers keep the referenced snapshot protected until completion. No API keys or authentication tokens enter either topic.

## 14. Relay, acknowledgements and retries

Use PostgreSQL outbox relays with leased tenant/stream ownership and ordered publication. Select idempotent Kafka producers, `acks=all`, and at most five in-flight requests, subject to the supplied supported client profile. Those settings reduce broker duplicates but do not make PostgreSQL/Kafka one transaction; the [Kafka producer contract](https://kafka.apache.org/41/configuration/producer-configs/) is distinct from Appchi's event-level deduplication.

After durable publication acknowledgement, record publication progress. A crash between publish and that record republishes the same event. Consumers disable automatic offset commits: first record receipt/progress durably or complete the idempotent PostgreSQL effect, then advance broker offsets. The processor still drains the tenant inbox in admission order; a late Kafka hint cannot change ordering. A projection consumer may durably enqueue referenced work before committing its broker offset because the work remains recoverable in PostgreSQL.

Retry transient worker/relay failures with full jitter and exponential delays starting at one second, capped at 30 seconds. Preserve alert operations 13's source-head exception: after ten consecutive processing failures, mark that tenant blocked and require an audited global-super-admin retry after repair, resuming the same item/order. Relay/projection retries continue while required work remains; blocked source work remains durable and is never skipped. Database conflicts/deadlocks retry from fresh state, within an interactive request's remaining deadline or the durable job loop.

Deterministic incompatible events or missing authoritative proof are quarantined with a visible affected-tenant/stream block, not acknowledged as applied, dropped into a dead-letter queue and forgotten, or bypassed. Cleanup requires every registered required consumer and reconstruction/proof hold to release the event; Kafka publication/offset alone is insufficient. The required consumers are source application for received work and search projection for changed work. Correlation retains its separate journal/cursor proof; its Kafka wakeup acknowledgement is not that proof.

An active rebuild registers an additional durable hold, including for newly created tenants, until completion or fenced cancellation. Live notification outbox records can complete after publication because the durable view-state reconciliation recovers missed hints.

## 15. Projection ordering and deletion markers

Allocate a separate transactionally monotonic per-tenant `projection_seq` for every committed searchable snapshot, including unchanged receipt updates. Keep it distinct from original admission order, semantic change order and per-alert projection version. Index workers use PostgreSQL pending projection work; Kafka remains a wakeup/transport path.

Batch up to 500 documents, 4 MiB or 100 milliseconds of accumulated work, whichever is first. One oversized complete document is handled separately within the supplied service limit; if that limit cannot represent accepted content, block/report projection capacity rather than truncate history/notes or claim a fresh result. Keep unacknowledged snapshots durable. Projection work may collapse intermediate snapshots of the same alert to a verified newer complete snapshot, recording coverage of the replaced sequences; source processing/history/correlation never collapse events this way.

Use alert UUID as Elasticsearch document ID with default ID distribution, not tenant-only routing that puts all Global traffic on one shard. Use `external_gte` projection versions only with immutable identical bytes for equal versions. Reject inconsistent equal-version content and verify newer-version conflicts against authoritative coverage. Before retries, check retired identities and active index epoch. Elasticsearch describes the [equal-or-newer version behavior and its cautions](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-index).

Logical deletion writes a higher-version minimal `deleted=true` document containing only tenant/alert identity and final version. All product searches require `deleted=false`. Keep these small markers for the serving index's lifetime; do not depend on a short-lived Elasticsearch delete-version cache to stop delayed writes. A rebuild may omit retired IDs only because PostgreSQL fences and epoch-checked writers prevent their recreation. Underlying segment/backup erasure remains the owning team's operation.

## 16. Searchable progress and refresh proof

Issue projection bulk writes with `refresh=wait_for`. Do not force a refresh per alert. Confirm every item succeeded or is covered by an already-search-visible identical/newer version, with no shard failures/timeouts; verify uncertain conflict/retry cases through search, not a realtime GET. Elastic distinguishes write acknowledgement from [refresh visibility](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/refresh-parameter).

Persist a contiguous per-tenant `searchable_seq` only when every required sequence through that point is covered by visible state or a visible retired marker. A failed hole prevents advancing past it. A later complete snapshot may cover older versions of that same alert, but never another alert's hole. Record the index epoch and verification time. The Elasticsearch service's supplied refresh behavior must support the five-second end-to-end target; confirm it through integration/measurement rather than independently changing service policy.

Commit the new progress, live generation and notification outbox atomically. Consequently a Redis/SSE search invalidation means the reported progress is searchable. Authoritative detail/history/configuration invalidations can occur earlier, with their separate committed generation; the browser must not infer search freshness from them. Return committed/searchable positions and verified time in search responses. A watermark is a lower bound on covered changes, not a claim that no newer document was visible in the query snapshot.

## 17. Search snapshots, counts and purged IDs

Use Elasticsearch point-in-time (PIT) plus `search_after` and the selected sort/tie-break, with an absolute five-minute Appchi cursor lifetime. Set each PIT keep-alive no later than the remaining application lifetime, carry the newest returned PIT ID, close it on disposal when possible, and let it expire after abandoned views. A successful first-page live refresh disposes the replaced PIT after accepting the new result; do not accumulate five minutes of abandoned PITs on every one-second refresh. A snapshot still being traversed retains its own lifetime. The [PIT pagination contract](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/paginate-search-results) preserves a stable traversal.

An authenticated cursor contains/binds tenant, session/principal visibility scope, index/environment epoch, effective-filter digest, sort, captured query time, latest PIT ID, last sort tuple and expiry. Protect it using authenticated encryption with the existing approved application secret mechanism; never expose a raw client-editable Elasticsearch request. Query changes/expiry/retired index restart traversal. Reauthorization can invalidate an otherwise live snapshot.

Capture the verified searchable vector before opening a new PIT and recheck its epoch afterward. Report at most that pre-PIT verified lower bound; reading a newer watermark after opening the PIT cannot make its older snapshot fresh. Return a newer observed vector separately as a reason to refresh, never as a rendered acknowledgement for that snapshot.

Request exact total hits and reject partial-shard/time-limited results as unavailable; row and total filters/time/PIT must agree. Batch-check returned IDs against PostgreSQL retained-identity state, not one database request per row. Omit logically purged IDs even in an older PIT. Advance its cursor by the last examined Elasticsearch hit, not the last surviving row; an empty filtered page may still have a continuation. Do not perform an unbounded scan to fill holes. If purge generation advanced after that PIT opened, mark its total updating/unavailable until a fresh snapshot is obtained; do not subtract only the purged IDs found on the current page and call that an exact total. This preserves the existing purge and count contracts without scanning all retained alerts in Python.

## 18. Durable live state and SSE protocol

Select `GET /api/tenants/{tenant_id}/events` using the existing same-origin session cookie. Events carry hints/progress, never alert bodies, credentials or unrestricted tenant lists. Persist a tenant view-state row with deployment/index epoch, monotonic `view_generation`, committed projection sequence, searchable sequence, authoritative-resource generation and purge generation. Domain commits and verified search progress update the appropriate fields plus durable outbox in the same transaction.

Use Redis Pub/Sub for low-latency fan-out. Every API replica also reconciles PostgreSQL view-state for its connected tenants every two seconds, coalescing reads across connections. Redis loss therefore delays a hint but cannot lose the current generation or make authorization depend on Redis. Select SSE event names `state`, `invalidate` and `resync`, with the full small current vector and scoped changed-resource categories. Event IDs encode epoch/generation; they are hints, not access credentials.

On connect/reconnect, reauthorize, register local delivery, read current PostgreSQL state and send a `state`/`resync` event. Accept Last-Event-ID only as an observed-generation hint. An epoch mismatch, unknown/future ID or missed history causes a complete current-state resync. Do not maintain or promise replay of every transient SSE message; replaying the latest durable invalidation state is sufficient because actual data is refetched. Periodic reconciliation closes subscribe/read races.

## 19. Browser refresh, reconnect and relative time

Coalesce live invalidations for 250 milliseconds, with at most one request in flight per visible resource and one pending refresh. Foreground feeds on the first page refresh; a user traversing older snapshot pages gets a New results available indicator instead of inserted/reordered rows. Refresh visible alert details/history, preserving unsaved notes and older-page position; show new activity rather than overwriting a draft. Preset clean/dirty behavior remains its selected contract. Visible count panels consume searchable generations; dashboard completion 4/9–12 selects its specialized batching/layout.

Use exponential SSE reconnect delays of one, two, four, eight and at most 30 seconds with jitter; reset after a stable connection. Reconnect/refocus refetches generation and visible data before calling the view current. Detect a missing heartbeat after 30 seconds. During a disconnected foreground view, poll authorized view state every two seconds and refetch when it changes; expose live delivery as degraded even when polling obtains fresh data. Pause data polling/relative-time refresh while hidden, close a hidden tab's stream after 60 seconds, and fully reconcile on return. A background tab does not extend authentication.

Relative-query one-second ticks in decision 4 operate even without data changes, with the same in-flight/coalescing rules. Existing session activity uses its separate 60-second foreground heartbeat. Normal five-second incoming/maintenance visibility remains an end-to-end p99 objective; polling, indexing and rendering must be included in qualification rather than adding their individual percentiles as a proof.

## 20. Stream security, bounded delivery and proxy contract

Authorize the tenant at stream open, before each protected hint and at least every 30 seconds. End expired/revoked sessions and lost-tenant delivery, including metadata hints. Preserve permitted reads after edit/admin loss. Recheck against PostgreSQL grants/sessions and the accepted identity checkpoint; no stale effective-role cache or new identity-age cutoff is introduced. If authorization authority is unavailable, stop protected delivery. Use same-origin validation and no cross-origin credentialed streams.

Send a comment heartbeat every 15 seconds; it contains no tenant data and does not count as user activity. Bound each connection to one coalesced pending state vector and 64 KiB of transport buffering; disconnect slow clients and require resync rather than accumulate an unbounded event queue. Maintain one stream per active tenant/tab. Include stream counts and memory in the qualified client profile instead of introducing a new user-access cap.

Request no intermediary response buffering/cache/compression that delays flushes, a 75-second or greater idle timeout, and a 30-minute application stream lifetime followed by reconnect. Keep finite ordinary API timeouts unchanged. These are Appchi's OpenShift/Kong integration requirements for the owning teams to confirm, not settings changed by this design. SSE setup uses ordinary 401/403/404/503 behavior before headers; after opening, close on loss of authority and let the client reconcile its session.

## 21. Rendered acknowledgements and freshness

Add `GET /api/tenants/{tenant_id}/view-state` for the authorized durable vector and `POST /api/tenants/{tenant_id}/view-observations` for sampled render acknowledgements. The latter accepts at most 100 observations and 64 KiB per request, with session-bound server-issued observation IDs, resource/view/query digest, observed versions/generation and outcome. It uses normal CSRF/tenant checks. These endpoints do not update the user's activity clock.

Return observation IDs with eligible view responses. The browser acknowledges after rendering the matching data or the confirmed nonmatching result for that query, not after merely receiving an SSE hint. Validate acknowledgements against server-issued scope/version bounds; duplicated or impossible future acknowledgements cannot manufacture success. Use server receipt time as the conservative completion bound. Preserve the reliability supplement's 10% incoming observation sampling, all maintenance-expiry observations and full qualification instrumentation. Missing acknowledgements remain misses/coverage gaps; the browser is not authority for alert state.

Show last successful fetch/evaluation time, projection lag and live/disconnected state separately. An empty correct result is zero; an unavailable result is unavailable. Operational observations use the agreed telemetry retention, not a new product history lifetime.

## 22. Alert and history screen organization

Select alert-detail sections Overview, Activity, Source events, Occurrences and Notes, sharing the same tenant/alert identity. Overview shows current state, acknowledgement/assignee, suppression causes, incident links and current source fields. Activity shows meaningful source/user/system changes and original effective time beside recording time; unchanged received repeats belong in Source events rather than fabricated semantic activity. Occurrences expose lifecycle cycles without splitting the logical alert identity.

Show note revisions/deletions and actor snapshots under Notes/history while primary notes/search use current undeleted text. Source event detail renders escaped plain text/JSON and supplied-versus-defaulted time provenance; it never executes payload content or fetches runbook URLs. Distinguish loading, empty history, unavailable dependency, expired resource and late processing. User commands apply their authoritative response immediately and show search updating until the response's projection sequence is covered. Keep existing edit permissions and no manual alert Delete action.

## 23. Logical purge and bounded physical cleanup

Keep the hourly retention eligibility scan, 30-day inactivity policy and 90-day post-resolution lifetime. Under the coordinator, recheck latest resolution, current revision, pending target inputs and protected dependencies. Prepare a versioned purge intent without releasing the live identity. Protect that minimal intent through decision 24, then reacquire the coordinator and recheck eligibility. If changed, cancel it; if still valid, atomically retire the alert, make parent-owned content inaccessible, release live key/ownership claims and commit the final tombstone, deletion snapshot, purge job and live generation. A later firing admission may create a new UUID under the same logical key, as already selected.

This refines the earlier atomic-purge wording: **visibility/identity retirement is atomic; physical removal of large history is resumable**. It does not shorten retention or allow partially visible history. Every detail/history route joins the retained-parent guard. Surviving incident references become unavailable identity/provenance only; cleanup never deletes incidents or counterpart content. No new raw input can attach to a retired UUID.

After the final minimal fence is independently protected, delete payload/history/outbox content in chunks of at most 1,000 rows or 100 milliseconds of work, yielding between transactions. Keep stable identity fences and the existing 90-day post-purge external item-retry associations; expired external retry IDs may later be reused under the original API contract. Protect outstanding consumer/proof dependencies before removing their payloads. Target physical application cleanup within 24 hours of eligibility and released holds under normal supplied capacity; measure it, and report delayed jobs rather than dropping proof or claiming erasure from backups/segments.

## 24. Protected evidence and restore readiness

Define a recovery-evidence adapter supplied through the owning teams' supported storage interface: idempotent append of immutable intent/final/cancel records, durable acknowledgement, ordered namespace/checkpoint enumeration and integrity verification independently of the database recovery point being restored. Minimal alert evidence contains tenant/alert UUID, intended/final projection version, evidence ID/state/order and integrity metadata, never source bodies, note text or actor display names. Appchi chooses this contract; it does not choose the team's backup product, schedule or topology.

Protect an intent before final logical retirement so a crash/rollback cannot erase every trace of a potentially completed purge. Protect its final fence before physical content cleanup. On restore, a committed final fence forbids resurrection; an unresolved protected intent fences that identity for reconciliation rather than guessing that deletion either completed or never happened. A canceled intent requires trusted cancellation/eligibility evidence before release. If the adapter is unavailable, keep eligible content logically unavailable when its retirement has committed, hold physical cleanup and show protection failure; do not claim the retention job completed.

Keep minimal retired-ID fences indefinitely in the initial release. There is no automatic age-based compaction and no required finite replay-horizon guess. After rollback restore, use a fresh independently established deployment epoch, reconcile current evidence/pending orders/consumer progress, apply product retention and rebuild/verify projections before reopening affected reads. Preserve the separately selected fresh-SSO/directory/grant reconciliation and operator credential rules. Unknown evidence gates affected paths. The supplied evidence endpoint, guarantees and exercised recovery remain integration/qualification deliverables.

## 25. Search rebuild and index switching

Use a new physical index and immutable index epoch behind the application read/write alias. Register a durable rebuild hold before opening a consistent PostgreSQL snapshot, then capture its per-tenant projection positions and copy retained current alerts/notes. Serialize hold registration with outbox cleanup so no required gap can be purged; newly created tenants inherit the active hold. Copy in bounded keyset pages, then apply subsequent complete snapshots/retired markers in order until caught up. This rebuild never replays source lifecycle, resolves/reopens alerts or runs correlation actions.

Validate per-tenant live IDs, versions, representative query/count parity, mapping/profile compatibility and retired-ID exclusion. At cutover, fence index writers, drain in-flight old-epoch work and capture a per-tenant cutover position. Make the replacement search-visible through those positions before recording its verified progress/new epoch and switching the alias through the team's supported atomic operation. Canonical ingestion may continue, with later snapshots queued for the new epoch. If switch/control-state outcome is uncertain, gate search until reconciled; authoritative ingestion can continue with durable projection backlog. Resume current-epoch writers and emit resync. Old PIT cursors receive `409 index_changed` and restart. Keep the previous index available for controlled repair until readers/work are released and the team performs its normal cleanup; no infrastructure retention duration is imposed.

## 26. Schema, event and application rollout

Use checked-in SQL migrations with an ordered application schema version. Apply expand/backfill/validate/contract changes through the database team's supported change process. Backfills use small resumable transactions and the selected tenant/order/version guards. Build supporting indexes using the supported online method and measure lock impact; do not independently change the database's operational policy.

Roll out readers of both old/new internal envelope versions before changing writers. Unknown major versions remain protected and block the affected consumer visibly. Switch writers with a durable epoch boundary, drain old pending work and only then remove old readers/columns/mappings. Application rollback must remain able to read committed data; never roll back by restoring an old database or lowering projection versions. Native v1/v2 ingestion remains concurrently supported and its identity formats unchanged. No historical enriched import or cross-version identity merge is added.

## 27. Operational diagnostics and retention

Expose per-tenant pending-head age, ordered processing/correlation lag, outbox age, committed/searchable sequence gap, blocked projection IDs, native query errors/cost, SSE reconciliation/reconnects, render coverage and purge/evidence hold age. Avoid source values/bodies/secrets as metrics/log labels. Access to tenant-visible status follows current tenant permission; privileged global repair remains an operational role with the existing protected audit destination, not a new end-user bypass.

Keep completed alert purge-job summaries and repair-attempt records for 90 elapsed days after completion, with IDs, outcome, timing and dependency reason only. Required pending work/fences persist longer; resource content/actor snapshots follow their existing parent lifetime. Operational logs/metrics/traces remain governed by their owning teams. Do not add product notifications; use the already selected company operational escalation mechanisms. Repairs must record proof and preserve ordering/identity, not offer Skip accepted alert or Replay history as new deliveries.

## 28. Supplied capability and readiness gates

Before enabling each dependent path, verify the supplied PostgreSQL partition/locking/RLS capabilities, Elasticsearch PIT/wildcard/external-version/refresh/alias behavior, Kafka record/client limits and Redis/proxy connectivity against the selected contracts. Pin the deployed versions and record authenticated endpoints, supported timeouts, allocation and recovery-evidence handoff. Obtain values from the owning teams; do not invent them or silently switch engines when incompatible.

Separate admission, authoritative Product API, source processing, correlation, search and live-delivery health. Search outage does not disable valid PostgreSQL admission; missing automatic-evaluation budgets/proof blocks the affected unsafe work. Use the existing global/per-tenant item/byte admission budgets and 429/503 behavior. Extend measured allocation accounting to pending projection snapshots and retained source/history growth; apply backpressure before allocation is exhausted, without deleting accepted work. The existing recovery-throughput and one-tenant stress requirements remain unchanged.

## 29. Qualification and acceptance evidence

See [required alert execution and recovery checks](./verification-plan.md#alert-execution-and-recovery).
