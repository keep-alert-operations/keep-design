# Independent Keep repositories

Status: user-authorized repository split, 2026-10-01 (REV-37). This supersedes
the monorepo and shared backend image selections in system completion. Product
behavior, database transaction boundaries and current worker scope are unchanged.

## Ownership

| Repository | Authoritative contents |
|---|---|
| keep-frontend | Next.js application including the sign-in page, UI tests, generated HTTP types, frontend image |
| keep-api | Product routes, password sign-in and human sessions, directory search and save on pick, management commands, synchronous operator provisioning, live publishing and SSE |
| keep-ingestion | Public v1 and private v2/Grafana Kafka admission, gateway proof, Kong policy, ingestion image |
| keep-processor | Kafka source consumer, alert source processing and source transaction entrypoint |
| keep-correlation | Changed-record consumer and correlation worker entrypoint |
| keep-indexer | Elasticsearch writer, changed-record consumer, reconciliation, local search bootstrap |
| keep-domain | Shared Python domain rules, persistence helpers, authority/recovery checks and infrastructure adapters |
| keep-contracts | Native/Kafka wire models, serialization and generated HTTP/event schema artifacts |
| keep-migrations | Complete ordered Alembic/PostgreSQL migration chain and checksum-verifying migration runner/image |
| keep-delivery | Workspace setup/AGENTS, deployment templates, local dependency services, system tests, runbooks, implementation evidence and revision inventory |
| keep-design | Normative specifications, decision register, architecture/design assets and acceptance requirements |

The service name is **Ingestion API**. The repository is `keep-ingestion`.
Network ingress remains a network concept. A repository rename alone does not
rename wire fields, Kafka roles, native endpoints or deployed database roles;
such migrations require explicit contracts. [REV-67](../decisions/design-register.md#rev-67--the-system-is-named-keep-2026-11-10)
is that contract for the rename from Appchi to Keep, including migration `0066`.

## Package and runtime boundaries

Assistant-selected implementation details:

- Python distributions own disjoint modules in the `keep` namespace under
  `src/`. Namespace paths support coordinated editable development; no source
  file has two runtime owners. Contracts may not depend on domain or applications;
  domain may not import service implementations. Services depend on contracts and
  domain, never another service. Delivery may depend on all packages for system tests.
- `keep-domain` is a versioned library, with no process, port or deployment.
  Shared transactional helpers accept the existing connection. Repository
  boundaries do not introduce HTTP calls inside PostgreSQL transactions or give
  each service an independently managed copy of the shared database schema.
- Product API and Ingestion API have separate application factories. Product API
  never mounts admission routes, including in development. Ingestion owns only
  Kafka admission and health endpoints; it starts no SQL, Redis, CEL or directory
  adapter. It still validates any supplied capacity profile before startup.
- Processor, correlation and indexer have distinct process entrypoints and images.
  Shared consumer mechanics receive an explicit service-owned handler. Indexer
  PostgreSQL reconciliation remains usable during unavailable Kafka hints.
- Delivery retains the legacy dispatcher for explicit helpers and historical
  verification. Active worker templates use the service entrypoints. REV-34–36
  deferrals and Product API live publishing remain authoritative.
- Internal Python requirements carry immutable Git commit references. Each project
  commits its own `poetry.lock`; frontend locks the contracts Git revision in npm.
  Local editable overrides do not alter release pins. A contract change requires
  compatible producer and consumer checks before downstream pins are advanced.
  The user selected Poetry for all Python repositories on 2026-10-12; current
  commands and the preserved resolution constraints are documented in delivery's
  [workspace setup](https://github.com/keep-alert-operations/keep-delivery/blob/main/docs/repository-workspace.md).
- Contracts owns the checked schema artifacts. Delivery generates product and
  ingestion OpenAPI from their separate installed producers, then merges the
  compatible documents for frontend type generation. Producers never load their
  implementation from the contracts repository.
- Migration SQL bytes and ordering are preserved during extraction. Migration
  execution is an explicit deployment step before new writers; services never
  migrate automatically. PostgreSQL remains the single transactional authority.

## Workspace and release identity

Develop from a non-Git parent directory containing all eleven independent Git
checkouts and the system-wide `AGENTS.md`. Its canonical source is delivery's
`workspace/AGENTS.md`; the bootstrap command installs the parent copy. Each
repository also has scoped guidance. No submodules or parent Git history are required.

Delivery's `workspace/manifest.json` pins the other ten repositories. Delivery is
identified by its own checked-out commit, avoiding a self-referential commit hash.
The generated inventory records every actual revision, dirty state, deviations
from the pinned set, migration checksums and design revision. A release must reject
dirty or mismatched checkouts and additionally record image digests, SBOMs, scans,
configuration/capacity bindings and executed qualification evidence. A source
inventory alone does not qualify a production release.

The original monorepo is retained. Extraction preserves filtered file history and
records the original commit plus the captured local working state in `SOURCE.md`.
Historical evidence describes its original code and environment; it is not proof
for a new repository revision. Production deployment and shared infrastructure
changes remain separately authorized activities.

## Alembic migration execution (REV-38)

**User decision — 2026-10-01:** use Alembic for the PostgreSQL migration chain.
**Assistant-selected transition:** retain every published SQL filename, byte,
checksum and numbering gap. One linear Alembic revision chain executes those SQL
files. The packaged checksum manifest is `migration_sql/checksums.json`.
`schema_migrations` remains immutable application history; `alembic_version`
records the current revision. Each must describe the same ordered prefix.

An existing database without an Alembic version table may be adopted only after
all applied names/checksums form a complete known prefix. Adoption preserves its
ledger rows/timestamps and does not rerun applied SQL. Reject unknown, changed,
missing, non-prefix or inconsistent histories. Validate pending SQL against the
packaged manifest before execution. Adoption, pending SQL and ledger/version
changes share the existing PostgreSQL advisory transaction lock and commit or
roll back together. Runtime API/worker roles cannot access either ledger.

Keep the existing migration job, identity and before-writer ordering. Alembic
adds no service database, ORM requirement or startup migration. Existing offline
cutover and stopped-worker prerequisites remain. Use forward corrective migrations;
no arbitrary stamping, schema downgrade or offline execution bypasses checksum
and history verification. Stop using the legacy runner after adoption. The
`current` command is read-only; history/heads inspection needs no database.
