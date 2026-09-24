# Reliability and operations

Application service objectives, capacity, backpressure, failure handling and recovery. These are selected objectives; measured results and supplied service guarantees belong in [Delivery readiness](./delivery-readiness.md).

## 1. Preserved requirements and ownership

Preserve the user-selected sustained requirement of 15,000 deliveries/minute (250/second), including concentration in one tenant or Global. Normal traffic is about 4,000/minute; peak duration is unknown. Preserve p99 normal-operation targets of one second for durable ingestion acceptance, five seconds for incoming alert/status UI visibility and five seconds for maintenance-expiry UI visibility. Preserve PostgreSQL admission commit before acknowledgement, original event/effective times, tenant ordering, occurrence semantics and protection of admitted work.

Appchi owns application objectives/instrumentation, processing correctness, tenant isolation, retries, idempotency, degraded-state UX, logical lifecycle rules, application backpressure and safe post-restore checks. Each technology team owns its service's operation, infrastructure retention, backups, HA, failover, maintenance, capacity and recovery. Appchi supplies workload and safety requirements; both sides agree supported integration settings, allocations and recovery handoff.

Record the application operational contact and each dependency team's support route before rollout. Automatic operator-specific Kong/Grafana provisioning remains application integration behavior; running those technologies belongs to their teams. No individual names or supplied service guarantees are assumed.

## 2. Availability and measurement window

Use a rolling 30-day UTC window, evaluated every minute, with daily summaries. Select **99.9% request-based availability separately** for native v1 ingestion, native v2 ingestion, the Grafana adapter, authoritative Product API reads, Product API commands, and search/count queries. Do not combine a failing path with a busier healthy path. A batch is one request for availability; item outcomes are also reported separately.

Numerator: eligible requests that receive a correct successful service outcome. Denominator: all eligible attempts observed at the public boundary, including service failures. The budget is 0.1% of eligible requests, not a downtime allowance. Planned maintenance and deployments count. Zero eligible requests means no data, not 100% availability. This is an application design objective, not an asserted SLA from the technology teams. Confirm offered service guarantees and maintenance behavior before claiming end-to-end compliance; dependency-caused failures remain visible in the application metric. External probes supplement request accounting; an edge outage that prevents observations is reported as an outage and coverage gap, never invented successful requests.

## 3. Eligibility and failure accounting

Include valid traffic and failures caused by infrastructure, capacity, timeouts, lost connections after full receipt, and unavailable authentication dependencies. Capacity-related 429/503 responses count as failures. Exclude proven malformed/oversized input, invalid or revoked credentials, expected permission/business-conflict rejections, health probes and identified load tests from production request SLIs; report those outcomes separately. An incorrect 4xx response to valid work is a service failure. Unknown eligibility during a dependency failure is counted as bad unless evidence establishes a genuine client error.

A partial batch is successful only when all admissible items are durably admitted and rejected items have correct outcomes. Later legitimate semantic processing rejection does not retroactively change the durable-receipt contract. External retries count as request attempts; idempotent duplicates do not become new source events. Report fresh and duplicate-request cohorts separately. Gateways must not automatically replay mutating POST requests.

## 4. The three agreed latency objectives

Measure each separately as the fraction meeting its threshold over the rolling 30-day window; the required fraction is at least 99%:

| Objective | Start | Successful end | Threshold |
|---|---|---|---|
| Durable acceptance | Complete request body at public ingress | Acceptance response sent after PostgreSQL admission commit | 1 second |
| Incoming alert/status visibility | Original system receipt timestamp | Correct state rendered in an eligible connected foreground view | 5 seconds |
| Maintenance expiry visibility | Stored scheduled end | Expired maintenance and resulting suppression/count state rendered in an eligible view | 5 seconds |

Include authentication, validation, queueing, processing, projection and rendering wherever they fall between the relevant boundaries. Enqueueing or sending a live hint is not completion. An error, timeout or still-incomplete observation past its deadline is a miss. A later correct state can satisfy an earlier observation without flashing every intermediate transient state.

Retain the previously agreed normal-operation scope: separately identify dependency outages, declared recovery/load-test periods and already offline/backgrounded clients. Do not declare a period abnormal merely because latency missed. Publish all-traffic outcomes alongside this normal-operation cohort; outages continue to consume availability budgets. Filters and current permissions determine which views are eligible. Never reset the timing start on retries or worker recovery.

## 5. Additional latency objectives

Select p99 at two seconds for normal feed/list/search/count requests; one second for ordinary authoritative detail reads and local user commands; and two seconds from canonical change commit to completion of the resulting correlation evaluation/arbitration pass. Use the same rolling window and explicit normal-operation accounting. Local commands that launch external work return a durable job acceptance; these targets do not promise completion of Grafana or Kong operations.

Correlation pass completion includes a deterministic exclusion or a recorded blocked outcome. Blocked-rule health and absent required actions remain separately visible; a quick failure is not successful correlation. End-to-end targets are measured directly: adding component p99 values does not prove an end-to-end p99.

## 6. Qualification workload

Preserve provisional representative/stress cases of 50/100 enabled correlation rules, 20 active maintenance windows, 50/100 connected clients and 5,000/10,000 unresolved alerts in the busiest tenant. Exercise new-alert/update mixes of 50/50, 20/80 and 80/20, all-v1 in Global, all-v2 in one tenant and distributed traffic. These counts are qualification scenarios, not product caps or proven capacity. Vary rule complexity, grouping cardinality and attachment size within existing contracts.

Use provisional 1, 4 and 16 KiB payload profiles and the largest valid member within the existing 64 KiB limit. Test singles and batches of 10, 50 and 100 within the existing 4 MiB envelope. Start with one view per client; separately test three tabs per user and ten count panels per dashboard. Retain actual new-row/history growth throughout tests. The primary profile must meet the targets at both normal and sustained peak input. A larger profile may be called qualified only after it passes, rather than implying every possible workload is supported.

Define the primary profile as 50 correlation rules, 20 maintenance windows, 50 clients, an initial 5,000 unresolved rows, 4 KiB source members and a 50/50 new-row/update mix, exercised both as single requests and ten-member batches. Include valid resolutions in the updates to keep the primary unresolved population near its starting level while retained resolved rows/history accumulate. The 80/20 new-heavy profile deliberately permits unresolved population growth; 5,000/10,000 are starting populations, not an instruction to delete or suppress newly created rows. Other scenarios vary these inputs separately and in the combined stress case, with their achieved envelope reported explicitly.

## 7. UI measurement and low-volume treatment

Use complete backend outcome counters, deterministic 10% sampling of real incoming-event/view observations, 100% of maintenance-expiry observations and 100% UI observation in qualification tests. Report sampling coverage, missing acknowledgements and exclusions. UI percentiles estimated from samples must be labelled as estimates. A rendered projection/version acknowledgement establishes visible state; a hint alone does not. Server receipt of that acknowledgement supplies a conservative completion bound without trusting the browser clock.

Missing or late eligible acknowledgements cannot count as successes. With fewer than 100 eligible observations, show raw outcomes and insufficient-confidence status rather than a confident percentile claim. Tenant reports remain permission-scoped. The live transport and observation protocol is defined in [Alerts and history technical design](./spec-alert-history-technical.md).

## 8. Request timeouts and retries

Set ingestion handler timeout to five seconds after full body receipt, with a ten-second gateway timeout. The one-second p99 remains the performance objective, not a forced commit deadline. Cancel safely before commit where possible; an uncertain commit follows the existing idempotency/retry contract and must not be reported as a proven rollback.

Ordinary Product API and search requests have a ten-second handler timeout and fifteen-second gateway timeout. Technical supplement 18–20 selects SSE heartbeat, bounded buffering and stream/proxy timeout requirements; deployed compatibility remains to be confirmed. Bound database waits by the remaining request budget. HTTP timeout does not truncate an already admitted atomic background attachment or other mandatory operation. Use the selected 429/503 retry contracts below. Gateway timeouts are requested integration settings for the gateway team to confirm and apply; Appchi owns its handler deadlines and does not independently reconfigure the shared gateway.

## 9. Recovery capacity and overload tests

Require demonstrated processing recovery capacity of **500 deliveries/second** for a concentrated tenant while 250/second continue arriving. Net drain of 250/second clears a two-hour, 1.8-million-item backlog in two hours after dependencies are healthy. This is a qualification requirement, not measured capacity.

Test an overload burst of 1,000 deliveries/second for sixty seconds. This is not a new guaranteed admission rate: durably accept only within available capacity, explicitly reject the rest, and process everything accepted. Display recovery lag without claiming five-second visibility for old queued events. Preserve the existing blocked-head and trusted-repair rules; recovery never skips an unproven predecessor.

## 10. Application backlog limits and admission control

The application capacity requirement is two hours of full single-tenant input. Select pending-item limits of 1.8 million per tenant and 2.25 million globally. Agree sufficient allocation with the owning teams and derive application byte budgets from measured costs before launch. These are application admission limits, not Kafka retention or physical storage policy. For scale, 1.8 million 64 KiB members alone occupy about 110 GiB before overhead; the owning teams size infrastructure from the supplied workload.

Reserve capacity atomically for the admissible subset of a batch using [shared backlog accounting](./spec-system-completion.md#backlog-accounting). If that whole subset cannot fit, reject the admission operation for retry rather than partially admitting otherwise-valid items merely to fit capacity. Warn at 70% of an application queue budget, escalate at 85%, and stop admission at the count/byte cap or when the service reports insufficient safe capacity. Resume below 75% of the relevant application budgets once the dependency permits safe admission. The storage team supplies its capacity/health contract and owns infrastructure disk thresholds.

Use 429 with Retry-After: 10 seconds for capacity rejection and 503 with Retry-After: 5 seconds for unavailable authority/durability. Never delete accepted items to free room. Keep feasible read/status/repair paths available. Record and resolve any mismatch between supplied allocation and the application buffering requirement before qualification.

## 11. Fairness and rule budgets

Use fair scheduling across ready tenants, yielding between atomic work units after 100 events or 100 milliseconds, whichever is reached first. Finish an in-progress atomic unit before yielding; do not truncate complete incident attachment or skip tenant order. Admission caps also prevent one tenant from consuming the whole global pending budget.

Preserve the correlation supplement's finite platform budgets for enabled rules, groups, evidence and evaluation. Derive and version their numerical limits from measured engine costs before enabling automatic correlation in production. The 50/100-rule test scenarios are not those limits. Missing qualified budget configuration prevents automatic-correlation readiness and produces visible degraded health; it does not silently discard evidence or invalidate otherwise admissible v1 delivery. Technical supplement 5 selects deterministic cost accounting and static syntax bounds; numerical deployment budget values remain measured qualification outputs. Measured limits are a required delivery artifact, not fabricated benchmark results.

## 12. Dependency failure behavior

| Unavailable dependency | Behavior |
|---|---|
| PostgreSQL or its agreed durable-commit capability | Return 503; never acknowledge uncommitted admission. Obtain the offered durability/failover contract instead of assuming a replication mode. |
| Kong or trusted v2 authentication | Reject affected v2 requests; no anonymous fallback. Preserve the separate unauthenticated v1 path when its own dependencies work. |
| Kafka | Continue PostgreSQL durable admission within backlog limits; retain pending work and repair missed wakeups in order. |
| Elasticsearch | Continue authoritative processing. PostgreSQL details/commands remain available; feeds/counts show stale or unavailable status, never fabricated zero counts. |
| Redis/live delivery | Continue authoritative work; expose stale/disconnected view state. Technical supplement 18–21 selects durable generation reconciliation, SSE reconnect and foreground fallback polling. |
| Grafana | Preserve existing pending operator jobs and rename/delete gates. Established independent senders continue where valid. |
| Identity provider/LDAP access | Preserve five-minute normal-operation LDAP membership/disablement enforcement, including active sessions. During refresh outages use last-known trusted identity evidence for normal authorization without an age-only cutoff, alongside valid sessions, current Appchi grants and known revocations. Identity supplement 1–14 completes the delegated session, checkpoint, synchronization, logout and recovery configuration. Ordinary restarts preserve the accepted checkpoint; rollback/disaster restore gates human authorization on fresh identity and permission reconciliation. The user's team owns Keycloak; other service ownership remains unchanged. Deployment and end-to-end qualification are unperformed. |
| Dependency backup/recovery protection | The owning team detects and handles backup failures. Appchi consumes any supplied degraded-protection signal and coordinates impact; otherwise valid durable admission need not stop solely because a backup failed. |

Failures consume the relevant service budgets. No outage automatically resolves alerts, clears suppression, changes tenant ownership or rewrites source times.

## 13. Managed-service availability and HA boundary

Dedicated technology teams choose and operate PostgreSQL replication/failover, Kafka broker/topic durability, Elasticsearch redundancy and other service HA.

Obtain documented durable-write/acknowledgement semantics, failure/reconnect behavior, supported client settings, maintenance expectations and endpoints. Appchi client configuration must match that contract; uncertain writes retain the existing idempotency/receipt rules.

The application supports restart-safe workers, durable coordination, readiness and graceful draining without relying on one process's memory for correctness. Arrange application replica/runtime placement and scaling through the deployment team's supported platform model and measured requirements. Do not prescribe cluster topology or claim unconfirmed failure guarantees.

## 14. Transport retention and application search rebuilds

The Kafka team owns topic retention and broker/topic operational policy. Record the supplied retention, replay/offset behavior and client/topic capabilities. PostgreSQL pending work/outbox records are application state: do not purge them merely because Kafka acknowledges publication or retention expires. Cleanup respects required consumer completion/checkpoints and replay/proof protection. Verify gap recovery from authoritative state within the offered service contract.

Treat Redis as disposable application transport/cache state. The Elasticsearch team owns the service, physical lifecycle and capacity. Appchi owns projection semantics and reconstruction: snapshot plus ordered catch-up, no source lifecycle replay, validation of tenant scope/versions/counts before complete-index switching. Coordinate index creation, switching and cleanup with the team's supported interfaces and policies. [Alerts/history technical completion](./spec-alert-history-technical.md), decisions 12–17/25–26, selects relay/consumer/offset, projection and rebuild mechanics; supplied-service compatibility and implementation remain D2 delivery work.

## 15. Scheduler cadence and clock protection

Select a one-second due scan for maintenance transitions and recovery of missed pipeline wakeups. Use durable job claims with ten-second leases, renewed every three seconds, and generation/ownership fences checked at commit. Recheck the current maintenance revision and end under the selected tenant coordination boundary so extensions cannot expire early. Maintenance completion 4–11 now selects detailed proof/state ordering.

Preserve hourly alert/incident inactivity sweeps and the existing operator thirty-second job sweep/five-minute reconciliation. Startup recovery finds overdue work while preserving original effective times and checking current eligibility. Use clock-health observations to warn Appchi above 100 milliseconds and escalate above one second through the owning team; host/database clock synchronization and repair belong to that team. A confirmed backward/untrusted authoritative clock fences timestamp-dependent admission and automatic/control transitions until trusted time catches up; do not rewrite historical times to recover.

## 16. Dependency recovery guarantees and application recovery

Obtain each team's documented recovery-point objective (possible data loss), recovery-time objective, durability/failure guarantees, recovery scope and restore procedure. No numerical infrastructure RPO/RTO is assumed. Record supplied guarantees and qualify the application against them before release.

Appchi retains protection of admitted work against application crashes/retries and the requirement to drain an intact two-hour backlog within two hours while 250/second arrive, once dependencies are healthy and qualified capacity is supplied. It cannot recreate authoritative data missing from a restored recovery point. Record offered data-loss behavior and consequences explicitly; do not silently permit loss or pretend it was recovered.

Operating teams restore their services; Appchi checks credentials, deletion fences, tenant order, pending work and projections before reopening affected paths. Measure search reconstruction against supplied capacity and retained data. End-to-end restoration includes both stages, and outages/maintenance remain visible in application availability.

## 17. Backup ownership and recovery handoff

Dedicated technology teams own backup methods, frequency, retention, encryption/key custody, locations, monitoring, restore execution and infrastructure recovery exercises. Record actual team policies without inventing Appchi defaults.

Appchi supplies authoritative-data inventory, product lifecycle/deletion requirements, schema/version compatibility, credential/deletion safety constraints and post-restore verification. Agree how independently current recovery evidence is protected and provided. The owning teams supply recoverability evidence and limitations; Appchi verifies application correctness during coordinated exercises. No teams have been contacted or service guarantees assumed.

## 18. Application restore fencing and deletion safety

After service restoration, keep affected application paths fenced until current deployment authority, tenant order, clocks, pending-work identities and independent credential/deletion evidence are verified. Infrastructure teams protect and recover that evidence through an agreed interface; Appchi supplies and consumes the logical IDs and versions.

Before physical application-content deletion, require confirmation that its minimal identity/version purge fence is protected under the agreed recovery contract. Otherwise delay physical purge while retaining logical inaccessibility. Keep minimal fences until a safe replay horizon is proved using actual service retention/restore policies and application consumer progress.

Preserve operator supplement decision 28: invalidate unprovable credentials; keep unknown/deleted identities fenced; re-provision only independently verified surviving operators. Never revive revoked/expired keys. Apply current product retention before exposing restored content. Missing order/proof requires trusted repair or an explicitly permitted reset; a successful database restore alone does not establish application readiness.

## 19. Capacity input to the operating teams

Appchi measures per-delivery growth, new/update ratios, retained history, backlog, query pressure and processing demand and supplies these to the teams. Sustained all day, normal input is 5.76 million deliveries/day and peak input is 21.6 million/day, not distinct alert counts.

Owning teams decide physical sizing, replicas, headroom, expansion, forecasts and infrastructure alert thresholds. Agree allocated capacity and observable exhaustion behavior for safe application backpressure. Retain generated test data to expose growth. Agreed product-visible alert/history lifetimes remain requirements; reconcile infrastructure policies rather than silently deleting required application records earlier.

## 20. Application observability and telemetry ownership

Appchi emits outcomes/latency, application queue depth/age/budget use, blocked processing/proof, correlation health, scheduler/projection lag and UI acknowledgement coverage through supported company observability interfaces. Use Prometheus-compatible metrics where provided. Dedicated teams monitor their services and expose agreed health/incident signals.

Observability/technology teams own telemetry storage/retention and infrastructure audit policy. Obtain sufficient measurements or supported aggregates for rolling 30-day application SLIs; record any compatibility gap. Retain 1% successful application trace sampling with bounded error coverage within the collector team's limits.

Appchi redacts secrets/alert bodies from diagnostics, avoids high-cardinality source values as metric labels and scopes tenant-visible health. Already selected product alert/incident/operator history and audit lifetimes remain product contracts, distinct from infrastructure logs. Send application recovery/privileged-action audit events to the agreed destination; its infrastructure retention is not prescribed here.

## 21. Operational alerting

For each SLO separately, compute burn rate as observed bad fraction divided by its allowed fraction: 0.001 for availability, 0.01 for the p99 latency threshold. Require both windows to breach: 14.4 times budget burn over one hour and five minutes, or six times over six hours and thirty minutes, triggers urgent response; one times over three days and six hours creates a non-urgent work item. This follows the [Google SRE multiwindow burn-rate approach](https://sre.google/workbook/alerting-on-slos/).

Ratio-based paging requires at least 100 observations in the long window and twenty in the short one. Independently probe every ten seconds; three consecutive failures trigger outage handling even at low volume. Accepted-data loss, tenant isolation failure, unsafe primary state and unprovable credential restoration require immediate escalation. Escalate an unrecoverable tenant head/proof gap after one minute; warn when maintenance execution lag exceeds five seconds and page above thirty seconds. Preserve existing operator fifteen-minute persistent-failure signals.

Route Appchi symptoms to application support and underlying-service incidents to their owning teams through existing independent company on-call mechanisms. Appchi is not its own sole outage notifier. Deduplicate and clear application signals on verified recovery; the owning teams set and operate their infrastructure monitors. This design does not send messages, create external alerts or schedule automations.

## 22. Error-budget policy

Correctness, tenant isolation and accepted-work safety are never permitted failures merely because a budget remains. With more than 50% of the relevant budget remaining, use normal change controls. At 25–50%, require owner review of risky changes and pause production chaos exercises. Below 25%, defer nonessential high-risk changes and prioritize reliability. An exhausted budget freezes feature rollouts affecting the failing component; recovery, security and reliability fixes remain allowed. Resume after a documented repair, owner review and positive remaining budget.

Do not lower objectives retroactively or reset budgets after incidents. Record a material-breach follow-up within two working days. Review objectives monthly for the first three months after launch, then quarterly. These are engineering objectives, not a customer contractual SLA. The change policy applies to Appchi releases only; it does not authorize freezing another team's releases or overriding its change/incident process.

## 23. Qualification and fault tests

See [required reliability checks](./verification-plan.md#reliability).
