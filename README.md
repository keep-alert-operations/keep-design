# keep-design

Authoritative system specifications, design decisions, architecture and verification requirements.

See [system design](https://github.com/keep-alert-operations/keep-design), [workspace setup](https://github.com/keep-alert-operations/keep-delivery) and [source provenance](SOURCE.md).

## Reading order

Start with the [context map](context/map.md) and [context guide](context/README.md).
Choose the sources applicable to the task and expand when dependencies or
uncertainty emerge. Behavior, architecture and cross-repository changes require
the relevant [system design](specs/spec-alerts-management-system.md),
[current worker scope](specs/spec-worker-scope.md), contracts and acceptance
requirements. Read introductory scope corrections with selected sections; a
section that a later decision changes also carries a **Current scope** note.
Domain supplements are in
`specs/`, decisions in `decisions/`, architecture artifacts in `architecture/`,
and acceptance requirements in `verification/`. Implementation evidence is owned
by delivery. Preserve issue IDs and distinguish user choices, assistant-selected
details, normative contracts and historical examples.

Current repository and deployment ownership: [REV-37 repository layout](specs/spec-repository-layout.md).
