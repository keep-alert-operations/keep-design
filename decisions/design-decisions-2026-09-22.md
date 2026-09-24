# Decision history — 2026-09-22

The user delegated completion of every remaining product and technical subject on 2026-09-22. **The 68 numbered decisions listed here are assistant-selected.** Their full contracts are in the linked specifications. Earlier user decisions remain unchanged; this list reports the additions from this final completion, not earlier sessions' decisions.

This is a provenance record, not an additional normative contract. Current specifications govern details. Later clarifications are recorded in the [design register](./design-register.md#documentation-review--2026-09-22); implementation and executed evidence are tracked in [Delivery readiness](./delivery-readiness.md#evidence-register).

## Maintenance — 20 decisions

Details: [Maintenance operations](./spec-maintenance-operations.md).

1. **Identity and content:** immutable tenant/UUID; duplicate names allowed, 1–200 characters; optional 10,000-character reason; separate intent, phase and health; start/CEL lock at scheduled start even while disabled.
2. **Schedule input:** explicit IANA timezone and second-precision local endpoints; explicit first/second choice at DST ambiguity; reject nonexistent times; retain UTC, original local/offset and tzdata evidence.
3. **Schedule changes:** explicit metadata/timezone/schedule edit modes; timezone-only edits preserve execution; tzdata changes show original/current rendering without rescheduling.
4. **Temporal controls:** immutable revision/segment history with database time and tenant order for every coverage change; extension preserves continuity and equal-time ordering is deterministic.
5. **Qualifying changes:** require trustworthy before/after proof; new matching resolved alerts may have coverage but no invented firing occurrence; no repeats, missing-state or configuration backfill.
6. **Overlapping causes:** independent maintenance-segment causes plus v2 source suspension; effective suppression is their union; retain individual and combined intervals.
7. **Delayed input:** reconstruct historical coverage from the configuration valid at admission; derive current state separately; durable checkpoints, unique effects and linked corrections prevent replay duplication.
8. **Correlation handoff:** state, history, proof and downstream work commit together; final unsuppression uses its actual effective time, with no duplicate creation qualifier or revival of expired evidence.
9. **Immediate controls:** disable/delete establishes the authoritative boundary immediately; bounded jobs update materialized alerts/search; current detail and correlation derive cause truth while views show updating.
10. **Scheduling:** one-second scan, fenced leases, revision/end checks, bounded 100-alert/100-ms fan-out and durable cursors; stale expiry cannot defeat an extension.
11. **Storage:** explicit window/revision/control/segment/cause/job tables, tenant foreign keys, indexes, child history partitions and consistent lock order.
12. **APIs:** create/update/enable/disable/delete/history/validate/test/timezone routes; revision/idempotency contracts, structured time errors and 256 KiB definition envelope.
13. **Screens:** current/upcoming default list, ended/deleted views, disambiguated duplicate names, affected-alert explanation list, explicit shared saves and copy-to-new form.
14. **Testing experience:** explicit validation and one-alert read-only test; clear no-backfill explanation; no historical simulation or automatic overlap scan.
15. **History:** complete configuration timeline while non-deleted; preserve the user's 90-day deleted-window history plus dependency extensions; command results 90 days.
16. **Cleanup:** no undelete; protected retirement and daily dependency-checked cleanup; pending work/history references prevent unsafe purge.
17. **Failures and limits:** unknown proof/CEL errors block unsafe work and preserve causes; measured overlapping-window reservations prevent oversubscription without dropping accepted inputs.
18. **Live visibility:** maintenance completion generations include fan-out and searchable progress; distinguish updating from current, and measure the full five-second rendered-visibility objective.
19. **Acceptance:** explicit DST, overlap, lifecycle, delayed-input, race, crash, retention, access and concentrated-expiry cases.
20. **Completion:** close M1–M5 product/technical design; keep supplied capabilities and measured results as delivery evidence.

## Dashboards — 18 decisions

Details: [Dashboard operations](./spec-dashboard-operations.md).

1. **Ownership and names:** shared tenant resources with immutable IDs, unique active names and existing view/edit/admin permissions; no private dashboards or resource-specific access lists.
2. **Definition:** zero through 24 panels; each references an active same-tenant preset's current saved query; repeated presets allowed; no saved personal controls.
3. **Titles:** preset name by default, optional 120-character custom title, always retain the preset link and exact accessible count.
4. **Layout:** saved 12-column desktop grid, defined panel sizes, validated nonoverlap, two/one-column responsive presentation and keyboard editing.
5. **Threshold colors:** neutral default, up to three increasing count thresholds with a fixed palette and text explanation; presentation only, without notifications or incident effects.
6. **Time and suppression:** no separate dashboard time picker or suppression switch; saved preset CEL supplies time restrictions; counts exclude suppression and impose no hidden status filter.
7. **Drill-through:** open current preset results with a fresh snapshot and explain that counts may have changed; no hidden historical query pinning.
8. **Editing:** explicit Save/Discard/Save as new, memory-only drafts, revision conflicts and new identities on copies; no autosave or overwrite merging.
9. **Viewing:** name-searchable list, live default, transient Pause/Refresh/fullscreen, normal session expiry and no kiosk/public access.
10. **Count consistency:** one PIT and captured clock for a batch, current revision/authority checks, repeated-query deduplication and exact totals.
11. **Failure states:** per-panel exact/unavailable/stale results with batch provenance; no false zero or claim that mixed stale/current panels are all current.
12. **Caching/load:** no persistent completed-count cache initially; compile caching, one in-flight browser request, coalesced updates and qualified fair concurrency limits.
13. **Storage/references:** explicit dashboard/panel/revision/history tables and shared preset-reference guard; concurrent saves/deletes cannot create dangling references.
14. **APIs:** list/detail/create/replace/delete/history/counts/preview/validate with selected permissions, envelopes, revisions and pagination.
15. **Deletion/history:** delete panels' live references without deleting presets; no undelete; 90-day revision/event/deleted-definition and command lifetimes with protected cleanup.
16. **Accessibility:** readable exact counts, keyboard/fullscreen controls, status beyond color, reduced motion and restrained screen-reader announcements.
17. **Acceptance:** query parity, clocks, preset edits/deletion, layout, partial failures, purge/maintenance/index races, role loss and retention tests.
18. **Completion:** close U3 and dashboard time/suppression/API/storage/history design; implementation and qualification remain delivery work.

## Application architecture and repository — 2 decisions

Details: [System completion 1–2](./spec-system-completion.md#1-application-framework-and-module-boundaries).

1. **Frameworks and boundaries:** FastAPI/Uvicorn, strict Pydantic models, Psycopg/explicit SQL, Next.js App Router/TypeScript and selected service clients; Python owns business/authentication authority; reuse PG durable work rather than introduce another queue.
2. **Repository and contracts:** monorepo with backend/frontend/contracts/migrations/deployment/qualification/docs; locked dependencies, generated API types, checked-in SQL migrations, immutable images and release manifests.

## General experience and API behavior — 8 decisions

Details: [System completion 3–10](./spec-system-completion.md#3-navigation-and-visual-system).

3. **Navigation/visuals:** tenant-scoped navigation and administration, last accessible tenant with Global fallback, compact responsive interface, English labels/Unicode content and WCAG 2.2 AA acceptance target. The original automatic light/dark choice is superseded by the user's 2026-09-24 visual direction recorded below.
4. **Interactions:** explicit configuration saves, concrete deletion/revocation confirmations, preserved conflict drafts, immediate protected-state clearing on access loss, and no offline/private/export/attachment additions.
5. **HTTP/JSON:** strict bodies and field types, safe decimal-string counters, common envelopes, resource-specific definition size limits and unchanged native ingestion contracts.
6. **Errors:** shared structured status/code/field/conflict/request-ID responses; no secret/inaccessible-object leakage; same-command reconciliation after uncertain mutation results.
7. **Commands/authorization:** stable command fingerprints, commit-time authorization guards, parent-specific result retention and minimal internal replay fences; external retry windows stay finite as previously selected.
8. **Reads/search:** preserve snapshot versus live-list distinctions; consistent incident detail reads; current-note/title/description token search using digest lookup plus full equality.
9. **Correlation UI/API:** exact CRUD/action/history/diagnostic/validation/test routes, reset explanations, current health and bounded single-alert tests; no new priority/threshold/backfill behavior.
10. **Incident APIs:** exact lifecycle/content/assignment/notes/link/unlink/move routes, aggregate revisions and bounded manual selections; no incident delete or severity mutation.

## Data, transactions and events — 8 decisions

Details: [System completion 11–18](./spec-system-completion.md#11-shared-postgresql-conventions).

11. **Database conventions:** typed relational state, scoped keys/foreign keys, minimal identity records, selected history partitions and non-owner tenant RLS roles.
12. **Identity/access storage:** explicit principal/binding/grant/checkpoint/edge/session/login/logout/guard/audit records, complete-generation publication and safe negative-evidence handling.
13. **Operator storage:** credential/state uniqueness, encrypted secret separation, durable desired/observed remote steps, global name claims and provisioning/recovery indexes.
14. **Preset/configuration storage:** validated current definitions, immutable revisions/activity, name claims, collection generations and atomic reference transactions.
15. **Incident storage:** current/cycle/note/link/claim/history/search records, minimal unavailable counterpart identities and source-to-incident activity locking.
16. **Correlation storage:** durable rule/condition/context/evidence/journal/boundary/cursor records; compare complete typed group bytes so digest collisions cannot merge contexts.
17. **Transaction order:** authorization guards before domain locks, explicit common lock hierarchy, short transactions, remote calls outside locks and whole-unit conflict retries.
18. **Other-resource events:** PG-transactional metadata invalidations and durable jobs, with Redis as hints; no Kafka topic per resource or secret-bearing live payload.

## Retention, deletion and recovery — 2 decisions

Details: [System completion 19–20](./spec-system-completion.md#19-unified-retention-and-configuration-history).

19. **Remaining lifetimes:** consolidate every category; final deleted correlation definitions retain 90 days, platform configuration/repair audit 365 days, maintenance keeps its complete non-deleted timeline, and infrastructure retention remains owner-managed.
20. **Cross-resource recovery:** protected intent/final fences before irreversible cleanup, bounded physical deletion, survivor-safe incident purge, independent recovery evidence, current permission/key/deletion reconciliation and fresh sessions after rollback restore.

## Security, runtime and service integration — 5 decisions

Details: [System completion 21–25](./spec-system-completion.md#21-application-security-and-secret-boundaries).

21. **Security:** same-origin HTTPS, strict trust/headers, escaped content, no arbitrary URL fetching, no protected shared cache, role-scoped versioned secrets and separate key purposes.
22. **OpenShift runtime:** separate workload roles, migration job, least-privilege containers, capability-specific readiness, bounded pools and safe draining/fenced retries.
23. **Capacity profile:** versioned measured combined budgets with an application safety margin and explicit enforcement; missing/unqualified limits gate affected capabilities instead of pretending capacity is known.
24. **Service handoff:** required version/endpoint/capability/allocation/ownership/recovery manifest; actual facts come from the service owners and incompatible capabilities gate release.
25. **Keycloak operations:** the user's team owns controlled realm/client changes, individually accountable administrators, MFA, staged upgrade tests and recovery validation without changing other teams' infrastructure policies.

## Verification, delivery and support — 5 decisions

Details: [System completion 26–30](./spec-system-completion.md#26-ci-and-release-artifacts).

26. **CI/release artifacts:** domain/migration/contract/integration/browser/security gates, actual CEL/ES differential tests, immutable images, schema/profile manifests and compatibility records.
27. **Acceptance:** cross-subject race/outage/restore/security cases and the existing sustained/recovery/visibility workloads; correctness requires zero isolation, replay or revoked-credential violations.
28. **Delivery/rollout:** six dependency-ordered milestones, environment separation, simultaneous native v1/v2, expand/migrate/contract, compatible canaries and rollback without database rewind.
29. **Support:** application/Keycloak accountability, service-owner escalation, defined containment/exit checks and audited, preconditioned repair tools rather than arbitrary product SQL access.
30. **Closure:** preserve all 55 original IDs as design-closed; separately require eight delivery evidence records for actual bindings, code, measured budgets, acceptance, recovery, identity/integrations, release/support and operational observation.

## Later user direction — 2026-09-24

The user requested username/password-only Appchi login and removal of the one-time
code. This supersedes the earlier assistant-selected TOTP requirement for Appchi
users, including global administrators. Separate Keycloak console MFA remains in
place. [Identity section 3](./spec-identity-configuration.md#3-username-and-password-authentication)
and REV-15 in the [design register](./design-register.md) record this correction;
the original 68-decision numbering is preserved.

Follow-up REV-16 records an assistant-selected recovery screen for expired or
already-used sign-in links after the user reported a raw callback error. The screen
starts a new sign-in only on an explicit click; expiry and replay rejection remain
unchanged. The original decision numbering is preserved.

The user's preset creation report supersedes REV-14's assistant-selected grouping
exception for default preset columns. REV-17 requires every configured column list
to render its fields individually and in order from creation onward, under the
existing [preset contract](./spec-preset-operations.md#4-columns-and-sorting).

The user's loading-text and layout-jump report is recorded as REV-18. The
assistant-selected correction keeps completed content and empty states visible
during refreshes of the same query, with initial loading and genuine failures
kept distinct under [shared system section 4](./spec-system-completion.md#4-common-interaction-and-information-boundaries).

The later screenshot of the session-check screen appearing on every navigation
identified a separate workspace-lifetime issue (REV-19). A shared operational
layout now retains the session-owning workspace across route changes while
preserving the existing authorization and tenant-isolation rules.

The user supplied the [Option B full-system visual reference](https://claude.ai/artifact/XMD6gScr8TVDnWvYtcvNWP) and requested its application throughout the frontend. This supersedes the earlier visual shell and OS-selected theme, while preserving the domain contracts and original decision numbering. [REV-12](./design-register.md) and [shared system section 3](./spec-system-completion.md#3-navigation-and-visual-system) record the updated visual contract. The [UI mapping](./docs/ui-design.md) distinguishes the user's reference from assistant-selected responsive and live-data adaptations.
