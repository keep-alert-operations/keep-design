# Initial-release worker scope

**User corrections — 2026-09-30 (REV-34).** This supplement supersedes earlier
requirements to deploy automatic maintenance release, assignment cleanup,
inactivity/retention sweeps and operator provisioning workers. Their earlier
algorithms remain design references for optional future work, not release gates.
Kafka admission, source processing, correlation, indexing, authentication,
authorization and explicit user commands retain their existing safeguards.

## 1. Maintenance without a scheduler

**User decision:** keep a suppressed alert suppressed after its maintenance window
ends; its next source update may clear that suppression. A source repeat counts
as an update for this purpose. No timer, read, indexer scan, note edit or unrelated
correlation decision clears suppression just because time passed.

**Assistant-selected details:** disable/delete likewise stops new coverage without
sweeping existing alerts. The next source input received at or after the coverage
end/control boundary closes that cause at that input's receive time. A delayed
input received inside coverage remains covered even if applied after expiry.
Before/after matching transitions during coverage retain their existing behavior,
including permitted manual field changes. Other maintenance causes and the v2
source-suspension cause remain independent. Ending a window never resolves alerts.
An actual source-driven final release may supply correlation eligibility through
the existing Kafka source event; time passing creates no synthetic qualifier.

Read, search, counts and affected-alert lists use persisted suppression/cause
state. The window can correctly show Ended while some alerts remain suppressed.
There is no pending fan-out or expiry-visibility SLO to imply future automatic
release. Controls keep immutable coverage proof and no-backfill semantics.

**Later user decision — 2026-10-28 (REV-49):** a timed alert dismissal is a
separate cause evaluated against the clock at read time, so it ends at its end time
without a scheduler; see [alert operations 29](spec-alert-operations.md#29-timed-dismissal-rev-49).
Maintenance causes keep the source-update release above.

**Assistant-selected migration:** 0046 records an immutable database UTC cutover.
Coverage boundaries preceding it retain the old reduction rules, preserving old
history/qualifiers; subsequent boundaries require source-driven release. Existing
jobs become obsolete without deleting their evidence. Stop old schedulers before
the migration; old binaries must not run alongside this release. No alert is
resurrected, purged, resolved or reassigned by this migration.

## 2. Assignment and data lifetime automation

**User decisions:** automatic assignment cleanup, inactivity resolution and
retention workers are nice-to-have components and are not deployed now.

Assignments do not confer access. Current authorization and eligibility checks
remain mandatory. **Assistant-selected presentation:** preserve existing masking
of known-ineligible stored assignees; do not invent an unavailable-person UI or
clear the database assignment automatically. Ordinary explicit reassignment and
new-occurrence behavior continue normally.

No sweep automatically resolves a 30-day-inactive alert/incident or retires a
resource at its 90-day resolution deadline. Stored activity/deadline fields are
retained for compatibility and future automation. **Assistant-selected boundary:**
deferring storage cleanup does not extend existing audit/configuration-history and
command-result access windows. Those read-time access rules remain; storage can
grow while physical removal is deferred. Previously retired content stays hidden.
Explicit configuration deletion, protected recovery fences, replay deduplication,
correlation evidence expiry, browser/session/key expiry and backup policy are not
removed. Protected deletion/recovery helpers remain available for explicit deletes.

## 3. Request-owned operator provisioning

**User decision:** execute provisioning inside the backend and hold the HTTP request
until verified success or failure. Do not start an operator worker or a backend
background retry loop. Automatic retries, periodic drift repair and independent
scaling are nice-to-have.

The API commits the intended command/identities first, then performs remote work
outside SQL transactions. Keep durable operation progress, generation fences,
all-node Kong proof, Grafana verification and global routing serialization.
Removing the scheduler does not make the cross-service operation atomic.

**Assistant-selected request contract:** creation returns 201 only after verified
completion; other provisioning mutations return 200 only after completion.
Copy and ordinary validation/authorization retain their current contracts. A
failed/incomplete remote operation returns 503 (or an applicable 409), with
operator/operation IDs, `outcome_may_be_partial: true` and an explicit retry path.
No successful 202 means provisioning continues in the background. Failure does
not claim rollback: keep names, credentials, admission fences and partial progress
until verified completion/cancellation. Revocation erases local ciphertext first
and reports success only after verified remote denial.

**Later user decision — 2026-11-15 (REV-73):** save on pick may answer 202
`{status: "pending"}` when a picked group is too large to save inside the request
([tenant access 5](spec-tenant-access.md#5-directory-selection-and-visibility)).
This is a deliberate exception to the no-202 rule above, limited to that route and
serviced by the request-started background save in section 4. Operator
provisioning keeps the no-202 rule.

Retry the recorded operation using its retry endpoint and current revision.
Replaying the original command inspects its original operation and returns current
verified completion or failure, never a second operator/key. Operation reads remain
available for troubleshooting. A restart or disconnected caller leaves recoverable
progress; it does not schedule autonomous continuation. A superseded generation
cannot commit completion. The existing 15-second denial barrier and Kafka deletion
drain remain mandatory; an uncompleted drain yields an explicit request failure.

**Assistant-selected budgets:** 90 seconds for request-owned work, starting no
30-second remote attempt with less than 35 seconds remaining; 100-second gateway
and development proxy allowance; 105-second browser timeout and backend shutdown
grace. These are requested settings, not measured latency guarantees. Ordinary
API/ingress deadlines remain unchanged. Qualify connection loss, slow dependencies,
concurrent callers and the complete proxy chain before deployment.

The Product API mounts the qualified operator binding and management credentials.
Use a separate `KEEP_OPERATOR_DATABASE_URL` with the existing provisioning-role
privileges, a shared one-connection pool per API process and the existing global
remote lease. Ordinary API SQL retains its RLS connection. Account for this extra
connection per replica in the supplied allocation; never mount these credentials
into ingress/frontend. Missing bindings fail the operation, not unrelated APIs.

Fixed retiring-key expiry continues to be enforced by Kong at the exact deadline.
**Assistant-selected disposal:** with the expiry sweep deferred, expired ciphertext
is erased on the next successful operator mutation using the existing expiry
recheck; no expired key can become valid or copyable while waiting. Immediate
revocation disposal and restore denial fences remain mandatory.

## 4. Directory synchronization is nice-to-have

**Later user decision — 2026-09-30 (REV-35):** remove the separately deployed
directory worker from the current release and list automatic identity refresh as
nice-to-have. This supersedes REV-34's unchanged directory-worker deployment and
the earlier requirement to qualify five-minute LDAP membership/disablement
propagation through automatic Keep polling. That propagation target is deferred
with the worker; the current release does not claim it.

**Later user decision — 2026-11-15 (REV-73):** Keep's password sign-in (one LDAP
bind) and the ADAPI directory replace the earlier identity provider.
Keycloak, OIDC and Keep's LDAP directory reader were removed by REV-73.
The group refresh remains
a manual command. Saves started by an administrator's pick may finish in the
background; for those saves only, this replaces the earlier rule that no autonomous
job services an API request for an unknown identity.

**Boundary:** preserve Keep-owned grants and the accepted PostgreSQL identity
checkpoint. Existing eligible users use the last trusted checkpoint without an age
cutoff. Current Keep grant edits, known revocations and session expiry still apply.
Sign-in reads only the person's own ADAPI row and publishes it when it changed; it
never reads groups, and sessions are not rechecked. Do not treat AD groups as Keep
permissions or quietly introduce a background poller or a scheduled refresh; a
scheduled refresh is a later change with its own REV.

Explicit, complete trusted publication supplies initial bootstrap, manual refresh,
sign-in of a new or changed person, save on pick and restore validation. Active
Directory, read through ADAPI, remains authoritative; the local directory
development exception ([identity 14](spec-identity-configuration.md#14-local-directory-development-exception))
remains separate. Grants accept only saved principals; without the required
published evidence they return the existing dependency failure. Initial bootstrap
and restore-integrity gates are not bypassed.

**Request-started background save (user decision Q9, REV-73).** When a picked group
cannot be saved inside the request, the Product API hands it to its background
saver ([tenant access 5](spec-tenant-access.md#5-directory-selection-and-visibility)).
Saves start only from an administrator's request; there is no schedule and no
poller, and the saver only runs jobs handed to it.

- Each job runs in a fresh context with no inherited request deadline, under its
  own 80-second request budget. The verifier deadline is the smaller of 60 seconds
  and the remaining budget minus 15 seconds; each ADAPI call takes the smaller of
  5 seconds and the remaining budget minus 1 second. A job therefore ends before
  its 120-second lease, so an expired lease means the owner is gone.
- When a job starts, it checks that it still owns the lease and extends
  `lease_until`; otherwise it drops the job. Reading ADAPI holds no database
  connection; the claim, the publish and the result update each take one briefly.
- Success publishes and deletes the pending row. Failure records `last_failure`
  (`directory_unavailable`, `directory_group_too_large`,
  `directory_verification_deadline`, or `directory_busy` after two fence
  rejections) and clears the lease. Every row update and delete filters on
  `lease_owner`. A catch-all turns any unexpected error, such as a lock or pool
  timeout, into `directory_unavailable`, logged without secrets.
- The verifier reports a structured reason (allocation exceeded, deadline,
  unavailable) so these failures can be told apart.

**Manual refresh.** The company CLI permits `directory --once` with qualified
bindings, but rejects continuous directory startup. It reads tracked roots through
ADAPI, including pending saves that have no `last_failure`; failed pending rows are
skipped, so one bad pick cannot break the refresh. Coverage is split: one evidence
for all user roots (looked up in batches) and one evidence per team root, each with
its own generation and 10,000-object cap, so one large or failing team cannot block
the rest. A publication rejected because a newer generation touched its roots
retries once with a new generation; a second rejection fails that root with
`directory_publication_incomplete`. The command lists every failed root and exits
non-zero if any failed. A successful publication deletes the pending rows it
covered. Each publication advances the directory revision, so a refresh fences
in-flight visibility proofs once per team. With `KEEP_DIRECTORY_BOOTSTRAP_QUALIFIED`,
the publication covering the global-super-admin group carries the bootstrap flag.

Local Start publishes once before starting API/UI. Local administrators use
`scripts/local-identity.ps1 -Action Refresh` after identity changes; this action
publishes once and does not start a worker.

## 5. Nice-to-have components

| Component | Future benefit / prerequisite |
|---|---|
| Maintenance scheduler and bounded release fan-out | Release without another source input; reinstate and qualify expiry visibility, overlap, control and correlation semantics. |
| Assignment cleanup | Persistently clear a still-current ineligible assignee with rechecks and audit. |
| Inactivity sweeps | Automatically resolve stale alerts/incidents under their distinct activity anchors. |
| Retention sweeps | Reclaim eligible content under dependency, replay, rebuild and protected-recovery proof. |
| Operator background orchestration | Automatic retry/restart recovery and periodic drift repair with independent scaling. |
| Directory worker | Automatic or scheduled trusted user/team refresh through ADAPI (the user wants a scheduled group refresh later, under its own REV); reinstate and qualify complete membership, disablement, five-minute propagation and last-trusted outage behavior. |

CLI startup rejects the deferred roles. Retained internal algorithms/tests are not
an environment flag to enable them silently. Reintroduction requires an explicit
scope decision and qualification. Core application components remain ingress,
processor, indexer, correlation, frontend and backend. Two kinds of background
work run inside the Product API: live publishing under REV-36 and request-started
directory saves under REV-73 (section 6). Explicit recovery/proof helpers remain.
This is not a claim of exactly six running processes or replicas.
The directory role is deferred by REV-35; explicit one-off publication remains.
See [implementation evidence](https://github.com/keep-alert-operations/keep-delivery/blob/main/docs/worker-scope-implementation.md).

## 6. Live updates inside the Product API

**User decision — 2026-09-30 (REV-36):** move live hint publishing into the Product
API. There is no separately deployed live worker. The API owns publishing, Redis
subscription, SSE delivery and PostgreSQL reconciliation for connected tenants.

**Assistant-selected implementation:** each Redis-configured Product API process
starts one background publisher using its existing bounded SQL pool. Blocking
SQL/Redis calls run outside the HTTP event loop. A turn reads at most 100 pending
tenant generations, starts no new publication after one second or shutdown, and
waits one second before the next turn. In-flight calls retain their bounded
SQL/Redis timeouts; Redis publishing has no internal automatic transport retries.
Stop the publisher and await its current turn before closing its SQL pool. Ingress
roles start neither live publisher nor subscriber.

Multiple API replicas may publish duplicate hints. Generation-conditional deletion
preserves an invalidation committed during publishing; failed publication leaves
pending work. No single-publisher lease is required because hints are idempotent
invalidations, not domain commands. Redis failure is logged without secret data
and does not make otherwise healthy Product API paths unready. Existing two-second
PostgreSQL reconciliation, tenant/session checks and scoped SSE messages remain.

Migration 0047 gives the API role cross-tenant SELECT/DELETE permission only on
the minimal live-hint outbox (tenant UUID, generation and update time). This is a
trusted server-side publishing privilege, not a browser endpoint. Tenant-scoped
outbox writes and domain RLS remain unchanged; no worker database credential or
additional pool is mounted into the API. Account for publishing SQL/Redis work in
the supplied API allocation. Apply the migration before the updated API starts,
stop old live workers and qualify the combined API workload before deployment.

**Later user decision — 2026-11-15 (REV-73):** the directory saver is the second
background component inside the Product API, next to the live publisher. It
services only saves handed over by save on pick (section 4); it is not a poller.

**Assistant-selected implementation:** each Product API process runs one saver
thread with a queue of 20 jobs and an in-process set of queued principals. It uses
the existing bounded SQL pool and holds at most one connection at a time, briefly,
for the lease claim, the publication and the result update; it holds none while
reading ADAPI. Account for this one connection per process, next to the live
publisher's share, in the supplied API allocation. Migration 0070 grants the API
role the directory writes a save needs: SELECT, UPDATE and DELETE on pending saves,
INSERT, UPDATE and DELETE on directory edges and root checkpoints, and USAGE on
the directory generation sequence. On shutdown, before the SQL pool closes, the
lifespan sets a stop event that the ADAPI reader checks between calls, releases
this process's leases and shuts the executor down with `wait=True` and
`cancel_futures=True`; the next poll restarts the job elsewhere. Ingress roles
start no saver.
