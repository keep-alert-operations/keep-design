# Current service flow

The diagram below reflects Kafka-first admission, REV-34–36 worker scope, the
REV-37 repository split and REV-73 password sign-in with the ADAPI directory. PostgreSQL remains transactional authority; Kafka offsets
advance only after the required durable application proof.

```mermaid
flowchart LR
    V1[Native v1 - fixed Global] --> IN[Ingestion API<br/>keep-ingestion]
    V2[Native v2 / Grafana] --> KONG[Kong / operator policy]
    KONG --> IN
    IN --> RECEIVED[Kafka alerts.received]
    RECEIVED --> PROC[Source processor<br/>keep-processor]
    PROC --> PG[(PostgreSQL authority)]
    PROC --> CHANGED[Kafka alerts.changed]
    CHANGED --> CORR[Correlation<br/>keep-correlation]
    CORR --> PG
    CHANGED --> IDX[Indexer<br/>keep-indexer]
    PG -->|committed snapshots / reconciliation| IDX
    IDX --> ES[(Elasticsearch projection)]
    UI[Frontend<br/>keep-frontend] --> API[Product API + live publishing + SSE<br/>keep-api]
    API --> PG
    API --> ES
    API --> REDIS[Redis hints + search cache]
    REDIS --> API
    API -->|SSE + PG reconciliation| UI
    AD[Active Directory<br/>LDAP bind] -->|password check at sign-in| API
    ADAPI[ADAPI directory REST] -->|sign-in lookup, search, save on pick| API
    ADAPI -->|directory refresh command, daily CronJob or by hand| PG
    MIG[keep-migrations] -->|explicit ordered migration job| PG
```

`keep-domain` and `keep-contracts` are libraries/artifacts shared by the relevant
processes. They do not run as services. `keep-delivery` owns deployment and system
verification; `keep-design` owns normative design. See
[repository ownership](../specs/spec-repository-layout.md).

The preserved `keep-service-flow.png` is a **historical pre-Kafka-first image**.
Its direct SQL admission/outbox relay and generic ingress labels are superseded by
the current diagram and specifications. Retain it as design provenance only.
