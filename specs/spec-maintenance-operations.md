# Maintenance

**Later user decision — 2026-10-24 (REV-39):** maintenance is always on in every environment; there is no capability gate or activation command, and restore does not turn it off. Per-window Enable/Disable intent stays. Section 17 budgets are optional configured numbers; an unset budget is unlimited. Alert reads still fail with `maintenance_proof_unavailable` when an alert has no current maintenance checkpoint. Window deletion still requires the `recovery` and `human_auth` gates and the recovery evidence store. See the [design register](../decisions/design-register.md#rev-39--always-on-correlation-and-maintenance-2026-10-24).

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

The 2026-09-30 [Kafka-first pipeline](spec-kafka-alert-pipeline.md) governs alert transport, gateway admission, UTC ordering, manual correlation, search reconciliation and cutover (REV-33). Unrelated product behavior remains unchanged.

One-time suppression windows: scheduling, matching evidence, overlap, APIs, history and recovery.

## 1. Window identity and editable content

Use an immutable UUID and immutable tenant ownership. Names remain **nonunique**, normalized to NFC, trimmed, 1–200 Unicode code points, single-line, with Unicode control/format/line/paragraph separators rejected. Preserve capitalization and interior ordinary spaces. Reason is optional plain text, default empty, at most 10,000 code points, preserving line breaks and rejecting NUL. Editors may change name, reason and display timezone on any retained non-deleted window, including after expiry. No owner, recurrence, tags, priority, archive, bulk mutation or cross-tenant copy is added.

Create enabled. Store configured enabled intent separately from derived phase (`scheduled`, `active`, `ended`, `deleted`) and processing health (`healthy`, `updating`, `blocked`). Disabled is a visible intent, not a way to rewind time. Expiry is permanent; a disabled window also becomes ended at its end. The irreversible start lock is set once trusted database time reaches its configured start, regardless of enabled state or scheduler delay. Late creation or a permitted edit moving start into the past locks start/CEL immediately. Rename/timezone/reason changes never unlock or restart it.

## 2. Schedule representation and timezone conversion

Creation requires `timezone`, `start_local`, `end_local`, and `start_occurrence`/`end_occurrence` when the corresponding local time is ambiguous. Local values use `YYYY-MM-DDTHH:mm:ss` without offset; occurrence is `first` or `second`. Seconds precision suffices for entered schedules; database action/receipt instants retain microseconds. Require year 0001–9999 and UTC conversion within that range. Require a recognized case-sensitive IANA identifier or explicit `UTC`. Reject numeric-offset-only timezone identifiers, nonexistent local times, omitted ambiguity choices and choices supplied for a nonambiguous endpoint. Return the two candidate UTC instants/offsets for ambiguity errors. End must be strictly after start and the authoritative action time. No arbitrary maximum window duration is added.

Use a pinned application tzdata release and Python `zoneinfo`. Validate by converting each possible fold to UTC and back, retaining only exact local round-trips and deduplicating identical instants; construction alone is not validation of a nonexistent time. First/second means earlier/later UTC instant. Save the chosen timezone, UTC endpoints, entered local endpoints, offsets, occurrence choices and tzdata version. The browser obtains supported zones and conversion previews from the API so a different browser timezone database cannot silently change the accepted instants. See [Python timezone support](https://docs.python.org/3/library/zoneinfo.html).

## 3. Schedule edits and timezone-rule changes

Use explicit update variants: metadata-only, timezone-only, or schedule edit. A timezone-only change recomputes display values from existing UTC endpoints and never reschedules. A schedule edit explicitly identifies the changed endpoints, submits their local values/ambiguity choices in the resulting selected timezone, and preserves unchanged UTC endpoints. Once started, reject changing start or CEL, including alongside a timezone change. End changes before expiry must stay future and after start; an ended window cannot be extended/re-enabled. Validate against database time after acquiring the window/coordinator locks, not HTTP arrival time.

Return stored UTC endpoints, current local rendering and the original accepted local/offset/tzdata evidence. A tzdata upgrade changes only current rendering. If different, show “Timezone rules changed; execution time is unchanged,” with original/current values. Record the application tzdata activation once in platform configuration history; do not create a user edit/revision for every window. Explicit timezone/schedule edits record before/after instants, local values, offsets, timezone, rule-data version, actor and action time.

## 4. Durable temporal configuration

Every coverage-changing control retains immutable revision, database UTC boundary, application proof order, expression/schedule and activation/deactivation lineage under the coordinator. Segments keep independent causes and end-edit history. Compare source receive UTC with that coverage; a source equal to an activation/control boundary is conservatively excluded. Scheduled start is inclusive and end exclusive when activation precedes receipt. Never use PG application order to infer ingress arrival order. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 5.

## 5. Qualification and before/after proof

**Current scope (REV-34):** Automatic assignee cleanup is deferred, so no cleanup mutation reaches this evaluation; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Qualification and before/after rules below remain normative.

For each accepted source/manual/system mutation of rule-visible fields, evaluate the historical applicable expression against its validated before/after rule-field snapshots. Use ingress source receipt UTC for coverage and PostgreSQL application order for its field chain, or authoritative manual/system action time/order. Never substitute source `time_created` or processing time for receipt eligibility. This includes verified assignee cleanup; a note-only change cannot alter a maintenance expression because notes are excluded from its catalog. Qualification is a new logical alert, a resolved-to-firing transition, or a real permitted false-to-true condition transition on a firing alert. A first-seen resolved logical alert may have historical/current maintenance coverage if it matches; it remains resolved and supplies no correlation evidence. This resolves the new-alert edge case without inventing a firing occurrence.

Repeated true matches, missing prior state, starting/enabling/editing a rule and changing a display field are not qualifying alert transitions. Evaluate both sides using the same expression selected for that input. A pre-start expression edit therefore cannot manufacture a field transition. Reconstruct a before snapshot from the immediately preceding authoritative alert state in tenant source order; do not compare against an Elasticsearch result or an arbitrary earlier history event. Missing required proof blocks unsafe processing visibly, with the admitted item retained for repair.

## 6. Per-cause suppression and interval history

Maintain one independently addressable cause per alert and maintenance coverage segment, plus the separate **v2 source-suspension cause**. V1 has no accepted source-suppression override. A qualified matching event opens the segment's cause once. True-to-true retains it; true-to-false closes it at the accepted change time, even on a resolved alert. Resolution alone does not clear a still-matching maintenance cause. Refiring may open a fresh cause under the current segment. Disabling, deletion or scheduled end stops new coverage; the next eligible source update closes existing causes under the worker-scope contract. Re-enabling never reopens old cause rows.

Effective suppression is the union of all cause intervals. Store both individual cause intervals and effective OR transitions; simultaneous ends yield one effective unsuppression, not one per rule. Every interval has start/end proof, window UUID/revision/segment or source-event reference, and recorded-at time distinct from effective time. Half-open intervals and zero-duration coalescing prevent fabricated visible suppression between equal ordered transitions. No earliest-rule-wins selection: show every actual cause, not every condition that happens to match now. Existing incident links, ownership and status remain intact.

## 7. Delayed processing and temporal reduction

Delayed source processing reduces the complete before/after field chain in application order, using each original ingress UTC instant for historical coverage. Keep current state in that application order even when receive timestamps reverse. Persist cause/union corrections and exact source-origin/release-snapshot references. Never invent a processing-time qualifier or move the original receive instant. Independent overlapping causes prevent premature release. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 5.

## 8. Correlation handoff

Commit suppression, cause/union/qualifier proof and per-alert maintenance correlation effects atomically. Source effects are consumed in tenant Kafka order; inline maintenance cannot use source proof before its changed event reaches correlation. Stable qualifiers retain their original effective release time and source lineage. A manual-created cause or manual resolve/reopen cannot seed fresh evidence at scheduled release. Clear suppressed/withdrawn evidence, recheck current state and arbitrate under the complete decision locks. Search notifications are best-effort after commit with authority reconciliation fallback. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) sections 4–6.

## 9. Controls without fan-out

Disable/delete/end stops new coverage. Existing alerts keep persisted suppression
until a subsequent source update received at or after that boundary releases the
cause. Detail, affected-alert lists and search use that persisted state. Manual
field changes within coverage retain their matching semantics. See [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler).

## 10. Deferred scheduler

A one-second due scan, durable leases and bounded expiry/control fan-out are
nice-to-have. They are not deployed and carry no initial-release expiry visibility
objective. The previous scheduler implementation is retained for future work.
Extensions still validate authoritative current time; no scheduler is needed to
reject extending or re-enabling a window whose configured end has passed.

## 11. Maintenance storage and constraints

**Current scope (REV-34):** New controls create no fan-out jobs; existing `maintenance_fanout_jobs` rows remain only as preserved pre-cutover evidence; see [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler). Other tables, constraints and lock order below remain normative.

Use PostgreSQL tables `maintenance_windows` (UUID, tenant, current revision, name/reason, CEL source/profile/digest, UTC schedule, timezone evidence, enabled intent, irreversible started lock, deleted-at), `maintenance_revisions` (window/revision immutable snapshots), `maintenance_controls` (window/control UUID, tenant order/time, old/new revision, control kind), and `maintenance_segments` (window/segment UUID, activation proof, expression revision, end/deactivation proof and generation).

Use `alert_maintenance_causes` keyed by tenant/alert/cause UUID with unique alert/segment/opening-proof; `maintenance_fanout_jobs` keyed by boundary UUID with cursor/lease/fence; and the technical baseline's alert-owned suppression history/checkpoints. All foreign keys include tenant. Current cause rows reference minimal alert identity records, while history follows the retained alert. Window identity is separate from purgeable content so surviving proof has no dangling foreign key. No unique name constraint. Check end > start, valid phase/intent, monotonically increasing revisions, unique control order and one current revision.

Index `(tenant, deleted_at, end_at, id)`, scheduled start/end partial indexes, `(tenant, normalized_name, id)` for listing (nonunique), revision/control order, cause `(window_id, segment_id, alert_id)` and `(tenant, alert_id)`, job due/lease and retention dependencies. Window/control/revision/job records start unpartitioned; per-alert cause history uses the technical baseline's 32 alert-ID hash partitions. Locks follow coordinator → sorted rule/window UUIDs → contexts → incidents → alerts → cause/checkpoint rows. Scheduling never acquires the coordinator after a domain lock.

## 12. Lifecycle and command APIs

All routes below are under `/api/tenants/{tenant_id}`. Viewer reads; edit/admin manages. Create/update bodies are limited to **256 KiB for maintenance definitions**, accommodating the reason and CEL limits with JSON escaping; this is an explicit resource exception to the common 64 KiB default. Validate decoded field limits as well as raw body size.

| Route | Contract |
|---|---|
| `GET /maintenance` and `GET /maintenance/{id}` | Current list/detail; optional retained-deleted list mode. |
| `POST /maintenance` | Command UUID, name, reason, CEL and explicit local schedule/timezone; 201 authoritative definition. |
| `PATCH /maintenance/{id}` | Command UUID, expected revision and explicit metadata/timezone/schedule update; 200. |
| `POST /maintenance/{id}/enable` or `/disable` | Command UUID and expected revision; 200, including valid no-op. |
| `DELETE /maintenance/{id}` | Command UUID in Idempotency-Key and quoted revision in If-Match; 200 deletion receipt. |
| `GET /maintenance/{id}/history` and `/history/{revision}` | Retained revisions/events, including deleted definition for current readers. |
| `GET /maintenance/{id}/alerts` | Paged current cause-bearing alerts, or explicit retained historical coverage; tenant authorization and parent retention apply. |
| `POST /maintenance/validate` | Read-only candidate validation; 200 with valid/diagnostics and converted endpoints. |
| `POST /maintenance/test` | Valid candidate plus one existing alert UUID; side-effect-free results. |
| `POST /maintenance/{id}/test` | Assistant-selected saved-window convenience: current `expected_revision` and one `alert_id`; evaluates persisted CEL and UTC endpoints, including ended windows, without rescheduling. |
| `GET /timezones` | Supported zone identifiers, tzdata version and current offsets; no implicit schedule selection. |

Strong ETag is current configuration revision. Same-value saves/actions are no-ops with a receipt, not new revisions or activations. Expired re-enable/extension, immutable start/CEL, stale revision and conflicting retry are 409 with stable codes. Invalid local time/zone/field/CEL is 422 on save; missing explicit timezone is never defaulted server-side. Authorization and common errors follow [system completion](spec-system-completion.md).

## 13. List, detail and editing experience

Default list is “Current and upcoming”: non-deleted windows with future ends, including disabled ones. Separate Ended, Deleted and All filters; support name text, enabled intent, phase and schedule-overlap range. Sort default start ascending then UUID; allow name, start, end and updated-at. Pages 50/default, 200/max; live keyset cursor expires after 15 minutes, bound to tenant/filter/order, with refresh-from-first-page behavior on changes. Duplicate names show schedule, timezone and short ID to distinguish them.

Detail shows phase/intent, schedule with timezone, reason, CEL, current causes count, processing health and history. Count affected current logical alerts including resolved/suppressed rows; this is an explanation count, not the dashboard default filter. Link to a PostgreSQL-paginated affected-alert list that includes suppression and unavailable historical references as appropriate. Do not synthesize an unsupported maintenance-ID CEL field. Editors use explicit Save/Discard; conflicts preserve memory-only drafts, with no automatic merge. Explain that deletion stops new coverage and existing suppression waits for source updates; disable is a separate action. Copy creates an unsaved new-window form requiring a future schedule, no copied identity/history/causes.

## 14. Validation and testing experience

Use the same catalog editor, explicit validation and source-span diagnostics as presets/correlation. No search on every keystroke. Validate/test is available to viewers without save rights. Test against one current alert reports condition result, selected-time coverage, and whether its current status would meet an entry category; label that a match alone does not prove a new transition. Show the no-backfill explanation prominently. Test cannot create causes, alter evidence, block a saved window or promise a future count. No historical simulation, overlap scan or hypothetical affected-alert sweep is introduced.

## 15. Audit and history retention

Record all effective creates/metadata/schedule/timezone/enable/disable/delete changes with before/after, actor identity/display, revision, control proof and reset/lock explanation. Record system start/end processing with effective versus recorded timestamps. Keep the complete configuration/change timeline while a window exists, including ended windows: automatic expiry does not delete configuration. A user deletion retains the complete window timeline for 90 elapsed days after committed deletion, and longer while retained alert history or pending proof references it, preserving the user's selected policy.

Commands retain results for 90 days from completion; protected pending operations and referenced proof persist. Minimal command and retired-window UUID fences persist indefinitely under the common recovery protocol. Actor snapshots follow their owning history, not a separate indefinite profile copy. Viewers can inspect maintenance history; tenant/access audit's 365-day policy does not silently replace this resource policy.

## 16. Deletion and cleanup

**Current scope (REV-34):** Daily retention cleanup is not deployed; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Deletion semantics, read-time hiding of expired content and protected deletion evidence below remain normative.

Deletion requires expected revision and serializes with create-cause/control writes. Close its coverage segment at the deletion boundary, mark deleted, and preserve the final definition/history; do not queue release work for existing alerts. Active URL returns 404 after deletion; explicit retained-history routes remain available. An idempotent retry returns its original deletion receipt without restarting retention. There is no undelete; copying a retained definition creates a new UUID with new future coverage.

Daily cleanup checks the 90-day deadline, retained alert references, retained Kafka replay/retention proof, pending control/reducer/correlation evidence and recovery holds. Kafka-mode cleanup stays held until that replay boundary is verified. Expired unprotected content is hidden from reads even before physical cleanup. Retire content through independently protected deletion intent/final evidence, then delete bounded chunks using the technical baseline's 24-hour normal cleanup target. Keep only minimal UUID/tenant/version/deletion/replay proof afterward. Ended but non-deleted windows remain configurations until explicitly deleted; they do not consume active evaluation quota.

## 17. Failure, capacity and recovery behavior

**Current scope (REV-34):** No expiry or control fan-out runs and overdue boundaries are not processed on a timer; ended coverage is released by later source input; see [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler). Blocking, capacity-reservation and proof-replay rules below remain normative.

Unknown rule state, timeline gaps, corrupt before/after proof or maintenance CEL failure never mean no suppression. Mark the affected window/processing health blocked and retain admitted work; stop unsafe affected source/manual transitions and automatic decisions while allowing independent reads and unaffected processing where proof permits. Do not remove existing causes on evaluation error. Since tenant source order is retained, a blocked earliest item can delay that tenant's later source work; expose that consequence. Explicit disable/delete can establish a trusted future boundary but does not guess missing historical truth for earlier accepted items. Platform repair restores proof or records a reviewed corrective event through the common repair workflow.

Use capacity-profile limits for concurrently evaluated windows and maintenance work bytes/fan-out derived by the qualification procedure in system completion. An unset limit is unlimited and an invalid configured value fails with `capacity_profile_invalid` (REV-39). Reject a new/extended/enabled reservation exceeding a configured budget with 409 before changing state; never drop already admitted events or truncate causes. Future scheduled coverage reserves overlapping-interval capacity, so a later start cannot unexpectedly violate its allocation. The reservation includes disabled windows until explicitly removed or ended if they could be re-enabled; a disabled window may release its reservation only when subsequent enablement performs a fresh capacity check. Recovery replays retained control/source proof, processes overdue boundaries at original effective times, and uses current-time correlation checks.

## 18. Live views and visibility proof

**Current scope (REV-34):** There is no fan-out completion record or scheduled-end visibility objective; reads use persisted suppression state; see [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler). Stale-count labelling below remains normative.

Each coverage control advances tenant maintenance generation and creates its fan-out completion record. Per-alert reconciliation advances projection sequence; completion records the highest required sequence after all existing affected causes are reconciled. A search/count claims maintenance current only when the applicable fan-out generation is complete and its sequence is searchable, including any newly applied delayed source work. The ordinary two-second state reconciliation and SSE invalidations carry this status. A newer control cannot be marked covered by an older completion.

Surface “Updating suppression” during lag and “Updates delayed” when unhealthy. Keep stale counts labeled rather than zero. Measure stored scheduled end → rendered current state for the existing five-second p99 objective. History, scheduler, projection and render observations retain separate timing to identify the bottleneck.

## 19. Acceptance scenarios

**Assistant-selected scalability implementation (2026-10-06):** persist a
versioned continuation at the exact input head and maintenance generation. A
strictly advancing input can update active causes and the final union interval
without rereading the alert's lifetime proof. Record full versus tail history
representations explicitly so historical union reconstruction remains exact.
The historical-input allocation is a read page size, not a lifetime alert limit;
evaluation work budgets apply to one admitted input.

For delayed inputs, changed catalogs or legacy checkpoints, read immutable input
pages in short read transactions and prepare exact reduction outside tenant
writer locks. Consume only against the same alert head, catalog generation and
source proof. An unrelated alert's tenant-order advance can relabel the prepared
new boundary without repeating historical evaluation; a same-alert conflict
requires fresh preparation. Preparation remains linear in that alert's retained
history and is not a promise of constant memory or durable background progress.
It introduces no scheduler, physical cleanup or backfill.

Normal catalog selection includes temporally relevant segments and explicitly
active cause segments. Ended or deactivated historical segments do not consume
the concurrently evaluated-window budget. Bulk commands scope preparation to
their target alerts. Exact historical fallback retains every relevant old
boundary and must not silently discard proof to fit an allocation.

See [required maintenance checks](../verification/verification-plan.md#maintenance).
