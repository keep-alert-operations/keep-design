# Alerts and history technical design

**Later user decision — 2026-10-24 (REV-39):** correlation and maintenance are always on, with no capability gate. Their CEL and capacity budgets are optional numbers; an unset budget is unlimited. Missing proof still blocks unsafe processing, and an alert without a current maintenance checkpoint still fails reads with `maintenance_proof_unavailable`. See the [design register](../decisions/design-register.md#rev-39--always-on-correlation-and-maintenance-2026-10-24).

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

The 2026-09-30 [Kafka-first pipeline](spec-kafka-alert-pipeline.md) governs alert transport, gateway admission, UTC ordering, manual correlation, search reconciliation and cutover (REV-33). Unrelated product behavior remains unchanged.

Shared CEL, PostgreSQL records, ordered processing, search, live updates and protected deletion. Product behavior is defined in [Alert operations](spec-alert-operations.md).

## 1. Authority and implementation boundary

**Current scope (REV-34, REV-37):** No scheduling or cleanup workload role is deployed, and each service has its own entrypoint and image; see [worker scope](spec-worker-scope.md#5-nice-to-have-components) and [repository layout](spec-repository-layout.md#package-and-runtime-boundaries). The authority and ownership rules below remain normative.

Keep the Python backend, PostgreSQL authority, Elasticsearch current-alert projection, Kafka delivery and Redis/SSE live hints. No new independently operated query service, full-history search index or event-sourcing authority is introduced. PostgreSQL can reconstruct committed alert/search state; accepted but unprocessed Kafka inputs can be lost on retention expiry.

Use separately deployable application workload roles for ingress, Product API, Kafka source processing, correlation, search projection and scheduling/cleanup, sharing versioned Python packages/images with role-specific entrypoints. Ingress publishes directly to Kafka; source processing and indexing remain separate workloads. Replica counts, resource placement and allocations follow the OpenShift team's supported model and measured profile.

Keep owns its schemas, query/compiler code, transactions, worker protocol, migrations and client behavior. Dedicated teams supply service versions, supported capabilities, credentials, capacity, durability and recovery interfaces; they retain infrastructure retention, backups, HA and topology. The user's team-owned Authelia remains the already-selected identity-service ownership exception. All numerical application settings below are selected defaults or qualification requirements, not measured throughput or imposed infrastructure settings.

## 2. CEL compiler and runtime

Select `cel-expr-python`, the CEL project's Python wrapper around its C++ implementation, embedded in the Python application. Pin a tested package/native-runtime/protobuf combination in the application lock/build manifest. Use its parsed/checked protobuf expressions to build a small Keep typed intermediate representation (IR). The wrapper supplies compile/type-check/evaluate operations; its serialized expression is a protobuf `Any` carrying a parsed or checked expression. These integration facts are documented in the [project](https://github.com/cel-expr/cel-python) and [expression implementation](https://github.com/cel-expr/cel-python/blob/main/cel_expr_python/py_cel_expression.cc).

The pipeline is source parsing, Keep field/operator/type/size validation, null/presence lowering, checked compilation of the lowered program, and either native evaluation or Elasticsearch translation from the same IR. Parse-only output may be inspected but is never executed. Lower catalog fields to statically declared internal variables and explicit presence bits; users cannot address those internal variables. Require a boolean checked result. Do not accept client-supplied compiled expressions, disable checking on executable programs, use Python eval/exec, or load arbitrary CEL extensions.

Compile on save/preview and cache immutable programs by environment/catalog/translator versions and source digest. Saved resource revision and tenant remain part of the authorized cache lookup. Cache native programs only within the owning process and bound their memory by the application's qualified allocation. Package upgrades require the equivalence suite and supported OpenShift image/ABI check; no package version is claimed installed or qualified.

## 3. Complete initial searchable language

Select this initial subset, used consistently wherever the resource permits the referenced fields:

Reference an approved catalog field by its bare identifier (`application`, `severity`, `display_status`). **Assistant-selected compatibility:** the historical `alert.field` spelling remains accepted, including in retained saved expressions; new editor suggestions and examples use bare identifiers. Bare identifiers do not enable arbitrary variables or expand a context's field whitelist.

| Construct | Contract |
|---|---|
| `true`, `false`, parentheses, `&&`, `\|\|`, `!` | Ordinary boolean composition; no implicit truthiness. |
| `==`, `!=` | A catalog scalar compared with a compatible literal, including null; constant comparisons may fold. No field-to-field comparisons. |
| `<`, `<=`, `>`, `>=` | Integers or timestamps compared with compatible constants/time bounds. String/enum/boolean ordered predicates are excluded; table sorting keeps its separately selected order. |
| `in` | Scalar membership in a homogeneous literal list; nullable lists may additionally contain null. Feed-only literal UUID membership in `incident_ids` is also supported. |
| `startsWith`, `endsWith`, `contains` | Case-sensitive literal string operations on approved string fields (for example, `application.contains("payments")`); arguments must be literal strings. |
| `has(field)` | True exactly when an approved scalar field has a non-null value. Unknown fields are compile errors. |
| `timestamp`, `duration`, `now` | Only the bounded forms in decision 4. |

Reject regex/matches, comprehensions/macros other than the selected presence form, arbitrary maps/objects, collection transforms/indexing, ternaries, numeric arithmetic/conversions, floating-point/unsigned literals, string concatenation and all unlisted functions. No arbitrary source labels are added. Maintenance retains its field whitelist; correlation excludes assignee_id and blocks incompatible saved rules; feed-only occurrence/receipt/suppression/relationship fields stay unavailable to those rules. `incident_ids` supports membership only, not list equality or grouping.

Compare strings as exact Unicode scalar sequences without case folding or normalization. Boolean catalog fields may stand alone in boolean expressions. Enums validate against their published values and support equality/inequality/membership, not string methods or ordered predicates. Integers are signed 64-bit with overflow rejected. Missing approved nullable fields are null: null equals null; null differs from a non-null literal; ordered/string predicates on null are false. Consequently negation of such a false predicate is true. Implement these rules with presence guards in both execution paths rather than inheriting accidental missing-field behavior from either engine. Empty string predicates follow literal string semantics for present values; they remain false on null.

## 4. Dates, durations and the query clock

Use RFC 3339 timestamp literals with an explicit `Z` or numeric offset, valid years 0001–9999, no leap seconds and at most six fractional-second digits. Normalize the literal to a UTC instant without altering stored source text. Native source `time_created` retains its previously selected `DD-MM-YYYY HH:mm:ss` input format; query literals do not change ingestion.

Allow nonnegative duration literals composed of integer hours, minutes and seconds, with optional microsecond-precision fractional seconds, such as `24h` or `1h30m0.5s`; maximum 3,652,500 days. Permit a timestamp literal or feed-only `now()` plus/minus one literal duration. Reject an out-of-range resulting instant. No field arithmetic or nested arithmetic is supported. Constant time expressions may be used in rules; `now()` and any moving clock are forbidden in maintenance/correlation conditions so time passing cannot manufacture an unjournaled condition transition.

For a new feed/count snapshot, capture one PostgreSQL UTC time and bind every `now()` to it. Reuse that instant across rows, exact total and every page of the snapshot. Return `evaluated_at`; a refresh starts a new snapshot/time. Foreground live first pages and count views with a relative expression schedule a fresh query at least once per second when no request is in flight, coalescing pending ticks. Historical pagination retains its captured time and shows that newer results may exist. This chooses a moving live view and a fixed pagination snapshot, without introducing a saved preset time-range field or dashboard time picker. A confirmed untrusted authoritative clock makes relative queries unavailable until clock health recovers; fixed-time queries may continue with the degraded-clock indication. Never substitute the browser clock.

## 5. Limits, cost and failure handling

Bound each expression to 16 KiB UTF-8, 256 AST nodes after macro expansion, depth 32, and 100 members per literal list. Validate the source-size bound before parsing and reject unsupported syntax before execution/translation. Literal text is additionally constrained by that source envelope, not silently truncated. Bound compiler jobs to one second in a replaceable worker process; exhausting that wall-time guard is a visible validation-service failure, not proof that a valid expression is false.

Define deterministic cost accounting as AST visits plus scalar comparisons, with string comparison/matching charged by conservative operand-byte work and list membership by its comparison work. Use catalog maximum lengths to compute an upper bound for rule inputs. Record a versioned cost-model ID. The per-expression and aggregate rule/group/evidence capacity budgets are configurable numbers from the N1 profile; do not fabricate a qualified numerical budget or reinterpret the 50/100-rule test scenarios as product caps. Under REV-39 an unset budget is unlimited and an invalid one fails with `capacity_profile_invalid`; automatic-query readiness is not gated on budgets, and Kafka admission remains independent of processing lag.

A user query failure returns diagnostics or unavailable results, never a broader filter or false zero. Correlation deterministic evaluation/cost failures retain the selected blocked-rule/fresh-restart behavior. If maintenance suppression cannot be established, retain pending affected work and block its unsafe state transition rather than treating the condition as false or clearing existing suppression. Process crashes roll back and retry from authoritative state. No expression performs network, filesystem or database calls.

## 6. Elasticsearch translation and mappings

**Assistant-selected REV-27 compatibility:** `display_status` is a virtual feed field derived from raw `status` and `assignee_id`. Native evaluation and search translation use the same table in alert operations section 17. Translate `acknowledged` to firing AND an existing assignee, `firing` to firing AND no assignee, and `resolved` to raw resolved; inequality/membership/presence compose through the same IR. Page totals and dashboard/preset counts use this same filter. Do not add a physical `display_status` mapping, scripts or runtime fields, or change the existing full-snapshot encoding/digest. Existing indices need no rebuild for this addition.

Keep the previous physical acknowledgement fields and their CEL evaluation intact for retained predicates and immutable evidence. Omit them from current response presentation and discovery. The maintenance/correlation whitelist is unchanged; its accepted legacy programs continue to execute against their original inputs. New rules can express ownership with raw lifecycle and assignee predicates. Do not offer `display_status` to those rule profiles. The additive feed field does not reinterpret an existing expression or require rewriting a saved revision. Current PostgreSQL presentation derives status after visible-assignee eligibility handling; projected reads retain the existing lag/watermark guarantees.

Use explicit strict mappings and stored `_source`; do not depend on dynamic keyword defaults or synthetic source to preserve original values. Translate typed IR to parameterized bool/term/terms/range/exists queries, escaped literal prefix/suffix/substring patterns and constant filters. No user query-string DSL, Elasticsearch scripts, runtime fields or application-wide post-filter scan is permitted. Wrap the compiled query in mandatory tenant, live-document and suppression filters.

**REV-54:** the strict mapping adds the effective `name` as a keyword with its `missing_name` flag, so documents carry the name a v2 alert reads as, including its `key_field` default. Existing indices need a rebuild under section 25 before an indexer with this mapping writes; until the switch, `name` predicates match nothing.

**REV-55:** the strict mapping adds `provider` as a keyword enum and `alert_rule_url` with the same representation as `runbook_url`, each with its missing flag. Documents carry the provider an alert reads as: the stored value, else `api` for v1, else missing. Existing indices need a rebuild under section 25, as for REV-54.

IDs/enums and bounded identifiers use keyword fields; booleans use boolean and counts/versions use long. Give sortable nullable fields an explicit missing flag, ascending in either sort direction. Severity uses a clear/missing-last flag followed by the selected urgency rank. Store a dedicated keyword alert ID for the final tie-break; do not sort on Elasticsearch `_id`.

Map timestamp search/sort values to signed epoch-microsecond longs, with the original ISO UTC string retained for presentation. This preserves both microseconds and the admitted years 0001–9999; Elasticsearch's `date_nanos` has a narrower range and ordinary `date` has millisecond precision. See [Elastic's date documentation](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/date_nanos).

Use wildcard representations for literal string matching, including the message's possible 8,192 four-byte characters. Bounded sortable identifiers fit exact keyword/doc-value fields under the existing source limits. Set mapping length limits explicitly so every accepted value is indexed; never silently ignore a valid long message. Equality on a wildcard representation is an exact-value query, and wildcard metacharacters in user string literals are escaped. Elastic documents the [keyword byte limit and wildcard representation](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/keyword).

For plain-text `q`, tokenize Unicode letter/mark/number/underscore runs, apply default Unicode full case folding without source normalization, discard separators and require every distinct token across message, impact, the effective name (REV-54) and current undeleted note text. Version the Unicode/tokenizer profile. Persist searchable tokens as a derived keyword projection; words from deleted/old note revisions do not remain searchable. Derive the maximum possible normalized query-token size from the pinned Unicode profile and the existing 256-code-point q bound. Omit only larger source tokens that no valid q token can equal; this avoids keyword limits without changing a supported match or truncating source text. An all-separator nonblank query is invalid, not match-all. CEL remains case-sensitive and has no note-text input.

## 7. Query versions and migration

Name the first application profile `keep-cel-v1`; its version covers field types/null semantics, allowed syntax, time rules, cost model, text tokenizer and Elasticsearch translator/mapping compatibility. Bare field identifiers are the current syntax; the assistant-selected `alert.field` alias is retained because accepting bare names is additive and does not change existing expression meaning. Preserve source and environment version in each saved definition without rewriting its source. Keep source-span mapping through lowering for useful diagnostics. Ship a common conformance corpus for feed search, preset preview, rule testing and rule execution.

Before changing the profile, compile every active saved expression and compare old/new results over the boundary corpus and a retained-data sample. Block activation of incompatible resources until a reviewed migration or supported old execution profile exists. An equivalent compiler/index optimization does not reset correlation evidence; a genuine rule-logic/profile semantic change uses its existing revision/reset boundaries and no backfill. Never re-evaluate history as new source events. Keep old compiler/mapping readers while protected active work needs them; retire them only after all references are cleared.

## 8. PostgreSQL physical record families

Use ordinary relational columns for identities, scope, state, order, revisions and timestamps; JSONB only for versioned snapshots/configuration/provenance and bytea for exact admitted customer bytes. PostgreSQL timestamptz stores instants; checks reject infinity and out-of-contract years. The alert catalog remains the complete current-state column contract, with internal lifecycle/job fields kept out of customer inputs.

| Record family | Selected keys and purpose |
|---|---|
| `alert_identities` | UUID primary key; tenant, retirement state/final version and minimal purge evidence. Stable target for surviving references. Unique `(tenant_id,id)` supports scoped foreign keys. |
| `alerts` | UUID primary/foreign key to identity; typed current catalog, occurrence pointer, semantic/projection versions, last source activity and retention deadline. |
| `alert_key_claims` | Primary key `(tenant_id,schema_version,key_digest)`; exact key/canonical identity material and unique live alert ID. Compare full material after digest lookup; a digest collision is a conflict, never a merge. |
| `kafka_source_results`, `kafka_consumer_positions`, `kafka_pipeline_faults` | Internal delivery UUID/first coordinate/digest/result/immutable changed proof, observed consumption and sanitized diagnostics. Old ingest tables remain solely for a fenced cutover drain. |
| `alert_source_events`, `alert_occurrences`, `alert_activity` | Parent UUID plus event/occurrence/activity UUID keys; source application order versus canonical activity order, exact admitted bytes/parsed values and required provenance. |
| `alert_notes`, `alert_note_revisions`, `alert_suppression_history` | Parent-scoped current notes and immutable note/suppression changes. |
| `alert_active_ownership` | Unique `(tenant_id,alert_id)` active claim; incident/context uniqueness remains the existing incident/correlation contract. |
| `alert_command_results` | Actor/tenant/alert/command identity, request digest and committed result; selected parent lifetime. |
| `tenant_work_state`, `projection_work`, `search_reconciliation`, `kafka_correlation_events` | Coordinator/application order, immutable projection proof for replay/rebuild, bounded current-state scan positions and consumed changed-event identity. Unrelated resource outboxes retain their existing role. |
| `tenant_view_state`, `projection_progress` | Separate live generations and per-index-epoch search progress. Updating these rows never requires taking a coordinator after a domain row lock. |
| `alert_purge_jobs`, `recovery_evidence` | Eligibility/version checks, protected intent/final fence references, chunk progress and sanitized outcomes. |

Source application stores exact payload/provenance in history and immutable delivery/result proof in the same PG transaction. No ingress pending payload is stored in PG. Rejection details are retained for 90 days; minimal UUID/coordinate/digest/result fences remain through replay risk. Product command lifetimes are unchanged. References point to permanent alert identities; outstanding source publication/correlation/rebuild proof holds prevent unsafe payload cleanup.

## 9. Partitioning and indexes

Keep current alerts, identity/key registries, active claims, ready work and command lookup tables unpartitioned initially. Hash-partition the large source-event, activity, note-revision, suppression and occurrence histories into 32 partitions by alert UUID; partitioned primary/unique keys include that UUID. This distributes even a single busy tenant's many alerts and prunes parent-history reads. Do not drop time partitions to enforce retention: an old event can belong to a still-retained alert. PostgreSQL requires partition keys in partitioned uniqueness constraints; see [partitioning documentation](https://www.postgresql.org/docs/current/ddl-partitioning.html).

Add B-tree indexes for `(tenant_id,alert_id,admission_order,event_id)` source pages; `(tenant_id,alert_id,change_order,activity_id)` activity pages; parent/note/revision lookups; legacy pending `(tenant_id,admission_order)` and target-key indexes retained for offline drain; ready job `(next_attempt_at,id)`; non-alert outbox `(tenant_id,stream,stream_order)`; and live operator/assignee/ownership lookups. Use partial due indexes for active inactivity checks and resolved retention deadlines. Use the exact tenant/version/key digest uniqueness above, rather than indexing potentially large canonical identity material. Query note/source payload JSON through explicit detail reads, not a blanket JSONB GIN index.

Partition count and indexes are an application-schema baseline to measure, not a service replica/shard allocation. Expand partitions through a checked application migration when justified; service teams own physical resource allocation, vacuum/backup operation and capacity.

## 10. Transactions, locks and tenant isolation

Use READ COMMITTED with explicit row locks for mutations. Preserve the common domain order: tenant coordinator, sorted rule IDs, full context keys, incident IDs, then alert IDs. Source application, ownership/reset decisions and logical purge take the same coordinator. Kafka ingress admission does not take a PostgreSQL lock. Never acquire it after a domain row lock. Validate mutation authorization under the existing access-version guard; avoid holding transactions across external service calls.

Use `FOR UPDATE SKIP LOCKED` to claim ready tenants/jobs, never to skip an earlier source item within one tenant. Persist ten-second leases, renew every three seconds and require matching lease generation/deployment epoch at commit. Leases schedule work; PostgreSQL locks and predicates establish correctness. Read a consistent parent/history page in a short transaction and release it before returning a browser cursor.

Enable and force tenant row-level security on human-facing tenant tables, in addition to Product API authorization. The Product API role is neither table owner nor BYPASSRLS; set transaction-local tenant context only after authenticated route authorization and clear it with the transaction. Use composite tenant foreign keys and trusted scope on every join. System workers use a separate limited role/claim path, never the human request connection role. RLS is defense against omitted predicates, not a substitute for the LDAP/access policy or a defense against a compromised trusted backend. PostgreSQL documents [owner/bypass behavior](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

## 11. History reads and detail contracts

Use keyset history pagination, default 50/max 200, with opaque authenticated 15-minute cursors fixing an upper committed order watermark. Bind cursors to tenant, alert, collection, sort direction, filters and current deployment epoch. Reauthorize and recheck retained parent/content on each page. New events appear on refresh; expired parents/history cannot be recovered through an old cursor. No long-lived PostgreSQL transaction is held for pagination.

Activity defaults newest first by canonical change order and UUID; source events default newest first by application order and event UUID. Support existing ascending mode, optional occurrence ID, activity-kind filters and an explicit inclusive `from`/exclusive `to` UTC interval. Label activity filtering by recording time and source filtering by receipt time; display effective/source time separately. No default short date window conceals older retained history.

Collection pages contain metadata/summaries, not 200 embedded raw payloads. Add `GET /api/tenants/{tenant_id}/alerts/{alert_id}/source-events/{event_id}` for a retained applied event's exact UTF-8 `raw_json` string, parsed values and provenance. It uses current tenant read permission and the retained-parent guard. Unattached rejected deliveries remain internal diagnostic records and never masquerade as applied alert history. No bulk raw-history export is introduced.

## 12. Durable processing and fairness

The source consumer applies Kafka partition append order with PostgreSQL delivery-UUID idempotency. Allocate application proof order only while applying; receipt UTC is immutable ingress data. Retain source history for unchanged repeats without creating semantic evidence. The two-commit crash/fencing/replay protocol is [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 3.

## 13. Kafka topics and event encoding

alerts.received schema version 2 is self-contained and keyed by canonical JSON [tenant, application, key_field]. alerts.changed is keyed by tenant UUID bytes. Native versions and internal envelope versions remain distinct. Correlation/indexer use separate read_committed groups; source transactions include changed publication and input offset. Protocol and immutable encoding are defined in [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 3. Freeze partition counts until a fenced migration.

## 14. Relay, acknowledgements and retries

**Current scope (REV-34, REV-36):** Operator background jobs and retention workers are deferred, and live hints are published inside the Product API; see [worker scope](spec-worker-scope.md#5-nice-to-have-components). The no-relay and proof rules below remain normative.

The active alert path has no PostgreSQL inbox/outbox relay or CDC. Kafka is the source work trigger. PostgreSQL retains current state, before/after history, delivery/result/immutable-publication proof and consumption evidence. Do not poll those proofs as an alert dispatch queue. Other durable operator/configuration/retention jobs and live hint publication retain their contracts. Cleanup and restore must preserve required proof through the bounds in [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 8.

## 15. Projection ordering and deletion markers

Every visible mutation atomically allocates tenant projection_seq, per-alert projection_version and identity current_projection_seq. Search rejects older snapshots, verifies equal-version identity and retains permanent versioned deletion markers. Changed records prompt current-authority reads; bounded scans repair lost notifications. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 6. No pending projection-work scan is the active indexing trigger.

**Assistant-selected scalability implementation (2026-10-06):** coalesce changed
hints into bounded bulk writes and reuse process-owned search clients. Verify
already refresh-visible matching versions/digests without rewriting them. Bound
bulk bytes and individual projection bytes using the supplied capacity profile;
`search_max_document_bytes` is mandatory outside development. A development
fallback is unqualified. Read current note text with bounded cursors and retain
every searchable token; never silently truncate notes or impose a new note quota.
Use the partial live-note `(tenant_id, alert_id, id)` index for existence probes
and ordered streaming reads. Probe note presence with the current alert batch;
an alert without live notes requires no separate streaming cursor.
A document beyond the supplied integration allocation is a visible failed
projection, not a false watermark advance. Partition and tenant retries preserve
their predecessor fences while allowing independent partitions/tenants to run.

## 16. Searchable progress and refresh proof

Capture committed S at the beginning of a tenant authority scan. Verify every keyset page is refresh-visible, then advance searchable_seq only to S after the full pass. Concurrent writes and behind-cursor insertions have sequence above S and belong to later passes. Individual hints never advance the tenant watermark to their maximum. Expose committed/searchable positions and verified time; publish live invalidations from durable view-state reconciliation. Details and rebuild fencing are in [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 6.

Claim reconciliation pages using expiring PostgreSQL owner tokens. Only the
current owner may checkpoint a page; stale owners cannot advance progress.
Persist a failed tenant's safe error code and retry time and yield to other
eligible tenants. Authority scans continue when Kafka notifications are
unavailable, and healthy notifications can continue when a scan fails.

After a verified pass, an incremental pass persists that verified sequence as
its lower bound and scans current identities whose projection sequence exceeds
it. Capture a new upper boundary S at pass start. Do not exclude identities newer
than S: their complete current snapshot can cover the earlier required state.
A write behind the UUID cursor necessarily has sequence greater than S and is
covered by a later pass. A new epoch starts at lower bound zero and requires a
complete initial pass before advancing its searchable watermark.

Five minutes after the previous audit completes, a full-authority repair audit
becomes eligible. Persist its own UUID cursor, captured sequence S, start time,
last-page time and scheduling counter. Select current identities with sequence
greater than zero and no greater than S; subsequent writes have larger sequences
and remain covered by ordinary delta passes. New identities cannot appear behind
this audit cursor with a sequence at or below S. Give an audit at most one bounded
page for every four ordinary reconciliation turns, under the same expiring
tenant lease. Audit progress never advances or resets the ordinary searchable
watermark, and an unfinished audit never replaces ordinary delta progress.
Recheck lease ownership after locking the checkpoint row. Persist audit failure
and retry time separately from ordinary scan failure: an old document failing
repair must not prevent healthy new deltas from advancing the watermark.
Completion depends on retained tenant size and available repair allocation; the
five-minute eligibility interval is not a repair-completion promise. This repairs
unchanged missing search documents without making routine freshness wait for a
large historical scan. Restore/rebuild gates and complete rebuild copy passes
remain required.

## 17. Search snapshots, counts and purged IDs

Use Elasticsearch point-in-time (PIT) plus `search_after` and the selected sort/tie-break, with an absolute five-minute Keep cursor lifetime. Set each PIT keep-alive no later than the remaining application lifetime, carry the newest returned PIT ID, close it on disposal when possible, and let it expire after abandoned views. A successful first-page live refresh disposes the replaced PIT after accepting the new result; do not accumulate five minutes of abandoned PITs on every one-second refresh. A snapshot still being traversed retains its own lifetime. The [PIT pagination contract](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/paginate-search-results) preserves a stable traversal.

An authenticated cursor contains/binds tenant, session/principal visibility scope, index/environment epoch, effective-filter digest, sort, captured query time, latest PIT ID, last sort tuple and expiry. Protect it using authenticated encryption with the existing approved application secret mechanism; never expose a raw client-editable Elasticsearch request. Query changes/expiry/retired index restart traversal. Reauthorization can invalidate an otherwise live snapshot.

First-page responses include a separate purpose-bound `meta.close_token`.
`POST /api/tenants/{tenant_id}/alerts/snapshot/close` accepts `{token}` and
reauthorizes its session, tenant and index scope without requiring the old filter
or preview revision. Discarded late responses and disposed views close their PIT;
transport uncertainty retains the existing finite expiry fallback. Pagination
tokens retain all their original filter and visibility bindings.

`POST /api/tenants/{tenant_id}/alerts/counts` accepts at most 24 uniquely identified
queries with CEL, text and suppression options and returns a decimal count map.
This bounded quick-count operation uses the count engine; it does not fetch feed
rows or allocate one PIT per badge. Existing preset/dashboard authorization and
specialized count contracts remain authoritative for those resources. Query
responses identify relative-time expressions so the browser can run their
existing one-second refresh contract even without a data invalidation.

Capture the verified searchable vector before opening a new PIT and recheck its epoch afterward. Report at most that pre-PIT verified lower bound; reading a newer watermark after opening the PIT cannot make its older snapshot fresh. Return a newer observed vector separately as a reason to refresh, never as a rendered acknowledgement for that snapshot.

Request exact total hits and reject partial-shard/time-limited results as unavailable; row and total filters/time/PIT must agree. Batch-check returned IDs against PostgreSQL retained-identity state, not one database request per row. Omit logically purged IDs even in an older PIT. Advance its cursor by the last examined Elasticsearch hit, not the last surviving row; an empty filtered page may still have a continuation. Do not perform an unbounded scan to fill holes. If purge generation advanced after that PIT opened, mark its total updating/unavailable until a fresh snapshot is obtained; do not subtract only the purged IDs found on the current page and call that an exact total. This preserves the existing purge and count contracts without scanning all retained alerts in Python.

**Grouped snapshots (REV-44).** A grouped first view opens one PIT and sends one search with no rows: a composite aggregation over the effective filter returns each distinct value of the grouping keyword field, including the missing-value bucket, with `filters` sub-aggregations for severity counts and, for severity groups, visible-status counts. Status groups and visible-status counts use the compiled `display_status` predicates of section 6, never a physical field, script or runtime field, so they agree with the Status quick views. Collect at most 1,000 buckets; one more returns `422 too_many_groups`. The API orders buckets under preset section 4 and slices the requested groups. One multi-search on the same PIT then fetches the first rows of those groups with the group's term, or its `missing_` flag, added to the effective filter and the effective sort. Group totals and their sum come from the same exact hit total; a partial result is unavailable, and a retired returned ID or an advanced purge generation marks every total updating/unavailable as for page totals. Each group's continuation cursor is an ordinary feed cursor whose filter digest also binds the group field and value; a group-list cursor binds the PIT, query digest, grouping field and offset and reruns the aggregation on that PIT. Neither exposes an Elasticsearch request. The first view returns a close token while any continuation remains and closes the PIT otherwise.

## 18. Durable live state and SSE protocol

Select `GET /api/tenants/{tenant_id}/events` using the existing same-origin session cookie. Events carry hints/progress, never alert bodies, credentials or unrestricted tenant lists. Persist a tenant view-state row with deployment/index epoch, monotonic `view_generation`, committed projection sequence, searchable sequence, authoritative-resource generation and purge generation. Domain commits and verified search progress update the appropriate fields plus durable outbox in the same transaction.

Use Redis Pub/Sub for low-latency fan-out. Every API replica also reconciles PostgreSQL view-state for its connected tenants every two seconds, coalescing reads across connections. Redis loss therefore delays a hint but cannot lose the current generation or make authorization depend on Redis. Select SSE event names `state`, `invalidate` and `resync`, with the full small current vector and scoped changed-resource categories. Event IDs encode epoch/generation; they are hints, not access credentials.

**REV-36 user decision:** the Product API also owns background outbox-to-Redis
publishing; no live worker is deployed. [Worker scope section 6](spec-worker-scope.md#6-live-updates-inside-the-product-api)
defines bounded turns, replica duplicates, shutdown and the minimal API outbox
privilege. Existing SSE authorization/reconciliation contracts remain unchanged.

On connect/reconnect, reauthorize, register local delivery, read current PostgreSQL state and send a `state`/`resync` event. Accept Last-Event-ID only as an observed-generation hint. An epoch mismatch, unknown/future ID or missed history causes a complete current-state resync. Do not maintain or promise replay of every transient SSE message; replaying the latest durable invalidation state is sufficient because actual data is refetched. Periodic reconciliation closes subscribe/read races.

## 19. Browser refresh, reconnect and relative time

Coalesce live invalidations in a trailing window: refresh after 500 milliseconds without a further change, and no later than one second after the first unrefreshed change. For five seconds after the user's own command is committed or has an unknown outcome, the window is 250 milliseconds, so the command's projection hint is not held back (assistant-selected 2026-10-22, replacing a fixed 250 milliseconds; see the [design register](../decisions/design-register.md#live-invalidation-merge-window--2026-10-22)). A reconnect, return to a visible tab or the user's own refresh reloads at once. Keep at most one request in flight per visible resource and one pending refresh. Foreground feeds on the first page refresh; a user traversing older snapshot pages gets a New results available indicator instead of inserted/reordered rows. Refresh visible alert details/history, preserving unsaved notes and older-page position; show new activity rather than overwriting a draft. Preset clean/dirty behavior remains its selected contract. Visible count panels consume searchable generations; dashboard completion 4/9–12 selects its specialized batching/layout.

Use exponential SSE reconnect delays of one, two, four, eight and at most 30 seconds with jitter; reset after a stable connection. Reconnect/refocus refetches generation and visible data before calling the view current. Detect a missing heartbeat after 30 seconds. During a disconnected foreground view, poll authorized view state every two seconds and refetch when it changes; expose live delivery as degraded even when polling obtains fresh data. Pause data polling/relative-time refresh while hidden, close a hidden tab's stream after 60 seconds, and fully reconcile on return. A background tab does not extend authentication.

Relative-query one-second ticks in decision 4 operate even without data changes, with the same in-flight/coalescing rules. Existing session activity uses its separate 60-second foreground heartbeat. Normal five-second incoming/maintenance visibility remains an end-to-end p99 objective; polling, indexing and rendering must be included in qualification rather than adding their individual percentiles as a proof.

## 20. Stream security, bounded delivery and proxy contract

Authorize the tenant at stream open, before each protected hint and at least every 30 seconds. End expired/revoked sessions and lost-tenant delivery, including metadata hints. Preserve permitted reads after edit/admin loss. Recheck against PostgreSQL grants/sessions and the accepted identity checkpoint; no stale effective-role cache or new identity-age cutoff is introduced. If authorization authority is unavailable, stop protected delivery. Use same-origin validation and no cross-origin credentialed streams.

Send a comment heartbeat every 15 seconds; it contains no tenant data and does not count as user activity. Bound each connection to one coalesced pending state vector and 64 KiB of transport buffering; disconnect slow clients and require resync rather than accumulate an unbounded event queue. Maintain one stream per active tenant/tab. Include stream counts and memory in the qualified client profile instead of introducing a new user-access cap.

Request no intermediary response buffering/cache/compression that delays flushes, a 75-second or greater idle timeout, and a 30-minute application stream lifetime followed by reconnect. Keep finite ordinary API timeouts unchanged. These are Keep's OpenShift/Kong integration requirements for the owning teams to confirm, not settings changed by this design. SSE setup uses ordinary 401/403/404/503 behavior before headers; after opening, close on loss of authority and let the client reconcile its session.

## 21. Rendered acknowledgements and freshness

**Current scope (REV-34):** Maintenance windows no longer release alerts on a timer, so maintenance-expiry observations have no visibility objective to sample; see [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler). Endpoints and incoming acknowledgement rules below remain normative.

Add `GET /api/tenants/{tenant_id}/view-state` for the authorized durable vector and `POST /api/tenants/{tenant_id}/view-observations` for sampled render acknowledgements. The latter accepts at most 100 observations and 64 KiB per request, with session-bound server-issued observation IDs, resource/view/query digest, observed versions/generation and outcome. It uses normal CSRF/tenant checks. These endpoints do not update the user's activity clock.

Return observation IDs with eligible view responses. The browser acknowledges after rendering the matching data or the confirmed nonmatching result for that query, not after merely receiving an SSE hint. Validate acknowledgements against server-issued scope/version bounds; duplicated or impossible future acknowledgements cannot manufacture success. Use server receipt time as the conservative completion bound. Preserve the reliability supplement's 10% incoming observation sampling, all maintenance-expiry observations and full qualification instrumentation. Missing acknowledgements remain misses/coverage gaps; the browser is not authority for alert state.

Show last successful fetch/evaluation time, projection lag and live/disconnected state separately. An empty correct result is zero; an unavailable result is unavailable. Operational observations use the agreed telemetry retention, not a new product history lifetime.

## 22. Alert and history screen organization

Select alert-detail sections Overview, Activity, Source events, Occurrences and Notes, sharing the same tenant/alert identity. Overview shows derived status and assignee, suppression causes, incident links and current source fields. Activity shows meaningful source/user/system changes and original effective time beside recording time; unchanged received repeats belong in Source events rather than fabricated semantic activity. Occurrences expose lifecycle cycles without splitting the logical alert identity.

Show note revisions/deletions and actor snapshots under Notes/history while primary notes/search use current undeleted text. Source event detail renders escaped plain text/JSON and supplied-versus-defaulted time provenance; it never executes payload content or fetches runbook URLs. Distinguish loading, empty history, unavailable dependency, expired resource and late processing. User commands apply their authoritative response immediately and show search updating until the response's projection sequence is covered. Keep existing edit permissions and no manual alert Delete action.

## 23. Logical purge and bounded physical cleanup

**Current scope (REV-34):** Retention and inactivity sweeps are not deployed, so nothing retires alerts at the 90-day deadline; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). The purge protocol, fences and proof holds below remain the design for explicit deletes and future automation.

Keep the hourly retention eligibility scan, 30-day inactivity policy and 90-day post-resolution lifetime. Under the coordinator, recheck latest resolution, current revision, unconfirmed applied source results and protected dependencies. Unknown Kafka target inputs are governed by the retained logical-key UTC retirement fence, not an inbox scan. Prepare a versioned purge intent without releasing the live identity. Protect that minimal intent through decision 24, then reacquire the coordinator and recheck eligibility. If changed, cancel it; if still valid, atomically retire the alert, make parent-owned content inaccessible, release live key/ownership claims and commit the final tombstone, deletion snapshot, purge job and live generation. A later firing admission may create a new UUID under the same logical key, as already selected.

This refines the earlier atomic-purge wording: **visibility/identity retirement is atomic; physical removal of large history is resumable**. It does not shorten retention or allow partially visible history. Every detail/history route joins the retained-parent guard. Surviving incident references become unavailable identity/provenance only; cleanup never deletes incidents or counterpart content. No new raw input can attach to a retired UUID.

After independently protecting minimal retirement and logical-key replay boundaries, delete eligible content in chunks of at most 1,000 rows or 100 milliseconds, yielding between transactions. Preserve minimal delivery UUID/digest/first-coordinate and retired identity/key fences; sender IDs have no deduplication lifetime. Unconfirmed source publication, correlation and rebuild proof holds prevent premature cleanup. Target physical application cleanup within 24 hours after eligibility and released holds under supplied capacity; record delays without discarding proof. Protected restore qualification remains mandatory.

## 24. Protected evidence and restore readiness

Define a recovery-evidence adapter supplied through the owning teams' supported storage interface: idempotent append of immutable intent/final/cancel records, durable acknowledgement, ordered namespace/checkpoint enumeration and integrity verification independently of the database recovery point being restored. Minimal alert evidence contains tenant/alert UUID, intended/final projection version, evidence ID/state/order and integrity metadata, never source bodies, note text or actor display names. Keep chooses this contract; it does not choose the team's backup product, schedule or topology.

Protect an intent before final logical retirement so a crash/rollback cannot erase every trace of a potentially completed purge. Protect its final fence before physical content cleanup. On restore, a committed final fence forbids resurrection; an unresolved protected intent fences that identity for reconciliation rather than guessing that deletion either completed or never happened. A canceled intent requires trusted cancellation/eligibility evidence before release. If the adapter is unavailable, keep eligible content logically unavailable when its retirement has committed, hold physical cleanup and show protection failure; do not claim the retention job completed.

Keep minimal retired-ID fences indefinitely in the initial release. There is no automatic age-based compaction and no required finite replay-horizon guess. After rollback restore, use a fresh independently established deployment epoch, reconcile current evidence/pending orders/consumer progress, apply product retention and rebuild/verify projections before reopening affected reads. Preserve the separately selected fresh-SSO/directory/grant reconciliation and operator credential rules. Unknown evidence gates affected paths. The supplied evidence endpoint, guarantees and exercised recovery remain integration/qualification deliverables.

## 25. Search rebuild and index switching

Use a new physical index and immutable index epoch behind the application read/write alias. Register a durable rebuild hold before opening a consistent PostgreSQL snapshot, then capture its per-tenant projection positions and copy retained current alerts/notes. Serialize hold registration with projection-proof cleanup so no required gap can be purged; newly created tenants inherit the active hold. Copy in bounded keyset pages, then apply subsequent complete snapshots/retired markers in order until caught up. This rebuild never replays source lifecycle, resolves/reopens alerts or runs correlation actions.

Validate per-tenant live IDs, versions, representative query/count parity, mapping/profile compatibility and retired-ID exclusion. At cutover, fence index writers, drain in-flight old-epoch work and capture a per-tenant cutover position. Make the replacement search-visible through those positions before recording its verified progress/new epoch and switching the alias through the team's supported atomic operation. Source application and commands may continue, with immutable proof and authority scans covering writes beyond the captured cutover. If switch/control-state outcome is uncertain, gate search until reconciled; source application can continue with recoverable committed projection proof. Resume current-epoch writers and emit resync. Old PIT cursors receive `409 index_changed` and restart. Keep the previous index available for controlled repair until readers/work are released and the team performs its normal cleanup; no infrastructure retention duration is imposed.

## 26. Schema, event and application rollout

Use forward migrations and the offline drain, group-offset initialization, partition-count and writer fences in [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 8. Retain old tables/history; do not mix the old relay/journal consumer with new protocol workers. A rollback after Kafka-first admission must drain new records with compatible consumers. Generated HTTP/event schemas and frontend contracts must match the selected protocol.

**REV-55 provider rollout.** Migration 0060 adds nullable `alerts.provider` and `alerts.alert_rule_url` with checks and rewrites no rows. The source processor derives both from each received event's existing `adapter_version` and retained original bytes, so Kafka envelopes and ingestion are unchanged. After every source processor runs this release, a one-time backfill sets both on each alert still lacking a provider from its latest applied source event (`history_id`), in short batches under the tenant coordinator and alert row locks. It stores the row and publishes a non-semantic projection change with cause `provider-backfill`, so search and live views see the values without activity, correlation or maintenance input. It is idempotent and can be rerun. Rebuild the search index for the new mapping before or after the backfill.

## 27. Operational diagnostics and retention

Record post-202 semantic rejection, UUID conflict, invalid protocol proof, broker offsets/low watermarks/retention gaps, oldest receive age and search pass progress. No receipt lookup or resubmission-dedup promise remains. Never log keys or raw secret-bearing context. Scope internal diagnostics by tenant and operational privilege. Retention and recovery limits are [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 8.

## 28. Supplied capability and readiness gates

Before enabling each dependent path, verify the supplied PostgreSQL partition/locking/RLS capabilities, Elasticsearch PIT/wildcard/external-version/refresh/alias behavior, Kafka record/client limits and Redis/proxy connectivity against the selected contracts. Pin the deployed versions and record authenticated endpoints, supported timeouts, allocation and recovery-evidence handoff. Obtain values from the owning teams; do not invent them or silently switch engines when incompatible.

Separate Kafka admission, authoritative Product API, source processing, correlation, search and live-delivery health. PostgreSQL or search outage does not disable valid Kafka admission. Missing automatic-evaluation proof blocks the affected unsafe processing; an unset correlation or maintenance budget is unlimited (REV-39). No application backlog or tenant pending-item budget rejects ingress while Kafka can acknowledge publication. Monitor Kafka retention risk and retained PostgreSQL proof/history growth; capacity, recovery-throughput and one-tenant stress qualification remain required. Expired unprocessed Kafka records are an accepted acknowledged-loss risk, with offset-gap diagnostics and fenced source/correlation recovery as specified in [Kafka alert pipeline](spec-kafka-alert-pipeline.md).

## 29. Qualification and acceptance evidence

See [required alert execution and recovery checks](../verification/verification-plan.md#alert-execution-and-recovery).
