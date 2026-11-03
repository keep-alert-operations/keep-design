# Dashboards

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

Shared dashboards display preset alert counts. This document defines editing, layout, count consistency, APIs and history.

## 1. Identity, names and permissions

Dashboards have immutable UUIDs and tenant ownership. Active names are unique within the tenant using the preset name profile: NFC, surrounding whitespace trimmed, 1–128 Unicode code points, full casefold comparison, control/format/line/paragraph separators rejected, capitalization preserved. Deleted names are reusable without transferring identity/history/references. Viewers read/explore; editors/admins create, change, copy and delete. No owner, private dashboard, folders, tags, favorites, archive, disablement or per-resource ACL.

## 2. Saved definition and initial state

Save name and an ordered collection of panels with immutable panel UUID, preset UUID, optional custom title, layout and color thresholds. A dashboard may contain zero through 24 panels; zero is a valid empty state with an Add panel action for editors. New dashboards start empty. Panels reference only active presets in the same tenant, always their **current saved queries**; repeated references are allowed. Panel identity remains stable across rearrangement and edits; copy/new panels receive new IDs. Save no time range, free-text search, suppression switch, refresh interval, fullscreen state or individual user's preference.

**Later user decision — 2026-11-03 (REV-57):** a panel has a type. `count` is the
panel described in this document. `html` has an optional title and sanitized HTML
content, references no preset and has no thresholds; it is never counted. A panel
without `type` is `count`. A panel keeps its type for its lifetime. Allowed HTML,
size and sanitizing rules are in [REV-57](../decisions/design-register.md#rev-57--dashboard-panel-types-and-html-panels-2026-11-03).

## 3. Panel titles and content

Without a custom title, show the current preset name; a preset rename updates that title automatically. Custom titles are optional trimmed NFC single-line text, 1–120 code points when present, using the same character exclusions as names. Clearing a title restores the preset-name default. Always expose the preset name/link even with a custom title. Show the exact logical-alert count, freshness state and an accessible explanation of color. Show zero only for a successful exact zero result. No abbreviated rounded number replaces the exact accessible value; use locale separators and allow a compact abbreviation only alongside the full value.

## 4. Layout and responsive behavior

Use a 12-column desktop grid. Panel width is 3 through 12 columns in steps of one; height is 2 or more grid units with no maximum other than the grid bound, each unit 48 CSS pixels, with 12-pixel gaps following the user's 2026-09-24 visual reference. Default panel is 3 by 2. Store integer x/y/w/h, nonnegative x/y, x+w <= 12 and y+h <= 100. Reject overlapping rectangles or duplicate IDs on save. Add places a panel into the first fitting row-major gap. Editor drag/resize may preview deterministic downward displacement, but the submitted whole layout must already be valid; the server does not silently rearrange it.

Below 1,024 CSS pixels, render two equal columns; below 640, one. Order is saved y, x, then panel UUID. Responsive display does not write the shared desktop layout. Provide keyboard Move up/down and keyboard width/height resizing with the same packing preview, focus retention and announcements. Counts remain readable at 200% zoom and controls do not require dragging.

**Later user decision — 2026-10-28 (REV-50):** panel width grows one column at a
time from 3 to the full 12-column row, and height has no maximum beyond y+h <= 100.
Width and height are set only by resizing on the grid; the panel create/edit dialog
no longer has Width and Height fields. This supersedes the fixed 3/4/6/12 widths and
2/3/4 heights above.

**Later user correction — 2026-10-08:** dragging and resizing should feel fluid,
like Grafana panels. Panels stick to the top: no panel may leave empty vertical
space above it unless another panel in an overlapping column blocks upward movement. The
frontend compacts upward after placement, resizing, creation, deletion and
reordering. Existing sparse definitions also display compacted, including viewer
and fullscreen views; opening alone does not enable Save or write a revision.
The next explicit changed-definition Save includes compacted coordinates.
This supersedes preserving empty vertical gaps in earlier layout guidance.

Assistant-selected presentation follows the pointer in CSS pixels while a
placeholder shows the valid compacted drop destination. Neighbor movement and
release settle smoothly; reduced-motion preference skips settling animations.
Stored widths/heights remain whole grid units within the allowed range. Vertical gravity keeps
x/width/height and panel identity, processes y/x/UUID order, and stops beneath
earlier horizontally overlapping panels; it does not pass through a blocker.
Collision displacement still prioritizes the edited rectangle, followed by
compaction and validation of the complete 100-unit layout. Escape/cancel restores
the pre-gesture draft. Count refresh does not rearrange the layout.

## 5. Colors and thresholds

Default is neutral for every value, avoiding an implied incident-severity mapping. A panel may define up to three increasing, distinct, nonnegative integer lower bounds with selected palette colors (`blue`, `green`, `amber`, `red`); the largest bound <= count applies. Bounds use exact integer arithmetic and the JSON decimal-string count representation. No arbitrary CSS, gradients, blinking, sounds or automatic action is accepted. A threshold is presentation only and never creates an incident, changes alert severity or sends a notification.

A text/accessible label states the matching threshold, so color is not the only signal. Loading/unavailable/stale states use a separate status marker; do not give an old result a fresh threshold status without its stale label. Preview thresholds locally against returned counts without saving shared changes.

**Later user decision — 2026-11-03 (REV-57):** HTML panels may carry the inline
style properties REV-57 allows, inside their own content area only. Thresholds and
count colors are unchanged.

## 6. Time, suppression and count meaning

There is **no separate dashboard time picker** in the initial release. Time restrictions belong to saved preset CEL, including its supported relative time expressions. All panels in a count batch share one captured database query time. Dashboards also have no Include suppressed switch initially: every panel uses default suppression exclusion outside CEL and no implicit lifecycle exclusion. The same saved preset therefore means the same query wherever referenced. Users inspect suppressed alerts through the feed's existing transient switch.

Count distinct retained logical alert rows, not occurrences, deliveries, notes or incident links, across the complete effective query. Preset sort/columns do not affect counts. Duplicate panels using the same preset share one query result. No aggregation over history, historical count chart or historical dashboard replay is introduced.

## 7. Drill-through

Clicking a ready panel opens its saved preset in the same tenant, with empty free-text search and Include suppressed off. Use the current saved columns/sort and a fresh feed snapshot; pass observed dashboard/preset revision and count observation as navigation context only. Label “Opened current results; count may have changed” when the new feed clock/revision differs. Do not promise that an evolving feed reproduces an earlier count, pin a hidden historical query, or modify the preset. Browser back returns to the dashboard and refreshes it. Support ordinary open-in-new-tab links. Loading/stale panels still allow opening an accessible preset; a deleted/inaccessible resource uses the ordinary 404/access-loss flow.

## 8. Shared editing, copying and conflicts

Editing creates a memory-only per-tab draft. Explicit Save commits the complete name/panel/layout definition in one transaction; Discard reloads the current saved revision. Read-only candidate validation/count APIs do not save or affect other users. Warn before voluntarily leaving a dirty draft; access loss clears protected state immediately. No autosave, collaborative cursor, field merge or forced overwrite.

**Later user decision — 2026-10-08:** edit directly on the regular dashboard
screen, without a separate dashboard editing modal or screen. Clicking the name,
with an adjacent pen icon, opens inline name editing. Create panel opens a dialog
for one panel; each panel's options offers Edit panel and Delete panel. Drag and
resize operate on the ordinary dashboard grid. Panel dialog Apply/Create updates
only the tab's draft. Save is enabled only when the complete definition differs
from the saved baseline, including name, panel creation/edit/deletion and layout.
Canceling a dialog leaves the dashboard draft unchanged; reverting all changes
leaves Save disabled. Saving restores
the saved baseline and disables Save again. These controls require edit access;
fullscreen hides editing controls. Existing draft, revision, conflict, access and
history contracts continue to apply.

**Later user decision — 2026-10-29 (REV-52):** the panel dialog chooses its preset
in one Saved preset field instead of a separate search box above a preset list.
Typing in the field searches shared presets by name and lists the loaded page in a
list that overlays the dialog below the field; a chevron marks it as a dropdown, and
choosing a preset shows its name in the field. First page and Next page sit at the
bottom of the open list. Preset paging, search and selected-reference rules are unchanged.

**Later user correction — 2026-10-09:** replace Pause updates with Discard changes
in the main dashboard toolbar. Discard requires edit access and is enabled only
for an unsaved draft while commands are unlocked; its existing confirmation and
current-saved-revision reload remain. Remove Preview draft counts from the UI.
The ordinary screen, new/history drafts and fullscreen expose no pause control;
count updates remain automatic, with manual Refresh counts available. Uncounted
draft preset references require explicit Save before displaying counts. The
existing read-only backend preview/validation contracts are unchanged.

Use expected dashboard revision and command UUID. Preserve the draft on 409 and offer Reload/compare or Save as new with an explicitly chosen unique name. A clean open dashboard loads remote saves; a dirty one keeps its base revision and says that a newer shared version exists, without revision numbers (REV-43). Duplicate uses the current saved definition or the explicitly selected draft, new dashboard/panel IDs, and the same currently active preset references, revalidated at save. Historical revision reuse is also a draft followed by a new validated save, never history mutation or undelete.

## 9. List, fullscreen and refresh controls

List dashboards by name then UUID, with name search, updated-at sorting, panel count and updated-by/time. Pages default 50/max 200, 15-minute live keyset cursor; collection change prompts refresh rather than mixing a frozen snapshot claim. Open a stable tenant/dashboard URL. Updates are live, using the shared SSE/invalidation and relative-clock refresh; offer Refresh now. Fullscreen is transient tab state. Hidden-tab behavior and permission/deletion rechecks continue; no pause control is exposed following the 2026-10-09 correction.

Assistant-selected query spelling: `sort=name|updated_at` and
`direction=asc|desc`, defaulting to name ascending; UUID ties remain ascending
in either direction. Both bind into the cursor. Deleted-history discovery uses
the newest retained definition's recording time for its updated-at sort/display,
without inferring erased final metadata. `panel_count` is an exact decimal string.

Fullscreen hides navigation and editor chrome but retains tenant, name, live/paused/degraded status, current time context and an obvious Exit control. It uses the ordinary human session and its existing idle/absolute expiry; there is no kiosk session, public sharing or tokenized read URL. Hidden-tab and reconnect behavior follows the shared live contract. No per-dashboard polling interval setting is saved.

## 10. Consistent count batches

For a saved dashboard count request, authorize and load dashboard revision plus all current preset definitions in one PostgreSQL repeatable-read transaction. Copy only authorized immutable definitions to the request. Capture the technical baseline's verified searchable position, index epoch, purge and maintenance completion generations **before** opening one Elasticsearch PIT. Capture one database query clock for every expression. Execute bounded size-zero searches with exact totals through `_msearch` against that same PIT, deduplicating identical preset query/profile contexts. Do not combine results from different PITs/clocks into one complete dashboard observation.

Recheck current dashboard/preset revisions, tenant access, purge generation, index epoch and maintenance completion before publishing the response. A mismatch discards the batch and returns 409 with a retry code; the browser coalesces invalidations and retries once from fresh state before showing Updating. Close the PIT on completion/failure; keep-alive is 30 seconds, long enough for the ten-second handler deadline plus cleanup, and never refreshed after the handler finishes. Track any replacement PIT IDs returned by subsearches and close all returned contexts best-effort; their expiry bounds uncertain cleanup. A count request does not create the five-minute feed traversal. PIT requests omit index/routing/preference overrides because the opened PIT supplies that context. See [Elasticsearch PIT](https://www.elastic.co/guide/en/elasticsearch/reference/current/point-in-time-api.html) and [multi-search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-msearch).

## 11. Partial failures, stale values and atomic display

**Current scope (REV-34):** Maintenance release fan-out and retention purges are deferred, so current automation does not produce the pending-fan-out or purged-alert cases below; see [worker scope](spec-worker-scope.md#5-nice-to-have-components). Batch provenance and stale/unavailable rules remain normative.

Response includes a batch observation ID, dashboard revision, preset revision map, query clock, searchable position, index epoch and per-panel success/error. A timeout/partial shard response is never an exact total. Successful siblings may be shown with their common batch provenance; failed panels show unavailable or their previous value explicitly marked stale with its old time/revision. Do not label a mixed success/stale display “all current.” The client installs the new successful panel set in one render pass and rejects late responses for old tenant/dashboard/draft/request IDs.

Assistant-selected response metadata: `relative` is a server-computed boolean
indicating whether any compiled referenced expression depends on the query clock.
It selects the existing one-second relative refresh behavior; it does not change
query semantics, revision checks or snapshot provenance.

If retention purged an alert since PIT capture, exact counts require a new PIT under the selected purge-generation contract; do not subtract the rows seen on one page. If maintenance fan-out is pending, label the snapshot Updating suppression; searchable position alone cannot claim completion. Elasticsearch failure leaves shared definitions and editing available through PostgreSQL. PostgreSQL authority failure prevents serving new protected results from cached definitions.

## 12. Count caching and load control

Initially **do not persist or reuse completed count results server-side**. Deduplicate repeated panels within a request, cache compiled expressions under the selected version/digest checks, and use one in-flight request plus a pending refresh per browser dashboard. This avoids authorizing a stale cached definition or freezing relative time. Connected foreground views coalesce changes in the live merge window of [technical baseline section 19](spec-alert-history-technical.md#19-browser-refresh-reconnect-and-relative-time) and refresh relative expressions on the selected one-second clock; static queries refresh on committed searchable/configuration/purge/maintenance changes and Refresh now. No empty periodic query runs merely to animate the clock.

Bound each request to 24 panels and the saved dashboard's actual references; draft previews have the same limit. Capacity-profile limits bound concurrent ES requests per process/tenant with fair scheduling and 429/Retry-After on exhaustion, preserving the existing p99 two-second count and five-second end-to-end objectives. A later cache requires a separately reviewed version/time/purge-safe design; it is not necessary for the initial system design. Qualify 24 distinct queries and repeated-preset cases under the selected concurrent-client workloads.

## 13. Storage and reference transactions

Use `dashboards` (UUID, tenant, canonical name/key, revision, created/updated actor/time, deleted-at), `dashboard_panels` (tenant/dashboard/panel UUID, preset UUID, custom title, grid integers, threshold JSONB), immutable `dashboard_revisions` (dashboard/revision and full canonical snapshot), and `dashboard_activity` (event UUID, before/after revisions, actor/cause/recorded-at). A `dashboard_name_claims` row uniquely owns `(tenant, name_key)` while active. Current panels use composite tenant foreign keys to dashboard/preset identities and an indexed `(tenant, preset_id, dashboard_id)` reference lookup.

Guard every dashboard create/save/copy/delete and preset delete with one short tenant configuration-reference guard. Acquire it before sorted preset identity rows and then dashboard rows; never acquire tenant coordinator after holding this guard. These operations do not mutate alert/correlation state. Replace the complete panel set atomically, enforce panel uniqueness/layout/threshold validation in the service and relational range checks, update name claims, history, command receipt, collection generation and live outbox together. No persisted dashboard panel can refer to a deleted/cross-tenant preset. Preset deletion rechecks the same live-panel table under this guard and remains blocked while references exist.

## 14. APIs

All paths use `/api/tenants/{tenant_id}`. Bodies have the common 64 KiB raw limit plus decoded field/panel limits. Return strong revision ETags.

| Route | Contract |
|---|---|
| `GET /dashboards`, `GET /dashboards/{id}` | Authoritative current metadata/definition. |
| `POST /dashboards` | Command UUID plus complete definition; 201. |
| `PUT /dashboards/{id}` | Command UUID, expected revision, complete definition; 200. |
| `DELETE /dashboards/{id}` | Idempotency-Key command UUID and If-Match revision; 200 receipt. |
| `GET /dashboards/{id}/history`, `/history/{revision}` | Current-authorized retained revision/activity, including deleted definitions. |
| `POST /dashboards/{id}/counts` | Expected dashboard revision; read-only batch observation, no command identity/history. |
| `POST /dashboards/preview` | Candidate definition plus referenced preset revision map; read-only validation/count batch for viewers. |
| `POST /dashboards/validate` | Read-only structure/reference validation, 200 valid/diagnostics. |

Counts read current saved queries, not client-supplied replacement CEL for a saved reference. Preview may use an unsaved layout but still only references saved presets; test new CEL through preset preview. History uses 50/default, 200/max and 15-minute watermark cursors. Common 400/401/403/404/409/413/422/429/503 distinctions apply. Same-value saves commit a receipt without a new revision/history event.

**Later user decision — 2026-11-03 (REV-57):** panel objects carry `type`
(`count` or `html`); `html` panels carry `html` instead of `preset_id` and
`thresholds`. Count, preview and reference routes consider `count` panels only.
Validate also reports the parts of HTML content that sanitizing removed. Saving an
existing panel ID with another type returns 422 `panel_type_changed`.

## 15. Deletion and history

**Current scope (REV-34):** Daily history cleanup is not deployed; expired history stays unreadable without physical deletion; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Deletion, retention windows and fences below remain normative.

Deletion is editor-authorized, revision-checked and confirmed with “Delete this shared dashboard”; it removes its current panel references and name claim atomically, preserving presets and alerts. Active URL becomes 404; history remains readable through explicit retained-history routes. A clean open view returns to the list with a deletion message; a permitted dirty draft may be saved as a new UUID after reference validation. There is no restore/undelete action.

Keep active configuration and minimal creator/editor metadata until deletion. Superseded revisions retain 90 elapsed days from supersession; activity 90 days from recording; final deleted definition/deletion event 90 days from deletion. Retained events hold their before/after snapshots. Command results last 90 days from completion. Pending dependencies extend only required records. Expired history is unavailable even before physical deletion; daily guarded cleanup targets 24 hours after eligibility. Minimal retired IDs/command fences and protected restore evidence follow system completion. Dashboard history contains references and presentation only, never retained count snapshots or expired alert payloads.

## 16. Accessibility and visual states

The user's dashboard refresh correction requires stable panel positions while
incoming alerts are processed. Assistant-selected presentation keeps routine
count refresh, indexing lag and suppression progress in the existing status line,
with a reserved width and a stable narrow-screen layout. Keep the last successful
counts, threshold colors and captured time while refreshing; an in-flight request
alone does not mark every panel stale or add warning banners. Failed or invalidated
observations still show their unavailable/stale state. No animation or added
refresh delay is needed.

**Later user correction — 2026-10-09:** remove the visible draft reminder,
preset-opening hint, drag/resize help paragraph and tenant/live/captured-time/
dashboard-revision status line. This supersedes the visible status-line
presentation above. Unsaved state remains clear through its chip and Save/Discard
controls. Preserve keyboard help through accessible handle descriptions and
visually hidden count status. The subsequent same-day user correction removes
the Count provenance button, details panel and reserved action row. Batch metadata
and revision/context checks remain internal to count processing. Count refresh
must keep panels steady. Visible count failures and stale/unavailable indicators
remain.

**Later user correction — 2026-10-26 (REV-43):** the dashboard header loses its
"Shared · revision · panels" subtitle and the standing Live pill; the Unsaved changes
chip sits beside the name. Dashboard list cards show the editor and a time relative
to now without a revision number, and a stale panel's captured time is relative too.

Use the system's selected light or dark palette, tabular numerals, visible focus, labeled count cards and text status alongside color. The visual reference and theme behavior are governed by [shared system section 3](spec-system-completion.md#3-navigation-and-visual-system). Announce an aggregated “Dashboard updated” politely after a batch; do not announce every second or every changed digit. Reduced-motion preference removes count transitions; do not animate counting through intermediate false values. A screen reader can read panel title, exact count, preset, freshness and threshold. Keyboard users can enter/exit fullscreen, open presets and operate all editing controls.

**Later user decision — 2026-11-03 (REV-57):** the panel dialog has a fixed size for
every type with a Panel type dropdown, settings on the left and a preview on the
right. An HTML panel is labeled by its title or "HTML panel"; its content allows
headings `h3`–`h6` only so it cannot break the page's heading order, and its content
area scrolls without growing the panel.

## 17. Acceptance and observability

See [required dashboards checks](../verification/verification-plan.md#dashboards).
