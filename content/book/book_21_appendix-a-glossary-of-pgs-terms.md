---
title: Appendix A — Glossary of PGS Terms
date: '2026-06-04'
draft: false
weight: 21
slug: appendix-a-glossary-of-pgs-terms
---

This glossary defines the operational vocabulary of Protocol-Governed Systems. PGS vocabulary is structural, not descriptive --- each term corresponds to a specific architectural role. Understanding these terms is understanding the system.

## Core Paradigm

**Protocol-Governed System (PGS)**\
A computational model in which system behavior is defined as compiled governance artifacts rather than as an emergent property of implementation code. All permissible behavior is declared before execution; only declared behavior is executable.

**Protocol Artifact**\
A declarative unit of behavior (Intent, Workflow, Capability Contract, etc.) that is authored, validated against governance invariants, and compiled into an execution structure. Artifacts are the law of the system --- they define what is permitted, not what is implemented.

**Behavioral Admissibility**\
The property that a behavior has been declared, validated, and compiled into the execution graph. Only admissible behaviors can execute. Admissibility is determined at compile time, not at runtime.

**Correct-by-Construction**\
The property that execution correctness is established structurally, at compile time, rather than verified post-hoc. If the compiler accepts an artifact, the execution graph it produces cannot contain unauthorized paths.

**Semantic-Agnostic Execution**\
The property of the runtime engine: it traverses the compiled execution graph and dispatches capabilities without interpreting the meaning of domain operations. The engine does not know what "register an actor" means --- it knows only structural prefixes (`CC_`, `CT_`, `CS_`) and declared routing outcomes.

**Generation-Governance Impedance Mismatch**\
The structural gap that arises when implementation velocity ($V_{g}$) exceeds governance velocity ($V_{gov}$). Conventional systems assume $V_{g} \leq V_{gov}$; AI-speed code generation makes $V_{g} \gg V_{gov}$. PGS resolves this by making governance compile-time rather than runtime.

**Governance Dividend**\
The long-term reduction in system complexity and cost-of-change achieved by constitutional constraint. As PGS systems grow, the marginal cost of adding new domains decreases. Conventional systems exhibit the opposite trend.

## The Lifecycle Axis (How Behavior is Constructed)

**Tooling Layer (L-TO)**\
The lifecycle phase in which governance artifacts are declared by domain authors. The tooling layer produces the source-of-truth protocol declarations that all downstream phases consume.

**Governance Layer (L-GO)**\
The lifecycle phase in which declared artifacts are validated against constitutional invariants. An artifact passes governance if and only if it satisfies all invariants. Governance determines admissibility --- not runtime behavior.

**Compiler Layer (L-CP)**\
The lifecycle phase that transforms validated governance artifacts into a deterministic execution graph ($\mathcal{G}$). The compiler is a first-class architectural primitive --- it constructs the reachability structure of the system. If a path is not constructed by the compiler, it cannot be traversed.

**Execution Layer (L-EX)**\
The lifecycle phase in which the compiled execution graph is traversed. The runtime is domain-agnostic; all domain logic is encoded in the graph, not in the engine.

**Structure Layer (L-ST)**\
The lifecycle phase responsible for canonical identity and FQDN resolution. Every artifact has a unique, stable identity independent of its physical location.

**Builder**\
The tooling implementation of the Compiler Layer. In the PGS reference implementation, the builder is `pgs_compiler`'s compilation pipeline. It discovers artifacts, validates them, materializes compiled output into `protocol_snapshot/`, and produces a build manifest.

**Protocol Snapshot**\
The compiled, immutable output of the builder --- a closed set of execution-ready artifacts. The runtime reads only the snapshot. The snapshot is read-only at runtime.

## The Execution Axis (What Behavior Does)

**Transport Ingress (TI)**\
Normalizes external input into canonical internal protocol representation. External callers do not send raw data to the execution engine --- they send it through TI, which validates and transforms it.

**Actor Context (AC_)**\
The authority principal of an execution. An AC_ artifact binds identity, role, and permissions to an execution session. Code does not inherit authority from its environment --- authority is established by AC_ declarations.

**Intent (IN_)**\
The admission gate for a workflow. An IN_ artifact declares the admission rules: what payload shape is required, what actor context is permitted, and what workflow is triggered. If the intent is not satisfied, the workflow does not execute.

**Workflow (WF_)**\
The execution graph definition. A WF_ artifact declares the directed acyclic graph (DAG) of Capability Contracts: which nodes execute, in what order, and how outcomes route to subsequent nodes. The workflow is compiled into $\mathcal{G}$ by the builder.

**Capability Contract (CC_)**\
A named node in the execution graph. A CC_ artifact declares the node's input bindings (JSONPath expressions), its pipeline of CT_ and CS_ steps, and its outcome routing table. CC_ is the interface --- it does not implement behavior; it orchestrates declared capabilities.

**Capability Transform (CT_)**\
A pure computational unit --- deterministic, side-effect free. Given identical inputs, CT_ always produces identical outputs. CT_ atoms cannot write to storage, call external APIs, or mutate state. CT_ is resolved to its implementation via an RB_ binding.

**Capability Side Effect (CS_)**\
A controlled interface to external state. CS_ performs bounded mutations (registry writes, event appends, JSON updates, email delivery, cross-workflow invocation). Every CS_ step is explicitly declared in a CC_ pipeline, bound via RB_, and recorded in the execution trace.

**Event (EV_)**\
The observability and control plane. Events contribute to the immutable execution trace, enable cross-boundary signaling, and participate in governance decisions (admission control, execution halt). Observability is an active governance mechanism.

**Transport Egress (TE)**\
Projects internal execution results into the representation required by external callers. TE is the output boundary --- internal state is not directly accessible outside the TE boundary.

**Runtime Binding (RB_)**\
An orthogonal resolution artifact that maps both CT_ and CS_ capability codes to their concrete implementations. RB_ is not an execution concern --- it does not define behavior or orchestration. It enables the runtime to dispatch capabilities without knowing their implementations. The same binding mechanism applies symmetrically to all capability types. RB_ provides execution mapping, not authority.

**Admissibility Graph (**$\mathcal{G}$**)**\
The deterministic, compiled set of all authorized execution paths. $\mathcal{G = (}V,E)$ where $V$ is the set of authorized nodes and $E$ is the set of authorized transitions. A path that does not exist in $\mathcal{G}$ cannot be traversed --- by construction, not by policy enforcement.

**Execution Trace (**$T_{\text{evidence}}$**)**\
The immutable, append-only record of an execution. The trace captures every node transition, every capability invocation, every input and output, every outcome. The trace is the ground truth of what happened --- it proves that execution followed an admissible path. Audit reads the trace, not the code.

## The Capability Surface

**CT Atom**\
The smallest unit of pure computation --- a single-purpose, side-effect-free function. Atoms compose into molecules.

**CT Molecule**\
A declarative composition of CT atoms with explicit dataflow between steps. Molecules are compiled into CT-IR (Intermediate Representation) for uniform execution by the CT executor.

**CT-IR (Intermediate Representation)**\
The normalized execution format for capability transforms. The CT executor consumes CT-IR --- it does not distinguish atoms from molecules at execution time.

**CS Runtime Type**\
The concrete storage or interaction class that fulfills a CS_ capability. The current runtime types are: `RegistryRuntime`, `MutableJsonRuntime`, `AppendOnlyJsonlRuntime`, `SendEmailRuntime`, `WorkflowGatewayRuntime`, `NameRegistryRuntime`. The set is closed --- extending it requires a runtime engine change.

## Identity and Structure

**FQDN (Fully Qualified Domain Name)**\
The canonical identity format for all PGS artifacts: `domain::ARTIFACT_CODE`. Examples: `blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0`, `capability_transforms::CT_PURE_GENERATE_ID_V0`. FQDN is the stable identifier --- artifact files, artifact references, and runtime dispatch all use FQDN.

**FQDN Tree**\
The structural registry of all domains and their artifact namespaces, declared in `STRUCTURE_DISCOVERY_V0`. The builder discovers artifacts by traversing the FQDN tree. Adding a domain requires registering it in the tree (Act I of domain construction).

**Version**\
The `_V0`, `_V1`, etc. suffix on all artifact codes. Versions are immutable --- an artifact cannot be modified in place. Changes require a new version. Multiple versions coexist; references are always to a specific version. There is no "latest."

## Security Properties

**Security Inversion Principle**\
Security is achieved by restricting the space of constructible behaviors, not by constraining execution of arbitrary behavior. Unauthorized behavior is not prevented at runtime --- it is never constructed.

**Ambient Authority**\
Authority derived implicitly from an execution environment (e.g., a process running with database write access). PGS eliminates ambient authority: code has no inherent authority; all authority originates from $(AC,IN,WF,CC)$ declarations.

**Bounded Mutation Surface**\
The enumerable set of all state-change operations in the system: $|\text{CS_}| + |\text{AC_}| + |\text{RB_}|$. No mutation can occur outside this surface by construction.

**Vocabulary Closure Invariant**\
No behavior may occur outside the declared concern vocabulary ($V$). All behavior must originate from protocol artifacts and be routable through known execution concerns. Behavior not expressible in $V$ cannot be compiled and therefore cannot execute.

**Implementation Blindness**\
The property that implementations cannot access each other or alter execution structure. All interaction between capabilities is mediated through protocol-defined pathways. A CT atom cannot call a CS operation directly.

**Structural Purity**\
The guarantee that CT_ transforms are free of side effects --- enforced structurally, not by language semantics. Even an impure implementation inside a CT_ atom cannot produce side effects observable outside its declared outputs.

**Referential Persistence of Governance**\
Governance survives the temporal decay of implementation. Even if the code responsible for an action is regenerated, deleted, or replaced, the governance relationship --- recorded in the execution trace and declared in the protocol artifacts --- remains persistent, enforceable, and auditable.

## Domain Construction

**Domain**\
A coherent set of protocol artifacts (workflows, capability contracts, actors, events, intents) that express a bounded business or technical concern. Domains compose through federation, not modification.

**Act 0 (Domain Specification)**\
The pre-construction architectural design phase. Produces the domain specification: business thesis, actor inventory, workflow inventory, capability surface, invariants, and success criteria. All downstream acts implement what Act 0 specifies.

**Seven Architectural Acts**\
The construction method for a PGS domain, as described in Chapter 13: - Act I: Register the domain namespace - Act II: Author governance artifacts\
- Act III: Validate against invariants - Act IV: Compile the protocol snapshot - Act V: Wire capability implementations via RB_ bindings - Act VI: Execute with test payloads - Act VII: Verify traces and lock down

**Compositional Isolation**\
The property that adding a new domain does not modify any prior domain's artifacts, engine code, or test outcomes. New domains are consumers of the platform, not contaminants of it.

**Declarative Federation**\
The mechanism by which multiple domains coexist without coupling: each domain registers in the FQDN tree, the builder discovers all domains at compilation time, and execution routes by FQDN without domain-specific logic.
