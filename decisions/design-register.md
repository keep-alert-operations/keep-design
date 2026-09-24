# Design register

All 55 original issue identifiers are retained below. Status: **design closed** for the initial release. The domain specifications own the contracts; this index records coverage. [Delivery readiness](./delivery-readiness.md#evidence-register) tracks implementation, supplied service facts and executed qualification separately. Record newly discovered gaps here without reusing or deleting an identifier.

## A. Identity, tenant administration, and permissions

| ID | Selected contract and reference |
|---|---|
| A1 | Tenant identity, globally unique names, fixed Global, creation/rename and no delete/disable are selected in tenant/access 1–4/10–12; physical constraints and bootstrap in system completion 11–12/28. |
| A2 | Team-owned internal Keycloak, LDAP immutable identity, nested memberships and OIDC/session settings are selected in identity configuration 1–14; runtime/schema and installed-version acceptance in system completion 1/12/24–25. |
| A3 | Five-minute normal-operation access-change enforcement and last-known trusted identity during refresh outages remain unchanged. Authorization guards, checkpoint persistence and restore gates are selected in identity configuration 6–12 and system completion 7/12/20. |
| A4 | Highest-role grants, local-admin continuity, orphaned principals, eligible assignees and access-loss handling are selected in tenant/access and identity supplements; atomic enforcement is completed in system completion 7/12/17. |
| A5 | The tenant/access permission matrix, Global/global-super-admin exceptions and 365-day admin-readable access audit are preserved. Resource UI/API enforcement and scoped physical records are complete in system completion 3–12. |

## L. Alert schema, identity, and lifecycle

| ID | Selected contract and reference |
|---|---|
| L1 | Native v1/v2 validation, field catalog, managed/source separation and body/field limits are selected in alert operations 1–7; strict common models and wire conventions are completed in system completion 1/5. |
| L2 | Tenant/schema/operator-specific identity, exact immutable material, collision handling, occurrences and no v1/v2 merging are selected in alert operations 5–9 and technical baseline 8–10. |
| L3 | PG durable admission, finite external retry windows, tenant FIFO source order and semantic change-order separation are selected in alert operations 8–14 and technical baseline 12–14. Maintenance temporal integration is complete in maintenance 4–10. |
| L4 | Only selected source fields mutate; manual pending-source/revision guards and source/manual precedence remain alert operations 5–7/13–18. Maintenance/correlation evaluate trustworthy before/after snapshots without inventing transitions. |
| L5 | PG-authoritative source/activity/occurrence/note history, current-note-only search, snapshots and read-your-writes are complete in alert operations 20–27 and technical baseline 8–22. |
| L6 | 30-day source inactivity/hourly expiry, 90 days after latest resolution, reopening cancellation and no creation-age cap/manual deletion remain selected. Technical baseline 23–27 completes protected logical retirement and physical cleanup. |

## O. Operators, Kong, and Grafana

| ID | Selected contract and reference |
|---|---|
| O1 | V1 unauthenticated Global and v2 immutable operator tenant routing, strict batches and Grafana native-equivalent adapter are selected in alert/operator supplements. No alternate routing or credential bypass is introduced. |
| O2 | Operator names/ownership/lifecycle, admin-only management, retained-alert/pending-input deletion guard and Grafana-gated rename/delete are complete in operator operations; physical records and saga integration in system completion 13/17–20. |
| O3 | One current key plus a 24-hour retiring overlap, repeatable copy-only retrieval, encryption, immediate revoke, exact admission and restore denial fences remain operator operations 4–14/28. Secret/runtime integration is complete in system completion 13/20–22. |
| O4 | Mandatory shared Grafana contact point/policy, exact Appchi - {operator name}=true matcher, safe external writer, durable setup/rename/delete/cancel and adapter contracts remain operator operations 15–28; capability acceptance is system completion 24. |

## Q. CEL, filtering, sorting, and pagination

| ID | Selected contract and reference |
|---|---|
| Q1 | Shared cel-expr-python checked IR/runtime/ES translation, initial vocabulary, type/null rules, profile migration and deterministic cost accounting are complete in technical baseline 2–7. Measured numeric budgets follow system completion 23. |
| Q2 | Supported predicates/literals, presence, Unicode/string/time semantics, rule whitelist, fixed/captured clocks and no scripts/full scans are complete in technical baseline 2–7; shared editor/test behavior is completed in maintenance 14 and system completion 9. |
| Q3 | Default suppression exclusion remains outside CEL; feed inclusion is transient, incident linked views show suppression, dashboard counts have no inclusion switch. Preset 6/12 and dashboard 6 define identical effective count filters. |
| Q4 | Feed sorting/columns/PIT pagination and no separate feed time picker remain selected. Dashboard 4/6/9–12 completes responsive layout, no separate dashboard time filter, live/pause and same-PIT/clock count batches. |

## C. Correlation behavior and processing

| ID | Selected contract and reference |
|---|---|
| C1 | Every one of 1–10 named conditions needs eligible evidence; one alert may satisfy multiple conditions, with no count thresholds. Correlation 1–4/10 and system completion 9/16 select editor/API/storage without changing this rule. |
| C2 | Arrival/effective-time memberships, half-open expiry, no refresh from repeats, current-time recovery and reset fences remain correlation 3–4/8–11/16–18. Maintenance 4–10 completes temporal producer proof. |
| C3 | Firing/unsuppressed eligibility, permitted group movement, ownership and fresh-transition re-entry are unchanged. Correlation 2–4/9–15 plus maintenance 5–8 and system completion 15–17 complete integration. |
| C4 | Condition/name normalization, explicit severity, 1–1,440-minute windows, up to three typed grouping fields, validation, health and read-only selected-alert tests are complete; API and editor in system completion 9. |
| C5 | Earlier-created-rule/UUID/full-group arbitration, complete atomic eligible attachment and current-time checks remain correlation 12–14. Full-key physical context identity and lock integration are system completion 16–17. |
| C6 | Revision/epoch/grouping generations, metadata versus logic resets, enable/disable/delete/name reuse and no backfill remain correlation 5–9/18. System completion 9/16/19–20 closes routes, records and final-deleted-definition retention. |
| C7 | Incident resolution/unlink/reopen atomically updates context/alert boundaries and ownership; old-generation incidents never reset current contexts. Correlation 15 and system completion 10/15–17 preserve those contracts. |
| C8 | PG journal/cursor/evidence, atomic proof/action commits, blocked errors/quotas and replay-safe recovery are complete in correlation 8–24, technical baseline and system completion 16–18/20/23. |

## M. Maintenance rules

| ID | Selected contract and reference |
|---|---|
| M1 | Maintenance 1–5/7/9–10 completes immutable-start/CEL locks, temporal controls, no-backfill activation/re-enable, exact receipt/effective times and schedule/edit races while preserving prior product choices. |
| M2 | Maintenance 6–9/11 defines per-segment cause intervals plus separate v2 source suspension, complete overlap OR, historical versus current state and bounded fan-out with authoritative derived checks. |
| M3 | Maintenance 1–3/12–15 completes duplicate names, reason/metadata, explicit IANA/local/occurrence API, DST rejection/choice, fixed UTC instants across tzdata changes, audit and UI. |
| M4 | Maintenance 5–8 preserves alert lifecycle and incident membership during suppression, manual suppressed linking and separate subset counts. First-seen resolved coverage creates no firing occurrence/evidence. |
| M5 | Maintenance 4–11/17–19 completes scheduler leases/generation fences, immediate controls, delayed effective-end correlation, proof recovery, exact overlap release and searchable/rendered completion generations. |

## I. Incident operations

| ID | Selected contract and reference |
|---|---|
| I1 | Manual/automatic creation, immutable origin/severity, optional initial links and fixed content rules remain incident operations 1–3; routes/schema in system completion 10/15. |
| I2 | Independent status/assignment, lifecycle cycles, direct resolve, reopen conflicts and unchanged alert statuses remain incident operations 4/9/12/17–18. Physical claims and transactions are system completion 15–17. |
| I3 | Active-only manual link/unlink/Move, <=100 explicit distinct IDs, atomic ownership and unavailable counterpart references remain incident operations 5–7/17–18; exact routes and tables are system completion 10/15. |
| I4 | 30-day qualifying inactivity/hourly expiry and 90-day latest-resolution retention remain unchanged. Source activity ordering and protected parent purge are complete in system completion 15/19–20. |
| I5 | Incident list/detail/current text search, notes/history, assignment and counters are selected in incident operations. System completion 8/10/15 completes token lookup, API routes, physical records and consistent reads. |

## D. Persistence, events, consistency, and recovery

| ID | Selected contract and reference |
|---|---|
| D1 | Versioned alert snapshots and separate domain metadata invalidations, immutable references/digests, consumer holds and atomic source/control proof are complete in technical baseline 8–14, maintenance 4–11 and system completion 18. |
| D2 | PG durable work/outbox, Kafka tenant-keyed delivery, fenced retries/scans/offsets and Redis hint reconciliation are selected; other-resource jobs/live events complete in system completion 18/22. Supplied capabilities are DEL-01. |
| D3 | Protected recovery evidence, fresh restore epochs, session/permission/key/deletion gates and snapshot-plus-catch-up search rebuild are complete in technical baseline 24–26 and system completion 20/24/29. Exercises are DEL-05. |
| D4 | All domain/source/history/receipt/outbox atomic boundaries, full lock hierarchy, authorization guards, maintenance fan-out and reference races are selected in technical baseline, maintenance 4–11, dashboard 13 and system completion 7/17. |
| D5 | Physical record families, types/constraints/FKs/indexes/partitioning, RLS, search tokens and full-key context identity are complete in technical baseline 8–10, maintenance 11, dashboard 13 and system completion 11–17. DDL implementation is DEL-02. |

## R. Retention and deletion

| ID | Selected contract and reference |
|---|---|
| R1 | Alert and incident independent inactivity and 90-day latest-resolution retention remain selected, with no absolute creation-age cap. System completion 19 consolidates lifetimes without changing them. |
| R2 | Parent-owned source/occurrence/note/activity/command history, finite ingress retry windows and protected pending proof remain selected. System completion 7/19–20 distinguishes internal-command fences from external retry retention. |
| R3 | Every product history category is selected in system completion 19, including final deleted correlation definitions, complete maintenance timeline, dashboards and platform configuration/repair audit. Infrastructure telemetry policy remains owner-managed. |
| R4 | All-resource retirement/replay fences, independently protected intents/finals, dependency-aware bounded cleanup and restore gates are complete in technical baseline 23–27 and system completion 19–20; service protection/exercises remain DEL-05. |

## U. User experience, APIs, and live updates

| ID | Selected contract and reference |
|---|---|
| U1 | All initial resource screens, tenant navigation, drafts/conflicts, responsive layouts, accessibility and scoped degraded states are selected across resource supplements and system completion 3–4/8–10. |
| U2 | One shared catalog/CEL editor, explicit validation/run/test, source-span errors and side-effect-free single-alert rule tests are complete in preset 5/9, maintenance 14 and system completion 9. No automatic overlap scan or historical simulation. |
| U3 | Dashboard 1–18 completes shared CRUD/copy/history, panel layout/titles/thresholds, drill-through, no separate time filter/suppression switch, refresh/pause/fullscreen, atomic references, exact count batching and failures. |
| U4 | Technical baseline 16–21 completes searchable positions, PG generations, Redis/SSE reconciliation, bounded streams/reconnect/observations; maintenance 18 and dashboard 9–12 close their specialized generation/count presentation. |
| U5 | Common HTTP/JSON/errors/revision/idempotency/pagination and all remaining incident/correlation/maintenance/dashboard routes are selected in system completion 5–10 and resource supplements. Existing auth/ingress/operator contracts remain unchanged. |

## N. Infrastructure, capacity, and delivery planning

| ID | Selected contract and reference |
|---|---|
| N1 | Capacity requirements are preserved; system completion 23 selects the combined measurement procedure, safety margin, versioned budgets and readiness enforcement. Actual numerical profile and results are required DEL-03 evidence, not unresolved architecture. |
| N2 | System completion 1–2/21–25 selects frameworks/repository/workloads/security/Keycloak operation and required environment capability manifest. Dedicated teams retain infrastructure policy; actual service bindings/allocation are DEL-01/06. |
| N3 | Selected SLOs, outage behavior and ownership remain reliability operations. System completion 20–25/29 closes application recovery/readiness/runbooks; actual service guarantees and observed SLOs remain DEL-01/05/08. |
| N4 | System completion 26–30 selects CI, acceptance matrix, six delivery milestones, compatible rollout/rollback, support and evidence gates. Implementation/executed qualification is DEL-02–08, not a remaining design choice. |

## Documentation review — 2026-09-22

The following assistant-selected clarifications close ambiguities found during the full-document review. They preserve prior product decisions.

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-01 | L1, L2 | Consolidated the exact native field inventory in Alert operations. Removed obsolete “confirm encoding” text; v1 omission uses the selected length-prefixed key and v2 uses its selected canonical hash. |
| REV-02 | U5, L4 | Preserved native ingestion at `/api/ingest/v1/alerts` and `/api/ingest/v2/alerts`, correcting the inconsistent abbreviated roots. Made every alert-owned route explicit, selected the bulk command route/body/result order, rejected duplicate IDs with conflicting revisions, applied the common DELETE header contract to note deletion, and made the existing preset/tenant-creation idempotency-scope exceptions explicit in the shared contract. |
| REV-03 | D4, N1 | Specified durable item reservations, global/tenant counter lock order, atomic reserve/release and mismatch recovery for backlog limits. Duplicates do not consume another reservation; accepted work is never discarded. |
| REV-04 | M2, L4 | Clarified that manual status changes do not directly erase suppression causes, but maintenance matching is recomputed from before/after state and can release a cause when its expression becomes false. |
| REV-05 | U1–U5, N4 | Consolidated the architecture overview; separated acceptance, delivery evidence and decision provenance; removed stale scope/dependency/completion narratives. Detailed resource contracts remain in their authoritative documents, including idempotent Global bootstrap/readiness rules formerly stated only in the overview. |

Review validation checks documentation consistency, identifiers, local links and structural integrity. It does not supply runtime or capacity evidence.

## Implementation clarifications — 2026-09-23

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-06 | L4, U1, U5 | Alert notes add a default-off deleted-note discovery selector bound into cursors; retained revision text remains on the existing history route. Source details render received JSON as plain text. This adds no retention or source-input behavior. |
| REV-07 | U5 | Corrected the shared cursor implementation to return 409 for authenticated cursor context changes, as already required by system completion 6. Malformed cursor encoding remains 400; authorization is still checked before cursor use. |
| REV-08 | M4, U2, U5 | Added a read-only saved maintenance tester using existing persisted UTC endpoints and expected revision, so ended windows remain testable without converting them into invalid new schedules. It preserves no-backfill and performs no activity, command or cause writes. |
| REV-09 | U3, U5 | Dashboard list ordering uses explicit sort/direction and ascending UUID ties; deleted discovery orders by the newest retained recording time. Counts expose compiler-derived relative-clock metadata. Corrected string/integer generation comparison so unchanged configuration cursors page successfully. |
| REV-10 | L4, D4 | Alert detail now derives suppression in one PostgreSQL repeatable-read snapshot and returns unavailable when a closed maintenance gate leaves a retained timeline unprovable. Independent maintenance CEL tests derive only permitted input fields. Alert note authors, revision actors and human activity capture display names; existing unknown historical names remain null rather than being reconstructed from today's directory. These implement existing contracts. |
| REV-11 | N2, U5 | Later user direction authorizes isolated local Keycloak users/groups in place of external LDAP for development. Identity configuration 14 defines the exception: immutable native UUID/sub binding, real OIDC and guarded directory publication, bounded read-only Admin API polling, and no restore-gate bypass. Production LDAP remains unchanged. |

## User visual direction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-12 | U1, U2, U3, U5 | User supplied a full-system visual reference and requested the entire UI adopt it. Shared system section 3 now records its left rail, typography and fixed light palette, superseding automatic OS theme selection. Assistant-selected adaptations retain responsive stacking, real API data, existing authorization and conflict/recovery controls; illustrative prototype counts and people are not application defaults. See [UI mapping](docs/ui-design.md). |
| REV-13 | U1, U5, I4 | User reported gaps between the implemented UI and the reference and asked for an exact match. Every screen now uses the reference page frame, grid tables and controls (see [UI mapping](docs/ui-design.md)). Assistant-selected read-time enrichment adds optional current-directory labels beside principal ids — `assignee_display_name`, `acknowledged_by_display_name`, `created_by_display_name`, `updated_by_display_name` — plus `active_incident_id`/`active_incident_title` on alerts and `origin_rule_id`/`origin_rule_name` on incidents. These are presentation labels for current records; recorded history keeps its captured labels per REV-10. **Open gap:** incident activity stores only `actor_id`, so the UI cannot show captured actor names there without new persisted evidence; historical names are not rebuilt from today's directory. |
| REV-14 | Q4, U1, U5 | Continuation review found the redesigned table ignored saved/draft preset columns and always indicated descending last-received sorting. Corrected custom field order and actual sort indicators under the existing [preset column contract](spec-preset-operations.md#4-columns-and-sorting). Assistant-selected presentation adaptation retains the reference's compact default grouping and uses individual columns for custom selections; row navigation and suppression remain visible independently of Message. Added browser regressions, and scoped the saved-preview pagination assertion to its cursor request rather than the last concurrent count request. See [UI mapping](docs/ui-design.md). |

## User sign-in direction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-15 | A2, N2, U5 | User requested removal of the one-time-code step and username/password-only Appchi login. [Identity section 3](spec-identity-configuration.md#3-username-and-password-authentication) supersedes the earlier assistant-selected application TOTP requirement. Assistant-selected migration disables local application OTP execution/enrollment, preserves existing accounts and passwords, and requires protected password evidence in the backend. Separate Keycloak console MFA and production LDAP identity ownership remain unchanged; no shared service was modified. |
| REV-16 | A2, U5 | User reported the raw expired/consumed sign-in transaction error. Assistant-selected recovery sends HTML browser callbacks with unavailable transactions to a public page with an explicit fresh sign-in link. No rejected code is exchanged and no session is created; JSON clients retain 401 and existing ten-minute expiry/one-use checks remain authoritative. Corrected stale authenticator-code copy in the sign-in shell. See [identity section 2](spec-identity-configuration.md#2-login-flow-and-browser-boundary). |

## Preset creation correction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-17 | Q4, U1, U5 | User reported new presets only matched their column configuration after editing the columns. The renderer incorrectly treated the default field list as permission to substitute composite Alert/Ownership cells. Every explicit saved/draft column list now renders individual fields in its configured order. This supersedes REV-14's assistant-selected default-preset grouping exception. New-form defaults also match preset section 3; existing saved orders are preserved. Creation/reload/editor and original-default browser regressions passed. |

## Loading-state correction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-18 | U1, U5 | User reported transient text moving page content and loading text repeatedly replacing confirmed empty states. Assistant-selected presentation correction distinguishes initial loading from a refresh of a completed result: preserve rows and confirmed empty states for the same query, keep transient status inside existing areas, and show unavailable warnings only for failures. Saved preset empty results retain their completed query identity. This adds no caching, refresh delay or domain behavior; shared system section 4 and the UI mapping record the contract. |

## Navigation session correction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-19 | U1, U5, N2 | User supplied a screenshot of the initial session-check screen appearing between every page. The catch-all page recreated the session-owning workspace on each route change. Assistant-selected implementation correction moves that workspace into a shared route-group layout while keeping the public expired-sign-in page outside it. Internal navigation preserves the mounted workspace; tenant resets, revalidation, access-loss clearing and sign-out remain enforced. No authentication policy or session duration changes. |
