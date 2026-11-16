# Observability: logs, metrics and RUM

**User decisions — 2026-11-12 (REV-74).** Every Keep service emits structured logs
and metrics, and the browser reports real user monitoring (RUM). This supplement is
the signal contract. Objectives, alert thresholds and telemetry ownership stay in
[Reliability and operations](spec-reliability-operations.md) sections 2–5, 20 and 21;
implementation and executed evidence belong in delivery. Assistant-selected details
are labelled in the [design register](../decisions/design-register.md#rev-74--observability-logs-metrics-and-rum-2026-11-12).

## 1. Scope and ownership

Logs say what happened in each service. Metrics give current numbers. RUM reports
what users experience in the browser. Every flow and every failure path produces a
log record and moves a metric. Distributed tracing is not built in this scope; the
1% trace sampling in reliability 20 stays a recorded gap.

Keep owns its instrumentation, the log record contract, the shipping client and the
single Fluent Bit deployment. Whoever operates Prometheus or the OpenTelemetry
collector, and whoever operates the logs Elasticsearch, owns collection, storage,
retention, access control and index settings. This design configures none of those.

No new deployed application component is added (worker scope, REV-34 to REV-36).
Fluent Bit is log transport, not an application worker.

## 2. Log records

Each event is one JSON object using Elastic Common Schema names, nested by namespace.
Every record is written to stderr and, when shipping is configured, sent to Fluent
Bit. The stderr copy may be rendered as `event key=value` text for a local console.

| Field | Content |
|---|---|
| `@timestamp` | UTC time from the application clock, millisecond precision |
| `log.level`, `log.logger` | `debug`, `info`, `warning` or `error`; logger name |
| `message` | A plain sentence saying what happened |
| `event.action` | The fixed snake_case event name |
| `event.outcome` | `success`, `failure` or `unknown` |
| `event.duration` | Nanoseconds, where the event has a duration |
| `event.sequence` | The order of a step within one alert's pass through a service; section 3 |
| `service.name` | `ingestion`, `processor`, `correlation`, `indexer`, `api`, `frontend`, `browser` or `migrations` |
| `service.version`, `service.environment`, `service.node.name`, `process.pid` | Build revision, environment, instance name, process ID |
| `error.code`, `error.type`, `error.stack_trace` | The error code the API returns; exception class; file, line and function frames |
| `http.request.id`, `http.request.method`, `http.response.status_code` | The server-generated request ID, method and status |
| `user.id` | The principal's UUID |
| `keep.role`, `keep.route` | Workload role; route template |
| `keep.tenant_id`, `keep.incident_id`, `keep.operator_id`, `keep.rule_id`, `keep.window_id`, `keep.preset_id`, `keep.dashboard_id`, `keep.assignee_id` | Resource identifiers; the assignee is a principal UUID |
| `keep.alert.*` | The alert; section 3 |
| `keep.delivery_id`, `keep.changed_event_id`, `keep.command_id`, `keep.operation_id` | Work identifiers |
| `keep.kafka.topic`, `keep.kafka.partition`, `keep.kafka.offset`, `keep.kafka.consumer`, `keep.projection_seq` | Positions |
| `keep.outcome`, `keep.reason`, `keep.cause`, `keep.status_before`, `keep.status_after`, `keep.revision`, `keep.suppressed` | The domain outcome and its cause |
| `keep.count`, `keep.member`, `keep.attempt`, `keep.repeats`, `keep.fields`, `keep.time_defaulted`, `keep.audit` | Batch size, index of the alert in its request, attempt number, number of like records not written since the last one, names of the fields a rejected alert got wrong, whether the creation time was defaulted, audit marker |

Every field is declared once, with one type, in a field registry in `keep-domain`,
and every event once in an event catalog there. A record may use only registered
fields and registered events. Because the logs Elasticsearch is not configured by
Keep, this registry is what keeps each field's type stable across services.

Request identifiers stay server-generated. An inbound `X-Request-ID` is not trusted
as the identity of a request.

## 3. Alert content in logs

**User decision.** The alert is in the logs, so records can be found by application,
component and the alert's other fields. This supersedes "alert bodies" in the
redaction sentence of reliability 20 for log records only. Metric labels are
unchanged (section 7).

`keep.alert.*` uses the alert's native field names
([alert operations](spec-alert-operations.md)):

| Fields | Records |
|---|---|
| `id` | Every record that concerns an alert, from the source processor's identity lookup onward |
| `key_digest` | Every ingestion record of a valid alert, and source-processor records |
| `application`, `component` (v2), `object` (v1), `node_name`, `name`, `site`, `severity`, `status`, `native_version`, `provider` | Every alert-level record written where the service holds the alert's content: every ingestion and source-processor step, correlation's attachment and outcome records, and the indexer's searchable record |
| `message`, `impact`, `runbook_url`, `operator`, `time_created`, `key_field` | The whole-alert records: the source processor's record that an input was applied or refused, and ingestion's record of a member that is rejected or whose publication is unconfirmed |

Ingestion handles an input before an alert identifier exists and has no PostgreSQL
dependency. Its records carry the identifying fields and `key_digest`, the native
identity digest; the source processor records the same digest beside `id`.

Only registered field names are used. A sender-supplied field name never becomes a
log field. A member rejected for unknown or missing fields is recorded with the
fields it had under their known names and the names of the offending fields as the
reason. The exact original JSON is not repeated.

**The alert's flow inside each service (user decision, 2026-11-12).** Each service
records every step an alert takes inside it as its own record, so the logs show
where an alert is, what each service decided about it and where it stopped.

| Service | Steps of one alert, in order |
|---|---|
| ingestion | `alert_received`; `alert_validated` or `alert_rejected`; `alert_publish_failed` for each attempt Kafka did not confirm; `alert_published` or `alert_unconfirmed` |
| processor | `alert_consumed`; `alert_matched` (an existing alert or a new one) or `alert_replayed` (already applied); `source_receive_time_ahead` when it waits for the clock; `alert_applied` (created, updated, unchanged, resolved or reopened) or `alert_refused`; `alert_change_published` or `alert_input_committed`; `source_partition_retry` or `source_partition_fenced` when it fails |
| correlation | `alert_change_consumed`; `alert_changed` and `alert_incident_attached` for each alert a decision attached; `alert_correlated` (incident created, attached or no incident) or `alert_correlation_skipped` with the reason; `changed_partition_retry` when it fails |
| indexer | `alert_change_consumed`; `alert_indexed` or `alert_index_deferred`; `changed_partition_retry` when it fails |
| api | `alert_changed` for each alert a request changed, naming the cause (`set_status`, `set_assignee`, `set_dismissal`, a note, an incident link, unlink or move), the user, the status before and after and the revision; `alert_notification_published` when the change is sent to Kafka, or `alert_notification_unconfirmed` or `alert_notification_failed`; then the request's own `http_request` record |

**Every change to an alert is a step.** A change that does not come from a
delivered input is recorded as `alert_changed` by the code that publishes it,
in whichever service made it: a user's command in the Product API, a link made
by correlation, or a maintenance effect. It carries the alert's identifying
fields and the ID of the changed event that change produced, which correlation
and the indexer then record under the same ID. A bulk request leaves one
`alert_changed` for each alert it changed.

A Product API request is one pass. Its steps carry the request ID and the
user. A command that is refused (a revision conflict, a missing permission)
changes nothing and leaves only its `http_request` record, which carries the
error code, the user and, when the alert is named in the path, the alert ID.

- **One pass, one set of identifiers.** A pass is one delivered input in ingestion
  and the source processor, and one changed event in correlation and the indexer.
  Every step of a pass carries what the pass has learned so far: the request ID and
  the alert's index in its request (ingestion); `keep.delivery_id` (every ingestion
  step of a valid alert, the source processor, and correlation for a change a
  delivery caused);
  `keep.changed_event_id` (the source processor's applied and published records,
  and every correlation and indexer record); the key digest, the alert ID once it
  is known, and the Kafka position.
- **Order.** `event.sequence` numbers the steps of a pass from 1, so they sort
  correctly even when several share a millisecond.
- **True after commit.** A step that reports a PostgreSQL effect is written only
  after that transaction commits. An attempt that rolls back leaves its failure
  record and nothing saying the effect happened. The shared unit of work does
  this for every service: steps noted inside it are written at its commit and
  dropped at its rollback.
- **A failed step is the same record as the failure.** The retry or fence record
  of a partition is the last step of the alert that caused it and carries its
  identifiers; the failure is not recorded twice.

Every step is recorded; none is sampled. A setting reduces the trail to each
service's outcome records (published; applied and change published; correlated;
indexed). Failures, refusals and rejections are always recorded.

## 4. What is never logged

Credentials, tokens, cookies, session identifiers, CSRF tokens, API keys, database
and service addresses, query strings, CEL and search text, user names, display
names, email addresses, request and response bodies other than the alert fields of
section 3, and exception message text. Exceptions are recorded as class, controlled
error code, SQLSTATE and stack frames.

A sign-in is recorded as one event for its outcome: completed, rejected or
unavailable, with a reason from a fixed list. Only a completed sign-in names the
user, by ID. The typed username is never logged, because a rejected one names
nobody Keep knows and can be a mistyped password.

## 5. Log quality rules

1. Every record says what happened, to what, with what result, and why if it failed.
   Each event's catalog entry lists its required fields.
2. Every event is registered with its level, message, when it fires and what to do.
   The operations runbook's event reference is generated from the catalog.
3. One record per fact. A failure is recorded once, by the operation that met it.
4. `error` means a person needs to look. `warning` means degraded or failed but
   recovering, and every 5xx response. `info` is a business or lifecycle fact.
   `debug` is off in production.
5. A condition that persists is recorded when it starts, at most once a minute with
   a repeat count while it lasts, and when it ends. Polls, heartbeats, probes and
   metric scrapes are not recorded individually.
6. Successful automatic refreshes of the same route by the same session within a
   minute are recorded as one summary. Failures and slow requests are always
   recorded individually. Metrics count every request. A successful read,
   search or session check, repeated by the same user for the
   same resource, is written the first time and then once a minute with the
   number left out in between; a request slower than one second is always written.
7. Library loggers run at `warning` through the same formatter.

## 6. Shipping and indices

**User decisions.** One Fluent Bit deployment receives the logs of every service
and writes them to Elasticsearch, one index per service. Keep configures no
retention, templates, roles or other Elasticsearch settings. The logs Elasticsearch
and the alert-search Elasticsearch are configured independently and may be the same
cluster or different ones.

Each service posts its records to Fluent Bit over HTTP in batches from a background
thread, to the path named for its service. Shipping never blocks or fails the work
being logged: an unreachable Fluent Bit is retried with backoff, a full queue drops
its oldest records from shipping and counts them, and the stderr copy remains.
Ingestion's admission path gains no dependency beyond Kafka. Queues are flushed on
shutdown.

Fluent Bit routes by request path to one Elasticsearch output per service, writing
to `keep-logs-<service>`. It leaves the application's `@timestamp` as the event time
and adds its own receive time as `shipped_at`; a batch sent twice cannot duplicate
records. Index names and the logs Elasticsearch connection are
Fluent Bit settings. The alert-search connection keeps its existing application
settings. Browser records are written by the Product API under `service.name`
`browser` and go to their own index.

Only records written through the logger are shipped. Output that bypasses it, and
records still queued in a process that is killed outright, remain in the container
log.

## 7. Metrics

Metrics are Prometheus-format and served at `/metrics` on a dedicated metrics port
in every process, for collection by Prometheus or an OpenTelemetry collector. The
public application ports do not serve `/metrics`.

Names start with `keep_`, use seconds and bytes, and counters end in `_total`.
Histogram buckets include each objective's threshold. Labels are closed sets defined
in code: service, role, route template, method, status, outcome, error code,
consumer, partition, dependency, operation and similar. No tenant, alert, operator,
user or source value is a metric label.

**Every recorded event is also a number.** Each catalogued log event increments
one counter under the event's own name, with its outcome and its reason, cause
or error code, whether or not the record is written at the configured log
level. An event that carries a duration, or the delay since the receipt or
change it follows, is also observed in a histogram under the same name. A flow
or failure that is logged is therefore always counted, and the logs and the
metrics share one vocabulary. HTTP requests are counted by route instead.

Kafka consumer lag, committed and end offsets, client queue depth and broker
state come from the Kafka client's own statistics, with no extra broker calls,
and only where a metrics port is configured. Only clients that live as long as
their process and are polled regularly report statistics; the source processor's
per-partition transactional producers, administration clients and probes do not.

State held in PostgreSQL (backlogs, watermarks, blocked rules, pending operations) is
read by bounded aggregate queries inside existing processes when scraped, with a
short cache and statement limit. A failed read is reported as a collector failure,
not as a failed scrape.

## 8. Service level classification

Each HTTP request is classified once into `ingest_v1`, `ingest_v2`,
`ingest_grafana`, `read`, `command`, `search`, `operator_command`, `validate`,
`auth`, `live`, `rum`, `admin` or `health`, and its outcome into good, bad or
excluded under reliability 3. Every registered route has exactly one class; a
request that matches no route is `unmatched` and always excluded.
Recording rules over these counters give the availability and latency indicators of
reliability 2–5. Application metrics begin at Keep's own listener; edge and gateway
numbers come from their owning teams and the difference is a recorded coverage gap.

## 9. Real user monitoring

**User decision.** RUM goes through the Product API. The browser collects page-load
timings, navigation, view loads, API calls as the browser sees them, command
outcomes, live-connection state, panel loads and JavaScript errors, and posts
bounded batches to a same-origin endpoint. High-frequency timings are aggregated in
the browser.

The endpoint requires the session and CSRF token, validates strictly and limits
each session's rate. It accepts at most
100 events and 64 KiB per request. It turns events into metrics and writes error
events as log records. It is excluded from the Product API's own indicators. Events
carry route templates and resource identifiers, never addresses, query text or
content.

Nothing a browser sends becomes a metric label unless it belongs to a closed set
held by the Product API: the sections of the UI, the application's own route
templates, and fixed lists of outcomes, states and reasons. An event outside them
is counted as invalid and dropped. A JavaScript error is recorded as its class and
its same-origin stack frames, never its message text, as section 4 requires of
server errors. A failed API call is recorded with the failed request's own ID, so
it joins the Product API's record of that request. An unhealthy clock does not
refuse monitoring events, because they change no Keep data. A browser that is told
the endpoint does not exist stops sending for the rest of its session.

The rendered-visibility acknowledgement protocol of
[alert-history technical design](spec-alert-history-technical.md) section 21 is
unchanged and is not provided by RUM. A RUM estimate of receipt-to-screen delay is
always labelled an estimate and never reported as that indicator.

## 10. Configuration and rollout

Everything is additive and off unless configured: no metrics listener without a
metrics port, no shipping without a Fluent Bit address, RUM behind its own setting.
The alert's step records are on by default and can be reduced to outcome records.
No Kafka record value, HTTP response or stored data changes shape. Unset, behavior
is unchanged except that stderr logs are structured.

## 11. Qualification

See [required observability checks](../verification/verification-plan.md#observability-rev-74).
