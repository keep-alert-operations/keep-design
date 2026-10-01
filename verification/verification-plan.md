# Verification plan

**REV-35 scope:** directory polling and its five-minute LDAP-change propagation cases are future qualification. Current identity acceptance must cover explicit complete bootstrap/refresh, unknown-user/team refusal without evidence, last-trusted authorization, immediate Appchi grant edits, known revocation/logout/session expiry and unchanged restore gates. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**REV-34 scope:** [Worker scope](spec-worker-scope.md) supersedes acceptance requirements for deferred schedulers. Existing timer/fan-out and automatic-cleanup scenarios are future qualification, not active release gates. Pre-cutover maintenance history still requires compatibility checks.

Required acceptance cases for the selected design. Record executions, environment/version, workload, results and defects during implementation. No tests are reported as executed here. Link failures to [Design register](./design-register.md) and release evidence to [Delivery readiness](./delivery-readiness.md).

## Alerts

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

Required tests cover both DST ambiguities and gaps, timezone-only edits, tzdata upgrades, disabled-at-start locking, create/edit at exact boundaries, late creation, repeats/retained matches, real false-to-true and true-to-false changes, manual refiring, first-seen resolved, two overlapping windows plus v2 source suspension, simultaneous ends, disable/re-enable, shorten/extend versus stale leases, deletion versus new causes, delayed input before/after controls, late history corrections, missing proof, crash after every transaction boundary, revision/no-op/retry behavior, tenant/role loss, retained deleted explanation, dependency holds and rollback restore. Verify exactly one effective unsuppression and no expired correlation evidence revival. Execute the selected sustained load and concentrated expiry scenarios before asserting latency.

## Dashboards

Hold a live count refresh while tenant search and the count batch report lag,
then release it and reconcile suppression/search completion. Panel positions,
retained counts and colors must stay steady on desktop, narrow and fullscreen
views; update labels stay readable without transient warning rows. Verify that
actual search failures still identify stale values and blocked source processing
still displays its error.

Test duplicate references, same-PIT/clock parity with equivalent feed queries, relative-time boundary, saved-query edits during requests, name reuse, preset-delete/save races, same-value retries, stale revision/draft preservation, exact zero versus failed/partial results, purge and maintenance generation races, index switch, access loss during paused/fullscreen/dirty views, responsive/keyboard layouts, threshold integer boundaries and deleted-history retention. Include counts/render observations in existing visibility measurements without storing sensitive query text in metrics. No additional dashboard-specific availability promise supersedes reliability objectives.

## Tenants and access

Qualify canonical-name collisions, reserved Global/name reuse, atomic creation, duplicate/reordered retries, expired receipts, stale revisions and concurrent last-admin removals. Cover self-demotion, empty/nested/cyclic groups, alternate membership paths, orphaned/recreated principals, unknown versus cached directory evidence and every matrix capability. Verify tenant switching, delayed responses, hidden-resource lookups, audit reader loss, secret redaction, LDAP baseline/diff events, no-op deduplication, 365-day boundaries/protected cleanup and permission-safe restore.

## Reliability

Run the primary 250/second concentrated-tenant workload for 24 hours, including retained data growth, and larger representative cases for four hours each. Repeat the primary path for v1 and v2 and characterize Grafana adapter overhead. Exercise the selected mixes, valid maximum sizes/batches, UI views and combined rules. Record a ten-minute startup period separately, without hiding subsequent growing backlog. Verify per-logical-key source append order and per-tenant changed order, headroom and all applicable latency objectives.

Appchi owns application load/correctness tests. Coordinate dependency fault injection and recovery in approved environments: owning teams perform infrastructure failover/restoration and Appchi verifies resulting application behavior. Also test the sixty-second overload burst; two-hour durable backlog and 500/second recovery; tenant fairness; post-commit disconnects; duplicate/reordered messages; leader loss and dependency outages; maintenance expiry racing edits/deletion; restored revoked credentials; deletion/replay protection; and full search rebuild. Require zero cross-tenant effects, duplicate internal effects or application-caused loss of retained acknowledged inputs or revoked-key activation. Assess infrastructure disaster-loss behavior against supplied service contracts rather than assuming a zero-loss capability. A profile is qualified only if its correctness and applicable objectives pass. Executed local checks are recorded separately in implementation status.

## Cross-system acceptance

The implementation must exercise each supplement's acceptance cases, with requirement IDs and failing evidence traceable to the preserved register. Add cross-subject scenarios: LDAP role loss during a dirty dashboard or key copy; permission edit versus command commit; scheduled maintenance expiry during source backlog and correlation reset; dashboard preset save/delete/count race; incident move/reopen versus source processing; operator deletion versus admitted batch; current source-suspended plus overlapping maintenance; all Global traffic; deleted-resource restoration; and old-worker/new-schema interoperation.

Run sustained 250 deliveries/s for 24 hours and selected four-hour stress variants, full one-tenant concentration, 500/s recovery with 250/s continued intake, the two-hour backlog and 1,000/s sixty-second overload case. Include longest permitted text/Unicode, growing parent history, 24 distinct dashboard panels, relative clock queries, largest qualified maintenance fan-out and atomic correlation attachment sets. Measure p99 one-second admission/authoritative commands, two-second searches/counts and five-second incoming/maintenance rendered visibility as already selected; do not infer one from the other. Availability evaluation retains its rolling 30-day definition and low-volume rules.

Inject process crashes at commit/ack boundaries and coordinate real dependency failures/restores with owning teams. Require zero cross-tenant effects, duplicate internal effects or application-caused loss of retained acknowledged inputs, expired-evidence revival or restored revoked-key activation. Verify secret redaction and no protected browser caches after access loss. Separate application correctness from the supplied infrastructure disaster-loss contract.

## Incidents

The implementation must demonstrate: manual creation without alerts; explicit immutable severity; atomic rollback of a conflicting multi-alert selection; linking a suppressed/resolved alert to an active incident; rejecting membership edits on a resolved incident; an atomic move without dual ownership; reopening conflicts leaving all state intact; lifecycle cycles preserving previous timestamps; repeated deliveries not refreshing inactivity; genuine linked-alert transitions using original accepted times; activity updates taking effect without waiting for the hourly check; an hourly check selecting only due active incidents without rereading activity history; concurrent activity defeating a stale expiry job; expiry preserving alert statuses while releasing ownership/resetting evidence; idempotent retries creating no duplicate history/activity; note revision/deletion affecting current search while preserving history; post-resolution edits not extending retention; and tenant isolation across search, conflicts, assignment and relationship references.

## Identity

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

Verify the [normative Kafka pipeline](spec-kafka-alert-pipeline.md) separately from legacy cutover compatibility tests:

- HTTP: no PG connection at ingress; immutable receive/default time and UUID across three attempts; concurrent partial batches; broker acknowledgement before202; failed Kafka503; no backlog gate; legacy IDs syntax-only; removed receipt lookup; five-second request and ten-second gateway deadlines.
- Source: partition append order despite reversed UTC, PG commit before Kafka failure, immutable replay after manual edit, transaction unknown outcome and fenced rebalance, duplicate UUID at another offset, mismatched UUID bytes, client resubmission and unchanged-repeat evidence, terminal semantic rejection, no offset advancement on transient failure.
- Correlation/maintenance: tenant changed order, manual resolve atomic evidence removal without incident unlink, ignored manual reopen/assignment/notes, delayed source after boundaries, exact release snapshot/origin provenance, all supporting source inputs consumed, inline release first discovered by manual edit, independent causes, equal-time control wins and clock-health faults.
- Search: lost manual/relationship/suppression/deletion hints, complete authority pass with captured lower bound, write behind cursor, newer version fencing, purge/tombstone, concurrent writes during rebuild and epoch cutover, scan progress during Kafka outage.
- Gateway: actual open-source Key Auth and installed policy plugin, prepared deny/current allow, revoked/expired deny, stale generation rejection, node-local identity and complete serving pool, exact digest/tenant/expiry proof, clock failure, erased plaintext cleanup, final rename/cancel phase, bounded authorization lifetime and deletion offset barrier.
- Migration: old work drained, new groups start at captured topic boundaries, active legacy writers refused, incompatible saved correlation CEL/grouping blocked by parsed field reference, edited rule starts fresh epoch, old event schema never consumed as new.
- Recovery: retained minimal delivery/key fences, outstanding publication/proof holds, missing protected replay baseline keeps restore closed, explicit Kafka low-watermark loss interval and reviewed reset. No client receipt service or zero-loss promise beyond supplied retention.

Production capacity, multi-node failover/rebalance, clock-discontinuity and rollback-survival runs remain required even when focused local tests pass. Actual results and remaining gaps belong in [implementation evidence](docs/kafka-first-implementation.md).

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
[worker scope](spec-worker-scope.md#6-live-updates-inside-the-product-api).
