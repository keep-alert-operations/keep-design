# Reliability and operations

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

The 2026-09-30 [Kafka-first pipeline](spec-kafka-alert-pipeline.md) governs alert transport, gateway admission, UTC ordering, manual correlation, search reconciliation and cutover (REV-33). Unrelated product behavior remains unchanged.

Application service objectives, capacity, backpressure, failure handling and recovery. These are selected objectives; measured results and supplied service guarantees belong in [Delivery readiness](https://github.com/keep-alert-operations/keep-delivery/blob/main/status/delivery-readiness.md).

## 1. Preserved requirements and ownership

**Current scope (REV-34):** The five-second maintenance-expiry visibility target no longer applies because windows release no alerts on a timer; see [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler). Throughput, acceptance, incoming-visibility and ownership requirements below remain normative.

Preserve the user-selected sustained requirement of 15,000 deliveries/minute (250/second), including concentration in one tenant or Global. Normal traffic is about 4,000/minute; peak duration is unknown. Preserve p99 normal-operation targets of one second for durable ingestion acceptance, five seconds for incoming alert/status UI visibility and five seconds for maintenance-expiry UI visibility. Preserve broker acknowledgement before 202, original ingress/effective times, per-key source order, tenant changed order and occurrence semantics. Acknowledged unprocessed inputs remain subject to Kafka retention.

Keep owns application objectives/instrumentation, processing correctness, tenant isolation, retries, idempotency, degraded-state UX, logical lifecycle rules, application backpressure and safe post-restore checks. Each technology team owns its service's operation, infrastructure retention, backups, HA, failover, maintenance, capacity and recovery. Keep supplies workload and safety requirements; both sides agree supported integration settings, allocations and recovery handoff.

Record the application operational contact and each dependency team's support route before rollout. Automatic operator-specific Kong/Grafana provisioning remains application integration behavior; running those technologies belongs to their teams. No individual names or supplied service guarantees are assumed.

## 2. Availability and measurement window

Use a rolling 30-day UTC window, evaluated every minute, with daily summaries. Select **99.9% request-based availability separately** for native v1 ingestion, native v2 ingestion, the Grafana adapter, authoritative Product API reads, Product API commands, and search/count queries. Do not combine a failing path with a busier healthy path. A batch is one request for availability; item outcomes are also reported separately.

Numerator: eligible requests that receive a correct successful service outcome. Denominator: all eligible attempts observed at the public boundary, including service failures. The budget is 0.1% of eligible requests, not a downtime allowance. Planned maintenance and deployments count. Zero eligible requests means no data, not 100% availability. This is an application design objective, not an asserted SLA from the technology teams. Confirm offered service guarantees and maintenance behavior before claiming end-to-end compliance; dependency-caused failures remain visible in the application metric. External probes supplement request accounting; an edge outage that prevents observations is reported as an outage and coverage gap, never invented successful requests.

## 3. Eligibility and failure accounting

Include valid traffic and failures caused by infrastructure, capacity, timeouts, lost connections after full receipt, and unavailable authentication dependencies. Capacity-related 429/503 responses count as failures. Exclude proven malformed/oversized input, invalid or revoked credentials, expected permission/business-conflict rejections, health probes and identified load tests from production request SLIs; report those outcomes separately. An incorrect 4xx response to valid work is a service failure. Unknown eligibility during a dependency failure is counted as bad unless evidence establishes a genuine client error.

A partial batch is successful only when all admissible items are durably admitted and rejected items have correct outcomes. Later legitimate semantic processing rejection does not retroactively change the durable-receipt contract. External retries count as request attempts; client resubmissions are new deliveries; same-delivery internal retries do not apply twice. Report accepted, unconfirmed and rejected cohorts separately. Gateways must not automatically replay mutating POST requests.

## 4. The three agreed latency objectives

Measure each separately as the fraction meeting its threshold over the rolling 30-day window; the required fraction is at least 99%:

| Objective | Start | Successful end | Threshold |
|---|---|---|---|
| Durable acceptance | Complete request body at public ingress | Acceptance response sent after Kafka durable acknowledgement | 1 second |
| Incoming alert/status visibility | Original system receipt timestamp | Correct state rendered in an eligible connected foreground view | 5 seconds |
| Maintenance expiry visibility | Deferred under REV-34 | No timer-driven release in this scope | Nice-to-have |

Include authentication, validation, queueing, processing, projection and rendering wherever they fall between the relevant boundaries. Enqueueing or sending a live hint is not completion. An error, timeout or still-incomplete observation past its deadline is a miss. A later correct state can satisfy an earlier observation without flashing every intermediate transient state.

Retain the previously agreed normal-operation scope: separately identify dependency outages, declared recovery/load-test periods and already offline/backgrounded clients. Do not declare a period abnormal merely because latency missed. Publish all-traffic outcomes alongside this normal-operation cohort; outages continue to consume availability budgets. Filters and current permissions determine which views are eligible. Never reset the timing start on retries or worker recovery.

## 5. Additional latency objectives

Select p99 at two seconds for normal feed/list/search/count requests; one second for ordinary authoritative detail reads and local user commands; and two seconds from canonical change commit to completion of the resulting correlation evaluation/arbitration pass. Use the same rolling window and explicit normal-operation accounting. Synchronous operator commands use the separate budgets in worker scope; the one-second ordinary-command target does not cover their remote completion.

Correlation pass completion includes a deterministic exclusion or a recorded blocked outcome. Blocked-rule health and absent required actions remain separately visible; a quick failure is not successful correlation. End-to-end targets are measured directly: adding component p99 values does not prove an end-to-end p99.

## 6. Qualification workload

Preserve provisional representative/stress cases of 50/100 enabled correlation rules, 20 active maintenance windows, 50/100 connected clients and 5,000/10,000 unresolved alerts in the busiest tenant. Exercise new-alert/update mixes of 50/50, 20/80 and 80/20, all-v1 in Global, all-v2 in one tenant and distributed traffic. These counts are qualification scenarios, not product caps or proven capacity. Vary rule complexity, grouping cardinality and attachment size within existing contracts.

Use provisional 1, 4 and 16 KiB payload profiles and the largest valid member within the existing 64 KiB limit. Test singles and batches of 10, 50 and 100 within the existing 4 MiB envelope. Start with one view per client; separately test three tabs per user and ten count panels per dashboard. Retain actual new-row/history growth throughout tests. The primary profile must meet the targets at both normal and sustained peak input. A larger profile may be called qualified only after it passes, rather than implying every possible workload is supported.

Define the primary profile as 50 correlation rules, 20 maintenance windows, 50 clients, an initial 5,000 unresolved rows, 4 KiB source members and a 50/50 new-row/update mix, exercised both as single requests and ten-member batches. Include valid resolutions in the updates to keep the primary unresolved population near its starting level while retained resolved rows/history accumulate. The 80/20 new-heavy profile deliberately permits unresolved population growth; 5,000/10,000 are starting populations, not an instruction to delete or suppress newly created rows. Other scenarios vary these inputs separately and in the combined stress case, with their achieved envelope reported explicitly.

## 7. UI measurement and low-volume treatment

**Current scope (REV-34):** Maintenance-expiry observations are not required because no expiry-visibility objective applies; see [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler). Incoming-event sampling and acknowledgement rules below remain normative.

Use complete backend outcome counters, deterministic 10% sampling of real incoming-event/view observations, 100% of maintenance-expiry observations and 100% UI observation in qualification tests. Report sampling coverage, missing acknowledgements and exclusions. UI percentiles estimated from samples must be labelled as estimates. A rendered projection/version acknowledgement establishes visible state; a hint alone does not. Server receipt of that acknowledgement supplies a conservative completion bound without trusting the browser clock.

Missing or late eligible acknowledgements cannot count as successes. With fewer than 100 eligible observations, show raw outcomes and insufficient-confidence status rather than a confident percentile claim. Tenant reports remain permission-scoped. The live transport and observation protocol is defined in [Alerts and history technical design](spec-alert-history-technical.md).

## 8. Request timeouts and retries

Bound ingestion handling to five seconds, including body read, and retain the ten-second gateway timeout. Each Kafka attempt has a one-second broker delivery deadline and at most 1.1 seconds application wait; three attempts fit the handler budget. A timeout is an uncertain outcome, never proof of rollback. V2 context expires ten seconds after gateway authorization; deletion waits fifteen seconds after all-node denial before capturing its Kafka drain barrier. The one-second p99 remains an unqualified performance objective.

Ordinary Product API and search requests have a ten-second handler timeout and fifteen-second gateway timeout. Technical supplement 18–20 selects SSE heartbeat, bounded buffering and stream/proxy timeout requirements; deployed compatibility remains to be confirmed. Bound database waits by the remaining request budget. HTTP timeout does not truncate an already admitted atomic background attachment or other mandatory operation. Use the selected 429/503 retry contracts below. Gateway timeouts are requested integration settings for the gateway team to confirm and apply; Keep owns its handler deadlines and does not independently reconfigure the shared gateway.

The handler propagates an absolute request budget into database acquisition,
statement/lock waits and the pre-commit check. Cancellation alone cannot stop a
synchronous Python thread; a late local transaction must observe the expired
budget before committing. Operator mutations retain a 100-second handler budget
for their separately bounded remote provisioning contract. SSE setup is bounded;
each later reconciliation iteration receives its own bounded request budget.
Run synchronous database work outside the async event loop. Registry locks
protect in-memory state only, with per-tenant loading coordination across users.

The user's 2026-10-06 implementation check adds a combined diagnostic scenario of
5,000 deliveries/minute, 100 active users and 50 tenants. This does not supersede
the existing 250/second sustained and 500/second recovery qualification gates.
Record retained population, enabled features, payload size, replica/pool counts,
test duration, routing/identity fixtures, failures and measured latency boundaries.
A library-admission or synthetic-session workload cannot establish gateway, sign-in
or rendered-visibility qualification; those paths need their own real checks.

## 9. Recovery capacity and overload tests

Require demonstrated processing recovery capacity of **500 deliveries/second** for a concentrated tenant while 250/second continue arriving. Net drain of 250/second clears a two-hour, 1.8-million-item backlog in two hours after dependencies are healthy. This is a qualification requirement, not measured capacity.

Test an overload burst of 1,000 deliveries/second for sixty seconds. This is not a new guaranteed admission rate: accept only broker-confirmed publications within the request deadline and return explicit publication failures otherwise. Demonstrate processing of retained accepted inputs while separately reporting Kafka retention loss; no application backlog gate is introduced. Display recovery lag without claiming five-second visibility for old queued events. Preserve the existing blocked-head and trusted-repair rules; recovery never skips an unproven predecessor.

## 10. Application backlog limits and admission control

Do not reject ingress based on source/correlation/index lag or an application PG backlog allocation. Keep payload, authentication, request deadline and Kafka-service safeguards. A valid item receives 202 only after broker acknowledgement; three unconfirmed attempts return a retryable item failure. Monitor lag and low watermarks, and report retention risk honestly. Capacity/retention ownership remains with Kafka operators. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 2.

## 11. Fairness and rule budgets

Use fair scheduling across ready tenants, yielding between atomic work units after 100 events or 100 milliseconds, whichever is reached first. Finish an in-progress atomic unit before yielding; do not truncate complete incident attachment or skip tenant order. Kafka assignment/partition scheduling and bounded authority reconciliation replace the old per-tenant ingress capacity reservations; qualify concentrated-tenant fairness without a lag-based admission cap.

Preserve the correlation supplement's configurable platform budgets for enabled rules, groups, evidence and evaluation. Derive and version configured numerical limits from measured engine costs. The 50/100-rule test scenarios are not those limits. Under REV-39 correlation is always on and an unset budget is unlimited; an invalid configured value fails the operation with `capacity_profile_invalid` and visible degraded health, without silently discarding evidence or invalidating otherwise admissible v1 delivery. Technical supplement 5 selects deterministic cost accounting and static syntax bounds; numerical deployment budget values remain measured qualification outputs. Measured limits are a required delivery artifact, not fabricated benchmark results.

## 12. Dependency failure behavior

PostgreSQL failure blocks application processing and commands, but healthy Kafka ingress continues without a database connection. Kafka failure blocks new acknowledged admission and source transactional progress; manual PG commands can succeed with lost best-effort search hints. Search reconciliation continues during Kafka outages. Elasticsearch failure affects search/visibility while PG authority remains. Redis failures recover through existing PG/SSE reconciliation. Kong policy-store or trusted-context failure denies v2; v1 remains independent. Existing last-known trusted identity behavior remains unchanged.

## 13. Managed-service availability and HA boundary

Dedicated technology teams choose and operate PostgreSQL replication/failover, Kafka broker/topic durability, Elasticsearch redundancy and other service HA.

Obtain documented durable-write/acknowledgement semantics, failure/reconnect behavior, supported client settings, maintenance expectations and endpoints. Keep client configuration must match that contract; uncertain source publication retains one internal UUID across attempts; client resubmission is new. Product command idempotency remains unchanged.

The application supports restart-safe workers, durable coordination, readiness and graceful draining without relying on one process's memory for correctness. Arrange application replica/runtime placement and scaling through the deployment team's supported platform model and measured requirements. Do not prescribe cluster topology or claim unconfirmed failure guarantees.

## 14. Transport retention and application search rebuilds

Kafka may expire an acknowledged unprocessed receipt; the user explicitly accepted this narrowed guarantee. No zero-acknowledged-loss claim applies across an arbitrary Kafka outage/retention interval. Broker offsets below low watermark produce visible loss diagnostics and fenced source/correlation recovery. Search can reconstruct committed PostgreSQL state through the bounded scan and fenced rebuild in [Kafka-first pipeline](spec-kafka-alert-pipeline.md) sections 6 and 8. The Kafka team owns transport retention and recovery policies.

## 15. Scheduler cadence and clock protection

**Current scope (REV-34):** The maintenance due scan, inactivity sweeps and the operator job sweep and reconciliation are not deployed; see [worker scope](spec-worker-scope.md#5-nice-to-have-components). Clock-health thresholds and untrusted-clock fencing below remain normative.

Select a one-second due scan for maintenance transitions and recovery of missed pipeline wakeups. Use durable job claims with ten-second leases, renewed every three seconds, and generation/ownership fences checked at commit. Recheck the current maintenance revision and end under the selected tenant coordination boundary so extensions cannot expire early. Maintenance completion 4–11 now selects detailed proof/state ordering.

Preserve hourly alert/incident inactivity sweeps and the existing operator thirty-second job sweep/five-minute reconciliation. Startup recovery finds overdue work while preserving original effective times and checking current eligibility. Use clock-health observations to warn Keep above 100 milliseconds and escalate above one second through the owning team; host/database clock synchronization and repair belong to that team. A confirmed backward/untrusted authoritative clock fences timestamp-dependent admission and automatic/control transitions until trusted time catches up; do not rewrite historical times to recover.

## 16. Dependency recovery guarantees and application recovery

Validate supplied service guarantees without inventing infrastructure RPO/RTO. A PostgreSQL-committed source effect survives a failed Kafka transaction through immutable replay proof; this is not one distributed commit. Unprocessed Kafka retention loss is unrecoverable unless the producer independently resubmits, which is a new delivery. Restores must reconcile delivery/retirement fences, consumer offsets, rule boundaries and search epochs before reopening affected capabilities. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 8.

## 17. Backup ownership and recovery handoff

Dedicated technology teams own backup methods, frequency, retention, encryption/key custody, locations, monitoring, restore execution and infrastructure recovery exercises. Record actual team policies without inventing Keep defaults.

Keep supplies authoritative-data inventory, product lifecycle/deletion requirements, schema/version compatibility, credential/deletion safety constraints and post-restore verification. Agree how independently current recovery evidence is protected and provided. The owning teams supply recoverability evidence and limitations; Keep verifies application correctness during coordinated exercises. No teams have been contacted or service guarantees assumed.

## 18. Application restore fencing and deletion safety

After service restoration, keep affected application paths fenced until current deployment authority, tenant order, clocks, pending-work identities and independent credential/deletion evidence are verified. Infrastructure teams protect and recover that evidence through an agreed interface; Keep supplies and consumes the logical IDs and versions.

Before physical application-content deletion, require confirmation that its minimal identity/version purge fence is protected under the agreed recovery contract. Otherwise delay physical purge while retaining logical inaccessibility. Keep minimal fences until a safe replay horizon is proved using actual service retention/restore policies and application consumer progress.

Preserve operator supplement decision 28: invalidate unprovable credentials; keep unknown/deleted identities fenced; re-provision only independently verified surviving operators. Never revive revoked/expired keys. Apply current product retention before exposing restored content. Missing order/proof requires trusted repair or an explicitly permitted reset; a successful database restore alone does not establish application readiness.

## 19. Capacity input to the operating teams

Keep measures per-delivery growth, new/update ratios, retained history, backlog, query pressure and processing demand and supplies these to the teams. Sustained all day, normal input is 5.76 million deliveries/day and peak input is 21.6 million/day, not distinct alert counts.

Owning teams decide physical sizing, replicas, headroom, expansion, forecasts and infrastructure alert thresholds. Agree allocated capacity and observable exhaustion behavior for safe application backpressure. Retain generated test data to expose growth. Agreed product-visible alert/history lifetimes remain requirements; reconcile infrastructure policies rather than silently deleting required application records earlier.

## 20. Application observability and telemetry ownership

Keep emits outcomes/latency, Kafka partition lag/age/retention risk, non-alert job depth, blocked processing/proof, correlation health, scheduler/projection lag and UI acknowledgement coverage through supported company observability interfaces. Use Prometheus-compatible metrics where provided. Dedicated teams monitor their services and expose agreed health/incident signals.

Observability/technology teams own telemetry storage/retention and infrastructure audit policy. Obtain sufficient measurements or supported aggregates for rolling 30-day application SLIs; record any compatibility gap. Retain 1% successful application trace sampling with bounded error coverage within the collector team's limits.

Keep redacts secrets/alert bodies from diagnostics, avoids high-cardinality source values as metric labels and scopes tenant-visible health. Already selected product alert/incident/operator history and audit lifetimes remain product contracts, distinct from infrastructure logs. Send application recovery/privileged-action audit events to the agreed destination; its infrastructure retention is not prescribed here.

## 21. Operational alerting

**Current scope (REV-34):** Maintenance execution-lag alerts assume the deferred maintenance scheduler and do not apply; see [worker scope](spec-worker-scope.md#1-maintenance-without-a-scheduler). Burn-rate, probe, escalation and operator failure signals below remain normative.

For each SLO separately, compute burn rate as observed bad fraction divided by its allowed fraction: 0.001 for availability, 0.01 for the p99 latency threshold. Require both windows to breach: 14.4 times budget burn over one hour and five minutes, or six times over six hours and thirty minutes, triggers urgent response; one times over three days and six hours creates a non-urgent work item. This follows the [Google SRE multiwindow burn-rate approach](https://sre.google/workbook/alerting-on-slos/).

Ratio-based paging requires at least 100 observations in the long window and twenty in the short one. Independently probe every ten seconds; three consecutive failures trigger outage handling even at low volume. Accepted-data loss, tenant isolation failure, unsafe primary state and unprovable credential restoration require immediate escalation. Escalate an unrecoverable tenant head/proof gap after one minute; warn when maintenance execution lag exceeds five seconds and page above thirty seconds. Preserve existing operator fifteen-minute persistent-failure signals.

Route Keep symptoms to application support and underlying-service incidents to their owning teams through existing independent company on-call mechanisms. Keep is not its own sole outage notifier. Deduplicate and clear application signals on verified recovery; the owning teams set and operate their infrastructure monitors. This design does not send messages, create external alerts or schedule automations.

## 22. Error-budget policy

Correctness, tenant isolation and accepted-work safety are never permitted failures merely because a budget remains. With more than 50% of the relevant budget remaining, use normal change controls. At 25–50%, require owner review of risky changes and pause production chaos exercises. Below 25%, defer nonessential high-risk changes and prioritize reliability. An exhausted budget freezes feature rollouts affecting the failing component; recovery, security and reliability fixes remain allowed. Resume after a documented repair, owner review and positive remaining budget.

Do not lower objectives retroactively or reset budgets after incidents. Record a material-breach follow-up within two working days. Review objectives monthly for the first three months after launch, then quarterly. These are engineering objectives, not a customer contractual SLA. The change policy applies to Keep releases only; it does not authorize freezing another team's releases or overriding its change/incident process.

## 23. Qualification and fault tests

See [required reliability checks](../verification/verification-plan.md#reliability).
