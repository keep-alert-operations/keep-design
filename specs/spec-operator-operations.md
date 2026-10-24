# Operators, API keys and Grafana

**Later user decision — 2026-09-30 (REV-35):** automatic directory synchronization is nice-to-have and is not deployed. Explicit trusted publication supplies identity updates; the five-minute LDAP-change propagation target is deferred. See [worker scope](spec-worker-scope.md#4-directory-synchronization-is-nice-to-have).

**Later scope correction — 2026-09-30:** [Worker scope](spec-worker-scope.md) (REV-34) supersedes timer-driven maintenance release, automatic assignment cleanup, inactivity/retention worker deployment and asynchronous operator provisioning below. Earlier automation algorithms are retained as deferred design references; unaffected authorization, explicit commands, history access and recovery safeguards remain normative.

The 2026-09-30 [Kafka-first pipeline](spec-kafka-alert-pipeline.md) governs alert transport, gateway admission, UTC ordering, manual correlation, search reconciliation and cutover (REV-33). Unrelated product behavior remains unchanged.

Operator lifecycle, credentials, mandatory Grafana provisioning and safe remote reconciliation. V1 legacy operator strings remain outside this workflow.

## 1. IDs and names

Generate operator, credential-record and operation IDs as UUIDv4, serialized as lowercase canonical UUID strings. Never reuse an ID. Keep the existing tenant/version/operator-based alert identity contracts.

For display names, trim Unicode whitespace at both ends, normalize to NFC, require 1–128 Unicode code points, and reject Unicode control, format and surrogate characters. Interior ordinary spaces are allowed. Preserve display capitalization; compute the uniqueness key as NFC of the normalized name's Unicode case-folded value. Enforce a global database uniqueness constraint on claimed names, including setup-pending operators. Use the same pinned Unicode data version in all replicas; changing it requires a collision-checked data migration. These rules affect display names, not native alert fields. Reserve the requested new name while a rename is pending, retaining the old name claim. Only after the required Grafana updates succeed does atomic completion change the name and release its old claim; a capitalization-only rename retains its claim but still migrates the case-sensitive Grafana label. Historical names are not routing aliases.

## 2. Operator state and management page

Use lifecycle states `setup_pending`, `ready`, and `deleted`. Separate integration health (`in_sync`, `pending`, `needs_attention`) and operation progress from lifecycle. Losing all valid keys does not delete or disable the operator; show "No active key." Only Kong cleanup can remain pending after authoritative deletion; required Grafana changes must succeed before deletion completes. There is no general operator disabled state.

Tenant-readable rows show name, ID, setup/health state, current-key availability, retiring-key deadline, creation time and last reconciliation time. Admins additionally see management actions and sanitized operation errors. The list uses PostgreSQL, name-key/ID ordering, cursor pagination of 50 by default and at most 200, and case-insensitive name search. It contains all nondeleted tenant operators, including pending ones. Display instants in the browser timezone and show the timezone for key-expiry deadlines. Retained completed/deletion operations are available to admins separately. Never render key values or include them in list/detail data.

## 3. Management commands and logical records

All management and key-copy operations require current tenant-admin authorization, with inherited global-super-admin access. Reads follow tenant read permission; detailed key-operation audit is admin-only. Recheck authorization at execution, including idempotent replay. Return 404 for inaccessible tenant/operator resources and 403 for a visible resource with insufficient permission. Reject managed-operator creation in the global v1 tenant with 422; only specific v2 tenants own managed operators.

Mutations use a command ID scoped to tenant, actor and operation plus an expected operator revision, except creation. The request fingerprint includes target and intended change; identical retries return the original operation reference, conflicting reuse or stale revision returns 409. Retain command receipts for 90 elapsed days after completion; active operation records persist until terminal. Returning an old receipt does not repeat its mutation. Serialize competing operator changes; rename runs during its HTTP request and changes the desired Grafana matcher and affected rule labels under section 16. The old display name remains authoritative until verified completion. During initial setup, fold a requested rename into that setup generation while reserving both names; commit the new name only after full required setup succeeds. Revision changes track semantic management changes, not background retry counters.

The logical catalog includes operator ID/tenant/name/name claim/state/revision/timestamps; credential ID/operator/ciphertext and wrapping metadata/state/activation/expiry/revocation times/Kong credential ID; operation ID/type/target generation/actor/request fingerprint/step/attempt/due time/error/lease; owned remote resource IDs and desired/observed generation; and append-only audit. PostgreSQL owns these records. Secrets never enter Kafka, Elasticsearch, ordinary outbox bodies or audit; jobs carry secret-record references.

## 4. Key generation and recovery

Generate keys server-side from 32 cryptographically random bytes, encoded as unpadded base64url with the fixed `vena_` prefix. Keys have no embedded tenant/name and cannot be chosen or imported by tenant users. Uniqueness is checked using a SHA-256 verifier; never log the value or verifier. A key record ID is safe metadata and is not the API credential.

Current keys have no automatic age-based expiry in this initial release. Expiry applies to the selected retiring-key deadline. Admins rotate or revoke explicitly. Credential states are `prepared`, `current`, `retiring`, `revoked`, and `expired`. Prepared keys cannot admit alerts or be copied. Revoked/expired keys never become valid again. Operator identity remains independent of every credential generation.

## 5. Recoverable encrypted storage

**Current scope (REV-34):** Provisioning runs inside Product API requests, so the Product API, not a provisioning worker, holds decryption access; see [worker scope](spec-worker-scope.md#3-request-owned-operator-provisioning). Encryption, wrapping and fail-closed rules below remain normative.

Store each key encrypted in PostgreSQL using AES-256-GCM with a fresh random per-record data-encryption key and nonce. Bind operator ID, credential ID and format version as authenticated associated data. Wrap the data key under a versioned platform encryption key, also using authenticated encryption and unique nonces. Keep wrapping keys in restricted, mounted OpenShift Secrets, outside the database and application source. Restrict decryption to the credential-copy backend and provisioning workers; ingestion authorization does not decrypt keys.

Require encryption at rest for the cluster secret store and for Grafana/Kong credential stores and backups, as deployment prerequisites. Rotate wrapping keys every 90 days and on suspected compromise; rewrap data keys without changing customer API keys. Retain old wrapping-key versions for live ciphertext and required backup recovery, then retire them under the platform backup policy. This selects the operator secret-storage approach; platform-wide backup media and retention remain N2/N3/R4. Missing wrapping keys cause copy/provisioning to fail without exposing plaintext or changing already-valid credential state.

## 6. Copy behavior and secret disposal

Keep the user-selected repeatable, admin-only Copy action. Fetch only the current valid key through a dedicated POST after an explicit click, using HTTPS, authenticated session/CSRF protection, and `Cache-Control: no-store`. Responses and traces must redact the field. No secret is returned by creation, rotation, job polling or error responses. During a pending rotation Copy still returns the existing current key; after activation it returns the replacement. Success feedback requires successful clipboard write; failure offers retry without revealing the key. A credential may be revoked after retrieval, so server retrieval is not a promise of future validity.

Erase application-held ciphertext/data-key material for revoked or expired credentials in the invalidation transaction, keeping nonsecret identity/state metadata. With the sweep deferred, expiry disposal occurs on the next successful operator mutation; authorization still expires at the exact deadline without waiting for disposal. Queue deletion from Kong and removal/replacement in Grafana. Revocation remains pending until serving-node policy denial is verified; after that verification, delayed remote resource cleanup cannot extend authorization. Fixed expiry is enforced by Kong without waiting for cleanup. Never retain invalid plaintext for rollback. A still-valid old current key may be used for a cancelled rotation's repair. Clipboard contents and backup copies cannot be erased by this action; expiry/revocation remains authoritative after restoration under section 28.

## 7. Kong identity contract

One Kong Consumer and managed Key Auth credentials represent an operator. The required OSS Appchi policy plugin verifies credential state, fixed expiry, immutable operator/tenant and monotonic policy generation, and supplies trusted stripped context over private mTLS. Ingress performs no Appchi PostgreSQL authorization/routing lookup. The actual plugin, policy store and complete serving-pool proof contract are [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 7; legacy Key Auth identity-only proof is insufficient.

## 8. Exact admission, expiry and revocation

Kong policy is admission authority for v2. Prepared denies; current allows; retiring requires a fixed UTC expiry and denies at or after that instant. Revocation commits local invalidation/ciphertext erasure immediately but returns pending until every serving node proves denial under the exact policy generation/digest. Never describe Appchi PG commit as instant remote revocation. Policy failure fails closed, and stale lower-generation remote writes cannot restore access. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 7.

## 9. Synchronous provisioning and explicit retry

Run the existing verified remote steps within the Product API request under the
[request-owned provisioning contract](spec-worker-scope.md#3-request-owned-operator-provisioning).
Persist identities/progress and reconcile uncertain effects before repeating a
write. Remote calls stay outside SQL transactions; generation and routing leases
remain mandatory. No automatic retry sweep or periodic repair is deployed.

## 10. Initial setup sequence

Prepare the local candidate, install Key Auth plus a deny policy, and verify prepared-deny across the serving pool while completing the existing Grafana checks. Commit activation intent/current state and any retiring deadline once. Distribute the active policy and prove actual Key Auth plus policy admission across the entire serving pool before operation completion or Copy. Retrying an activation phase never moves the retiring deadline. Rename/cancel also distribute and verify their final policy. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 7.

## 11. Rotation and Grafana failure

When no retiring key remains valid, an admin may start one pending rotation. Prepare one replacement, provision it in Kong, and update the existing managed Grafana contact point to use it. Keep the old current key valid and copyable until the Grafana update is acknowledged/reconciled. A Grafana failure leaves Rotation pending and retries the same replacement; do not start the 24-hour clock early or add further candidates.

Once replacement configuration succeeds, atomically make the replacement current and the old current key retiring, recording activation time and old-key expiry exactly 24 elapsed hours later. Subsequent retries preserve both instants. Non-Grafana senders are updated by the tenant during that overlap; show the deadline in management UI. Never extend the overlap automatically. The two-valid-key limit and prior requirement to expire/revoke the retiring key before another rotation remain in force.

Remote Grafana switching and the PostgreSQL activation commit cannot be one transaction. A short interval of rejected replacement-key webhooks can occur before activation; the prepared credential returns 401 inactive until the active policy is verified. Policy-store or clock-health unavailability returns 503. Expose these failures. Keep this limitation explicit: the design does not promise lossless delivery from Grafana during every failure/cutover, and does not silently accept an unactivated key to hide the gap.

## 12. Cancel rotation, revoke and revoke all

Admins may cancel a pending rotation before replacement activation. Invalidate the prepared candidate/generation, retain the old valid current key, and reconcile Grafana back to it if needed. Cancelling after activation returns 409; use explicit revocation or a later permitted rotation. Never roll back alert/operator identity.

Provide Revoke key and Revoke all keys. Revocation is irreversible and commits locally before remote cleanup; it never waits for Grafana. Revoke all also cancels every pending credential-creation/rotation operation. Revoking the current key during a pending rotation cancels that operation so a stale worker cannot activate a replacement after the admin's stop action. Revoking a retiring key does not affect the current key. Revoking only the current key during an established overlap leaves the retiring key usable until its original expiry, but does not promote it to current or make it copyable. The UI explains this and offers Revoke all when stopping all senders is intended. Show an explicit in-product confirmation for revocation describing which senders lose access; this is future product behavior, not an approval request during design work.

## 13. Issuing a key after revocation

Create key on an existing operator is available only when no valid current/retiring key and no pending credential operation remain. It retains operator ID, tenant, alert identity and retry namespace, but generates a fresh secret. If only a retiring key remains valid, wait for expiry or explicitly revoke it first. Perform the same Kong/Grafana preparation and readiness gate as initial creation. This gives an operator with no active key a recovery path without restoring revoked secrets, creating a new operator, or introducing disable/re-enable.

## 14. Platform Grafana configuration and compatibility

Use one platform-managed connection to the shared company Grafana: HTTPS base URL, explicit organization/namespace, trusted CA configuration, service-account credential, adapter profile and managed-resource prefix. Tenant users cannot override destination, organization or credentials. Store the service-account credential in a restricted OpenShift Secret mounted only by the provisioning component; do not expose it through operator Copy. Use the narrowest receiver/routing and affected-alert-rule read/write permissions the selected Grafana profile supports. Rule writes are restricted by this application to the operator routing-label migration/removal below; server-wide administration is not required by this product design. Missing access or externally provisioned, uneditable rules keeps the action pending with an actionable error rather than pretending migration succeeded. Platform super-admins manage connection metadata and reference secret versions through deployment configuration.

Select a versioned adapter against the actual installed API and run a deployment capability check. Prefer supported App Platform receiver/routing APIs; support the legacy provisioning API only under the controlled-writer rule in section 16. Record the tested Grafana/Kong version pair in deployment configuration rather than inventing the company's installed version. Required capabilities are secret-bearing webhook authorization, preserved resolved notifications, receiver/policy read/write/delete, deterministic resource identity, and safe routing-tree updates. Unsupported capability keeps setup pending with a platform error; there is no skip-Grafana or plaintext-secret fallback. Re-test before upgrades. Grafana documents the legacy policy API's whole-tree overwrite behavior and its newer routing API replacement. [Grafana provisioning API](https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/api-legacy/alerting_provisioning/)

## 15. Grafana resource identity and ownership

Give each operator one managed webhook integration in one contact point, plus one exact-match notification-policy entry. Derive the receiver name from `vena-operator-` plus the operator UUID and the resource UID from `vena-` plus the UUID's 32 hexadecimal digits; keep both stable on rename. Record actual remote IDs, owning operator and desired configuration generation in PostgreSQL. Never find, adopt or delete a resource solely by the operator's display name. A preexisting resource without matching ownership is a visible conflict, not something to overwrite.

Our product owns destination, authentication, integration settings and the exact managed policy entry. Teams own their Grafana alert rules; setup does not create or delete rules. To fulfill the user-selected Grafana-success gate for rename/deletion, the product may migrate/remove only that operator's routing-label key on affected rules, preserving all other rule content. This is a narrow exception to the earlier no-rule-edit choice. Show the required routing label and an example field mapping in operator details. Prevent routine Grafana-UI editing of managed resources where supported; a platform-admin override is detected and reconciled, not adopted as the desired product configuration.

## 16. Shared policy tree and routing label

**User-selected routing label:** use label name `Appchi - {operator name}`, equality operator `=`, and the literal string value `true`. Substitute the stored display name, preserving capitalization and interior spaces; the prefix includes one space on each side of the hyphen. For operator Payments, the label is `Appchi - Payments` and the value is `true`. API-key authentication still determines the immutable operator ID and owning tenant; the routing label is excluded from the native v2 hash. During controlled platform bootstrap, preserve the existing company routing behavior inside a final catch-all child: copy its original root receiver/settings and entire ordered child tree into that branch. Keep the outer root defaults as well. Place the product's exact-match routes before this company branch, sorted by UUID, with continued sibling evaluation enabled. Every alert still reaches the company branch, preserving both its matching routes and its original default-receiver fallback; merely adding continued operator routes beside the old children would not preserve that fallback. Record the wrapper as platform-owned structure and verify equivalent company deliveries before enabling provisioning. Subsequent company changes use that preserved branch through the selected writer mechanism. Operator deletion removes only its entry, not the wrapper or company branch. A missing operator label matches no managed operator route. Labels select notifications, not authenticated tenancy. See [Grafana notification-policy routing](https://grafana.com/docs/grafana/latest/alerting/fundamentals/notifications/notification-policies/) for the parent/child and default-receiver behavior this layout preserves.

Read fresh state, merge only the managed entries and write through one platform routing coordinator. Use server-enforced resource-version preconditions when the selected API supports them and retry conflicts from a fresh read. With a legacy API lacking such protection, require the platform to establish one controlled writer for the whole shared tree: other teams' changes must pass through that coordinator and direct UI/API writers must be restricted. A local lock or read-then-write check alone is not sufficient protection from outside writers. Until one of these safe modes is available, keep provisioning pending and report the platform prerequisite. Never reset/delete the entire tree, replace it from a stale local snapshot, or claim to protect other writers without that enforcement.

### Rename and name reuse after verified Grafana updates

**User decision — 2026-09-21:** an operator may be renamed or deleted only if the required Grafana updates succeed. This resolves the name-reuse follow-up: keep its old name reserved until that operation completes successfully. It supersedes metadata-only rename and deletion completion before Grafana cleanup; it does not change the retained-alert/pending-input deletion guards.

**Assistant-selected implementation of that gate:** for rename, reserve the new name and persist an operation while the authoritative display name remains old. Prepare the new exact-name policy entry pointing to the same immutable contact-point identity; retain the old entry only during this transition. Update affected Grafana rules by moving the old routing-label key to the new key, preserving its configured value/expression and all other rule fields. If the new key already exists with a conflicting value, block for repair. Migrate capitalization-only changes too. Rules must use explicit operator-routing label keys; a source that generates those keys outside the managed rule inventory needs an approved migration path before the operation can complete.

Inventory and recheck affected rules. Require acknowledged writes and readback of the desired rules and policy; lack of permission, an unknown write outcome or incomplete inventory is not success. Use supported version preconditions, or controlled writer access for affected rules when the API lacks them; never overwrite a concurrent team's rule changes from an old snapshot. After rule migration, remove the old policy entry and verify the final configuration. Then atomically commit the new display name and release the old name claim. Resource IDs, credentials and authenticated tenant ownership stay unchanged.

The webhook adapter may accept either old or new routing label only for this same authenticated operator while its recorded rename generation is pending and both name claims remain held. On completion it requires the new label. No lasting old-name alias is created. Configuration changes can produce Grafana resolution/firing events; process them through the existing occurrence rules. Already queued old-label deliveries can be rejected after cutover; successful configuration writes are not a promise to rewrite remote delivery queues.

Failures stay pending with the old name and both claims retained; retry the same operation. Admins can cancel before final commit, but cancellation completes and releases the proposed name only after restoring the old rule labels/policy and verifying removal of the temporary new route. Undo only this operation's label changes with version checks, preserving unrelated edits. While restoration is incomplete, keep the operation and claims pending. For deletion, use section 21.

**Assistant-selected compatibility requirement:** deployment checks must round-trip the exact label, including spaces, hyphen and permitted Unicode, through rule labels, policy equality matchers and webhooks. Do not sanitize it or fall back to a different key. Use Grafana's built-in Alertmanager for this managed route; alternate external Alertmanagers need the same verified capabilities. See [Grafana label support](https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rules/annotation-label/).
## 17. Grafana webhook transport

Add `POST /api/ingest/v2/grafana` as a dedicated transport adapter in the Ingestion API. The two native v1/v2 endpoints keep their exact strict schemas. Configure Grafana's standard webhook payload, HTTPS POST, resolved notifications enabled, certificate verification, and its secret Authorization credential field using `Bearer <operator API key>`. Do not store the key as ordinary visible extra-header metadata or put it in a URL.

Only on this route, a gateway pre-auth adapter validates one Bearer credential, converts it internally to the Key Auth input, then strips both credential headers upstream. Reject duplicate/ambiguous Authorization or simultaneous client X-API-Key headers. Native v2 remains X-API-Key-only. All routes converge on the same operator/credential binding and Kong policy admission gate; a claimed body operator/tenant cannot route a request. No extra shared Grafana ingestion credential is introduced. Grafana supports its Authorization credential field and a standard payload containing per-alert status, labels, annotations and start time. [Grafana webhook documentation](https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/)

## 18. Grafana-to-v2 field mapping

Validate the supported standard webhook envelope and iterate its `alerts` in order. Produce one native-equivalent v2 payload per member using this fixed mapping; store adapter version and original source bytes with the existing received-event provenance, never headers/secrets.

| v2 field | Grafana source |
|---|---|
| application, component, severity, site | Same-named per-alert labels, required. |
| node_name | Same-named per-alert label, optional only when absent. |
| message, impact, runbook_url | Same-named per-alert annotations, required. |
| status | Per-alert status: firing or resolved. Ignore group status for lifecycle. |
| time_created | Required per-alert startsAt, parsed as RFC3339, converted to UTC and truncated to seconds for the native format. |
| operator, tenant, key_field, history_id, timestamp | System-derived exactly as native v2, never taken from Grafana metadata. |

Require each member to contain the authenticated operator's expected `Appchi - {operator name}` label with the exact string value `true`. Do not require the superseded UUID routing label. During a recorded pending rename, accept the old or new label only as specified in section 16; after completion require the new label. Do not infer an operator or tenant from any label. This catches misconfigured contact points but does not replace key authentication. Apply existing required-field, severity, URL, size, hash and occurrence rules after mapping. No aliases or fallback from summary/title, no severity inference, and no additional identity fields. Extra Grafana transport fields/labels/annotations are retained only in source provenance and never added to the managed field catalog or hash. Grafana silence/muting is not a suspended alert event and does not create our source-suppression cause.

Teams must use stable labels/annotations for identity-bearing fields and repeat the original values on resolution. In particular, impact and runbook_url already participate in the v2 hash; changing them creates a separate logical alert. Grafana fingerprint/groupKey are not our logical key or a unique delivery ID. The adapter does not merge v1/v2 or reopen previous occurrences differently from native v2.

## 19. Grafana delivery, limits and repeats

The Grafana adapter retains its payload/field-mapping limits and routes with literal Appchi - {operator name}=true. Each mapped valid alert uses Kafka-first publication and partial item results. Repeats/resubmissions have new delivery UUIDs and receive times; no sender-key deduplication is promised. Unchanged applied logical repeats do not create fresh correlation evidence. The adapter remains a separate transport, never expands native payload fields. See [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 2.

## 20. Explicit repair

Reconcile owned resources during each requested provisioning operation. Automatic
five-minute drift checks and repair are nice-to-have. Failed requests remain
visible and require explicit Retry. Unavailability does not revoke valid keys or
change existing alert lifecycle. Never recreate revoked credentials during repair.

## 21. Deletion and pending-setup cancellation

**Preserved user guards:** deletion is admin-only and requires no retained owned alerts, including resolved/suppressed alerts, and no pending admitted inputs. Recheck atomically under tenant coordination. An eligibility rejection returns 409 with tenant-scoped counts and changes neither operator nor keys; no early purge is allowed. Completed receipts, tombstones and unavailable references do not block deletion.

**User correction — Grafana must succeed first:** do not mark the operator deleted or release its name before required Grafana changes have succeeded. **Assistant-selected workflow:** after eligibility passes, persist a deletion operation and fence new admissions under the same coordination, preventing new alerts from invalidating that eligibility during remote work. Show Deletion pending and disable Copy while it runs. This is a deletion-progress restriction, not the excluded general disable/enable feature. Preserve the operator record/name claim and existing key state until successful completion; explicit key revocation and natural expiry still apply independently.

Fence/cancel pending key-provisioning generations so they cannot activate during deletion. Remove only this operator's routing-label key from affected Grafana rules, preserving the rules and all other fields. Remove its managed policy entry and contact point, preserving the company branch and other notifications. Read back the relevant configuration and confirm absence; an acknowledged not-found result is valid cleanup evidence, an outage is not. Unmanaged references to the contact point, insufficient rule access, externally locked rules, incomplete inventory, or ambiguous writes block completion with a visible error. Do not force-delete rules or unrelated references to clear a blocker.

Only after verified Grafana success, atomically recheck eligibility and generation, mark the operator deleted, revoke every remaining key, erase application credential ciphertext, release its name, append audit and enqueue remaining Kong cleanup. From this commit the name is reusable. Kong cleanup may finish later because authoritative admission rejects the deleted identity; Grafana cleanup is no longer deferred past deletion completion. If remote work fails, keep Deletion pending and the name reserved, and retry. Late remote effects target the original resource IDs and cannot revive a deleted operator or affect a different operator reusing its name.

Deleting an initial Setup pending operator follows the same gate: cancel its setup generation, verify/remove any partial Grafana resources, and commit deletion only after successful verification. An admin may cancel a deletion before the final commit. Restore this operation's Grafana label/resource changes with current-version checks before clearing the admission fence; preserve unrelated rule edits and never reactivate a revoked/expired key. Failed restoration remains pending. Once deletion commits, it cannot be undone; reusing its name creates a new operator.
## 22. Retention and audit

Keep nonsecret credential metadata while the operator exists, plus 365 elapsed days after operator deletion or until referenced admitted work/history is gone, whichever is later. Keep detailed operator configuration/name history and key/management/retrieval audit for 365 days from each action, extending only where a retained record requires that reference. Completed provisioning-attempt detail lasts 90 days; unfinished work persists. Keep minimal deleted-operator IDs, credential-ID denial bindings and cleanup/replay fences indefinitely until a verified replay-safe purge horizon is designed. They do not reserve names or retain raw keys/alert content.

Audit actor stable ID/display snapshot, tenant/operator/credential record IDs, operation ID, action, before/after nonsecret state, time and outcome. Include creation/rename/deletion, key prepare/activate/rotate/revoke/expire, copy retrieval, cancellation/retry, remote repair and platform connection changes. Never include raw key values, wrapping keys, management credentials, Authorization headers or secret-bearing remote bodies. Audit successful mutations in the same authoritative transaction. Tenant admins read their operator audit; global super-admins read platform/cross-tenant operations. This selects operator-scope retention, not a new retention policy for unrelated tenant configuration.

## 23. Product API contracts

Use `/api/tenants/{tenant_id}/operators` for list/create, `/{operator_id}` for detail/name PATCH/delete, and these subresources: `/keys/current/copy` (POST), `/keys/rotate` (POST), `/keys/create` (POST), `/keys/{key_id}/revoke` (POST), `/keys/revoke-all` (POST), `/operations/{operation_id}` (GET), `/operations/{operation_id}/retry` (POST), `/operations/{operation_id}/cancel` (POST for pre-activation rotation or uncommitted rename/deletion, with verified restoration before cancellation completes), and `/audit` (GET). Initial setup cancellation uses DELETE operator. Every nested ID is checked against the tenant/operator; no cross-tenant lookup by name reveals details.

Creation returns 201 after verified completion. Rename, deletion, rotation, revocation and retry/cancellation return 200 only after their required verification completes. Incomplete requests return failure with the durable operation reference; see worker scope for partial-outcome and timeout semantics. Copy returns 200 only for a currently copyable key. Validation is 422, semantic conflict/stale revision/name taken/no copyable key is 409, permission failure 403, concealed resource 404, and unavailable durable command/decryption service 503. Operation reads contain progress and sanitized failures, never credentials. A pending operation is not a completed setup or deletion cleanup. Use the selected command idempotency and revision rules, and keep management separate from ingestion authentication.

## 24. Platform credentials and configuration changes

**Current scope (REV-34):** Platform credentials are mounted into the Product API for request-owned provisioning; there are no provisioning workers to switch; see [worker scope](spec-worker-scope.md#3-request-owned-operator-provisioning). Credential separation and migration rules below remain normative.

Use separate restricted credentials for Grafana management, Kong management and application key wrapping. Rotate platform service credentials by installing and verifying a new secret version, switching workers, then retiring the old version; do not rotate tenant keys as a side effect. Tenants cannot select arbitrary remote hosts. Endpoint/organization/namespace changes are explicit global-super-admin migration operations: validate the destination, inventory owned resources, prepare/reconcile replacements and switch only with an audited plan. Ordinary retries must never silently create the fleet in another Grafana organization. Live migration orchestration belongs to platform deployment work, not a tenant operator feature.

## 25. Operational visibility

**Current scope (REV-34):** Retry sweeps and five-minute reconciliation are not deployed; a failed operation waits for explicit retry; see [worker scope](spec-worker-scope.md#3-request-owned-operator-provisioning). Metrics, monitoring signals and secrecy rules below remain normative.

Expose pending-job age, last successful reconciliation, setup/rotation/cleanup failure counts, rejected admissions by reason, Grafana mapping/truncation errors, and expired/revoked credential rejections without secrets. Create platform monitoring signals after 15 minutes of persistent failure and clear them on recovery; recurring attempts do not create endless duplicate incidents. Do not send email/Slack or notifications outside existing product/platform monitoring as part of this design. Tenant UI shows its own operation state and errors only. Retry sweeps and five-minute reconciliation are scheduling targets, not a system-wide availability SLO.

## 26. Concurrency and failure verification

See [required operators checks](../verification/verification-plan.md#operators).

## 28. Restoration and replay boundary

Restoring a database snapshot must not automatically revive revoked/expired credentials or deleted operators from that snapshot. Keep v2 admission and provisioning activation fenced during recovery until platform reconciliation proves credential/deletion state against current authoritative recovery evidence. If that cannot be proved, invalidate the restored credential set and require new-key provisioning for independently verified surviving operators before reopening v2 ingestion; preserve operator/alert IDs.

Operators whose existence/deletion state cannot be verified remain fenced rather than being recreated from the snapshot. Never use old operation/audit replay to regenerate a revoked secret or reset an overlap deadline. Reliability supplement 17–18 assigns backup/restore to the dedicated teams and requires an agreed independently current recovery-evidence interface, with application verification in section 23/N4; this remains the mandatory credential-safety boundary that implementation must satisfy.

V1 recovery and broader alert replay continue to follow their selected contracts.

## 29. Isolated local development

The isolated development stack installs the actual appchi-policy Lua plugin alongside Kong OSS Key Auth and exercises the same policy evaluator and non-ingesting proof routes. Native UUID/Keycloak development exceptions remain unchanged. Bind the observed node-local gateway identity and actual installed versions; synthetic identity-only readiness is not plugin proof. Local results are development evidence, not qualification of a shared company fleet. See [local v2](https://github.com/appchi-alert-operations/appchi-delivery/blob/main/docs/local-v2.md) and [Kafka-first pipeline](spec-kafka-alert-pipeline.md) section 7.
