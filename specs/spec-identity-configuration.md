# Identity and sign-in configuration

**Later user decision — 2026-11-15 (REV-73):** Keep's own password sign-in (one LDAP bind against Active Directory) and the ADAPI directory replace the earlier identity provider; Keycloak, OIDC, Keep's LDAP directory reader, the idle timeout and provider logout were removed by REV-73. This document describes the current behavior. See [REV-73](../decisions/design-register.md#rev-73--keep-password-sign-in-and-adapi-directory-replace-keycloak-2026-11-15).

**Later user decision — 2026-11-17 (REV-75):** the refresh command runs once a day as an OpenShift CronJob; sections 7 and 9 and [worker scope 4](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have) describe it. See [REV-75](../decisions/design-register.md#rev-75--daily-scheduled-directory-refresh-2026-11-17).

**Later user decision — 2026-11-17 (REV-76):** Keep no longer handles disabled or deleted people: sign-in does not check whether an account is disabled, no publication ends sessions, and a person missing from ADAPI is not stored as a tombstone. Deleted groups keep their handling. Exact single-person lookups use ADAPI `/users/user`. See [REV-76](../decisions/design-register.md#rev-76--keep-stops-tracking-disabled-or-deleted-people-2026-11-17).

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

Password sign-in, directory membership, sessions and access-change enforcement. [Tenants and access](spec-tenant-access.md) defines product grants, directory search, save on pick and audit.

**User decisions:** Active Directory (AD) remains authoritative for users and teams. Keep checks a password with one LDAP bind and reads people and groups from ADAPI, the company AD REST API. Nested membership applies to both tenant grants and the designated global-super-admin group. During directory outages, use last-known identity data for normal authorization without an identity-data age cutoff. The five-minute enforcement target for directory changes is deferred with automatic refresh (REV-35).

**Later user decision — 2026-09-24:** Keep sign-in uses only username and password, with no one-time-code challenge or enrollment. This supersedes the earlier assistant-selected TOTP requirement for application users, including Keep global administrators.

**Accepted risks (user decisions, 2026-11-15, REV-73):** passwords cross the private network unencrypted while LDAP encryption is off; Keep has no lockout of its own; a reused username inherits the old holder's access.

**Accepted risk (user decision, 2026-11-17, REV-76):** the organization does not disable or delete people, so Keep does not track it. If someone is disabled after all, AD refuses their next bind, but an open session lasts to its 24-hour deadline, and they still count as a group member (for example as a tenant administrator or an assignee) until they are removed from the group. A deleted person drops out of a group's members at the next refresh, because the members route stops listing them; their direct grants stay. This replaces REV-73's risk that a disabled person keeps access until the next refresh.

## 1. Ownership and sign-in page

The user's team owns Keep's sign-in configuration: the LDAP host and bind settings, the ADAPI binding and the designated global-super-admin group. Active Directory, its domain controllers and ADAPI keep their owning teams. Other underlying technologies retain the ownership described in the reliability supplement. Actual hostnames, the domain and installed versions are deployment facts to inventory, not values to invent.

Keep serves its own sign-in page at `/sign-in`, a Next.js page outside `/auth` (which the Product API serves) and outside the workspace catalog route (which runs the session check). It keeps the Keep-branded design the user approved on 2026-09-27: a centered card, light/dark appearance, a password visibility control, error messages and directory-support help. Users sign in with their company username and AD password. There is no self-registration, social sign-in or separate Keep password, and Keep never changes AD passwords or profile attributes.

## 2. Login flow and browser boundary

Next.js and the Product API are exposed under the same application origin. The browser receives an opaque Keep session cookie and never holds a directory credential.

Use these application routes:

| Route | Purpose |
|---|---|
| `POST /auth/login` | JSON `{username, password, return_to}`. Check the password with one LDAP bind, look the person up in ADAPI and establish the local session. |
| `GET /auth/session` | Return the signed-in user, effective tenant access and the session's `absolute_at`. |
| `POST /auth/logout` | Revoke the local session. |

`GET /auth/login`, `GET /auth/callback`, `POST /auth/activity` and `POST /auth/backchannel-logout` were removed by REV-73. There is no login transaction, callback or provider redirect.

`POST /auth/login` checks, in order, before any bind:

1. The human-authorization gate. While the initial bootstrap or a restore-integrity gate is closed, sign-in returns 503 and publishes nothing.
2. The exact same Origin. The endpoint enforces its own 4 KiB body limit and rejects any `Content-Encoding` other than identity, because the general request middleware exempts `/auth/` POSTs from those checks.
3. The username: trimmed, 1–64 characters, with no control characters, no AD-forbidden characters (`" / \ [ ] : ; | = , + * ? < >`) and no `@`. Otherwise 401 `authentication_rejected`.
4. The password: an empty password is refused with 401 `authentication_rejected` before any bind, because an empty-password simple bind succeeds anonymously on AD.

After sign-in, accept only a validated local relative `return_to` path; anything else returns to the workspace root.

**Time budget.** Sign-in runs under the ordinary ten-second Product API handler timeout. An async timeout cannot stop a worker thread, so sign-in sizes its own steps: LDAP connect 2 seconds, LDAP receive 2 seconds, and the ADAPI lookup the smaller of 3 seconds and the remaining request budget minus 1 second. Before publishing, at least 1 second must remain; otherwise sign-in returns 503 `sign_in_unavailable` with nothing published.

Assistant-selected entry behavior opens `/sign-in?return_to=…` after a session check returns 401 `unauthenticated`, preserving the current local path and query. Existing authenticated workspaces retain their mounted session across navigation. Session loss after admission, explicit sign-out, access denial and service failures retain their explicit recovery controls. `/signed-out` and an old `/sign-in-expired` address offer the sign-in page and never sign in by themselves.

## 3. Username and password authentication

Require the company username and AD password at fresh authentication for all human Keep users. Local development uses the credentials defined in section 14. Do not require a one-time code or authenticator enrollment. Password authentication is not repeated on every API request or tenant switch.

**The bind.** The Product API performs one ldap3 simple bind in a worker thread. The server comes from `KEEP_LDAP_HOST`, `KEEP_LDAP_PORT` and `KEEP_LDAP_USE_TLS`, with a 2-second connect timeout. The read-only connection binds as `KEEP_LDAP_BIND_FORMAT` filled with the username (for example `{username}@corp.example`), sends the typed password as UTF-8 bytes and has a 2-second receive timeout. After a successful bind it asks the LDAP WhoAmI extended operation who is bound, then unbinds.

**The password** is used for that one bind only. It is never stored, logged, forwarded, put in an exception message or written to the database.

**Which account signed in.** AD resolves `name@domain` by an explicit userPrincipalName before `sAMAccountName@domain`, so a bind can succeed as a different account than the one Keep looks up. The WhoAmI answer must name the typed username, or sign-in is refused:

- `u:DOMAIN\name`: `name` equals the username, case-insensitively. The domain part is not checked; multi-domain forests are not handled (user decision).
- `dn:…`: it equals the bind DN, case-insensitively (the local OpenLDAP form).
- Anything else is refused.

**The directory lookup.** After the bind, Keep reads the person's own row from ADAPI `/users/user` by exact samAccountName (section 6). Sign-in never reads groups and never rechecks a session later. Since REV-76 it does not check whether the account is disabled: AD itself refuses a disabled account's bind.

| Outcome | Response |
|---|---|
| Wrong password (`invalidCredentials`) or a WhoAmI answer naming someone else | 401 `authentication_rejected`. One message for all cases; the reason is logged without the password. |
| A correct bind but no ADAPI row | 403 `account_not_in_directory` ("Your account isn't in the company directory."). |
| A correct bind but more than one ADAPI row | 403 `account_ambiguous` ("More than one directory account has this username. Contact your administrator."). |
| LDAP or ADAPI unreachable, or the time budget spent | 503 `sign_in_unavailable`; no session. |
| The stored person is still unusable after the sign-in's publication | 503 `sign_in_unavailable`, retryable; no session. |

**What sign-in saves.** When the ADAPI row differs from the stored principal (a new person, a changed display name, or a row an earlier version stored as ineligible or deleted), sign-in publishes a single-object evidence for that person through the ordinary publisher (section 7). The person is always written as eligible (REV-76), so a sign-in lifts such an old row. A sign-in never ends anyone's sessions. An unchanged row publishes nothing, so routine sign-ins do not advance the directory revision. After publishing, sign-in reads the stored row again and creates a session only when it is a verified, eligible, not deleted person. When it is not (a newer publication fenced the sign-in's evidence and left the row unusable, or an older version wrote it ineligible during a rolling deploy), sign-in returns a retryable 503 `sign_in_unavailable` rather than a session the next request would refuse. A person in no granted group signs in with Global edit through Global's fixed policy.

**On success**, revoke the session of any cookie the browser already sent, issue a new handle, create a session whose absolute deadline is 24 hours after sign-in and set the cookie (section 5).

Keep has no lockout of its own (user decision). Failed binds still count toward AD's own lockout policy. Password changes and account unlock requests go through the existing company directory process.

## 4. Session settings

| Setting | Selected value |
|---|---|
| Absolute timeout | 24 hours from sign-in. |
| Idle timeout | None. |
| Activity heartbeat | None. |
| Remember-me, refresh or offline credentials | None. |
| Directory recheck during a session | None; changes arrive through publication. |

The Product API enforces the absolute limit on every authorization, including SSE reauthorization. A visible dashboard stays signed in until the limit; after 24 hours it requires fresh sign-in. No unattended kiosk identity is introduced. An expired local session cannot be extended merely because identity data still exists.

## 5. Session persistence and CSRF

Generate a 256-bit random session identifier. Set a nonpersistent `__Host-keep_session` cookie with `Secure`, `HttpOnly`, `SameSite=Lax`, `Path=/` and no `Domain`. Issue a new identifier at every sign-in. Store only its hash in PostgreSQL, together with the principal, the deployment epoch, the sign-in time, the absolute deadline and the revocation state. Keep stores no directory or provider credential. Never put session cookies or passwords in logs.

PostgreSQL is authoritative for local sessions, current grants and the identity checkpoint. Redis may distribute invalidations and cache picker searches but is not required to preserve authorization correctness. If PostgreSQL cannot supply a trustworthy authorization decision, return a dependency failure; the last-known-data policy does not authorize bypassing current Keep grants or session revocation.

Protect state-changing browser requests with a session-bound CSRF token and strict same-origin checks. Sign-in has no session yet, so it relies on the exact same-Origin check, its JSON body and its own size and encoding limits. No mutation uses GET. Do not allow cross-origin credentialed Product API access in the initial release. The cookie and server-enforced timeout approach follows [OWASP session guidance](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).

## 6. LDAP bind, ADAPI directory and stable identity

**LDAP.** Keep uses LDAP only to check a password with the user's own bind. It has no LDAP service account and runs no LDAP searches. Encryption is the `KEEP_LDAP_USE_TLS` setting, off for now on the private network (user decision, overriding the earlier rule that directory connections use TLS). When it is on, the server certificate is validated, optionally against `KEEP_LDAP_CA_FILE`.

**ADAPI.** Keep reads people and groups from ADAPI at `KEEP_ADAPI_URL`, sending the `ClientId` header from the secret `KEEP_ADAPI_CLIENT_ID`. It uses four routes:

- `/users` and `/groups`. Their query parameters (`samAccountName`, `customFilter`, `attributesToLoad` and others) are OR'ed and exact unless `*` is used. They return JSON arrays of string-valued rows and cap silently at 1,000 rows. Keep uses `/users` for batches and picker searches, and `/groups` for searches and exact group lookups.
- `/users/user` (REV-76). It takes the same query parameters as `/users` and returns the same row shape, as a list holding one object. Keep uses it for every exact single-person lookup: `samAccountName=<name>` with repeated `attributesToLoad`. When no person has that name it answers 404 (user answer, 2026-11-17); Keep reads that 404 as "no row" and never reads its body.
- `/groups/members/user?samAccountName=…&isRecursive=true`. It returns a group's recursive members with `sAMAccountName`, `distinguishedName`, `objectGUID` and `userAccountControl`, handles cycles, includes people reached through distribution groups, has no cap and does not take `attributesToLoad`. Keep reads only `sAMAccountName` from it.

Apart from that 404 from `/users/user`, a non-200 response (including a 404 from any other route) or malformed JSON means the directory is unavailable; it never proves absence. A 404 caused by a wrong ADAPI path also reads as "no row"; because a missing person is never stored or negated, the only effect is sign-in answering 403 `account_not_in_directory` and save on pick 422 instead of 503 (accepted risk; the private-qualification route check catches it). Each call has its own timeout: 5 seconds in the refresh command; inside a request, the smaller of 3 seconds and the remaining request budget minus 1 second; in a background save, the smaller of 5 seconds and the job's remaining budget minus 1 second.

**Identity.** Keep identifies users and groups by `(directory source adapi, lowercase samAccountName)` (user decision: samAccountName does not change). Keep stores no GUID and runs no GUID reuse check, so a reused username is the same Keep principal and inherits the old holder's grants (accepted risk). Display names and distinguished names are labels. A user's label is `displayName`; a group's label is `displayName` when ADAPI returns it, otherwise `cn`. Product rows reference the internal principal ID, never the username.

**Lookup.** The reader is given a kind hint: a stored principal's kind, the requested kind on save on pick, or `user` at sign-in. It asks the hinted endpoint first (`/users/user?samAccountName=<exact>` or `/groups?samAccountName=<exact>`) and the other endpoint only if the first has no row. An object is missing only when both endpoints answer that they have no row for it. More than one row is ambiguous and fails closed. A returned `sAMAccountName` that does not equal the key, case-insensitively, is refused. Members whose samAccountName ends in `$` (computer accounts) are skipped.

**People are always eligible (REV-76).** Keep neither requests nor reads `userAccountControl`, so a missing or odd value never fails a read, and every person ADAPI returns is saved as eligible. A missing group becomes a deleted tombstone (section 11). A missing person is reported as not found and is never stored or negated: no tombstone is written and a stored row is left as it is. Save on pick of a missing person returns 422 like a missing group ([tenant access 5](spec-tenant-access.md#5-directory-selection-and-visibility)), and sign-in returns 403 `account_not_in_directory`.

AD groups are not Keep tenant permissions by themselves. Keep keeps its own grants, and the group named by `KEEP_SUPERADMIN_GROUP` (a samAccountName) supplies global-super-admin eligibility. The Product API and the refresh command read that one setting.

## 7. Membership supply and the five-minute target

**REV-35 current boundary:** use explicit trusted publications for bootstrap,
the identity refresh, sign-in and save on pick. REV-75 runs the refresh once a day
as a scheduled job; the automatic polling algorithm and timing budgets below remain
deferred design references, not current deployment or release gates.

ADAPI supplies complete recursive membership, so live authorization never depends on login-time group data. A group's members come from the recursive members route as flattened group → user edges; Keep tracks no subgroups. Member display names come in batches of `KEEP_ADAPI_LOOKUP_BATCH` names (50) per call: `/users?customFilter=(|(sAMAccountName=a)(sAMAccountName=b)…)&attributesToLoad=sAMAccountName,displayName`, with the names escaped. A member that the members route returned but a batch omitted is saved with its samAccountName as label. A batch never marks it deleted, and it does not make the evidence incomplete.

Publications come from four places, all through the same guarded verifier and PostgreSQL publisher:

- the refresh command, run once a day by the scheduled job (REV-75) or by hand, which re-reads tracked roots: the global-super-admin group, teams and users referenced by grants, users with active sessions, current assignees and pending saves without a failure ([worker scope 4](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have));
- sign-in, for the signing-in person's own changed row (section 3);
- save on pick, when an administrator picks an unsaved person or group ([tenant access 5](spec-tenant-access.md#5-directory-selection-and-visibility));
- the request-started background save of a group too large to save inside the request.

One evidence covers at most 10,000 objects. Do not enumerate the entire company directory. A complete successful read may establish absence; a timeout, non-200 response, ambiguity or exhausted bound may not. Combine all applicable grants with the selected highest-role-wins rule.

Publish a complete verification generation atomically in PostgreSQL, including source, verification start/end, covered objects, completeness and revision. Tenant/access supplement 11/19 distinguishes ordered verification generation/time from semantic directory content revision. Generations are allocated before reading, so generation order matches read order. An evidence is rejected only when a covered root or team already has a newer generation. A covered user that a newer generation already holds is skipped, and memberships are rebuilt from each user's current stored eligibility, so the newer fact wins. Independently verified negative evidence, such as a deleted group, takes effect immediately; a later partial result cannot resurrect it. Since REV-76 no evidence is negative for a person.

Every publication that changes something advances the directory revision and fences in-flight visibility proofs. This includes first and changed sign-ins, saves on pick and, in a refresh, each team's own publication. The publisher's statements are set-based, so a 10,000-object publication holds the identity guard for well under one second.

Deferred normal-operation budgets for a future automatic refresh:

| Stage | Application target |
|---|---|
| Start verification of each tracked identity/group dependency | At least every 60 seconds. |
| Finish and publish the corresponding complete verification | Within 60 seconds of its start. |
| Product API use of a published revision | Next authorization check; mutations also guard the revision at commit. |
| Existing SSE subscription recheck | Before sending protected content and at least every 30 seconds. |

These budgets would leave at most 150 seconds of a five-minute target for directory replication and other upstream delay. They are selected budgets requiring measurement, not assertions about the company directory.

## 8. Applying access changes

**Current scope (REV-34):** Automatic assignment cleanup is deferred; known-ineligible assignees are masked, not cleared; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Authorization, session and administrator rules below remain normative.

Every Product API authorization combines the valid local session, accepted directory evidence and current Keep grants. Do not maintain an independently stale effective-role cache. Permission edits committed in Keep affect subsequent authorization checks immediately. Guard mutation authorization against concurrent changes to grants and identity revisions; re-evaluate if the decision changes before commit. Do not undo already committed work retroactively.

SSE subscriptions use the same authority. Stop delivery for lost tenants, including counts and invalidation messages that reveal their data. If view remains after loss of edit/admin, preserve permitted reads and remove write actions. No directory publication or sign-in ends a session (REV-76); a session ends as section 10 lists. There is no in-session recheck, and a person disabled in AD after all keeps an open session to its deadline (accepted risk, REV-76). Group membership changes, including a deleted group, apply at the next authorization check after the refresh that publishes them. Losing the global-super-admin group removes only that privilege and leaves other valid access, including Global edit for an otherwise eligible user.

Filter tenant listings, search, selectors, resource lookups and subscriptions through effective access. An inaccessible or cross-tenant resource returns the selected non-disclosing 404 behavior; a visible resource with a forbidden action returns 403. Authentication expiry returns 401. A dependency failure without the evidence needed to decide access returns 503 rather than inventing either permission or directory removal.

Recompute initial/last administrator checks from the same accepted membership revision, counting eligible people once. Known loss of every local administrator leaves the tenant operating and raises a repair condition visible to global super-admins. A directory timeout alone does not create that condition. On positively confirmed assignee ineligibility, immediately expose the alert/incident as unassigned and run the existing idempotent cleanup/history contracts; do not clear assignments solely because verification is unavailable.

## 9. Outage behavior

**Current scope (REV-35, REV-75):** Automatic directory retry and polling, and assignment reconciliation, are deferred; identity updates come from explicit publication, including the daily scheduled refresh; see [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have). The last-trusted-data outage policy below remains normative.

Keep the user's selected policy: existing valid sessions retain normal read, write and administrative permissions from the last stored identity data combined with current Keep grants. No staleness cutoff, read-only downgrade or automatic privilege loss applies solely because AD, LDAP or ADAPI is unavailable. Known revocations and the session deadline remain effective.

New sign-ins need both a successful bind and an ADAPI lookup; if either is unavailable, sign-in returns 503 `sign_in_unavailable`. No cached credential or cached directory row replaces them. An ADAPI outage does not stop Keep permission edits on saved principals or local sign-out. Picker search may show results from the search cache; save on pick returns 503 `directory_unavailable`.

A failed or partial refresh preserves the last complete evidence and its original timestamp. The refresh command reports every failed root and exits non-zero, which fails the scheduled Job. Do not log a failed or partial refresh as a successful synchronization. The next daily run repeats it; an operator who cannot wait starts a run by hand after the outage. Roots a failed run missed can stay up to two days old.

## 10. Logout and revocation

On sign-out, revoke the local session in PostgreSQL before clearing its cookie. Sign-out is local only: the response carries no provider URL, and `/signed-out` does not sign in again by itself. Sign-out succeeds whether or not AD or ADAPI is reachable.

A session ends at its 24-hour deadline, at sign-out, when a later sign-in from the same browser replaces it, or when restore invalidates it (section 11). Since REV-76 no directory publication revokes sessions. Known revocation always applies, including during a directory outage.

## 11. Cache lifetime, restart and recovery

**Current scope (REV-34, REV-35):** Continuous synchronization and automatic cache eviction are deferred; see [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have). Checkpoint persistence, tombstones and the restore-integrity gate below remain normative.

Persist the last verified identity checkpoint in PostgreSQL so ordinary process/pod restarts do not lose the accepted outage view. A restart preserves original verification times and negative evidence; loading the checkpoint does not make it fresh.

Keep the current evidence while referenced by a grant, tracked group dependency, live session, assignment or retained product history. During an identity outage, pause identity-cache eviction. Under healthy synchronization, remove unreferenced cache-only records after 30 days without use; retain principal references and display snapshots for as long as their owning product history requires. This selects cache cleanup, not a new audit-history retention policy. The picker search cache in Redis expires after two hours and never feeds authorization.

Deleted groups, absent from both ADAPI endpoints, become ineligible tombstones. Their grants are visibly orphaned, and a group recreated with the same samAccountName is the same Keep principal again once it is saved. A person absent from both endpoints is not stored as a tombstone (REV-76): their stored row and direct grants stay as they are, and they drop out of group memberships when a refresh no longer finds them among a group's members. A new account with the same samAccountName is the same Keep principal and can use its still-current grants after fresh sign-in. A person an earlier version stored as ineligible or deleted is made eligible again by their next sign-in, a pick or a refresh that reads them. Existing alert/incident history and cleanup contracts remain authoritative.

After database rollback or disaster restore, invalidate all restored Keep sessions and require fresh sign-in. Before re-enabling human authorization, reconcile restored grants/configuration with protected permission-change recovery evidence and obtain a fresh complete directory checkpoint. If post-backup permission changes cannot be established, keep human authorization gated for operator reconciliation. This prevents restoring known-revoked access from an old backup; it is a restore-integrity gate, not an age cutoff during an ordinary identity outage. Ingestion recovery retains its separate reliability/operator contracts. Backup execution and protection of required recovery evidence follow the relevant owning teams' contracts.

## 12. Global-super-admin setup and repair

Store the samAccountName of the designated global-super-admin group in `KEEP_SUPERADMIN_GROUP`, controlled deployment configuration read by the Product API and the refresh command. Bootstrap validation must resolve that group and verify at least one eligible member before initial human administration is enabled. The refresh run with `KEEP_DIRECTORY_BOOTSTRAP_QUALIFIED` carries the bootstrap flag on the publication that covers the group. That flag may only open the initial bootstrap gate; it cannot open a restore-integrity gate. No first-user promotion or Keep-local emergency super-admin account is introduced.

If a verified directory change leaves the group empty or deleted, keep tenants and ingestion operating and remove the now-ineligible global privilege. The user's team repairs the group through company directory administration, or changes the configured group through its controlled deployment process. An outage alone does not imply emptiness.

Validate a replacement group's complete eligible membership before switching. Switch atomically, invalidate the old derived privilege and record operator, old/new group, time and reason in protected operational change evidence. This deployment path is separate from tenant permission editing.

## 13. Operation and qualification

**Current scope (REV-35):** The five-minute propagation target and continuous synchronization metrics are deferred and are not release gates; see [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have). Configuration, upgrade and audit requirements below remain normative.

Keep sanitized sign-in and directory settings under version control; inject `KEEP_ADAPI_CLIENT_ID` and other secrets separately. Record the AD domain, LDAP host and ADAPI version in the environment manifest. Before company use, one real call per ADAPI route confirms the response shapes the local mock copies, and one real sign-in confirms the bind name format and the WhoAmI answer. A mismatch fails closed with 401 or 503. When strengthening authentication requirements or changing the directory source, invalidate affected local sessions so old authentication cannot bypass the new policy.

Deliver sign-in failures (with their reason, never the password), administrative configuration changes and refresh results to the approved operational logging service without credentials. Since REV-75 the refresh writes `directory_root_failed` for each failed group root (its samAccountName) and each failed batch of person roots (their number, never their names), `directory_refresh_completed` with units, published units, failed roots and duration, and `directory_refresh_failed` with a reason and error class when it cannot start; both entry points log as service `api`, role `directory-refresh`. Its stdout lines and exit codes are unchanged. Keep supplies these records and the failed Job; the team that operates the cluster sets alert rules. Measure verification age, coverage/completeness, refresh duration and failed roots; the verification-age metric waits for the REV-74 state collector. Operational telemetry retention remains with its owning service. The tenant/access audit policy permits current tenant admins and global super-admins only; Global's corresponding audit history is global-super-admin-only. Enforce current effective access through this supplement's session and identity policy. Tenant/access supplement 13–19 completes audit event coverage, the user's 365-day tenant audit period, assistant-selected platform audit readership/retention, and recovery integration.

See [identity acceptance cases](../verification/verification-plan.md#identity).

## 14. Local directory development exception

Local development replaces AD and ADAPI with two local services when the application explicitly runs in `development`. This is the user's local deployment choice, not a replacement of the company directory for staging/production. The application still performs a real LDAP bind and its normal PostgreSQL session, grant, directory-publication and recovery checks. It introduces no test login endpoint, browser-supplied principal or automatic first-user promotion.

- **OpenLDAP** (a pinned image) checks passwords with plain LDAP on `127.0.0.1:58389`. Its users are seeded with generated passwords stored under `.local/identity/`. OpenLDAP does not accept `user@domain`, so the bind format is `uid={username},ou=people,dc=keep,dc=local`, and WhoAmI answers in the `dn:` form.
- **A mock ADAPI** (`keep-delivery/scripts/local_adapi.py` on `127.0.0.1:58092`), started by local Start, serves the same users and groups from `.local/identity/adapi-directory.json`. It copies the response shapes (including `userAccountControl`, which Keep ignores), the `ClientId` check, the parameter semantics, the 1,000-row search cap and non-200 errors, and serves the four routes of section 6, including `/users/user`. It includes a distribution-group chain and offers hooks that remove a user or group. Since REV-76 it has no disabled test user and no disable or enable hooks.

Local principals use the same `adapi` source and samAccountName keys as the company. Local Start publishes once with the bootstrap flag before starting API/UI. After identity changes, local administrators run the refresh action, which publishes once and starts no worker. Store generated local credentials, the wrapping key and the deployment epoch outside version control and preserve them across ordinary restarts. The [local runtime instructions](https://github.com/keep-alert-operations/keep-delivery/blob/main/docs/local-runtime.md) contain operational commands and verification status.
