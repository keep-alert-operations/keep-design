# Project guidance

## Project and phase

Keep is an internal multi-tenant alerts management system with CEL feeds/shared
presets, incidents/correlation, one-time maintenance and shared count dashboards.
The initial-release product and application technical design is complete as of
2026-09-22. Implementation is now authorized and in progress; production
qualification remains unperformed. See implementation-status.md for evidence.

The implementation request authorizes application code, scaffolding, dependency
installation, isolated local infrastructure and tests across the initial release.
Production deployment and changes to shared company services require separate
authorization. Preserve the design, ownership and consistency rules below.

## Read the design first

Read [System design](../specs/spec-alerts-management-system.md) before project work and
reread affected normative supplements before changing behavior:

- [Current worker scope](../specs/spec-worker-scope.md).
- [Alert operations](../specs/spec-alert-operations.md).
- [Alerts/history technical baseline](../specs/spec-alert-history-technical.md).
- [Kafka-first alert pipeline](../specs/spec-kafka-alert-pipeline.md).
- [Incident operations](../specs/spec-incident-operations.md).
- [Correlation rules](../specs/spec-correlation-rules.md).
- [Operator operations](../specs/spec-operator-operations.md).
- [Reliability and operations](../specs/spec-reliability-operations.md).
- [Identity configuration](../specs/spec-identity-configuration.md).
- [Tenant and access](../specs/spec-tenant-access.md).
- [Preset operations](../specs/spec-preset-operations.md).
- [Maintenance completion](../specs/spec-maintenance-operations.md).
- [Dashboard completion](../specs/spec-dashboard-operations.md).
- [Shared system completion](../specs/spec-system-completion.md).

The [grouped final decision list](design-decisions-2026-09-22.md) summarizes the
68 choices made under the final all-subject delegation. [Design register](design-register.md) preserves all 55 original issue identifiers.
[Delivery readiness](https://github.com/keep-alert-operations/keep-delivery/blob/main/status/delivery-readiness.md) tracks DEL-01–DEL-08; required test
scenarios live in [Verification plan](../verification/verification-plan.md).

## Decisions and gaps

- On 2026-09-22 the user delegated every remaining product and technical design
  decision and requested autonomous completion plus a report grouped by subject.
  This supersedes earlier subject-limited discretion and ask-next-question rules
  for that completion. The selected contracts are now recorded in the supplements.
- Preserve explicit user choices and later corrections. Distinguish user decisions,
  assistant-selected decisions, normative contracts and illustrative examples.
  Older examples do not expand accepted native inputs or override completed APIs.
- Label new autonomous design choices assistant-selected and report them. Record
  newly discovered gaps or contradictions in the existing register, preserving IDs.
  Do not silently reverse settled decisions or reopen intentionally excluded features.
- Keep requirements, diagrams, examples, supplements, register and decision list
  consistent. Detailed decisions belong in specifications, not this orientation file.
- Do not invent service versions/endpoints/allocations/guarantees, employee names,
  test results or production readiness. Actual facts and executed evidence belong
  to the delivery checklist. A design-closed issue is not implemented functionality.

## Technical and ownership boundaries

- Python/FastAPI backend; Next.js/TypeScript frontend; OpenShift deployment.
- PostgreSQL transactional authority; Elasticsearch current-alert search projection;
  Kafka alert pipeline; Redis Pub/Sub/SSE hints backed by PG reconciliation.
- Native v1 and v2 both remain accepted during migration. V1 is unauthenticated and
  routes to fixed Global. V2 uses Kong/operator keys and immutable owning-tenant routing.
- Company LDAP is authoritative for users/nested teams. The user's team owns and
  configures internal Keycloak. Automatic directory synchronization and its
  five-minute LDAP-change propagation target are nice-to-have under REV-35.
  Preserve explicit trusted publication and last-known trusted identity data.
  The user's 2026-09-23 local-development exception permits an isolated Keycloak
  realm with native custom users and groups, using immutable native UUIDs and
  the normal OIDC/directory-publication path; production LDAP remains unchanged.
  See identity configuration section 14 and docs/local-keycloak.md.
- Preserve fixed Global, no tenant delete/disable, existing role/admin continuity,
  365-day tenant/access audit, operator key/Grafana gates, alert/incident retention,
  no-backfill maintenance and shared preset/dashboard reference contracts.
- One shared company Grafana; exact routing label is `Keep - {operator name}` with
  literal string value `true`. Do not restore the superseded UUID label.
- Other underlying technologies belong to dedicated operating teams. They own
  infrastructure retention, backups, HA, topology, allocation and recovery operations.
  Keep defines application behavior and validates supplied service contracts;
  do not prescribe those teams' infrastructure policy.
- No product notifications, recurring maintenance, personal presets/dashboards,
  enriched historical import or full event-sourcing architecture in the initial release.

## Verification

For documentation work, verify cross-document consistency, local links, fences,
issue identifiers and decision numbering. Do not claim runtime tests were run.
For later authorized implementation, follow the verification plan, delivery-readiness
checklist and normative migration/recovery contracts. Keep provenance and delivery
status separate from runtime specifications; avoid duplicating authoritative contracts.
