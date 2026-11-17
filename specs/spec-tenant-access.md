# Tenants and access

**Later user decision — 2026-11-15 (REV-73):** directory search and save on pick read ADAPI, and people and groups are keyed by samAccountName; Keycloak and OIDC were removed by REV-73. Section 5 defines search and save on pick. See [REV-73](../decisions/design-register.md#rev-73--keep-password-sign-in-and-adapi-directory-replace-keycloak-2026-11-15).

**Later user decision — 2026-11-17 (REV-76):** Keep no longer handles disabled or deleted people; every person ADAPI returns is eligible, and a person missing from ADAPI is never stored as a tombstone. Deleted groups keep their handling. Sections 3–6 apply this. See [REV-76](../decisions/design-register.md#rev-76--keep-stops-tracking-disabled-or-deleted-people-2026-11-17).

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

Tenant lifecycle, grants, permissions, directory selectors and audit. [Identity configuration](spec-identity-configuration.md) defines authentication, trusted membership and sessions.

**User-selected audit policy:** tenant and permission changes are retained for 365 days and readable only by current tenant admins and global super-admins.

## 1. Tenant identity and names

Give each tenant an application-generated immutable UUID and immutable kind (`specific` or `global`). Names are labels, not route keys or identity. Retain current tenant records while the tenant exists; audit expiry does not remove tenants or release current names.

Trim surrounding Unicode whitespace, normalize the display name to NFC and require 1–128 Unicode code points. Reject remaining control/format characters and line/paragraph separators. Preserve capitalization and internal spaces. Compare names using a separately stored canonical key: NFD, default full case folding, then NFC. This completes the existing case-insensitive global uniqueness rule, including the reserved Global name. Apply the same procedure on creation and rename, and enforce uniqueness atomically.

Use one versioned normalization profile across API replicas; record its Unicode table version at implementation and keep it fixed across routine runtime upgrades. Changing the profile requires collision detection and an explicit migration before activation. The selected algorithm uses [Unicode normalization](https://www.unicode.org/reports/tr15/) and [default case-folding definitions](https://www.unicode.org/versions/latest/core-spec/chapter-3/); the length and character restrictions are Keep choices. These tenant-name rules do not modify operator names, LDAP labels or source alert fields.

Provision Global through idempotent initialization before admitting alerts. Reuse its immutable UUID on repeated/concurrent initialization; never reset its data. Enforce one global-kind row and the reserved, non-editable display name `Global`. Route v1 by that identity, not a supplied name. If the singleton/name cannot be established consistently, keep ingestion unready. Global has no local grants or managed v2 operators. No role may rename it, delete a tenant or disable a tenant.

## 2. Tenant creation

**Later user decision — 2026-11-11 (REV-71):** a global super-admin may create a tenant
with no grants, and creating a tenant never adds its creator. The new tenant starts
without a local administrator, and its Permissions page then requires adding one. See
[REV-71](../decisions/design-register.md#rev-71--a-new-tenant-starts-without-an-administrator-2026-11-11).

Creation accepts a name and 0–100 initial user/team grants. An empty list creates the tenant without a local administrator; a non-empty list must include at least one eligible local administrator after expansion. Any supported tenant role may appear among those grants. Resolve directory evidence before the commit; a user need not have signed into Keep previously to receive a grant.

Commit the tenant, name claim, initial grants, revision, audit and command receipt in one PostgreSQL transaction. A failure creates none of them. Return 201 only after commit. Creation does not create a directory group, operator, Grafana resource, default preset or dashboard. Operators retain their separately selected setup flow. Initialize the tenant revision to 1; the server determines the specific-tenant kind and identity.

An unsaved principal or incomplete new team expansion cannot satisfy the administrator requirement. Grants accept only principals already saved from the directory (section 5); creation with an unsaved principal returns 503 `directory_evidence_required` and leaves creation uncommitted. Creation itself never reads ADAPI or starts a background save. Existing complete evidence remains usable under the selected outage policy; do not add a freshness cutoff.

A tenant without an eligible local administrator keeps operating, as after a verified external vacancy (section 4), and global super-admins administer it through inherited access. Its permission roster reports that no eligible local administrator exists. Every permission batch must leave at least one, so the first saved batch adds one. The administration UI opens the new tenant's Permissions page as soon as creation commits and asks for confirmation before leaving that page while no administrator is saved; REV-71 defines that page's behavior.

## 3. Grant model and changes

Maintain at most one explicit grant per tenant and directory principal, with role `view`, `edit` or `admin`. Assigning another role replaces that grant's role. Direct-user and team-derived grants combine through the existing highest-role-wins rule; a direct lower role does not override a higher team grant. No custom roles, explicit denies, resource-level ACLs or creator privileges are introduced.

A person's grants stay in force whatever happens to the account in AD (REV-76): a person is always eligible, and only a group can become a deleted tombstone whose grants are orphaned.

Permission editing uses an atomic batch of 1–100 set/remove operations. Reject repeated principals within a batch rather than depending on operation order. Evaluate the complete resulting grant set and commit it together. Setting the existing role or removing an absent grant is a no-op; a batch containing only no-ops does not advance the revision or append change audit. There is no implicit full-list replacement that can erase grants absent from a stale page.

## 4. Administrator continuity

Serialize local permission changes per tenant and guard their identity revision. Count distinct eligible users reached through the tenant's own admin grants, including nested members. Inherited global-super-admin access alone still does not count. Recheck the resulting count at commit; reject a change leaving no eligible local admin with 409 `last_admin_required`. This includes a tenant created without grants (REV-71): its first permission batch must add an eligible local admin.

Admins may remove or demote their own grant when another eligible local admin remains. If that change removes their access, return only the successful command receipt and their resulting access state, then remove the tenant from their UI; do not return newly protected grant/audit data. Reauthorize subsequent requests and retries normally.

Existing empty teams may hold grants, including admin grants, but contribute zero eligible administrators. Reject new or elevated grants to a deleted team, or to a person an earlier version stored as ineligible or deleted until a sign-in, pick or refresh lifts that row; allow their existing grants to be reduced or removed. Since REV-76 no person becomes ineligible, so a person disabled in AD after all still counts as an eligible administrator until removed from the granting group (accepted risk). Unknown evidence produces a dependency failure, not a fabricated zero count. Verified external loss of the last local admin creates a repair condition and audit event without suspending the tenant, ingestion or otherwise-authorized users. Restoration clears that condition once, with audit.

## 5. Directory selection and visibility

Tenant admins can search company users/teams when managing their tenant's grants; global super-admins can also search the directory. These pickers expose the display label, principal type, whether the principal is saved, and the stored eligibility of saved principals, not grants in other tenants. Permission pages, grant lists and flattened team-member previews require tenant admin. Non-admins may see their own effective role, not the permission roster.

**Search.** Require 2–100 code points for company-directory search terms and treat them as literal data. A search asks ADAPI `/users` and `/groups` with `samAccountName=*term*` and `customFilter=(displayName=*term*)` (OR'ed), with no security-group filter. In `customFilter`, `(`, `)`, `*` and `\` are escaped as `\28`, `\29`, `\2a` and `\5c`. Rows show the display name only. Return 50 results by default with a maximum of 200. ADAPI caps a search silently at 1,000 rows, so a 1,000-row answer is reported in the response metadata and the picker asks the user to type more. Rows ADAPI returns that Keep has not saved have `id: null`; saved rows show their stored state, and a search never changes what is stored or queues anything. Flatten team previews with cycle-safe deduplication and the selected complete-membership semantics. Directory searches never modify AD.

**Search cache.** The raw ADAPI `/users` and `/groups` search answers, including the 1,000-row flag, are cached in Redis for two hours (`KEEP_ADAPI_SEARCH_CACHE_TTL_SECONDS`, 7,200; the user asked for "a couple of hours"). The key is a SHA-256 of the kind and the normalized term, so it holds no raw term. Stored principal state is merged from PostgreSQL on every request. The cache feeds only picker listings: save on pick, lookups, members, sign-in and the refresh always read ADAPI directly, so a stale entry cannot save a person or group that ADAPI no longer returns. If Redis is down or a value is corrupt, the search goes to ADAPI uncached; it never fails because of the cache. During an ADAPI outage, cached results may be shown, labelled as possibly out of date, and are never presented as the complete company directory.

**Save on pick (user decision, REV-73).** When an administrator picks a person or group that Keep has not saved, Keep reads it (and a group's recursive members) from ADAPI and saves it at once, so it can be granted. `POST /api/tenants/{tenant_id}/permission-principals/resolve` takes `{kind, username, retry}`: `kind` is `user` or `team`; `username` follows the sign-in username rules ([identity 2](spec-identity-configuration.md#2-login-flow-and-browser-boundary)) and also refuses `*`; `retry` is optional. Only tenant admins and global super-admins may call it. It is the only save route: tenant creation picks no principals (REV-71), and `POST /api/tenants` with unsaved principals keeps its refusal. The transaction takes the exclusive identity guard first, then authorizes, then publishes, so two concurrent saves cannot deadlock on a lock upgrade.

The POST checks, in order, before reading ADAPI:

1. A pending row exists for the principal. If it failed and the body has no `retry: true`, return 503 with its `last_failure`. If it failed and `retry: true` is sent, clear the failure and hand it to the background saver (below). If it is leased or queued, return 202 without calling ADAPI.
2. The principal is stored and usable (an eligible user, or a team with a root checkpoint, neither deleted): return 200 as stored, with no re-read. Its stored state decides whether it is selectable; later changes come from the refresh. A person an earlier version stored as ineligible is not usable, so picking them reads ADAPI again and saves them as eligible (REV-76).
3. Otherwise, save inline.

**Inline save.** Inside the ten-second request timeout, the verifier gets a 7-second deadline, and at least 1 second of the request budget must remain before publishing. The save is one single-root publication through the ordinary publisher ([identity 7](spec-identity-configuration.md#7-membership-supply-and-the-five-minute-target)). If it fits, return 200 with the stored principal. If it does not fit, publish nothing, create a pending row, hand it over and return **202** `{status: "pending"}`. If the publication fence rejects the save because a newer publication touched the same root, retry once while the request budget allows, then return 503 `directory_busy` ("Try again"). An ADAPI outage returns 503 `directory_unavailable`; an ADAPI call that outlasts its own timeout means the save didn't fit, so it returns 202. A deleted stored principal isn't usable: picking it reads ADAPI again. A name that neither ADAPI endpoint knows returns 422 `principal_not_in_directory`, and a name that more than one row matches 422 `principal_ambiguous`, with nothing saved; this holds for a person as for a group (REV-76). A person's exact lookup uses `/users/user` ([identity 6](spec-identity-configuration.md#6-ldap-bind-adapi-directory-and-stable-identity)).

**Polling.** `GET /api/tenants/{tenant_id}/permission-principals/resolve?kind=…&username=…` has the same authorization and reads only PostgreSQL, never ADAPI: a stored, usable principal returns 200; a leased or queued row returns 202; a failed row returns 503 with its `last_failure`; a pending row with no live lease (its process stopped) is handed over again and returns 202.

**Background save (user decision Q9, REV-73).** A pending save is one `directory_verification_requests` row per `(source, object_id)` with its `kind`, `lease_owner`, `lease_until`, `last_failure` and `updated_at`. The hand-over claims a 120-second lease with a conditional update that succeeds only when no live lease exists, and only the caller that wins the claim queues the job, so polls from other tabs or API processes queue nothing. Each Product API process runs one saver thread with a queue of 20; if the queue is full, the claim is released and the row waits for the next poll. [Worker scope 4 and 6](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have) define the saver's budget, results and shutdown. Failure reasons are `directory_unavailable`, `directory_group_too_large`, `directory_verification_deadline` and `directory_busy`. If the administrator leaves the page, the save still finishes. The refresh, daily or by hand, also saves pending rows that have no failure.

**Picker.** A pending row shows "Saving from the directory…" and is not selectable until saved. The picker polls the GET 3 seconds after each response, not on a fixed timer. A 503 shows "Couldn't add this group" with Try again, which sends the POST with `retry: true`. Grants still accept only saved principals.

Assignee selection retains its existing separate contract: editors may search users with effective edit or higher in that tenant, and assignment grants no access. All authenticated eligible company users still enter Keep without an invitation or an application-access group. No invitation, approval or access-request workflow is added initially.

## 6. Directory identity lifecycle

**Current scope (REV-34):** Automatic assignment eligibility cleanup is deferred; known-ineligible assignees are masked, not cleared; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Identity lifecycle and grant rules below remain normative.

A principal's identity is its lowercase samAccountName ([identity 6](spec-identity-configuration.md#6-ldap-bind-adapi-directory-and-stable-identity)). Changing a user's or team's display name updates its current label without changing grants, assignments or identity. Historical audit keeps the label captured at the action. Deleted groups leave inactive, visibly orphaned grant references; they are not silently reassigned or deleted. A person is never marked deleted (REV-76): a person missing from ADAPI keeps their stored row and direct grants, and leaves group memberships when a refresh no longer finds them among a group's members. A new directory object with the same samAccountName is the same Keep principal and inherits its grants (user decision, accepted risk, REV-73). Removing an orphaned grant is an explicit authorized operation subject to last-admin checks.

A person whom an earlier version stored as ineligible or deleted becomes eligible again at their next sign-in, a pick or a refresh that reads them, and their still-current grants apply again; revoked sessions stay revoked. Existing alert/incident eligibility cleanup remains in force and does not automatically recreate an old assignment when access returns. First observation establishes a current identity baseline, not a claim about historical LDAP membership.

## 7. Global permissions

**Later user decision — 2026-11-11 (REV-72):** Global's Administration shows only Integrations and Platform, to global super-admins. Global has no Permissions or Access audit page, so the read-only access-policy view below is no longer shown; the policy itself is unchanged. See [REV-72](../decisions/design-register.md#rev-72--global-administration-shows-integrations-and-platform-2026-11-11).

Global has a fixed access policy: every eligible authenticated company user has edit, and the designated AD group (`KEEP_SUPERADMIN_GROUP`) supplies administration. Expose no editable local grant list for Global, including redundant view/edit grants. The universal baseline cannot be removed through tenant permission commands. This completes the previously selected prohibition on local Global admin grants.

The designated global-super-admin group remains controlled deployment configuration, never a tenant permission field. Its bootstrap, replacement and empty/deleted-group recovery follow identity supplement 12. Tenant admin status does not grant Keep global privilege.

## 8. Permission matrix

Apply this matrix only where the resource lifecycle already permits the action. Global super-admins inherit tenant admin but cannot override prohibited operations.

| Capability | View | Edit | Tenant admin | Global super-admin |
|---|---|---|---|---|
| Read accessible tenant alerts, incidents, feeds, presets, dashboards, rules and ordinary metadata | Yes | Yes | Yes | Every tenant |
| Read resource history/diagnostics already exposed to resource readers | Yes | Yes | Yes | Every tenant |
| Temporarily change an open feed's query, sorting or columns without saving shared state | Yes | Yes | Yes | Yes |
| Persist shared presets/dashboards; execute permitted alert, incident, note, correlation and maintenance edits | No | Yes | Yes | Yes |
| Manage operators/API keys, copy keys, or read their protected management audit | No | No | Yes | Yes |
| Rename a specific tenant, manage its grants, inspect permission/team rosters, read tenant/access-change audit | No | No | Own administered tenants | Every specific tenant |
| Create specific tenants; read Keep's platform access audit | No | No | No | Yes |
| Administer Global or read its tenant/access-change audit | No | No | No local admin role | Yes |
| Delete/disable a tenant, rename Global, delete an incident manually, or disable an operator | No | No | No | No |

Viewer table adjustments are temporary in the current view and cannot write a preset or create a private/personal saved preset. [Presets](spec-preset-operations.md) defines explicit shared Save/Save as new, per-tab drafts, retained history and deletion blocked by current dashboard references. [Dashboards](spec-dashboard-operations.md) defines presentation and editing. Existing resource audit visibility and retention are not replaced by the new tenant audit policy.

## 9. Tenant navigation and access loss

List only accessible tenants, placing Global first and other tenants in canonical-name/ID order. Lists and details expose ID, kind, name, revision, creation/update times and the caller's effective role. Admin views additionally expose permission state and verified local-admin vacancy/identity-degradation diagnostics. Global super-admins get the all-tenant administration view.

Use immutable IDs in URLs and links. Warn before a voluntary tenant switch would discard an unsaved draft and offer Stay or Discard and switch. A confirmed switch clears tenant-specific rows, counts, selections, drafts and subscriptions before loading the new tenant; never apply a delayed response from the previous tenant to the new view. On loss of all tenant access, stop protected delivery, clear that tenant's displayed/cached data and move to Global with a generic access-changed message without delaying enforcement for a draft prompt. Lesser role reductions preserve permitted reads and remove disallowed actions. Preserve no inaccessible-tenant names or rows in navigation. Previously delivered data cannot be retroactively withdrawn.

Use the last tenant only while it remains accessible; otherwise enter Global. A direct inaccessible-tenant link shows the same unavailable page as an unknown tenant. Name conflicts return `name_unavailable` without revealing another tenant's identity, members or contents. No self-service tenant deletion, suspension, invitation or ownership-transfer screen is introduced.

## 10. Authorization consistency

The server selects every tenant scope from the authenticated route/resource and verifies every nested reference belongs to it. Client-provided roles, tenant names, selectors, search cursors and ingestion keys cannot confer Product API permissions. Apply access predicates before listing, counting, searching or returning data; do not fetch a global page and hide unauthorized rows afterward.

Use current local grants with the identity evidence accepted under the existing session/outage policy. Guard mutation authorization and last-admin checks through commit. Record whether a committed operation needed global-super-admin authority or was already allowed by ordinary tenant rights. UI visibility is a convenience, not the enforcement boundary. System processing and already-admitted external operations retain their domain contracts; they do not require the originating browser to stay signed in, and an expired human cookie is not workload authority. Keep the existing account-disablement, direct-grant propagation and SSE revocation behavior; these requirements do not select the general live-update transport.

## 11. Revisions, retries and errors

Use one monotonically increasing tenant revision for effective local metadata/grant changes. Require `expected_revision` for rename and permission batches and `command_id` for all these mutations and creation. Directory refresh has a separate semantic content revision and verification generation: unchanged re-verification updates freshness without advancing the semantic revision or tenant revision. Recheck current directory evidence at command commit without requiring the browser to predict the next synchronization generation.

Scope command IDs by actor, operation and tenant, or actor and creation operation before a tenant exists. Bind the request fingerprint to the target, intended change and expected revision. Identical retries return their recorded outcome after current authorization checks; conflicting reuse returns 409. Keep terminal command receipts for 90 elapsed days; unfinished records persist. Retain a minimal used-command digest/scope/fingerprint/outcome-reference fence indefinitely until a separately verified replay-safe migration permits its removal. After full receipt expiry, return 409 `command_result_expired`; never execute that command ID again. Fences contain no request body, secret or historical display labels and do not reserve released names.

Tenant commands are synchronous local transactions: 201 for creation, 200 for committed edits/no-ops, 409 for revision/name/continuity conflicts, 422 for invalid fields/principals/batch shape, 401 for invalid sessions, 403 for insufficient authority on visible resources and 404 for inaccessible/cross-tenant resources. Use 503 when required authoritative evidence is unavailable; use existing capacity-related 429 behavior. Save on pick is the one directory route that may answer 202 while its background save runs (section 5). Limit tenant command bodies to 64 KiB and reject excess with 413. Preserve the reliability supplement's handler deadlines; do not hold locks while waiting for LDAP or ADAPI.

## 12. Tenant and directory API surface

| Route | Selected contract |
|---|---|
| `GET /api/tenants` | Authorized list, optional name query, cursor and limit. |
| `POST /api/tenants` | Global super-admin; name, initial grants (possibly none, REV-71) and command ID. |
| `GET /api/tenants/{tenant_id}` | Tenant-readable metadata and caller role. |
| `PATCH /api/tenants/{tenant_id}` | Rename only; name, expected revision and command ID. |
| `GET /api/tenants/{tenant_id}/permissions` | Admin-only grants, eligibility diagnostics, whether an eligible local admin exists (REV-71) and revisions. |
| `PATCH /api/tenants/{tenant_id}/permissions` | Admin-only atomic set/remove batch; each item names an immutable principal ID and, for set, a role. |
| `GET /api/tenants/{tenant_id}/permission-principals` | Admin-only company-directory search through ADAPI and the search cache. |
| `POST /api/tenants/{tenant_id}/permission-principals/resolve` | Admin-only save on pick: `{kind, username, retry}`; 200 saved, 202 pending, 503 failed or unavailable (REV-73). |
| `GET /api/tenants/{tenant_id}/permission-principals/resolve` | Admin-only poll of a save by `kind` and `username`; reads PostgreSQL only (REV-73). |
| `GET /api/tenants/{tenant_id}/permission-principals/{principal_id}/members` | Admin-only flattened preview for a verified team. |
| `GET /api/admin/directory/principals` | Global-super-admin directory search. |
| `GET /api/tenants/{tenant_id}/audit` | Tenant/access-change audit, current admin authorization. |
| `GET /api/admin/access-audit` | Global-super-admin platform access audit. |
| `POST /auth/login` | Password sign-in ([identity 2](spec-identity-configuration.md#2-login-flow-and-browser-boundary)). |
| `GET /auth/session` | The signed-in user, effective tenant access and session deadline. |
| `POST /auth/logout` | Local sign-out. |

REV-73 removed `GET /auth/login`, `GET /auth/callback`, `POST /auth/activity` and `POST /auth/backchannel-logout`. Resource-specific APIs remain unchanged. Reject unknown mutation fields, attempts to set server-owned tenant IDs/kind/current revision or directory attributes, and unsupported role values. Principal IDs in grant operations are verified references; expected_revision is a concurrency precondition rather than a caller-assigned current revision. No tenant delete/disable or audit-edit endpoint exists. Permission PATCH on Global returns 422 `fixed_global_policy` for an authorized global super-admin; ordinary users cannot reach that administration operation.

List pages default to 50 and max out at 200. Bind opaque, tamper-checked cursors to query/scope/order and relevant content revision, expire them after 15 minutes and reauthorize every page. A changed tenant/grant/roster ordering revision requires restart with 409 `list_changed`; an expired cursor returns 409 `cursor_expired`. Freshness-only refresh does not invalidate a roster cursor. Do not maintain a long database transaction for a browser cursor.

## 13. Tenant audit coverage

Record successful tenant creation with initial grants, effective renames, every effective explicit grant addition/removal/role replacement, verified local-admin vacancy/restoration and directory-caused effective tenant-access changes. Record administrative repairs under the same action types with their cause. Directory-derived tenant events concern that tenant's explicit grant paths; global privilege changes belong to the platform trail and are not copied into every tenant merely because global privilege inherits access. A batched permission edit is one event containing its bounded list of before/after grant changes; creation includes the initial grant snapshot.

Do not duplicate change history for retries or no-ops. Validation failures, denied requests, ordinary reads and search traffic go to operational diagnostics rather than this product change history. Alert, incident, operator, correlation, preset and maintenance content changes remain in their own resource histories; do not copy their payloads into the tenant access trail.

## 14. Directory-caused audit events

Directory changes reach Keep through publications from the refresh (daily under REV-75, or by hand), sign-in and save on pick ([identity 7](spec-identity-configuration.md#7-membership-supply-and-the-five-minute-target)). Compare consecutive successfully verified semantic identity states and record effective tenant-role/eligibility changes for affected principals and local-admin vacancy transitions. Removing one path without changing effective access creates no synthetic access-loss event. Local grant edits still receive audit even when another grant keeps effective access unchanged.

Use the system directory-synchronizer actor, directory revision and observation time; include an authoritative source-change time only when actually available. Do not invent a human LDAP administrator or backdate an observed change. First synchronization records baseline establishment, not fabricated historical grant actions. Failed or partial refreshes do not generate removal, vacancy or assignment-loss events. Automatic identity refresh and the five-minute LDAP-change propagation target are deferred under REV-35; explicit publications retain these audit and completeness rules.

## 15. Platform access audit

Provide a separate Keep platform access trail readable only by current global super-admins. Record global-super-admin mapping activation/replacement, observed effective global-privilege gains/losses, identity-binding conflicts and their resolution, authorization recovery gates/resumption, and successful management actions that needed global privilege. Include tenant/resource references and operation metadata for privileged actions, without copying full resource content or credentials. Tenant-specific actions also retain their normal tenant/resource audit record.

Choose 365 elapsed days for this platform access trail as an assistant-selected alignment with the user's tenant audit period and existing operator audit. Operational authentication attempts, MFA resets, routine reads and provider/infrastructure diagnostics remain in their approved logging services under those owners' retention policies; this choice does not impose a new infrastructure log policy.

Configuration activation records identify the trusted deployment operation and actor when supplied by the controlled deployment process; otherwise identify the configuration-loader system actor. Provider-console changes are not falsely attributed to a Keep user. Repeated reports of the same unresolved binding/configuration fault do not append duplicate product events; record the first detected condition and its resolution, with repeated attempts in operational diagnostics. During an empty-super-admin-group incident, repair remains available through the established directory/deployment procedure and operational evidence, without granting another application user platform-audit access.

## 16. Audit records and atomicity

Each product audit record has an immutable event ID, scope/tenant ID, server recording time, optional verified source time, action and cause, stable actor ID/type with an action-time display snapshot, affected immutable principal/resource IDs, bounded before/after changes, command/operation reference, resulting revisions and authorization basis. Preserve identity verification time/degraded status for permission decisions made using cached evidence. Render historical labels as plain text.

Never record passwords, OTP material, session cookies, OAuth/API tokens, raw credentials, Authorization headers or full unrelated LDAP profiles/member rosters. Redact secret-bearing configuration values; retain safe secret-version references only where needed. Events are append-only through the application. Corrections append a linked correction event through the controlled repair/migration process, not an ordinary audit-editor UI; no user, including global super-admins, can edit or manually delete audit history.

Commit successful local state changes and their audit/command receipt in the same PostgreSQL transaction. External log delivery may retry from an outbox but is not a prerequisite for local success. Publish verified directory changes and their product audit together. Failure to persist already-known revocation is an authorization-integrity failure: block affected authorization until it can be durably reconciled; do not apply the unavailable-source fallback to positively known revocation. Required integrity gates must survive recovery, as in the identity supplement.

## 17. Audit retention and cleanup

**Current scope (REV-34):** The daily audit cleanup is not deployed and storage may grow; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). The 365-day read-time window and dependency rules below remain normative.

Apply the user's **365 elapsed days** from each audit event's server recording time. Later views, tenant renames, role changes, directory-label changes and retries do not restart the clock. Late-discovered LDAP changes use their actual recording time and separately retain any verified source time. Current tenants, current grants, global-group configuration and active identity state persist independently of audit expiry.

After the deadline, purge expired audit content only when no unfinished command, explicit retained reference or required recovery proof still depends on it. Retain the minimum required referenced evidence until that dependency is safely released, matching the existing protected-purge approach. Alert/incident references keep their own actor/name snapshots and do not automatically retain every tenant audit event. Minimal replay/revocation fences have their separate safety lifetimes and do not preserve full audit payloads indefinitely.

Run dependency-checked audit cleanup daily, with an application target of removing unprotected expired rows within 24 hours after eligibility under healthy operation. Recheck the deadline and dependencies at deletion. Delayed cleanup does not make expired, unprotected rows available through the audit API. Backups and infrastructure copies follow their owning teams' contracts; restoration must reapply retention and the existing authorization reconciliation gates before human access resumes.

## 18. Audit browsing

Tenant admins browse their tenant audit; global super-admins may also use the platform trail and filter it by tenant. Provide time range, action, actor and affected principal/resource filters; show newest recorded events first with event ID as a deterministic tie-breaker. Display times in the browser timezone with the timezone visible, and expose stored UTC instants through the API.

Default to the last 30 days, with explicit access to the full retained period and any dependency-protected entries. Use the 50/default, 200/max page limits and 15-minute cursor lifetime. Audit cursors fix an upper recording watermark so new events do not reshuffle subsequent pages; every page reapplies current authorization and retention. Detail shows before/after values, actor, cause, original labels and verification context. Mark a referenced expired resource unavailable without reconstructing its deleted content.

No editable audit notes, bulk export/download workflow or audit-read access delegation is included initially. Authorized clients may paginate the same protected API. This does not change normal resource-history reading or operator audit routes.

## 19. Persistence and recovery integration

PostgreSQL owns tenant/name claims, grants, local revisions, principal bindings, accepted directory state, command receipts/fences and tenant/platform access audit. Enforce unique tenant name keys, one Global singleton, one grant per tenant/principal and one command identity per scope. Index tenant/principal lookups and audit scope/recording-time/event-ID reads. Audit browsing uses PostgreSQL; no Elasticsearch copy becomes an authorization authority or a new audit retention dependency.

Separate directory semantic content revision from ordered verification generation/time. Materialized effective-role or team-membership results must identify their source grant/directory revisions and cannot outlive authority changes independently. Session, LDAP and SSE enforcement continue to follow the identity supplement. System completion 11–12/17–18 selects physical SQL layout, partitioning and transport design constrained by these contracts; migration execution and implementation remain delivery work.

After rollback/disaster restore, do not reopen human authorization from older grants or sessions. Apply protected post-backup permission/configuration recovery evidence, obtain the required current directory checkpoint and invalidate restored sessions before fresh sign-in. If correctness cannot be established, keep the existing recovery gate rather than promoting a user or trusting an older grant. Preserve other services' ownership and the separately selected ingestion/credential recovery rules.

## 20. Acceptance

See [required tenants and access checks](../verification/verification-plan.md#tenants-and-access).
