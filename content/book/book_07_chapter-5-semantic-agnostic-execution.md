---
title: Chapter 5 — Semantic-Agnostic Execution
date: '2026-02-26'
draft: false
weight: 7
slug: chapter-5-semantic-agnostic-execution
---

Chapters 3 and 4 established the legislative pipeline: governance artifacts are authored, validated, ratified, and compiled into protocol JSON. The law is written. The law is compiled. But it has never executed.

This chapter is the moment of enforcement. It answers the question that separates PGS from every workflow engine, orchestrator, and application framework: **Can a single execution engine process any domain's workflows --- financial, medical, industrial, blockchain --- without containing a single line of domain-specific logic?**

The answer is semantic-agnostic execution. The engine loads a compiled DAG, constructs it as an immutable in-memory graph, resolves runtime bindings that map abstract capability codes to concrete implementations, and traverses the graph by structural prefix alone --- `IN_` for admission, `CC_` for capability dispatch, `EXIT` for termination. It never inspects what a payload contains. It never interprets what a workflow means. It routes structure. The chapter walks through the complete execution of the User Registration workflow from Chapter 3, step by step, showing how each node is dispatched and how the resulting trace constitutes structural proof of what the engine did. By the end, the reader will understand why the same engine that processes user registration can process loan approval, device provisioning, or AI agent governance --- without modification.

> **The Structural Invariance Principle**
>
> Five invariants govern all execution in a protocol-governed system. They are established by the architectural layers defined in Chapters 2--4 and enforced by the execution engine described in Chapters 5--8. They are stated here once and referenced throughout.

1.  **The engine is domain-blind.** It interprets structure, not meaning. No domain concept enters the execution layer.
2.  **Execution is edge-bound.** The engine traverses compiled DAG edges. No execution path exists outside the graph.
3.  **Mutation is declared.** Only CS_ steps with explicit runtime bindings can change world state. CT_ steps are pure. Both CT_ and CS_ are resolved to their concrete implementations via RB_ (Runtime Binding) artifacts --- the same symmetric binding mechanism applies to all capability types.
4.  **Behavior is deterministic.** Identical artifacts and identical inputs produce identical execution, always.
5.  **Undeclared behavior is impossible.** The vocabulary is finite, the artifacts are validated, and the engine enforces only what is declared. There is no ambient authority.

> These five invariants are not design aspirations. They are structural consequences of the architecture. Each is independently verifiable. Together they constitute the guarantee that makes protocol-governed execution trustworthy.

## 5.1 --- The Engineering Objective

The compiled protocol artifacts sit in `protocol/artifacts/`. They were authored in Chapter 3. They were compiled in Chapter 4. They have never executed.

This chapter changes that.

But the execution engine that runs these artifacts knows nothing about users, registration, or email addresses. It does not know what `user_record` contains. It does not know why `CC_GENERATE_USER_ID_V0` exists. It does not know the difference between a financial transaction and a user registration --- and it must not. The moment the engine understands domain semantics, it becomes entangled with the domain it executes. Entanglement means every domain change requires an engine change. That path leads back to the application-centric model.

**The Task:** Execute the compiled user registration workflow from Chapter 4 --- traversing the DAG, dispatching capabilities, recording a trace.

**The Constraint:** The execution engine must not contain domain-specific logic. No references to "user," "registration," or "email." Routing is determined entirely by structural prefix (IN_, CC_, EXIT) and compiled edge conditions (SUCCESS, VIOLATION, BACKEND_ERROR). The engine sees structure. It is blind to meaning.

In the application-centric approach, the runtime is the locus of domain logic. Controllers parse domain objects. Services apply business rules. Repositories know their entity schemas. Scale this to hundreds of workflows across dozens of domains and the execution engine must understand insurance claims, loan applications, inventory management, compliance reporting --- it becomes an encyclopedia with a runtime. The runtime and the domain are inseparable --- and that inseparability is the root of semantic entanglement.

In PGS, the execution engine is a graph walker. PostgreSQL does not know the difference between customer records and inventory items --- it executes queries against relational structures. The PGS execution engine is the same: it does not know the difference between user registration and financial settlement. It loads a compiled DAG. It follows edges. It dispatches to capabilities by prefix. It records a trace. It does not think.

## 5.2 --- The Immutable DAG

The first thing the engine does is construct a DAG from the compiled workflow JSON. This is not a planning step --- it is a structural translation. The JSON becomes a frozen, immutable graph data structure.

**Definition:** The DAG (Directed Acyclic Graph) is the engine's internal representation of a compiled workflow --- an immutable set of nodes, edges, and entry/terminal points.

**Key Properties:**

1.  **Immutable.** Once constructed, the DAG cannot be modified. No nodes can be added, no edges can be removed, no routing can change during execution. The DAG is frozen. The engine never queries governance registries during traversal; it executes solely from compiled protocol artifacts loaded at startup.
2.  **Prefix-classified.** Each node carries a `node_type` derived from its concern prefix: `IN_` becomes `"intent"`, `CC_` becomes `"capability_contract"`, `EXIT` becomes `"exit"`. The type determines how the engine dispatches the node --- nothing else.
3.  **Edge-conditioned.** Each edge carries a `condition` --- the result status that triggers traversal. The edge from CC_GENERATE_USER_ID_V0 with condition `SUCCESS` leads to CC_REGISTER_USER_KYC_V0. The edge with condition `VIOLATION` leads to EXIT. The engine selects the edge matching the returned result status.

### Example 5.1 --- DAG Constructed from WF_REGISTER_USER_UNVERIFIED_V0

    DAG {
      dag_id:        "WF_REGISTER_USER_UNVERIFIED_V0"
      workflow_code: "WF_REGISTER_USER_UNVERIFIED_V0"
      entry_nodes:   ["IN_USER_REGISTERED_V0"]
      terminal_nodes: ["EXIT"]

      nodes:
        IN_USER_REGISTERED_V0  → type: intent
        CC_GENERATE_USER_ID_V0 → type: capability_contract
                                  inputs: {user_record: "$.payload.user_record"}
        CC_REGISTER_USER_KYC_V0 → type: capability_contract
                                   inputs: {user_record: "$.payload.user_record",
                                            user_id: "$.payload.user_id"}
        CC_APPEND_USER_EVENT_V0 → type: capability_contract
                                   inputs: {event_type: "EV_USER_REGISTERED_..._V0",
                                            user_id: "$.payload.user_id",
                                            data: "$.payload.user_record"}
        EXIT                    → type: exit, reason: "EXITED"

      edges:
        IN_USER_REGISTERED_V0  --[ACK]-->     CC_GENERATE_USER_ID_V0
        IN_USER_REGISTERED_V0  --[NACK]-->    EXIT
        CC_GENERATE_USER_ID_V0 --[SUCCESS]--> CC_REGISTER_USER_KYC_V0
        CC_GENERATE_USER_ID_V0 --[VIOLATION]-->EXIT
        CC_REGISTER_USER_KYC_V0--[SUCCESS]--> CC_APPEND_USER_EVENT_V0
        CC_REGISTER_USER_KYC_V0--[ALREADY_EXISTS]-->CC_APPEND_USER_EVENT_V0
        CC_REGISTER_USER_KYC_V0--[VIOLATION]-->EXIT
        CC_REGISTER_USER_KYC_V0--[BACKEND_ERROR]-->EXIT
        CC_APPEND_USER_EVENT_V0--[SUCCESS]--> EXIT
        CC_APPEND_USER_EVENT_V0--[VIOLATION]-->EXIT
        CC_APPEND_USER_EVENT_V0--[BACKEND_ERROR]-->EXIT
    }

**Analysis:**

- **What the engine sees.** Nodes with types (`intent`, `capability_contract`, `exit`). Edges with conditions (`ACK`, `SUCCESS`, `VIOLATION`). Input bindings with JSONPath expressions (`$.payload.user_record`). This is the engine's entire world.
- **What the engine does not see.** It does not see "user registration." It does not see "email validation." It does not see "KYC compliance." The strings `user_record`, `user_id`, `email` are opaque tokens to the engine --- they are keys it resolves, not concepts it understands.
- **Immutability is structural.** The DAG is constructed from frozen data structures. There is no `add_node()` method. There is no `remove_edge()` method. The engine cannot modify the graph it executes --- by construction, not by convention.

## 5.3 --- Runtime Bindings

The compiled protocol artifacts declare abstract capability codes: `CT_PURE_GENERATE_ID_V0`, `CS_USER_ALIAS_INDEX_V0`, `CS_USER_EVENTS_V0`. These are not function names. They are not class names. They are protocol-level identifiers. Something must map them to executable code.

That something is the Runtime Binding artifact (RB_).

**Definition:** A Runtime Binding is a mapping from abstract capability codes --- both CT_ (Capability Transforms) and CS_ (Capability Side Effects) --- to their concrete runtime implementations, resolved at startup before any workflow executes. The same binding mechanism applies symmetrically to both capability types: the runtime is fully implementation-agnostic across the entire capability surface.

**Key Properties:**

1.  **Resolved at startup.** The engine resolves all bindings before the first node is dispatched. If a binding is missing --- for either a CT_ or CS_ code --- execution halts before the DAG traversal begins, not mid-workflow.
2.  **Environment-scoped.** The same compiled protocol can execute against different runtime bindings. In development, `CS_USER_EVENTS_V0` might bind to a local JSON file. In production, it might bind to a distributed event store. The DAG is identical. The bindings differ.
3.  **Immutable during execution.** Once resolved, bindings cannot change. A capability contract that dispatches to `MutableJsonRuntime` at the start of execution dispatches to `MutableJsonRuntime` at the end. There is no dynamic rebinding.

### Example 5.2 --- Runtime Binding Resolution

    Abstract Code              → Concrete Runtime          → Configuration
    ─────────────────────────────────────────────────────────────────────
    CT_PURE_GENERATE_ID_V0     → PureTransformRuntime      → module: pgs_transforms.transforms.generate_id
    CS_USER_ALIAS_INDEX_V0     → RegistryRuntime           → path: data/user_kyc_index.json
    CS_USER_EVENTS_V0          → AppendOnlyJsonlRuntime    → path: data/user_events.jsonl

The RB_ artifact declares this mapping for all CT_ and CS_ codes used by a domain's workflows.

*(Representative RB_ artifact examples are available in* `protocol_snapshot/artifacts/runtime_bindings/`*.)*

**Analysis:**

- **Separation of protocol from environment.** The workflow declares `CS_USER_EVENTS_V0`. The runtime binding resolves it to `AppendOnlyJsonlRuntime` with a specific file path. The workflow does not know what `AppendOnlyJsonlRuntime` is. The runtime does not know why the workflow uses `CS_USER_EVENTS_V0`. Each knows only its own concern. The same isolation applies to CT_ bindings.
- **Parameter substitution is explicit.** `{{module_data_root}}` is a declared parameter, substituted at binding resolution time --- not a hidden environment variable discovered at runtime. The set of parameters is finite and declared in the RB_ artifact.
- **The closed runtime registry.** The engine maintains a fixed set of runtime classes: `MutableJsonRuntime`, `RegistryRuntime`, `AppendOnlyJsonlRuntime`, `PureTransformRuntime`, and others. The RB_ artifact's `host` field must name one of these. An RB_ artifact that references an undeclared class fails at binding resolution --- before any workflow executes. There is no plugin discovery. The runtime surface is bounded. Extending the runtime surface requires modifying the engine codebase --- not an RB_ artifact. This is a deliberate authority boundary: runtime bindings configure which implementations are used; only the engine codebase determines which implementations are available.

## 5.4 --- The Execution Context

Everything in the execution model is immutable --- the DAG, the bindings, the compiled artifacts --- except one thing: the execution context.

**Definition:** The Execution Context is the single mutable structure in the execution model. It carries the evolving payload, tracks node states, accumulates capability results, and records termination.

**Key Properties:**

1.  **Payload evolution.** The context starts with the initial payload (the intent's input). As each capability executes, its outputs are merged into the payload. After CC_GENERATE_USER_ID_V0 completes, `user_id` appears in the payload. Subsequent steps can reference it via `$.payload.user_id`.
2.  **Terminal classification.** The context tracks whether execution ended in SUCCESS, FAILURE, ABORT, or TIMEOUT. This is a structural classification, not a domain judgment.
3.  **Context hash.** The engine computes a SHA-256 hash of the payload at termination. This hash enables replay verification --- an auditor can re-execute the workflow and compare context hashes to confirm determinism.

### Example 5.3 --- Context Evolution Through Execution

    STEP 0 — Initial payload (from intent submission):
      payload: {
        user_record: {first_name: "Jane", last_name: "Doe", email: "jane@example.com"}
      }

    STEP 1 — After CC_GENERATE_USER_ID_V0 (SUCCESS):
      payload: {
        user_record: {first_name: "Jane", last_name: "Doe", email: "jane@example.com"},
        user_id: "AC_7f3a2b..."
      }

    STEP 2 — After CC_REGISTER_USER_KYC_V0 (SUCCESS):
      payload: {
        user_record: {first_name: "Jane", last_name: "Doe", email: "jane@example.com"},
        user_id: "AC_7f3a2b...",
        target_ref: "AC_7f3a2b..."
      }

    STEP 3 — After CC_APPEND_USER_EVENT_V0 (SUCCESS):
      payload: {
        user_record: {first_name: "Jane", last_name: "Doe", email: "jane@example.com"},
        user_id: "AC_7f3a2b...",
        target_ref: "AC_7f3a2b...",
        result_status: "SUCCESS"
      }

    EXIT — Classification: SUCCESS → COMPLETED
      context_hash: sha256:e4a1c9...

**Analysis:**

- **The payload is a monotonically growing record.** Each capability adds to it. No capability removes from it. Capabilities may overwrite their own declared output keys, but cannot delete prior keys from the payload. The context is an accumulation of structural results, not a domain object.
- **Expression resolution is mechanical.** When CC_REGISTER_USER_KYC_V0 declares `user_id: $.payload.user_id`, the engine resolves this by looking up the path in the current payload. It does not know what a `user_id` is. It finds the value at the path, or it returns None --- which fails the step. Resolution is a dictionary lookup, not a semantic interpretation. Expression resolution does not evaluate predicates --- it only dereferences paths. There is no `$.payload.user_id > 100` or `$.payload.email contains "@"`. The engine resolves values; it does not judge them.
- **The engine does not interpret results.** After CC_GENERATE_USER_ID_V0 returns SUCCESS, the engine merges its outputs into the payload and follows the SUCCESS edge. It does not inspect what `user_id` contains. It does not validate that the ID looks like a user ID. It follows the edge.

## 5.5 --- DAG Traversal: The Execution Loop

The engine has loaded the DAG. The bindings are resolved. The execution context is initialized. Now the engine traverses.

The traversal loop is structurally simple:

    while current_node exists and execution not terminated:
        1. Get node from DAG
        2. If EXIT → classify exit, terminate
        3. Route by node_type:
             "intent"              → validate payload against intent schema
             "capability_contract" → execute capability pipeline
        4. Get result_status
        5. Follow edge matching result_status → next node
        6. If no matching edge → NO_TRANSITION failure
           (The absence of an edge is a protocol violation, not an implicit termination)

### Walking the User Registration Workflow

**Node 1: IN_USER_REGISTERED_V0** (type: `intent`)

The engine dispatches to the intent executor. The intent executor validates the payload against the intent's declared input schema: does the payload contain `user_record`? Does `user_record` contain `first_name`, `last_name`, `email`? Are the types correct?

The payload is valid. The intent executor returns `ACK`.

The engine looks up the edge: `IN_USER_REGISTERED_V0 --[ACK]--> CC_GENERATE_USER_ID_V0`.

Current node becomes CC_GENERATE_USER_ID_V0.

**Node 2: CC_GENERATE_USER_ID_V0** (type: `capability_contract`)

The engine resolves the node's input bindings:

    user_record: $.payload.user_record → {first_name: "Jane", last_name: "Doe", email: "jane@example.com"}

The engine dispatches to the capability pipeline with the resolved inputs. The pipeline loads the capability contract, finds the pipeline declaration (`[CT_PURE_GENERATE_ID_V0]`), resolves step-level bindings, and dispatches to the CT executor.

The CT executor runs the atom. It returns a deterministic ID: `AC_7f3a2b...`.

The pipeline wraps the result: `{user_id: "AC_7f3a2b...", result_status: "SUCCESS"}`.

The engine merges the result into the execution context. The payload now contains `user_id`.

The engine follows the edge: `CC_GENERATE_USER_ID_V0 --[SUCCESS]--> CC_REGISTER_USER_KYC_V0`.

**Node 3: CC_REGISTER_USER_KYC_V0** (type: `capability_contract`)

The engine resolves input bindings:

    user_record: $.payload.user_record → {first_name: "Jane", ...}
    user_id:     $.payload.user_id     → "AC_7f3a2b..."

Note: `$.payload.user_id` resolves because CC_GENERATE_USER_ID_V0 merged it into the payload in the previous step. If that step had failed, this binding would resolve to None, and the pipeline would return VIOLATION.

The capability pipeline executes two steps: CT_PURE_GENERATE_ID_V0 (generates a KYC key) then CS_USER_ALIAS_INDEX_V0 (registers the key in the alias index). The CT_ step is pure computation. The CS_ step is a governed side effect --- the first point in the workflow where the system writes to the world.

Result: `SUCCESS`.

Edge: `CC_REGISTER_USER_KYC_V0 --[SUCCESS]--> CC_APPEND_USER_EVENT_V0`.

**Node 4: CC_APPEND_USER_EVENT_V0** (type: `capability_contract`)

The engine resolves input bindings:

    event_type: "EV_USER_REGISTERED_UNVERIFIED_V0"  (literal — not a path expression)
    user_id:    $.payload.user_id → "AC_7f3a2b..."
    data:       $.payload.user_record → {first_name: "Jane", ...}

The pipeline executes one step: CS_USER_EVENTS_V0 with operation `APPEND`. The runtime binding resolved this to `AppendOnlyJsonlRuntime`. The runtime appends a record to an immutable event log.

Result: `SUCCESS`.

Edge: `CC_APPEND_USER_EVENT_V0 --[SUCCESS]--> EXIT`.

**Node 5: EXIT** (type: `exit`)

The engine reaches the terminal node. It classifies the exit: the last edge condition was `SUCCESS`, so the exit reason is `COMPLETED`. The execution context is marked as SUCCESS.

The traversal loop terminates.

### What the Engine Did Not Do

The engine did not:

- Parse `user_record` to understand what a user is
- Validate that `email` looks like an email address (the intent schema did that)
- Decide whether a duplicate registration should continue or terminate (the workflow edges declared that)
- Choose between different storage backends (the runtime binding declared that)
- Add retry logic, timeout handlers, or error recovery (none were declared)

The engine followed the graph. It resolved bindings. It dispatched capabilities. It recorded results. It followed edges. That is all it does.

This reveals a profound separation of concerns:

  -------------------------------------------------------------------------------------------------------------------
  Concern                                        Owner                Changes When
  ---------------------------------------------- -------------------- -----------------------------------------------
  **Execution** (graph traversal)                Engine               Never --- write once, run any domain

  **Behavior** (workflow composition)            Protocol artifacts   When governance authors change business rules

  **Domain logic** (computation, side effects)   Capabilities         When implementations evolve
  -------------------------------------------------------------------------------------------------------------------

Three different concerns. Three different change surfaces. Zero overlap. The engine does not change when the domain changes. The protocol does not change when an implementation is optimized. The capabilities do not change when a workflow is recomposed. This is not layered architecture --- it is constitutional separation.

## 5.6 --- Validation and Failure Surface

Chapters 3 and 4 showed governance and compilation failures --- structural violations caught before execution begins. This section shows a third failure surface: runtime failures. These occur when the compiled protocol is structurally valid, the FQDN tree is correct, the Builder succeeded --- but the runtime environment cannot satisfy the protocol's requirements.

### Runtime Failure Table

  ---------------------------------------------------------------------------------------------------------------------------------------------------------
  Step            Failure                         Cause                                                                           When
  --------------- ------------------------------- ------------------------------------------------------------------------------- -------------------------
  1               Missing protocol artifact       Compiled JSON not found at expected path                                        Load time

  2               Unbound capability              RB_ artifact missing a binding for a declared CS_ code                        Startup

  3               Intent rejection                Payload violates intent input schema                                            First node

  4               Expression resolution failure   `$.payload.user_id` not yet in payload                                          Mid-traversal

  5               Undeclared result status        Capability returns status not in `result_status_contract.allowed`               Mid-traversal

  6               No transition                   Result status has no matching edge in the DAG                                   Mid-traversal

  7               Context hash mismatch           Re-execution produces different payload hash --- non-deterministic capability   Post-execution (replay)
  ---------------------------------------------------------------------------------------------------------------------------------------------------------

### A Runtime Failure

Suppose the RB_ artifact declares a binding for `CS_USER_ALIAS_INDEX_V0` that references a runtime class not in the closed registry *(see Appendix B, Example 5.4)*.

The engine rejects this at startup:

    RUNTIME FAILURE
      Phase:      Binding Resolution
      Artifact:   RB_CAPABILITY_BINDINGS_V0
      Binding:    CS_USER_ALIAS_INDEX_V0
      Check:      Runtime class lookup
      Detail:     "MongoRegistryRuntime" is not a registered runtime class.
                  Available: [MutableJsonRuntime, RegistryRuntime,
                              AppendOnlyJsonlRuntime]
      Resolution: Use a registered runtime class or extend the runtime registry

**Key distinction from earlier failures:**

  ---------------------------------------------------------------------------------------------------
  Failure Surface         Chapter      When             What It Validates
  ----------------------- ------------ ---------------- ---------------------------------------------
  Governance validation   Ch 3         Authoring time   Individual artifact structure

  Compilation             Ch 4         Build time       Artifact relationships, dependency closure

  Runtime                 Ch 5         Execution time   Environment readiness, binding satisfaction
  ---------------------------------------------------------------------------------------------------

Each failure surface catches violations that earlier surfaces cannot detect. Governance does not know about runtime classes. The Builder does not know about binding satisfaction. The execution engine validates what only it can see --- the runtime environment.

## 5.7 --- Structural Insight (Doctrine Moment)

The reader has now seen a compiled workflow execute from first node to last --- prefix-driven routing, expression resolution, capability dispatch, and payload evolution. At no point did the engine interpret domain semantics.

This is Chapter 2's **Property 4 --- Semantic Agnosticism** made operational. The engine is not merely "unaware" of the domain --- it is structurally incapable of encoding domain awareness. The dispatch table is fixed:

  ----------------------------------------------------------------------
  Prefix   Dispatch                          Domain Knowledge Required
  -------- --------------------------------- ---------------------------
  IN_     Validate payload against schema   None

  CC_     Execute capability pipeline       None

  EXIT     Classify and terminate            None
  ----------------------------------------------------------------------

There is no `if node.code.startswith("USER")` in the engine. There is no handler registry keyed by domain concept. The engine sees prefixes and conditions --- structural markers that determine execution behavior without semantic interpretation.

**Invariant I-E1 --- Prefix-Driven Execution:** Execution routing is determined solely by structural prefix and compiled edge conditions. The engine contains no conditional logic based on payload content. A workflow that registers users and a workflow that processes financial transactions traverse the same engine, use the same dispatch table, and produce traces in the same schema. The engine is domain-invariant. It enforces protocol law the way a CPU enforces instruction order --- without understanding the program's purpose.

This is a direct consequence of the Structural Invariance Principle (Chapter 5 opening): execution is edge-bound, the engine is domain-blind, and undeclared behavior is impossible. The engine cannot invent new states, edges, or outcomes --- the compiled DAG is law.

A common intuition resists this: flexibility requires intelligence. The opposite is true. An engine coupled to one domain must be rewritten for another. An engine that understands nothing is coupled to nothing. Semantic blindness is not a limitation --- it is the precondition for domain-invariant execution. This matters acutely as AI-generated artifacts enter production. The engine does not care who authored the protocol. It enforces the law.

## 5.8 --- Solved Problems

### Problem 5.1 --- Hidden Business Logic in Runtime

**Scenario:** A runtime handler checks whether a user has a premium account and conditionally skips a validation step.

**Application-Centric Approach:** The handler contains `if user.is_premium: skip_kyc_check()`. This logic is invisible in the architecture diagram, absent from any specification, and discoverable only by reading source code. When the business rule changes, a developer must find this conditional --- in a handler, in a service, in middleware --- and modify it without breaking surrounding logic.

**PGS Approach:**

1.  The engine dispatches CC_REGISTER_USER_KYC_V0 by prefix --- it is a CC_ node
2.  The engine resolves input bindings mechanically --- `$.payload.user_record`, `$.payload.user_id`
3.  The engine receives a result status --- SUCCESS, ALREADY_EXISTS, VIOLATION, or BACKEND_ERROR
4.  The engine follows the corresponding edge. There is no conditional. There is no `if premium`. The engine does not know what "premium" means
5.  If the business requires different treatment for premium users, that must be authored as a different workflow (WF_REGISTER_PREMIUM_USER_V0) with different governance artifacts --- visible, validated, and ratified

**Eliminated pathology:** Semantic entanglement. Domain logic cannot hide in the engine because the engine has no mechanism to express it.

### Problem 5.2 --- Runtime Environment Drift

**Scenario:** The same codebase behaves differently in staging and production because of environment variables and feature flags.

**Application-Centric Approach:** `process.env.ENABLE_KYC_CHECK` controls whether KYC validation runs. Staging has it set to `false`. Production has it set to `true`. The deployed code is identical; the behavior diverges. A test that passes in staging fails in production --- and the cause is invisible in the code itself.

**PGS Approach:**

1.  The compiled protocol artifact is identical in staging and production. The DAG has the same nodes, same edges, same input bindings
2.  Only the runtime binding (RB_) differs. In staging, `CS_USER_ALIAS_INDEX_V0` binds to a local JSON file. In production, it binds to a persistent store
3.  The behavioral surface --- which steps execute, in what order, with what edges --- is invariant across environments
4.  Environment variability is scoped to a single, explicit artifact (RB_) that can be audited independently

**Eliminated pathology:** Execution drift. The protocol artifact is the same everywhere. Environmental differences are confined to binding resolution --- a separate, auditable concern.

### Problem 5.3 --- Implicit Exception Semantics

**Scenario:** A capability throws an unhandled exception that propagates up the call stack, skipping cleanup logic and leaving the system in an inconsistent state.

**Application-Centric Approach:** Exceptions are control flow. A database timeout throws `ConnectionException`. If caught at the service level, the service retries. If caught at the controller level, the controller returns a 500. If caught nowhere, the process crashes. The failure path depends on where the exception is caught --- a non-local, implicit decision with no formal specification.

**PGS Approach:**

1.  The capability contract declares `result_status_contract: {allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]}`
2.  The capability must return one of these statuses. It does not throw exceptions into the engine
3.  The engine follows the edge matching the returned status. BACKEND_ERROR → EXIT is a declared path, not an exception handler
4.  Every failure mode has a declared edge. There are no unhandled exceptions in the protocol sense --- every outcome is structural

**Eliminated pathology:** Implicit control flow. Failure paths are edges in the graph --- declared, visible, and auditable. Exceptions do not propagate across the protocol boundary. The engine sees result statuses, not stack traces.

## 5.9 --- Generated Output: The Execution Trace

The DAG has been traversed. Every node was entered and exited. Every result status was recorded. Every edge was followed. The trace is the structural proof of what happened.

> **[DIAGRAM 6] --- Execution Flow: DAG to Trace**

    Compiled Protocol Artifacts (JSON)
            ↓
    Protocol Loader (static load, no discovery)
            ↓
    DAG Construction (frozen, immutable graph)
            ↓
    Runtime Binding Resolution (RB_ → concrete runtimes)
            ↓
    Execution Loop
      IN_USER_REGISTERED_V0     → ACK
      CC_GENERATE_USER_ID_V0    → SUCCESS
      CC_REGISTER_USER_KYC_V0   → SUCCESS
      CC_APPEND_USER_EVENT_V0   → SUCCESS
      EXIT                      → COMPLETED
            ↓
    Execution Trace (JSONL)

### The Trace

    {"event_type": "execution_start",
     "execution_id": "EX_20260222_143012",
     "workflow_code": "WF_REGISTER_USER_UNVERIFIED_V0",
     "timestamp": "2026-02-22T14:30:12.001Z",
     "sequence": 1}

    {"event_type": "node_start",
     "node_id": "IN_USER_REGISTERED_V0",
     "node_type": "intent",
     "timestamp": "2026-02-22T14:30:12.002Z",
     "sequence": 2}

    {"event_type": "node_end",
     "node_id": "IN_USER_REGISTERED_V0",
     "result_status": "ACK",
     "duration_ms": 3,
     "timestamp": "2026-02-22T14:30:12.005Z",
     "sequence": 3}

    {"event_type": "node_start",
     "node_id": "CC_GENERATE_USER_ID_V0",
     "node_type": "capability_contract",
     "timestamp": "2026-02-22T14:30:12.006Z",
     "sequence": 4}

    {"event_type": "node_end",
     "node_id": "CC_GENERATE_USER_ID_V0",
     "result_status": "SUCCESS",
     "duration_ms": 12,
     "timestamp": "2026-02-22T14:30:12.018Z",
     "sequence": 5}

    {"event_type": "node_start",
     "node_id": "CC_REGISTER_USER_KYC_V0",
     "node_type": "capability_contract",
     "timestamp": "2026-02-22T14:30:12.019Z",
     "sequence": 6}

    {"event_type": "node_end",
     "node_id": "CC_REGISTER_USER_KYC_V0",
     "result_status": "SUCCESS",
     "duration_ms": 8,
     "timestamp": "2026-02-22T14:30:12.027Z",
     "sequence": 7}

    {"event_type": "node_start",
     "node_id": "CC_APPEND_USER_EVENT_V0",
     "node_type": "capability_contract",
     "timestamp": "2026-02-22T14:30:12.028Z",
     "sequence": 8}

    {"event_type": "node_end",
     "node_id": "CC_APPEND_USER_EVENT_V0",
     "result_status": "SUCCESS",
     "duration_ms": 5,
     "timestamp": "2026-02-22T14:30:12.033Z",
     "sequence": 9}

    {"event_type": "workflow_complete",
     "exit_condition": "SUCCESS",
     "exit_reason": "COMPLETED",
     "total_duration_ms": 32,
     "context_hash": "sha256:e4a1c9...",
     "timestamp": "2026-02-22T14:30:12.034Z",
     "sequence": 10}

**What the trace proves:**

- **Completeness.** Every node entry and exit is recorded. No step is invisible. The trace captures the entire traversal --- from `execution_start` to `workflow_complete`.
- **Structural ordering.** Events are sequenced monotonically (`sequence: 1, 2, 3...`). The trace is a total order over execution events. There is no ambiguity about what happened when.
- **Result status fidelity.** Each `node_end` records the result status returned by the node. The transition from one node to the next can be verified against the compiled DAG: did the engine follow the correct edge for the returned status?
- **Context hash.** The `workflow_complete` event includes a SHA-256 hash of the final payload. An auditor can re-execute the same workflow with the same inputs, compute the context hash, and compare. If the hashes match, execution was deterministic. If they differ, something changed --- and the trace identifies where.
- **No domain content in trace events.** The trace records `node_id`, `node_type`, `result_status`, `duration_ms`. It does not record "Jane Doe was registered" or "email was jane@example.com." The trace is structural, not narrative. Chapter 9 explores trace structure in full depth.
- **Auditability is a consequence of blindness.** Because the engine cannot distinguish important events from unimportant ones, it records everything --- every node entry, every node exit, every result status, every edge traversal. In regulated industries, this is not a feature added as an afterthought. It is a structural consequence of the engine's ignorance. The engine does not choose what to log. It logs what it does, and what it does is everything. Audits become queries against structured trace data --- not forensic investigations through application logs.
- **From confidence to proof.** Traditional systems rely on test-driven confidence: unit tests, integration tests, observability dashboards. These tell you something probably worked. The execution trace offers something stronger: trace-proven correctness. Instead of asking "did our tests catch it?" an operator can ask "show me exactly what happened --- and why it was allowed." Every decision is traceable to a declared edge. Every capability dispatch is traceable to a compiled contract. Chapter 9 develops this into the full trace examination model.

**Structural impossibility:** The engine cannot invent new states, edges, or outcomes. The trace is a faithful record of the compiled DAG's traversal --- nothing more and nothing less. If the trace records `CC_GENERATE_USER_ID_V0 → SUCCESS → CC_REGISTER_USER_KYC_V0`, then the compiled DAG declares that edge and the capability returned that status. The trace cannot contain a transition that the DAG does not declare.

You authored governance artifacts. The Builder compiled them. The engine executed them. The trace recorded the execution. At no point did the engine know what it was doing --- and that is the point.

The same engine that executed user registration will execute financial settlement, compliance auditing, and supply chain orchestration in later chapters. No code changes. No configuration tweaks. No domain-specific extensions. Just different protocol artifacts. The execution problem is solved once. Every domain thereafter is a protocol authoring problem --- not an engineering problem.

## 5.10 --- Boundary and Forward Pointer

This chapter proved that the execution engine traverses compiled protocol artifacts without domain awareness --- routing by prefix, resolving bindings mechanically, and recording a structural trace.

**What this chapter did not cover:**

- Capability transform internals --- how CT_ atoms and molecules compute results (Chapter 6)
- Capability side-effect internals --- how CS_ runtimes interact with the world (Chapter 7)
- The full failure taxonomy --- classifying failures by structural category (Chapter 8)
- Trace inspection and replay --- what traces reveal under forensic examination (Chapter 9)
- Admission control --- pre-execution precondition enforcement (Chapter 8)

**What comes next:** The engine dispatched to CT_ and CS_ steps as black boxes --- it sent inputs and received result statuses. Chapter 6 opens the CT_ box. The reader will see how pure computation is expressed as composable, deterministic capability transforms --- atoms and molecules --- with constitutional isolation from side effects.

We are moving from the execution loop into execution internals.

## 5.11 --- Review Questions

1.  **Why must execution be semantic-agnostic?**

- *If the engine encodes domain logic, every domain change requires an engine change. Semantic entanglement means the execution layer and the domain are inseparable --- the engine becomes an application. Semantic agnosticism ensures the engine is domain-invariant: it can execute any workflow from any domain without modification.*

2.  **What determines node routing at runtime --- payload content or compiled edges?**

- *Compiled edges. The engine selects the next node by matching the returned result_status against declared edge conditions. It does not inspect payload content to make routing decisions. The routing is structural, not semantic.*

3.  **Can the engine inspect payload meaning to alter flow? Why not?**

- *No. The engine resolves payload paths mechanically (e.g.,* `$.payload.user_id` *→ value lookup) but does not interpret what the values mean. There is no mechanism in the engine to write* `if payload.email == "admin@..."`*. The dispatch table is fixed: prefix → handler. The handler does not branch on payload semantics.*

4.  **What happens if a capability returns a status not declared in its result_status_contract?**

- *The engine rejects the status. The result_status_contract declares the bounded set of allowed outcomes. A status outside this set is a protocol violation --- the engine cannot follow an edge that was never declared. This prevents capabilities from inventing new control flow paths.*

5.  **How do runtime bindings (RB_) differ from governance artifacts?**

- *Governance artifacts (IN_, WF_, CC_) declare behavioral law --- what the system does. Runtime bindings (RB_) declare operational mapping --- how abstract codes resolve to concrete implementations. Changing an RB_ changes which runtime executes a CS_ step, but does not change the workflow's behavioral surface (nodes, edges, result statuses). RB_ is an execution concern, not a governance concern.*

6.  **Why does prefix-driven dispatch preserve the WHAT/HOW separation?**

- *The WHAT (behavioral specification) lives in governance artifacts and compiled protocol. The HOW (execution mechanics) lives in the engine's dispatch table and runtime bindings. Prefix-driven dispatch is the mechanism that connects them without entangling them: IN_ → intent validation, CC_ → capability pipeline, EXIT → termination. The dispatch is structural, not domain-specific.*

7.  **How does execution determinism differ from compilation determinism (I-C1)?**

- *Compilation determinism (I-C1) guarantees that identical governance inputs produce identical compiled artifacts. Execution determinism guarantees that identical compiled artifacts with identical inputs and identical runtime bindings produce identical traces and context hashes. Compilation determinism is about the Builder. Execution determinism is about the engine. Both are structural guarantees, but they operate on different inputs at different phases.*
