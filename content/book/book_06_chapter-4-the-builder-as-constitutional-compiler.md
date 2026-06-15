---
title: Chapter 4 — The Builder as Constitutional Compiler
date: '2026-02-19'
draft: false
weight: 6
slug: chapter-4-the-builder-as-constitutional-compiler
---

Chapter 3 authored governance artifacts and proved that constitutional validation rejects incomplete or invalid declarations at authoring time. The artifacts are ratified --- immutable, versioned, hash-anchored. But they are YAML embedded in markdown, organized for human readability. The execution engine does not read YAML. It loads compiled JSON.

This chapter addresses the bridge between ratification and execution: **How do ratified governance artifacts become the compiled protocol that the execution engine loads --- and what guarantees that the compilation is faithful, deterministic, and complete?**

The Builder is not a convenience tool like a bundler or minifier. It is a constitutional compiler --- a six-phase pipeline that translates behavioral law from governance representation to execution representation without adding, removing, or reinterpreting any behavioral content. The chapter introduces the FQDN tree (the build constitution that declares what exists, where it lives, and in what order it compiles), walks through the governance-to-protocol transformation side by side, and exposes a failure surface invisible to governance validation: compilation failures that emerge only when individually valid artifacts are assembled together. By the end, the reader will understand why the gap between what was authored and what executes is structurally zero.

## 4.1 --- The Engineering Objective

Chapter 3 produced ratified governance artifacts --- an intent, a workflow, three capability contracts. They passed constitutional validation. They are immutable, versioned, and hash-anchored. But they are not executable.

The governance artifacts are written in YAML, embedded in human-readable markdown files, and organized into governance registries. The execution engine does not load YAML. It does not parse markdown. It does not scan registries. It loads compiled protocol artifacts --- normalized, machine-readable JSON files in a deterministic directory structure.

Something must stand between ratification and execution. That something is the Builder.

**The Task:** Transform the ratified user registration artifacts from Chapter 3 into compiled protocol artifacts ready for the execution engine.

**The Constraint:** The Builder may not reinterpret, mutate, or extend behavioral law. It must compile deterministically or fail loudly. If a governance artifact is incomplete, the Builder does not repair it. If a reference is unresolved, the Builder does not guess. It fails.

In the application-centric approach, the distinction between authoring and execution barely exists. A developer writes code; a build tool packages it; the runtime loads the package. The build step is a mechanical convenience --- minification, bundling, dependency resolution --- with no constitutional authority. The builder can and often does silently modify what the developer wrote: injecting polyfills, rewriting imports, adding instrumentation.

A natural question arises: why not let the execution engine load YAML directly? The answer is structural. Governance artifacts are human-facing --- organized by concern, scoped to registries, embedded in markdown for readability and review. Execution must be registry-agnostic and concern-blind: it loads a normalized DAG and traverses it. Compilation removes governance-layer traversal from the runtime path entirely. The engine never opens a registry, never parses YAML, never resolves a governance path. This preserves runtime determinism and performance isolation --- the cost of structural resolution is paid once at compile time, not on every execution.

In PGS, the compilation boundary is constitutional. The Builder is a separate phase with its own failure surface. It translates law --- it does not make law. The governance layer has already determined what the system will do. The Builder determines whether that declaration can become executable protocol.

## 4.2 --- The Build Constitution: The FQDN Tree

Before the Builder can compile anything, it must know what exists, where it lives, and in what order to process it. In application-centric systems, build tools typically discover this by scanning the filesystem --- searching for files matching patterns, inferring module boundaries from directory structure, resolving dependencies at build time.

The Builder does none of this. Its first action is loading a governance artifact: the FQDN tree.

**Definition:** The FQDN tree (Fully Qualified Domain Name tree) is the authoritative declaration of every package, registry, artifact pattern, and dependency relationship in the system. It is itself a governance artifact, governed by a constitution.

**Key Properties:**

1.  **Sovereign Authority.** The FQDN tree is loaded first --- before any artifact is discovered, validated, or compiled. No build phase may execute until the tree is loaded and validated.
2.  **Explicit Build Ordering.** Each package declares a `build_order` integer. The Builder processes packages in this order. Dependencies must be forward-only: a package at order N may depend on packages at order \< N, never on packages at order \>= N.
3.  **Hash-Anchored.** The FQDN tree's content hash is recorded in the build manifest. Any change to the tree --- a new package, a reordered dependency, a modified pattern --- produces a different hash and constitutes a governance-visible change.

### Example 4.1 --- FQDN Tree Excerpt

*(The full artifact is provided in Appendix B, Example 4.1.)*

**Analysis:**

- **Build order is law.** The `governance` package builds at order 1. The `blockchain` package builds at order 4. The Builder cannot reverse this. If `blockchain` depends on `reusable`, and `reusable` builds at order 3, then `blockchain` cannot be compiled until `reusable` completes. The ordering is declared, not computed.
- **Discovery is declared.** The `artifact_patterns` section tells the Builder exactly which file patterns to match in which registry paths. `wf_*.md` discovers workflow artifacts. `CC_*.md` discovers capability contracts. The Builder does not scan the filesystem speculatively --- it looks where the FQDN tree says to look.
- **Dependencies are acyclic.** `blockchain` depends on `[governance, reusable]`. Both have lower build orders. If an author declared `depends_on: [transport]` (build order 8), the Builder would reject the FQDN tree before any artifact is discovered.

## 4.3 --- Governance Input vs. Protocol Output

The reader authored governance artifacts in Chapter 3. Now the Builder compiles them. The transformation is structural: YAML governance → JSON protocol. The content is preserved. The representation changes. The Builder adds nothing.

### Example 4.2 --- Governance Input: WF_REGISTER_USER_UNVERIFIED_V0 (YAML)

This is the artifact the reader authored in Chapter 3, now viewed as input to the Builder *(see Appendix B, Example 4.2)*.

### Example 4.3 --- Compiled Protocol Artifact: WF_REGISTER_USER_UNVERIFIED_V0 (JSON)

This is what the Builder emits --- the protocol artifact loaded by the execution engine *(see Appendix B, Example 4.3)*.

**Analysis:**

- **Structural equivalence.** Every node, every edge, every input binding in the JSON traces to a corresponding declaration in the YAML. The Builder has not invented any edges. It has not added any nodes. The behavioral surface is identical.
- **Normalization.** The compiled artifact adds a `code` field to each node --- making the node's identity explicit rather than derived from its key name. This is a structural normalization, not a behavioral addition.
- **Machine-readability.** The execution engine loads this JSON directly. No YAML parsing, no markdown extraction, no governance registry traversal at runtime. The cost of compilation is paid once; the cost of execution is minimized.

### Example 4.4 --- Compiled Capability Contract: CC_GENERATE_USER_ID_V0 (JSON)

*(The full artifact is provided in Appendix B, Example 4.4.)*

**Analysis:**

- **The compilation surface is richer for capability contracts.** The compiled artifact includes resolved input/output schemas, a `result_status_contract` with failure-handling semantics (`on_input_failure`), and per-step result routing (`on_ct_result`, `on_result`). These are compiled from the governance declarations --- they are structural elaborations, not behavioral additions.
- **Pipeline execution semantics are frozen.** The `on_result` block declares that SUCCESS continues the pipeline and VIOLATION exits. The engine does not decide this at runtime --- it reads the compiled contract. The decision was made at authoring time, compiled at build time, and enforced at execution time.
- **The CT/CS boundary is preserved.** `CT_PURE_GENERATE_ID_V0` is still a CT_ step. The compilation has not changed its classification. The constitutional boundary between pure computation and world interaction survives compilation intact.

## 4.4 --- The Builder Pipeline

The Builder does not perform a single compilation pass. It executes a phased pipeline, where each phase has constitutional authority over a specific concern and each phase must complete before the next begins.

### The Six Phases

  -----------------------------------------------------------------------------------------------------------------------------------------------------------
  Phase         Name                   Input                                         Output                                Halts On
  ------------- ---------------------- --------------------------------------------- ------------------------------------- ----------------------------------
  0             FQDN Load              FQDN tree file                                Validated package hierarchy           Malformed tree

  1             Discovery              FQDN tree + registries                        Enumerated artifact list              Fatal discovery error

  2             Validation             Discovered artifacts + schemas + vocabulary   Validated artifact set                Schema or vocabulary violation

  3             Conformance            Validated artifacts                           Test descriptors                      Test generation error

  4             Materialization        Validated artifacts                           JSON protocol artifacts               Serialization or path failure

  5             Molecule Compilation   Materialized artifacts                        CT-IR (intermediate representation)   Invalid molecule or missing atom

  6             Manifest               All phase outputs                             Build manifest with hashes            Manifest generation failure
  -----------------------------------------------------------------------------------------------------------------------------------------------------------

**Phase ordering is constitutional.** The FQDN tree must load before discovery. Discovery must complete before validation. Validation must pass before materialization. The pipeline is strictly sequential --- no phase may execute out of order. This is not an optimization choice; it is a constitutional constraint that guarantees each phase operates on verified inputs from the previous phase.

**Halt semantics.** If any phase produces a fatal or error-level failure, the pipeline halts. No subsequent phase executes. The Builder does not "compile what it can" --- it succeeds completely or fails completely. Partial compilation is not a valid state.

### What Each Phase Proves

- **Phase 0** proves the build constitution exists and is well-formed.
- **Phase 1** proves every artifact the FQDN tree declares actually exists on disk, and no undeclared artifacts are included.
- **Phase 2** proves every discovered artifact conforms to its schema and uses only registered vocabulary.
- **Phase 3** proves the artifact set is mechanically testable --- the system can derive test descriptors from governance declarations without author input. If conformance tests cannot be generated, the artifact set is structurally incomplete.
- **Phase 4** proves the governance declarations can be materialized into executable protocol without loss or invention.
- **Phase 5** proves composite transforms (molecules) can be decomposed into valid atom sequences. Molecule compilation reduces multi-step transforms into atomic instruction sequences (CT-IR), preserving execution determinism while enabling composition at the authoring level.
- **Phase 6** proves the entire build is content-addressable --- any future build from identical inputs will produce an identical manifest hash.

## 4.5 --- Validation and Failure Surface

Chapter 3 showed governance validation --- the five checks that an artifact must pass before ratification. This section shows a different failure surface: compilation failures. These are structural violations that governance validation does not and cannot catch, because they emerge only when artifacts are compiled together.

### Compilation Checks (Beyond Governance)

  --------------------------------------------------------------------------------------------------------------------
  Step           Check                   What It Catches
  -------------- ----------------------- -----------------------------------------------------------------------------
  1              FQDN Resolution         Package not declared in tree --- artifact exists but has no build authority

  2              Dependency Closure      Artifact references a code from a package outside its declared dependencies

  3              Build Order Integrity   Forward dependency --- package at order N depends on package at order \> N

  4              Pattern Match           Artifact file in a registry path doesn't match declared file patterns

  5              Deterministic Hash      Same governance input produces different compiled output between runs
  --------------------------------------------------------------------------------------------------------------------

**Why governance cannot catch these.** Governance validates individual artifacts against their constitutional schemas. It verifies that CC_GENERATE_USER_ID_V0 has a valid pipeline declaration, valid bindings, and a valid result status contract. But governance does not know which packages are declared in the FQDN tree. It does not know the build order. It does not know whether a cross-package reference falls within the dependency closure. These are compilation concerns --- they emerge when individually valid artifacts are assembled into a protocol.

### A Compilation Failure

Suppose the `blockchain` package's workflow references a capability transform from a package called `experimental`, which is not declared in the FQDN tree *(see Appendix B, Example 4.5)*.

The governance layer does not reject this. The artifact schema is valid. The pipeline declaration is well-formed. The prefix `CT_` is a registered vocabulary term.

The Builder rejects it:

    COMPILATION FAILURE
      Phase:      Discovery
      Artifact:   CC_GENERATE_USER_ID_V0
      Package:    blockchain
      Check:      Dependency Closure
      Rule:       Pipeline references must resolve to artifacts within the
                  declared dependency closure
      Detail:     CT_EXPERIMENTAL_HASH_V0 is not discoverable in packages
                  [governance, reusable] (declared dependencies of blockchain)
      Resolution: Either declare 'experimental' as a dependency of 'blockchain'
                  in the FQDN tree, or use a CT_ from an existing dependency

**What this proves:** The Builder enforces constraints that governance cannot. Governance validates the individual artifact's structure. The Builder validates the artifact's relationship to the system. Both are constitutional. Both are deterministic. Both fail loudly. Neither repairs silently.

### The Contrast

  --------------------------------------------------------------------
           Application-Centric Build   PGS Builder
  -------- --------------------------- -------------------------------
  Step 1   Scan filesystem             Load constitution (FQDN tree)

  Step 2   Infer modules               Discover declared artifacts

  Step 3   Inject defaults             Validate deterministically

  Step 4   Package code                Compile or halt
  --------------------------------------------------------------------

## 4.6 --- Structural Insight (Doctrine Moment)

The reader has now seen governance artifacts compiled into protocol artifacts through a six-phase pipeline. The compilation preserved behavioral content and changed only representation. The failure surface caught violations invisible to governance validation.

This is Chapter 2's **Property 3** made concrete: *The compilation boundary hardens the WHAT/HOW separation.* Governance declares WHAT the system does --- in human-readable YAML, organized by concern. The Builder compiles this into HOW the system executes --- in machine-readable JSON, organized by execution type. The two representations are structurally equivalent, but the transformation is irreversible in authority: the execution engine loads only the compiled artifact. It never reads governance YAML. The compilation boundary is a one-way gate.

**Invariant I-C1 --- Deterministic Compilation:** Identical ratified governance artifacts always produce identical compiled protocol artifacts. The Builder is a pure function. Given the same FQDN tree and the same governance registries, the Builder produces the same protocol artifacts, the same manifest, and the same content hash. This is not an aspiration --- it is a structural consequence of the pipeline design. There are no timestamps in compiled artifacts. There is no environment-dependent behavior. There is no randomness.

**Structural impossibility:** The Builder cannot inject new behavior or repair incomplete artifacts. If a workflow node has an undeclared outcome edge, the Builder does not add a default. If a capability contract references an atom that does not exist, the Builder does not substitute an alternative. The Builder's authority is translation --- structural transformation from one representation to another. It has no legislative authority. It cannot create law. It can only compile it. Equally, the Builder cannot inspect runtime state. It compiles structure, not behavior. It has no access to execution payloads, runtime bindings, or trace history. Compilation is entirely static.

**Authority chain:**

    Governance (Law) → Builder (Translation) → Execution (Enforcement)

Governance defines behavioral law (Chapter 3). The Builder translates law into executable form (this chapter). The Execution engine enforces law at runtime (Chapter 5). Each layer has exactly one responsibility. No layer performs another layer's function. This separation is not organizational --- it is constitutional.

Traditional software relies on test-driven confidence: unit tests, integration tests, canaries, and observability after the fact. These techniques tell you something probably worked. The Builder offers something stronger: compile-time proof that the governance declarations are structurally complete, dependency-closed, and deterministically reproducible --- before a single line of execution occurs.

## 4.7 --- Solved Problems

### Problem 4.1 --- Silent Graph Mutation

**Scenario:** A build tool encounters a workflow with a missing error-handling edge and silently adds a default fallback.

**Application-Centric Approach:** The build tool detects the incomplete graph and auto-inserts a default error handler --- a catch-all retry, a fallback to a generic error page, or a silent swallow of the exception. The developer never sees the addition. The deployed system contains behavior that was never authored.

**PGS Approach:**

1.  The workflow artifact is discovered and validated in Phase 2
2.  If the workflow has incomplete outcome edges, governance validation rejects it (Chapter 3)
3.  If the workflow passes governance but references a non-existent artifact, the Builder rejects it in Phase 1 (Discovery) or Phase 4 (Materialization)
4.  The Builder cannot add edges. It cannot insert default handlers. It compiles what is declared or it fails

**Eliminated pathology:** Silent repair. The gap between what was authored and what executes is zero, because the Builder is a faithful translator with no editorial discretion.

### Problem 4.2 --- Cross-Package Leakage

**Scenario:** A capability contract in the `blockchain` package imports a utility from a shared `utils` package that is not declared as a dependency.

**Application-Centric Approach:** The import resolution mechanism (Node.js, Python, Java classloader) silently resolves the import. The dependency is real but invisible. When `utils` changes, `blockchain` breaks --- and no one knows why, because the dependency was never declared.

**PGS Approach:**

1.  The FQDN tree declares `blockchain` depends on `[governance, reusable]`
2.  The `utils` package is not in the dependency list
3.  The Builder's discovery phase enumerates artifacts only within declared dependencies
4.  A reference to an artifact in `utils` is unresolvable --- compilation fails at dependency closure check
5.  The developer must either add `utils` to the FQDN tree's dependency list for `blockchain`, or use an artifact from an already-declared dependency

**Eliminated pathology:** Namespace drift. Cross-package dependencies are declared in the FQDN tree and enforced by the Builder. Implicit imports cannot exist because the Builder does not scan --- it resolves within declared scope only.

### Problem 4.3 --- Non-Deterministic Builds

**Scenario:** Two developers compile the same governance artifacts and get different protocol artifacts.

**Application-Centric Approach:** Build artifacts differ by environment: timestamps embedded in output, platform-specific file ordering, locale-dependent string comparisons, environment variables that influence bundler behavior. Debugging production issues becomes forensic archaeology.

**PGS Approach:**

1.  The FQDN tree declares package ordering explicitly --- `build_order: 1, 2, 3, 4...`
2.  Discovery patterns are declared --- `wf_*.md`, `CC_*.md` --- not filesystem-dependent globs
3.  Compiled artifacts contain no timestamps, no environment references, no platform-dependent values
4.  The build manifest records the FQDN tree hash --- if the tree hasn't changed, the manifest hash is reproducible
5.  Invariant I-C1 guarantees: identical governance inputs → identical protocol outputs

**Eliminated pathology:** Build inconsistency (compilation drift). The build is a deterministic function. The same inputs produce the same outputs on any machine, at any time.

## 4.8 --- Generated Output: The Compiled Protocol Bundle

The artifacts are authored (Chapter 3). They are validated and ratified (Chapter 3). Now they are compiled (this chapter). The Builder has transformed governance YAML into protocol JSON through a six-phase pipeline. The output is a compiled protocol bundle.

> **[DIAGRAM 5] --- Builder Pipeline: Governance to Protocol**

    FQDN Tree (STRUCTURE_DISCOVERY_V0)
            ↓
    Phase 0: Load & Validate Tree
            ↓
    Phase 1: Discover Artifacts
      governance/registry/ → [constitutions, schemas]
      reusable/governance/registry/ → [CT_, CS_]
      blockchain/governance/registry/identity/ → [IN_, WF_, CC_, EV_]
            ↓
    Phase 2: Validate (Schema + Vocabulary)
            ↓
    Phase 3: Generate Conformance Tests
            ↓
    Phase 4: Materialize → protocol/artifacts/
      workflows/wf_register_user_unverified_v0.json
      capability_contracts/CC_GENERATE_USER_ID_V0.json
      capability_contracts/CC_REGISTER_USER_KYC_V0.json
      capability_contracts/CC_APPEND_USER_EVENT_V0.json
            ↓
    Phase 5: Compile Molecules → CT-IR
            ↓
    Phase 6: Generate Manifest (content hash)
            ↓
    BUILD MANIFEST
      fqdn_tree_hash: sha256:a3f7...
      packages: [governance(1), execution(2), reusable(3), blockchain(4)]
      artifacts: 4 materialized
      status: SUCCESS

**What the output proves:**

- **Traceability.** Every compiled JSON file in `protocol/artifacts/` traces to a governance YAML file in `governance/registry/`. The manifest records what was compiled, from which packages, in what order.
- **Completeness.** The Builder materialized all artifacts discovered in the FQDN tree's declared registries. No artifact was skipped. No artifact was invented.
- **Determinism.** The manifest hash anchors the entire build. Run the Builder again with the same FQDN tree and the same governance artifacts, and the manifest hash is identical. The build is reproducible. The manifest becomes the root of trace integrity in Chapter 9 --- every execution trace references the manifest hash of the build that produced the protocol artifacts it ran.
- **Separation.** The governance registries (YAML .md files) remain untouched. The protocol artifacts (JSON files) are generated alongside them in `protocol/artifacts/`. The two representations coexist but serve different consumers: governance is for authors and auditors; protocol is for the execution engine.

**Structural impossibility:** The Builder cannot create an artifact that does not correspond to a governance declaration. Every line of compiled JSON traces to a line of governance YAML. The Builder cannot add a node to a workflow, extend a pipeline, or modify a result status contract. It is constitutionally incapable of invention.

You authored YAML. The Builder compiled JSON. The two are structurally equivalent. The execution engine will load the JSON in Chapter 5.

## 4.9 --- Current Compiler Architecture Note

The six-phase pipeline described in this chapter (Discover → Parse → Validate → Assert → Materialize → Snapshot) reflects the conceptual structure that remains accurate. The current compiler implementation names these phases as nine explicit stages:

  ---------------------------------------------------------------------------------------------------------------------------------
  Stage             Name                  Corresponds To
  ----------------- --------------------- -----------------------------------------------------------------------------------------
  S1                EXTRACT               Discover + Parse

  S2                CANONICALIZE          Normalization + edge typing

  S3                SEMANTIC_ADDRESSING   Address space closure

  S4                GOVERN                Assert (all invariants + conformance assertions)

  S5                CONSTRUCT             Materialize (IR build + topology seal)

  S6                PROJECT               Visualization projection

  S7                MATERIALIZE           Snapshot write + evidence graph

  S8                VERIFY                Post-write integrity verification + snapshot admission

  S9                ATTEST                Cryptographic attestation computed and written for each structure and the full snapshot
  ---------------------------------------------------------------------------------------------------------------------------------

The **STRUCTURE_ artifact** is the current compiler's build constitution --- analogous to the FQDN tree described in this chapter. It declares what exists, which registries contribute, and in what scope to compile.

**Two Phase Types.** Compilation runs in two phase types:

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Phase Type                    Name                          Semantics
  ----------------------------- ----------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------
  **Phase Type A**              Per-Structure Local           S1--S9 within a single structure; self-contained semantic closure

  **Phase Type B**              Cross-Structure Aggregation   Consumes declared output surfaces from multiple Phase Type A builds; produces federated governance products (vocabulary, transport, authority)
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Phase Type B is governed by an aggregation STRUCTURE_ artifact with an `aggregation_type` field. It must run after all contributing Phase Type A builds complete. Phase Type B may never introduce execution node types or alter workflow behavior --- it synthesizes governance products only.

**S4 GOVERN: Three categories of enforcement (v0.4.0).** The GOVERN stage runs all registered assertion handlers. As of v0.4.0, three assertion families run at this stage --- each is a hard fail on violation:

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Assertion                                                               Scope                What It Enforces
  ----------------------------------------------------------------------- -------------------- --------------------------------------------------------------------------------------------------------------------------------------------
  **Constitutional invariants**                                           All artifacts        Schema closure, FQDN identity, vocabulary closure, topology completeness

  **CC Storage Op Conformance** (`ASSERT_CC_STORAGE_OP_CONFORMANCE_V0`)   All CC_ artifacts   Every storage operation declared in a CC_ must be bounded, enumerated, and expressible within the declared CS_ surface

  **RB Policy Conformance** (`ASSERT_RB_BINDING_POLICY_CONFORMANCE_V0`)   All RB_ artifacts   Every runtime binding must declare a policy-compliant mapping; undeclared or policy-violating bindings are rejected before materialization
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**FQDN 100% compliance** is enforced as a hard invariant in S4. Every artifact reference anywhere in the compiled surface must use the full `domain::ARTIFACT_CODE_Vn` form. Short names --- even in comments or metadata fields --- produce a GOVERN-stage failure. There are no warnings; the pipeline halts.

**Snapshot Admission Control (S8 gate).** After S7 writes the snapshot and evidence graph to disk, S8 runs `assert_snapshot_valid()` before allowing S9 to attest. This gate verifies: - All declared artifacts are present on disk and non-empty - Evidence graph integrity hash checks out - No unexpected files appear in snapshot directories - The snapshot is structurally complete for the declared structure scope

If `assert_snapshot_valid()` fails, S9 does not run and the snapshot is never attested --- the runtime will refuse to load an unattested snapshot. This gate is the final constitutional seal between compilation and attestation.

The **PIR (Protocol Intermediate Representation)** is the internal typed structure produced by S1. All subsequent stages operate on PIR, not raw YAML. The PIR is never exposed outside the compiler.

## 4.10 --- The Compiler Evidence Graph

The current compiler emits a second governed artifact during S7: `evidence_graph.json`. This is the compiler's own observability record --- the compilation equivalent of the execution trace described in Chapter 9.

**Why it exists:** The compiler performs hundreds of semantic operations across nine stages. Without a structured record of that work, the only way to answer "why was this artifact produced this way?" is to re-run the compiler with debug flags. The evidence graph makes that record permanent, inspectable, and consumer-accessible without compiler re-execution.

**What it contains:**

Every compiler trace event (S1--S7) becomes a node in the graph:

    event_id  stage          operation             family        subject_fqdn
    1         S1_EXTRACT     discovery_complete    DISCOVERY     blockchain
    2         S1_EXTRACT     node_created          DISCOVERY     blockchain::CC_GENERATE_ACTOR_ID_V0
    3         S1_EXTRACT     node_created          DISCOVERY     blockchain::CC_REGISTER_ACTOR_KYC_V0
    ...

Edges are typed and directed:

  -----------------------------------------------------------------------------------------------------------------------------
  Edge Kind                               Meaning
  --------------------------------------- -------------------------------------------------------------------------------------
  `CAUSALITY`                             Parent event caused/gated child event (e.g., `discovery_complete` → `node_created`)

  `STAGE_SEQUENCE`                        Last event of stage N → first event of stage N+1
  -----------------------------------------------------------------------------------------------------------------------------

The graph is sealed with a SHA-256 integrity hash covering the core content (events, edges, families, counts). S8 verifies it.

**The consumer contract:**

The `visualization/consumers/` package is the only sanctioned interface between `evidence_graph.json` and all downstream consumers:

    load_evidence_graph(path)  →  EvidenceQuery
    EvidenceQuery              →  TraceEventDTO, EvidenceEdgeDTO
    EvidenceProjection         →  StageView, provenance, construction summary

Consumers --- visualization, AI tooling, debugging, replay --- never import from the compiler. The JSON schema is the contract. This means the compiler can be replaced, refactored, or versioned independently of every consumer.

**Evidence Semantics Doctrine (the formal guarantees):**

The full doctrine is in the companion paper `pgs_compiler_conceptual_model_v0.md`. The critical guarantees:

- Causality is inferred from two patterns: `discovery_complete` → `node_created` (S1), and IR build events → `construction_complete` (S5)
- Stage sequencing produces exactly 7 STAGE_SEQUENCE edges (S1→S7); deterministic
- The evidence graph covers S1--S7 only; S8's `verification_complete` is absent by design
- Identical source artifacts always produce an identical evidence graph
- The file is self-contained --- no compiler state needed to read it

**Structural parallel to the execution trace:**

  ---------------------------------------------------------------------------------------------------------
                          Execution Trace                        Compiler Evidence Graph
  ----------------------- -------------------------------------- ------------------------------------------
  Produced by             Runtime (S8+ equivalent)               Compiler (S7)

  Records                 Workflow execution events              Compilation events

  Integrity               Hash chain (ADVANCED policy)           SHA-256 over core content (S8 Check 7)

  Consumer API            Trace Examiner                         `EvidenceQuery` / `EvidenceProjection`

  Contract                `SCHEMA_TRACE_EVENT_V0`                `evidence_graph.json` schema

  Sovereignty             Append-only; immutable post-emission   READ-ONLY post-build; never edit by hand
  ---------------------------------------------------------------------------------------------------------

Both artifacts embody the same principle: **observability is a governed constitutional obligation, not optional instrumentation**.

## 4.11 --- Boundary and Forward Pointer

This chapter proved that ratified governance artifacts are compiled deterministically into executable protocol artifacts through a constitutionally governed pipeline.

**What this chapter did not cover:**

- Runtime execution --- how the engine traverses the compiled DAG (Chapter 5)
- Runtime state transitions --- how the execution payload evolves step by step (Chapter 5)
- Runtime binding resolution --- how abstract codes (CT_PURE_GENERATE_ID_V0) map to concrete implementations (Chapter 5)
- Trace emission --- what the engine records during execution (Chapter 9)
- Capability transform internals --- how CT_ steps compute their results (Chapter 6)
- Capability side-effect internals --- how CS_ steps interact with the world (Chapter 7)
- Compiler evidence graph querying --- the consumer API for inspecting compilation semantics (`pgs_compiler_conceptual_model_v0.md`)

**What comes next:** The protocol artifacts are compiled. They sit in `protocol_snapshot/artifacts/`, waiting. Chapter 5 picks them up. The execution engine loads the compiled DAG, resolves runtime bindings, and traverses the graph node by node. The reader will see the same user registration workflow --- authored in Chapter 3, compiled in Chapter 4 --- execute for the first time.

We are crossing from the Governance/Execution boundary into the Execution layer.

## 4.12 --- Review Questions

1.  **Why is compilation a separate constitutional phase from governance validation?**

- *Governance validates individual artifacts against their schemas --- structural conformance. Compilation validates relationships between artifacts --- dependency closure, build ordering, cross-package resolution. An artifact can pass governance validation but fail compilation if it references an artifact outside its declared dependency scope.*

2.  **What happens if a workflow references a CC_ from a package not declared in the FQDN tree?**

- *The Builder fails at the dependency closure check. The referenced capability contract is not discoverable within the workflow's package dependencies. The Builder cannot resolve the reference and halts compilation.*

3.  **Can the Builder add missing edges to an incomplete workflow? Why not?**

- *No. The Builder's authority is translation, not legislation. It compiles what is declared. Adding an edge would constitute creating behavioral law --- a function reserved for the Governance layer. The Builder must fail, and the author must fix the governance artifact.*

4.  **True or False: The compiled JSON artifact may contain fields not present in the governance YAML.**

- *True --- but only structural fields, not behavioral ones. The compiled artifact adds normalization fields (e.g.,* `code` *on each node,* `on_result` *routing) that are derived from the governance declarations. These are structural elaborations, not behavioral additions. No new edges, nodes, or outcomes appear in the compiled artifact that were not declared in the governance YAML.*

5.  **How does the FQDN tree prevent non-deterministic builds?**

- *The FQDN tree declares package ordering (build_order), registry locations, artifact patterns, and dependency relationships explicitly. The Builder uses these declarations --- not filesystem scanning --- to discover and order artifacts. Since the inputs are deterministic and the pipeline is pure, the outputs are deterministic (Invariant I-C1).*

6.  **What is the structural difference between a governance validation failure (Chapter 3) and a compilation failure (Chapter 4)?**

- *A governance validation failure rejects a single artifact for violating its schema --- a missing field, an unregistered prefix, a broken reference within the artifact. A compilation failure rejects an artifact (or the entire build) for violating system-level constraints --- a cross-package dependency outside the FQDN closure, a build-order violation, or a discovery mismatch. Governance validates the artifact. Compilation validates the artifact's place in the system.*

7.  **Why must the FQDN tree be loaded before any other build phase?**

- *The FQDN tree defines what packages exist, where their registries are, what artifact patterns to match, and in what order to process them. Every subsequent phase --- discovery, validation, materialization --- depends on this information. Without the tree, the Builder does not know what to compile. Loading it first is constitutional, not conventional.*
