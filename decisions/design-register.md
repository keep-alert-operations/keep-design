# Design register

All 55 original issue identifiers are retained below. Status: **design closed** for the initial release. The domain specifications own the contracts; this index records coverage. [Delivery readiness](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/status/delivery-readiness.md#evidence-register) tracks implementation, supplied service facts and executed qualification separately. Record newly discovered gaps here without reusing or deleting an identifier.

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
| I2 | Independent status/assignment, lifecycle cycles, direct resolve, reopen conflicts and unchanged alert statuses remain incident operations 4/9/12/17–18; REV-46 adds resolution when all linked alerts resolve. Physical claims and transactions are system completion 15–17. |
| I3 | Active-only manual link/unlink/Move, <=100 explicit distinct IDs, atomic ownership and unavailable counterpart references remain incident operations 5–7/17–18; exact routes and tables are system completion 10/15. |
| I4 | 30-day qualifying inactivity/hourly expiry and 90-day latest-resolution retention remain unchanged. Source activity ordering and protected parent purge are complete in system completion 15/19–20. |
| I5 | Incident list/detail/current text search, notes/history, assignment and counters are selected in incident operations. System completion 8/10/15 completes token lookup, API routes, physical records and consistent reads. |

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
| REV-12 | U1, U2, U3, U5 | User supplied a full-system visual reference and requested the entire UI adopt it. Shared system section 3 records its left rail, typography and original fixed light palette, which superseded automatic OS theme selection at the time. REV-42 later replaces the colors with the Ocean palette and keeps the rest of the reference. REV-20 later adds user-selectable dark mode while retaining this light reference as default. Assistant-selected adaptations retain responsive stacking, real API data, existing authorization and conflict/recovery controls; illustrative prototype counts and people are not application defaults. See [UI mapping](https://github.com/appchi-alert-operations/appchi-frontend/blob/main/docs/ui-design.md). |
| REV-13 | U1, U5, I4 | User reported gaps between the implemented UI and the reference and asked for an exact match. Every screen now uses the reference page frame, grid tables and controls (see [UI mapping](https://github.com/appchi-alert-operations/appchi-frontend/blob/main/docs/ui-design.md)). Assistant-selected read-time enrichment adds optional current-directory labels beside principal ids — `assignee_display_name`, `acknowledged_by_display_name`, `created_by_display_name`, `updated_by_display_name` — plus `active_incident_id`/`active_incident_title` on alerts and `origin_rule_id`/`origin_rule_name` on incidents. These are presentation labels for current records; recorded history keeps its captured labels per REV-10. **Open gap:** incident activity stores only `actor_id`, so the UI cannot show captured actor names there without new persisted evidence; historical names are not rebuilt from today's directory. |
| REV-14 | Q4, U1, U5 | Continuation review found the redesigned table ignored saved/draft preset columns and always indicated descending last-received sorting. Corrected custom field order and actual sort indicators under the existing [preset column contract](../specs/spec-preset-operations.md#4-columns-and-sorting). Assistant-selected presentation adaptation retains the reference's compact default grouping and uses individual columns for custom selections; row navigation and suppression remain visible independently of Message. Added browser regressions, and scoped the saved-preview pagination assertion to its cursor request rather than the last concurrent count request. See [UI mapping](https://github.com/appchi-alert-operations/appchi-frontend/blob/main/docs/ui-design.md). |

## User sign-in direction — 2026-09-24

| Review ID | Original coverage | Resolution |
|---|---|---|
| REV-15 | A2, N2, U5 | User requested removal of the one-time-code step and username/password-only Appchi login. [Identity section 3](../specs/spec-identity-configuration.md#3-username-and-password-authentication) supersedes the earlier assistant-selected application TOTP requirement. Assistant-selected migration disables local application OTP execution/enrollment, preserves existing accounts and passwords, and requires protected password evidence in the backend. Separate Keycloak console MFA and production LDAP identity ownership remain unchanged; no shared service was modified. |
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
| REV-20 | U1, U5 | User requested dark mode after the full-system light visual reference. Shared system section 3 now requires an explicit Light/Dark choice for Appchi-owned screens, superseding REV-12's fixed-light behavior. Assistant-selected behavior retains the light palette (the Ocean palette since REV-42) by default, independent of OS preference, and persists the user's choice locally across navigation and reloads without identity or tenant data. Both palettes keep readable controls, status text and focus. External Keycloak pages retain their separate theme. |

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
| REV-23 | U1, U5, N2 | User approved implementing the Appchi login mock after requesting a custom form backed by Keycloak. The `appchi` client login theme supersedes minimal stock-page branding and REV-20's separate-theme limitation. Assistant-selected integration preserves Keycloak's generated form action, code flow/PKCE and console theme; only an initial 401 `unauthenticated` starts login automatically, preserving the requested local path. Explicit logout, expired callbacks, access denial and service failures retain recovery controls. Light/dark preference is local to each origin. Identity sections 1–2 and shared system section 3 record the contract. |
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
| REV-29 | Q2, U2 | User requested that alert CEL conditions use field names directly (for example, `application`) without requiring `alert.`. Assistant-selected compatibility retains `alert.field` for saved source, keeps the existing context allow-lists, and treats bare identifiers as additive within `appchi-cel-v1` because old expression meaning is unchanged. The editor, chips, functions, quick views and new examples use bare identifiers; stored source is not rewritten. |

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
| REV-33 | L1–L4, C1–C8, D1–D4, N1, R1–R4 | User accepted Kafka-first admission, no Appchi PG ingress dependency, transactional source changed+offset publication, tenant Kafka correlation order, ignored manual edits except resolve, inline maintenance effects, best-effort search hints with reconciliation, and actual Kong policy enforcement. [Kafka-first pipeline](../specs/spec-kafka-alert-pipeline.md) records all eight assistant-selected technical decisions and the accepted Kafka retention-loss limitation. Implementation/qualification evidence remains separate. |

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
[worker-scope implementation](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/docs/worker-scope-implementation.md).

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
GitHub organization, retain the original repository, use `appchi-frontend`,
`appchi-ingestion` and `appchi-migrations`, and work from a parent directory with
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
100 active users and 50 tenants. The [review evidence](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/qualification/scalability-review-2026-10-06.md)
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

- **A. Persistent compiler worker.** A long-lived process per Appchi process takes
  compile requests from a queue and is restarted after a crash or deadline. Open
  questions: one process would see sources from many tenants in turn, so recycling
  after N compiles or any error; concurrency and pool size; memory limits; eager or
  lazy start and shutdown. The deadline would no longer include process start.
- **B. Preloaded fork server.** Python's `forkserver` start method on Linux, with the
  compiler modules preloaded. Each compile still runs in a fresh child forked from a
  server that never sees expression text, so per-compile isolation and the deadline
  measurement stay as they are. Open questions: accepting one long-lived helper
  process per Appchi process; Windows development keeps `spawn`; behaviour of the
  native CEL module after fork must be qualified on the Linux image.
- **C. Keep spawn.** Rely on cache sizing; misses stay slow.

Assistant recommendation: B, after measuring miss latency on the supported Linux
image. Until a choice is recorded, each miss keeps a disposable spawned process
with the one-second deadline.

Assistant-selected under the existing CEL contracts: test, validation, search,
count and configuration save handlers keep fresh compiled instances, because they
build no native handle or one per request. Alert, incident and admin mutation handlers already prepare
inline with reused programs on each server thread, as the workers do.
`APPCHI_CEL_CACHE_ENTRIES` keeps its 4096 default with documented sizing guidance;
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
- The domain helper `appchi.shared.capacity` defines `UNLIMITED` as 2^53−1
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
  only `appchi.cel.compiler`. A spawned multiprocessing child re-imported the
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
- `python -m appchi.kafka_cutover --record-topic-identity` records the IDs for a
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
  [UI mapping](https://github.com/appchi-alert-operations/appchi-frontend/blob/main/docs/ui-design.md).
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
