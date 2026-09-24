# Incidents

Severity cannot change after creation; status and assignment are independent; correlation-created incidents start unassigned; incidents have no owning team; one active incident may own an alert; reopening is blocked by ownership or originating-rule/group conflicts; resolving an incident leaves alert statuses unchanged and requires fresh transitions for later automatic reuse; suppression preserves links; unchanged repeats do not reset incident inactivity. There are no notifications, incident acknowledgements, or automatic resolution merely because every linked alert resolved.

## Creation, content, assignment, and lifecycle

### 1. Creation and origin (I1)

Manual creation requires a title and explicit severity (`critical`, `high`, `medium`, or `low`); description and initial alert selection are optional. There is no preselected severity because it becomes immutable. Manual incidents start `open` and unassigned; assignment is a subsequent action. Correlation-created incidents also start `open` and unassigned. Creation plus any requested initial links succeeds or fails together. Creation origin is immutable: a manual incident cannot be adopted as a correlation rule's incident, and manually adding alerts never changes incident origin or grouping context. No empty placeholder incident is left after failed creation.

### 2. Text validation and generated content (I1, I5, C4)

Trim surrounding title whitespace; require a single-line title of 1–200 Unicode code points. Duplicate incident titles are allowed; identity uses the incident identifier. Descriptions are optional plain text up to 10,000 code points, with line breaks preserved; an omitted description is empty. Render content as text, without HTML or Markdown interpretation. These limits apply to manual content and subsequent edits. For automatic titles, use the rule name alone without grouping, or the rule name followed by configured grouping fields in their configured order as `field=value` pairs.

Separate the rule name from grouping text with an em dash and separate pairs with commas; replace generated line breaks with spaces. Render values as text and retain the full typed grouping context independently; titles never determine group identity. Truncate an oversized generated title to 199 code points plus an ellipsis. Rule-provided descriptions use the same 10,000-character limit and are validated on rule creation/edit. Require explicit rule severity selection with no preselected value.

These formatting/validation decisions do not change rule matching or overwrite existing incident content on later rule edits/additions. Grouping fields use the alert catalog and shared CEL type profile.

### 3. Assignment and permissions (I5)

Any user with effective tenant `edit` permission or higher may assign, reassign, or clear assignment on an active or resolved incident. Assignees must satisfy the already agreed effective-edit eligibility rule; picking a user grants no access. Offer an explicit Assign to me action and an unassigned option, with no automatic assignment on investigation or reopening. Reopening preserves the assignee if still eligible. Revalidate actor permission and assignee eligibility when the change is committed. On detected permission loss, clear only the still-ineligible current assignee, preserve history, and leave status and links unchanged. Automatic eligibility cleanup does not count as incident activity. Identity supplement 6–11 selects shared freshness, outage and eligibility-cleanup configuration; its five-minute normal-operation target and last-known-data policy apply here. Do not introduce a separate incident-specific polling interval.

### 4. Lifecycle cycles and timestamps (I2)

Keep immutable creation time and a separate lifecycle cycle for initial creation and every successful reopening. Each cycle records opened time, first entry into `investigating` (nullable), resolution time (nullable), and resolution cause (`manual` or `inactivity`). Returning from investigating to open preserves that cycle's first-investigation time; investigating again does not overwrite it. Reopening starts a new cycle with fresh opened time and empty investigation/resolution values, while retaining earlier cycles. Keep the latest status-change time and append each real transition with actor and timestamp. A repeated request for the current status is a no-op. System expiry uses `resolved`, not a fourth lifecycle status. No resolution note is required; users may add one separately.

## Alert links and moves

### 5. Linking and unlinking (I3)

Link changes are allowed only on active (`open`/`investigating`) incidents; reopen a resolved incident before changing its membership. Within the same tenant, users with edit permission or higher may manually link firing or resolved alerts, including acknowledged and suppressed alerts. Manual linking does not require a correlation-condition match. It cannot steal an alert from another active incident. Linking an already-linked alert or unlinking an absent link is a no-op. A successful unlink ends current membership but preserves the link/unlink history and establishes the previously agreed fresh-transition boundary for automatic correlation. It does not change alert status, suppression, assignment, or incident status; an empty incident remains available under the settled rules.

### 6. Explicit moves and selections (I3)

Offer an explicit Move action between two active incidents in the same tenant. Validate both incidents and all selected alerts, then transfer ownership atomically: end source membership, establish the unlink boundary, and add destination membership without an intermediate unowned state visible to other transactions. Manual destination attachment is allowed despite that automatic-reentry boundary. No implicit move occurs during ordinary Link. A multi-alert link/unlink/move request is all-or-nothing, with at most 100 distinct alerts per request, including initial manual-creation selection; reject duplicates in the submitted selection. This limit does not cap automatic correlation additions, which retain the agreed all-eligible-alert policy. On conflict, identify conflicting alerts and their accessible active incidents and change nothing. Limit this initial bulk support to alert membership; mass incident status/assignment changes are not included.

### 7. Linked-alert presentation (I3, I5)

The incident detail shows all linked alerts, including resolved and suppressed ones, and their status, suppression indicator, and history access. Display `total linked` and the suppressed subset distinctly, counting each logical alert once. The manual-selection dialog offers an explicit Include suppressed toggle, off initially; selecting a suppressed alert never clears suppression. Use the managed catalog in the [alert supplement](./spec-alert-operations.md); do not invent additional source fields.

Cross-tenant alerts are neither discoverable nor selectable. After counterpart retention purge, show a minimal unavailable-reference entry rather than silently losing the relationship; distinguish its unknown current state and show the unavailable subset separately from the known suppressed subset. Link-reference totals remain distinct logical identifiers, including unavailable references. Unavailable references are historical only: they cannot be claimed or moved. Reopening checks actual retained alerts for ownership conflicts, retains unavailable references as history, and never recreates purged alerts.

## Notes, audit, and incident inactivity

### 8. Incident notes (I5)

Users with tenant edit permission or higher may add, edit, and delete any incident note, including on resolved incidents. Notes are plain text, limited to 10,000 Unicode code points, and must contain non-whitespace content. Preserve line breaks and display text safely. Editing appends a revision; deletion hides the current note and adds a deletion record rather than erasing prior revisions. Incident readers may inspect the revision/deletion history, with actor and time. Search only current, non-deleted note text. Alert-note policy is independently selected in alert supplement 18 and preserves the same editor/revision/search rules.

### 9. Audit and accountability (I2–I5)

Record incident creation, effective content/status/assignment changes, note revisions/deletion, link/unlink/move, reopen, and automatic expiry. Include prior/new values or relationship change, actor (user or system), authoritative timestamp, cause, and originating command/event reference. Keep stable actor identifiers plus the display label captured at the action, so later LDAP renames or deletion do not rewrite history. Preserve originating rule/group snapshots and lifecycle cycles. Do not generate duplicate change records or refresh inactivity for retries/no-ops. These are incident activity records available to incident readers; standalone tenant/platform access audit follows [Tenant and access completion](./spec-tenant-access.md), while incident activity visibility and retention remain as selected here.

### 10. Inactivity period and scope (I4)

Use a fixed incident inactivity period of **30 elapsed days (30 × 24 hours)** across tenants in the initial design, with no per-tenant, per-severity, or per-incident override. Start the timer at successful creation or reopening. It applies only to active incidents, including empty incidents and those with firing, resolved, or suppressed linked alerts. There is no pause or keep-open exemption. Alert supplement 19 separately selects 30 days of source inactivity; valid unchanged repeats refresh the alert timer but never the incident timer.

### 11. What resets incident inactivity (I4)

Reset for an actual user change to incident title, description, assignee, status, notes, or membership; an actual automatic alert addition; and an accepted firing-to-resolved or resolved-to-firing transition of a currently linked alert. A move counts for both active incidents. Do not reset for unchanged deliveries, allowed alert-content/metric updates without a lifecycle transition, alert acknowledgement/assignment/notes, suppression changes, rule edits, reads/searches, retries/no-ops, or automatic assignee clearing.

Use the authoritative transaction timestamp of successful incident actions/new links and the accepted transition's system-arrival time for source-driven alert lifecycle changes (authoritative action time for manual alert transitions). Update last qualifying activity as part of the transaction handling each qualifying action or accepted transition, without waiting for a scheduled expiry check. Advance activity time monotonically with the maximum qualifying timestamp; delayed processing/replay cannot refresh it merely to worker catch-up time.

Resolved incidents have no active timer, and post-resolution edits do not reopen them or move their resolution time.

### 12. Expiry and races (I4, I2)

An active incident becomes eligible for automatic resolution at `last qualifying activity + 30 days`, including that exact cutoff. At execution, recheck current status and last activity atomically; skip a stale expiry attempt if a qualifying action has extended the deadline. Resolve at the successful transaction's timestamp, with system actor and cause `inactivity`, retaining the deadline that caused the action in history. Apply the same ownership release, originating-rule/group evidence reset, fresh-transition boundaries, and unchanged alert statuses as manual resolution.

A delayed job does not backdate resolution or reopen an already resolved incident. A late historical source transition cannot undo a committed expiry; explicit reopening must pass the normal conflicts. Resume overdue checks after downtime. Run the due-incident expiry check hourly. Query active incidents whose recorded last qualifying activity is at least 30 elapsed days old; do not reread their activity histories to discover activity. The hourly cadence controls only the delay after the 30-day deadline: under normal operation, resolution can occur roughly up to one hour later.

This is not an availability guarantee before N3 is designed. Qualifying activity is maintained when the change is handled, independently of the expiry check.

## Retention, search, and screens

### 13. Incident retention and deletion (I4–I5, R1–R4)

Retain a resolved incident and its incident-owned notes, revisions, lifecycle cycles, and activity for **90 elapsed days from its latest successful resolution**; resolution by inactivity follows the same policy. Reopening before purge cancels the old deadline; the next resolution starts a new 90-day period. Post-resolution content edits do not extend retention. Before purge, atomically recheck that the incident is still resolved and its latest-resolution deadline is due; a stale job must never delete a reopened incident.

There is no manual Delete incident action, including for admins; resolve the incident and use retention. Incident purge does not delete linked alerts. If one side of a relationship outlives the other, retain only minimal counterpart identity and link provenance with the surviving parent, mark the counterpart unavailable, and do not preserve/recreate its full expired content. Those references expire with the surviving parent. System completion 19–20 now selects cross-resource application purge, tombstones and replay protection; infrastructure backups remain under the supplied owner contract.

This resolves incident-specific durations and parent-owned history retention, not alert or standalone audit retention.

### 14. Incident list and search (I5)

Default to active incidents, sorted by last qualifying activity descending, then immutable incident identifier as a deterministic tie-breaker. Support Active, Resolved, and All views; filters for status, severity, assignee (including unassigned/me), creation source, originating rule, linked alert identifier, and created/activity/resolved time ranges. Offer sorting by creation time, last activity, fixed severity rank, and resolution time. Support exact incident-identifier lookup and search current title/description and current non-deleted note text using case-insensitive ANDed text terms; no incident CEL, regex, fuzzy matching, or advanced query language in the initial design. Use cursor pagination, default 50 and maximum 200 rows. The list is a live view rather than a frozen cross-page snapshot; refresh from the first page to see reordered updates, preserve explicit selection by identifier, and do not promise snapshot pagination across concurrent changes.

### 15. Detail and mutation UX (I3, I5)

Detail includes editable title/description, read-only severity and origin, independent status/assignee controls, link totals/table, current notes and revision access, lifecycle cycles, and chronological activity. Show last qualifying activity and inactivity deadline for active incidents; show resolution cause/time and retention deadline for resolved incidents. Conflicting reopening links to the blocking rule/group incident and conflicting alert owners, as already agreed. Keep user drafts on conflict and require review/retry rather than silently overwriting. Apply successful authoritative mutation responses immediately and refetch affected lists/counts; do not wait for Elasticsearch. The preset and alert technical specifications define feed filtering, captured query clocks and SSE delivery.

## Processing and persistence

### 16. Authority and search (I5, D3–D5)

Read incident details, lists, notes, activity, membership and counts from PostgreSQL. Use transactional incident-owned search text for current title/description/non-deleted notes, with case-insensitive token matching, plus exact identifier lookup. Select tenant-prefixed indexes for common status/activity, severity, assignee, origin and link lookups, and the bounded digest/full-token search index selected in system completion 8/15. Update search text in the same transaction as searchable incident content.

No separate Elasticsearch incident projection is required initially. Alert feeds/current-note search use Elasticsearch; alert details/history are authoritative in PostgreSQL under alert supplement 20/24. Incident counters are computed from unique retained membership references and authoritative current alert state; unavailable references have a separate count, not an assumed suppression state. The alert supplement supplies shared logical mappings; shared system sections 8/15 define incident physical records and indexes.

### 17. Atomic ownership, revision, and retries (I2–I5, D4)

Treat each incident's metadata, notes, cycle and membership mutations as versioned PostgreSQL operations. Lock/recheck all affected incidents and alerts in one transaction for create-with-links, link/unlink/move, resolution, and reopening. Enforce one active claim per `(tenant, alert)` and one active incident per correlation context with database constraints; the latter uses the immutable rule/grouping-revision context provided by correlation, whose logical identity is selected in the correlation supplement as tenant, rule, grouping generation and full typed group key; system completion 15–17 selects physical layout.

Commit state, audit, reentry/reset boundaries, and required outbox records together. All writers, including correlation/expiry workers, must enforce these boundaries; delayed Kafka/Redis delivery cannot temporarily permit invalid claims. Advance the incident revision on every effective aggregate change, including last-activity changes; no-ops do not advance it. Linked-alert field changes keep their own alert revisions. Read incident detail and counters from one consistent database snapshot.

The correlation supplement selects the common tenant coordinator, lock order and fixed cross-rule arbitration; independent worker-local ordering is insufficient. The alert supplement supplies alert event contracts; system completion 15–18 selects physical integration.

### 18. Command and conflict contract (I2–I5, U5)

Require an expected incident revision on mutations to an existing incident (both incident revisions for Move) and a command idempotency key for creation/mutations. Scope each key by tenant, actor or system producer, and operation; reauthorize retries before returning a saved result. Keep successful command identity/result with incident activity through its retention lifetime; a matching retry returns the prior outcome without a new activity timestamp, and reusing a key with different content conflicts.

A stale revision, invalid lifecycle/link target, or ownership conflict returns HTTP 409 with a machine-readable reason and authorized current version/conflict references; the operation is atomic and changes nothing. Invalid fields/selection limits return 422. Inaccessible or cross-tenant resources return 404; a visible resource with insufficient write permission returns 403. A successful creation returns 201 and its authoritative representation; other successful commands return 200, including no-ops.

Do not expose an incident deletion endpoint. System completion 5–10/20 now selects exact routes, shared envelopes and post-purge command fences; identity/session protection remains in its normative supplement.

### 19. Authorization changes and event delivery (I5, A2–A4, U4)

Check current product grants and the identity integration's trusted membership view for every incident mutation and assignment choice. Fail the write closed when a trustworthy authorization decision cannot be obtained. A permission-loss cleanup job rechecks current assignee and effective permission inside the transaction so it cannot clear a replacement assignee or a user who regained another sufficient grant. Commit cleanup/audit/outbox together. Refresh the incident after committed version changes; use the shared SSE invalidation/reconciliation channel selected in technical supplement 18–21, with mutation-response/refetch behavior already defined above.

The identity configuration defines five-minute normal-operation LDAP enforcement and last-known identity fallback during refresh outages. A cached membership view accepted under that policy can support a trustworthy authorization decision; absent required evidence still fails closed. Use the identity configuration and shared live-update protocol for enforcement.

Correlation context and coordination are now defined in [Correlation rules](./spec-correlation-rules.md); the incident product policies above remain unchanged.

### Verification scenarios

See [incident acceptance cases](./verification-plan.md#incidents).
