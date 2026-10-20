# Shared system contracts

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

The 2026-09-30 [Kafka-first pipeline](spec-kafka-alert-pipeline.md) governs alert transport, gateway admission, UTC ordering, manual correlation, search reconciliation and cutover (REV-33). Unrelated product behavior remains unchanged.

Cross-resource UI, HTTP, persistence, transactions, security and application deployment. [System design](spec-alerts-management-system.md) maps each domain to its authoritative specification.

## 1. Application framework and module boundaries

Select FastAPI with Uvicorn for Python HTTP APIs, Pydantic strict request/response models, Psycopg 3 pools and explicit parameterized SQL for transactional repositories. Use one Uvicorn process per API container; scale application containers through the platform's supported deployment model and qualified allocation. CPU-intensive CEL compilation/evaluation uses bounded isolated workers, not the event loop. Native input parsing preserves duplicate-key detection and exact object bytes before model validation; framework coercion must not weaken the strict v1/v2 contract. [FastAPI container guidance](https://fastapi.tiangolo.com/deployment/server-workers/) and [Psycopg concurrency](https://www.psycopg.org/psycopg3/docs/advanced/async.html) support these runtime choices.

Use Next.js App Router with TypeScript for the frontend, a server-rendered non-sensitive shell and client-managed operational views. Python remains the sole business-command/authentication authority; no duplicate Next.js mutation backend or direct browser database/service access. Use the official Elasticsearch and Redis clients and `confluent-kafka` for Kafka. Select Authlib for OIDC protocol handling, `ldap3` for the read-only directory adapter, and the already selected `cel-expr-python` runtime. Pin tested package/runtime versions and native builds in lockfiles after capability qualification; floating latest tags are prohibited. These library selections do not assert compatibility with unprovided company versions. [Authlib](https://authlib.org/projects/authlib/), [Kafka Python client](https://docs.confluent.io/kafka-clients/python/current/overview.html), [ldap3](https://ldap3.readthedocs.io/en/latest/index.html).

Organize backend modules by identity/access, ingestion, alerts, incidents, correlation, maintenance, presets/dashboards, operators, search/live and shared persistence/protocols. A module exposes command/query services and repositories; it does not bypass another module's invariants by editing its tables from ad hoc routes. Cross-resource operations use the explicitly selected shared transaction/lock service, not distributed HTTP calls between domain services. Use Kafka for the alert path and the existing PostgreSQL jobs/outboxes only for unrelated configuration/operator/retention work; no Celery/RabbitMQ or CDC.

## 2. Repository, generated contracts and documentation

REV-37 supersedes the original monorepo selection. Use the eleven independent repositories and service-owned images in [repository layout](spec-repository-layout.md), each with owned source, tests and locked dependencies. PostgreSQL migrations remain one ordered chain in `appchi-migrations`. Builds produce immutable image digests, SBOMs and a multi-repository release inventory; qualification remains separate.

Keep machine-readable OpenAPI and internal JSON Schemas under contracts, generated from reviewed strict models and checked for breaking diffs. Generate the frontend client/types; business validation stays server-authoritative. Store checked-in ordered SQL migrations with checksums and an Alembic migration runner using a dedicated role/lock, under [REV-38 migration execution](spec-repository-layout.md#alembic-migration-execution-rev-38). Markdown decisions are normative for behavior; generated schemas must conform rather than turn old illustrative JSON into accepted inputs. Publish developer API documentation internally, authenticated, with secrets and real payload examples removed.

## 3. Navigation and visual system

**Later user correction — 2026-10-11:** name the default alert-query page Feed.
Use Feed in the sidebar, page title and breadcrumbs, including return navigation
from alert details. This supersedes the Alerts page label below; existing
`/alerts` resource URLs and API contracts remain unchanged.

Use the user's 2026-09-24 [Option B full-system design](https://claude.ai/artifact/XMD6gScr8TVDnWvYtcvNWP) as the visual reference. A persistent 76-pixel left rail contains Alerts, Incidents, Presets, Correlation rules, Maintenance and Dashboards, with Administration and the identity/session menu at its foot. The top breadcrumb contains the tenant selector and current role; scoped update status remains visible. Administration contains Operators, Permissions and tenant/access audit only for their authorized audience. Global super-admins additionally get tenant creation and platform health/audit. Existing resource-read permissions still apply: hiding an admin action is not a substitute for authorization, and permitted read-only operator summaries remain available as selected earlier.

Preserve the prior navigation rule: open the last accessible tenant, falling back to Global, with Alerts as its default page. Keep the last-tenant hint in the server-side human session and preserve validated local return paths; reauthorize it before use. A new session without a valid hint enters Global. Explicit deep links preserve their accessible tenant. Do not add an editable personal default tenant or server-side table preferences. Browser history includes tenant/resource IDs and safe resource subpages, not raw credentials, note drafts or unsaved CEL. When an alert is opened from saved preset results, its detail view offers a return link to that preset and steps through the visible result page. Returning to the preset follows its normal transient-filter reset. Use the reference's compact desktop-first interface: Geist and Geist Mono, 13.5-pixel body text, 24-pixel page titles, warm off-white backgrounds, dark primary actions, semantic tables and consistently placed filters. Narrow screens use scrollable data tables with stable row-open controls and stacked forms. Keep visible focus and text status alongside color. The supplied reference's light palette remains the default. The user's subsequent dark-mode request adds an explicit Light/Dark choice for Appchi-owned screens, including sign-in and session states; persist the choice locally across navigation and reloads without storing identity or tenant data. Assistant-selected behavior keeps the light reference on first use, independent of OS preference, and gives an explicit user choice precedence over OS preference. Both palettes retain readable text, status meaning and visible focus. [UI implementation mapping](https://github.com/appchi-alert-operations/appchi-frontend/blob/main/docs/ui-design.md) records reference provenance and responsive adaptations.

Use English initial labels, Unicode content, browser locale number formatting and the previously selected date format/timezone labels. Maintenance continues to display its selected IANA zone. All controls have keyboard alternatives, descriptive labels and error association; target WCAG 2.2 AA in implementation acceptance, including contrast, zoom, focus, dialog trapping/return and reduced motion. No audio, toast-only critical error, blinking count or inaccessible drag-only workflow. This is an acceptance target, not certified accessibility.

The alert detail's **View alert** action presents its already-loaded detail response as read-only formatted JSON in an accessible native modal. Closing the modal returns interaction to its opener. It does not request additional resource data or mutate state; the alert detail endpoint's authorization remains the data boundary.

Keep the authenticated workspace mounted during internal page navigation. A route
change alone does not return users to the initial session-check screen. Continue
normal session revalidation, clear protected content on access loss or expiry,
and reset tenant-scoped content and subscriptions when switching tenants.

The later user-approved sign-in design uses the Appchi Keycloak theme described in [identity section 1](spec-identity-configuration.md#1-ownership-and-realm-boundary). Its light/dark selection is stored on the identity origin, independently of the application origin, with light as the initial default. Only the appearance string is persisted; credentials remain in the normal Keycloak form submission.

## 4. Common interaction and information boundaries

Use explicit Save/Discard for configuration; immediate scoped actions for lifecycle/assignment with authoritative server responses. Confirm irreversible resource deletion and key revocation with the resource name and concrete effect. No repeated confirmation for ordinary save, validation, preview or an idempotent retry. Offer undo only where an existing explicit inverse action is valid; never imply that deletion, expired history or revoked keys can be restored.

Maintain drafts in tab memory, display their base revision, and keep them on conflicts/transient failure. Voluntary navigation warns; sign-out, session expiry or tenant access loss clears protected state. Clear API query caches, selections, clipboard staging buffers and subscriptions on tenant/session change, and reject late responses whose scope/request generation no longer matches. No offline mode, service-worker caching, localStorage drafts, personal presets, attachments, bulk export, notification center or public sharing in the initial release.

A scoped nonmodal status area explains source backlog, indexing delay, maintenance updates, identity verification outage or integration pending; tenant users see only their scope, platform details stay restricted. Routine indexing and suppression progress uses existing status areas without inserting banners or shifting content. Actual failures, including blocked source processing and unavailable tenant health, remain prominent. `GET /api/tenants/{tenant_id}/health` returns safe tenant-scoped statuses to current readers; `GET /api/admin/health` returns platform capability/queue/job summaries to global super-admins. These are read-only current snapshots, with bounded paged diagnostics, no secret values or infrastructure administration controls.

Distinguish initial loading from refreshing a completed result. For the same scope
and query, keep the completed rows or confirmed empty state visible during a
background refresh. Routine refreshing must not insert an unavailable warning or
replace an empty state with a loading placeholder. First requests and changed
queries must not claim an empty result before completion; errors remain explicit.
Keep transient refresh feedback in existing status areas so it does not move the
content. Retained results from a different query follow the preset preview's
existing provenance rules.

## 5. Common HTTP and JSON contract

Use same-origin HTTPS JSON Product API under the existing `/api` routes and the selected `/auth` routes. Native `/api/ingest/v1/alerts`, `/api/ingest/v2/alerts` and Grafana adapter remain separate versioned ingress contracts. Human Product API authentication uses the selected session/CSRF model; operator keys authorize ingestion only. No new personal API tokens or machine resource-management API is introduced.

Reject malformed UTF-8, duplicate keys, unknown writable fields, illegal nulls, type coercion and nonfinite numbers. UUIDs use canonical lowercase strings. UTC instants use RFC3339 with `Z` and up to six fractional digits; entered maintenance schedules retain their special local representation. Revisions, orders, counters and exact potentially unbounded counts are nonnegative decimal strings on the wire to avoid JavaScript integer loss; bounded panel coordinates/page sizes are JSON integers. Persist counters as PostgreSQL bigint and reject overflow rather than wrap. Existing native source fields remain strings with their exact formats.

Default raw decoded-body limit is 64 KiB for control endpoints; ingestion retains 4 MiB request/64 KiB native member bounds. Correlation definition/validation/test bodies allow 1 MiB for up to ten 16 KiB CEL conditions and description; maintenance definition/validation/test allows 256 KiB. These are resource-specific exceptions, not enlarged alert inputs. Both raw envelope and decoded field limits apply. No compressed request bodies initially; reject unsupported content encoding before parsing, and require `application/json` on JSON bodies. Large descriptions in older 64 KiB routes remain subject to both existing limits; allowed field maxima do not guarantee every possible escaped combination fits an envelope.

Responses contain `data` and `meta` (request ID, current revision/ETag, relevant freshness/query context); lists add `next_cursor`. Errors use decision 6. Use the ordered per-member acceptance/error representation in Kafka pipeline section 2 rather than replacing it with an all-or-nothing generic error. GET never mutates user state. Read-only POST validation/preview/count calls require same-origin/session safeguards but neither a command identity nor activity audit.

## 6. Errors and recovery

Use `{error: {code, message, request_id, fields, conflicts, retry_after_seconds}}`, omitting inapplicable fields. `fields` contains stable JSON paths and CEL source spans; `conflicts` contains only currently accessible IDs/revisions and repair instructions. Never echo secret/body values, SQL, stack traces, directory rosters or inaccessible resource names. Translate database unique/check conflicts into the resource's stable errors.

Browser navigation recovery for an expired/consumed/missing sign-in callback follows
[identity section 2](spec-identity-configuration.md#2-login-flow-and-browser-boundary):
a no-store redirect to the public retry page. JSON clients retain the error envelope.

| Status | Meaning and client behavior |
|---|---|
| 400 | Malformed JSON, duplicate parameter or cursor encoding; fix request. |
| 401 | Missing/expired session or invalid ingestion credential; human UI signs in. |
| 403 | Visible resource but forbidden action; remove unavailable write controls. |
| 404 | Inaccessible/cross-tenant/nonexistent active resource, expired unprotected history; do not reveal which. |
| 409 | Revision/name/reference/lifecycle/retry conflict, expired/changed cursor or changing query context; preserve draft, refresh and review. |
| 413 / 415 | Body too large / unsupported content type or encoding. |
| 422 | Well-formed but invalid submitted definition/fields. Read-only validate returns 200 with `valid=false` instead. |
| 429 | Capacity rejection; Retry-After 10 seconds, no accepted operation silently dropped. |
| 503 | Required authority/dependency/proof unavailable; Retry-After 5 seconds; distinguish stale readable views from new unavailable results. |
| 500 | Unexpected application defect; generic message/request ID, no false success. |

Clients retry reads with bounded jitter within a view's current scope; mutation timeouts are reconciled using the original command identity, never a fresh key. A timeout does not prove failure. Preserve selected 201 create, 200 completed command/no-op and 202 durable asynchronous operation/ingress responses. Do not silently retry a stale revision with a newly fetched revision. Existing specialized operator prepared-key/admission statuses remain intact.

## 7. Shared commands, authorization and receipts

Resource APIs use `command_id` UUID in JSON and `expected_revision` for existing resources; DELETE uses Idempotency-Key and quoted If-Match. Move contains both incident revisions. Legacy optional ingress IDs are syntax-only; they do not deduplicate resubmissions. Scope command uniqueness by tenant, immutable actor/system producer and operation family; include canonical semantic payload, target IDs and expected revisions in the fingerprint. Preserve the preset-specific scope: existing preset commands additionally include immutable target ID in their namespace. Tenant creation uses actor and creation operation before a tenant ID exists. Verify authorization before reading/replaying a stored result. An identical committed retry returns its original outcome; a changed fingerprint is 409. A no-op records a command receipt without synthetic activity or revision advance.

Current grants, accepted identity evidence, assignee eligibility and relevant resource revisions are rechecked/guarded at commit. Serialize grant/checkpoint publication with a short authorization guard: acquire applicable principal/tenant authorization guard in stable order before domain coordination; publishers use the same guard. Do not hold it over remote calls. Authorization sampling plus guard defines the permitted commit boundary, not an arbitrarily stale token group claim. Directory refresh failure still uses the user's last-known-data policy; PostgreSQL failure does not.

Alert/incident command results follow their parent lifetime. Tenant, preset, dashboard, maintenance, correlation and operator completed command results retain 90 days unless their existing supplement requires a longer hold. After full result expiry, a minimal command fence returns 409 `command_result_expired`; it never executes the old command again. This permanent internal-command fence is separate from explicitly finite external ingestion retry windows. Protect minimal command completion evidence independently before compacting its authoritative replay record; do not retain response content indefinitely.

## 8. Collection reads and search consistency

Preserve the existing differences: alert feeds/previews use five-minute PIT snapshots; incident and new maintenance/dashboard/rule lists use live keyset pages with 15-minute cursors; identity/grant lists invalidate on their relevant semantic collection revision; retained history/audit uses an upper recording watermark and 15-minute cursors. Default 50/max 200 everywhere unless a prior bounded selection contract differs. Every page reauthorizes, reapplies retention, and binds cursor to tenant, session, query, ordering and environment/epoch when relevant. No long database transaction survives a browser request.

For live lists explain that concurrent edits can reorder items; refresh from the first page and preserve explicit selection by immutable ID, not row number. Within one incident detail/count response use a PostgreSQL repeatable-read read-only transaction so links and counters agree. All PG detail responses expose current authority; ES results expose indexing/maintenance freshness. Do not claim a single atomic snapshot across PG authority and ES search.

Use the alert technical profile's Unicode tokenization/full casefold for incident free text: AND all distinct tokens across current title, description and undeleted notes, q <= 256 code points. Select transactional `incident_search_tokens(tenant_id, incident_id, token_digest, token_text)` rather than a length-limited tsvector lexeme: SHA-256 digest supports indexed candidate lookup, full token text confirms equality so collisions never merge matches. Unique `(tenant, incident, digest, token_text)` is implemented through a per-incident digest guard plus exact comparison, not a potentially oversized B-tree text key.

Do not index a source token longer than any possible normalized valid query token; keep the original content intact. Store one token row per distinct full token with UUID identity and a nonunique bounded digest index; serialize replacement under incident lock. This avoids index-key size limits without imposing a new note-content limit. Other resource name search uses normalized literal substring matching, with no regex/query DSL and a 128-code-point search bound; index-assisted optimization must preserve the literal semantics.

## 9. Correlation APIs, editor and diagnostics

Under `/api/tenants/{tenant_id}`, select `GET/POST /correlation-rules`, `GET/PUT/DELETE /correlation-rules/{id}`, `POST /correlation-rules/{id}/enable`, `/disable`, `GET /correlation-rules/{id}/history`, `/history/{revision}`, `/diagnostics`, and `POST /correlation-rules/validate` and `/test`. Create 201; replace/action/delete 200 with existing command/revision conventions. DELETE requires headers. Full replacement explicitly classifies metadata versus expression/window/grouping changes and returns the resulting revision/epoch/grouping generation/reset reason. No priority, threshold count, owner or assignee field is accepted.

Default list includes active non-deleted enabled/disabled rules in their actual arbitration order: original creation time then UUID bytes. Preserve name/intent/health filters and optional retained deleted-history access; a name sort may be selected explicitly without changing arbitration. Editor has name, explicit incident severity, description, 1–10 labeled condition rows, window default ten minutes and up to three ordered grouping fields. Show an unblocking overlap reminder, and explain which edits clear evidence or change grouping before Save. Test selects one current tenant alert; results include each condition, typed group and eligibility exclusions without generating evidence. Diagnostics pages current health, bounded group/condition summaries, counts and safe last error/reset reason; no unbounded membership dump or sensitive payload in errors. Deleted rules remain read-only through retained history; copy requires a new name/UUID and fresh boundaries.

## 10. Incident routes and aggregate contracts

Under the same tenant prefix, select `GET/POST /incidents`, `GET /incidents/{id}`, `PATCH /incidents/{id}` for title/description, `POST /incidents/{id}/status`, `/assignment`, `/alerts/link`, `/alerts/unlink`, and `POST /incidents/move-alerts` with source/destination IDs, both expected revisions and <=100 distinct alerts. `GET /incidents/{id}/alerts`, `/activity`, `/cycles`, `/notes` and `/notes/{note_id}/history` are paged reads. `POST /incidents/{id}/notes`, `PATCH/DELETE /incidents/{id}/notes/{note_id}` use expected incident revision and command identity; no independent note lock can bypass the aggregate revision. No incident DELETE route or severity mutation exists.

Status accepts the target among open/investigating/resolved and performs the already selected transition/reopen rules. Assignment accepts one eligible immutable user ID or explicit null. Mutations return authoritative aggregate revision and relevant changed values, not an unbounded incident with all links/history. Creation with initial links is atomic. Automatic all-eligible attachment remains uncapped by the manual 100 selection limit; large background operations are not truncated by HTTP timeouts. Lifecycle/history/inactivity and counterpart-unavailable semantics are unchanged.

## 11. Shared PostgreSQL conventions

The physical schemas below complete D5 alongside technical supplement 8–10 and maintenance/dashboard schemas. Use UUIDv4 resource/event identifiers, bigint monotonic revisions/orders, `timestamptz` for system instants, bytea for canonical digests/raw evidence, text for exact user/source content, and JSONB only for validated immutable snapshots or bounded variable structures. Use explicit NOT NULL, check constraints for enums/ranges, tenant-inclusive unique/FK relationships, and minimal identity tables when content may expire before references. No cascade may delete another resource's surviving history.

Current metadata, grants, sessions, name claims, jobs and evidence tables start unpartitioned. Alert history retains its 32 alert-ID hash partitions; incident history uses 32 incident-ID hash partitions. Append-only product audit uses unpartitioned tenant/time indexes initially because dependency holds make dropping whole time partitions unsafe. Choose indexes listed below and validate actual query plans/allocations; no universal JSONB GIN or infrastructure partition/shard count prescription.

Human API roles are non-owner/non-BYPASSRLS with FORCE tenant RLS and transaction-local tenant scope; separate narrowly granted system worker/migration roles have explicit trusted scope. Global access still performs an explicit tenant authorization decision. Reset pooled transaction state before reuse; never let session variables leak a tenant. SQL migration ownership is separate from runtime identities. Tenant foreign keys and row-level security are complementary, not replacements for application permission checks.

## 12. Identity, access and audit physical records

Use `tenants` (UUID, kind, display name/key, revision, permission revision), a partial unique Global singleton and unique global name claims; `principals` (internal UUID, directory source/immutable object ID, kind, eligibility/tombstone), unique source/object identity; `oidc_bindings` unique issuer/subject referencing that principal; and `tenant_grants` unique tenant/principal with role, actor and revision. No tenant delete/disable column is exposed as a feature.

Use immutable `directory_verifications` with completeness/timing/coverage and semantic revision, staged `directory_objects`/`directory_edges` then atomic accepted-generation pointers. Unchanged re-verification advances freshness, not semantic content. Key group edges by immutable IDs; keep accepted complete membership sets/closure for tracked roots with path/coverage proof, cycles deduplicated. Publish known negative eligibility immediately with its own revision; partial absence never deletes grants. Bound staging by the qualified directory allocation and abandon only unpublished incomplete generations. Current negative evidence cannot be overwritten by an older generation.

Use `auth_sessions` keyed by hashed random handle with principal, provider binding/sid, encrypted tokens, auth/activity/absolute times, revocation and refresh generation; `login_transactions` one-use hashed state/browser binding, encrypted verifier/nonce and expiry; `logout_fences` and `authorization_guards`; and tenant/platform audit events with actor snapshots and before/after grant/config evidence. Index session principal/sid/expiry, principal/object ID, grants principal/tenant, tracked root/dependency, audit `(scope, recorded_at, event_id)` plus actor/action. Keep the identity supplement's cache/session/audit lifetimes; encrypt sensitive protocol state using the selected versioned envelope mechanism. Never index/log raw tokens.

## 13. Operator and provisioning physical records

Use `operators` (UUID, immutable tenant, display name, lifecycle, revision, integration health, admission-fence and desired generation), global `operator_name_claims`, `operator_credentials` (UUID, operator/tenant, state, verifier digest, encrypted material/wrapping-key version, activation/retirement/revocation times, Kong IDs), `operator_operations`, `operator_steps`, `remote_bindings`, `operator_activity` and command/denial fences. Partial unique indexes enforce at most one current and one retiring credential per operator; unique verifier/remote credential binding; checks require retiring deadlines and erase invalidated ciphertext as part of revocation/expiry transactions. Prepared generations may exist only within the single serialized provisioning operation.

Index pending operation/due/lease, operator tenant/name, credential ID/operator/deadline, alerts by operator and pending inputs by operator for deletion guards. Persist nonsensitive desired state, step fingerprint, observed remote version, acknowledgement/readback and uncertain outcome separately; never store secret-bearing remote response bodies. Use a dedicated global Grafana-writer coordination record, with the actual external CAS or controlled-writer prerequisite unchanged. Runtime service accounts accessing ciphertext are limited to copy/provisioning roles; ingestion checks IDs/verifiers/state without decrypting.

## 14. Preset, dashboard and configuration schemas

Use `preset_identities`, `presets` (UUID/tenant, name/key, revision, CEL source/profile/digest, validated ordered sort/columns JSONB, actor/times), scoped name claims, immutable `preset_revisions` and `preset_activity`; dashboard tables are defined in its supplement. JSONB configuration has schema-version validation and cardinality checks, not arbitrary caller attributes. Tenant/preset/revision and tenant/event IDs are unique; index tenant/name, update time, history recording order and dashboard references.

Use `tenant_configuration_guard` for preset-delete/panel-reference races and `tenant_resource_generations` for each resource collection. The guard precedes resource locks; collection/generation writes happen after domain work and cannot reacquire a domain lock. Current queries/definitions are authoritative in PG, never ES. Saved configuration commits history, receipts, resource generation and live outbox together. History references immutable content revisions with required retention holds; deleting metadata does not cascade into alerts or presets referenced by surviving current dashboards.

## 15. Incident persistence and search

Use `incident_identities` for minimal UUID/tenant/retirement fences; `incidents` for current title/description/fixed severity/status/assignee/revision, immutable manual/correlation origin, context UUID, current cycle, last activity/deadline and latest resolution/retention deadline; `incident_cycles`, `incident_activity`, `incident_notes`, `incident_note_revisions` and incident command results. Partition parent-owned histories by incident UUID with keys including that partition key. Lifecycle checks prevent an active status with a resolved current cycle; severity/origin changes are prohibited by command contracts and guarded database mutation routines.

Use `incident_alert_links` with a current membership identity and link/unlink provenance, plus parent-owned link activity. Unique tenant/incident/alert current references prevent duplicate logical counts. Active alert claims remain the baseline's unique `(tenant, alert_id)` relation; active context claims are unique tenant/context. A link can remain after resolution without an active claim. Retained link references target minimal identities, so one parent's purge can remove its content without cascading into the survivor. Index incident current status/activity/id, severity/id, assignee, origin/context, resolved deadline and link alert/incident lookup. Search token storage follows decision 8 and updates in the same incident content/note transaction.

A source lifecycle change may affect linked active-incident activity. Under the coordinator, discover and lock the affected incident IDs before alert IDs; recheck links/status after locks. Text/note writers that skip the coordinator lock only their incident and never later acquire coordinator/alert locks. Expiry/reopen/links/moves use the common domain order. Counter/detail reads are PG-authoritative and distinguish retained suppressed alerts from unavailable references.

## 16. Correlation persistence and large grouping values

Use `correlation_rules`, `correlation_conditions`, immutable revisions/activity, `correlation_contexts`, `correlation_evidence`, `correlation_boundaries`, `correlation_journal`, per-tenant cursor/pending state and bounded diagnostics. Conditions have stable UUIDs and ordered labels/source/profile; current rule stores configured intent, health, original creation time, revision/epoch/grouping generation, window, severity/description and normalized-name claim. Uniqueness includes tenant and immutable identity; enabled/disabled active rules share the name namespace.

Context identity must include the **complete typed canonical group key** even when values are large. Store canonical bytes plus SHA-256 lookup digest and an immutable context UUID. Under tenant coordination, search the bounded digest bucket and compare full bytes before reusing a context; distinct full keys sharing a digest receive distinct context UUIDs. Do not use a unique digest as group identity or put unbounded group bytes in a B-tree key. Context ordering for arbitration compares complete canonical bytes in the application under the qualified bounded candidate set. Active claims use context UUID, which was established by full equality.

Evidence key is tenant/rule/epoch/context/condition/alert, with original qualifier reference/start/expiry/observed semantic revision. Index rule/context/condition/expiry and alert ID for retraction; index journal `(tenant, change_order)`, boundary scope and expiry cleanup. Unique epoch memberships prevent replay duplication. Keep full before/after journal snapshots until cursor/consumer holds permit compaction, never only a digest that cannot prove transitions. Contexts with active/retained incident or pending reset/proof dependencies persist; stale empty evidence does not count against live budgets. Current metadata and fences remain distinct from purgeable detailed diagnostics.

## 17. Complete transaction and lock hierarchy

Use READ COMMITTED for writes plus explicit locks; request-scoped consistent multi-query reads may use REPEATABLE READ. Acquire authorization guards first, then any required tenant coordinator. Domain order is sorted rule/window IDs → full context keys → incident IDs → alert IDs → owned child/proof rows. Operator provisioning/credential operations acquire coordinator then operator/credential rows and do not subsequently acquire earlier domain categories. Configuration-reference operations use their independent guard and preset-before-dashboard order; they do not acquire domain coordinator afterward. If a future operation needs both domains, acquire coordinator before configuration guard from the start.

Allocate view/resource/projection progress after domain changes without reversing lock order. Outbox/receipts commit in the same transaction. Remote HTTP, LDAP traversal, CEL compilation and ES searches happen outside locks; compiled input is checked against current revision/profile before applying. Bounded evaluation that determines authoritative state runs under the selected transaction/proof guards. Deadlocks/serialization failures roll back and retry the whole unit from fresh state, using the same command/event identity, within request deadlines or durable-worker retry policy. No distributed transaction is required for remote operator work; its existing saga and admission fences apply.

### Alert transport progress

The Kafka alert path has no PG capacity reservation or backlog gate. Observe partition offsets, low watermarks and retention risk without rejecting healthy broker admission for processor lag. Source UUID/result and immutable changed bytes are proof rather than polled dispatch work. Legacy capacity tables persist only for the offline cutover drain. Commands still commit their idempotency receipts and state atomically; non-source alert changes attempt best-effort search notifications after commit, repaired by authority reconciliation. See [Kafka pipeline](spec-kafka-alert-pipeline.md).

## 18. Non-alert events and background work

Every effective resource mutation appends a versioned application outbox event with event UUID, tenant/resource kind/UUID/revision, cause/command identity, recorded time, and affected resource-generation vector. Default payload is invalidation metadata, not full configurations, LDAP membership, alert bodies or keys. Durable domain consequences already reside in PG jobs/journal; Redis hints only prompt authorized refetch. No new Kafka topic per resource and no hidden dependence on Kafka delivery for a successful local configuration save.

Use explicit consumer keys/delivery state in `application_outbox`; acknowledge a resource live hint after publication because generation reconciliation repairs loss. Required provisioning/cleanup/maintenance work has its own durable completion proof and is not deleted with a hint. UI mutation responses carry the committed generation for read-your-writes. Versioned worker job envelopes contain immutable task identity, expected generation, scope, checkpoint and retry state; unsupported versions block visibly. Alert received schema 2 carries validated payload/routing/time; source changed events reference immutable committed proof. Neither uses a PG dispatch relay.

## 19. Unified retention and configuration history

This matrix summarizes product retention; resource documents define hold and cleanup details. “Days” always means elapsed 24-hour days; holds extend only needed content/proof. No manual history editor/deleter is added.

| Record family | Product lifetime |
|---|---|
| Alert and incident current/history/notes/commands | Retain while active; retire 90 days after latest actual resolution together with parent-owned content. Reopening cancels retirement. |
| Tenant/access and platform access audit | 365 days from recording, with required recovery/dependency holds. |
| Operator history, key management/copy audit | Existing 365-day rules; metadata after operator deletion follows operator supplement. |
| Preset and dashboard configuration | Active current persists; superseded revisions 90 days from supersession, events 90 days from recording, final deleted definition 90 days from deletion. |
| Correlation configuration | Active current persists; superseded revisions/events retain their existing 90-day rules; **final deleted definition 90 days after deletion**, extended by retained incident/pending-proof references. |
| Maintenance configuration/history | Complete while non-deleted, including ended; 90 days after deletion and longer while retained alert/pending proof requires it. |
| Platform application configuration and controlled repair audit | 365 days from action; safe secret-version references only. Current sanitized deployed configuration persists. |
| Completed jobs/attempts/ordinary command results | Existing resource rules, otherwise 90 days from completion; pending work never expires by age. |
| Minimal retired IDs/internal command and recovery fences | Indefinite initially; no unproved finite replay horizon. External ingestion retry keys retain their separate finite windows. |

A retained event holds its referenced before/after content for its lifetime. Actor display snapshots follow the owning record; current principals/caches follow identity rules. Daily dependency-aware cleanup targets removal within 24 hours of eligibility under qualified healthy capacity, with bounded work and rechecks. Expired unprotected history is hidden even if cleanup is delayed. Infrastructure logs, backups, Kafka and physical ES segments remain owner-managed; no product retention claim promises media erasure there.

## 20. Cross-resource deletion, replay and restore

Generalize the technical baseline's protected intent → authoritative logical retirement → independently protected final fence → bounded physical deletion to incident purge and deletable configuration resources. For presets/dashboards/rules/maintenance, protect the deletion intent before successful logical deletion can erase its last independently recoverable identity; reconcile pending/cancelled intent after races. A remote evidence failure leaves the requested deletion pending/uncommitted with an explicit retry result, never a false successful delete. Configuration deletion does not depend on ES, but does depend on required recovery protection. No name is released before its resource's logical deletion/rename gate succeeds. Operator deletion retains its additional mandatory Grafana gate.

Incident purge rechecks resolved/latest-resolution deadline and pending commands/proof under coordinator/context/incident/alert lock order; it releases no active ownership because only resolved incidents are eligible. Remove incident content and search tokens, remove its own link history, preserve only minimal counterpart provenance in surviving alert history. Never cascade-delete linked alerts or retain a purged incident's title/description through another current projection. Configuration history cleanup similarly preserves required references and minimal identity fences without retaining full expired payloads.

Use one **recovery-evidence adapter contract** for all minimal irreversible effects: immutable idempotent append, ordered namespace checkpoints, integrity verification, durable acknowledgement and independent protection against the PG recovery point. It carries IDs, revisions/digests, operation kind and intent/final/cancel evidence, no source/config content or keys. Actual supplied storage/interface is an integration binding, not an assumed new application datastore. If no service can supply the required independence/durability, retirement/restore readiness remains gated; do not weaken deletion or credential safety.

Rollback restore always rotates deployment epoch, invalidates restored human sessions, verifies clocks and protected permission/credential/deletion/command evidence, reconciles pending work/order/retention, rebuilds or verifies search and only then reopens the corresponding paths. A database restore alone never proves readiness. Missing authoritative data cannot be regenerated from Kafka guesses. Manual repair records exact scope, operator, reason, evidence, precondition and corrective event; unsupported gaps remain fenced rather than silently skipped. Existing explicitly authorized correlation reset remains a fresh-boundary action, not a general source-data-loss waiver.

## 21. Application security and secret boundaries

Serve a single HTTPS origin; require strict configured issuer/upstream hosts, certificate validation and managed trust bundles. Apply CSP restricted to self with per-response nonces where needed, frame-ancestors none, no object embedding, nosniff, restrictive referrer policy and HSTS through the approved gateway configuration. Load fonts/scripts/assets locally. Escape all source/user text; no HTML/Markdown evaluation. Render validated runbook URLs as links with safe new-tab relations, never server-fetch arbitrary alert URLs. No user-configured external webhook/test destination or SSRF-capable preview is added.

Disable caching of protected API/session/HTML data at Next.js, browser intermediary and reverse proxy layers (`private, no-store`); hashed public static assets may be cached. Next.js data cache must not share one tenant's protected fetch across users. Keep CSRF/session/OIDC protections from the identity supplement. Limit accepted proxy identity/forwarded headers to trusted ingress; native v1 remains deliberately unauthenticated but reachable only through its intended internal route with size/capacity controls, not an invented user-auth requirement.

Use mounted, versioned OpenShift Secrets for service credentials/wrapping keys under approved encrypted secret storage. Share the operator AES-GCM envelope mechanism for session/token secret material; use separate key purposes/associated data. Rotate wrapping keys on the existing 90-day/compromise schedule, test rewrap before retirement and preserve required supported recovery versions. Cursor/CSRF signing/encryption keys have separate purposes, key IDs and rotation overlap at least the longest valid cursor/login transaction; deployment-epoch change invalidates obsolete cursor contexts. Restrict access by workload role, never expose secrets in health/metrics/logs or client bundles. Service identity privileges are capability-scoped; no runtime database owner, platform admin or shared human credential.

## 22. OpenShift workloads and readiness

Select separately deployable frontend, Product API/SSE, Ingestion API, Kafka source processor, correlation worker and search indexer roles, plus explicit recovery/proof helpers. REV-36 puts live hint publishing inside the Product API alongside SSE and reconciliation. Maintenance/scheduler, retention sweeps and directory polling are nice-to-have; operator provisioning runs inside Product API requests. Each active service owns its image and entrypoint, with separate pools, concurrency budgets, credentials and probes (REV-37). A migration job is separate and runs before new writers; APIs never race schema migration during startup. Run as a non-root arbitrary UID compatible with OpenShift, read-only application filesystem with explicitly bounded temporary storage, dropped capabilities and least-privilege service accounts. No dependence on pod-local files for durable state.

Liveness checks process health only; readiness is capability-specific. Ingress needs Kafka acknowledgement and trusted Kong policy context for v2, with immutable Global routing for v1; it has no Appchi PG, ES or Redis dependency. Product metadata needs PG/auth authority; search endpoints additionally require ES/profile/index readiness. Workers require their processing/proof dependencies. Global process readiness must not unnecessarily take healthy metadata or ingestion offline during a search failure; expose per-capability status internally and return route-specific 503. Public probes contain no tenant details. Client pool/concurrency totals across replicas must stay within agreed service allocation, with bounded acquisition timeout and no unlimited connection burst.

On termination, mark the instance draining, stop new admissions/jobs, finish or roll back ordinary transactions, close SSE with reconnect hints, flush bounded producer work and release only owned leases. Request a 60-second application termination grace through the deployment team. A longer atomic worker operation interrupted at the deadline rolls back and safely retries; shutdown never truncates a committed attachment set. Fencing prevents an old worker from committing after lease loss. Actual replica placement/autoscaling/resources are outputs of the qualified application profile and OpenShift team's allocation; no infrastructure topology is prescribed. Next.js standalone deployment is the selected build target. [Next.js self-hosting](https://nextjs.org/docs/app/guides/self-hosting).

## 23. Measured capacity profile and readiness rules

Close N1's decision process with a versioned **application capacity profile** per release/allocation. It records enabled-rule, live-group/evidence, CEL work-unit, overlapping maintenance-window, queued projection/work-byte, DB/ES/client concurrency and compilation-worker limits. Keep already selected hard native sizes, panel count, 1.8m/2.25m pending item limits, 250/s sustained and 500/s recovery objectives. Previously illustrative 50/100-rule workloads are not automatically promoted to product quotas.

Determine each new numerical budget by increasing the relevant workload dimension under the other worst-supported dimensions, measuring the maximum profile that passes all correctness/latency/recovery requirements within supplied allocation, then selecting an application limit at or below 80% of that demonstrated capacity. If a dimension is not monotonic or interactions invalidate that margin, qualify the chosen combined profile directly; do not multiply independent maxima. This margin applies to application limits, not another team's infrastructure headroom policy. CEL uses the already selected deterministic cost units, validated against elapsed execution; memory/bytes include retained history and projection expansion, not only JSON input bytes.

Every profile contains workload generator seed/distribution, data sizes/history growth, software/service capability digests, measured results, limit values, approval record and failure behavior. Missing/invalid profile keeps affected automatic processing or new configuration reservations unready and visibly blocked, preserving accepted work and prior native-admission semantics. Do not enable a feature with infinite/default fabricated quotas. Lowering a limit cannot evict accepted state: reject a profile rollout whose current protected usage exceeds it, or drain through ordinary lifecycle while retaining the prior qualified profile. This is a completed sizing method and enforcement design; measurements still must be produced.

For the isolated local development stack only, a bounded correlation preview may use an explicitly unqualified profile after connected PostgreSQL rule/runtime checks. Bind that preview to the local deployment epoch, source digest and retained check evidence; require finite rule, group, evidence and CEL limits, an audited local activation, healthy source order and no maintenance windows or effects. Staging and production continue to require the fully measured, approved profile above. The preview establishes no release throughput, recovery or production-readiness claim (REV-30).

## 24. Service capability manifest and integration handoff

See [delivery service bindings](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/status/delivery-readiness.md#service-bindings).

## 25. Team-owned Keycloak operations

Retain the selected existing internal Keycloak and dedicated environment realms. The Appchi team owns sanitized realm/client/mapper configuration, theme/application password sign-in/console MFA/refresh policy, administrative access and upgrade/recovery verification. Require at least two individually accountable trained administrators, MFA, separate nonproduction credentials, and an audited privileged recovery procedure through the company's identity verification process. This is staffing responsibility, not invented employee assignments or an Appchi-local super-admin bypass.

Release realm/config changes through staging exports/diffs and reviewed deployment jobs, with secrets injected separately. Keep a safe configuration export with each release; it is not a backup of user/session/database state. Coordinate Keycloak's database/secret recovery with their owning services, then verify immutable LDAP bindings, application password sign-in, console MFA and revocation before login readiness. Test upgrades against the full sign-in/directory/logout matrix before production. Operational logging/retention uses the existing approved service; no new infrastructure backup schedule or HA topology is asserted. A Keycloak outage continues the already selected valid-local-session/last-known-identity behavior.

## 26. CI and release artifacts

See [delivery ci and release artifacts](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/status/delivery-readiness.md#ci-and-release-artifacts).

## 27. Full-system acceptance matrix

See [required cross-system acceptance checks](../verification/verification-plan.md#cross-system-acceptance).

## 28. Delivery sequence and rollout

See [delivery delivery sequence and rollout](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/status/delivery-readiness.md#delivery-sequence-and-rollout).

## 29. Source processor repair API

Preserve the existing source-head rule: ten consecutive processing failures block that tenant's source processor until an audited global-super-admin retry after repair. Expose `POST /api/admin/tenants/{tenant_id}/processing/retry` with command UUID, expected block generation and a required 1–1,000-code-point plain-text reason. Recheck current global privilege and unchanged head/proof condition; 200 resumes that same durable item without marking it applied or changing its event/time/order. A stale generation is 409; unrepaired required proof is 409 `repair_required`. Record the attempt/result in platform repair audit and current health. This action cannot skip/reject the item, reset correlation evidence or lower any retention/credential fence. Relay/index retries retain their automatic durable retry policy.

Operational response procedures are in [Runbooks and support](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/status/delivery-readiness.md#runbooks-and-support).

## 30. Delivery evidence

Track implementation and executed evidence in [DEL-01–DEL-08](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/status/delivery-readiness.md#evidence-register). Design issue IDs are preserved in [Design register](../decisions/design-register.md).
