# Verification plan

## Additional scalability regressions — 2026-10-06

- Verify coalesced indexing, unchanged-document no-op, all note tokens beyond the
  former 1 MiB projection ceiling, visible over-allocation failure and continued
  progress for independent tenants. Exercise exclusive reconciliation leases,
  expired/stale owners, lost Kafka hints, retained lower watermarks and retries.
  Keep an audit unfinished across multiple pages, admit changes ahead of and
  behind its cursor, and prove ordinary delta watermarks continue advancing while
  unchanged missing documents are repaired under the bounded audit allocation.
- Compare incremental maintenance with exact replay over long, repeated,
  overlapping and out-of-order histories. Historical input count is a paging
  concern, not a lifetime admission cap; ended windows do not consume the current
  concurrently evaluated-window budget. Verify immutable proof and no backfill.
- Confirm correlation changes only altered evidence and locks required live or
  explicitly targeted contexts while preserving dormant reset proof and order.
- Exercise one feed plus one bounded quick-count request per invalidation,
  replacement/navigation/late-response PIT disposal, idle relative-time ticks,
  hidden-tab pause, healthy-SSE polling suppression and foreground activity across
  repeated session refreshes. Recheck tenant/session token misuse rejection.
- Exercise concurrent users and arrivals together at 5,000 deliveries/minute,
  100 users and 50 tenants, recording retained data growth, exact durable/search
  counts, errors, latency boundaries and resource allocation. Keep fixture API
  tests, real OIDC/browser tests and supplied-service qualification distinct.
- Verify request deadlines under database contention and that timed-out local
  transactions cannot later commit. Recheck synchronous operator and SSE budgets.
  With ordered SQL pipelining, change the restore fence between acquisition's
  statement snapshot and the following control read; reject business entry.
  Uncertain acquisition/release must discard the connection without leaking a
  session lock.

These cases supplement the existing stronger sustained/recovery and enabled-rule
qualification requirements; executed outcomes belong in delivery.

**REV-35 scope:** directory polling and its five-minute LDAP-change propagation cases are future qualification. Current identity acceptance must cover explicit complete bootstrap/refresh, unknown-user/team refusal without evidence, last-trusted authorization, immediate Appchi grant edits, known revocation/logout/session expiry and unchanged restore gates. See [worker scope](../specs/spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**REV-34 scope:** [Worker scope](../specs/spec-worker-scope.md) supersedes acceptance requirements for deferred schedulers. Existing timer/fan-out and automatic-cleanup scenarios are future qualification, not active release gates. Pre-cutover maintenance history still requires compatibility checks.

Required acceptance cases for the selected design. Record executions, environment/version, workload, results and defects during implementation. No tests are reported as executed here. Link failures to [Design register](../decisions/design-register.md) and release evidence to [Delivery readiness](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/status/delivery-readiness.md).

## Alerts

**Current scope (REV-34):** Retention purge is deferred, so the purge-race row is future qualification; see [worker scope](../specs/spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Other rows remain required.

Following the 2026-10-11 user correction, verify Feed as the page title, sidebar
label and breadcrumb on desktop and narrow views. Alert-detail return navigation
uses Feed and existing `/alerts` URLs; saved-preset breadcrumbs remain contextual.

Implementation verification must cover these specified outcomes:

| Scenario | Required outcome |
|---|---|
| Firing → repeat → resolved → firing | One logical row; two occurrences; correct time_created; assignment reset only on the second occurrence; legacy history preserved. |
| First clear → manual firing → known source severity | Initial resolved row with clear/no invented occurrence; manual occurrence keeps time_created; known severity initialized without another occurrence. |
| Resend with same optional legacy request/item ID after manual resolution | New delivery UUID/time; source may reopen. Same internal UUID at a different Kafka offset applies only once. |
| Same payload without retry identity after manual resolution | A new arrival may reopen under the agreed source-order policy. |
| Batch contains distinct logical keys and valid/invalid members | Publish valid items concurrently, acknowledge only after broker confirmation, return ordered per-member outcomes and exact 202/207/422/503 aggregate status. |
| Same v1 key with different fixed fields or v2 digest collision | Terminal conflict; existing alert unchanged, internal terminal diagnostic retained. |
| V2 impact/severity/runbook changes | New logical key/alert; previous alert remains independent. |
| Alert operator display and managed rename | Detail, source activity and configured Operator columns show the current same-tenant v2 name; v1 shows its exact source string. Rename changes presentation without changing the stored operator ID, identity, CEL or sort behavior. Missing/cross-tenant names do not expose an ID or another tenant's name. |
| Queued Kafka source followed by manual command | Manual command commits with normal revision checks; queued source may apply later. No source_updates_pending rejection. |
| Source suspended plus maintenance; one cause ends | Remain suppressed until the final cause ends; only then can firing re-enter correlation. |
| Unchanged repeats continue for 30 days | Alert inactivity refreshed; incident inactivity still follows its independent non-repeat policy. |
| Purge races with reopening or stale projection replay | Atomic recheck protects a reopened row; deleted UUID never returns through replay; a new external firing can create a new UUID. |
| Elasticsearch/Kafka unavailable | PG history survives; Kafka failure prevents new acknowledged admission, and retained inputs resume through transactional replay. Search reconciles PG independently. Report retention loss explicitly and do not mistake lag for rollback. |

## Alert execution and recovery

**Current scope (REV-34):** Retention-purge cases are future qualification while purge is deferred; see [worker scope](../specs/spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Other execution, fault and load cases remain required.

Require a differential query suite comparing native evaluation with Elasticsearch over every supported construct, null/negation, enums, Unicode case/normalization, literal wildcard characters, long messages, years 0001/9999, pre-1970 instants, microseconds, relative-time boundaries and incident membership. Include invalid syntax/types, cost bounds and all saved-resource profile migrations. A compiled query that differs between paths cannot ship.

Exercise concurrent admission/manual writes, no-op repeats, event duplication/reordering, source crash between PG/Kafka commits, unknown commits, offset loss, blocked partitions, wrong-epoch writers, partial bulk failures, refresh delays, old PITs after purge, note deletion/search removal, SSE loss and subscribe races, identity revocation, slow/background tabs, purge/reopen/admission races, protected-intent failures, rollback restore and index switching. Require zero cross-tenant access, duplicate internal effects, fabricated correlation evidence or retired-content resurrection.

Run the existing concentrated 250/second 24-hour profile, 500/second recovery with continued 250/second input, retained-history growth and prescribed payload/rule/client mixes. Verify complete atomic attachment sets and all existing p99/availability goals. Measure the static/numeric cost budgets and allocations before publishing a qualified profile. Deliver reproducible results, migration/repair/restore runbooks and deployment capability evidence. None of these runtime tests has been performed in this documentation task.

## Operators

For the opt-in isolated local v2 setup (operator section 29), also verify that
bootstrap rejects nonlocal/production databases, restore fences and foreign gate
reasons; prepared keys remain unusable until normal activation; authenticated
serving-member proof rejects stale generation, wrong verifier and untrusted
callers without reflecting secrets; public headers cannot replace pinned mTLS;
and missing/duplicate/query/body keys fail. Verify a real native batch, per-member publication outcomes, resubmission as a new delivery, processing, search and tenant concealment through the running gateway.
Repeated Start/restart must preserve credentials, operator IDs and remote data.

Before implementation is considered complete, verify Grafana failure/partial success during rename/deletion, old/new name reservation, case-sensitive rule-label migration, concurrent rule edits, cancellation restoration, delayed old-label deliveries, and name reuse only after verified completion; also verify name races across tenants; case-only rename and name reuse; duplicate create/rotation commands; timeout after remote success; process death before/after activation; two rotations in parallel; overlap expiry under delayed cleanup; revocation/admission serialization with stale Kong state; prepared-key rejection; copy/revoke races; cancellation versus activation; deletion versus admission/late remote writes; cleanup after name reuse; and policy updates concurrent with unrelated teams under both supported writer modes.

Also verify mixed firing/resolved Grafana batches, required-field failures, timezone conversion, overflow/truncation, same-problem repeat versus new occurrence, body-label/authenticated-operator mismatch, secret absence from UI/logs/job data, successful continuation by non-Grafana senders during Grafana outages, and restore fencing. These are required implementation acceptance scenarios, not a claim that code has been built or tested in this design task.

## Presets

Verify implementation against at least: view-versus-edit separation; Global behavior; Unicode name collisions/reuse; transient filters never saved; suppressed/resolved count parity; all permitted sorts/columns and default tie-breaks; invalid/costly queries; stale environment handling; saved versus candidate preview isolation; no-op/retry/expired-receipt behavior; concurrent saves; delete versus panel-reference creation; historical-copy validation; deletion/name reuse without old-link rebinding; retention boundaries/holds; rollback resurrection protection; tenant/revision-bound cursors; late response rejection; role loss with a dirty draft; Elasticsearch/Redis/PostgreSQL outages; and shared count changes without false zero values.

## Maintenance

**Current scope (REV-34):** Lease and expiry-latency cases are future qualification; source-driven release acceptance is in the [worker scope correction](#worker-scope-correction). Other cases remain required.

Required tests cover both DST ambiguities and gaps, timezone-only edits, tzdata upgrades, disabled-at-start locking, create/edit at exact boundaries, late creation, repeats/retained matches, real false-to-true and true-to-false changes, manual refiring, first-seen resolved, two overlapping windows plus v2 source suspension, simultaneous ends, disable/re-enable, shorten/extend versus stale leases, deletion versus new causes, delayed input before/after controls, late history corrections, missing proof, crash after every transaction boundary, revision/no-op/retry behavior, tenant/role loss, retained deleted explanation, dependency holds and rollback restore. Verify exactly one effective unsuppression and no expired correlation evidence revival. Execute the selected sustained load and concentrated expiry scenarios before asserting latency.

## Dashboards

Hold a live count refresh while tenant search and the count batch report lag,
then release it and reconcile suppression/search completion. Panel positions,
retained counts and colors must stay steady on desktop, narrow and fullscreen
views; update labels stay readable without transient warning rows. Verify that
actual search failures still identify stale values and blocked source processing
still displays its error.

Verify the 2026-10-08 inline dashboard flow: name-click/pen editing; one-panel
Create/Edit dialogs with Cancel/Escape and focus restoration; each panel's options
including Delete; main-board drag/resize and keyboard alternatives; Save disabled
while clean, enabled for all definition changes, disabled after reverting or saving.
Keep CRUD/layout changes local until one complete expected-revision save. Cover
conflicts, uncertain exact-command retries, remote saves/deletion, access loss,
saved count failures and narrow layouts without responsive repacking of desktop
columns/sizes; vertical compaction applies equally across viewport sizes.

Verify the later fluid-motion/top-compaction correction: sub-cell pointer movement
and resizing follow pixels, with a valid compacted placeholder and smooth neighbor
settling. Cover rapid pickup during a settling animation, reduced motion,
Escape/pointer cancellation, unchanged snapped drops remaining clean, dropping
into empty columns, vertical reorder, gap closure after shrink/delete, sparse
saved layouts opening clean, viewer/fullscreen compaction, and explicit Save of
compacted coordinates. Horizontal blocker order, allowed sizes, non-overlap,
identity/metadata and the final 100-unit bound remain required.

Verify the 2026-10-09 toolbar correction: one editor-only Discard changes button
replaces Pause updates, stays disabled while clean/locked, confirms before reload,
and restores focus correctly on cancel/discard. No pause/resume or draft-count
preview control/request remains. Automatic foreground refresh, hidden-tab
suspension, manual refresh, saved count context checks and fullscreen focus/navigation
continue. Uncounted draft preset references ask users to Save.

Verify the later removal of visible dashboard helper/status text on ordinary,
narrow and fullscreen views. Dirty drafts retain working Save/Discard controls
without the extra reminder; accessible handle descriptions and hidden count status
remain. Following the subsequent same-day correction, Count provenance has no
button, details panel or reserved action row; internal revision/context checks remain.
Count refresh, suppression/lag completion and unavailable/stale feedback must
continue without moving panel positions.

Test duplicate references, same-PIT/clock parity with equivalent feed queries, relative-time boundary, saved-query edits during requests, name reuse, preset-delete/save races, same-value retries, stale revision/draft preservation, exact zero versus failed/partial results, purge and maintenance generation races, index switch, access loss during hidden/fullscreen/dirty views, responsive/keyboard layouts, threshold integer boundaries and deleted-history retention. Include counts/render observations in existing visibility measurements without storing sensitive query text in metrics. No additional dashboard-specific availability promise supersedes reliability objectives.

## Tenants and access

**Current scope (REV-34):** Physical audit cleanup is deferred; verify the 365-day read-time boundary rather than protected cleanup; see [worker scope](../specs/spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Other cases remain required.

Qualify canonical-name collisions, reserved Global/name reuse, atomic creation, duplicate/reordered retries, expired receipts, stale revisions and concurrent last-admin removals. Cover self-demotion, empty/nested/cyclic groups, alternate membership paths, orphaned/recreated principals, unknown versus cached directory evidence and every matrix capability. Verify tenant switching, delayed responses, hidden-resource lookups, audit reader loss, secret redaction, LDAP baseline/diff events, no-op deduplication, 365-day boundaries/protected cleanup and permission-safe restore.

## Reliability

**Current scope (REV-34):** Maintenance windows do not expire on a timer; test edits and deletion against end-time validation and source-driven release instead; see [worker scope](../specs/spec-worker-scope.md#1-maintenance-without-a-scheduler). Other cases remain required.

Run the primary 250/second concentrated-tenant workload for 24 hours, including retained data growth, and larger representative cases for four hours each. Repeat the primary path for v1 and v2 and characterize Grafana adapter overhead. Exercise the selected mixes, valid maximum sizes/batches, UI views and combined rules. Record a ten-minute startup period separately, without hiding subsequent growing backlog. Verify per-logical-key source append order and per-tenant changed order, headroom and all applicable latency objectives.

Appchi owns application load/correctness tests. Coordinate dependency fault injection and recovery in approved environments: owning teams perform infrastructure failover/restoration and Appchi verifies resulting application behavior. Also test the sixty-second overload burst; two-hour durable backlog and 500/second recovery; tenant fairness; post-commit disconnects; duplicate/reordered messages; leader loss and dependency outages; maintenance expiry racing edits/deletion; restored revoked credentials; deletion/replay protection; and full search rebuild. Require zero cross-tenant effects, duplicate internal effects or application-caused loss of retained acknowledged inputs or revoked-key activation. Assess infrastructure disaster-loss behavior against supplied service contracts rather than assuming a zero-loss capability. A profile is qualified only if its correctness and applicable objectives pass. Executed local checks are recorded separately in implementation status.

## Cross-system acceptance

**Current scope (REV-34):** Scheduled maintenance expiry, maintenance fan-out and maintenance-visibility latency are future qualification; see the [worker scope correction](#worker-scope-correction). Other scenarios and objectives remain required.

The implementation must exercise each supplement's acceptance cases, with requirement IDs and failing evidence traceable to the preserved register. Add cross-subject scenarios: LDAP role loss during a dirty dashboard or key copy; permission edit versus command commit; scheduled maintenance expiry during source backlog and correlation reset; dashboard preset save/delete/count race; incident move/reopen versus source processing; operator deletion versus admitted batch; current source-suspended plus overlapping maintenance; all Global traffic; deleted-resource restoration; and old-worker/new-schema interoperation.

Run sustained 250 deliveries/s for 24 hours and selected four-hour stress variants, full one-tenant concentration, 500/s recovery with 250/s continued intake, the two-hour backlog and 1,000/s sixty-second overload case. Include longest permitted text/Unicode, growing parent history, 24 distinct dashboard panels, relative clock queries, largest qualified maintenance fan-out and atomic correlation attachment sets. Measure p99 one-second admission/authoritative commands, two-second searches/counts and five-second incoming/maintenance rendered visibility as already selected; do not infer one from the other. Availability evaluation retains its rolling 30-day definition and low-volume rules.

Inject process crashes at commit/ack boundaries and coordinate real dependency failures/restores with owning teams. Require zero cross-tenant effects, duplicate internal effects or application-caused loss of retained acknowledged inputs, expired-evidence revival or restored revoked-key activation. Verify secret redaction and no protected browser caches after access loss. Separate application correctness from the supplied infrastructure disaster-loss contract.

## Incidents

**Current scope (REV-34):** Hourly inactivity-expiry cases are future qualification while auto-resolution is deferred; see the [worker scope correction](#worker-scope-correction). Other cases remain required.

The implementation must demonstrate: manual creation without alerts; explicit immutable severity; atomic rollback of a conflicting multi-alert selection; linking a suppressed/resolved alert to an active incident; rejecting membership edits on a resolved incident; an atomic move without dual ownership; reopening conflicts leaving all state intact; lifecycle cycles preserving previous timestamps; repeated deliveries not refreshing inactivity; genuine linked-alert transitions using original accepted times; activity updates taking effect without waiting for the hourly check; an hourly check selecting only due active incidents without rereading activity history; concurrent activity defeating a stale expiry job; expiry preserving alert statuses while releasing ownership/resetting evidence; idempotent retries creating no duplicate history/activity; note revision/deletion affecting current search while preserving history; post-resolution edits not extending retention; and tenant isolation across search, conflicts, assignment and relationship references.

## Identity

**Current scope (REV-35, REV-34):** LDAP-change propagation timing (item 2) and assignee cleanup (item 4) are future qualification; verify explicit publication instead; see [worker scope](../specs/spec-worker-scope.md#4-directory-synchronization-is-nice-to-have). Other items remain required.

1. First and returning login with username/password only (including users with previously enrolled OTP), incorrect-password rejection, no application OTP enrollment/challenge, SSO return, idle expiry, 24-hour expiry, foreground dashboards and multiple-tab refresh races. Verify separate Keycloak console MFA/recovery.
   Expired, consumed and missing callback transactions offer browser retry without
   exchanging the rejected code or creating a session; JSON clients still receive
   401. Explicit retry must create a new transaction and permit valid sign-in.
2. Direct/nested grant additions/removals, cycles, alternative paths, account disablement and super-admin loss, measured from the LDAP change through an already-open API/SSE session.
3. Partial/paged LDAP failures, identity-provider failure, independently healthy LDAP/Keycloak paths, unknown-user login and verified recovery without empty-cache authorization changes.
4. Last-admin protection and concurrent grant edits, external admin vacancy, assignee cleanup and inaccessible-tenant discovery checks.
5. Local/provider logout, signed backchannel validation, delayed callbacks, known revocation during an outage, pod restart and stale database restore.

## Correlation

Verify same-alert multi-condition matches; independent condition windows; no-op repeats after reset or restart; equal-time boundary ordering; permitted group movement; grouping A→B→A; old-generation resolution; competition between creation/addition and manual linking; no partial attachment set; delayed unsuppression without shifted membership; exact expiry boundaries despite late cleanup; stale alert revisions; crash/replay idempotency; blocking/quotas; and side-effect-free tests.


## Review regression cases

- Navigate between operational pages, administration tabs, Home and browser
  history after sign-in: preserve the mounted workspace without starting another
  initial session check. Switching tenants must clear the old tenant's content
  while the destination loads. Periodic expiry checks and sign-out must still
  clear protected content. The expired-sign-in recovery page remains accessible
  without mounting the operational workspace.

- Hold initial and refresh responses on list pages: no empty-state claim before
  the first successful response, no replacement of a confirmed empty state during
  same-query refresh, and no layout movement from routine warning/loading rows.
  Include saved preset results, maintenance timelines, populated results, changed
  filters, empty-to-populated transitions and failures before/after success.

- Compare both native schemas with the field inventory: missing required fields, optional omission versus null, unknown/generated fields, immutable identity inputs and v1/v2 separation.
- Exercise every alert-owned route, typed command value and DELETE header. Verify atomic bulk results, consistent duplicate selection, conflicting duplicate revisions and reauthorized retries.
- Race admissions in different tenants with source processors paused. Broker-confirmed items remain accepted without a PG capacity reservation; no legacy inbox/outbox row is created. Source replay applies each delivery UUID once and records terminal semantic rejection safely.
- Change alert status manually while source suppression and maintenance overlap. Source causes remain; maintenance expressions are recomputed and only their own false matches are released. Effective suppression and correlation reflect the remaining union.

## Assignment-based alert status (REV-27)

- Cover firing/resolved × assigned/unassigned, independently of legacy acknowledgement values; suppressed alerts follow the same matrix.
- Cover self assignment, assignment to another eligible user, reassignment, no-op, unassignment, resolution, repeated firing, new source occurrence and manual reopening. Verify authoritative revisions, activity, permission/eligibility checks, atomic bulk actions and uncertainty/replay handling.
- Reject retired acknowledgement commands and attempts to write lifecycle `acknowledged`; preserve stored receipts and historical activity. Verify current detail/feed/preview/incident-linked/maintenance-affected responses omit legacy ownership fields and derive status consistently. Known lost eligibility clears visible ownership; outages retain trusted data.
- Verify CEL equality/inequality/membership/presence for `display_status` and native/search equivalence under tenant and suppression filters, including page/count parity. Existing mappings/digests, old CEL rules and saved acknowledgement sorts keep their compatibility semantics; rule profiles and derived-status sorting reject the feed-only field.
- Check one detail assignment menu, bulk self/other/unassign, no independent acknowledgement actions, quick views, responsive status labels, retained activity, preset defaults and legacy column adaptation without automatic shared saves.
- Check sortable headings on All alerts and saved preset results cycle ascending, descending and regular order across server pages; changing sort restarts pagination and clears selection. Preset overrides replace the saved multi-field sort in read-only previews, and the third click restores the saved definition without a shared save. Unsupported derived/composite headings stay static.
- Regenerate and check API types; record executed checks and any unavailable dependencies in implementation status. These checks do not establish production qualification.

### Current alert JSON viewer (REV-28)

Verify View alert is available to readers and editors on alert detail, shows the loaded detail response as formatted JSON without another request/mutation, scrolls long payloads on narrow screens, and closes via Close, Escape and backdrop while preserving keyboard focus and readable content in Light and Dark themes.

### Bare CEL field identifiers (REV-29)

Verify direct approved field references, string methods on bare fields, `has(field)`, and `incident_ids` membership compile and produce equivalent native/search behavior to their `alert.field` compatibility spellings. Reject unknown bare identifiers and fields unavailable in the current context. Confirm editor suggestions, field chips, `has()` completion and quick views insert bare identifiers, while saved expressions using the old prefix remain executable without rewriting.

## Kafka-first redesign (REV-33)

Verify the [normative Kafka pipeline](../specs/spec-kafka-alert-pipeline.md) separately from legacy cutover compatibility tests:

- HTTP: no PG connection at ingress; immutable receive/default time and UUID across three attempts; concurrent partial batches; broker acknowledgement before202; failed Kafka503; no backlog gate; legacy IDs syntax-only; removed receipt lookup; five-second request and ten-second gateway deadlines.
- Source: partition append order despite reversed UTC, PG commit before Kafka failure, immutable replay after manual edit, transaction unknown outcome and fenced rebalance, duplicate UUID at another offset, mismatched UUID bytes, client resubmission and unchanged-repeat evidence, terminal semantic rejection, no offset advancement on transient failure.
- Correlation/maintenance: tenant changed order, manual resolve atomic evidence removal without incident unlink, ignored manual reopen/assignment/notes, delayed source after boundaries, exact release snapshot/origin provenance, all supporting source inputs consumed, inline release first discovered by manual edit, independent causes, equal-time control wins and clock-health faults.
- Search: lost manual/relationship/suppression/deletion hints, complete authority pass with captured lower bound, write behind cursor, newer version fencing, purge/tombstone, concurrent writes during rebuild and epoch cutover, scan progress during Kafka outage.
- Gateway: actual open-source Key Auth and installed policy plugin, prepared deny/current allow, revoked/expired deny, stale generation rejection, node-local identity and complete serving pool, exact digest/tenant/expiry proof, clock failure, erased plaintext cleanup, final rename/cancel phase, bounded authorization lifetime and deletion offset barrier.
- Migration: old work drained, new groups start at captured topic boundaries, active legacy writers refused, incompatible saved correlation CEL/grouping blocked by parsed field reference, edited rule starts fresh epoch, old event schema never consumed as new.
- Recovery: retained minimal delivery/key fences, outstanding publication/proof holds, missing protected replay baseline keeps restore closed, explicit Kafka low-watermark loss interval and reviewed reset. No client receipt service or zero-loss promise beyond supplied retention.

Production capacity, multi-node failover/rebalance, clock-discontinuity and rollback-survival runs remain required even when focused local tests pass. Actual results and remaining gaps belong in [implementation evidence](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/docs/kafka-first-implementation.md).

## Kafka topic incarnation (REV-41)

- Source: another delivery at a recorded coordinate rolls its application back and
  records `source_coordinate_conflict`; only that partition is fenced, with no timed
  retry, and unrelated partitions continue. Other retained failures log the
  exception class and code, never exception text or payload.
- Assignment: on a real broker, a received topic deleted and created again is refused
  before any producer, offset or input, with `source_topic_identity_changed` per
  assigned partition; an unrecorded identity also refuses. A full-width topic ID and
  a Windows client's 32-bit halves of the same ID compare equal.
- Cutover records both topic IDs. `--record-topic-identity` requires stopped pipeline
  groups, refuses a partition that ends below a recorded position or source result or
  holds another record at the last result, and commits no offsets.
- Qualify topic ID support and a broker-storage loss drill on the supplied broker in a
  disposable environment; local tests do not establish that.

## Worker scope correction

- End/disable maintenance without another source input: detail, search and cause
  lists remain suppressed. A note/correlation read does not release it. A source
  repeat received after the boundary releases only ended causes at receive time;
  overlapping/source suspension still applies. Delayed in-coverage input remains
  covered. Preserve pre-cutover history and no-backfill controls.
- Deferred role startup fails before connecting to services. New maintenance
  controls create no active fan-out jobs; migration preserves old job evidence.
- Operator HTTP covers all gateway/Grafana phases, returns no premature success,
  exposes uncertain/partial failure, and creates no duplicate identity on retry.
  Deleted-operator final-policy failure remains recoverable; cancelling initial
  deletion follows resumed setup. Concurrent requests respect the original leases.
- Browser retains pending state until completion, exposes failed operation recovery,
  uses the extended operator-only timeout and never advertises background progress.
- Qualify actual backend/provisioning DB roles, proxy deadlines, shutdown/disconnect,
  fleet-wide gateway proof, production concurrency/capacity and migration rollback
  independently of synthetic local tests. Identity/Keycloak replacement needs a
  separate accepted design plus nested-group/freshness/outage qualification.

## REV-36 Product API live publishing

Verify that Product API startup/shutdown owns a bounded background publisher,
blocking dependencies do not stall HTTP, Redis failure preserves pending hints,
repeated/replica publication preserves newer generations, domain RLS and SSE
authorization remain intact, and SQL pools close only after publication drains.
Ingress starts neither publisher nor subscriber. Apply 0047 and confirm the
separate live role is rejected; qualify combined API resource use and Redis loss
with PostgreSQL reconciliation in the supplied deployment. See
[worker scope](../specs/spec-worker-scope.md#6-live-updates-inside-the-product-api).

## Alembic migration conversion (REV-38)

Require fresh installation and repeated no-op execution from the packaged wheel;
all historical SQL bytes/checksums and numbering gaps must remain unchanged.
Exercise adoption of full and partial legacy histories without replaying applied
SQL or changing existing ledger timestamps/application data. Reject altered SQL,
checksum mismatches, missing/unknown migrations, history gaps, multiple heads and
version/ledger disagreement before committing any change. `current` must not
adopt or mutate a legacy/fresh database.

Using isolated real PostgreSQL, prove complete rollback of adoption and pending
DDL/ledger changes after a later revision fails, successful retry, serialization
of two migration processes under the original lock, unchanged tenant RLS, and
no API/worker access to either migration ledger. Verify native Alembic CLI and
existing Python/CLI deployment entrypoints, including execution from a wheel
without a source checkout. Reject arbitrary stamp, downgrade and offline paths.
Run affected API/identity/maintenance/search SQL compatibility cases. Existing
Kafka/scheduler cutover prerequisites and production qualification remain separate.

## Isolated cluster initialization and serving proof

Exercise initial development search activation on real isolated PostgreSQL and
the supplied HTTPS Elasticsearch version. Require strict mapping, external
version protection, refresh-visible exact totals/counts, native CEL equivalence,
tenant isolation, PIT pagination, tombstone replay and atomic alias checks.
Verify worker-role SQL permissions, fresh activation, matching repeated execution,
crashes after reservation/index creation, cleanup uncertainty, target/config/epoch
conflicts, populated authority, active writers, stale clocks and restore fences.
Failures must not open the initial gate; retries must not adopt unrelated data.

Exercise the private operator helper's actual caller/response contract with
selected active/prepared keys and credential-ID-only old/revoked policy proof.
Require fresh nonce, all exact serving members, policy digest/generation, tenant,
expiry, current operation/lease/binding and before/after checks. Reject wrong
secrets, unknown/duplicate/missing nodes, redirects, malformed/oversized replies,
partial timeouts and concurrent invalidation. Verify no alert is admitted and no
credential is reflected in errors/logs. Execute real Kong/Grafana lifecycle checks
against the eventual supplied binding before claiming that integration qualified.
Verify OpenShift restricted execution, private routing, direct member TLS/DNS,
startup order and replacement/requalification. Record local and target-cluster
evidence separately.
