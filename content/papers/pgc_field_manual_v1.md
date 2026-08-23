---
title: 'Protocol-Governed Computing: Field Manual'
date: '2026-08-22'
weight: 40
slug: field-manual
---
**Author:** Bhash Ganti (aka Bachi)

**© 2026 Bhash Ganti. All rights reserved. Released under the Apache-2.0 License.**

**Audience:** architects · compiler engineers · runtime engineers · governance engineers · AI coding
agents under human supervision

---

## What this manual is

A high-density restoration artifact. Its purpose is to rebuild the correct mental model of
Protocol-Governed Computing in under thirty minutes — not to teach it, not to document code, not to
walk a codebase.

**What it is not.** Not the architecture and not the standard. The architecture is developed in the
three papers; the standard is the sealed snapshot plus the conformance definition. This manual is
how you *operate the reference implementation* and read its artifacts correctly. Where this document
and a compiled artifact disagree, the artifact wins.

**Reading rule.** When something is ambiguous, governance overrides implementation convenience. That
single rule settles most decisions correctly.

**This revision.** v1 supersedes v0. It corrects the identity model — governance namespaces no
longer carry an `fb.` prefix, and authority and concern are declared fields rather than parts of a
name — and adds *The human block* (§4), which states what the prose beside a machine block is for
and what it may not become. v0 remains archived under its own DOI as the superseded record.

**PGC is not** workflow orchestration with governance wrappers · a policy engine · a runtime
authorization framework · a service mesh · a BPM engine.

**PGC is** compile-time construction of admissible execution.

### For AI coding agents

PGC contains constraints that general-purpose agents violate without meaning to — they add
convenience abstractions, collapse boundaries, push domain logic into the runtime, and introduce
fallbacks. These are non-negotiable before any substantial change:

```
no fallback logic          no runtime discovery
no heuristic resolution    no ambient authority
no short-name artifacts    no dynamic imports
compile-time governance    no runtime topology synthesis
strict layer separation
```

| Situation | Read |
|---|---|
| Orientation from cold | §1 · §2 · §3 |
| Compiler work | §6 · §4 |
| Runtime work | §7 · §8 · §14 |
| Transport work | §9 |
| Inspection work | §10 |
| Changing the system | §11 |
| Debugging | Appendix C · §8 |
| Adding a domain or capability | Appendix D · §4 |

---

## 1. PGC in one page

A governed system's life is **three functions**, and nothing else:

```
   (Bₙ, P) ──𝒯──▶ Bₙ₊₁ ──𝒞──▶ Sₙ₊₁ ──Φ──▶ (R, T)

   𝒯  transformation   a baseline plus a problem becomes the next baseline
   𝒞  compilation      the baseline is sealed into a snapshot
   Φ  execution        the snapshot produces a result and evidence
```

Concretely:

```
protocol artifacts → protocol_compiler → domain projections
    → snapshot_assembler → sealed snapshot → protocol_runtime → result + trace
```

| Step | Statement |
|---|---|
| **Protocol declares.** | What may exist and how it may execute — workflows, capability contracts, governance rules. |
| **Compiler constructs.** | What is admissible is built. What is not admissible is not blocked — it is *absent*, with no path to reach it. |
| **Assembler seals.** | Many compiled domains become one snapshot with a content-derived identity. |
| **Runtime executes.** | Traverses the snapshot and nothing else. It carries no domain knowledge and decides nothing. |
| **Trace proves.** | Append-only execution evidence. If an action is not in the trace, it did not happen. |

Three consequences follow directly:

> The runtime does not decide what may exist — the compiler already decided.
> The runtime does not interpret behaviour — the protocol already declared it.
> The compiler does not execute — the runtime executes only what was sealed.

**The mantra:** *Governance defines. Compiler constructs. Assembler seals. Runtime executes. Trace
proves.*

### Two partitions

Everything in PGC descends from two rules about who is allowed to decide:

| Partition | Rule | Governs |
|---|---|---|
| **Execution Partition** | the compiler determines behaviour; the runtime only realizes it | how the system *runs* |
| **Knowledge Partition** | only a human-directed author may create meaning; a machine may derive it, never originate it | how the system *changes* |

---

## 2. A platform is a composition, not a repository

This is the distinction newcomers most often get wrong, and it is a category error rather than a
detail.

A **Profiled Normative Platform (PNP)** is what you get when a governance surface, a chosen set of
conformance workloads, and optionally business domains are compiled and assembled together **under a
conformance profile**. There are as many platforms as there are profiles. There is no single or
minimal platform, and no repository is one.

```
   software_governance        conformance_workloads       business_domains
   what is GOVERNED           what is EXECUTED to         what is done for
                              prove it holds              a business
          └────────────────────────┼────────────────────────┘
                                   ▼
                        compiler → assembler
                                   ▼
                        ┌────────────────────┐
                        │  sealed snapshot   │   one PNP
                        └─────────┬──────────┘
                                  ▼
                   runtime · transport · inspector
```

A profile is a conformance contract over a snapshot: it states the properties a snapshot **shall**
satisfy, never an inventory of what a build happens to contain. A profile names required governance
artifacts, required component capabilities, required workloads, and the conformance claims the
composition must support.

### The five conditions of a functioning platform

Checkable properties, not adjectives. A platform is functioning when it:

| | condition |
|---|---|
| **composes** | the parts assemble under a named profile into one artifact |
| **seals** | that artifact has a content-derived identity and is reproducible from committed source |
| **executes** | the declared workloads run and produce the effects their declarations require |
| **answers** | it can be interrogated about its own contents through governed operations |
| **proves** | every execution yields evidence sufficient to check that it conformed |

---

## 3. Core doctrine

**Protocol is the source of truth.** Behaviour is carried by protocol artifacts, not by code. Code
may be regenerated, replaced or machine-authored; governance is unaffected.

**The runtime is dumb, deliberately.** It enforces graph structure and interprets no domain meaning.
The same engine runs a blockchain domain, an AI-governance domain and a Collatz workload
identically. Its simplicity is load-bearing: every judgement it declines to make was made, checked
and sealed earlier where it could be reviewed.

**Everything resolves at compile time.** If the compiler did not construct the path, nothing can
traverse it.

**Zero inference.** No implicit defaults, no heuristics, no filesystem scanning, no `cwd`, no `../`.
Undeclared means absent, and absent stops the compile.

**Fail hard.** Missing artifact, missing binding, violated invariant → refusal. No graceful
degradation, because degradation hides architectural violations.

**Determinism.** `Φ(G, input, actor_context) → (result, trace)`. Replay is structural, not
reconstructed.

**No ambient authority.** Code has no authority from its execution context. Authority comes only
from declarations — `AC`, `IN`, `WF`, `CC`. Confused-deputy attacks are structurally absent rather
than defended against.

**Snapshot sovereignty.** The runtime executes sealed state exclusively. To change behaviour: change
source → recompile → reassemble.

**Compression is a feature.** A small ontology with strong invariants beats a large one with
heuristic flexibility. Growing the ontology without governance necessity is debt.

---

## 4. The artifact ontology

### Execution kinds

| Prefix | Name | Role |
|---|---|---|
| `TI_` | Transport Ingress | admits an external request and extracts the declared payload |
| `AC_` | Actor Context | binds execution authority context |
| `IN_` | Intent | admission gate — ACK or NACK before any traversal |
| `WF_` | Workflow | the topology: which contracts execute in what declared sequence |
| `CC_` | Capability Contract | a named node; drives its steps and declares its outcomes |
| `CT_` | Capability Transform | pure computation — no I/O, no clock, no randomness |
| `CS_` | Capability Side Effect | the only governed channel for changing anything |
| `EV_` | Event | a declared moment, announced; **records facts, never triggers execution** |
| `TE_` | Transport Egress | classifies the outcome and projects the declared response |
| `RB_` | Runtime Binding | maps a declaration to an implementation — location, never authority |

### Governance kinds

| Kind | Role |
|---|---|
| `CONSTITUTION` | the rules one kind of artifact is governed by |
| `INVARIANT` | a property the compiler checks and refuses to build without |
| `STRUCTURE` | build configuration — what is compiled, from where, to where |
| `SURFACE` | a surface contract: what a capability's result must look like |
| `VOCAB` | reserved protocol terminology |

**Versions are immutable.** There is no "latest". A behaviour change is a new version (`_V1`,
`_V2`); the old version stays valid and unchanged.

### Identity

```
<namespace>::<ARTIFACT_CODE>_V<n>

  blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0
  capability_side_effects::CS_MUTABLE_JSON_V0
  transport::CONSTITUTION_TRANSPORT_EGRESS_V0
  inspection::TI_SI_STORE_CONSUMERS_V0
```

Governance namespaces are the concern itself — `workflow`, `execution`, `transport`, `structure`.
Capability declarations live in `capability_transforms` and `capability_side_effects`. Business and
tool domains use their own name.

**A namespace resolves names and carries nothing else.** It is not an authority, not a jurisdiction,
and not an ownership boundary. Governance namespaces once carried an `fb.` prefix denoting a
*federation boundary* — a claim of distinct sovereignty. Measured against the composition, all
twenty-six of them were one authority's concerns, and the six candidates for genuinely distinct
authorities carried no prefix at all: the marker for "separate sovereign" sat on everything that was
not one. The prefix is retired.

**What it was carrying is now declared.** Two fields in every machine block:

```yaml
authority: pgc.platform     # from whom jurisdiction derives — CA-1, CA-2
concern:   transport        # the semantic subject — a classification, conferring nothing
```

`authority` must be constituted by a declared constituting act, and no value may be both an
authority and a concern. Both are refused at compile time, and neither could be checked while one
identifier carried both — a check could refuse an *unlisted* namespace but never an *illegitimate*
one, because the two were the same string.

**Folders are discovery; identity is declared.** An artifact's namespace comes from the `fqdn:` key
in its own `## Machine` block, never from the directory it sits in. A file may move without changing
what the artifact *is*.

**Never a short name.** `::` in an identity becomes `__` in a filename. Resolve an artifact through
`artifact_index/index.json` — never by deriving a path from an FQDN, because a namespace is not a
directory.

### The human block

An artifact has two parts and they answer different questions. The `## Machine` block is what the
implementation consumes and the only surface that determines anything. Everything else is prose for
a reader, and **it declares nothing.**

That prose has a job, and it is a job neither neighbour can do:

```
Normative Standard              what PGC requires
        ↓                       cited in the prose, never restated
Human-Consumable Realization    how this artifact realizes it
        ↓                       the prose — this is its whole purpose
Machine Block                   what the implementation actually consumes
```

The standard says what must be true of any realization and deliberately names no mechanism. The
machine block names the mechanism and says nothing about why. A reader holding both still cannot see
how one becomes the other, and reconstructs it every time.

**The failure to guard against is the middle layer growing into the top one.** Prose that explains a
mechanism drifts into prose that requires it; the requirement is then stated twice, once ungoverned,
and readers trust the copy they can read. Three rules keep it in place:

**Cite, never restate.** Every normative claim in the prose is a citation to a named document and
invariant. *"A transport ingress must have a verified, static invocation target"* is a requirement
with no authority behind it and no way to be wrong. *"`5a` IB-5 requires operation-to-target
resolution to be determined before interaction time; this artifact realizes that by…"* points at
something checkable and then explains a mechanism.

**Never restate a machine-block value.** Two copies can disagree; one cannot. This is not
hypothetical: 216 artifacts once carried a `## Header (Mandatory)` block restating artifact code,
kind, governing constitution, version, status and supersession — about 1,265 duplicated lines — and
the copies were already the weaker ones. `**Governed By:** CONSTITUTION_WORKFLOW_V0` sat beside a
machine block declaring `governed_by: workflow::CONSTITUTION_WORKFLOW_V0`: a short name where the
declaration carried an identity. A reader who trusted the prose had a name that resolves to nothing.
Status lines and prose version histories go the same way — supersession is a declared relation, and
a second record of a governed fact is a record that can already be wrong.

**Say what is not claimed.** The strongest guard against over-claiming is an explicit bound, and the
surface contains the model. `INVARIANT_TRANSPORT_TARGET_EXISTS_V0` distinguishes what its check
enforces per handler kind, then writes: *"for those kinds the enforced check is that the target is
declared and static; nothing stronger is claimed."* That sentence does more for a reader than any
restatement of the rule, and it is the sentence a specification never contains — a specification
states what must be true and has no reason to bound its own enforcement.

**Section names must not read as normative.** `Rule Statement`, `Validation Rules` and
`Enforcement Scope` announce that a rule is being stated, in a document that states none. Use *What
this realizes*, *How*, *What is not claimed*. `Intent`, `Purpose`, `Rationale` and `Scope` are fine
where they carry content — `Rationale` especially, since why a shape was chosen is exactly what
neither other layer records.

**Where each part lives.** The policy — the closed sets of forbidden section names and restated keys
— is a governed artifact, `vocabulary::VOCAB_HUMAN_BLOCK_CONSTRAINTS_V0`, compiled and sealed like
any other. `human_block_fidelity.py` reads it from the sealed composition and carries no copy, so
adding a forbidden name is an authoring act rather than an edit to a script. What the check cannot
decide is whether a sentence cites or restates — that is a reading, not a pattern, and it is a review
obligation stated as one.

---

## 5. The governance surface

`software_governance` holds two kinds of thing, and the difference between them is the most
important idea in the repository.

- **Rules** — constitutions, invariants, vocabularies. What may exist and what may never exist,
  enforced at compile time.
- **Capabilities** — the operations a business is permitted to perform. A domain *composes*
  capabilities; it may not invent one.

It contains no business meaning. The test is mechanical: search it for a business noun and find
nothing. It defines the alphabet, never the sentences.

### Transforms are open; side effects are closed

```
   ┌───────────────────────────────┬───────────────────────────────┐
   │  CAPABILITY TRANSFORM  (CT)   │  CAPABILITY SIDE EFFECT  (CS) │
   ├───────────────────────────────┼───────────────────────────────┤
   │  pure computation             │  governed mutation            │
   │  same input, same output      │  changes something outside    │
   │  no files, no network,        │  itself: a store, the clock   │
   │  no clock, no randomness      │                               │
   └───────────────────────────────┴───────────────────────────────┘
            open to extension              CLOSED — six of them
```

A pure transform can do no harm outside itself, so the set may grow. A side effect is how the
platform touches the world, so it is finite, enumerable and reviewable. To know everything a PGC
platform can *do to anything*, read six declarations rather than a codebase.

| capability | what it does |
|---|---|
| `CS_MUTABLE_JSON_V0` | records that change — write, read, update, update-where, delete |
| `CS_APPENDONLY_JSONL_V0` | a trail added to and never rewritten |
| `CS_REGISTRY_V0` | claims a key so two things cannot share one identity |
| `CS_CLOCK_V0` | supplies the current time |
| `CS_SNAPSHOT_QUERY_V0` | reads the sealed platform itself |
| `CS_TEXT_ARTIFACT_V0` | reads and writes text artifacts |

The closure is not a comment — `INVARIANT_CS_SURFACE_CLOSED_V1` names all six, and a seventh does
not compile.

**When a domain needs a mechanism the substrate lacks, the substrate gains it.** A domain
compensating with its own invariant produces a correction carrying an unstated promise wherever it
is copied. Adding to the closed set is a deliberate act with consequences for every platform — never
a convenience for one caller.

---

## 6. Compilation

Nine stages, each with one job. A stage may rely only on what earlier stages established.

```
   S1  EXTRACT              read declarations from source
   S2  CANONICALIZE         one normal form — two spellings, one meaning
   S3  SEMANTIC ADDRESSING  every name resolved to exactly one artifact
   S4  GOVERN          ◀──  the gate. every rule checked.
                            an illegal graph stops here
   S5  CONSTRUCT            build execution structure on the resolved graph
   S6  PROJECT              derive the views downstream components read
   S7  MATERIALIZE          write them out
   S8  VERIFY               check what was written matches what was built
   S9  ATTEST               sign the result as verified
```

**S4 is the gate.** Everything before establishes facts; everything after assumes legality. A
violation stops the whole compile — there is no partial output, because a partially admissible
system is not a meaningful thing.

**S8 exists because writing is not building.** It catches the case where construction was right and
materialization was wrong.

### Non-negotiable

- The compiler never executes an implementation. Admissibility never depends on running code.
- Static imports only. Assertion handlers are explicitly enumerated in a closed registry; a missing
  handler is an immediate failure.
- Deterministic output — same source, same result.
- The compiler validates and refuses. It never repairs.
- Domains are self-describing: adding one requires no compiler edit.

### What it produces

| projection | for |
|---|---|
| `canonical` | the artifacts in normal form — what the assembler seals |
| execution graph | every path a workflow may take, before anything runs |
| `tokenized` | address-resolved dispatch the runtime consults |
| `vocabulary` | every named concept, indexed |
| `evidence` | why each artifact was admitted |
| `behavior_logic` | rendered diagrams of the compiled graph |

That last one matters more than it sounds: **the compiled graph can be looked at.** A reviewer sees
every path, outcome and terminal state of a workflow before it has ever run — not a simulation, but
the literal structure the runtime will walk.

---

## 7. Assembly and the snapshot

The compiler produces one output per domain. The assembler composes them into **one sealed artifact**
and gives it an identity derived from its contents. Many in, one out, then many readers — this is the
only place the pieces become a whole, which is why identity and verification live here.

```
snapshot/
    manifest.json      identity, domains, provenance ← root of trust
    canonical/         the artifacts themselves
    behavior_logic/    execution graphs and rendered diagrams
    artifact_index/    what exists, and where       ← resolve FQDNs here
    kind_index/        what kinds exist
    store_index/       what stores exist, and what consumes them
    vocabulary/        every named concept
    evidence/          why each artifact was admitted
    tokenized/         address-resolved forms
    trust/             attestation
    conformance/       the composition-conformance record
```

**Identity is derived, never assigned.** Change any governed artifact anywhere and the identity
changes. Two people comparing snapshot identities are comparing the systems themselves, not their
descriptions. To *pin* a baseline is to name a snapshot; to claim a build is reproducible is to
rebuild and get the same identity back.

### Checks only possible on the whole

- **Round-trip verification.** The identity is recomputed from what was written and compared with
  what was recorded. A mismatch is a refusal.
- **Copies must agree.** A governance artifact is compiled into every domain that imports it, so one
  identity exists many times. Every copy is compared by content; a composition whose copies disagree
  is refused. This check exists because that failure occurred.
- **Composition conformance.** Rules that quantify over the whole — read from the assembled
  snapshot's own declarations, so **a domain is checked against the governance it actually compiled
  under**, never against whatever the tool happens to know.

**The indexes are not conveniences.** They are what let a composition be interrogated rather than
read. A governed system that cannot answer questions about itself is governed only in principle.

The snapshot is read-only to everything downstream. Nothing writes into it — ever.

---

## 8. Execution

Execution is **governed declarative graph traversal**, not orchestration.

```
   TI → IN (admission: ACK | NACK)
      → WF (traversal of the compiled topology)
        → CC → CT / CS steps → outcome
        → next node, per declared routing on that outcome
      → TE (classification and projection)
```

The scheduler asks one question at each step: *the last step produced this outcome; where does the
graph say that outcome goes?* It looks the answer up. It does not compute, infer, or fall back — a
missing answer is a failure, because the alternative is a runtime inventing a path nobody governed.

**Warm reboot.** The snapshot is loaded once, hash-verified against its manifest, and treated as
immutable for the life of the process.

### Composition rules

- A `WF` contains `IN`, `CC` and exit nodes only. **A workflow never appears inside a workflow.**
- Sub-workflow invocation, iteration and parallelism are declared side effects through a gateway
  `CC`, never runtime orchestration.
- `EV` records that something happened. There is no subscription mechanism; chaining is always a
  declared step.
- **A store is written only by its owning subdomain's contracts.** Cross-subdomain reads are
  declared and permitted; cross-subdomain writes are forbidden without exception.
- Every step's result surface must match the `canonical_surface` its governing surface contract
  declares. Routing a surface is permitted; redefining one is not.

### Purity and the mutation boundary

- `Effect(CT) = ∅`. A transform may call transforms; it may never call a side effect.
- `MutationSurface = { s : s ∈ CS }`. No implicit write path exists anywhere else.

### Outcomes

| gate | vocabulary |
|---|---|
| Intent | `ACK` · `NACK` |
| Contract | `SUCCESS` · `VIOLATION` · `NOT_FOUND` · `BACKEND_ERROR` · domain-declared outcomes |

An outcome that is not in the workflow's routing table is a failure, not a default path.

### Evidence

Execution writes a trace as it happens, not reconstructed afterwards.

| event | meaning |
|---|---|
| `WF_START` / `WF_COMPLETE` | a traversal began / ended |
| `CC_START` / `CC_COMPLETE` | a contract began / ended |
| `CC_STEP` | one step ran |
| `EVENT` | a declared moment was announced |

The trace turns *"this ran and conformed"* from an assertion into something a second party can check
without trusting the first. **Correct behaviour is checkable two ways: the result is what the
declarations require, and the path in the trace is a path present in the compiled graph.** The second
is the one that matters — it tests the guarantee rather than the outcome.

Traces are **output only**. They are never input to the compiler, the runtime, or anything else.

---

## 9. The transport boundary

`protocol_transport` knows **how** to transport and declares nothing about **what** may be
transported. Every business-specific fact — which routes exist, what an operation is called, which
workflow it runs, what a failure means — arrives as data the engine is pointed at.

### An operation is not a workflow

A route names an **Operation Identity**. The identity resolves through compiled boundary contracts to
one of exactly three handler kinds:

| handler kind | goes to |
|---|---|
| `WF_INVOCATION` | the runtime executes a workflow |
| `SNAPSHOT_READ` | the inspector projects published material |
| `SNAPSHOT_QUERY` | the inspector derives an answer |

```
   HTTP request
        ▼
   adapter    binding table (DATA): method + path → operation identity
        ▼
   TI         admit or refuse; extract the declared payload
        ▼
   handler    one of exactly three kinds — a closed table
        ▼
   TE         classify the outcome into a governed Result Class;
              project only the fields the output contract enumerates
        ▼
   adapter    Result Class → HTTP status
```

**Result Classes are protocol-neutral and closed:** `SUCCESS` · `VIOLATION` · `UNAUTHORIZED` ·
`EXECUTION_FAILURE` · `OPERATION_NOT_FOUND`. They carry no status code and no exit code; the adapter
alone projects one onto a wire. `OPERATION_NOT_FOUND` means the identity is absent from the governed
universe — a domain's own not-found is a *domain* result, not a transport one.

**The output contract enumerates every field that crosses the boundary.** A payload is never passed
through wholesale, because a boundary exposing whatever a handler returned declares nothing.

### The acid test

```bash
grep -rniE '<any workload or field name>' resolver/ adapters/
```

It returns nothing. If it ever returns something, this layer has stopped being a boundary and has
started being an application.

---

## 10. Inspection

Compilation answers *is this admissible?* Execution answers *what happens?* Inspection answers *what
does this snapshot contain?*

> Inspection is a **domain**, not a tool. Every question you may ask is a governed operation the
> snapshot itself declares — and answering it never runs anything.

`si.artifact.show` and `si.store.consumers` are identities of the same standing as any business
operation: declared in artifacts, compiled, sealed, attested. Adding, renaming or re-pointing an
operation is an authoring act on a governed artifact, never an edit to a table in code. Two snapshots
may legitimately offer different questions.

| class | authority | examples |
|---|---|---|
| `SNAPSHOT_READ` | projects published material — no traversal, no evaluation | artifact list/show, vocabulary, behaviour logic, capability surface, store list |
| `SNAPSHOT_QUERY` | derives an answer by traversing and evaluating | references, topology impact, snapshot validation |

The split is load-bearing: a read that quietly computed a relationship would be a query wearing a
read's clothes, cheaper to call and carrying authority it never declared.

**One entry point:** `inspector.api.query(operation, params, snapshot_root) → (status, payload)`.
The CLI, the browser surface and CI gates are peers — none privileged, none holding a capability of
its own. A hand-written client command accretes filters the API does not have, and the client
quietly becomes a second inspection engine with answers of its own.

**Why this repository exists:** without it, every consumer wanting to know something about a build
reaches into compiler internals — a dependency on *how the snapshot was made* rather than *what it
is*, which breaks the moment the compiler changes.

**A realization hazard worth remembering:** an inspection answer can be confidently empty and wrong.
Reading the compile trace (`evidence_graph.json`) where the semantic graph (`evidence.json`) was
meant yields an empty result, not an error. Fail hard on a malformed evidence file; never fall back.

---

## 11. Transformation — how the system changes

Everything above governs what the system does. This governs how it becomes something else.

> A change begins as a sentence someone in the business says, and ends as artifacts that compile.
> The pipeline is the graded path between those two things, and it refuses to let a step be skipped.

**Evolution is never greenfield.** Even a brand-new domain compiles against a normative closure that
already exists. The pipeline's distinguishing logic — reuse or extend, where something belongs, who
owns it, whether meaning was preserved — is only meaningful against a baseline. A greenfield run
leaves all of it unevaluated *while reporting success*.

### The language widens as you descend

```
   PHASE                    VOCABULARY ADMITTED         so that…

   p0  change seed      ┐
   p1  change request   │
   p2  domain model     ├─▶ business language only  the business can read
   p3  analysis loop    │                            and correct its own
   p4  business model   ┘                            problem
   ─────────────────────────────────────────────────────────────────────
   p5  business intent   ─▶ + provisional names     WHAT must be true
   p6  governance intent ─▶ + placement             WHERE it belongs
   p7  design intent     ─▶ + bindings, FQDNs       HOW it is realised
   p8  authoring mandate ─▶ + build order           IN WHAT ORDER
```

Each phase admits a strictly wider vocabulary than the one before, and **nothing may be said early
that belongs late**. A problem statement containing a module path has decided the design before
anyone examined the problem, and the phase's rule set refuses it. The one standing exception at every
rung: anything that *already exists* may be named exactly, because naming what exists is observation,
not design.

**Two gates are human, and only two:** Design Approval after p7, and Mandate Approval after p8, at
which point the dossier is locked.

### Two compilers, because they fail differently

| | failure reads as | fixed by |
|---|---|---|
| **Design Compiler** | *the mandate is incomplete or contradictory* | re-authoring a register |
| **Construction Compiler** | *the mandate was valid and did not determine an artifact* | amending the design language |

Different people fix those. Merging the compilers would blur both into "it didn't work".

### Construction completeness

The Construction Compiler measures whether a design determines the artifacts it schedules. The
threshold is **100**, and anything below it is a refusal rather than a warning:

> A fact the design does not state is a fact the generator would have to invent, and a generator that
> invents design is a second, ungoverned design authority.

### The baseline is pinned, and stays pinned

Validation never runs against "the current snapshot". It runs against a **named, frozen** one, and a
run observing a different identity fails before executing a phase.

**The pin lives with the change, not with the pipeline.** Each dossier carries its own, and each
change pins the composition its predecessor produced. A completed change is never re-pinned forward:
approving a register against a composition that arrived later asserts a re-reading of facts the build
already settled. An in-flight change may legitimately re-pin. Rebaselining is deliberate and
reviewed — never silent drift, because otherwise **a regression is indistinguishable from a rebuild**.

### Determinism and the worker

- **Governed and deterministic:** the register schema, the structural oracle, the gates, the mandate.
  These decide admissibility.
- **Assistive and non-deterministic:** a worker drafting prose into a register.

A non-deterministic drafter behind a deterministic oracle and a human gate is coherent. A
non-deterministic *decision* inside a governed pipeline is not. **No phase may depend on a worker
existing.** *The actor proposes; governance disposes.*

### Two hard rules

**Phases, never stages.** A dossier has phases (p0–p8); a compilation has stages (S1–S9). No
document, path, register field or identifier uses one word for the other. A word that names two
things names neither.

**Dossiers are evidence, not artifacts.** A dossier describes a change to a composition; it is not
part of one. It never enters a snapshot, and it lives with the domain it changes — the pipeline
judges dossiers, it does not own them.

### Admissibility is not excellence

A verdict is not a boolean. `ADMISSIBLE` is the gate; the **figure of merit** is a separate judgement
of quality. A document may be admissible while carrying an open question. Conflating the two makes
one of them useless.

---

## 12. Repository map

| Repository | Owns |
|---|---|
| `software_governance` | the governance surface: rules and the closed capability set |
| `conformance_workloads` | workloads whose execution proves the guarantee holds |
| `business_domains` | domains built for a business outcome |
| `protocol_compiler` | source → validated per-domain projections |
| `snapshot_assembler` | projections → one sealed, indexed snapshot |
| `protocol_runtime` | snapshot → execution and evidence |
| `protocol_transport` | the governed boundary — protocol-neutral ingress and egress |
| `snapshot_inspector` | read-only inspection: the `si.*` operations and their surfaces |
| `transformation` | the change lifecycle: design compiler and construction compiler |

**Import package names carry no repo prefix** — the org provides the namespace: `compiler`,
`assembler`, `runtime`, `inspector`, `transformation`.

**Dependency direction.** Everything depends on the governance surface; governance depends on
nothing. The runtime, transport and inspector depend on the *snapshot's on-disk format* — an input
contract — never on the tools that produced it. `transformation` reaches a snapshot only through
`inspector.api.query`; a compiler import there is an architectural violation, and building it without
one is the acceptance test for the whole separation.

---

## 13. Architectural properties

Structural outcomes of the governance → compiler → runtime separation, not design goals.

| Property | Statement |
|---|---|
| **Determinism** | Identical snapshot, inputs and initial state produce identical paths and traces, on every conforming runtime. |
| **Implementation independence** | Implementation can be replaced entirely without changing behaviour; protocol can evolve entirely without changing the runtime. |
| **Runtime multiplicity** | One protocol, one snapshot, many conforming runtimes — all producing semantically equivalent traces. |
| **Hosting transparency** | A deployment decision changes *where* execution happens. It cannot change *what* execution means. |
| **Transport orthogonality** | A workflow is constitutionally ignorant of its invocation surface. Over CLI and over HTTP it is indistinguishable at the topology level. |
| **Trace portability** | Evidence is substrate-neutral and structurally comparable across runtimes. |
| **Security by construction** | Unauthorized behaviour is never constructed, not merely blocked. What was not built has nowhere to occur. |
| **Structural parallelism** | Concurrency is a consequence of declared topology, not something engineered into the runtime. |
| **Governance dividend** | As the governance surface matures, cost-of-change falls rather than rises. Governance complexity compounds; execution complexity does not. |

> The compiler governs possibility. The runtime governs realization. The separation between them is
> where a system becomes governable.

---

## 14. Invariants

Hard constraints. Violation is architectural corruption, not a bug.

| Invariant | Statement |
|---|---|
| FQDN required | Every reference is `namespace::ARTIFACT_CODE_Vn`. No short names, ever. |
| Index resolution | An artifact is located through `artifact_index/`, never by deriving a path from its FQDN. |
| Snapshot immutability | The snapshot is read-only after assembly. Nothing downstream writes to it. |
| Identity is derived | A snapshot's identity comes from its content, never from assignment. |
| Copies agree | Every copy of one identity within a composition is byte-identical. |
| No execution in the compiler | Admissibility never depends on running an implementation. |
| No partial output | A failed compile writes nothing. |
| No runtime discovery | The runtime resolves from the snapshot only; no filesystem scanning. |
| No runtime topology synthesis | Topology is never generated or inferred from payload, environment, or state. |
| Topology immutability | No step is added, removed, or rerouted after compilation. |
| Topology closure | Every step input resolves at compile time; no dangling references. |
| Topology traversal scope | Topology governs sequence only — never authority, never transport. |
| Canonical surface | A step's result surface matches the governing surface contract exactly. |
| CT purity | Transforms have no side effects and never call a side effect. |
| Closed mutation surface | Every state change goes through one of the six declared side effects. |
| No ambient authority | Authority comes only from `AC` / `IN` / `WF` / `CC` declarations. |
| No fallback | Missing artifact, binding, route or handler → hard failure. |
| Static imports only | No dynamic imports, no reflection-based module loading, no handler discovery. |
| No `sys.path` manipulation | Roots are environment-provisioned, never synthesized in code. |
| Trace is output only | Never input to any component. |
| Explicit data root | The instance root is passed explicitly; never inferred. |
| Dossiers stay out | A dossier never enters a snapshot. |
| Baseline pinned | A transformation run against a snapshot other than its pin fails before any phase. |

---

## 15. Anti-patterns

| Anti-pattern | Why it violates PGC | Instead |
|---|---|---|
| Smart runtime | puts domain logic in the execution layer | the runtime is generic; behaviour lives in the snapshot |
| Fallback logic | masks violations; destroys determinism | hard failure; fix the cause |
| Dynamic imports | breaks static resolution; permits injection | static imports; closed registries |
| Filesystem inference | violates zero inference | declare every path |
| Editing the snapshot | modifies compiled output; overwritten next build | change source, recompile, reassemble |
| Trace as input | trace is evidence, not protocol | traces are output only |
| CT calling CS | breaks purity | side effects only through contract-authorized steps |
| Routing in transport | couples boundary to behaviour | routing lives in workflow declarations |
| Role branching in topology | puts authority semantics in traversal | authority resolves before traversal begins |
| Result surface deviation | the author redefines what a capability produces | declare the canonical surface; route, never redefine |
| Event-driven triggering | there is no subscription mechanism | chain through a declared gateway step; events record facts |
| A workflow inside a workflow | workflows are not node types | gateway contract for sub-workflow invocation |
| Cross-subdomain store write | breaks store ownership | a contract owned by the store's subdomain, triggered by the change |
| Authoring what already exists | splits one identity in two | search the index before declaring anything new |
| Reaching into compiler internals | depends on how a snapshot was made | ask the inspector; add an operation if the answer is missing |
| A client that derives | the client becomes a second engine | render answers; never compute relationships |
| Short-name references | breaks identity resolution | always `namespace::CODE` |
| A dead field | reads as meaning; masks a real absence | remove it — a dead field is worse than the work of removing it |

---

## Appendix A: Operations

Every entry script resolves its own roots. No `PYTHONPATH` or `cd` gymnastics required.

### Build a platform

```bash
./protocol_compiler/compile.sh              # the governance surface
./protocol_compiler/compile_domain.sh <d>   # one domain against it
./snapshot_assembler/assemble.sh            # compose · seal · verify · conform
```

`assemble.sh` **with no arguments auto-discovers** the governance surface and every compiled domain.
Any argument bypasses discovery entirely, so an explicit source list silently omits domains added
later. Prefer no arguments.

Environment overrides where needed: `PGC_PLATFORM_ROOT`, `PGC_SNAPSHOT_ROOT`, `PGC_SNAPSHOT_OUT`,
`PGC_SOURCE_ROOTS`, `PGC_IMPL_ROOTS`, `PGC_DATA_ROOT`.

### Execute

```bash
./protocol_runtime/run.sh                    # warm-boot and verify
./protocol_runtime/run.sh run \
    --wf <domain>::<WF_CODE> \
    --payload <file> \
    --data-root /abs/instance/root
./protocol_runtime/run.sh examine /abs/path/to/trace.jsonl
```

**Runtime output is never snapshot.** Traces and governed state go to a separate instance root; the
snapshot is read-only input.

### Inspect

```bash
si --snapshot ./snapshot catalog    # what this snapshot answers
si snapshot summary
si artifact show <fqdn>
si artifact refs <fqdn>             # who references this
si topology impact <fqdn>           # transitive consumer closure
si store consumers <store>
si behavior_logic show <domain>::<WF_CODE>
si snapshot validate
si --json <group> <verb> …          # stable payload for agents and CI
```

Seventeen operations ship in this release — fourteen reads, three queries.

### Transform

```bash
cd transformation
python -m transformation phase list        # phases, rules, vocabulary
python -m transformation phase check --phase p1 <doc> \
    --snapshot ../snapshot --prior p0=<doc>
python -m transformation baseline show --snapshot ../snapshot
python -m transformation construction check <dossier>
python -m transformation phase meta        # rules checked against themselves
```

`phase meta` is the one to trust — it verifies that every declared rule resolves to a check that
exists and every check is declared. A pipeline whose rules are not themselves checkable can quietly
stop enforcing something.

### Verify the environment

```bash
python tools/pgc_env_check.py
```

---

## Appendix B: Layout reference

### Instance state and traces

```
<data-root>/<client>/
    traces/<domain>/<WF_CODE>/<TIMESTAMP>__<WF_CODE>__<ID>/
        *.jsonl   append-only event log — input to `examine`
        *.md      human-readable summary
        *.png     execution path
    <domain>/<subdomain>/...
        governed state, written only through declared side effects
```

Store paths are declared in `STRUCTURE` artifacts and resolved through bindings. Never hardcode one.

### Where a thing is declared

| To find | Look in |
|---|---|
| what artifacts exist | `snapshot/artifact_index/index.json` |
| what a capability produces | its surface contract |
| what a workflow does | `snapshot/behavior_logic/<domain>/<WF>/` |
| which store something writes | `snapshot/store_index/index.json` |
| why an artifact was admitted | `snapshot/evidence/<domain>/evidence.json` |
| what a snapshot *is* | `snapshot/manifest.json` |

`evidence.json` is the **semantic** graph — typed, FQDN-keyed edges. Its sibling
`evidence_graph.json` is the **compile trace**, keyed by event id, with no artifact-level edges.
Reading the wrong one returns empty, not an error.

---

## Appendix C: Debugging

| Symptom | Cause | Fix |
|---|---|---|
| no binding for a capability | declared in protocol; no binding artifact | add the binding |
| payload rejected at the intent | payload violates admission rules | read the intent's schema |
| conformance check failed | an artifact violates an invariant | read the named rule and the named artifact |
| editing the snapshot has no effect | it is compiled output | change source → recompile → reassemble |
| artifact not found | wrong namespace, or outside the build scope | check the structure artifact's scope |
| unexpected routing | an outcome does not match a routing edge | compare declared outcomes to the workflow's edges |
| an inspection answer is empty | the wrong evidence file was read | read `evidence.json`, not `evidence_graph.json` |
| a transformation run fails before p0 | the snapshot is not the pinned baseline | re-pin deliberately, or point at the right snapshot |
| identity changed without a source change | something entered the build that nobody declared | find it — this is the check working |

**Compile-time vs run-time.** An invariant violation or a malformed artifact is caught at compile
time and cannot enter a snapshot. A missing binding surfaces at boot; a rejected payload at the
intent; an unroutable outcome mid-traversal. Anything caught at run time that *could* have been
caught at compile time is a gap in the governance surface, not merely a bug.

---

## Appendix D: Extending a platform

### Add a capability transform
1. Implement a pure function in `software_governance/capability_transforms/implementation/`.
2. Declare `CT_<NAME>_V0`, naming its implementation in the `## Machine` block.
3. Reference it from a capability contract's step.
4. Recompile and reassemble.

### Add a capability side effect
This is a **governance act**, not a convenience. It changes what every platform can do.
1. Establish that the need is neutral — a mechanism the substrate lacks, not one domain's problem.
2. Implement it, declare `CS_<NAME>_V0`, and amend `INVARIANT_CS_SURFACE_CLOSED_V1` to name it.
3. Recompile the surface; every composition is now checked against the new closure.

### Add a domain
1. Create the domain's `registry/` of protocol artifacts and its `STRUCTURE` build declaration.
2. Compile it against the governance surface, then reassemble.
3. Nothing in the compiler, assembler, runtime or transport changes. **A domain that requires a tool
   edit is not self-describing** — fix the declaration, not the tool.

### Add an inspection operation
1. Author the boundary contracts declaring the identity, handler kind, input contract, presentation
   and implementation reference.
2. Register the implementation in the inspector's static table.
3. Recompile and reassemble. The CLI gains the command from the catalog — no client code changes.

### Add a governed boundary operation
1. Author the ingress and egress contracts in the *domain that owns the operation*, not in transport.
2. Enumerate every field of the output contract explicitly.
3. Recompile and reassemble. No file in `protocol_transport` changes.

---

## Manual evolution rule

**New content must improve architectural cognition density.** If something is already obvious from
source or from a compiled artifact, it does not belong here. If a section does not improve decision
quality or restoration speed, it does not belong here.

Two grades of claim may harden into doctrine: a **validated finding** (reproduced, mechanism
understood, survives adversarial check) and a **candidate invariant** (holds so far, not yet
reproduced — flagged provisional). Hypotheses are tracked, never stated as doctrine. A trait of a
particular tool, model or harness is a benchmark fact and never governance. A claim is promoted by
re-grading, never by repetition.

**Defect discovery in a governed system is a coverage property, not a maturity one.** Defects live on
paths that have never been executed. They are not waiting to be outgrown; they are waiting to be
walked into.

When architecture and convenience conflict, prefer: explicitness over convenience · governance over
heuristics · determinism over flexibility · compile-time refusal over run-time repair.