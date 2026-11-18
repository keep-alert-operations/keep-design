# Design register

All 55 original issue identifiers are retained below. Status: **design closed** for the initial release. The domain specifications own the contracts; this index records coverage. [Delivery readiness](https://github.com/keep-alert-operations/keep-delivery/blob/main/status/delivery-readiness.md#evidence-register) tracks implementation, supplied service facts and executed qualification separately. Record newly discovered gaps here without reusing or deleting an identifier.

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
| L2 | Tenant/schema/operator-specific identity, exact immutable material, collision handling, occurrences and no v1/v2 merging are selected in alert operations 5–9 and technical baseline 8–10. REV-54 adds identity format 2 for a supplied v2 name; unnamed keys are unchanged. |
| L3 | REV-33 selects Kafka-confirmed admission, internal delivery UUID replay, per-logical-key append order and tenant-keyed changed order. Ingress UTC and PG application proof order are distinct. Kafka pipeline sections 2–5 and the revised alert/maintenance supplements govern. |
| L4 | Only selected source fields mutate; manual revision guards remain, while REV-33 removes the pending-source guard and permits queued Kafka input after a manual commit (alert operations 5–7/13–18). Maintenance/correlation evaluate trustworthy before/after snapshots without inventing transitions. |
| L5 | PG-authoritative source/activity/occurrence/note history, current-note-only search, snapshots and read-your-writes are complete in alert operations 20–27 and technical baseline 8–22. |
| L6 | REV-34 defers automatic 30-day inactivity resolution and 90-day retirement/cleanup as nice-to-have components. Existing retirement fences and read-time access rules remain; worker scope is authoritative over the retained algorithms in technical baseline 23–27. No creation-age cap or manual alert deletion is introduced. |

## O. Operators, Kong, and Grafana

| ID | Selected contract and reference |
|---|---|
| O1 | V1 unauthenticated Global and v2 immutable operator tenant routing, strict batches and Grafana native-equivalent adapter are selected in alert/operator supplements. No alternate routing or credential bypass is introduced. |
| O2 | Operator names/ownership/lifecycle, admin-only management, retained-alert guard, verified gateway denial plus Kafka drain, and Grafana-gated rename/delete are complete in operator operations; physical records and saga integration in system completion 13/17–20. |
| O3 | One current key plus a 24-hour retiring overlap, repeatable copy-only retrieval, encryption, immediate local invalidation and verified all-node revocation completion, exact admission and restore denial fences remain operator operations 4–14/28 and Kafka pipeline 7. Secret/runtime integration is complete in system completion 13/20–22. |
| O4 | Mandatory shared Grafana contact point/policy, exact Keep - {operator name}=true matcher, safe external writer, durable setup/rename/delete/cancel and adapter contracts remain operator operations 15–28; capability acceptance is system completion 24. |

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
| I2 | Independent status/assignment, lifecycle cycles, direct resolve, reopen conflicts and unchanged alert statuses remain incident operations 4/9/12/17–18; REV-46 adds resolution when all linked alerts resolve. Physical claims and transactions are system completion 15–17. |
| I3 | Active-only manual link/unlink/Move, <=100 explicit distinct IDs, atomic ownership and unavailable counterpart references remain incident operations 5–7/17–18; exact routes and tables are system completion 10/15. |
| I4 | 30-day qualifying inactivity/hourly expiry and 90-day latest-resolution retention remain unchanged. Source activity ordering and protected parent purge are complete in system completion 15/19–20. |
| I5 | Incident list/detail/current text search, notes/history, assignment and counters are selected in incident operations. System completion 8/10/15 completes token lookup, API routes, physical records and consistent reads; REV-53 adds period reports in incident operations 20; REV-56 adds link counts to list rows. |

## D. Persistence, events, consistency, and recovery

| ID | Selected contract and reference |
|---|---|
| D1 | Versioned alert snapshots and separate domain metadata invalidations, immutable references/digests, consumer holds and atomic source/control proof are complete in technical baseline 8–14, maintenance 4–11 and system completion 18. |
| D2 | REV-33 replaces alert PG queues/relays with self-contained received records and transactional changed/offset publication. PG retains authority/replay proof; bounded search reconciliation repairs lost manual hints. Unrelated PG jobs/live events remain in system completion 18/22. Supplied capabilities are DEL-01. |
| D3 | Protected recovery evidence, fresh restore epochs, session/permission/key/deletion gates and snapshot-plus-catch-up search rebuild are complete in technical baseline 24–26 and system completion 20/24/29. Exercises are DEL-05. |
| D4 | Domain/source/history/proof transactions, the separate Kafka changed/offset transaction, full lock hierarchy, authorization guards, inline maintenance effects and bounded fan-out/reference races are selected in Kafka pipeline, technical baseline, maintenance 4–11, dashboard 13 and system completion 7/17. |
| D5 | Physical record families, types/constraints/FKs/indexes/partitioning, RLS, search tokens and full-key context identity are complete in technical baseline 8–10, maintenance 11, dashboard 13 and system completion 11–17. DDL implementation is DEL-02. |

## R. Retention and deletion

| ID | Selected contract and reference |
|---|---|
| R1 | Alert and incident independent inactivity and 90-day latest-resolution retention remain selected, with no absolute creation-age cap. System completion 19 consolidates lifetimes without changing them. |
| R2 | Parent-owned source/occurrence/note/activity/command history and protected proof remain selected. Kafka pipeline 8 preserves minimal delivery and retired-key fences; client resubmissions have no deduplication promise. System completion 7/19–20 retains internal command replay protections. |
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
| REV-10 | L4, D4 | Alert detail now derives suppression in one PostgreSQL repeatable-read snapshot and returns unavailable when a closed maintenance gate leaves a retained timeline unprovable. Independent maintenance CEL tests derive only permitted input fields. Alert note authors, revision actors and human activity capture display names; existing unknown historical names remain null rather than being reconstructed from today's directory. These implement existing contracts. Superseded for maintenance by REV-39: there is no maintenance gate; detail is unavailable (`maintenance_proof_unavailable`) only when an alert has no current maintenance checkpoint. |
| REV-11 | N2, U5 | Later user direction authorizes isolated local Keycloak users/groups in place of external LDAP for development. Identity configuration 14 defines the exception: immutable native UUID/sub binding, real OIDC and guarded directory publication, bounded read-only Admin API polling, and no restore-gate bypass. Production LDAP remains unchanged. |

## User visual direction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-12 | U1, U2, U3, U5 | User supplied a full-system visual reference and requested the entire UI adopt it. Shared system section 3 records its left rail, typography and original fixed light palette, which superseded automatic OS theme selection at the time. REV-42 later replaces the colors with the Ocean palette and keeps the rest of the reference. REV-20 later adds user-selectable dark mode while retaining this light reference as default. Assistant-selected adaptations retain responsive stacking, real API data, existing authorization and conflict/recovery controls; illustrative prototype counts and people are not application defaults. See [UI mapping](https://github.com/keep-alert-operations/keep-frontend/blob/main/docs/ui-design.md). |
| REV-13 | U1, U5, I4 | User reported gaps between the implemented UI and the reference and asked for an exact match. Every screen now uses the reference page frame, grid tables and controls (see [UI mapping](https://github.com/keep-alert-operations/keep-frontend/blob/main/docs/ui-design.md)). Assistant-selected read-time enrichment adds optional current-directory labels beside principal ids — `assignee_display_name`, `acknowledged_by_display_name`, `created_by_display_name`, `updated_by_display_name` — plus `active_incident_id`/`active_incident_title` on alerts and `origin_rule_id`/`origin_rule_name` on incidents. These are presentation labels for current records; recorded history keeps its captured labels per REV-10. **Open gap:** incident activity stores only `actor_id`, so the UI cannot show captured actor names there without new persisted evidence; historical names are not rebuilt from today's directory. |
| REV-14 | Q4, U1, U5 | Continuation review found the redesigned table ignored saved/draft preset columns and always indicated descending last-received sorting. Corrected custom field order and actual sort indicators under the existing [preset column contract](../specs/spec-preset-operations.md#4-columns-and-sorting). Assistant-selected presentation adaptation retains the reference's compact default grouping and uses individual columns for custom selections; row navigation and suppression remain visible independently of Message. Added browser regressions, and scoped the saved-preview pagination assertion to its cursor request rather than the last concurrent count request. See [UI mapping](https://github.com/keep-alert-operations/keep-frontend/blob/main/docs/ui-design.md). |

## User sign-in direction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-15 | A2, N2, U5 | User requested removal of the one-time-code step and username/password-only Keep login. [Identity section 3](../specs/spec-identity-configuration.md#3-username-and-password-authentication) supersedes the earlier assistant-selected application TOTP requirement. Assistant-selected migration disables local application OTP execution/enrollment, preserves existing accounts and passwords, and requires protected password evidence in the backend. Separate Keycloak console MFA and production LDAP identity ownership remain unchanged; no shared service was modified. |
| REV-16 | A2, U5 | User reported the raw expired/consumed sign-in transaction error. Assistant-selected recovery sends HTML browser callbacks with unavailable transactions to a public page with an explicit fresh sign-in link. No rejected code is exchanged and no session is created; JSON clients retain 401 and existing ten-minute expiry/one-use checks remain authoritative. Corrected stale authenticator-code copy in the sign-in shell. See [identity section 2](../specs/spec-identity-configuration.md#2-login-flow-and-browser-boundary). |

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

## Dark-mode direction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-20 | U1, U5 | User requested dark mode after the full-system light visual reference. Shared system section 3 now requires an explicit Light/Dark choice for Keep-owned screens, superseding REV-12's fixed-light behavior. Assistant-selected behavior retains the light palette (the Ocean palette since REV-42) by default, independent of OS preference, and persists the user's choice locally across navigation and reloads without identity or tenant data. Both palettes keep readable controls, status text and focus. External Keycloak pages retain their separate theme. |

## Dashboard refresh correction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-21 | U3, U5 | User reported two brief yellow banners pushing dashboard panels down when an alert arrived. Tenant health and the count batch independently displayed indexing lag, while every in-flight count request marked retained panels stale. Assistant-selected presentation moves routine lag/progress into existing status areas and preserves panel positions, values and colors during refresh. Actual failures remain explicit. This refines the prior generic banner wording in shared system section 4 and dashboard section 16 without changing count snapshots, refresh timing or processing. |

## Local v2 configuration — 2026-09-24

| ID | Original coverage | Resolution |
|---|---|---|
| REV-22 | O1, O2 | User requested configuring v2 for local development after test alerts could only enter Global through v1. Assistant-selected dedicated local Kong/Grafana services and a worker-authenticated serving-member proof preserve the normal operator saga, encrypted keys, exact labels and pinned mTLS tenant routing. Local initial-gate bootstrap refuses production/shared databases and restore fences. Operator section 29 records the scope; docs/local-v2.md contains runtime bindings and evidence. |

## Approved login design — 2026-09-27

| ID | Original coverage | Resolution |
|---|---|---|
| REV-23 | U1, U5, N2 | User approved implementing the Keep login mock after requesting a custom form backed by Keycloak. The `keep` client login theme supersedes minimal stock-page branding and REV-20's separate-theme limitation. Assistant-selected integration preserves Keycloak's generated form action, code flow/PKCE and console theme; only an initial 401 `unauthenticated` starts login automatically, preserving the requested local path. Explicit logout, expired callbacks, access denial and service failures retain recovery controls. Light/dark preference is local to each origin. Identity sections 1–2 and shared system section 3 record the contract. |
| REV-24 | U1, U5 | User requested an icon-based Light/Dark switch after reviewing the account menu. The signed-in account menu and signed-out application state now share an accessible sun/moon switch; existing preference persistence and the light default remain. The UI mapping records the control. |

## Preset alert return navigation — 2026-09-27

| ID | Original coverage | Resolution |
|---|---|---|
| REV-25 | U1, U3, U5 | User reported that opening an alert from saved preset results offered only the All alerts return path. Assistant-selected correction reuses the existing browser-tab alert-list context to show the preset breadcrumb and Back to preset action, and keeps Previous/Next scoped to the visible result page. A direct alert link without source context still opens normally. Returning to the preset resets transient filters under the existing preset contract. |
| REV-26 | U1, U5 | User requested opening presets by clicking anywhere in a list row. The existing primary link now covers the row; Edit, History and the action menu retain independent hit targets. The same primary destinations and unsaved-change navigation guard remain in effect. |

## Assignment-based alert status — 2026-09-27

| Review ID | Original coverage | Decision / correction |
|---|---|---|
| REV-27 | L4, A4, Q4, U1, U5 | User approved one assignment control, removal of independent acknowledgement, and Acknowledged status whenever an alert is firing and assigned. Assignment, reassignment, unassignment and occurrence transitions follow alert operations section 17. Assistant-selected compatibility retains old physical fields, immutable evidence and legacy CEL/sort meanings without exposing a second current ownership field; current responses derive `display_status`, and search lowers that feed field onto the existing index. Retire `set_acknowledged` with 422; adapt legacy current-view columns without rewriting saved history. The new visible status is filterable but not sortable; raw lifecycle sort is labelled Lifecycle. This supersedes REV-13's current acknowledger display-name addition and the old independent acknowledgement contract. |

## Current alert JSON viewer — 2026-09-27

| Review ID | Original coverage | Decision / correction |
|---|---|---|
| REV-28 | U1, U5 | User requested a View alert button on the specific alert detail page. It displays the currently loaded detail response as formatted, read-only JSON in a native dialog available to page readers. Dismissal and focus follow native dialog behavior; opening performs no second request or mutation. UI mapping and shared system section 3 record this presentation contract. |

## Bare CEL field identifiers — 2026-09-27

| Review ID | Original coverage | Decision / correction |
|---|---|---|
| REV-29 | Q2, U2 | User requested that alert CEL conditions use field names directly (for example, `application`) without requiring `alert.`. Assistant-selected compatibility retains `alert.field` for saved source, keeps the existing context allow-lists, and treats bare identifiers as additive within `keep-cel-v1` because old expression meaning is unchanged. The editor, chips, functions, quick views and new examples use bare identifiers; stored source is not rewritten. |

## Local correlation preview — 2026-09-27

| Review ID | Original coverage | Decision / correction |
|---|---|---|
| REV-30 | C1–C8, N1 | User asked the assistant to make correlation rules creatable in the isolated local stack. Assistant-selected development preview uses explicit finite limits while keeping the profile unqualified. Code, local deployment epoch and disposable-PostgreSQL check evidence bind the preview; audited activation requires healthy source order and no maintenance windows or effects. Production/staging retain the fully measured profile requirement. The preview worker uses the normal PostgreSQL journal and incident transaction path; its limits are local safety ceilings, not release capacity claims. Superseded for correlation/maintenance by REV-39: the preview, its activation and its preview profile flags are removed; correlation is always on. |

## Alert operator display — 2026-09-28

| Review ID | Original coverage | Decision / correction |
|---|---|---|
| REV-31 | L2, U1, U5 | User requested operator names in alert views where the managed operator ID appeared. Alert detail, source activity and configurable Operator columns display the current same-tenant managed name for v2; v1 displays its exact source string. Assistant-selected implementation adds read-time `operator_display_name` to alert detail/feed/preview responses and shows Unknown operator when a v2 name cannot be resolved. The stable `operator` ID and its identity, CEL and sort contracts remain unchanged. See [alert operations section 3](../specs/spec-alert-operations.md#3-managed-field-catalog). |

## Quick result sorting — 2026-09-28

| Review ID | Original coverage | Decision / correction |
|---|---|---|
| REV-32 | Q4, U1, U5 | User requested column-title sorting on All alerts and saved preset results, cycling ascending, descending and regular order. The transient override replaces the preset's whole sort while active and never saves it. Assistant-selected scope makes only existing server-sortable fields clickable; composite and derived headings stay static under the existing sort whitelist. Sort changes restart the alert snapshot on page one and clear selection. See [alert operations section 24](../specs/spec-alert-operations.md#24-reads-search-and-presentation) and [preset operations section 4](../specs/spec-preset-operations.md#4-columns-and-sorting). |

## Kafka-first alert redesign — 2026-09-30

| Review ID | Original coverage | Decision / correction |
|---|---|---|
| REV-33 | L1–L4, C1–C8, D1–D4, N1, R1–R4 | User accepted Kafka-first admission, no Keep PG ingress dependency, transactional source changed+offset publication, tenant Kafka correlation order, ignored manual edits except resolve, inline maintenance effects, best-effort search hints with reconciliation, and actual Kong policy enforcement. [Kafka-first pipeline](../specs/spec-kafka-alert-pipeline.md) records all eight assistant-selected technical decisions and the accepted Kafka retention-loss limitation. Implementation/qualification evidence remains separate. |

## REV-34 — User-deferred workers and synchronous provisioning (2026-09-30)

User correction: defer maintenance timer release, assignment cleanup, inactivity/
retention workers and operator background orchestration. A later source update
may clear ended maintenance suppression. Keep operator HTTP requests open until
verified success/failure. Keycloak-only identity supply is a question, not an
accepted replacement. [Worker scope](../specs/spec-worker-scope.md) records the normative
supersession, nice-to-have components and explicitly assistant-selected details:
source-time release/cutover, unchanged history access windows and assignee masking,
durable partial-operation recovery, HTTP budgets, isolated provisioning connection
and expiry disposal on the next successful mutation. Original issue IDs remain.
Implementation/qualification evidence is tracked separately in
[worker-scope implementation](https://github.com/keep-alert-operations/keep-delivery/blob/main/docs/worker-scope-implementation.md).

## REV-35 — Directory worker nice-to-have (2026-09-30)

User decision: remove the directory worker from current deployment and put it in
the nice-to-have list. This supersedes REV-34 section 4 and the automatic
five-minute LDAP-change propagation release gate. Assistant-selected boundary:
retain explicit complete trusted publication for bootstrap/manual refresh,
existing identity/grant/session checks and restore gates; unknown identities
remain unavailable until verified publication. No Keycloak-only identity supply
is implied. See [worker scope](../specs/spec-worker-scope.md#4-directory-synchronization-is-nice-to-have). Original IDs are unchanged.

## REV-36 — Live publishing in the Product API (2026-09-30)

User decision: move live hint publishing into the Product API and remove the
separate live worker. Assistant-selected details in [worker scope section 6](../specs/spec-worker-scope.md#6-live-updates-inside-the-product-api) cover off-event-loop bounded publishing,
replica-safe duplicate invalidations, generation-conditional completion, drained
shutdown and minimal API outbox privileges. SSE authorization and PostgreSQL
reconciliation remain. Existing IDs and prior worker deferrals are preserved.

## REV-37 — Independent Git repositories (2026-10-01)

User decision: implement the agreed eleven-repository split inside the existing
GitHub organization, retain the original repository, use `keep-frontend`,
`keep-ingestion` and `keep-migrations`, and work from a parent directory with
system-wide AGENTS.md. [Repository layout](../specs/spec-repository-layout.md)
records ownership and assistant-selected packaging, immutable dependency pins,
HTTP/worker entrypoint separation, schema generation and workspace conventions.
This supersedes the monorepo/shared-backend-image selections without changing
product contracts, transaction boundaries or REV-34–36 worker scope.

## REV-38 — Alembic PostgreSQL migration runner (2026-10-01)

User decision: convert migrations to Alembic. Assistant-selected details in
[repository layout](../specs/spec-repository-layout.md#alembic-migration-execution-rev-38)
preserve SQL bytes/checksums and the original ledger, add one linear revision
chain, verify legacy adoption, retain the transaction/advisory lock, and protect
both ledgers from runtime roles. Forward-only execution and the dedicated
before-writer job retain existing cutover and rollback requirements. Original
issue IDs and decision numbers are unchanged. Executed evidence belongs in delivery.

## Private-cluster initialization implementation — 2026-10-05

User requested implementation of the two remaining load-test bootstrap gaps.
Assistant-selected details under the existing REV-33/34 contracts are recorded in
[pipeline section 9](../specs/spec-kafka-alert-pipeline.md#9-isolated-cluster-initialization-tools):
development-only explicit search initialization with fresh live ES checks and
durable owned retry, plus an API-owned private serving-pool proof helper with
fixed direct members and read-only SQL fences. This is implementation scope for
the isolated cluster; it changes no original issue/decision numbering and grants
no production readiness, automatic retries or infrastructure guarantees.

## Scalability and code review observations — 2026-10-06

The user requested a system-wide review against 5,000 deliveries/minute,
100 active users and 50 tenants. The [review evidence](https://github.com/keep-alert-operations/keep-delivery/blob/main/qualification/scalability-review-2026-10-06.md)
records implementation findings under the existing N1/reliability, search/live,
maintenance and correlation contracts: serial refresh-bound indexing, failed
projection isolation, browser search amplification, blocking async paths,
lifetime maintenance proof limits, whole-evidence rewrites, broad context locks,
activity timer resets, duplicate live polling and missing ordinary request
deadlines. The ended-window evaluation quota discrepancy remains unresolved.

These are review observations and proposed corrections, not new approved design
choices, measured capacity, altered release gates or authorization to reintroduce
deferred workers. Existing 250/second sustained and 500/second recovery requirements,
REV-34–36 scope, all original issue identifiers and decision numbering remain.

## Scalability implementation authorization — 2026-10-06

The user subsequently requested implementation of all review corrections and
combined load/browser testing. Assistant-selected implementation details under
the existing contracts are bounded/coalesced projection batches, per-tenant
leased reconciliation and retry isolation, count-only quick-filter batches,
session-bound PIT disposal, stable activity heartbeats, off-thread SQL, pooled
clients and absolute request budgets. See the updated search and reliability
supplements. Continuation and differential persistence preserve replay proof,
source order, tenant ordering, history access and current worker scope. These
are application implementation choices, not production capacity claims or
authorization to modify shared infrastructure. Executed evidence belongs in
delivery; release pins must advance coherently only after the source combination
is committed and its immutable artifacts are available.

Further assistant-selected implementation detail: periodic repair of unchanged
search documents uses a persisted cursor separate from ordinary delta progress,
with at most one audit page per four ordinary reconciliation turns. A growing
tenant's historical scan must not hold its ordinary searchable watermark at the
audit's starting point. Initial epoch verification remains a complete authority
pass; background audit progress itself never advances that watermark. Database
setup statements may use ordered wire pipelining while preserving separate SQL
snapshots, recovery lock acquisition/check order and transaction boundaries.

## Inline dashboard editing — 2026-10-08

Later explicit user correction removes the separate dashboard editor. The ordinary
board provides inline name editing with a pen icon, a single-panel Create/Edit
dialog, panel options including deletion, and direct dragging/resizing. Save is
enabled only for a changed complete draft and commits it together. See
[dashboard section 8](../specs/spec-dashboard-operations.md#8-shared-editing-copying-and-conflicts).
Original issue IDs and numbered decisions remain unchanged. Existing revision,
permission, count and memory-only draft contracts continue. Executed evidence
belongs in delivery.


## Fluid dashboard layout and upward compaction - 2026-10-08

Later explicit user correction requests fluid dragging/resizing like Grafana and
panels sticking to the top without unsupported vertical gaps. This supersedes
preserving sparse placement. Assistant-selected pixel-following presentation,
drop placeholder, settling animations and vertical gravity are specified in
[dashboard section 4](../specs/spec-dashboard-operations.md#4-layout-and-responsive-behavior).
Opening an older sparse layout displays compacted while remaining clean; only a
subsequent explicit changed-definition Save persists compacted coordinates.
API sizes, identities, permissions, revisions and count contracts continue.
Original issue and numbered decision identifiers remain unchanged. Executed
evidence belongs in delivery.

## Context navigation implementation — 2026-10-12

The user requested implementation of a task-based context layer and linked map.
Assistant-selected implementation details are a design-owned JSON catalog of
exact source sections, mandatory and conditional route edges, a delivery-owned
standard-library reader, and generated Markdown pages that can be browsed in
Obsidian. See the [context guide](../context/README.md). These are navigation
choices, not changes to product requirements or authorization boundaries.
The concise workspace entrypoint retains universal constraints and links the
preserved detailed engineering policies. Scope corrections accompany extracted
sections; keyword matches and routing fixtures never establish complete context
or agent understanding. Original issue IDs and REV numbering are unchanged.
**Superseded in part (2026-11-01):** change-oriented routes are replaced by topics
and intents; see [Context topics and intents](#context-topics-and-intents--2026-11-01).

## Source partition batching — 2026-10-18

The user approved correcting a throughput review finding: the source processor ran
one Kafka transaction and separate PostgreSQL bookkeeping for every input. The
assistant-selected change in [pipeline section 3](../specs/spec-kafka-alert-pipeline.md#3-kafka-keys-fencing-and-two-independent-commits)
takes at most 100 already-fetched inputs per turn. Each input keeps its own
PostgreSQL replay-proof transaction, and each input partition then publishes its
applied inputs in one Kafka transaction: their changed events in input order plus the
next offset. A batch closes after 100 milliseconds of application, the existing yield
bound. Confirmation and position bookkeeping takes one PostgreSQL transaction per
batch. A failed input first lets the inputs before it commit; its own offset is then
retained. Unchanged under REV-33: stable per-partition transactional IDs, assignment
fencing, read_committed consumers, rejoin on uncertain outcomes, per-partition order,
replay at the original coordinate and fault recording. This is an implementation
choice, not a capacity claim. Original issue IDs and REV numbering are unchanged.
Executed evidence belongs in delivery.

## Source receipt ahead of the tenant clock — 2026-10-19

An integration run found an ingress receipt about 10 milliseconds ahead of the
PostgreSQL tenant clock. Maintenance proof correctly refused an effective time after
its application time, and the source processor recorded a fault and held the
partition for 5 seconds. Healthy clocks can differ by more than pipeline latency, so
this recurs as latency falls. The user chose to wait out the lead rather than accept
a tolerance, clamp receipt to processing time or keep the strict hold.
Assistant-selected details in [pipeline section 5](../specs/spec-kafka-alert-pipeline.md#5-utc-maintenance-and-bounded-inline-effects):
the processor compares receipt with the clock it reads under the tenant coordinator,
before any write. A receipt ahead of that clock rolls back the whole application,
including the allocated order. Within the one-second clock-health bound it is not a
fault: only that input partition waits for the measured lead plus 10 milliseconds, an
idle poll is bounded by that deadline, and leads above 100 milliseconds log a
warning. A larger lead records the `source_receive_time_ahead` fault and keeps the
existing 5-second retry. Unchanged: receipts are never replaced by processing time,
no input is applied before the tenant clock reaches its receipt, maintenance and
correlation proof checks, equal-time control precedence and clock-health fencing.
Original issue IDs and REV numbering are unchanged. Executed evidence belongs in
delivery.

## CEL cold compilation process — 2026-10-21

**Open decision; nothing is selected.** Performance item #10 found that each
checked-data cache miss starts a spawned compiler process. An idle miss, including
process start, module import and the compile itself, took 0.35–0.85 seconds on a
12-core Windows development machine (medians about 0.4 and 0.6 seconds in two
runs). With every core busy, 12 of 12 misses overran the one-second compile
deadline and reported CEL unavailable. The contract in
[alert history technical section 5](../specs/spec-alert-history-technical.md#5-limits-cost-and-failure-handling)
requires one-second compiler jobs in a replaceable worker process; options A–C
are implementation choices within it. Because A and B change process isolation,
resource use and lifecycle, the user is asked to choose:

- **A. Persistent compiler worker.** A long-lived process per Keep process takes
  compile requests from a queue and is restarted after a crash or deadline. Open
  questions: one process would see sources from many tenants in turn, so recycling
  after N compiles or any error; concurrency and pool size; memory limits; eager or
  lazy start and shutdown. The deadline would no longer include process start.
- **B. Preloaded fork server.** Python's `forkserver` start method on Linux, with the
  compiler modules preloaded. Each compile still runs in a fresh child forked from a
  server that never sees expression text, so per-compile isolation and the deadline
  measurement stay as they are. Open questions: accepting one long-lived helper
  process per Keep process; Windows development keeps `spawn`; behaviour of the
  native CEL module after fork must be qualified on the Linux image.
- **C. Keep spawn.** Rely on cache sizing; misses stay slow.

Assistant recommendation: B, after measuring miss latency on the supported Linux
image. Until a choice is recorded, each miss keeps a disposable spawned process
with the one-second deadline.

Assistant-selected under the existing CEL contracts: test, validation, search,
count and configuration save handlers keep fresh compiled instances, because they
build no native handle or one per request. Alert, incident and admin mutation handlers already prepare
inline with reused programs on each server thread, as the workers do.
`KEEP_CEL_CACHE_ENTRIES` keeps its 4096 default with documented sizing guidance;
evictions log a rate-limited warning without source text. See the domain
`docs/cel-implementation.md`. Original issue IDs and REV numbering are unchanged.
Executed evidence belongs in delivery.

## Clock-health evidence reuse — 2026-10-21

**Assistant-selected (performance item #6).** A long-running worker loop reuses
parsed clock-health evidence between file changes instead of reading both files on
every turn. Each check stats the file; the parse is reused only while the file's
identity (device, inode or file ID, size, modification and change times) is
unchanged and the parse is less than one second old. Atomic replacement, including
the Kubernetes ConfigMap symlink swap, changes the identity and is seen on the next
check. An in-place rewrite that a coarse file timestamp leaves indistinguishable is
seen within one second. The one-second offset bound and `synchronized` are validated
before any evidence is reused, and age (at most 60 seconds old and at most 1 second in
the future) is evaluated on every check from the cached `measured_at`, so cached
evidence is never accepted past its own validity. Missing, unreadable, oversized,
malformed, unsynchronized or out-of-bound-offset evidence is never cached and fails
closed on that check; stale or future evidence is rejected on every check, and its
replacement is seen at once when the file identity changes, otherwise within one
second. The source processor's turn no longer repeats the worker loop's
check. HTTP mutation and ingress checks still read the files on each request until
they opt in. Section 5 of the Kafka pipeline specification is unchanged. Original
issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## Batched changed-consumer commits — 2026-10-22

**Assistant-selected (performance item #7).** The correlation and search changed
consumers no longer commit the broker offset and write `kafka_consumer_positions`
after every input. A handled input's offset is committed only after its handler's
durable writes complete (the correlation PostgreSQL transaction; the search
Elasticsearch bulk acknowledgement), so the committed offset never runs ahead of
durable state. The broker commit is batched to the next consumer turn after 100
handled inputs or 100 milliseconds; it is not a hard time bound, because a long
handler or a search reconciliation page between turns delays it. Pending offsets are
also flushed before a revocation, after a failed input (its offset stays uncommitted)
and on shutdown. Positions remain diagnostics and are written in
one statement after each broker commit. Partitions reported lost belong to a fenced
generation: their uncommitted progress is dropped without a commit and the next owner
replays from the committed offset. Replay after a crash between the PostgreSQL and
offset commits is idempotent: correlation recognizes `kafka_correlation_events`
under the tenant coordinator before any decision. The correlation consumer also reads
the capability gate under the coordinator in its consuming transaction instead of a
separate transaction, still failing the input while the gate is closed (superseded for
correlation by REV-39: the consumer no longer reads a gate). See [Kafka
pipeline section 3](../specs/spec-kafka-alert-pipeline.md#3-kafka-keys-fencing-and-two-independent-commits).
The PostgreSQL-before-Kafka replay protocol, original issue IDs and REV numbering are
unchanged. Executed evidence belongs in delivery.

## HTTP checks reuse clock-health evidence — 2026-10-22

**Assistant-selected (performance item #19).** This supersedes the sentence in
"Clock-health evidence reuse" saying that HTTP mutation and ingress checks still
read the files on each request. Each HTTP application now keeps one evidence cache,
and its ingress and mutation checks use it under the same rules as the worker loop.
The check stays off the event loop, because every call still stats the file. A
fresh cache hit therefore still runs in a worker thread. One behaviour changes: an
in-place rewrite to unhealthy evidence that a coarse file timestamp leaves with the
same identity now fails ingress and mutations up to one second later than before.
Atomic replacement is still seen on the next request. Age is still judged on every
request, so evidence is never accepted past its 60-second validity. Missing,
unreadable, malformed, unsynchronized or out-of-bound evidence still fails closed on
that request. Original issue IDs and REV numbering are unchanged. Executed evidence
belongs in delivery.

## Idle reconciliation waits for due work — 2026-10-22

**Assistant-selected (performance item #15).** The search indexer's reconciliation
no longer takes a physical-index writer lease, inserts missing reconciliation rows
and runs a claim transaction on every worker turn. It first reads, in one
read-only statement, whether the search gate is open, whether any view state lacks
a reconciliation row, and the earliest time a tenant matches the unchanged claim
predicate (unfinished or audit pass, two seconds after a completed pass, claim
expiry, `retry_after`). When nothing is due it issues no statement until that time,
rechecking at least once a second so new tenants, rebuild epochs and gate changes
are seen within a second. Due work keeps the existing writer lease, per-tenant
30-second claims, ownership rechecks, audit selection and failure backoff, so
paused or rebound writers remain fenced. Kafka hints keep the consumer's bounded
poll on every loop. Without a Kafka transport, the shared worker loop waits until
the scan's next due time, bounded to one second, instead of 10 milliseconds. The
two-second pass spacing of [Kafka pipeline section 6](../specs/spec-kafka-alert-pipeline.md#6-search-reconciliation-progress-and-rebuild)
is unchanged; REV-34–36 worker scope is unchanged and no sweep or polling worker is
added. Original issue IDs and REV numbering are unchanged. Executed evidence belongs
in delivery.

## Search hints share one bulk across partitions — 2026-10-22

**Assistant-selected (performance item #11).** The search indexer no longer indexes
at most 50 changed hints from a single partition per turn, each behind its own
refresh wait. A turn passes the first pending group of every busy partition, at most
500 hints in all, to one projection request; identities are deduplicated and the
projection writer's unchanged 500-document and 4 MiB limits and `refresh=wait_for`
visibility proof apply to that one bulk. Each partition then records only its own
covered prefix, and offsets are still committed only after the bulk acknowledgement
and visibility check, in one broker commit that carries every advanced partition's
offset. If the shared request fails (including a partially failed bulk), nothing
from it is committed; if it fails or does not reach the head partition, that
partition is handled alone through the existing single-partition path, so faults
stay isolated and fenced per partition. After a failed shared request, every
non-head partition it included is left out of shared requests until it has handled
every input it had in that request alone (or was fenced, revoked or lost), and no
shared request is made while such a partition is the head. Per-partition order,
lost and revoked partition fencing and `external_gte` idempotency are unchanged.
Authority scans keep 50-identity pages. Correlation keeps its 50-input default and single-partition
turns. See [Kafka pipeline section 6](../specs/spec-kafka-alert-pipeline.md#6-search-reconciliation-progress-and-rebuild).
Original issue IDs and REV numbering are unchanged. Executed evidence belongs in
delivery.

## Live invalidation merge window — 2026-10-22

**Assistant-selected (performance item #22), at the user's request to lengthen the
window.** The browser merged live `invalidate` changes for a fixed 250 milliseconds,
and each merged change reloaded the visible feed (a new search snapshot) and then
the quick-view counts, so a tenant with steady changes reloaded about four times a
second per open tab. [Technical baseline section 19](../specs/spec-alert-history-technical.md#19-browser-refresh-reconnect-and-relative-time)
now selects a trailing window: refresh once changes have been quiet for 500
milliseconds, and at most one second after the first change not yet refreshed.
Dashboard count panels use the same window ([dashboard section 12](../specs/spec-dashboard-operations.md#12-count-caching-and-load-control)).

Under normal traffic (about 66.7 deliveries a second, possibly all in Global) an open
tab rarely sees 500 milliseconds of quiet, so the one-second cap governs. The window
cuts reloads from about four to about one per second per tab. The browser adds a
delay of up to one second, spread over 0 to 1 second, instead of 0 to 250
milliseconds. Using the additive framing as a rough guide, the five-second
incoming/maintenance visibility p99 then leaves about two seconds after this one
second and the two-second p99 feed request. Those two seconds cover admission (its own
one-second p99), the source turn, the indexer's wait for a search refresh, the Redis
hint, SSE delivery and rendering. This is tighter than the 250 milliseconds it
replaces and is a **known qualification risk**: the end-to-end p99 must be measured,
and the cap should be lowered if it is the margin that fails. A two-second cap was
considered and rejected because it would leave about one second.

The user's own command is reloaded at once, but search reflects it only after the
indexer's hint. For five seconds after a command this tab committed, or whose
outcome is unknown, changes for that tenant merge for only 250 milliseconds, as
before. A merge pending at that moment is shortened too, so the command's projected
result is not held back. This does not yet apply command responses to visible rows
or show search updating until the response's projection sequence is covered
(section 22); that remains outstanding.

Unchanged: reconnect, return to a visible tab and the user's own refresh reload
immediately (and drop the pending merge); hidden tabs schedule nothing; one request
in flight per visible resource with one pending refresh; the two-second disconnected
polling and SSE reconnect policy. It complements performance item #12, which stops
idle reconciliation passes from producing invalidations. Original issue IDs and REV
numbering are unchanged. Executed evidence belongs in delivery.

## Current scope notes — 2026-10-24

The user asked for section-level marking of later scope decisions. Specifications
state the REV-33 to REV-37 corrections in their preambles while the superseded text
stays in section bodies, so a reader who opens a section directly can take deferred
behavior as current. Assistant-selected presentation: a one-sentence **Current
scope** note directly under each affected heading names the decision, links the
governing section and says what remains normative. Headings, anchors, issue IDs,
REV numbering and the original text are unchanged; catalog sections still resolve.
The preset and dashboard preambles gain the REV-34 correction their retention
sections already depended on. The incident detail note records that stored
inactivity and retention deadlines are not presented as upcoming automatic actions,
matching the 2026-10-24 label removal. These are navigation and presentation
choices, not changes to product requirements.

## REV-39 — Always-on correlation and maintenance (2026-10-24)

User decisions: correlation rules and maintenance windows are always on in every
environment, with no feature-level capability gate; per-rule and per-window
Enable/Disable intent stays. Capacity limits are configurable numbers, and a limit
that is not configured is unlimited. A database restore no longer turns correlation
or maintenance off; the `human_auth`, `search`, `v2_ingress`, `recovery` and
`audit_retention` gates still close on restore as before. The user stated that the
single local stack on this workstation is the only environment, so no compatibility
shims are needed and its local data may be fixed directly.

Assistant-selected details:

- Migration 0053 deletes the `correlation` and `maintenance` capability-gate rows. It
  restarts rules stored `blocked` with `consumer_not_integrated` like a re-enable: a
  new evaluation epoch, `last_reset_reason='always_on'`, a boundary at migration time
  and a fresh tenant admission order, so changed events queued while the gate was
  closed never count. Pre-0053 code reads those rows; stop every writer before
  applying it.
- No code reads those gates. The maintenance activation command, the REV-30 local
  correlation preview and its profile flags (`correlation_preview`,
  `scope: local-development`, `allow_local_preview`) are removed. Correlation and
  maintenance budgets no longer need `qualified`. The API startup rule refusing an
  unqualified capacity profile outside `development` is unchanged; it also covers
  ingestion and search budgets.
- The domain helper `keep.shared.capacity` defines `UNLIMITED` as 2^53−1
  (9,007,199,254,740,991), safe for PostgreSQL `LIMIT budget+1` and JSON. A missing
  or null budget is unlimited; a configured value must be an integer from 1 to
  `UNLIMITED`, otherwise the operation fails with `capacity_profile_invalid` (503).
  This covers the correlation budgets for enabled rules, live groups and evidence,
  condition/rule/tenant cost and digest bucket, the three top-level maintenance
  work/input/segment budgets and `maintenance.max_overlap`/`max_work_bytes`. An
  optional `correlation.cost_model` must equal the CEL cost model
  (`correlation_cost_model_mismatch`). The development profile sets none of them.
- Maintenance always prepares its catalog (`maintenance_catalog_required` when a
  caller supplies none); there is no closed-gate write path. Alert reads keep the
  strict rule: no current maintenance checkpoint fails with
  `maintenance_proof_unavailable`. Alerts journaled before the upgrade are covered by
  running the existing maintenance warmup once per tenant; alerts without a creation
  baseline are reported to the user and then removed from the local data.
- Correlation rules are created `healthy`; the correlation consumer checks no gate;
  the API no longer returns `processing_ready`.
- Maintenance window deletion still requires the `recovery` and `human_auth` gates and
  the recovery evidence store, so it stays unavailable until protected recovery
  exists. Create, edit, enable and disable work.
- The local launcher always starts the correlation worker. Earlier load-test
  baselines were measured with correlation and maintenance off and do not describe
  the always-on default.
- The disposable CEL compile process is started as a plain subprocess that imports
  only `keep.cel.compiler`. A spawned multiprocessing child re-imported the
  calling service's entrypoint first (about 1.2 s for the processor and correlation
  workers here), so every compile in those workers exceeded the unchanged
  one-second deadline once maintenance windows were always compiled. Request,
  reply, deadline and sanitized failure logging are unchanged.

For correlation and maintenance this supersedes decision 23 and the local-preview
entry in [design decisions](design-decisions-2026-09-22.md), REV-30, REV-10's
closed-gate statement, the gate check in "Batched changed-consumer commits" and the
missing-profile and no-unlimited-quota rules of
[system completion section 23](../specs/spec-system-completion.md#23-measured-capacity-profile-and-readiness-rules).
See also [correlation section 20](../specs/spec-correlation-rules.md#20-high-cardinality-and-resource-limits-c4-n1)
and [maintenance section 17](../specs/spec-maintenance-operations.md#17-failure-capacity-and-recovery-behavior).
Measured capacity remains a qualification output. Original issue IDs and REV
numbering are unchanged. Executed evidence belongs in delivery.

## REV-40 — Reviewed reset after lost local Kafka storage (2026-10-25)

User decision: approve the local recovery plan of 2026-10-25 and re-enable the only
enabled correlation rule afterwards so it starts a fresh epoch. The local Kafka broker
kept its log in the container layer, so recreating the container on 2026-10-05 lost
both application topics. The launcher recreated them empty, their offsets restarted
under PostgreSQL replay proof, and the source stopped on a reused coordinate. This is
the [reviewed reset](../specs/spec-kafka-alert-pipeline.md#8-cutover-retention-and-diagnostics)
that section 8 requires for a loss interval.

Assistant-selected details:

- Stale coordinates are retired, never deleted: source-result rows from the lost topic
  incarnation keep delivery UUID, digest, first offset, alert and changed-event
  identity, and only their `topic` becomes `<topic>@lost-<date>`. This frees
  `UNIQUE(topic,partition,input_offset)` for the live topic while the section 8
  delivery and first-coordinate fences remain. Rejected: deleting the rows (removes
  fences) and a topic-incarnation column (schema and processor change; open follow-up).
- Diagnostic `kafka_consumer_positions` rows are set to the broker committed offsets;
  broker offsets stay authoritative (section 3).
- Correlation rules whose epoch spans the loss interval are disabled through the
  normal command before the source resumes and re-enabled afterwards, which starts
  a fresh epoch through the audited path.
- Inputs admitted to the lost incarnation after PostgreSQL's last confirmed offset
  are unrecoverable and recorded as such; search is repaired from PostgreSQL by
  authority reconciliation.
- The local launcher refuses to create application topics after the recorded cutover
  and refuses to start workers when the broker ends below, or holds another delivery
  at, an offset PostgreSQL recorded.

Detection inside the processor (recording the topic identity at cutover and a
specific coordinate-conflict fault) followed in [REV-41](#rev-41--kafka-topic-incarnation-detection-in-the-source-2026-10-26).
Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-41 — Kafka topic incarnation detection in the source (2026-10-26)

Follow-up to REV-40, requested so that environments without the local launcher also
refuse a recreated topic. Assistant-selected details, recorded in
[Kafka pipeline section 8](../specs/spec-kafka-alert-pipeline.md#8-cutover-retention-and-diagnostics):

- Migration 0054 adds nullable `received_topic_id` and `changed_topic_id` to
  `kafka_pipeline_control`, in Kafka's 22-character topic ID text. Cutover records
  both. The source verifies the received topic on every assignment and refuses a
  different or unrecorded ID before any producer, offset or input is used. The fault
  is `source_topic_identity_changed` per assigned partition at its committed offset.
- confluent-kafka 2.15.1 passes each 64-bit half of a topic ID through a C `long`,
  which is 32 bits on Windows, where every local worker runs. IDs are compared by the
  low 32 bits of each half, which every client reports correctly; on Linux the stored
  text equals `kafka-topics.sh` output. Rejected: a content check of the last recorded
  coordinate on every assignment (a record fetch per partition during rebalance) and
  checking only on full-width clients (no protection in the only environment).
- A source-result insert that violates `UNIQUE(topic,partition,input_offset)` is
  `source_coordinate_conflict`. The tenant coordinator and READ COMMITTED make the same
  delivery a replay first, so the violation means another delivery holds the
  coordinate. The partition is fenced with no retry deadline; the conflict is detected
  from the constraint, with no extra statement per input.
- Every retained source failure logs partition, offset, reason, exception class and the
  AppError code or SQLSTATE, in the message itself because no log handler is
  configured. Exception text is never logged.
- `python -m keep.kafka_cutover --record-topic-identity` records the IDs for a
  cutover from before 0054 and as the last step of a reviewed reset. It requires
  stopped pipeline groups and refuses (`kafka_topic_history_mismatch`) unless each
  partition ends at or beyond PostgreSQL's recorded positions and last source result
  and still holds that result's input digest. It never commits offsets.
- Open: the correlation and search groups do not verify the changed topic's identity;
  their replay is idempotent by event identity or external version, while source
  coordinates are replay proof.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-42 — Ocean palette on the existing design (2026-10-26)

User decision after a full visual redesign round for the frontend. The user rejected two
hands of bold directions, said the existing interface was the best so far because it is
simple and easy on the eye, and asked for a real color palette rather than black and
white. Five calmer palette prototypes were built on separate local frontend branches.
After comparing them, the user kept the existing design and replaced only its colors
with the Ocean palette, in light and dark.

- Supersedes the color part of REV-12 (warm off-white backgrounds, warm gray rail, dark
  primary actions) and the light palette REV-20 retains as default. Layout, the
  76-pixel rail, Geist type, components, copy, behavior and the REV-20/REV-24 light
  default with a persisted dark choice are unchanged. The REV-23 Keycloak theme uses
  the same palette.
- Assistant-selected details: every color is defined once per theme as a semantic
  role; Ocean blue marks primary actions, the active rail item and selection; status
  and severity keep their red, orange, amber and green meanings; text, placeholders
  included, meets 4.5:1; selection, caret, scrollbars, focus rings and native control
  accents follow the palette; shadows are navy-tinted. The values are recorded in the
  [UI mapping](https://github.com/keep-alert-operations/keep-frontend/blob/main/docs/ui-design.md).
- The four unchosen prototypes and Ocean's own structural changes (labelled sidebar,
  Mulish type, firing-dot halo) are not adopted; their branches stay local until the
  user decides.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-43 — Quieter alert, preset and dashboard screens (2026-10-26)

User decision. The user listed changes that make the Feed, saved presets and dashboards
easier on the eye, answered the open questions, and approved the result in a
[UI cleanup mock](https://claude.ai/artifact/7vm914Lhop6uEBDoTw37Sz) before implementation.

- **Row menu.** On Feed and saved-preset rows the ⋯ button opens a menu with Assign to
  me or Unassign, and Resolve or Reopen, instead of navigating to the alert. The inline
  Assign to me and Resolve buttons move into it; the message still opens the alert. The
  detail page keeps its single Assign control ([alert operations 17](../specs/spec-alert-operations.md#17-assignment-and-derived-acknowledgement)).
- **Live status.** The standing Live pill leaves the page header of every screen. This
  supersedes "scoped update status remains visible" in [shared system section 3](../specs/spec-system-completion.md#3-navigation-and-visual-system).
  Lost live delivery still shows a quiet notice with Refresh, as [preset section 14](../specs/spec-preset-operations.md#14-open-views-live-changes-and-access-changes)
  and [technical baseline section 19](../specs/spec-alert-history-technical.md#19-browser-refresh-reconnect-and-relative-time)
  require, and lagging search shows "Catching up · counts may lag". The saved-preset
  footer drops its "updates live on page 1" text. Assistant-selected: the brief
  Connecting and Reconciling steps show nothing, and below 1024 pixels, where the
  header wraps, the routine catching-up notice is announced to assistive technology
  but not drawn, so it never moves content; degraded notices stay visible and wrap.
- **Revision numbers.** Removed from the saved-preset subtitle and the dashboard
  subtitle (each whole line goes, including its editor, time and panel count; the
  dashboard's Unsaved changes chip moves beside the name), the presets list's Revision
  column, the dashboard list cards, the alert detail's Details panel and the dashboard's
  newer-version notice, which now says "A newer shared version is available" without
  numbers. This narrows the [dashboard section 8](../specs/spec-dashboard-operations.md#8-shared-editing-copying-and-conflicts)
  wording that a dirty board "shows the newer shared revision" and shared system section
  4's "display their base revision" for that notice. Revision-based commands and
  conflicts, history pages and comparisons, and note revision history are unchanged.
- **Quick views.** The user chose the lighter quiet-text style: smaller borderless
  buttons, light counts, and a coloured dot for each severity and status view. The
  Active view, which showed Firing and Acknowledged together, is removed. "Quick views
  are not saved" moves into the group's tooltip and accessible name.
- **Alert rows.** Feed and saved-preset rows show severity and status as coloured text
  without their shape marks; the detail page and other lists keep the marks. The source
  line under the message (application · component · node · site) is removed from these
  rows and from the alert detail summary; the Details panel still lists those fields.
  The New chip is removed.
- **Relative times.** Feed and preset rows, the saved-preset "evaluated" footer, the
  presets list, the dashboard list cards, stale dashboard panel captions and the alert
  detail (its fields, history, notes, occurrences, source events and note revisions)
  show time relative to now, such as "30 seconds ago", "2 hours ago" or "3 days ago".
  This narrows, for those screens, the [shared system section 3](../specs/spec-system-completion.md#3-navigation-and-visual-system)
  rule to show the selected date format and timezone labels. Assistant-selected
  details: English wording with "just now" under five seconds; one shared display clock
  that updates every five seconds while the tab is visible and requests no data; the
  exact time, in the selected format with the browser timezone label, stays in the
  tooltip, so the separate "Times in" labels go. Incidents, rules, maintenance, audit
  and history screens keep exact times.
- The Dashboards list remains its own page, reached from the rail; the mock's combined
  board was only a layout shortcut.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-44 — Group alert results by one field (2026-10-26)

User decision. The user asked to group alerts by a field on the Feed and saved-preset
pages, with each group shown as a mini table. They approved the
[alert grouping mock](https://claude.ai/artifact/FhJsfdk4VB7kAXkjBfx9Dm) and the
implementation plan, and chose most-alerts-first ordering with a 1,000-value cap.

- **Control and fields.** A Group by button on the quick-view row offers No grouping,
  Severity, Status (`display_status`), Application, Component, Node (`node_name`),
  Site, Assignee (`assignee_id`) and Incident (`active_incident_id`). Times, the
  message, the operator and the other columns are not offered.
- **Groups.** Each value gets its own table: a collapse toggle, the value, an exact
  alert count and a summary (status counts for severity groups, severity counts
  otherwise), its own column headings and select-all for its shown rows. The grouped
  column is hidden inside groups and rows follow the current sort. Five rows show,
  then Show 5 more; ten groups show, then Show 10 more groups; Collapse all and Expand
  all act on the shown groups. These choices are transient tab state.
- **Order.** Severity groups run critical, high, warning, clear; Status groups run
  Firing, Acknowledged, Resolved; other fields put the most alerts first, then the
  value in Unicode scalar order. Alerts without a value form the last group, labelled
  Unassigned, No incident or No value. Above 1,000 distinct values the request returns
  `too_many_groups` and the page keeps its single table with that explanation.
- **Feed.** Grouping is transient like the rest of the ad-hoc feed. Save as preset
  carries it into the new preset draft.
- **Presets.** `group_by` becomes an optional fifth saved definition field (null means
  no grouping), set in the editor under Sort, with revisions, no-ops and history like
  sort and columns. The results toolbar can change it for the current view only, with
  Reset to saved; a new revision or reopening clears that change, like the temporary
  sort ([preset section 4](../specs/spec-preset-operations.md#4-columns-and-sorting)).
  Dashboards count presets as before, and drill-through opens grouped results.
- **Search (assistant-selected).** Exact group counts come from one composite
  aggregation on the rows' point-in-time snapshot. Status groups use the compiled
  `display_status` predicates, so no mapping change, script or index rebuild is
  needed. The first rows of the shown groups come from one batched search on that
  snapshot, and continuation cursors bind the group
  ([technical baseline section 17](../specs/spec-alert-history-technical.md#17-search-snapshots-counts-and-purged-ids)).
  A grouped view refreshes on invalidations like a first page while only first rows
  and groups are shown, with one grouped request plus one quick-count request.
- **Compatibility (assistant-selected).** An omitted `group_by` in create or replace
  means null, and a null value is left out of command fingerprints so retries of
  commands sent before the upgrade still match. The column is additive; an older API
  leaves it unchanged. During a frontend rollback, saving from the older screens
  clears a preset's grouping.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-45 — Assigned to me, quick-view toggle and a shorter Reset (2026-10-27)

User decision. The user asked for a quick filter for alerts assigned to them, for
pressing a selected quick view again to return to All, and for the grouping toolbar's
Reset to saved button to read just Reset.

- **Assigned to me.** A quick view after the status views, past a divider, narrows the
  Feed, saved-preset results and the preset editor preview to `assignee_id` equal to
  the signed-in principal's ID. Like the other quick views it is transient and
  single-choice, shows an exact count, composes with the applied CEL, text search and
  Include suppressed, and is never saved
  ([alert operations, Product API and screens](../specs/spec-alert-operations.md#product-api-and-screens)).
  Assistant-selected: it carries no coloured dot, since REV-43's dots mark severity and
  status, and the principal ID enters the CEL as an escaped string literal. The
  quick-count batch gains one query, within its 24-query limit.
- **Toggle.** Pressing the selected quick view again selects All, on the Feed,
  saved-preset results and the preset editor preview; pressing All keeps All. Other
  view choices behave as before.
- **Reset.** On saved-preset results, the button that returns a temporary grouping
  change to the saved field reads Reset, with "Back to the saved grouping" as its
  tooltip. Behaviour is unchanged
  ([preset section 4](../specs/spec-preset-operations.md#4-columns-and-sorting)).

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-46 — Resolve an incident when all its linked alerts resolve (2026-10-27)

User decision. The user asked that an incident resolve when all of its linked alerts
are resolved. This reverses the earlier rule that incidents never resolve automatically
merely because every linked alert resolved
([incident operations](../specs/spec-incident-operations.md#4-lifecycle-cycles-and-timestamps-i2)).

- **Trigger.** An accepted firing-to-resolved transition of a currently linked alert
  (source, manual single or bulk command, or the deferred source-inactivity expiry)
  resolves each active incident it is linked to whose retained linked alerts are then
  all resolved. Suppression and acknowledgement do not matter; status alone decides.
- **Effects.** Resolution happens in the same transaction as the alert transition, at
  that transaction's decision time, with system actor and cause `alerts_resolved`. It
  applies the same effects as manual resolution: correlation-context reset, ownership
  release, per-alert fresh-transition boundaries, a 90-day retention deadline, an
  `alerts-resolved` incident activity record and an `incident-alerts-resolved` alert
  history entry. Alert statuses are unchanged.
- **Assistant-selected boundaries.** Only an alert transition triggers it: unlinking or
  moving the last firing alert away, linking resolved alerts, creating an incident from
  resolved alerts and empty incidents leave the incident active. Unavailable (purged)
  references are ignored, and an incident with only unavailable references stays
  active. A later re-firing alert does not reopen the incident; it is unowned and
  follows the normal correlation and reopening rules. A bulk command resolves
  incidents after all its selected alerts are applied. `cause` remains free text, so
  no migration or HTTP contract change is needed.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-47 — Preset editor settings in tabs beside the preview (2026-10-28)

User decision. The user found the preset create/update screen overloaded: every setting
was stacked in one Definition panel beside the preview, the column list and sort rows
were fiddly, and the filter area was noisy. From four mock directions the user chose
option D of the [preset editor options canvas](https://claude.ai/artifact/CkERUg32kLwT2AuWdzSJML):
keep the preview, and move the settings into a separate panel with tabs. The user kept
the Validate CEL button.

- **Layout.** The preview panel holds the draft status line, the quick views (Assigned to
  me included, REV-45), Include suppressed and the results table. A Preset settings
  panel beside it holds Name above four tabs, Filter, Columns, Sort and Group by, and
  "Changes apply to everyone" at its foot. The newer-revision notice and save feedback
  stay above both panels. Saved fields, defaults, validation, preview behaviour and
  the Save, Save as new and Discard actions are unchanged
  ([preset sections 3–9](../specs/spec-preset-operations.md#3-saved-definition-and-initial-defaults)).
- **Assistant-selected details.** Filter opens first each time; all tab panels stay
  mounted, so switching keeps the filter text, caret and validation. Tabs follow the
  standard keyboard pattern. A tab shows a problem marker: Filter when the preview or
  validation reports the filter invalid, Columns when none is chosen. A save rejected
  for its filter switches to Filter and focuses the editor; Name stays outside the
  tabs, so an empty name is always in view. The Insert field chips, the supported
  fields and functions reference and the byte count move into one Supported fields
  and functions popover in the Filter tab. Columns are an ordered list that can be
  dragged, with Move up and Move down shown on hover and keyboard focus, plus an Add
  columns checklist of the remaining columns that appends a ticked one. Group by is a
  list of radio buttons. Below 1024 pixels, where the panels stack, the settings panel
  sits above the preview. No "quick views are not saved" text is added; it stays in
  the quick views' tooltip (REV-43).

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-48 — Link an alert to an incident from the alert (2026-10-28)

User decision. The user wanted to link an alert to an incident from the alert itself,
not only from the incident's Link alerts dialog: a Link action on the alert page and in
the alert row's ⋯ menu on the Feed. Membership rules, limits and commands are unchanged
([incident operations 5–6](../specs/spec-incident-operations.md#5-linking-and-unlinking-i3)).

- **Entry points.** The alert page shows Link to incident… beside Assign…; Feed and
  preset result rows show Link to incident… after Assign and Resolve in their ⋯ menu.
  Users with view access see neither, as with the other alert actions.
- **Assistant-selected details.** Both open one dialog that lists active incidents
  (search by text, 50 at a time) with severity, title and status; one is chosen with a
  radio button and linked with the existing link command at that incident's revision.
  When another active incident already owns the alert, the dialog says so, marks that
  incident Linked here and not selectable, and the action becomes Move to incident,
  using the existing explicit move with both incident revisions; ordinary Link never
  takes the alert. Conflicts, stale revisions and uncertain outcomes use the shared
  command messages and retry. A success closes the dialog and refreshes the page or
  results. The action is for one alert; bulk linking from a selection is not added.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-49 — Dismiss an alert for a time window (2026-10-28)

User decision. The user wanted to dismiss an alert for some minutes or hours, or until a
chosen date, after which it returns on its own. From the
[dismiss mock canvas](https://claude.ai/artifact/Nvp1SJzsc29Y1HYSnfcK99) the user
approved a Dismiss… action in the alert row's ⋯ menu and on the alert page, and decided
that a dismissed alert is suppressed rather than a status of its own
([alert operations 29](../specs/spec-alert-operations.md#29-timed-dismissal-rev-49)).

- **Behaviour.** Editors dismiss one firing alert for a duration (15 minutes up to
  1 week presets, or a custom number of minutes, hours or days) or until a date and
  time, at most 30 days ahead, with an optional reason that is added as a note. While
  dismissed the alert is suppressed: Include suppressed covers it, rows show their
  ordinary status with a "Suppressed · until …" indicator, and correlation ignores it.
  Change dismissal replaces the end time and Undismiss ends it at once. A new
  occurrence ends it early; resolving alone does not. Assignment, incident links and
  notes are unchanged.
- **Return after the time passes (user decision, 2026-10-28).** The end time is checked
  against the authoritative clock on every read, so the alert stops being suppressed
  exactly at the end time without a scheduler. This is a deliberate exception for
  dismissal only: maintenance suppression still needs a source update to release
  (REV-34). The first source update after the end time may supply fresh correlation
  evidence, as an ended maintenance window does; time passing, Undismiss and Change
  never do.
- **Assistant-selected details.** The dismissal is a separate cause stored on the alert
  row; the stored `suppressed` flag keeps meaning the source and maintenance causes, so
  maintenance proofs are unchanged. The next source update or alert command after the
  end time records Dismissal ended with the system actor at the end time; until then
  reads report the dismissal as expired. Feed and count responses report the next end
  time among matching rows so a page refreshes when an alert returns. Durations are
  measured from the server clock. Dismissal is one alert at a time; bulk dismissal is
  not added. The command stays disabled until every writer runs this release.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-50 — Free panel width and height, sized on the grid only (2026-10-28)

User decision. The user asked to remove the Width and Height settings from the panel
create/edit dialog, remove the panel's maximum height, and let a panel's width grow one
column at a time up to the full width of the page
([dashboard operations 4](../specs/spec-dashboard-operations.md#4-layout-and-responsive-behavior)).

- **Rules.** Width is any whole number of columns from 3 to 12, still with x+w <= 12.
  Height is any whole number of grid units from 2, bounded only by the existing grid
  limit y+h <= 100. Overlap, compaction, 24-panel and save rules are unchanged; layouts
  saved under the old sizes remain valid.
- **Assistant-selected details.** The minimums stay at the earlier smallest sizes, 3 by 2,
  which is also the default for a new panel. Pointer resizing snaps to the nearest whole
  column and unit; keyboard resizing on the corner handle steps by one. The Product API
  contract replaces the width and height enums with integer ranges, and migration 0057
  widens the matching `dashboard_panels` checks; it runs before the API that accepts
  the new sizes. Below 1,024 pixels
  the move and resize handles stay hidden, so panel size can no longer be changed in the
  stacked responsive layout; the desktop layout is unaffected there.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-51 — Plainer alert actions and a steadier dismiss dialog (2026-10-29)

User decision. After trying REV-49 locally the user asked to drop the trailing "…" from
Dismiss, Link to incident and Assign in the alert row's ⋯ menu and on the alert page,
to give every alert-page action an icon like Dismiss, to stop the dismiss dialog from
reporting an error as soon as the custom number is chosen, and to keep that dialog one
size ([alert operations 29](../specs/spec-alert-operations.md#29-timed-dismissal-rev-49)).

- **Labels.** The row menu reads Assign to me, Resolve, Link to incident and Dismiss, or
  Change dismissal and Undismiss on a dismissed row. The alert page reads View alert,
  Resolve alert, Dismiss, Assign, Link to incident and Open runbook; the dismissal band
  reads Change and Undismiss. Bulk actions and incident pages keep their labels.
- **Icons.** Each of those alert-page buttons shows a small line icon before its label,
  drawn in the existing icon style; Open runbook's icon replaces its arrow character.
- **Assistant-selected details.** Choosing the empty custom field keeps it highlighted
  and shows "Enter how many minutes, hours or days to dismiss it for." without an error
  or red border, and Dismiss stays disabled; a typed value that is not a whole number
  above zero, or over 30 days, still shows the error. Both modes and the longest summary
  share fixed grid cells, so switching modes, messages or a command error never resizes
  the dialog at any width.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-52 — One field to search and choose a panel's preset (2026-10-29)

User decision. The user asked to merge the panel create/edit dialog's Search presets
box and its Saved preset list into one input
([dashboard operations 8](../specs/spec-dashboard-operations.md#8-shared-editing-copying-and-conflicts)).

- **Field.** Saved preset is a single text field. Typing searches shared presets by
  name, as the separate box did, and shows the loaded page as a list below the field;
  clicking a row, or Enter on the highlighted row, chooses it and the field shows its
  name. After trying it the user asked that the list overlay the dialog rather than
  grow it, and that the field show it is a dropdown: the list floats over the dialog
  and a chevron at the field's end opens and closes it. First page, Next page, the
  loaded count and Retry loading presets sit at the bottom of the open list.
- **Assistant-selected details.** The list opens on click, the chevron, typing or the
  arrow keys, not when the dialog first focuses the field. Escape closes only the list and keeps
  the dialog open; a second Escape closes the dialog as before. Leaving the field
  without choosing restores the chosen preset's name and keeps the last search's
  results. Focusing the field selects its text so typing starts a new search. The
  chosen preset is shown in bold in the list. Search, paging and the selected
  reference that stays available across pages are unchanged.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-53 — Incident reports by period (2026-10-30)

User decision. Add a Reports page to the rail with an incident report for one tenant and
a chosen period, as in the [incident reports mock](https://claude.ai/artifact/NxBWGUChKyvq1CnRJmxoky)
([incident operations 20](../specs/spec-incident-operations.md#20-incident-reports-i5-n3-rev-53)).
The user chose option A and the incident report only; noise reports are left for later
(user decision, 2026-10-30).

- **Location and access (user decision, 2026-10-29).** A Reports rail item after
  Dashboards; every tenant reader (view, edit, admin) can open it, including the
  breakdown by assignee.
- **Periods (user decision, 2026-10-29).** 24 hours, 7, 30 and 90 days and a custom date
  range, compared with the previous period of the same length.
- **First response (user decision, 2026-10-29).** Time from a cycle opening to its first
  assignment or first move to Investigating within that cycle, whichever comes first.
- **Breakdowns (user decisions, 2026-10-29 and 2026-10-30).** Severity, origin,
  correlation rule and assignee, in one panel with a switcher.
- **Links and deleted rules (user decision, 2026-10-30).** With the plan the user approved
  two proposals. A breakdown row links to the Incidents list filtered by that group and
  by created time; the list's counts can differ, because it filters by creation and
  current assignee. A deleted rule shows its last name tagged Deleted while its history
  is retained, and "Deleted rule" otherwise.
- **Assistant-selected details.** Figures count lifecycle cycles, so reopenings count as
  opened; 24 hours is rolling and the other periods are calendar days in the viewer's
  zone including today; reports reach back at most 90 days, the retention horizon, and
  compare only when the previous period is within it; an assignee carried over a
  reopening is not a response in the new cycle; the assignee of a resolved cycle is the
  one at resolution; figures are computed at read time in PostgreSQL with no worker,
  cache or stored counter; assignment history that cannot be read within its time
  budget leaves first response and the assignee breakdown unavailable rather than
  failing the report; the report refreshes only on request; there is no feature flag.
  Migration 0058 indexes incident cycles by tenant and opened or resolved time and
  assignment activity by incident; it runs in the stopped-writer migration window
  before the API, which stays correct but slower without it.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-54 — Optional alert name on native v2 (2026-10-31)

User decision. Native v2 alerts accept an optional `name`, and Grafana alerts take the
alert rule name ([alert operations field inventory, 3, 5, 7 and 24](../specs/spec-alert-operations.md#native-field-inventory);
[operator operations 18](../specs/spec-operator-operations.md#18-grafana-to-v2-field-mapping)).

- **Default (user decision, 2026-10-31).** An unnamed v2 alert is named by its
  `key_field`, the 64-character identity digest, after the user was told it is not a
  readable value.
- **V1 (user decision, 2026-10-31).** The v1 input schema is unchanged and v1 alerts
  have no name.
- **Title (user decision, 2026-10-31).** The name is the alert's title in the Feed,
  preset and dashboard rows and alert detail, with the message under it.
- **Rules (user decision, 2026-10-31).** The name can be used in Feed and preset search,
  sort and grouping and in correlation and maintenance rules.
- **Identity (user decision, 2026-10-31).** A supplied name is part of the v2 identity,
  so a different name, including a renamed Grafana rule, is a different alert. This
  supersedes the assistant's first proposal to leave it out of the hash.
- **Assistant-selected details.** Unnamed deliveries keep identity format 1 byte for
  byte and named deliveries use format 2 (prefix `alerts:v2:identity:2`, the name
  appended), so no stored key is reinterpreted; the default cannot be a hash input
  because it is the hash. The name follows the identifier rules (at most 256
  characters, no control characters). Grafana's `alertname` label, which Grafana sets
  to the mandatory rule title, is required. Only a supplied name is stored (migration
  0059 adds a nullable `alerts.name` and rewrites no rows); readers resolve the
  effective name, so rows written by older processors during rollout and recorded
  proof read correctly. Maintenance proof omits an absent name, so proof recorded
  before this change stays byte-identical. Free-text `q` matches the name. The
  grouping and sort option is labelled Alert name and the title column Alert. The
  search index needs a rebuild for its new mapping, and ingestion deploys after the
  processor.

## REV-55 — Alert provider and Grafana alert rule URL (2026-10-31)

User decision. Every v1 and v2 alert gains `provider` and `alert_rule_url`
([alert operations field inventory, 3, 7 and 24](../specs/spec-alert-operations.md#3-managed-field-catalog);
[operator operations 18](../specs/spec-operator-operations.md#18-grafana-to-v2-field-mapping);
[alerts technical 6 and 26](../specs/spec-alert-history-technical.md#26-schema-event-and-application-rollout)).

- **Provider (user decision, 2026-10-31).** `provider` is the source that sent the
  alert: `grafana` when it arrived through the Grafana webhook, `api` in every other
  case.
- **Rule URL (user decision, 2026-10-31).** For a Grafana alert, `alert_rule_url` is
  the URL of the alert rule that fired it. Native v1 and v2 senders cannot supply
  one, so `api` alerts have none and both native input schemas are unchanged.
- **Existing alerts (user decision, 2026-10-31).** Alerts stored before this change
  are backfilled from their stored deliveries rather than waiting for the next one.
- **Screens (user decision, 2026-10-31).** Alert detail shows the provider and a link
  to the rule; both fields are searchable, and provider is a Feed and preset column.
- **Assistant-selected details.** The rule URL is Grafana's per-alert `generatorURL`,
  which Grafana documents as the URL of the alert rule. A missing, non-string or
  invalid value (the `runbook_url` rules) leaves it null and still admits the alert,
  because rejecting would turn Grafana alerts accepted today into failures. Both
  fields follow the latest applied delivery like `message`, stay outside the identity
  and semantic revision, and are not maintenance or correlation rule inputs. The
  processor derives them from the received event's existing `adapter_version` and
  retained original bytes, so the Kafka envelope and ingestion code are unchanged.
  Migration 0060 adds nullable columns with checks (`provider` in `api`/`grafana`; a
  rule URL only with `grafana`) and rewrites no rows. The backfill is a one-time,
  rerunnable source processor command that reads each remaining alert's latest
  applied source event and publishes a non-semantic projection change (cause
  `provider-backfill`) under the normal lock order, so no stopped-writer window is
  needed. Readers resolve a missing provider as `api` for v1; a v2 alert reads as no
  provider until the backfill reaches it. The search index needs a rebuild for its
  new mapping.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## Context topics and intents — 2026-11-01

The user approved a redesign of the context navigation so that any request — a
question, a change, an investigation, a review or an operation — reaches the
relevant sources in one step and says what to do with them. Trials on 2026-10-31
showed that change-oriented routes left four of eight natural questions unmatched.
The user decided against a separate knowledge graph; requirement traceability
derived from test docstrings and headings is a later, separately approved phase.

Assistant-selected details, recorded in the [context guide](../context/README.md):
the 23 routes become subject topics with the same IDs, plus `requirements-and-decisions`,
`alert-pipeline`, `reliability` and `local-development`; five intents (`question`,
`change`, `review`, `investigate`, `operate`, unclear requests starting as
`question`) carry steps and a finish line; a generated topic index of at most 40
lines sits in the workspace AGENTS.md; matching uses conservatively stemmed whole
words and caps automatic selection at three topics; unmatched requests list ranked
headings from a `find` command; `plan --content` returns the selected text; and
document-level scope sections carry the verification plan's REV-34/35 corrections
into every partial read of it. No hook, retrieval service or database is added.
These are navigation choices, not changes to product requirements or authorization
boundaries. Original issue IDs and REV numbering are unchanged.

## REV-56 — Link counts on incident list rows (2026-11-01)

User decision. The Incidents list's Linked alerts column showed "—" on every row
because the list returned no link counts; only the detail computed them. Each list
row now carries the same counts as the detail
([incident operations 7, 14 and 16](../specs/spec-incident-operations.md#14-incident-list-and-search-i5);
[system completion 10](../specs/spec-system-completion.md#10-incident-routes-and-aggregate-contracts)).

- **Counts (user decision, 2026-11-01).** `GET /incidents` rows return `total_linked`,
  `suppressed` and `unavailable` as decimal strings, and the column shows the total
  and suppressed subset.
- **Missing maintenance proof (user decision, 2026-11-01).** A row whose retained
  linked alert has no complete maintenance proof returns `suppressed: null` and keeps
  its total; the page never fails for it. The detail keeps its 503
  `maintenance_proof_unavailable`.
- **Assistant-selected details.** One grouped PostgreSQL query per page, inside the
  list's existing repeatable-read transaction, shares the detail's definition, so list
  and detail agree. `maintenance_updating` stays detail-only. The column reads
  "N linked", adding "· M suppressed" and "· K unavailable" only when nonzero. The
  fields are documented on the shared incident response model, an additive OpenAPI
  change. No migration is needed.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## Context catalog fixes — 2026-11-02

The user asked whether the context navigation helps agents as much as it could and
approved four small fixes after a comparison. A retrieval study found that 72 of 261
specification sections belong to no topic and that plans carried procedure text that
questions do not use. A paired trial of a redesign (complete topic coverage plus a
section outline) then scored the same as the current layer (50.5/56 each). Agents
choosing topics by meaning searched the specifications for what plans lacked, so the
topic model stays as it is.

Assistant-selected details, recorded in the [context guide](../context/README.md):
the `delivery` alias "production" is removed because it stems to "product" and pulled
delivery policy into every Product API request; the agent-workflow policies, the
migration guide and the release-artifact runbook list `intents` (`change`, `operate`),
and other intents' plans keep them as pointers without text; `plan --content` emits a
document's preamble and shared sections once; `check` reports the specification
sections no topic reaches without failing on them; and intent inference ignores
failures inside suppositions, lets an opening instruction (with catalog `openers` such
as "plan" and "let") decide before question words, and treats a question sentence as a
question. Navigation choices only; no product requirement, authorization boundary,
issue ID or REV number changes.

## REV-57 — Dashboard panel types and HTML panels (2026-11-03)

User decision. A dashboard panel has a type. Today's preset count panel is type
`count`; a new `html` type shows sanitized HTML written by an editor. More types will
follow, so each type carries its own settings and the panel dialog is built for a
growing list
([dashboard operations 2, 3, 5, 14 and 16](../specs/spec-dashboard-operations.md#2-saved-definition-and-initial-state)).
The user chose the dialog from the canvas at
https://claude.ai/artifact/193U2ejvHGUg2tjpUjWq6k.

- **Types (user decision, 2026-11-03).** `count` keeps its preset reference, custom
  title and thresholds unchanged. `html` has an optional title and HTML content and
  references no preset. A panel sent without `type` is a `count` panel, so existing
  definitions, retained revisions and older clients keep their meaning.
- **Dialog (user decision, 2026-11-03).** Create and Edit panel open one dialog of a
  fixed 1000 × 720 size whatever the type: a Panel type dropdown at the top (icon,
  name and one-line description per type, with a search box), the chosen type's
  settings on the left, a preview at the panel's current size on the right, and the
  draft note with Cancel and Create/Apply at the bottom. Only the middle scrolls. On
  smaller viewports the dialog shrinks to fit the screen.
- **Sanitized HTML (user decision, 2026-11-03, accepting the assistant's proposed
  defaults).** The server sanitizes on every save and stores and returns only the
  sanitized HTML; the browser sanitizes again with the same allowlist before display.
  Allowed elements: `p br strong em b i u s code pre blockquote ul ol li h3 h4 h5 h6
  table thead tbody tr th td a span div hr`. Links allow `http`, `https` and `mailto`
  and always open in a new tab with `rel="noopener noreferrer"`; relative links
  are removed. The `style` attribute
  keeps only `color`, `background-color`, `font-weight`, `font-style`, `text-align`,
  `text-decoration`, `padding*`, `margin*`, `border*` and `border-radius`, with no
  `url()`. Images are not allowed in this release. Content is at most 16,000
  characters after sanitizing. Scripts, event handlers, iframes, forms, other URL
  schemes and every other element or attribute are removed.
- **Assistant-selected details.** A panel keeps its type: saving an existing panel ID
  with another type is rejected with 422 `panel_type_changed`. Storage adds `type` and
  a `content` JSON object for type-specific settings beside the count-only
  `preset_id` and `thresholds` columns, so preset references stay database-enforced;
  HTML panels hold `{"html": …}`. HTML panels are not part of count batches, never
  block preset deletion and do not appear in preset reference lists.
  `POST /dashboards/validate` reports what sanitizing removed, and the dialog warns
  before saving. The panel content area scrolls and uses `contain: content`. An HTML
  panel's accessible name is its title, else "HTML panel". Editors and admins write
  HTML panels, as for every panel. The server sanitizes only after authorizing the
  request, so an unauthenticated body is never parsed; style values also reject CSS
  comments, and a link's own `target` and `rel` are not reported as removals.
  Migration 0062 adds the columns and checks without rewriting rows; it follows
  REV-58's 0061.

This supersedes, for `html` panels only, section 2's rule that every panel references a
preset and section 5's exclusion of arbitrary styling; count panels are unchanged.

**Later user correction — 2026-11-03.** The count preview in the panel dialog showed
"—" until the dashboard was saved. It now counts the chosen preset as soon as it is
picked: the saved query over current alerts without suppressed ones, as a dashboard
counts it, through the existing `POST /alerts/counts`. Thresholds color that count as
they are edited. The 2026-10-09 removal of draft-count requests on the board stands:
unsaved panels on the board still ask to save the dashboard.

**Later user decision — 2026-11-04.** The `style` attribute of an HTML panel also keeps
`font-size`, on the server and in the browser. Assistant-selected: `font-size` follows
the same value rules as the other allowed properties and has no size limit, like
`padding` and `margin`, because the content area scrolls and contains its content, so
a large size affects only that panel.

## REV-58 — Noisy presets that sound an alarm (2026-11-03)

User decision. The user asked for presets that can be noisy: while such a preset is
open and has alerts, the page plays a loud sound meant to wake someone at night. They
approved the generated alarm (a heavy action-trailer track, 27 seconds, looping), the
[noisy preset design mock](https://claude.ai/artifact/9i9edScgrAKBYCxqrECxtF) and its
implementation ([preset sections 3, 8 and 16](../specs/spec-preset-operations.md#3-saved-definition-and-initial-defaults)).

- **Setting (user decision, 2026-11-03).** `noisy` is a saved boolean on the preset
  definition, shared with everyone in the tenant like the other fields. A Sound tab in
  the preset editor, after Group by, holds the Noisy preset switch, a Play sample button
  and three notes on how the alarm behaves.
- **When it sounds (user decision, 2026-11-03).** The results page loops the alarm
  while the preset is noisy and the view's exact total is above zero, the same total
  the page shows. It stops at an exact zero, when the page closes or after a revision
  turns the alarm off. A Noisy marker sits beside the title and in the preset list; an
  Alarm playing banner offers Mute.
- **Banner wording (user decision, 2026-11-03).** The button reads Mute. The playing
  banner no longer says the alarm stops when no alerts match, and the muted banner no
  longer says others still hear it. Both behaviors are unchanged.
- **Blocked sound (user decision, 2026-11-03).** Browsers refuse sound until the page
  receives a user gesture, so a freshly loaded screen shows that the alarm is waiting
  and starts it on the next click on the page. Keep cannot remove this step.
- **Assistant-selected details.** An omitted `noisy` in create or replace means false,
  and false is left out of command fingerprints so retries of earlier commands still
  match, as for `group_by`. Migration 0061 adds `presets.noisy boolean NOT NULL DEFAULT
  false`; older history snapshots without the field read as not noisy. Mute lasts for
  the tab until the preset is reopened or the page reloads and is not stored, because
  preset section 8 keeps personal settings out of browser storage. A loading or failed
  total keeps the previous alarm state instead of counting as zero. Editor previews,
  the Feed and dashboards never sound. The alarm is a static frontend asset with its
  generator script committed beside it, so no API serves audio.

Original issue IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-59 — Incident path on alert details (2026-11-03)

User decision. The user reported that an alert opened from an incident showed Feed as
its path, and asked for the incident instead, as an alert opened from a preset shows
its preset ([incident section 15](../specs/spec-incident-operations.md#15-detail-and-mutation-ux-i3-i5);
[shared navigation](../specs/spec-system-completion.md#3-navigation-and-visual-system)).

- **Path (user decision, 2026-11-03).** The alert detail's breadcrumb shows Incidents
  and the incident title, each linking to its page.
- **Return and stepping (assistant-selected, 2026-11-03).** The rest of REV-25 follows:
  a Back to incident action, and Previous and Next over the visible page of linked
  alerts, skipping unavailable references. The browser-tab alert-list context holds the
  source, so a direct alert link still starts at Feed. No API or stored data changes.

## REV-60 — Panels move on the grid only (2026-11-04)

User decision. The user asked to remove the Move up and Move down actions from
dashboard panels ([dashboard section 4](../specs/spec-dashboard-operations.md#4-layout-and-responsive-behavior)).

- **Menu (user decision, 2026-11-04).** The panel options menu holds Edit panel and
  Delete panel. This supersedes the keyboard Move up/down requirement in section 4.
- **Narrow screens (user decision, 2026-11-04).** The grip stays hidden below 1,024 CSS
  pixels, so panels cannot be rearranged there. The user confirmed this after being
  told those actions were the only way to reorder at that width.
- **Remaining ways to move (assistant-selected, 2026-11-04).** The grip still moves a
  panel by pointer or arrow keys, so keyboard users keep the same reach on the desktop
  grid. Saved layouts, the API and the preset editor's column Move up and Move down
  are unchanged.

## REV-61 — E opens Edit panel (2026-11-09)

User decision. The user asked that pressing E while hovering a dashboard panel open
its Edit panel dialog ([dashboard section 8](../specs/spec-dashboard-operations.md#8-shared-editing-copying-and-conflicts)).

- **Shortcut (user decision, 2026-11-09).** With the pointer over a panel, E opens the
  same Edit panel dialog as the panel options menu. Apply still changes only the draft.
- **Keyboard reach (assistant-selected, 2026-11-09).** When no panel is under the
  pointer, E edits the panel holding focus, such as a focused grip, so keyboard users
  get the same shortcut. The Edit panel menu item shows a muted E and declares
  `aria-keyshortcuts`.
- **When it is ignored (assistant-selected, 2026-11-09).** E does nothing without edit
  access, in fullscreen, with Ctrl, Alt or Meta held, while typing in a field, while a
  dialog or menu is open, during a drag, or while commands are locked, matching when
  the menu item is unavailable.

## REV-62 — Image panels (2026-11-09)

User decision. The user asked for a dashboard panel type that shows an image, either
uploaded or linked by address, and approved the mock at
https://claude.ai/artifact/DBAYiG4UFA3YEtsJec69w2
([dashboard operations 2, 13, 14 and 16](../specs/spec-dashboard-operations.md#2-saved-definition-and-initial-state)).

- **Panel (user decision, 2026-11-09).** `image` is the third panel type after
  `count` and `html`. It has an optional title, an image source, an optional
  description and a fit, references no preset and is never counted. Without a title
  the image fills the whole panel. The source is either an uploaded file or an
  `https` address. Fit is "Show whole image" (`contain`) or "Fill the panel"
  (`cover`, cropping the edges). The panel dialog shows a source switch, a drop area
  or address field, the description, the fit and a live preview; a link that does not
  load in the dialog warns but does not block saving. On the board an image panel
  shows a loading state and, when the image cannot load, "Image unavailable" with an
  Open link for linked images.
- **Storage (user decision, 2026-11-09).** Uploaded files live in PostgreSQL in a new
  tenant-scoped `dashboard_images` table with row-level security. An image is
  immutable and stored once per tenant and SHA-256; panels reference it by ID. No
  object store is introduced.
- **Limits (user decision, 2026-11-09).** PNG, JPEG, GIF and WebP only; no SVG.
  At most 5 MiB (5,242,880 bytes) per file, 8,000 pixels per side and 500 MiB of
  stored images per tenant.
- **File checks (user decision, 2026-11-09).** The server reads each file's own
  header with the standard library to find its real type and dimensions; no image
  library is added and files are not re-encoded. Images are served with the type found
  in the file, `X-Content-Type-Options: nosniff` and
  `Content-Security-Policy: sandbox; default-src 'none'`.
- **Assistant-selected details (2026-11-09).**
  - Wire shape: an image panel carries `image_id` (uploaded) or `url` (linked),
    exactly one, plus `fit` (`contain` default or `cover`) and `alt` (optional,
    single line, at most 300 characters). Addresses are absolute `https` URLs of at
    most 2,048 characters without user information.
  - `POST /dashboard-images` takes the raw file with its image `Content-Type`, an
    `Idempotency-Key` command UUID and the CSRF header; editors and admins may upload.
    The same bytes return the existing image (200) instead of a new one (201). It
    answers 413 above 5 MiB, 415 for other content types, 422 `invalid_image` when the
    header is not a supported image or exceeds 8,000 pixels, and 409
    `image_quota_exceeded` past 500 MiB.
  - `GET /dashboard-images/{id}` serves bytes to anyone who can read the tenant, with
    a strong ETag and `Cache-Control: private, no-cache`, so every view rechecks
    access and an unchanged image costs a 304.
  - `dashboard_panels.image_id` has a composite tenant foreign key to
    `dashboard_images`, so a saved panel cannot point at a missing or foreign image.
    Fit, description and address live in `content`. Saving or validating a panel with
    an unknown image returns 422 `image_unavailable`.
  - A save marks its images as used (`first_used_at`). Used images are kept like
    retained history, so past revisions keep showing them. Unused uploads cost space
    with no worker to clear them (REV-34), so each upload deletes up to 50 of the
    tenant's uploads that are more than 24 hours old and were never used. Uploads,
    their cleanup and dashboard saves hold the tenant configuration-reference guard;
    a save locks referenced image rows after preset rows and before dashboard rows.
  - Linked images load in the viewer's browser with `referrerpolicy="no-referrer"`;
    the server never fetches them. The dialog uploads a chosen file at once and
    previews it from the local file meanwhile.
  - The image's alternative text is its description, else its title, else "Image
    panel"; the panel itself is labeled by its title or "Image panel". Image panels are not part of count batches, never block preset deletion
    and do not appear in preset references, as for HTML panels.
  - Migration 0063 creates the table and widens the panel type checks without
    rewriting rows.

This extends REV-57's panel types; HTML panels still remove images.

## REV-63 — Alert table panels (2026-11-09)

User decision. A new dashboard panel type, `table`, shows the latest alerts of a saved
preset as a table, like the preset's own results
([dashboard operations 2, 3, 7, 14 and 16](../specs/spec-dashboard-operations.md#2-saved-definition-and-initial-state)).
The user chose the design from the canvas at
https://claude.ai/artifact/XscgPgm7y16jQqcwyAaVvi.

- **Settings (user decision, 2026-11-09).** A table panel references one saved preset,
  like a count panel, with an optional custom title and a number of alerts to show,
  `rows`, from 1 to 50 (10 by default). It has no thresholds and its top bar stays
  neutral. It appears in the Panel type list as "Alert table".
- **What it shows (user decision, 2026-11-09, accepting the canvas's proposed
  defaults).** The latest `rows` alerts matching the preset's current saved query,
  newest first by last received, whatever the preset's own sort; default suppression
  exclusion and no free-text search, as for counts. Columns are the preset's saved
  columns, read-only. Columns that do not fit the panel's width are hidden from the
  right; the Alert column is always kept. Rows that do not fit the panel's height
  scroll inside it. Rows have no checkboxes, bulk actions or row menu: a row opens
  the alert, the title and an "Open preset" footer link open the preset (section 7),
  and the footer states how many of the matching alerts are shown.
- **Assistant-selected details.** Storage reuses `preset_id` for the reference, so
  table panels block preset deletion and appear in preset references exactly like
  count panels, and keeps `{"rows": n}` in `content`; thresholds stay empty. Table
  panels are not part of count batches. The browser reads the rows through the saved
  preset preview (`POST /presets/preview` with `preset_id` and `expected_revision`),
  which gains `newest_first`: allowed only with a saved preset, it replaces the saved
  sort with last received descending, so the server still reads the saved query and
  fences it by revision; a changed preset reloads the panel. The panel reloads with
  the dashboard's live updates and refresh. A new table panel starts at 6 × 6 grid
  units so its rows have room. Viewers see table panels, as for every panel. A table panel's accessible name is its title, else the preset name.
  Migration 0064 widens the panel type check to `table` beside REV-62's `image` and
  ties `preset_id` to `count` and `table` panels without rewriting rows; it follows
  REV-62's 0063, which was built in parallel and merged first.

This extends, for `table` panels, section 2's preset reference and section 3's
content rules; count, HTML and image panels are unchanged. Original issue IDs and REV
numbering are unchanged. Executed evidence belongs in delivery.

## REV-64 — Threshold color picker (2026-11-09)

User decision. A count panel's threshold color is chosen from a palette of named
colors or entered as a custom color, like Grafana's color picker, instead of the four
fixed colors of [dashboard operations 5](../specs/spec-dashboard-operations.md#5-colors-and-thresholds).
The user approved the design from the canvas at
https://claude.ai/artifact/Jq25myWGjN3oAymCuc4Tdu.

- **Picker (user decision, 2026-11-09).** Each threshold shows a color button with
  the color and its name (or hex value). It opens a picker with two tabs. Colors
  offers eight hues (red, orange, amber, green, teal, blue, purple, gray), each in
  five shades from lightest to darkest. Custom offers a saturation and brightness
  area, a hue slider and a hex field. A pick applies to the dialog's preview at once;
  the dashboard still saves only when the editor saves it.
- **Stored values (assistant-selected, accepted by the user 2026-11-09).** `color` is
  either a palette name — the hue alone for the middle shade, or the hue prefixed by
  `lightest-`, `light-`, `dark-` or `darkest-` (for example `dark-teal`) — or a
  custom color `#RRGGBB`. Hex values are stored in upper case; any other value is
  rejected. The former names `blue`, `green`, `amber` and `red` are palette names, so
  saved panels keep their colors unchanged. No migration rewrites panels.
- **Themes (assistant-selected, accepted by the user 2026-11-09).** Palette names
  render in a shade tuned for the active light or dark theme; the middle shades of
  blue, green, amber and red match the existing theme marks. Custom colors render
  exactly as entered in both themes.
- **Unchanged.** A threshold color stays a presentation-only top border on the count
  panel and the dashboard list's panel thumbnails. No other CSS, gradients, blinking,
  sounds or automatic action is accepted, and bounds, counts and accessibility rules
  are unchanged.

This extends section 5's palette; the rest of section 5 and every other panel type
are unchanged. Original issue IDs and REV numbering are unchanged. Executed evidence
belongs in delivery.

## REV-65 — ServiceNow ticket panels (2026-11-09)

User decision. A new dashboard panel type, `servicenow`, shows how many ServiceNow
incidents a team has right now, as a number colored by thresholds, like KeepHQ's
"Service Now" widget
([dashboard operations 2, 3, 11, 12, 14 and 16](../specs/spec-dashboard-operations.md#2-saved-definition-and-initial-state)).
The user approved the design from the canvas at
https://claude.ai/artifact/Cz4RDE8QUBt35p4d1KrZ1e and removed its queue link.

- **Settings (user decision, 2026-11-09).** A ServiceNow panel has an optional custom
  title (blank shows "<team> tickets"), a team (free text, 1–200 characters), a
  ticket state (Open, In progress or Both), a detection method (Hamal: incidents the
  monitoring center raised; Direct: incidents reported straight to the team; All)
  and up to three count thresholds with the same rules and colors as count panels.
  It has no link and references no preset. It appears in the Panel type list as
  "ServiceNow tickets".
- **Where the count comes from (user decision, 2026-11-09).** The company's ticket
  counting service, the same one Keep uses, answers one HTTP GET per query. The
  panel's settings become query parameters exactly as KeepHQ sends them: `team`,
  `state` (`new`, `in_progress` or `all`) and `system_failure` (`true` for Hamal,
  `false` for Direct, absent for All). Parameters already in the configured address
  are kept; the panel's values replace same-named ones. `{"count": n}` shows n. How
  the service queries ServiceNow is outside Keep.
- **Configuration (user decision, 2026-11-09).** The service address is deployment
  configuration, like the Grafana connection
  ([operator operations 14](../specs/spec-operator-operations.md#14-platform-grafana-configuration-and-compatibility)):
  the secret `KEEP_TICKET_COUNT_URL`, `https` only, mounted only into the Product
  API, and it may carry an access key. Nobody edits it in the UI. Super admins see a
  read-only Integrations page with its status, host, last answer or error and a Test
  connection action; the path and query are never shown or logged. While it is not
  configured, the type is listed but disabled and existing panels say ServiceNow isn't
  connected.
- **Load control (user decision, 2026-11-09).** Each Product API process shares
  answers for the same team, state and detection for 30 seconds across viewers and
  tenants, and sends one request per key at a time; failures are reused for 10
  seconds. Panels refresh about every 60 seconds, on Refresh counts and when the tab
  becomes visible again, so a shown count can be up to about 90 seconds old. This
  is separate from alert counts, which section 12 still never reuses.
- **Results that differ from KeepHQ (user decision, 2026-11-09, accepting the canvas).**
  A "Team not found" answer, with a 2xx or 4xx status, shows Team not found instead
  of 0. Valid JSON without a whole-number count shows No count instead of 0. A
  timeout, connection error, other error status, redirect, oversized or non-JSON
  reply keeps the last count greyed
  with no threshold color and its age; with no earlier count it shows that the count
  is unavailable.
- **Assistant-selected details.** Storage keeps `team`, `ticket_state` (`open`,
  `in_progress`, `both`) and `detection` (`hamal`, `direct`, `all`) in `content` and
  thresholds in `thresholds`; migration 0065 widens the panel checks without
  rewriting rows. The browser asks for counts with
  `POST /api/tenants/{tenant_id}/ticket-counts`, sending up to 24 queries rather than
  panel IDs, so unsaved previews use the same call; each query has its own result
  (`count`, `not_found`, `no_count`, `unavailable`, `not_configured`) and a failing
  service never fails the request. Counts are decimal strings on the wire, like other
  dashboard counts. Outbound requests time out after 5 seconds, do
  not follow redirects, ask for an uncompressed reply and read at most 64 KiB. At most
  20 requests per process run at once; a query that finds no free slot within 3
  seconds is reported unavailable without being remembered as a service failure. An
  optional `KEEP_TICKET_COUNT_CA_FILE` names a trusted CA for the service. Teams are free text because the
  service lists no teams. ServiceNow panels are not part of count batches; a new one
  starts at 3 × 3. Viewers see them, as for every panel.

This adds a panel type beside sections 2, 3 and 14; count, HTML, image and table
panels are unchanged. Original issue IDs and REV numbering are unchanged. Executed
evidence belongs in delivery.

## REV-66 — Panel links (2026-11-09)

User decision. Every dashboard panel type (count, table, HTML, image and ServiceNow)
may have a panel link. When one is set, the panel shows a button that opens the
link's address. REV-65's "no link" for ServiceNow panels refers to the ticket queue
link the user removed from that design; the REV-66 panel link applies to ServiceNow
panels like every other type.
The user asked for this on 2026-11-09 and approved the design from the canvas at
https://claude.ai/artifact/4EeppYSGDV9QfWXR7Td6m9 ("Build it").

- **Settings (user decision, 2026-11-09).** The panel dialog ends every type's
  settings with a Panel link section: Link (optional) and Button text (optional),
  plus Remove link. Blank button text shows "Open link". The dialog's preview shows
  the button before the dashboard is saved.
- **Button (user decision, 2026-11-09).** The button sits at the end of the title
  row with an external-link icon and opens the address in a new tab. An untitled
  HTML panel shows a slim row with only the button; an untitled image shows it over
  the image's top-right corner. When the title row is too narrow, only the icon
  shows. While panels are moved or resized the button shows but does not open. The
  count panel's preset link still opens the preset; the button sits above it.
- **Stored values (assistant-selected, 2026-11-09).** A panel carries `link`, either
  `null` or `{url, label}`. `url` is an absolute `http` or `https` address with a
  host, at most 2,048 printable ASCII characters, with no spaces and no user name or
  password. `http` is allowed because internal tools often have no TLS; image
  addresses stay `https` only. `label` is optional trimmed NFC single-line text of
  at most 40 characters using the name character exclusions; blank is stored as
  `null`. The link lives in the panel's `content`, so no migration is needed;
  panels saved before REV-66 have no link.
- **Safety (assistant-selected, 2026-11-09).** The server never fetches the address.
  The browser opens it with `noopener noreferrer`, and the address shows on hover and
  focus so people can see where it goes. Like HTML panel links, it is set by
  editors and shown to everyone who can read the dashboard.

This extends section 2's panel definition and section 3's panel content for every
panel type; counts, thresholds, references and layout are unchanged. Original issue
IDs and REV numbering are unchanged; REV-65 (ServiceNow ticket panels) was built in
parallel and merged first. Executed evidence belongs in delivery.

## REV-67 — The system is named Keep (2026-11-10)

User decision. The system formerly named Appchi is named **Keep** everywhere: the
product name in the UI and documents, the eleven repositories (`keep-<part>`), the
GitHub organization (`keep-alert-operations`), the local workspace folder
(`keep-workspace`) and every internal identifier. The organization's current system,
the KeepHQ fork, is called **KeepHQ** in these documents so the two stay distinct.
The user asked for this on 2026-11-10 and approved the plan, choosing the full rename
over a visible-names-only rename.

- **Internal identifiers (user decision, 2026-11-10).** The Python namespace is `keep`
  (distributions `keep-contracts`, `keep-domain`, `keep-api` and so on); environment
  variables are `KEEP_*`; gateway headers are `X-Keep-*`; Kafka topics are
  `keep.<environment>.alerts.*`; the Keycloak realm, web client and login theme are
  `keep`, `keep-web` and `keep`; Elasticsearch, Redis, cache, image and template names
  use `keep-`; Grafana contact points are named `Keep - <operator>`; browser storage
  keys use `keep`. This supersedes the repository-layout rule that renaming a
  repository leaves these names unchanged.
- **Stored format tags (user decision, 2026-11-10).** Version and format tags that are
  written into stored data or used in hashes, identifiers and encryption (for example
  `keep-cel-v1`, `keep-grafana-v1`, `keep-visibility-sample-v1`, the `keep:1:`
  encryption context and the recovery evidence tags) are renamed too. Data written
  under the Appchi tags cannot be read after the rename: an environment upgraded from
  an Appchi release starts with empty application data, Kafka topics, search indexes
  and identity realm. The user accepted this because no production environment exists.
- **Database (assistant-selected, 2026-11-10).** Migrations `0001`–`0065` keep their
  exact bytes and checksums and still create `appchi_*` roles and `appchi.tenant_id`
  policies. Migration `0066` renames the `appchi_api`, `appchi_worker` and
  `appchi_recovery` roles to `keep_*`, rewrites every policy to read `keep.tenant_id`
  and moves the visibility sampling check to the new tag. When another database in the
  same cluster already renamed the roles, `0066` moves this database's policies,
  privileges, memberships and ownership to the `keep_*` roles and drops the re-created
  `appchi_*` roles once nothing uses them. Login roles and the migration identity are
  created outside the chain and use the `keep_` names from the delivery templates.
- **Kept as they were (assistant-selected, 2026-11-10).** Git history, the `SOURCE.md`
  origin records, migration SQL `0001`–`0065` with their checksums, the historical
  architecture image and dated screenshots in delivery evidence. The CI secret
  `APPCHI_REPOSITORIES_TOKEN` keeps its name until it is re-added under a new name,
  because its value cannot be read back. Records written before 2026-11-10 were
  written under the name Appchi; their names were updated by this decision.

Behavior, contracts other than the renamed identifiers, data authority and worker
scope are unchanged. Original issue IDs and REV numbering are unchanged. Executed
evidence belongs in delivery.

## REV-68 — Grafana panels (2026-11-10)

User decision. A new dashboard panel type, `grafana`, shows one live Grafana panel,
framed straight from Grafana in the viewer's browser, like KeepHQ's Grafana panel
widget ([dashboard operations 2, 3, 13, 14 and 16](../specs/spec-dashboard-operations.md#2-saved-definition-and-initial-state)).
It is its own type because HTML panels remove iframes and stay that way (REV-57). The
user approved the design from the canvas at
https://claude.ai/artifact/LPwZUY8L9QzEKYuJkkisF4 and said "build it", after removing
its theme option and moving its "Open in Grafana" button onto the address box.

- **Settings (user decision, 2026-11-10).** A Grafana panel has an optional title
  (blank by default, because Grafana draws the panel's own title) and one panel
  address. The dialog accepts the address or Grafana's Share › Embed `<iframe>` code,
  of which only the first iframe's `src` is used ("Using …" shows it), lists the
  allowed Grafana, describes the address (dashboard, panel, time range, refresh,
  variables) and previews the live panel. A button attached to the address box fills
  the REV-66 panel link with the panel's full dashboard view in Grafana ("Open in
  Grafana"). It appears last in the Panel type list as "Grafana panel"; a new one
  starts at 6 × 6.
- **Theme (user decision, 2026-11-10).** The panel always uses the viewer's Keep theme:
  Keep sets Grafana's `theme` to `light` or `dark` when framing it. There is no setting,
  and the saved address is not changed.
- **Allowed Grafana (assistant-selected, 2026-11-10, accepting the design note).** The
  deployment lists the Grafana instances panels may frame in
  `KEEP_GRAFANA_PANEL_ORIGINS`: comma-separated `https` addresses, each an origin with an
  optional base path for a Grafana served under a sub-path, mounted into the Product API.
  It is not a secret. Loopback `http` is accepted only in development. Entries that are
  unusable (another scheme, credentials, a query or fragment, Keep's own origin) are
  ignored with a reason instead of failing start-up. An empty list turns Grafana panels
  off: the type is listed but disabled, and existing panels keep their settings and say
  Grafana panels are turned off. The shared company Grafana used for operator routing is
  not allowed unless it is listed. Super admins see the list, the ignored entries and the
  Grafana-side settings on a read-only Admin › Integrations card; nobody edits it in the UI.
- **Address checks (assistant-selected, 2026-11-10).** In this order, the first failure
  shown: not empty; embed code holds an iframe `src`; parses; `http` or `https` and
  literally starts with `http://` or `https://`; not Keep's own origin; Grafana panels on;
  no user name or password; `https` unless the host is loopback; origin and base path
  allowed; path starts with the base path and `/d-solo/`; at most 2,048 characters.
  Credentials and `http` come before the allowed list, unlike KeepHQ, because Keep's list
  is `https` only and would otherwise hide the real problem. The browser checks on input
  and before every render, so a panel saved through the API or whose Grafana was removed
  from the list is never framed and shows "Grafana panel blocked" with the reason. The
  Product API checks a Grafana panel's address on save when it is new or differs from
  the same stored panel's, returning 422 `grafana_url_invalid`; an unchanged address
  saves even after its Grafana was removed, so the dashboard stays editable. A copy
  creates new panels, so its Grafana addresses are checked like new ones and a copy
  holding a blocked panel is refused with the reason.
- **Frame (assistant-selected, 2026-11-10).** `sandbox="allow-scripts allow-same-origin
  allow-forms allow-popups allow-popups-to-escape-sandbox"`, no top navigation,
  `referrerpolicy="no-referrer"`, `loading="lazy"`, the validated address only, titled by
  the panel title or "Grafana panel". `allow-same-origin` grants Grafana's origin, never
  Keep's, because Keep's own origin is refused. While panels are moved or resized a cover
  sits over the frames. Grafana refreshes the panel on its own schedule; Refresh counts
  does not reload it. The Product API never contacts Grafana for these panels.
- **Data boundary (assistant-selected, 2026-11-10).** What a framed panel shows is
  decided by Grafana and each viewer's own Grafana session (or Grafana's anonymous
  access), not by Keep's tenants or roles; the panel dialog and Integrations card say
  so. Only Grafana trusted as much as Keep should be listed.
- **Not built (assistant-selected, 2026-11-10).** A `frame-src` Content-Security-Policy
  limited to the allowed Grafana is left for a later decision: the UI's headers are
  fixed when the image is built, so a per-deployment list needs a runtime proxy on every
  request. Keep's pages keep `X-Frame-Options: DENY`. The Integrations card does not
  count panels per Grafana, since that would read across tenants.
- **Storage (assistant-selected, 2026-11-10).** `content` holds `{"url"}` beside the
  REV-66 `link`; thresholds stay empty and no preset or image is referenced. Migration
  `0067` widens the type check and requires a `url` string of 1–2,048 characters starting
  with `http://` or `https://`, without rewriting rows. Grafana panels are not part of
  count batches. Status for tenant readers is `GET /tenants/{tenant_id}/grafana-panels/status`
  and for super admins `GET /admin/integrations/grafana-panels`.

This adds a panel type beside sections 2, 3, 13, 14 and 16; other panel types are
unchanged. Original issue IDs and REV numbering are unchanged. Executed evidence belongs
in delivery.

## REV-69 — Incident count panels (2026-11-10)

User decision. A new dashboard panel type, `incident_count`, shows how many incidents
the alerts of a saved preset are in
([dashboard operations 2, 3, 7, 11, 14 and 16](../specs/spec-dashboard-operations.md#2-saved-definition-and-initial-state)).
The user approved the canvas at https://claude.ai/artifact/GUkDWqBYr5DjzkMyMJacpd
("build it", 2026-11-10).

- **What it counts (user decision, 2026-11-10).** Distinct incidents that actively own
  at least one alert matching the preset, as the preset's count matches them (saved
  query, current alerts, suppressed excluded). An incident counts once however many of
  its alerts match; alerts in no incident add nothing. The editor chooses Firing,
  Investigating or both, as two checkboxes with both ticked by default; resolved
  incidents are never counted. Firing is the incident status `open`, which the
  Incidents list labels Open.
- **Settings (user decision, 2026-11-10, accepting the canvas).** Optional title
  ("<preset> incidents" when blank), a preset, the statuses and up to three count
  thresholds like a count panel. It appears second in the Panel type list as
  "Incident count". The tile states "<preset> · <statuses>" under its title. The dialog
  preview shows the count and the numbers behind it: matching alerts, how many of
  them are in a counted incident, and the incidents.
- **Assistant-selected details.** Storage reuses `preset_id` and `thresholds` and keeps
  `{"incident_status": "open" | "investigating" | "both"}` in `content`; migration 0068
  widens the panel checks after REV-68's 0067 (Grafana panels, built in parallel and
  merged first). The count batch adds a `terms` aggregation on
  `active_incident_id` to the preset's count query in the batch's point in time and
  keeps, in its PostgreSQL revalidation transaction, the incidents with a matching
  status and an unretired identity. Alert ownership therefore comes from the search
  projection and incident status from PostgreSQL; a just-changed link shows once
  projected, as for alert counts. More than 10,000 distinct incidents for one panel
  is unavailable rather than a partial number. `POST /alerts/counts` gains
  `incident_status` per query for the dialog preview. The title opens the preset, as
  for a count panel: the canvas proposed opening those incidents in the Incidents
  list, which cannot filter by a preset's alerts.

This extends, for `incident_count` panels, sections 2, 3 and 11 and the APIs of
section 14; other panel types are unchanged. Original issue IDs and REV numbering are
unchanged. Executed evidence belongs in delivery.
## REV-70 — ServiceNow tickets on incidents (2026-11-10)

User decision. An incident can carry one ServiceNow ticket: editors link an existing
ticket, change or remove the link, or open ServiceNow's new incident form filled in
from the incident and then link the ticket they created there, like KeepHQ's ticketing
options on an incident
([incident operations 15 and 18](../specs/spec-incident-operations.md#15-detail-and-mutation-ux-i3-i5)).
The user approved the design from the canvas at
https://claude.ai/artifact/3qmYSHaGt7j1gYD31qssFT and the plan, and said "build it",
after renaming the Create dialog's first field to "Ticket Title".

- **Keep never calls ServiceNow (user decision, 2026-11-10, accepting the plan's
  default for its open question).** As in KeepHQ, Keep stores only the ticket's link
  and optional number; it never reads, creates or changes tickets and holds no
  ServiceNow credentials. Creating opens ServiceNow's new incident form in a new
  browser tab with its short description ("Ticket Title" in the dialog, at most 160
  characters, starting as the incident title) and description (starting as the
  incident description followed by its severity and a link back to the Keep
  incident) filled in through `sysparm_query`, with `^` written as `^^`; the
  description is shortened so the address stays within 4,000 characters. Keep writes
  nothing at that step. The dialog's second step links the new ticket with the same
  checks as linking an existing one. The standard `incident.do` form is used. The
  incident list and incident search are unchanged.
- **Stored on the incident (assistant-selected, 2026-11-10).** The ticket is part of
  the incident aggregate, not a generic enrichment: `ticket_url`, `ticket_number`,
  `ticket_linked_at` and `ticket_linked_by` on `incidents` (migration 0069). One
  ticket per incident. Linking, changing and unlinking are one command,
  `POST /incidents/{id}/ticket` with `url` and `number` (both null to unlink), under
  the incident command contract: `edit` permission, expected revision, idempotent
  command identity, 409 on a stale revision with nothing changed. An effective change
  advances the revision and records one `ticket` activity with the new and previous
  link and number; a no-op records nothing. It is allowed in every status, and
  resolving or reopening never changes it. It is not qualifying activity, so it does
  not move last activity.
- **Which links are accepted (assistant-selected, 2026-11-10).** The deployment names
  its ServiceNow in `KEEP_SERVICENOW_URL`: an `https` address with a host and an
  optional base path, no user name, password, query or fragment, mounted into the
  Product API. It is not a secret. Loopback `http` is accepted only in development.
  An unusable value is logged and treated as unset. A saved link must have that
  scheme, host and port, a path under that base path, no user name or password, no
  spaces or control characters and at most 2,048 characters; otherwise 422
  `ticket_url_invalid`. A number is optional, letters then digits
  (`^[A-Z]{2,8}[0-9]{4,12}$` after upper-casing), and requires a link. The dialog
  accepts a bare number and builds
  `<KEEP_SERVICENOW_URL>/nav_to.do?uri=task.do%3Fsysparm_query%3Dnumber%3D<number>`;
  it takes the number from a pasted link that contains `number=`, and otherwise offers
  an optional number field. Without `KEEP_SERVICENOW_URL`, linking returns 409
  `servicenow_not_configured`, unlinking still works, the ticket row is hidden on
  incidents with no ticket, and a ticket linked earlier still shows and opens.
  `GET /servicenow/status` tells the browser whether it is configured and its address.
- **Who sees what (assistant-selected, 2026-11-10).** The ticket row sits at the
  bottom of the incident's Status and Assignee panel. Everyone who can read the
  incident sees the ticket number (or "ServiceNow ticket" when none was given) as a
  link that opens the stored address in a new tab without a referrer, and who linked
  it and when. Editors also get Create in ServiceNow… and Link existing ticket… while
  none is linked, and Change… (Link a different ticket…, Unlink ticket) once one is.
  Activity shows ServiceNow ticket linked, changed or unlinked. Super admins see a
  read-only "ServiceNow tickets on incidents" card on Admin › Integrations.
- **Improvements over KeepHQ (assistant-selected, 2026-11-10).** Links are checked
  against the configured ServiceNow on the server, tickets can be unlinked and
  changed, every change is in the incident's activity, and the created ticket is
  linked back in the same dialog.

Alert behavior, incident membership, lifecycle and correlation are unchanged.
Original issue IDs and REV numbering are unchanged. Executed evidence belongs in
delivery.

## REV-71 — A new tenant starts without an administrator (2026-11-11)

User decision. When a global super-admin creates a tenant on Admin › Platform, Keep no
longer makes the creator its first administrator. The tenant is created with its name
only, the browser goes straight to the new tenant's Permissions page, and that page
requires adding an administrator
([tenant access 2 and 4](../specs/spec-tenant-access.md#2-tenant-creation)). Asked
whether the administrator should instead be chosen in the create form, so a tenant is
never without one, the user chose to create the tenant first and require the
administrator on its Permissions page.

- **Creation (assistant-selected, 2026-11-11).** `POST /api/tenants` keeps
  `initial_grants` required but accepts an empty list (0–100 grants). An empty list
  creates the tenant without a local administrator. A non-empty list keeps the earlier
  rule: it must include at least one eligible local administrator, so existing callers
  behave as before. Creation stays one transaction with its audit and command receipt;
  the `tenant-created` audit records the empty grant snapshot. The response still
  reports the caller's inherited `admin` role. Platform creation in the UI always sends
  an empty list. No migration is needed.
- **The roster says whether an administrator exists (assistant-selected,
  2026-11-11).** `GET /api/tenants/{id}/permissions` adds `meta.has_local_admin`,
  counted the same way as the last-admin check: distinct eligible, undeleted users
  reached through the tenant's own admin grants, including team members. It is also
  false after a verified external vacancy, so the same page shows that repair
  condition to global super-admins.
- **How the administrator is required (assistant-selected, 2026-11-11).** The server
  keeps the existing rule that every permission batch must leave at least one eligible
  local administrator, so the first save of a tenant without one must add one; any
  other batch returns 409 `last_admin_required` with nothing changed. In the UI, after
  creation commits, the Platform page refreshes the signed-in user's tenant list and
  opens `/tenants/{id}/permissions`. While `has_local_admin` is false, that page shows
  a warning that the tenant has no administrator, the role for a new grant starts at
  Admin, Save stays disabled until the draft sets at least one Admin grant, and leaving
  the page (another page, another tenant, Back, or closing the tab) asks for
  confirmation with a message that the tenant has no administrator. A super-admin who
  confirms leaves the tenant without one: it keeps operating like a tenant after an
  external vacancy, and the warning returns whenever its Permissions page is opened.
  Leaving the Platform page after creation still asks before discarding an unsaved
  source-repair reason; if the super-admin stays, the created-tenant message keeps
  its Open tenant permissions button.

Global, operators, directory publication and its vacancy and restoration audit are
unchanged; a tenant created without an administrator records no vacancy event,
because it never had one. Original issue IDs and REV numbering are unchanged.
Executed evidence belongs in delivery.

## REV-72 — Global administration shows Integrations and Platform (2026-11-11)

User decision. In the Global tenant, global super-admins get the Admin link at the
foot of the rail, and its Administration tabs are only Integrations and Platform. The
other Administration tabs (Operators, Permissions and Access audit) are not shown in
Global ([system completion 3](../specs/spec-system-completion.md#3-navigation-and-visual-system),
[tenant access 7](../specs/spec-tenant-access.md#7-global-permissions)). Before this,
Global had no Admin link, and super-admins reached Integrations and Platform from a
specific tenant.

- **Where the Admin link opens (assistant-selected, 2026-11-11).** The Admin link opens
  the first tab the user has in the current tenant: Integrations in Global, Operators in
  a specific tenant. Users who aren't global super-admins have no Admin link in Global.
  Specific tenants are unchanged: Operators for every reader, Permissions and Access
  audit for tenant admins, and Integrations and Platform for global super-admins.
- **Global's other Administration addresses (assistant-selected, 2026-11-11).**
  `/tenants/{global}/operators`, `/permissions` and `/audit`, including operator detail
  addresses, show the standard Page unavailable page for everyone. This removes the
  read-only Global access-policy page that section 7 selected; Global's fixed policy is
  unchanged and still has no editable grants. Global never holds managed operators
  (operator operations 3), and the API still serves Global's permissions summary and
  tenant/access audit to global super-admins; only the UI pages are gone.

APIs, authorization, audit and operators are unchanged; no migration. Original issue
IDs and REV numbering are unchanged. Executed evidence belongs in delivery.

## REV-73 — Keep password sign-in and ADAPI directory replace Keycloak (2026-11-15)

User decisions. The user's team found the Keycloak↔LDAP integration unreliable and
asked to remove Keycloak completely, in company and local environments. Keep gets
its own username/password page; the Product API checks the password with one ldap3
simple bind against Active Directory and reads people and groups from ADAPI, the
company AD REST API ([identity configuration](../specs/spec-identity-configuration.md),
[tenant access 5 and 12](../specs/spec-tenant-access.md#5-directory-selection-and-visibility),
[worker scope 3–6](../specs/spec-worker-scope.md#4-directory-synchronization-is-nice-to-have)).
The user calls this "the new SSO"; it is password sign-in, not single sign-on. The
user approved the plan on 2026-11-15 with background saves (Q9 = c). The user's
decisions:

- The sign-in page keeps the look of the former Keycloak theme. The bind is
  `username@<domain>` (the format is a setting) with the password sent as UTF-8
  bytes. The password is used for that one bind only: never stored, logged or
  forwarded.
- LDAP encryption is a setting, off for now on the private network; plain LDAP
  locally. This overrides identity section 6's earlier rule that directory
  connections use TLS with certificate validation.
- After the bind, Keep looks the person up in ADAPI by samAccountName for the
  display name and the disabled flag (`userAccountControl & 2`). A disabled person
  is refused. A person unknown to Keep is saved at that moment.
- Users and groups are identified by samAccountName ("samAccountName doesn't
  change"); no GUID and no GUID reuse check.
- Sessions last 24 hours absolute. There is no idle timeout, no Keep lockout and
  sign-out is local only. Sign-in reads no groups, and a session is not rechecked.
- Group membership and disablement change only through the manual directory
  refresh, which stays a command. A scheduled refresh comes later, in its own
  change with its own REV.
- Picker searches use `/users` and `/groups` with `samAccountName=*term*` and
  `customFilter=(displayName=*term*)`, with no security-group filter, and show the
  display name only. Search answers are cached in Redis for "a couple of hours".
- Save on pick: an administrator picking an unknown person or group makes Keep read
  it (and a group's recursive members) from ADAPI and save it immediately. A group
  too big to save within the request limit is saved in the background and shown as
  pending (Q9 = c). For these request-started saves only, this replaces REV-35's
  sentence in [worker scope 4](../specs/spec-worker-scope.md#4-directory-synchronization-is-nice-to-have)
  that unknown identities await explicit publication and "there is no autonomous job
  to service that request in this scope".
- Group members come from `/groups/members/user?samAccountName=…&isRecursive=true`,
  which the user stated handles cycles, includes people reached through
  distribution groups, has no 1,000 cap and does not take `attributesToLoad` (Q6).
  `/users` returns disabled accounts too (Q7). Searches cap silently at 1,000 rows;
  failures return non-200. Multi-domain forests are not handled (Q8: "dont consider
  it"); there are no domain settings.
- The `ClientId` header value comes from an environment variable (Q1).
- Global super-admins are the user's team AD group, configured by samAccountName.
- Keep's own LDAP directory reader is removed. Local development uses an OpenLDAP
  container for passwords and a mock ADAPI with the same test users. The branch
  `feature/replace-keycloak-authelia` is ignored.
- **Accepted risks (user decisions).** Passwords cross the private network
  unencrypted while encryption is off. Keep has no lockout; failed binds still count
  toward AD's own lockout. A disabled person keeps access until the next refresh or
  the end of their 24-hour session. A reused username inherits the old holder's
  access.

Removed by this decision: Keycloak and its realm, theme and local container; OIDC
and the Authlib dependency; the routes `GET /auth/login`, `GET /auth/callback`,
`POST /auth/activity` and `POST /auth/backchannel-logout`; Keep's LDAP directory
reader; the 30-minute idle timeout and activity heartbeat; provider logout,
backchannel logout and revocation fences.

- **Directory source and identity (assistant-selected, 2026-11-15).** The source is
  named `adapi`; `principals.object_id` holds the lowercase samAccountName. A lookup
  gets a kind hint (the stored kind, the requested kind, or `user` at sign-in), asks
  the hinted endpoint first and the other only if it has no row. An object is
  deleted only when both endpoints return 200 with zero rows. More than one row is
  ambiguous and fails closed, and a returned name must equal the key. Members whose
  name ends in `$` are skipped. A group's label is `displayName` when returned, else
  `cn`.
- **ADAPI client (assistant-selected, 2026-11-15).** An httpx client sends the
  `ClientId` header from `KEEP_ADAPI_CLIENT_ID`. Per-call timeouts are 5 seconds in
  the refresh command and the smaller of 3 seconds and the remaining request budget
  minus 1 second inside a request. A non-200 response or bad JSON means unavailable.
  Member display names come in batches of 50 (`KEEP_ADAPI_LOOKUP_BATCH`) through an
  escaped `customFilter` with `attributesToLoad`; a member a batch omits keeps the
  members route's `userAccountControl` and is never marked deleted from a batch.
- **Sign-in (assistant-selected, 2026-11-15).** The page is the Next.js route
  `/sign-in`, outside `/auth` and outside the workspace catalog route. `POST
  /auth/login` takes JSON `{username, password, return_to}` and checks, before any
  bind, the human-authorization gate, the exact Origin, its own 4 KiB body limit and
  identity-only `Content-Encoding`, the username (1–64 characters, no AD-forbidden
  characters, no `@` or `\`) and a non-empty password, because an empty-password
  simple bind succeeds anonymously on AD. The bind runs with 2-second connect and
  receive timeouts, then LDAP WhoAmI must name the typed username (`u:DOMAIN\name`,
  domain not checked, or the bind DN for `dn:`), because AD resolves a
  userPrincipalName before `sAMAccountName@domain`. Results: 401
  `authentication_rejected` for a wrong password, a WhoAmI mismatch or a disabled
  account; 403 `account_not_in_directory` or `account_ambiguous` for zero or two
  ADAPI rows; 503 `sign_in_unavailable` when LDAP or ADAPI is down or less than
  1 second of the request budget remains before publishing. Sign-in publishes a
  single-object evidence only when the person's row changed (new, renamed, enabled ↔
  disabled; saving a changed row is an assistant addition the user approved with
  the plan), so a re-enabled person can sign in and a disabled one loses their
  other sessions. On success the previous cookie's session is revoked and a new
  handle issued. `return_to` validation moves into the authentication module.
- **Kept routes (assistant-selected, 2026-11-15).** `POST /auth/logout` is local
  and returns no `logout_url`; `GET /auth/session` drops `refresh_uncertain` and
  keeps `absolute_at`. Authentication drops the idle test, and visibility proofs
  bind on the session handle hash, sign-in time and absolute deadline.
- **Settings (assistant-selected, 2026-11-15).** `KEEP_LDAP_HOST`, `KEEP_LDAP_PORT`,
  `KEEP_LDAP_USE_TLS` (default false), `KEEP_LDAP_CA_FILE`, `KEEP_LDAP_BIND_FORMAT`,
  `KEEP_ADAPI_URL`, `KEEP_ADAPI_CLIENT_ID` (secret), `KEEP_ADAPI_LOOKUP_BATCH` (50),
  `KEEP_ADAPI_SEARCH_CACHE_TTL_SECONDS` (7,200) and `KEEP_SUPERADMIN_GROUP`. The
  Product API and the refresh command read this one super-admin setting; the
  refresh's separate super-admin object ID setting is removed. The OIDC settings,
  the directory configuration file and the search profile are removed. Bootstrap
  stays `KEEP_DIRECTORY_BOOTSTRAP_QUALIFIED`.
- **Search and its cache (assistant-selected, 2026-11-15).** In `customFilter`,
  `( ) * \` are escaped. At most 200 rows are shown; a 1,000-row answer asks the
  user to type more. Unsaved rows return `id: null`, and a search never changes what
  is stored or queues anything. The cache holds the raw `/users` and `/groups`
  answers for 2 hours under a SHA-256 key of kind and normalized term, merges stored
  state from PostgreSQL on every request, feeds only picker listings, and falls
  through to ADAPI when Redis is down or a value is corrupt. This widens Redis from
  "hint transport" to "hint transport and non-authoritative picker search cache".
- **Save on pick (assistant-selected, 2026-11-15).**
  `POST /api/tenants/{id}/permission-principals/resolve` with `{kind, username,
  retry}` is the only save route; tenant admins and global super-admins only. It
  takes the exclusive identity guard first, then authorizes, then publishes. Check
  order: a pending row (failed without `retry: true` → 503 with `last_failure`;
  failed with `retry: true` → hand over again; leased or queued → 202); then a
  stored, usable principal → 200 with no re-read; otherwise an inline save with a
  7-second verifier deadline and at least 1 second left before publishing → 200,
  or, when it does not fit, nothing published, a pending row, a hand-over and 202
  `{status: "pending"}`. A fence rejection retries once within the budget, then 503
  `directory_busy`. A name neither endpoint knows, or that two rows match, returns
  422 with nothing saved. `GET …/resolve?kind=&username=` polls PostgreSQL only
  and hands a pending row with no live lease over again. The picker shows "Saving
  from the directory…", polls 3 seconds after each response, and offers Try again
  (`retry: true`) on 503. Grants still accept only saved principals. Added after
  review (assistant-selected, 2026-11-16): a deleted stored principal (a tombstone)
  isn't usable, so a group recreated in the directory is saved again on pick; and an
  ADAPI call that outlasts its own timeout means the save didn't fit (202), not an
  outage.
- **Background saver (assistant-selected, 2026-11-15).** Pending saves keep the
  `directory_verification_requests` table, one row per `(source, object_id)`, with
  `kind`, `lease_owner`, `lease_until`, `last_failure` and `updated_at`. The
  hand-over claims a 120-second lease with a conditional update, and only the
  winner queues the job. Each Product API process runs one saver thread with a
  queue of 20; a full queue releases the claim. Each job runs in a fresh context
  under its own 80-second budget (verifier deadline `min(60 s, remaining − 15 s)`,
  ADAPI calls `min(5 s, remaining − 1 s)`), re-checks and extends its lease at
  start, holds no database connection while reading ADAPI, filters every row update
  on `lease_owner`, and turns any unexpected error into `directory_unavailable`.
  Failure reasons are `directory_unavailable`, `directory_group_too_large`,
  `directory_verification_deadline` and `directory_busy`; the verifier reports them
  as structured reasons. The save-on-pick 202 is a deliberate exception to [worker
  scope 3](../specs/spec-worker-scope.md#3-request-owned-operator-provisioning)'s
  rule that no successful 202 means work continues in the background; operator
  provisioning keeps that rule. The saver is the second background component inside
  the Product API, next to REV-36's live publisher ([worker scope 5 and
  6](../specs/spec-worker-scope.md#6-live-updates-inside-the-product-api)). Its
  share of the existing API pool is one connection at a time per process, used
  briefly for the claim, the publication and the result. Shutdown, before the pool
  closes, sets a stop event, releases this process's leases and shuts the executor
  down with `cancel_futures`. It is not a poller: it runs only jobs handed to it.
- **Publications and the fence (assistant-selected, 2026-11-15).** Sign-in, save on
  pick, the background save and the refresh all publish through the same publisher,
  with generations allocated before reading. An evidence is rejected only when a
  covered root or team has a newer generation; a covered user that a newer
  generation holds is skipped, and memberships are rebuilt from current stored
  eligibility. The publisher's per-object statements become set-based, so a
  10,000-object publication holds the identity guard for well under one second.
  Every publication that changes something advances `directory_revision` and fences
  in-flight visibility proofs; this now also happens on first and changed
  sign-ins, on saves on pick and, during a refresh, once per team.
- **Refresh command (assistant-selected, 2026-11-15).** `directory --once` reads
  through ADAPI. It publishes one evidence for all user roots (batched lookups) and
  one per team root, each with its own generation and 10,000-object cap, so one
  large or failing team cannot block the rest. A fence rejection retries once with a
  new generation. Pending saves without a failure are included; failed ones are
  skipped. The command lists every failed root and exits non-zero if any failed. The
  publication covering the super-admin group carries the bootstrap flag. The group
  refresh remains a manual command.
- **Schema (assistant-selected, 2026-11-15).** Migration `0070_password_login_adapi`
  drops `oidc_bindings`, `login_transactions` and `logout_fences` and the session
  columns for issuer, subject, provider session, tokens, refresh state and activity;
  extends `directory_verification_requests` and deletes its old rows; and grants
  the API role SELECT, UPDATE and DELETE on it, INSERT, UPDATE and DELETE on
  directory edges and root checkpoints, and USAGE on the directory generation
  sequence. Applied migrations are unchanged.
- **Local development (assistant-selected, 2026-11-15).** A pinned OpenLDAP image on
  `127.0.0.1:58389` with bind format `uid={username},ou=people,dc=keep,dc=local`
  (OpenLDAP does not accept `user@domain`), and a mock ADAPI
  (`keep-delivery/scripts/local_adapi.py`, `127.0.0.1:58092`) started by local Start
  that copies the stated response shapes, the `ClientId` check, the 1,000 cap and
  non-200 errors. Local credentials, the wrapping key and the deployment epoch move
  with their values preserved. A one-time remap moves existing local principals to
  `adapi` usernames after migration 0070 and before the first refresh, so local
  grants and history keep their owners. The OpenShift load-test bundle uses the same
  two services.

No company deployment exists, so there are no company users or grants to migrate.
Before company use, one real call per ADAPI route and one real sign-in confirm the
response shapes, the bind format and the WhoAmI answer. Original issue IDs and REV
numbering are unchanged. Executed evidence belongs in delivery.

## Context catalog: identity work reads reliability — 2026-11-16

A retrospective of the REV-73 design and build sessions found that the design put
LDAP and ADAPI calls inside sign-in and save-on-pick requests without reading the
`reliability` topic, which holds the ten-second Product API handler timeout. Plan
critics raised two blockers from it and a change reviewer found a third defect in the
same budget handling, all before merge. The user approved one catalog fix.

Assistant-selected detail: the `identity-access` topic gains a related topic,
`reliability`, read when sign-in or directory work calls LDAP, ADAPI or another
outside service while a request waits; the identity-access topic page is regenerated.
Navigation choice only; no product requirement, authorization boundary, issue ID or
REV number changes.

## REV-74 — Observability: logs, metrics and RUM (2026-11-12)

User decisions. Every Keep service gets full logs and metrics; logs say what happened
in each service and metrics give the numbers at each moment; metrics cover service
monitoring and real user monitoring; every flow and failure path is monitored
([observability](../specs/spec-observability.md)). The user also decided:

- Metrics are exposed on a `/metrics` path and collected by Prometheus or an
  OpenTelemetry collector.
- Logs are sent to Elasticsearch through one Fluent Bit deployment that every service
  sends its logs to, one index per service.
- Keep configures no retention or other Elasticsearch settings. The logs Elasticsearch
  and the alert-search Elasticsearch are each configurable and may be the same cluster
  or different ones.
- Logs must be indicative and relevant, and easy to query: all logs of one alert, and
  the alert itself in the logs so it can be found by application, component and its
  other fields. This supersedes "alert bodies" in the redaction sentence of
  [reliability 20](../specs/spec-reliability-operations.md#20-application-observability-and-telemetry-ownership)
  for log records. Secrets stay out of logs and alert values stay out of metric labels.
- RUM goes through the Product API.
- No traces for now; the 1% trace sampling in reliability 20 stays a recorded gap.

Assistant-selected details (2026-11-12):

- **Record format.** JSON with Elastic Common Schema names, from the standard logging
  module, always also written to stderr. Existing event tokens and messages are kept.
- **Registry and catalog.** One field registry and one event catalog in `keep-domain`.
  With no index template, the registry keeps one type per field so Elasticsearch's
  automatic mapping never meets a conflicting value.
- **Where the alert goes.** Identifying fields on every alert-level record; the whole
  alert once per delivery on the source processor's record, and on ingestion's record
  of a rejected or unconfirmed member. Only the native field names are used; a
  sender-supplied name never becomes a log field.
- **Lookup.** `keep.alert.id` from source processing onward; the native identity
  digest on ingestion and source-processor records, because ingestion has no
  PostgreSQL dependency and cannot know the alert ID.
- **No sampling** of alert-level events, with an emergency setting that reduces
  successes only.
- **Shipping.** Services post batches to Fluent Bit's HTTP input from a background
  thread, each to its own path; shipping never blocks or fails the logged work.
  Indices are `keep-logs-<service>`; names are settings.
- **Metrics.** `prometheus-client` on a dedicated metrics port; closed label sets;
  PostgreSQL-held state read by bounded aggregates inside existing processes. No new
  deployed application component (REV-34 to REV-36).
- **Service level classes**, including a separate `validate` class for dry-run
  endpoints, which have no selected objective.
- **RUM endpoint.** Session and CSRF required, bounded batches, per-session rate limit,
  excluded from the Product API's own indicators.
- **Rollout.** Additive and off unless configured.

Later user decision (2026-11-12): the flow of an alert inside each service is visible
in the logs. Each service records every step an alert takes inside it as its own
record ([observability 3](../specs/spec-observability.md#3-alert-content-in-logs)).
This replaces the earlier choice of one alert-level record per service and delivery.

Assistant-selected details of that decision (2026-11-12):

- **Which steps.** Only points where an alert can stop, branch or wait: received,
  validated or rejected, each unconfirmed publish attempt, published or unconfirmed
  (ingestion); consumed, matched or replayed, applied or refused, change published
  (source processor); consumed, each attachment, correlated or skipped (correlation);
  consumed, indexed or deferred (indexer). Statements inside one transaction are not
  separate steps: they succeed or fail together.
- **Order.** A sequence number per pass, because timestamps have millisecond
  precision and several steps share one.
- **True after commit.** A step reporting a PostgreSQL effect is held and written
  after the commit, and dropped on rollback.
- **Linking.** The delivery ID is on ingestion, source-processor and correlation
  records; the changed-event ID on the source processor's applied and published
  records and on correlation and indexer records. Correlation reads the delivery ID
  from the source-result row it already reads as proof; no query is added.
- **Volume control.** One setting reduces the trail to outcome records. It replaces
  the emergency sampling setting chosen earlier under this REV.

Later user decision (2026-11-12): the Product API's actions on an alert are in the
same trail. Assistant-selected details:

- **One step for every change.** The code that publishes an alert change notes
  `alert_changed` for every cause except a delivered input, so user commands,
  notes, incident links and moves, correlation links and maintenance effects are
  all recorded without touching each route.
- **Commit boundary in one place.** The shared unit of work writes the steps
  noted inside it when it commits and drops them when it rolls back; a nested
  unit settles only its own.
- **A request is a pass.** Its steps carry the request ID and the user, taken
  where the request is authorized. A refused command leaves only its request
  record.
- **Repeated reads.** The summary of automatic refreshes is keyed by user, route
  and resource, covers reads, searches and the session check, and never hides
  a failure or a request slower than one second.

Assistant-selected details of the metrics (2026-11-12), under the user's decision
that metrics give the numbers at every moment:

- **One counter and two histograms for every event.** `keep_events_total` by
  event, outcome and reason; `keep_event_duration_seconds` and
  `keep_event_delay_seconds` by event. They are fed where the record is
  written, so coverage follows the event catalog instead of a second list.
  This replaces the separately named pipeline metrics first planned.
- **Stage timings.** Receipt to commit on `alert_applied`, change to the end of
  the correlation pass on `alert_correlated`, change to searchable on
  `alert_indexed`, and received to confirmed on `alert_published`.
- **Kafka numbers** from the client's statistics callback every five seconds.
- **Rules and dashboard as files** in delivery, with rule unit tests, run by a
  Prometheus and the existing Grafana in the local stack.

Assistant-selected details of real user monitoring (2026-11-12), under the user's
decision that it goes through the Product API:

- **What the browser reports.** Page views by section, page load timings, API
  calls as the browser saw them (counted in the browser into fixed duration
  buckets), failed calls one by one, time in each live-connection state and
  each loss with its cause, unhandled JavaScript errors, time with the tab
  visible or hidden, and events its own buffer dropped.
- **No error text.** A JavaScript error is logged as its class and same-origin
  frames only. The plan had allowed a truncated message; error text can quote
  content, and the rule for server errors already forbids it.
- **Closed labels.** Sections, outcomes, states and reasons are fixed lists, and
  a route must be one of the application's own templates.
- **Limits.** Twelve batches a minute for each session; a batch refused as
  malformed is refused whole.
- **Switch.** The Product API setting turns the endpoint on. A browser that
  gets "not found" stops sending for its session, so no second setting is
  needed in the frontend.

Assistant-selected details of sign-in outcomes (2026-11-16), after REV-73 replaced
the sign-in, under the user's decision that every flow and failure is monitored:

- **One event for each outcome.** A sign-in attempt ends in `sign_in_completed`,
  `sign_in_rejected` or `sign_in_unavailable`, with how long it took. Each is
  counted and timed like every other event, so no separate sign-in metric exists.
- **No way out without an outcome.** A failure outside sign-in's own checks,
  after the username check, is `sign_in_unavailable` under the error code the
  person was answered with: the database, the restore gate, an unexpected
  error. When the request's time ends first, the outcome is unavailable with
  `request_timeout`, whatever sign-in concluded afterwards. A request refused
  before the username check leaves only its request record.
- **Reasons are fixed codes.** The reason is the code the bind, the directory
  client or the stored person gave. Any other value is recorded as `other`, so
  an error's own text reaches neither a record nor a metric label.
- **Who.** A completed sign-in carries the user ID on the event and on its
  request record. A rejected or unavailable one names nobody: the typed
  username is not logged, because a mistyped one can be a password.
- **Levels.** A rejection is `info`: a wrong password is an ordinary fact and
  the counter shows the rate. Unavailable is `warning` and names the dependency
  that failed, LDAP or ADAPI.
- **Missing settings.** `sign_in_configuration_missing` is written once for
  each process and names the settings without their values. Each attempt
  refused for it is still counted as unavailable.
- **A fenced publication** at sign-in is recorded as `sign_in_publication_fenced`.
- **Not selected:** an alert rule for sign-in being unavailable, and events for
  sign-out, a person saved at sign-in and the directory refresh.

Not built in this step: view and panel load timings, command retries, the
estimated receipt-to-screen delay, long tasks and session-ended counts.

Not selected: a Kafka record header carrying the ingestion request ID (proposed,
awaiting the user's answer). Unchanged and still unbuilt: the rendered-visibility
acknowledgement protocol of alert-history technical 21; RUM reports a labelled
estimate only. Consequences recorded for the operating owners: the log indices hold
every tenant's alerts outside Keep's tenant permissions, and nothing rolls over or
deletes them. Original issue IDs and REV numbering are unchanged. Executed evidence
belongs in delivery.

## REV-75 — Daily scheduled directory refresh (2026-11-17)

User decisions. Under REV-73, group membership reached Keep's PostgreSQL only
through the manual directory refresh. The user asked for a job that refreshes the
groups ("later we need to create a cron job to refresh the groups", 2026-11-15),
accepted an OpenShift CronJob that runs the existing one-off refresh command
(2026-11-16) and chose to run it once a day (2026-11-17)
([worker scope 4](../specs/spec-worker-scope.md#4-directory-synchronization-is-nice-to-have),
[identity 7–9](../specs/spec-identity-configuration.md#7-membership-supply-and-the-five-minute-target)).
This supersedes REV-73's "the group refresh remains a manual command" and worker
scope 4's rule that a scheduled refresh is a later change. REV-35 is otherwise
unchanged: there is no directory worker, no poller inside a service, no in-session
recheck and no five-minute target. A membership change waits up to a day; an urgent
one is applied by running the job at once.

Assistant-selected details (2026-11-16 and 2026-11-17):

- **The job.** An OpenShift CronJob `keep-directory-refresh` (pod label
  `app: keep-directory-refresh`) runs
  `python -m keep.identity.worker --once --budget-seconds ${RUN_BUDGET_SECONDS}`
  from the Product API image, with the dedicated identity database login the
  refresh already uses. The schedule is a parameter, default `0 2 * * *` (the time
  of day is an assistant choice). `concurrencyPolicy: Forbid`, so runs never
  overlap; `startingDeadlineSeconds` 3,600; `activeDeadlineSeconds` 2,100;
  `backoffLimit: 0` and `restartPolicy: Never`, so a failed run waits for the next
  day or a manual run; a `SUSPEND` parameter; the migration Job's security
  context; `KEEP_POOL_SIZE=2`.
- **No bootstrap from the job.** It never passes `--bootstrap` and sets
  `KEEP_DIRECTORY_BOOTSTRAP_QUALIFIED=false` explicitly, so a scheduled run cannot
  open the initial bootstrap gate
  ([identity 12](../specs/spec-identity-configuration.md#12-global-super-admin-setup-and-repair)).
  Bootstrap stays a manual run.
- **Run budget.** `--budget-seconds` (job default 1,800, below the 2,100-second
  deadline) and a SIGTERM handler set the refresh's stop event, which is checked
  before every ADAPI call. A stop never interrupts a publication: units not yet
  read fail as `directory_stopped`, units already published stay published, and
  the run still writes its summary and exits 1. A manual run has no budget unless
  given one. `directory_stopped` is a refresh result only; it is never stored as a
  pending save's `last_failure`.
- **Logs.** Both entry points, `python -m keep.identity.worker` and delivery's
  `directory --once`, configure REV-74 logging as service `api`, role
  `directory-refresh`. The refresh writes `directory_root_failed` for each failed
  team root (the group's samAccountName and the reason) and for each failed batch
  of person roots (their number and the reason, never their names, because
  observability 4 keeps user names out of log records);
  `directory_refresh_completed` (units, published units, failed roots, duration);
  and `directory_refresh_failed` (reason and error class only, never a message or
  stack) when the run cannot start. This supersedes REV-74's "not selected: events
  for the directory refresh". The stdout lines and exit codes are unchanged.
  OpenShift has no Fluent Bit yet, so the records reach the pod's stderr only.
- **Signals, not alerts.** Keep supplies the failed Job and these records; the team
  that operates the cluster sets the alert rules
  ([reliability 21](../specs/spec-reliability-operations.md#21-operational-alerting)).
  A freshness metric waits for REV-74's state collector.
- **Where it runs.** The OpenShift load-test bundle renders the CronJob suspended,
  with network-policy allowlists for its label. The local stack stays manual: local
  Start and `local-identity.ps1 -Action Refresh`.

Accepted risks: a failed, slow or cut-short run leaves the roots it missed up to
two days old until the next run or a manual rerun, and a failure never removes
access. ADAPI load is about two calls per group, plus one per 50 group members and
one per 50 tracked people, once a day. Scheduling, Forbid, the deadline and
environment precedence are checked through the rendered template only; no
OpenShift run has been made. Original issue IDs and REV numbering are unchanged.
Executed evidence belongs in delivery.

## REV-76 — Keep stops tracking disabled or deleted people (2026-11-17)

User decisions. The user's organization does not disable or delete user accounts
("my organization does not disable or delete users", 2026-11-17), so Keep stops
handling disabled or deleted people, and the user chose to remove that handling
entirely ([identity 3 and 6–11](../specs/spec-identity-configuration.md#3-username-and-password-authentication),
[tenant access 3–6](../specs/spec-tenant-access.md#3-grant-model-and-changes)):

- Sign-in no longer refuses a person whom ADAPI reports as disabled; Keep no longer
  reads `userAccountControl`.
- No sign-in and no directory publication ends anyone's sessions.
- A person absent from both ADAPI endpoints is no longer stored as a deleted
  tombstone.
- Deleted groups keep their handling ("keep groups", 2026-11-17): a group absent
  from both endpoints is still a tombstone, and its members lose that path.
- Exact single-person lookups use ADAPI `GET /users/user`. It takes the same query
  parameters as `/users` (`samAccountName=<name>` and repeated `attributesToLoad`)
  and returns the same row shape, as a list holding one object. Batches
  (`customFilter`) and picker searches stay on `/users`; exact group lookups stay on
  `/groups`. This has not been checked against the real ADAPI.
- When no person matches, `/users/user` answers 404 (user answer, 2026-11-17). Keep
  reads that 404 as "no row" without reading its body; every other non-200 and every
  malformed body stays "directory unavailable". A 404 caused by a wrong ADAPI path
  also reads as "no row"; since a missing person is never stored or negated, that
  only turns sign-in's 503 into 403 `account_not_in_directory` and a pick's 503 into
  422 (accepted risk, assistant-selected handling).

This supersedes REV-73's disabled check at sign-in, its rule that a disabled person
loses their other sessions, and its accepted risk that "a disabled person keeps
access until the next refresh or the end of their 24-hour session". REV-73's text
stays as history.

**Accepted risk (user decision).** If someone is disabled after all, AD refuses
their next bind, but an open session lasts to its 24-hour deadline, and they still
count as a group member (for example as a tenant administrator or an assignee)
until they are removed from the group. A deleted person drops out of a group's
members at the next refresh, because the members route stops listing them; their
direct grants stay.

Assistant-selected details (2026-11-17):

- **Every person is eligible.** The reader neither requests nor parses
  `userAccountControl`, so a missing or odd value no longer fails a read, and people
  are always written as eligible and not deleted. The `principals.eligible` and
  `deleted` columns and the read-side checks for `eligible AND NOT deleted` stay,
  with no migration: they still serve deleted groups and access lost through
  grants, and for people they no longer trigger.
- **A missing person.** A lookup still reports a person absent from both endpoints
  as not found, but publication neither stores nor negates them: no tombstone and
  no change to a stored row. No failure reason is added, because a new one would
  need a migration widening `last_failure`'s check. A pending pick of a missing
  person therefore does not fail the other people in its refresh evidence: the
  evidence completes and the pending row is deleted. Save on pick of a missing
  person returns 422 `principal_not_in_directory`, as for a missing group.
- **Old rows are lifted.** A person stored as ineligible or deleted by an earlier
  version becomes eligible through their next sign-in, a pick (a stored person is
  usable on pick only when eligible, so the pick reads ADAPI again), or a refresh
  that tracks them or a group they are in.
- **Sign-in.** A correct bind for a person with one ADAPI row signs in. No row
  still returns 403 `account_not_in_directory`, and two rows 403
  `account_ambiguous`. Sign-in keeps its stored-row check after publishing: when the
  stored row is still unusable (a newer publication fenced the sign-in's, or an
  older version wrote it ineligible during a rolling deploy), it returns a
  retryable 503 `sign_in_unavailable` and creates no session. The rejection reasons
  `account_disabled` and `account_ineligible` are removed.
- **The refresh** still re-reads people, for display names and to lift old
  ineligible rows; its roots are unchanged.
- **Local development.** The `local-disabled` test user and the mock ADAPI's
  disable and enable hooks are removed. The mock keeps ADAPI's response shape,
  including `userAccountControl`, and its removal hooks, and it serves
  `/users/user`.
- **The frontend is unchanged.** Its "Ineligible" label for a person becomes
  unreachable; removing it is a separate follow-up.

Rollback is a revert: the schema is unchanged and stored rows stay valid under both
versions; after a revert, people stay eligible until their next sign-in or pick
reads `userAccountControl` again. Original issue IDs and REV numbering are
unchanged. Executed evidence belongs in delivery.

## REV-77 — V1 alerts kept as sent, shown as v1, and Grafana v1 (2026-11-18)

User decisions. The user asked that v1 alerts not be translated into v2 words
("dont change the labels and values of the v1 alerts to match v2 … save the alert as
it is", 2026-11-17), that alert details and columns show v1 fields for v1 alerts,
and that Grafana can send v1 alerts ("it will send a firing alert and then a
resolved alert"). The user then chose ([alert operations 3, 4 and 10](../specs/spec-alert-operations.md#3-managed-field-catalog),
[operator operations 30](../specs/spec-operator-operations.md#30-grafana-webhook-to-native-v1-rev-77)):

- **Stored as sent.** A v1 alert keeps `object` and its severities `error`, `major`
  and `warning`. This supersedes the error→critical and major→high mapping and the
  mapping of `object` to `component`.
- **Resolve keeps the severity** (2026-11-17). A resolved v1 alert keeps its last
  real severity and only its status becomes resolved, as before.
- **Status stays** (2026-11-17). v1 alerts keep showing Status (firing, acknowledged,
  resolved). A Grafana `resolved` keeps the previous severity and is treated as
  status resolved.
- **Grafana v1 route** (2026-11-17). Grafana sends its standard webhook to a new
  unauthenticated `POST /api/ingest/v1/grafana`, into Global, with provider
  `grafana`.
- **Convert automatically** (2026-11-17). Stored v1 alerts go back to their original
  values, and Global's saved presets, maintenance windows and correlation rules are
  rewritten so they keep matching.
- **Accepted** (2026-11-18). Grafana rules on the same application, object and node
  become one v1 alert unless they send different `key_field` labels. Rewriting a
  Global correlation rule restarts it as an edit would: alerts from before stop
  counting toward it, and open grouped incidents stop collecting new alerts.

Assistant-selected details (2026-11-17 and 2026-11-18):

- **Storage.** Migration 0071 adds a nullable `alerts.object`, makes `component`
  nullable and widens the severity check to both versions' values. It rewrites no
  rows. v1 rows hold `object` with a null `component`; v2 rows the reverse. Tightening
  the check per version is left for later.
- **Search and rules.** CEL gains `object` in the feed, maintenance and correlation
  fields, and the `severity` enum becomes critical, high, error, major, warning and
  clear. Urgency puts error with critical and major with high; severity groups list
  critical, error, high, major, warning, clear. Preset columns, sort and grouping
  gain `object`. Proof and evidence omit an absent `object`, so proof recorded
  before this change stays byte-identical, and every reader of stored snapshots
  tolerates a missing `object`. The search index needs a rebuild for its new
  mapping.
- **Older rows.** Rule evaluation uses stored values as they are. Display and search
  show a v1 row stored before REV-77 in v1 words until the conversion reaches it.
  When a source update reaches such a row, the processor first converts it in a
  separate non-semantic step (cause `v1-native-conversion`), then applies the
  update, so no activity row reports the change of words and the proof chain stays
  continuous.
- **The conversion.** One idempotent command with `--dry-run` and `--reverse`. It
  rewrites Global's definitions first, through their normal save paths (new
  revision and history entry), using CEL parse positions rather than text search,
  and lists any expression it cannot rewrite safely. Then it converts v1 alert rows
  through the same non-semantic step, so a window whose expression was rewritten
  keeps suppressing the alerts it suppressed. History, proof and old revisions are
  never rewritten; old activity keeps its old words.
- **Grafana-to-v1 mapping.** Labels `application`, `object`, `node_name`, `operator`
  and `severity` are required, `key_field` is optional, the `message` annotation is
  required and `startsAt` becomes `time_created`. A resolved member becomes v1
  `clear`, so a first-seen resolved alert shows `clear` like a first-seen v1 clear.
  There is no routing label, because Global has no operators. Errors name the
  Grafana source, for example `labels.object`. The adapter version
  `keep-grafana-native-v1` is allowed only for v1, and `keep-grafana-v1` only for
  v2; the processor deploys before ingestion.
- **The UI.** Columns, sort, grouping and quick views follow the tenant: Global uses
  v1 fields (Object, Error/Major/Warning), specific tenants v2. Alert details follow
  the alert's schema version. Error and major reuse the critical and high colors.

Accepted risks: the Grafana v1 route is unauthenticated, the same exposure as the
native v1 route; a rule or window whose expression the conversion cannot rewrite
matches only old-word alerts until someone edits it; rolling back requires pausing
ingestion and the processor, running `--reverse`, then reverting code and the search
alias. Original issue IDs and REV numbering are unchanged. Executed evidence
belongs in delivery.

## Context catalog: current skill names and plan files — 2026-11-16

The user reviewed the workspace agent guidance and asked to drop the Codex wording
and the `codex/` branch prefix, naming new branches by the kind of work instead
(`feat/`, `fix/` and similar). The guidance itself lives in delivery; this repository
changes only where the catalog and the context guide named retired skills or an
undefined task checkpoint.

Assistant-selected details: the `change` intent points to `write-plan` and
`verify-work` and the `review` intent to `review-change`; the old `eng-deliver`
pointer is dropped because no current skill replaces it. The context guide names a
substantial task's plan file in `.plans/` at the workspace root as the place for its
objective, decisions, verification and unresolved dependencies. Navigation and
process wording only; no product requirement, issue ID or REV number changes.
