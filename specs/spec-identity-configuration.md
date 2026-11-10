# Identity and sign-in configuration

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

OIDC sign-in, LDAP membership, sessions and access-change enforcement. [Tenants and access](spec-tenant-access.md) defines product grants and audit.

**User decisions:** the existing Keycloak installation belongs to the user's team, which can configure it. It runs inside company infrastructure and provides company-credential SSO. LDAP remains authoritative for users and teams. Nested membership applies to both tenant grants and the designated global-super-admin team. LDAP changes and account disablement target enforcement within five minutes under normal operation, including open sessions. During identity-refresh outages, use last-known identity data for normal authorization without an identity-data age cutoff.

**Later user decision — 2026-09-23:** deploy an isolated local Keycloak with custom users and groups instead of an external LDAP dependency for local development. Section 14 defines this development exception; the preceding company-deployment contracts remain in force.

**Later user decision — 2026-09-24:** Keep sign-in uses only username and password, with no one-time-code challenge or enrollment. This supersedes the earlier assistant-selected TOTP requirement for application users, including Keep global administrators. Separate Keycloak console administration retains its existing MFA policy.

## 1. Ownership and realm boundary

The user's team owns Keycloak configuration and operation for this integration. Other underlying technologies retain the ownership described in the reliability supplement; this correction does not transfer ownership of LDAP, PostgreSQL or other shared services.

Use a dedicated production realm named `keep`, with separate `keep-dev` and `keep-staging` realms and credentials. Keep tenants share the production realm; creating a tenant does not create a Keycloak realm, client or role. Use the existing installation rather than introducing another identity product. Actual hostnames and the installed release are deployment facts to inventory, not values to invent.

The user approved a Keep-branded username/password form on 2026-09-27. Implement it as the `keep` Keycloak login theme for the `keep-web` client, with the approved centered card, light/dark appearance, password visibility control, provider errors and directory-support help. This supersedes the earlier restriction to minimal standard-page branding. Submit credentials directly to Keycloak's generated form action and retain its authentication/session checks; do not add a Keep password API or authentication extension. Keep unrelated clients and console administration on their existing themes. Turn off self-registration, social sign-in, direct password grants, implicit flow, device/CIBA grants for this client, service-account grants and offline access. Users do not create a second Keep password.

## 2. Login flow and browser boundary

Register one confidential OIDC client, `keep-web`, per environment. The Python Product API owns the authorization-code exchange, with PKCE S256 and client-secret authentication. Next.js and the Product API are exposed under the same application origin. The browser receives an opaque Keep session cookie; OAuth access, ID and refresh tokens remain server-side.

Use these application routes:

| Route | Purpose |
|---|---|
| `GET /auth/login` | Start a login transaction and redirect to Keycloak. |
| `GET /auth/callback` | Validate and consume the one-use login transaction; establish the local session. |
| `POST /auth/logout` | Invalidate the local session and start provider logout. |
| `POST /auth/backchannel-logout` | Receive a signed OIDC logout notification. |
| `GET /auth/session` | Return current signed-in user and effective tenant access. |
| `POST /auth/activity` | Record foreground application activity, including a visible dashboard heartbeat. |

Configure exact HTTPS callback and post-logout redirect URLs for each environment, without wildcard origins. After login, accept only a validated local relative return path. Keep one-use state, nonce and PKCE verifier server-side; login transactions expire after ten minutes and are bound to the initiating browser. Callback replay or failed validation cannot create a session.

Assistant-selected entry behavior opens `/auth/login` after an initial session check returns 401 `unauthenticated`, preserving the current local path and query as `return_to`. Existing authenticated workspaces retain their mounted session across navigation. Session loss after admission, explicit sign-out, access denial and service failures retain their explicit recovery controls. `/signed-out` and `/sign-in-expired` never automatically restart login.

For a browser callback whose transaction is expired, consumed or missing, redirect
to `/sign-in-expired` with 303 and no-store caching. This public page explains the
stale attempt and offers an explicit `/auth/login` link to start a new transaction;
it neither exchanges the rejected code nor creates a session. Do not automatically
retry or forward old callback parameters. Non-HTML clients retain the structured
401 `authentication_rejected` response.

Request `openid profile` and a dedicated directory-identity scope. Include email only if a product display needs it; email is never an account key. Validate the ID token's signature, exact issuer, audience/authorized party, expiry, nonce and authentication time. Select RS256 and a maximum 30-second clock skew. Fetch signing keys from the configured issuer, refresh on an unknown key ID once, and reject unverifiable tokens. Do not discover an issuer from user-controlled input.

The code-flow/PKCE choice follows [OAuth security best practice](https://www.rfc-editor.org/rfc/rfc9700.html). These application paths, scope choices and timing values are Keep selections.

## 3. Username and password authentication

Require the company username and LDAP password at fresh authentication for all human Keep users. Local development uses the native credentials defined in section 14. Do not require a one-time code or authenticator enrollment for Keep admission, including users with previously enrolled factors. A valid Keycloak SSO session can satisfy a subsequent application login without prompting again. Password authentication is not repeated on every API request or tenant switch. The backend validates protected authentication evidence for the configured password flow; it must not require an OTP method claim.

Password changes and account unlock requests go through the existing company directory process. Keycloak must not write LDAP passwords or profile attributes. Do not use a Keep local password or automatic email-based account linking as a bypass. Lost-factor recovery for separate Keycloak console administrators remains the user's team's responsibility through the established identity-verification process.

Enable temporary Keycloak brute-force protection: five failed attempts trigger a 15-minute temporary login lock; no permanent automatic lock. This is an additional application setting, not a modification of LDAP's own password policy. Require MFA for separate Keycloak console administrators. Keycloak console administration and Keep global-super-admin membership are separate privileges.

## 4. Session and token settings

| Setting | Selected value |
|---|---|
| Keep idle timeout | 30 minutes since the last accepted application activity. |
| Keep absolute timeout | 24 hours from the original Keycloak authentication time. |
| Keycloak SSO Session Idle / Max | 30 minutes / 24 hours. |
| Keycloak client session timeouts | Inherit those realm bounds; do not extend them. |
| Keycloak access-token lifetime | Five minutes. |
| Refresh rotation | Enabled; refresh-token reuse allowance zero. |
| Refresh attempt interval while the local session is active | At most four minutes under healthy operation. |
| Remember-me / offline tokens | Disabled for Keep. |

The Product API enforces its own idle and absolute limits, regardless of provider grace windows or refresh traffic. A foreground dashboard sends an authenticated activity heartbeat every 60 seconds and therefore stays active. Stop it when the page is hidden. SSE data arriving at the browser, server refresh jobs and background tabs do not themselves reset Keep's idle clock. After 24 hours, even a continuously visible dashboard requires fresh authentication; no unattended kiosk identity is introduced.

Use `auth_time` and an appropriate OIDC `max_age` request to prevent an old SSO session from restarting the 24-hour clock indefinitely. An idle timeout may return through valid SSO; reaching the absolute limit requires fresh authentication. An expired local session cannot be extended merely because an identity snapshot still exists.

Serialize refresh per local session, persist the newly rotated refresh token atomically and fence stale workers. Multiple tabs must not race refresh tokens. Refreshed tokens must preserve the validated issuer, subject and immutable directory binding; a conflicting identity cannot replace the signed-in principal. A definitive provider revocation or `invalid_grant` ends the corresponding local session. A transport failure or ambiguous refresh response is not proof of revocation: apply section 9 while the local session remains valid, then reconcile or require fresh SSO. Never accept an expired access token as a Product API credential.

Keycloak documents separate session and token controls in its [administration guide](https://www.keycloak.org/docs/latest/server_admin/). The numbers above are selected Keep settings, not documented defaults.

## 5. Session persistence and CSRF

Generate a 256-bit random session identifier. Set a nonpersistent `__Host-keep_session` cookie with `Secure`, `HttpOnly`, `SameSite=Lax`, `Path=/` and no `Domain`. Regenerate the identifier after authentication. Store only its hash in PostgreSQL, together with the identity binding, issuer/subject/provider session ID, original authentication time, activity/absolute deadlines and revocation state. Encrypt retained provider tokens with an application encryption key supplied through the approved secret mechanism; never put tokens or session cookies in logs.

PostgreSQL is authoritative for local sessions, current grants and the identity checkpoint. Redis may distribute invalidations but is not required to preserve authorization correctness. If PostgreSQL cannot supply a trustworthy authorization decision, return a dependency failure; LDAP's last-known-data policy does not authorize bypassing current Keep grants or session revocation.

Protect state-changing browser requests with a session-bound CSRF token and strict same-origin checks. Use the OIDC transaction protections for the callback and signed-token validation for backchannel logout instead of browser CSRF tokens. No mutation uses GET. Do not allow cross-origin credentialed Product API access in the initial release. The cookie and server-enforced timeout approach follows [OWASP session guidance](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).

## 6. LDAP federation and stable identity

Configure Keycloak LDAP federation in `READ_ONLY` mode, with imported users and a maximum 60-second user-cache lifetime. Select changed-user synchronization every 60 seconds and a full reconciliation daily. These Keycloak jobs support authentication/profile consistency; they are not the proof that Keep's nested membership and disablement target is met.

Use TLS with certificate validation for directory connections and a read-only service identity. Keycloak handles human password authentication. Keep's separate directory reader never receives or binds with a user's password.

Keep identifies directory objects by `(directory source, immutable object ID)`: for example, validated `objectGUID` for Active Directory or `entryUUID` for a compatible LDAP directory. The deployed directory schema determines the actual mapping. DN, username, group name and email are mutable labels, not grant keys.

Configure a protected, read-only OIDC claim containing that immutable directory identity. Only users from the configured LDAP federation may supply it; local Keycloak accounts and user-editable attributes must not manufacture it. Bind `(issuer, sub)` to an internal Keep principal and this directory identity after validating the mapping. A conflicting mapping blocks admission and raises an operational error; never merge accounts by matching email or username. Deleting and recreating an account with the same name creates a different principal and inherits no old grants.

Keycloak groups/roles and browser token claims are not authoritative Keep tenant permissions. Keep keeps its own grants, and the designated LDAP team supplies global-super-admin eligibility. Use a standard Python OIDC library and a small directory-schema adapter; do not build a pluggable identity-provider framework for the first release.

## 7. Membership supply and the five-minute target

**REV-35 current boundary:** use explicit trusted publications for bootstrap and
manual identity refresh. The automatic polling algorithm and timing budgets below
are deferred design references, not current deployment or release gates.

Use a Keep background directory reader with a read-only LDAP connection to obtain account eligibility, group edges and complete transitive membership. This avoids making live authorization depend on login-time JWT groups or on Keycloak changed-user synchronization detecting every group-edge change.

Track the designated global-super-admin group, teams referenced by tenant grants, their transitive children, active-session users, directly granted users and current assignees. Support bounded directory search for administrative user/team selection. Before accepting a previously unknown principal or team grant, obtain the required complete eligibility evidence. Do not enumerate the entire company directory for every request.

Traverse by immutable IDs with cycle detection and deduplication; include the deployed directory's actual membership semantics, including primary-group membership where applicable. Do not assume `memberOf` alone contains transitive membership. A complete successful traversal may establish absence; a timeout, missing page, inaccessible subtree or incomplete traversal may not. Preserve alternative membership paths and combine all applicable grants with the selected highest-role-wins rule.

Select these normal-operation budgets:

| Stage | Application target |
|---|---|
| Start verification of each tracked identity/group dependency | At least every 60 seconds. |
| Finish and publish the corresponding complete verification | Within 60 seconds of its start. |
| Product API use of a published revision | Next authorization check; mutations also guard the revision at commit. |
| Existing SSE subscription recheck | Before sending protected content and at least every 30 seconds. |

This reserves up to 150 seconds for application polling, verification and idle-stream rechecks, leaving at most 150 seconds of the user's five-minute budget for directory visibility/replication and other upstream delay. The LDAP endpoint contract must fit that remaining budget. These are selected budgets requiring measurement, not assertions about the company directory or installed Keycloak. A slow successful cycle is a target miss and must be reported, not relabeled healthy.

Publish a complete verification generation atomically in PostgreSQL, including source, verification start/end, covered objects, completeness and revision. Tenant/access supplement 11/19 distinguishes ordered verification generation/time from semantic directory content revision: an unchanged re-verification updates freshness without invalidating content-based cursors or advancing a tenant revision. Fence out-of-order results. A refresh that reused older cached data does not advance its verification time. Independently verified negative evidence, such as account disablement, takes effect immediately even if another part of a refresh fails; a later partial result cannot resurrect it.

## 8. Applying access changes

**Current scope (REV-34):** Automatic assignment cleanup is deferred; known-ineligible assignees are masked, not cleared; see [worker scope](spec-worker-scope.md#2-assignment-and-data-lifetime-automation). Authorization, session and administrator rules below remain normative.

Every Product API authorization combines the valid local session, accepted directory evidence and current Keep grants. Do not maintain an independently stale effective-role cache. Permission edits committed in Keep affect subsequent authorization checks immediately. Guard mutation authorization against concurrent changes to grants and identity revisions; re-evaluate if the decision changes before commit. Do not undo already committed work retroactively.

SSE subscriptions use the same authority. Stop delivery for lost tenants, including counts and invalidation messages that reveal their data. If view remains after loss of edit/admin, preserve permitted reads and remove write actions. Positively confirmed account disablement terminates all that principal's local sessions. Losing the global-super-admin group removes only that privilege and leaves other valid access, including Global edit for an otherwise eligible user.

Filter tenant listings, search, selectors, resource lookups and subscriptions through effective access. An inaccessible or cross-tenant resource returns the selected non-disclosing 404 behavior; a visible resource with a forbidden action returns 403. Authentication expiry returns 401. A dependency failure without the evidence needed to decide access returns 503 rather than inventing either permission or directory removal.

Recompute initial/last administrator checks from the same accepted membership revision, counting eligible people once. Known loss of every local administrator leaves the tenant operating and raises a repair condition visible to global super-admins. A directory timeout alone does not create that condition. On positively confirmed assignee ineligibility, immediately expose the alert/incident as unassigned and run the existing idempotent cleanup/history contracts; do not wait for a later login, and do not clear assignments solely because verification is unavailable.

## 9. Outage behavior

**Current scope (REV-35):** Automatic directory retry and polling, and assignment reconciliation, are deferred; identity updates come from explicit publication; see [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have). The last-trusted-data outage policy below remains normative.

Keep the user's selected policy: existing valid sessions retain normal read, write and administrative permissions from the last successfully verified identity data combined with current Keep grants. No five-minute staleness cutoff, read-only downgrade or automatic privilege loss applies solely because LDAP or Keycloak is unavailable. Current known disablement, revocations and ordinary session deadlines remain effective.

Treat dependencies separately. A Keycloak outage does not stop a healthy direct LDAP reader from applying membership changes. An LDAP outage does not stop Keep permission edits or a valid signed Keycloak logout notification. Cached memberships cannot restore a session already invalidated by either source.

New sign-ins still need a valid OIDC exchange. If Keycloak can complete it during an LDAP-reader outage, an already linked principal may use its trusted stored directory evidence. A first-time user without the required verified directory binding cannot be admitted on a guessed username or group list. An unavailable Keycloak exchange cannot be replaced with cached credentials.

Retry failed directory verification every 60 seconds with small jitter; preserve the last complete evidence and its original timestamp. Show a degraded identity-service indicator and last successful verification time. Publish verified recovery changes immediately, recompute effective access and reconcile assignments/admin vacancies before declaring the affected coverage healthy. Do not log a failed or partial refresh as a successful synchronization.

## 10. Logout and revocation

On user logout, revoke the local session in PostgreSQL before clearing its cookie. Then use OIDC RP-initiated logout for the Keep realm, with a registered return URL to a signed-out page that does not automatically restart login. Local logout succeeds even if Keycloak cannot be reached; the UI states when provider logout could not be completed. A later explicit login may reuse provider SSO if provider logout failed. Revoke retained refresh credentials on a best-effort basis and remove local token material.

Configure a backchannel logout URL with provider session IDs required and front-channel logout disabled for this client. Validate the signed logout token's issuer, audience, time, logout event, subject/session binding and replay identifier; reject a nonce-bearing or wrong-purpose token. Apply it idempotently to matching local sessions, close their subscriptions and retain a revocation fence to prevent a racing callback from recreating the same session. This follows the [OIDC backchannel logout specification](https://openid.net/specs/openid-connect-backchannel-1_0.html).

Keep revocation fences for at least 24 hours and five minutes after the event, covering the maximum session lifetime and validation allowance. Refresh provides a secondary way to detect provider session termination under healthy operation. During a provider outage, unknown revocation follows the user's cached-identity/valid-local-session policy; known revocation never does.

## 11. Cache lifetime, restart and recovery

**Current scope (REV-34, REV-35):** Continuous synchronization and automatic cache eviction are deferred; see [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have). Checkpoint persistence, tombstones and the restore-integrity gate below remain normative.

Persist the last verified identity checkpoint in PostgreSQL so ordinary process/pod restarts do not lose the accepted outage view. A restart preserves original verification times and negative evidence; loading the checkpoint does not make it fresh.

Keep the current evidence while referenced by a grant, tracked group dependency, live session, assignment or retained product history. During an identity outage, pause identity-cache eviction. Under healthy synchronization, remove unreferenced cache-only records after 30 days without use; retain immutable principal references and display snapshots for as long as their owning product history requires. This selects cache cleanup, not a new audit-history retention policy. Purge unusable provider token material when a session expires or is revoked; retain only the minimal fences required by section 10.

Deleted directory identities become ineligible tombstones. Their grants are visibly orphaned and cannot transfer by name. A subsequently re-enabled account with the same immutable identity can use its still-current grants after fresh authentication; its old revoked sessions remain invalid. Existing alert/incident history and cleanup contracts remain authoritative.

After database rollback or disaster restore, invalidate all restored Keep sessions and require fresh SSO. Before re-enabling human authorization, reconcile restored grants/configuration with protected permission-change recovery evidence and obtain a fresh complete directory checkpoint. If post-backup permission changes cannot be established, keep human authorization gated for operator reconciliation. This prevents restoring known-revoked access from an old backup; it is a restore-integrity gate, not an age cutoff during an ordinary identity outage. Ingestion recovery retains its separate reliability/operator contracts. Backup execution and protection of required recovery evidence follow the relevant owning teams' contracts.

## 12. Global-super-admin setup and repair

Store the directory source and immutable ID of the designated global-super-admin team in controlled deployment configuration. Bootstrap validation must resolve that team and verify at least one eligible direct/nested member before initial human administration is enabled. No first-user promotion or Keep-local emergency super-admin account is introduced.

If a verified directory change leaves the group empty or deleted, keep tenants and ingestion operating and remove the now-ineligible global privilege. The user's team repairs the directory group through company directory administration, or changes the configured immutable group mapping through its controlled deployment process. An outage alone does not imply emptiness.

Validate a replacement group's complete eligible membership before switching mappings. Switch atomically, invalidate the old derived privilege and record operator, old/new immutable IDs, time and reason in protected operational change evidence. This deployment path is separate from tenant permission editing. Keycloak console recovery credentials do not themselves confer Keep super-admin access.

## 13. Operation and qualification

**Current scope (REV-35):** The five-minute propagation target and continuous synchronization metrics are deferred and are not release gates; see [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have). Configuration, upgrade and audit requirements below remain normative.

Keep sanitized realm/client settings and mapping definitions under version control; inject secrets separately. Record the deployed Keycloak version and test this configuration on that version before release. Avoid custom Keycloak provider code in the initial baseline. When strengthening authentication requirements or changing identity bindings, invalidate affected existing provider/local sessions so old authentication cannot bypass the new policy. Rehearse version upgrades in staging, including LDAP mapping, refresh rotation and logout; use the team's Keycloak maintenance process and the database owner's recovery contract.

Deliver authentication failures, factor resets, administrative configuration changes and synchronization health to the approved operational logging service without credentials. Measure verification age, coverage/completeness, cycle duration, end-to-end membership/disablement propagation, refresh failures and logout delivery. Operational telemetry retention remains with its owning service. The tenant/access audit policy permits current tenant admins and global super-admins only; Global's corresponding audit history is global-super-admin-only. Enforce current effective access through this supplement's session and identity policy. Tenant/access supplement 13–19 completes audit event coverage, the user's 365-day tenant audit period, assistant-selected platform audit readership/retention, and recovery integration. Operational telemetry ownership remains unchanged.

See [identity acceptance cases](../verification/verification-plan.md#identity).

## 14. Local Keycloak development exception

Use a dedicated local `keep-local` realm with native Keycloak users and groups when the application explicitly runs in `development`. This is the user's local deployment choice, not a replacement of company LDAP for staging/production. The application still performs real authorization-code OIDC authentication and its normal PostgreSQL session, grant, directory-publication and recovery checks. It introduces no test login endpoint, browser-supplied principal or automatic first-user promotion.

Assistant-selected local bindings use directory source `keycloak-local`, native immutable Keycloak user/group UUIDs and the validated OIDC `sub` claim as the user object ID. Mutable names, paths and email addresses do not confer identity or permissions. A recreated name has a different UUID and inherits no grants. Local administrators create users, credentials and group membership through the isolated Keycloak realm; nested groups supply transitive team membership. The configured global-super-admin group must contain an eligible person before initial human authorization opens.

A separate confidential `keep-directory` service account uses client credentials solely to read the local Admin REST API. Grant only the required realm-management read/query permissions; do not enable service accounts or password grants on `keep-web`. The dedicated reader requires a loopback HTTPS issuer, configured certificate trust, explicit allocation/page bounds, a secret environment binding and explicit `KEEP_ENVIRONMENT=development`. It enumerates this small local realm, including subgroup/member pagination, excludes service-account identities, and publishes through the same guarded directory verifier and PostgreSQL publisher. The company LDAP reader and schema configuration remain unchanged.

REV-35 removes continuous local polling. Startup performs one complete publication; subsequent identity changes require explicit manual refresh. The optional future poller starts each local verification cycle about every 60 seconds. Complete evidence can update users, teams, labels and memberships; incomplete traversal preserves the last complete publication while separately applying positively verified disablement. An identity missing from enumeration requires explicit absence from both the user and group endpoints before it becomes a tombstone. Provider timeouts, malformed responses, ambiguity and exhausted bounds cannot establish deletion or an empty successful roster. This implementation is not a measured claim about the five-minute production enforcement target.

Development startup may invoke the existing initial-bootstrap publication flag after verifying the configured group's membership. That flag may only open `directory_bootstrap_required`; it cannot open a restore-integrity gate. The regular signed-token, password authentication, CSRF, session timeout, reauthorization, assignment and audit contracts continue to apply. Store generated local credentials outside version control and preserve them across ordinary restarts. The [local setup instructions](https://github.com/keep-alert-operations/keep-delivery/blob/main/docs/local-keycloak.md) contain operational commands and verification status.
