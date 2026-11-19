# Presets

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

Shared saved feeds: configuration, editing, queries, dashboard references, APIs and history.

## 1. Identity, ownership and permissions

Give every preset an immutable server-generated UUID and immutable tenant ID. Renaming never changes links or dashboard references. A preset cannot move between tenants. Creating a tenant creates no default preset.

Tenant view permission permits listing, opening, temporary adjustments, previews, reference inspection and retained history. Edit or higher permits creation, saving, renaming and eligible deletion of any preset in that tenant; the creator has no exclusive rights. Global follows its existing universal authenticated edit permission and global-super-admin administration policy. No private copies, per-preset ACLs, folders, tags, favorites, archive/disable lifecycle or cross-tenant copy operation are included in the initial preset design.

## 2. Names and reuse

Require a unique active preset name within its tenant. Apply the tenant-name validation profile: trim surrounding Unicode whitespace, normalize display text to NFC, require 1–128 Unicode code points, reject control/format characters and line/paragraph separators, and compare NFC-normalized default full case-folded keys. Preserve display capitalization. Names in different tenants may match.

Enforce the name claim transactionally on create/rename. Release a former name after successful rename/deletion; a failure keeps it reserved. Reuse creates no identity, history or dashboard-reference inheritance. Deleted records display their original name and UUID even when a newer preset uses the same name.

## 3. Saved definition and initial defaults

The editable definition is exactly `name`, `cel`, `sort`, `columns` and the optional `group_by` that REV-44 adds (null means no grouping), and the `noisy` alarm flag that REV-58 adds (false means silent). Keep server-owned `id`, `tenant_id`, monotonic `revision`, CEL environment version, creator/last-editor identities and creation/update instants separately. Record UTC instants and render using the application's display timezone. Preserve immutable actor IDs and display snapshots when an LDAP identity is later renamed/deleted; these metadata do not confer ownership.

The new-preset form starts with CEL `true`, sort `timestamp` descending with alert ID ascending as the final tie-break, and these ordered columns: `severity`, `display_status`, `message`, `application`, `component`, `timestamp`, `assignee_id`, with no grouping and no alarm. A name is required before creation. Explicitly label `true` as all retained alerts subject to the current suppression switch; do not add a hidden firing-only or date condition. No preset is persisted merely by opening this form.

**Alarm (REV-58).** A noisy preset loops the shared alarm sound while its results page is open in a browser tab and that view's exact total is above zero. The alarm stops when the exact total is zero, the page closes or a saved revision turns the alarm off. A loading or unavailable total keeps the previous state; it never counts as zero. The total is the one the page shows, so transient search text, quick views and the suppression switch affect it. The results page shows a Noisy marker, which moves while the alarm sounds, and the preset list marks noisy presets. Mute silences only the current tab until the preset is reopened or the tab reloads. Muting changes nothing shared and is not stored. When the browser refuses sound until the page receives a user gesture, the page says so and starts the alarm on the next click there. The editor's Sound tab sets the flag and plays a sample. Editor previews, the Feed and dashboards never play the alarm, and dashboard counts are unchanged.

**Later user decision — 2026-11-19 (REV-78):** dashboards now play the alarm for their noisy panels, once per dashboard tab, with a mute per panel ([dashboard section 16](spec-dashboard-operations.md#16-accessibility-and-visual-states)). This supersedes "dashboards never play the alarm" above; editor previews and the Feed stay silent and dashboard counts are unchanged. The Sound tab's notes read "Play an alarm while this preset, or a dashboard panel showing it, is open and alerts match" and "Everyone who opens this preset or such a dashboard hears it until no alerts match or they mute it". See [REV-78](../decisions/design-register.md#rev-78--noisy-presets-sound-on-dashboards-2026-11-19).

## 4. Columns and sorting

Allow 1–30 distinct ordered columns from the searchable scalar fields in alert supplement 3, including `active_incident_id`, but excluding the collection `incident_ids`, internal revision/projection/history metadata and nested history/raw payloads. Canonicalize the supported `last_received_at` alias to `timestamp` before duplicate detection/storage. The mandatory row-open control and suppression indicator remain visible independently of selected columns and do not consume a column slot.

Allow 1–3 distinct user sort fields, each with `asc` or `desc`, from the existing sortable whitelist in alert supplement 24. Append alert ID ascending internally; users do not replace that tie-break. A sortable field need not be displayed. Preserve severity ordering, clear last and null last in either direction and the existing scalar ordering rules. Reject unknown/duplicate fields or an empty sort/column list. Column widths, density, horizontal position and selection are transient, not additional saved settings.

On saved preset results, clicking a supported sortable column heading temporarily replaces the entire saved sort with that field ascending, then descending on a second click; a third click restores the saved sort. Clicking a different supported heading starts its ascending cycle. This is a read-only view choice, never a shared preset edit or dirty definition draft. Each change restarts result pagination on page one and clears selection. A new preset revision or reopening the preset clears the override. Headings without a supported sort field remain static.

For current presentation, Status means `display_status`; the editor offers no separate acknowledgement columns. Assistant-selected REV-27 adaptation maps legacy `status` and `acknowledged` columns to a single Status column in their first position, removes old acknowledgement actor/time columns and preserves the other column order. If nothing remains, show Status. Apply this to current results and editor drafts without rewriting stored or historical revisions; an explicit normal save persists the adapted columns. Historical definitions remain readable as recorded. Raw lifecycle sorting is labelled Lifecycle; `display_status` sorting is unsupported. Existing acknowledgement sorts remain executable and visible as Legacy acknowledgement only when already selected.

**Grouping (REV-44).** `group_by` is null or one of `severity`, `display_status`, `name` (REV-54), `application`, `component`, `node_name`, `site`, `assignee_id` and `active_incident_id`; reject any other value. Grouped results show one table per distinct value of the effective result. Each table has the value, an exact alert count, a summary (visible-status counts for severity groups, severity counts otherwise), its own column headings and selection of its shown rows, and omits the grouped column. Rows inside a group follow the effective sort and tie-break. Severity groups follow the severity order with clear last, Status groups show Firing, Acknowledged then Resolved, and other fields show the most alerts first, then the value in Unicode scalar order. Alerts without a value form the last group. A result with more than 1,000 distinct values returns `422 too_many_groups`, and the view keeps its single table with that explanation.

Each group initially shows 5 rows and continues within the same snapshot; the first 10 groups show initially and further groups continue from the same snapshot. On saved preset results, the toolbar changes grouping for the current view only, like a sort override: it is a read-only view choice, offers Reset back to the saved grouping (labelled Reset by REV-45), restarts the snapshot and clears selection. A new preset revision or reopening the preset clears it. Collapsed groups and extra loaded rows or groups are transient.

## 5. CEL validation and compatibility

Require nonblank UTF-8 CEL source no larger than 16 KiB and a boolean result under the shared versioned environment. Reference catalog fields by bare identifier in new expressions; the accepted `alert.field` compatibility spelling remains valid for previously saved source. Preserve source text exactly rather than rewriting string literals or treating superficially similar expressions as equivalent. The initial form supplies `true`; the API rejects a blank expression rather than silently broadening it.

Run the shared parser, type checker, allowed-field/function checks, search-translation checks and bounded-cost validation on preview and every save, including a revision copied from history. Return field/source spans and actionable errors without mutating the stored preset. The size limit is an additional preset input bound, not permission to exceed shared CEL depth, cost or execution limits. Technical supplement 2–7 now selects the common language/runtime, field/operator restrictions, timestamp/clock behavior and cost accounting. Its feed-only `now()` is captured per snapshot; measured numerical deployment cost budgets remain qualification outputs. These shared limits apply in addition to this preset envelope.

Store the validated environment version with each revision. Before a shared-language rollout, check active presets for compatibility and provide a validated migration or retain the supported execution environment; do not silently change query meaning. If a stored definition cannot execute, show an unavailable-query error for that preset and permit authorized repair. Never replace it with `true`, drop a predicate or scan the retained dataset in application memory. Reading historical source does not require executing its old environment.

## 6. Transient filters and effective results

The effective feed filter is authorized tenant scope AND applied CEL AND transient plain-text `q` AND suppression policy. Preserve `q`'s 256-code-point plain-text contract and `include_suppressed=false` default. Neither field, a cursor/page, selection nor an independent time range is saved in a preset. The initial preset/feed UI has no separate time picker; date filtering uses the supported CEL language. Dashboard section 6 defines no independent dashboard time picker.

An expression asking for suppressed alerts still requires the explicit Include suppressed switch. Reopening a preset resets `q` to empty and suppression inclusion to false. Rows and count use identical effective filters and captured query context. Count logical alerts over the whole matching result, not the loaded page, occurrences or history events. Return an exact count for the reported search snapshot or mark it unavailable/updating; do not label a capped lower bound or failed request as an exact count or zero. This specifies preset results, not a dashboard batching/cache implementation.

## 7. Listing and opening

Use immutable UI links `/tenants/{tenant_id}/presets/{preset_id}`. Provide a tenant preset list with name, last editor and last modification time; creator and full identity metadata are in details/history. Default to active presets ordered by canonical name then UUID. Provide a literal case-insensitive name-substring filter of at most 128 code points and an explicit Deleted history view.

Metadata lists use 50 items by default, at most 200, and opaque 15-minute cursors bound to tenant, filter, state, ordering and the preset collection revision. A collection change requires restart with `409 list_changed`; expiry gives `409 cursor_expired`. The UI preserves the user's filter when restarting. These are configuration-list cursors, distinct from the existing five-minute alert-result snapshots. An empty tenant shows an empty state and a Create action only for editors; do not invent a default saved preset.

## 8. Explicit shared saves and temporary drafts

Opening a preset runs its saved definition. Query typing edits a local draft; Run or Ctrl+Enter applies a valid query to the current feed. Sort and column adjustments apply locally. None of these actions writes shared state. Show an Unsaved changes marker and, for editors, explicit Save, Save as new and Discard changes actions. Save as new requires an explicitly entered unique name and creates another tenant-wide preset, never a personal copy.

Save validates and persists the editor's current name/query/sort/columns/grouping/alarm setting atomically, even if the query has not been run. It also applies that saved definition locally and starts a fresh result traversal. Preview success is not a prerequisite for saving valid configuration. Clearly show that free-text search and Include suppressed are not saved. Discard reloads the current shared definition and clears its definition draft; it leaves transient search/suppression choices unchanged until a preset is reopened.

Keep drafts in memory per browser tab; do not persist personal settings/drafts in Keep, browser local storage or shared links. Voluntary navigation that would discard a definition draft offers Stay/Discard and Save when authorized; navigation proceeds only after a requested save succeeds. A browser-reload warning is best effort. Tenant access loss takes precedence over draft preservation and clears protected state under the tenant/access contract.

## 9. Preview and editor feedback

Provide field/type autocomplete from the approved alert catalog and the shared environment's supported operators/functions. Validation identifies the failing field or source span. Run is a read-only preview of retained current alerts using the normal feed page/count contract; it neither saves a preset nor simulates past alert states, triggers correlation/maintenance or modifies alerts.

Do not run a search on every keystroke. Empty matches are a valid result. Distinguish validation error, loading, no matches, indexing lag and search unavailable. Keep the previous successful results visibly labeled with their previous applied query while a replacement is loading or fails; never label them as results of the failed draft. Unsaved definition changes are not counted as preset revisions/history events.

## 10. Revisions, concurrency and retries

Creation starts revision 1. Every changed saved definition or deletion consumes the next revision; exact no-ops create neither a new revision nor a history change. Compare canonical stored fields, while CEL source changes count even if their meaning appears equivalent. Require `expected_revision` for update/delete and a client command UUID for every mutation. Check the expected revision before treating a write as a no-op.

Use command identity scoped to tenant, acting principal, operation and target (the create operation has no preexisting target). The same ID/body retries the committed result; reuse with different content returns `409 idempotency_conflict`. Reauthorize retries under current access before exposing the result. Receipts are not evidence that their old revision remains current, and retries never recreate a subsequently deleted preset. Preserve complete committed command results for 90 elapsed days; afterward a minimal fence returns `409 command_result_expired` instead of reexecuting an old command.

A concurrent edit gives `409 revision_conflict` with the latest readable revision and changed-field summary. Keep the local draft and offer comparison, reload/discard, or Save as new. Do not automatically merge or overwrite another editor's work. A deliberate later save uses the newly reviewed current revision. A reference change during deletion follows decision 13 and cannot be bypassed with a retry.

## 11. Revision history and reuse

Record immutable created/updated/deleted events with command identity, revision, actor/display snapshot, recorded UTC time, changed fields and the retained before/after definition references. Show revisions and side-by-side field/query changes to tenant readers; do not put ordinary preset content into the admin-only tenant access audit.

For an active preset, Use this revision loads a retained historical definition into an editor's draft. Saving it uses ordinary current validation, name uniqueness, current permissions and expected-revision checks and creates a new revision. History never moves backward. A deleted preset has read-only history and no undelete action; an editor may use its retained definition through Save as new with a new UUID. This does not repair/rebind old links automatically. Viewers may inspect history but cannot persist these actions.

## 12. Dashboard references and saved edits

Dashboard panels reference the immutable preset UUID in the same tenant and execute its current saved query. They do not pin a historical revision or use a user's unsaved draft, free-text search or suppression switch. Existing default counts exclude suppressed alerts, have no implicit lifecycle/time restriction and obey the shared current permission checks. Reusing one preset in multiple panels is permitted by this reference contract; dashboard completion selects panel layout and presentation.

A saved CEL change causes all referencing panels to request counts for the new revision. Rename updates the referenced preset label; any separately configured panel title remains the dashboard's concern. Sort/column changes do not change which alerts a panel counts. Show count provenance by preset revision and search freshness. During replacement, either show a clearly marked previous value with its old revision/time or show loading/unavailable; never display an old-query count as current or flash zero on failure. No implicit query copy or silent reference removal is permitted.

## 13. Deletion and reference races

Editors may delete an unreferenced preset after an explicit confirmation naming it. Block deletion while any current dashboard panel references it, returning `409 preset_in_use` and an authorized reference count/link to the paginated references view. An editor removes/replaces those panel references through dashboard editing first. Historical dashboard references are minimal provenance, not live blockers, and must not resurrect deleted preset content. Open feed tabs are not persistent reference blockers.

Atomically serialize reference creation/replacement and preset deletion using the same authoritative PostgreSQL preset/reference guard. A dashboard write must recheck that the target is active and in its tenant at commit; a delete must recheck both revision and live reference absence. The two operations cannot both succeed with a dangling reference. On deletion, atomically record the tombstone/history/receipt, release the name and emit a durable configuration-change event. Keep retained history separate from active resources; old active URLs return 404. Never cascade-delete panels or dashboards.

## 14. Open views, live changes and access changes

For a clean open feed, a newer saved preset revision reloads the definition and reruns results when the view is foreground. A dirty view retains its local definition, identifies its base revision and shows that the shared preset changed; no remote edit overwrites the draft. A late response is accepted only when tenant, view request, effective query context and relevant revision still match. A definition/filter/sort/grouping change starts a new five-minute alert snapshot; pages never mix revisions. Column-only local changes need not restart a snapshot. New arrivals use the existing refresh semantics rather than shifting a traversal mid-page. A grouped view refreshes like a first page while every group shows only its first rows and only the first groups are loaded; after more rows or groups load it keeps its snapshot and offers refresh.

If an unreferenced preset is deleted while open, show Deleted and stop treating the view as a saved preset. While tenant read access remains valid, its in-memory definition may continue as a clearly labeled unsaved feed and editors may Save as new. Full tenant access loss clears it; reduction to view removes persistent actions while retaining allowed temporary exploration. Apply server authorization to every read, count, preview, history/reference page and mutation, including commit-time mutation guards. Identity outages retain the previously selected last-known-data authorization behavior; this does not authorize stale preset configuration.

Configuration invalidations are hints backed by committed PostgreSQL revisions/outbox records. The saving user's authoritative response applies immediately. Other foreground views refetch when notified and after reconnect/refocus; losing live delivery must show the selected stale/disconnected state. Technical supplement 4/18–21 defines relative-time refresh, SSE/Redis transport, durable generation reconciliation, reconnect/fallback behavior and observation contracts.

## 15. Logical storage and transactions

Use PostgreSQL for current preset definitions, tenant-scoped name claims, immutable revisions/change events, live dashboard-to-preset references, command receipts/fences, deletion markers and durable configuration-change outbox records. The preset collection has a monotonic revision for metadata-list consistency. Create/update/delete atomically commits its definition/name changes, history, collection revision, command receipt and required outbox record. An exact no-op only commits its receipt. Do not make a successful save depend on Elasticsearch or Redis availability.

Elasticsearch continues to hold searchable alert projections, not authoritative preset definitions/history. Preset edits never rewrite alert source data, re-ingest alerts or trigger correlation/maintenance rules. System completion 14/17–18 selects physical tables, constraints, lock/index choices and relay integration; implementation must enforce the logical uniqueness, authorization and reference guards above.

## 16. API surface

All routes below are under `/api/tenants/{tenant_id}` and use the existing human-session, CSRF and tenant authorization contracts. Reject client-supplied tenant ownership/server metadata and unknown mutation fields. Mutation bodies are at most 64 KiB of UTF-8 JSON; CEL retains its smaller 16 KiB bound.

| Route | Selected contract |
|---|---|
| `GET /presets` | Active metadata by default; `state=active` or `deleted`, optional `name`, `limit`, `cursor`. Deleted results include only retained deletion history. |
| `POST /presets` | Required command ID plus the definition fields, where an omitted `group_by` is null and an omitted `noisy` is false; create and return 201 with committed definition/revision. |
| `GET /presets/{id}` | Current active definition/metadata; retained deleted records use history routes. |
| `PUT /presets/{id}` | Command ID, expected revision and complete definition replacement, where an omitted `group_by` is null and an omitted `noisy` is false; return 200 with committed definition/revision. |
| `DELETE /presets/{id}` | Required `Idempotency-Key` command UUID and `If-Match` quoted revision; return 200 deletion receipt after commit. |
| `GET /presets/{id}/references` | Current dashboard IDs/names, panel IDs and total reference count, 50/default and 200/max paging; bound 15-minute cursor to reference-set revision. A changed set requires restart. |
| `GET /presets/{id}/history` | Retained changes/revision metadata, including a tombstoned preset; descending recorded time/revision, optional UTC from/to and 50/default, 200/max pages. |
| `GET /presets/{id}/history/{revision}` | Retained read-only definition/change detail, including deleted presets; expired content is unavailable. |
| `POST /presets/validate` | Read-only validation of a candidate CEL/sort/columns/group_by definition, accessible to viewers; return validation result/environment version without search or history mutation. |
| `POST /presets/preview` | Read-only feed execution of either an active preset ID/revision or an explicit CEL/sort/columns/group_by candidate, plus optional `q`, `include_suppressed`, limit/cursor. Saved and candidate forms are mutually exclusive. With `group_key` or `group_empty=true`, rows are those of one group of the effective grouping. |
| `POST /presets/preview/groups` | Grouped execution of the same saved or candidate forms: exact group totals, summaries and the first rows of each shown group from one snapshot. `group_limit` 10/default, 50/max; `rows_per_group` 5/default, 50/max, at most 200 rows in all; `group_cursor` continues the group list. A definition without grouping returns `422 grouping_required`. |

Create/update JSON uses `command_id` and update additionally uses `expected_revision`; DELETE headers carry the equivalent fields. Read/command responses provide the active resource revision as a strong quoted ETag. Preview of a saved preset requires its observed revision; if it has changed, return `409 preset_changed` so the client reloads or explicitly uses a candidate draft. Preview returns normal alert rows, exact-or-unavailable total, cursor, applied query/environment context and indexing/freshness metadata. It reuses the selected alert search service and snapshot rules; it creates no second search semantics or privileged route. Preview limits are 50/default, 200/max; cursors expire after five minutes. Validation/preview bodies share the 64 KiB envelope and expression limits.

History cursors fix an upper recording watermark, expire after 15 minutes and reapply authorization/retention on every page; new changes do not reshuffle an existing traversal. References and history disclose nothing across tenant boundaries.

## 17. Errors and user recovery

Use the existing status distinctions: 400 malformed JSON/parameters; 401 absent/expired session; 403 a visible tenant resource with a forbidden action; 404 inaccessible/cross-tenant/nonexistent active resource or expired history; 409 name, revision, reference, cursor or idempotency conflict; 413 oversized body; 422 invalid definition; and the existing 429/503 capacity/dependency contracts. A well-formed validation request returns 200 with `valid=false` and structured diagnostics for an invalid candidate; save/preview returns 422 for that invalid definition. Include a stable code, message, relevant field/source span and request ID; omit inaccessible resource identities.

Keep a failed save's draft. Explain name conflicts and reference blockers beside the action that failed. For an uncertain mutation outcome, retry with the same command ID and body, then read the authoritative resource; never manufacture another create/save command automatically. Search failure does not imply save failure. Do not report a successful deletion until its PostgreSQL transaction commits.

## 18. Retention, purge and recovery

**Current scope (REV-34):** The daily purge job is not deployed; expired history stays unreadable but is not physically removed; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Retention windows, fences and restore rules below remain normative.

Current active definitions and their minimal current creator/last-editor metadata persist until deletion. Retain each superseded definition for 90 elapsed days from supersession; retain change-event details for 90 elapsed days from recording. Deletion starts a 90-day retention period for the final definition and deletion event. Do not restart the lifetime of already superseded revisions merely because the preset was deleted. Retain stable actor/display snapshots with their parent record, not indefinitely in a separate directory copy.

A retained change event must have its referenced before/after content for its own lifetime. Extend only the records needed by a still-pending command, retained dependency or recovery proof; current dashboard references ordinarily require only the current definition. Purge eligible history/receipts through a daily rechecked job targeting cleanup within 24 hours of eligibility. Expired records with no hold are unavailable to product reads even before physical cleanup. Never purge active definitions based on their age or purge proof while its consumer still needs it.

Retain minimal retired preset UUID/tenant/deletion-revision markers and command replay fences until a separately verified safe compaction protocol permits removal. These contain no CEL, name, actor display text or old response bodies; no safe finite tombstone horizon is assumed. Reconcile protected deletion/replay evidence after rollback restore before serving preset configuration or references so an old backup cannot silently reactivate a deleted preset or retired command. Dedicated teams continue to own backup infrastructure and physical retention; Keep supplies these application recovery requirements. The separate 365-day tenant/access audit does not extend preset content history automatically.

## 19. Caching, availability and bounded work

Authorize and load active preset/reference state from PostgreSQL on saved-definition requests. Cache compiled expressions only by tenant, preset UUID/revision, source digest and CEL environment version, after checking the current authoritative revision; cache candidate compilation by tenant/source/environment. A cache hit cannot bypass permission, deletion or environment checks. Redis loss cannot undo a save or authorize a removed resource. No persistent cache of preview rows/counts is introduced by this design; dashboard completion 10–12 selects same-PIT/clock batches with no persisted count cache.

If PostgreSQL authority is unavailable, return dependency errors for preset reads/writes; a stale cache cannot authorize or replace them. If Elasticsearch is unavailable, configuration reads/history and valid saves can continue, while previews/counts show stale or unavailable results. Preserve the reliability supplement's ordinary ten-second Product API handler budget, fifteen-second requested gateway budget, p99 one-second authoritative detail/local-command objective and p99 two-second list/search/count objective. These remain unqualified targets. Bound list/reference/history responses and previews as above; no initial bulk preset mutation, bulk export, unbounded preview or additional hard preset-count cap is selected. Qualify realistic preset/query/panel populations before claiming capacity.

## 20. Acceptance

See [required presets checks](../verification/verification-plan.md#presets).
