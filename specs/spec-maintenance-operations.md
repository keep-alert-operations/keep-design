# Maintenance

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

Every coverage-affecting control commits an immutable revision and control boundary under the tenant coordinator: create, pre-start CEL/schedule edit, end edit, enable, disable and delete. Boundaries contain database time, tenant order, revision and cause. Preserve a temporal coverage timeline, not just the latest enabled flag. A coverage segment identifies its expression version, activation order/time and exclusive end; disabling/deleting closes it, re-enabling opens a fresh segment. End extension before expiry extends the same segment without an interruption or fresh activation. End shortening replaces only its future end. Historical segments never silently use a newer expression or schedule.

Scheduled start/end have exact UTC effective times; command boundaries have their serialized database action time/order. Equal-time source/control ordering uses tenant order in addition to time. A delivery admitted before a create/enable/edit boundary cannot be retroactively covered, even if it is processed later. A delivery admitted after disable cannot be covered by the closed segment. At exactly scheduled end it is outside; at scheduled start it is inside if the enabling boundary already precedes it. This refines timing proof without changing native payloads or receipt-time semantics.

## 5. Qualification and before/after proof

For each accepted source/manual/system mutation of rule-visible fields, evaluate the historical applicable expression against its validated before/after rule-field snapshots. Use source admission time/order or authoritative manual/system action time/order, never source `time_created` or processing time. This includes verified assignee cleanup; a note-only change cannot alter a maintenance expression because notes are excluded from its catalog. Qualification is a new logical alert, a resolved-to-firing transition, or a real permitted false-to-true condition transition on a firing alert. A first-seen resolved logical alert may have historical/current maintenance coverage if it matches; it remains resolved and supplies no correlation evidence. This resolves the new-alert edge case without inventing a firing occurrence.

Repeated true matches, missing prior state, starting/enabling/editing a rule and changing a display field are not qualifying alert transitions. Evaluate both sides using the same expression selected for that input. A pre-start expression edit therefore cannot manufacture a field transition. Reconstruct a before snapshot from the immediately preceding authoritative alert state in tenant source order; do not compare against an Elasticsearch result or an arbitrary earlier history event. Missing required proof blocks unsafe processing visibly, with the admitted item retained for repair.

## 6. Per-cause suppression and interval history

Maintain one independently addressable cause per alert and maintenance coverage segment, plus the separate **v2 source-suspension cause**. V1 has no accepted source-suppression override. A qualified matching event opens the segment's cause once. True-to-true retains it; true-to-false closes it at the accepted change time, even on a resolved alert. Resolution alone does not clear a still-matching maintenance cause. Refiring may open a fresh cause under the current segment. Disabling, deletion or scheduled end closes that segment's causes at the exact control/end time. Re-enabling never reopens old cause rows.

Effective suppression is the union of all cause intervals. Store both individual cause intervals and effective OR transitions; simultaneous ends yield one effective unsuppression, not one per rule. Every interval has start/end proof, window UUID/revision/segment or source-event reference, and recorded-at time distinct from effective time. Half-open intervals and zero-duration coalescing prevent fabricated visible suppression between equal ordered transitions. No earliest-rule-wins selection: show every actual cause, not every condition that happens to match now. Existing incident links, ownership and status remain intact.

## 7. Delayed processing and temporal reduction

For a delayed source event, first apply its ordinary lifecycle/content transition using existing source ordering. Derive coverage using the window revisions/segments valid at its admission boundary. Reduce that event's causes through subsequent recorded control/end boundaries up to the current authoritative time. Record historical coverage even if already ended; current suppression includes only causes still effective now. Pending accepted items pin the rule timeline needed for that reconstruction, including deleted rules and earlier end revisions.

Persist a per-alert maintenance checkpoint and unique transition keys `(alert_id, cause_id, boundary_kind, boundary_id)`. The reducer merges source/manual transitions and relevant control/end boundaries in effective time plus original order; scheduled ends take precedence over a source at the same end instant. Never overwrite an already applied later alert snapshot with historical state. When a late item would affect an already recorded interval, append a linked historical correction derived from its trusted proof and recompute the affected union; do not rewrite previously recorded actor/action history. Canonical change order still describes commit order. A replay only advances a missing checkpoint/effect and cannot duplicate intervals or restart evidence.

## 8. Correlation handoff

Commit alert state, suppression materialization, interval/proof history, source outcome, correlation journal and projection/live outbox atomically. The journal distinguishes current before/after suppression from historical interval evidence. A still-firing alert whose final cause has ended receives a qualifier at the actual effective end, including when creation and historical suppression are first applied in one delayed transaction; it must not receive an additional unsuppressed-creation qualifier at the earlier admission time. Other source/manual field qualifiers retain their original proof. Resolved alerts supply none.

Correlation checks the current alert revision, current derived cause state, current rule/group/reset boundaries and current time before using evidence. A delay never extends membership or recreates a missed incident. For a delayed end at 11:00 processed at 11:05, a ten-minute membership expires at 11:10. Another continuing source/maintenance cause prevents that qualifier entirely. Any unknown maintenance proof makes that alert ineligible for automatic action until resolved; it is not treated as unsuppressed.

## 9. Immediate controls and bounded fan-out

Disable/delete atomically closes the coverage segment and publishes a durable invalidation generation. This is the authoritative effective release time; do not hold the control transaction open while rewriting every affected alert. Materialized alert booleans, search documents and per-alert history catch up through durable fan-out jobs. PostgreSQL detail and correlation decision paths derive current suppression from the cause plus current segment boundary, so an old materialized flag cannot retain an ended cause or permit premature eligibility. Detail exposes materialization pending where relevant.

Before another semantic mutation or correlation decision touches an affected alert, reconcile its due suppression boundaries in the same transaction and generate any missing journal/history/projection work. A read is side-effect-free; it may show authoritative derived current state and a history-updating indication until the durable job commits its explanation. Search/count responses expose suppression-work generation lag; they never claim to be current merely because the last indexed alert version is visible. Deletion success means authoritative rule removal/release committed, with affected-view refresh pending if fan-out has not finished. This preserves immediate semantics and the separately qualified five-second visibility objective.

## 10. Scheduler, extensions and races

Use the selected one-second due scan and durable ten-second leases renewed every three seconds. A due job carries window UUID, segment/revision, expected end and fencing generation. Under tenant coordinator then window/rule lock, recheck current authoritative time/end/intent before committing an end. A successful extension makes the old job obsolete; a shorten replaces the deadline. At the end boundary an extension is rejected even if the old scheduler has not run. Enable after expiry is rejected. Scanning start locks or ends late cannot change their effective instants.

Fan-out jobs traverse cause IDs by keyset, at most 100 alerts or 100 ms per transaction, yielding only between complete per-alert changes. Checkpoint progress, effect uniqueness and outbox commit together. New/delayed causes independently reconcile the segment on insertion, so insertion behind a completed scan cannot leave permanent suppression. Failed jobs retain pending work and retry with the shared backoff. Parallel tenants proceed independently. Qualify the largest supported expiry fan-out against the five-second p99 target; never claim that the scan interval alone achieves it.

## 11. Maintenance storage and constraints

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

Strong ETag is current configuration revision. Same-value saves/actions are no-ops with a receipt, not new revisions or activations. Expired re-enable/extension, immutable start/CEL, stale revision and conflicting retry are 409 with stable codes. Invalid local time/zone/field/CEL is 422 on save; missing explicit timezone is never defaulted server-side. Authorization and common errors follow [system completion](./spec-system-completion.md).

## 13. List, detail and editing experience

Default list is “Current and upcoming”: non-deleted windows with future ends, including disabled ones. Separate Ended, Deleted and All filters; support name text, enabled intent, phase and schedule-overlap range. Sort default start ascending then UUID; allow name, start, end and updated-at. Pages 50/default, 200/max; live keyset cursor expires after 15 minutes, bound to tenant/filter/order, with refresh-from-first-page behavior on changes. Duplicate names show schedule, timezone and short ID to distinguish them.

Detail shows phase/intent, schedule with timezone, reason, CEL, current causes count, processing health and history. Count affected current logical alerts including resolved/suppressed rows; this is an explanation count, not the dashboard default filter. Link to a PostgreSQL-paginated affected-alert list that includes suppression and unavailable historical references as appropriate. Do not synthesize an unsupported maintenance-ID CEL field. Editors use explicit Save/Discard; conflicts preserve memory-only drafts, with no automatic merge. Confirm deletion with its immediate release effect; disable is a separate action. Copy creates an unsaved new-window form requiring a future schedule, no copied identity/history/causes.

## 14. Validation and testing experience

Use the same catalog editor, explicit validation and source-span diagnostics as presets/correlation. No search on every keystroke. Validate/test is available to viewers without save rights. Test against one current alert reports condition result, selected-time coverage, and whether its current status would meet an entry category; label that a match alone does not prove a new transition. Show the no-backfill explanation prominently. Test cannot create causes, alter evidence, block a saved window or promise a future count. No historical simulation, overlap scan or hypothetical affected-alert sweep is introduced.

## 15. Audit and history retention

Record all effective creates/metadata/schedule/timezone/enable/disable/delete changes with before/after, actor identity/display, revision, control proof and reset/lock explanation. Record system start/end processing with effective versus recorded timestamps. Keep the complete configuration/change timeline while a window exists, including ended windows: automatic expiry does not delete configuration. A user deletion retains the complete window timeline for 90 elapsed days after committed deletion, and longer while retained alert history or pending proof references it, preserving the user's selected policy.

Commands retain results for 90 days from completion; protected pending operations and referenced proof persist. Minimal command and retired-window UUID fences persist indefinitely under the common recovery protocol. Actor snapshots follow their owning history, not a separate indefinite profile copy. Viewers can inspect maintenance history; tenant/access audit's 365-day policy does not silently replace this resource policy.

## 16. Deletion and cleanup

Deletion requires expected revision and serializes with create-cause/control writes. Close its segment at the deletion boundary, queue durable release work, mark deleted, and preserve the final definition/history. Active URL returns 404 after deletion; explicit retained-history routes remain available. An idempotent retry returns its original deletion receipt without restarting retention. There is no undelete; copying a retained definition creates a new UUID with new future coverage.

Daily cleanup checks the 90-day deadline, retained alert references, pending admission/control/reducer/correlation work and recovery holds. Expired unprotected content is hidden from reads even before physical cleanup. Retire content through independently protected deletion intent/final evidence, then delete bounded chunks using the technical baseline's 24-hour normal cleanup target. Keep only minimal UUID/tenant/version/deletion/replay proof afterward. Ended but non-deleted windows remain configurations until explicitly deleted; they do not consume active evaluation quota.

## 17. Failure, capacity and recovery behavior

Unknown rule state, timeline gaps, corrupt before/after proof or maintenance CEL failure never mean no suppression. Mark the affected window/processing health blocked and retain admitted work; stop unsafe affected source/manual transitions and automatic decisions while allowing independent reads and unaffected processing where proof permits. Do not remove existing causes on evaluation error. Since tenant source order is retained, a blocked earliest item can delay that tenant's later source work; expose that consequence. Explicit disable/delete can establish a trusted future boundary but does not guess missing historical truth for earlier accepted items. Platform repair restores proof or records a reviewed corrective event through the common repair workflow.

Use capacity-profile limits for concurrently evaluated windows and maintenance work bytes/fan-out derived by the qualification procedure in system completion. Reject a new/extended/enabled reservation exceeding a measured budget with 409 before changing state; never drop already admitted events or truncate causes. Future scheduled coverage reserves overlapping-interval capacity, so a later start cannot unexpectedly violate its allocation. The reservation includes disabled windows until explicitly removed or ended if they could be re-enabled; a disabled window may release its reservation only when subsequent enablement performs a fresh capacity check. Recovery replays retained control/source proof, processes overdue boundaries at original effective times, and uses current-time correlation checks.

## 18. Live views and visibility proof

Each coverage control advances tenant maintenance generation and creates its fan-out completion record. Per-alert reconciliation advances projection sequence; completion records the highest required sequence after all existing affected causes are reconciled. A search/count claims maintenance current only when the applicable fan-out generation is complete and its sequence is searchable, including any newly applied delayed source work. The ordinary two-second state reconciliation and SSE invalidations carry this status. A newer control cannot be marked covered by an older completion.

Surface “Updating suppression” during lag and “Updates delayed” when unhealthy. Keep stale counts labeled rather than zero. Measure stored scheduled end → rendered current state for the existing five-second p99 objective. History, scheduler, projection and render observations retain separate timing to identify the bottleneck.

## 19. Acceptance scenarios

See [required maintenance checks](./verification-plan.md#maintenance).
