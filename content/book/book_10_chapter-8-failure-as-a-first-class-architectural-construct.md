---
title: Chapter 8 — Failure as a First-Class Architectural Construct
date: '2026-03-19'
draft: false
weight: 10
slug: chapter-8-failure-as-a-first-class-architectural-construct
---

Chapters 5 through 7 proved that PGS execution works --- DAG traversal, pure computation, governed mutation. The happy path is established. But architects do not evaluate systems by their happy paths. They evaluate them by their failure modes.

This chapter answers: **When a protocol-governed system fails, what exactly happens --- and why is every failure classifiable, deterministic, and diagnosable without the original runtime?**

In application-centric systems, failures are discovered forensically --- log spelunking, stack trace analysis, hypothesis testing, and the dreaded "works on my machine." In PGS, failure is a first-class architectural construct. Every failure falls into exactly one of four canonical categories: governance violations, binding resolution failures, execution failures, and structural violations. Each category has a deterministic signature, a trace-complete record, and a reconstruction path. The chapter introduces the Reconstructability Property --- the guarantee that any failure can be fully diagnosed from governance artifacts and execution traces alone, without access to the original runtime environment. It establishes "no silent repair" as a constitutional invariant: no layer may fix, mask, or compensate for violations originating in another layer. Failures propagate honestly. The reader will understand why PGS systems are easier to debug than systems with more sophisticated error handling --- because the failure taxonomy is structural, not procedural.

## 8.1 --- The Engineering Objective

Chapters 5 through 7 proved that PGS execution works. The workflow executor traverses a compiled DAG. The CC_ pipeline dispatches CT_ and CS_ steps. Pure computation produces deterministic results. Governed side effects perform declared mutations. Traces record every step.

This chapter proves that PGS failure works.

Every architecture book explains how things succeed. Few explain how things break. Yet architects evaluate systems by their failure modes --- not by their happy paths. A system that works correctly under ideal conditions is unremarkable. A system that fails structurally, classifiably, and reproducibly under any conditions is architecturally sound.

**The Task:** Demonstrate that failure in PGS is classifiable into exactly four structural categories, deterministic under identical inputs, trace-complete without source code inspection, and reconstructable without the original runtime.

**The Constraint:** No silent repair --- the system may not auto-correct schema mismatches, substitute missing bindings, suppress failed CS_ operations, or retry without explicit declaration. No ambiguous failure classes --- every failure maps to exactly one category determined by the layer at which it occurs. No debugging by guessing --- diagnosis requires only governance artifacts and execution traces.

In the application-centric approach, failures manifest as stack traces, log fragments, and Slack threads. A NullPointerException in a service class could mean a missing database record, a misconfigured environment variable, a race condition in a cache, or a deployment that shipped the wrong version. The exception does not tell you which. Diagnosis requires reproducing the environment, reading source code, stepping through debuggers, and reasoning about hidden mutable state. Two identical inputs can fail differently because the runtime carries implicit context --- connection pools, cached values, session state, thread-local variables. "Works on my machine" is not a joke. It is the canonical symptom of systems where failure behavior depends on invisible runtime state.

In PGS, failure is structural. Every failure has a category, a diagnostic signature, and a trace record. The same governance artifacts with the same payload produce the same failure at the same step with the same classification --- on any machine, at any time, in any environment. Failure is not an operational accident. It is an architectural event.

## 8.2 --- The Failure Taxonomy

**Definition:** Every failure in PGS falls into exactly one of four structural classes, determined by the layer at which it occurs. The categories are exhaustive --- there is no fifth class. The categories are mutually exclusive --- a failure belongs to exactly one.

### The Four Categories

  -------------------------------------------------------------------------------------------------------------------------
  Category                         Layer               When Detected         Trace Generated?
  -------------------------------- ------------------- --------------------- ----------------------------------------------
  1. Governance Violation         Authoring / Build   Build time            No --- failure prevents execution

  2. Binding Resolution Failure   CC_ Pipeline       Pre-dispatch          Yes --- trace records the resolution failure

  3. Execution Failure            CT_ or CS_        During dispatch       Yes --- trace records the step failure

  4. Structural Violation         DAG / Routing       During traversal      Yes --- trace records the routing failure
  -------------------------------------------------------------------------------------------------------------------------

These categories classify failures by architectural layer, not by domain semantics. Domain-level errors (e.g., "insufficient funds," "duplicate registration") still manifest as one of these four structural classes --- typically as a Category 3 execution failure with a domain-classified result_status.

The ordering is not arbitrary. Category 1 is caught earliest (before execution begins). Category 4 is caught latest (during DAG traversal). The progression follows the execution pipeline from authoring through compilation through dispatch through routing. A failure detected at an earlier layer never reaches a later layer.

### Category 1 --- Governance Violations

Governance violations are caught at build time --- before any runtime execution occurs. The builder validates governance artifacts against constitutional schemas, vocabulary constraints, and referential integrity rules. A governance violation means: the artifact is structurally malformed and cannot be compiled into an executable protocol.

**When detected:** During `build.py` execution or constitutional validation.

**Trace generated:** No. The system never reaches execution. There is no runtime trace because there is no runtime. The builder produces a structured diagnostic instead.

**Diagnostic model:**

    BuildError:
      phase:         "validate"
      severity:      ERROR | FATAL
      message:       Human-readable description
      file_path:     Source artifact path
      violated_rule: Constitutional reference (e.g., CONSTITUTION_VOCABULARY_V0.result_status)

**Error sources:**

  -----------------------------------------------------------------------------------
  Check                   Example Failure
  ----------------------- -----------------------------------------------------------
  Schema validation       Required field missing, wrong type

  Vocabulary validation   Result status not in constitutional vocabulary

  Prefix validation       Artifact code uses wrong prefix for its type

  Referential integrity   CC_ references CT_ code that does not exist in registry

  Constitutional rules    CT_PURE atom contains forbidden opcode (ENGINE_000)
  -----------------------------------------------------------------------------------

### Example 8.1 --- Vocabulary Violation at Build Time

A capability contract declares `result_status: "OK"` in its binding *(see Appendix B, Example 8.1)*.

The builder rejects:

    BUILD ERROR
      Phase:         validate
      Severity:      ERROR
      Artifact:      CC_PROVISION_USER_V0
      File:          governance/registry/capability_contracts/cc_provision_user_v0.md
      Check:         Vocabulary validation
      Detail:        Unknown result_status "OK" not in constitutional vocabulary.
                     Allowed: SUCCESS, VIOLATION, BACKEND_ERROR, NOT_FOUND,
                     ALREADY_EXISTS, ACK, NACK
      Violated Rule: CONSTITUTION_VOCABULARY_V0.result_status
      Resolution:    Replace "OK" with "SUCCESS" and "FAIL" with "VIOLATION"

**Analysis:**

- **The failure never reaches execution.** No runtime is started. No trace is generated. No partial side effects occur. The artifact is rejected at the gate.
- **The diagnostic names the violation precisely.** It identifies the artifact, the field, the invalid value, the constitutional rule that was violated, and the allowed alternatives. An author reads one diagnostic and knows exactly what to fix.
- **The vocabulary is constitutional.** "OK" is not wrong because a linter flags it. It is wrong because the constitution defines the allowed result statuses and "OK" is not among them. The vocabulary boundary is a structural fact, not a style preference.

### Category 2 --- Binding Resolution Failures

Binding resolution failures occur during CC_ pipeline execution --- after artifacts have been loaded and validated, but before CT_ or CS_ steps are dispatched. The expression resolver attempts to satisfy input bindings from the pipeline state. When a required binding resolves to None, the step cannot execute.

**When detected:** During `resolve_inputs()` in the capability pipeline.

**Trace generated:** Yes. The pipeline was executing. The trace records the step at which resolution failed.

**Diagnostic model:** The pipeline returns the CC_ artifact's declared `on_input_failure` status (typically VIOLATION) and records the failed input name.

**Error sources:**

  ------------------------------------------------------------------------------------------------------
  Check                       Example Failure
  --------------------------- --------------------------------------------------------------------------
  Payload field missing       `$.inputs.employee_id` --- field not in workflow payload

  Prior step output missing   `$.results.CT_STEP.field` --- prior step did not produce expected output

  CS_ code not registered    Capability router cannot find runtime for CS_ code

  Nested dict resolution      Inner expression `$.inputs.nested.field` resolves to None
  ------------------------------------------------------------------------------------------------------

### Example 8.2 --- Missing Payload Field

A CC_ pipeline step binds its input to a payload field that was not provided *(see Appendix B, Example 8.2)*.

The workflow is invoked with a payload that contains `actor_id` but not `employee_id`. The expression resolver returns None for `$.inputs.employee_id`. The pipeline cannot dispatch the CT_ step.

    CC PIPELINE FAILURE
      Contract:     CC_ONBOARD_EMPLOYEE_V0
      Step:         CT_PURE_GENERATE_ID_V0
      Check:        Input resolution
      Failed Input: employee_id
      Expression:   $.inputs.employee_id
      Detail:       Expression resolved to None. Field "employee_id" not found
                    in pipeline inputs.
      Result:       VIOLATION (from result_status_contract.on_input_failure)
      Resolution:   Verify the workflow payload includes "employee_id", or
                    update the CC_ binding to reference the correct field name.

**Analysis:**

- **The failure occurs before dispatch.** The CT_ atom is never invoked. No computation occurs. No side effects execute. The pipeline detects the unresolvable binding and routes to the declared failure status.
- **The routing is governance-declared.** The CC_ artifact's `result_status_contract` specifies `on_input_failure: "VIOLATION"`. This is not a default --- it is a declared governance decision. A different CC_ might declare `on_input_failure: "BACKEND_ERROR"` if that classification is more appropriate for its domain.
- **The trace records the failure point.** The execution trace shows which step failed, which input could not be resolved, and which expression was attempted. An operator reads the trace and knows: the payload is missing a field.

The boundary between Category 2 and Category 3 is precise: if a step cannot be invoked, it is Category 2. If a step is invoked and fails during execution, it is Category 3.

### Category 3 --- Execution Failures

Execution failures occur during CT_ or CS_ dispatch --- the step was reached, inputs were resolved, but the computation or side effect failed during execution.

**When detected:** During `execute_ct()` or CS_ runtime `execute()`.

**Trace generated:** Yes. The trace records the failing step, the operation, and the classified result status.

**CT_ failures:** An atom raises an exception during execution. The pipeline catches `CTExecutionError` and maps it to the binding's `on_ct_result.on_failure` status (typically VIOLATION). The CT_ itself does not know about result statuses --- the pipeline performs the mapping.

**CS_ failures:** The runtime's `execute()` method returns a result with a non-SUCCESS `result_status`. The status is domain-classified: NOT_FOUND, ALREADY_EXISTS, VIOLATION, or BACKEND_ERROR. The CC_ pipeline routes on this status via the binding's `on_result` declaration.

### Example 8.3 --- Registry Collision (CS_ Failure)

A CS_REGISTRY_V0 REGISTER operation encounters a key that already exists:

    CC PIPELINE STEP
      Contract:    CC_REGISTER_ACTOR_KYC_V0
      Step:        CS_ACTOR_ALIAS_INDEX_V0
      Operation:   REGISTER
      Inputs:      {key: "KYC_8a4c1d9e", target_cs: "CS_ACTOR_STATE_V0",
                    target_ref: "AC_7f3a2b"}
      Result:      {result_status: "ALREADY_EXISTS",
                    address: "ADDR_f91b3c"}
      Routing:     ALREADY_EXISTS → continue

**Analysis:**

- **The failure is domain-classified.** The registry runtime returns ALREADY_EXISTS --- not a generic error code, but a specific semantic classification that tells the pipeline exactly what happened. The pipeline routes on this classification.
- **The routing may not terminate.** In this example, `ALREADY_EXISTS → continue` means the pipeline proceeds. This is a governance decision: the CC_ author decided that a duplicate registration is acceptable, not fatal. A different CC_ might declare `ALREADY_EXISTS → exit` if duplicates are violations.
- **The trace records the CS_ result.** The operation, inputs, and result_status are all visible. An auditor can determine that the registration was attempted, what key was used, and that the key already existed --- without reading runtime code.

### Example 8.4 --- CT_ Atom Exception

A CT_PURE atom raises during execution because the input data violates an internal invariant:

    CC PIPELINE STEP
      Contract:    CC_DERIVE_ADDRESS_V0
      Step:        CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
      Operation:   PRIVATE_KEY_TO_PUBLIC
      Inputs:      {private_key_bytes: "<32 bytes>", curve: "invalid_curve"}
      CT Result:   CTExecutionError("Unsupported curve: invalid_curve")
      Mapped To:   {value: null, result_status: "VIOLATION"}
      Routing:     VIOLATION → exit

**Analysis:**

- **CT_ failure is mapped, not propagated.** The atom raises a Python exception. The pipeline catches it and maps to the binding's `on_ct_result.on_failure` status. The exception does not escape to the workflow layer as an unhandled error --- it becomes a classified protocol result.
- **The mapping is governance-declared.** `on_failure: "VIOLATION"` is written in the CC_ artifact. The pipeline does not invent status codes at runtime. It applies the declared mapping.

### Category 4 --- Structural Violations

Structural violations occur during DAG traversal --- the workflow executor cannot route to the next node because the graph structure does not support the current execution state.

**Invariant I-F0 --- Graph Completeness:** A workflow must declare transitions for all result statuses its capability contracts permit. An undeclared transition is a governance defect, not a runtime anomaly.

**When detected:** During workflow runner's node traversal loop.

**Trace generated:** Yes. The trace records the failing node and the routing failure.

**Error sources:**

  ---------------------------------------------------------------------------------------------------------
  Check           Exit Reason Code                     Example
  --------------- ------------------------------------ ----------------------------------------------------
  No entry node   NO_ENTRY_NODE                        DAG has no start node

  Missing node    NODE_NOT_FOUND                       Edge references non-existent node ID

  No transition   NO_TRANSITION                        No edge declared for current result_status

  Unmapped exit   GOVERNANCE_VIOLATION                 Exit node receives status not in _EXIT_REASON_MAP
  ---------------------------------------------------------------------------------------------------------

### Example 8.5 --- Missing Transition

Node N003 (CC_PERSIST_RECORD_V0) returns BACKEND_ERROR, but no outgoing edge is declared for that status:

    WORKFLOW FAILURE
      Workflow:        WF_ONBOARD_EMPLOYEE_V0
      Current Node:    N003 (CC_PERSIST_RECORD_V0)
      Result Status:   BACKEND_ERROR
      Check:           Transition lookup
      Detail:          No outgoing edge from N003 for result_status "BACKEND_ERROR".
                       Declared edges: SUCCESS → N004, VIOLATION → EXIT_FAILED
      Exit Reason:     NO_TRANSITION
      Resolution:      Add an edge from N003 for BACKEND_ERROR in the workflow
                       specification. Route to an appropriate exit node.

**Analysis:**

- **The graph is incomplete.** The workflow author declared edges for SUCCESS and VIOLATION but forgot BACKEND_ERROR. The CC_ step can produce this status (it is in the result_status_contract), but the workflow has no edge for it. The execution cannot continue because there is no declared path.
- **The failure is not a runtime bug.** It is a governance incompleteness --- the workflow specification does not handle all possible outcomes of its capability contracts. This is detectable at build time by comparing CC_ result_status_contracts against workflow edge declarations.
- **The exit reason is constitutional.** NO_TRANSITION is a member of the constitutional exit_reason_code vocabulary. The workflow runner does not invent exit reasons --- it selects from a frozen governance-declared set.

### Comparative Case Study --- A Payment Processing Failure

Consider the same failure in both architectures: a payment service attempts to persist a transaction record, but the database connection is unavailable.

**Application-Centric:** The ORM throws a `ConnectionRefusedError`. A retry decorator catches it, waits, retries three times, then raises a `ServiceUnavailableException`. The calling service catches that, logs a message at WARN level, and returns HTTP 503. The API gateway retries the entire request. The payment may or may not have been partially committed --- it depends on whether the ORM flushed before the connection dropped. The engineering team investigates by correlating timestamps across three services' logs, checking database transaction logs, and reasoning about retry timing. Time to diagnosis: hours to days.

**Protocol-Governed:** The CS_ adapter returns `BACKEND_ERROR`. The CC_ pipeline maps this to the declared `on_result` status. The workflow follows the `BACKEND_ERROR` edge to the declared exit node. The trace records the exact step, the exact status, the exact exit reason, and the exact payload state at the point of failure. No partial commit is possible --- the CS_ step either succeeds completely or returns a classified error (the Structural Invariance Principle's mutation-is-declared guarantee). Time to diagnosis: the trace record is the diagnosis.

The difference is not tooling. It is structural. In the first case, the failure manifests across layers, services, and time --- diagnosis requires reconstruction. In the second case, the failure is classified at the point of occurrence --- diagnosis requires inspection.

## 8.3 --- The Structured Error Model

All errors in PGS carry structural metadata --- not just a message string, but a classified error code and a layer attribution.

**The StructuredError base class:**

    class StructuredError(RuntimeError):
        error_code:    str   # Constitutional error code (e.g., EXPRESSION_RESOLUTION_FAILED)
        node_category: str   # Layer attribution: WF, IN, CC, CT, or CS
        message:       str   # Human-readable description
        cause:         Exception  # Original exception if wrapping unstructured error

**Error Code Vocabulary** (from SCHEMA_TRACE_EVENT_V0):

  -------------------------------------------------------------------------------------------------
  Code                           Layer                  Meaning
  ------------------------------ ---------------------- -------------------------------------------
  EXPRESSION_RESOLUTION_FAILED   CC                     JSONPath expression could not be resolved

  BINDING_RESOLUTION_FAILED      CC                     Input binding could not be satisfied

  SCHEMA_VALIDATION_FAILED       CC                     Schema conformance check failed

  CT_VALIDATION_FAILED           CT                     CT-IR validation rejected the transform

  CT_EXECUTION_FAILED            CT                     CT atom raised during execution

  CT_ARTIFACT_NOT_FOUND          CT                     CT code not in transform registry

  CS_EXECUTION_FAILED            CS                     CS runtime returned error status

  CAPABILITY_NOT_FOUND           CC                     CS code not in capability registry

  CAPABILITY_DISPATCH_FAILED     CC                     Pipeline could not dispatch step

  NODE_NOT_FOUND                 WF                     DAG references non-existent node

  INTENT_NOT_FOUND               IN                     Intent specification missing

  PROTOCOL_LOAD_FAILED           WF                     Artifact loading error

  EXECUTION_ERROR                WF                     Generic execution failure

  ADMISSION_DENIED               WF                     Admission precondition not met
  -------------------------------------------------------------------------------------------------

**Node Category Attribution:**

Every error identifies the layer where it originated --- WF (workflow), IN (intent), CC (capability contract), CT (capability transform), or CS (capability side effect). This attribution is not a tag added after the fact. It is a required field on every StructuredError, set at the point of failure. When the trace records an error event, the `node_category` tells the operator which layer to investigate --- without reading a stack trace.

**Wrapping Unstructured Exceptions:**

When a CT_ atom or CS_ runtime raises an ordinary Python exception (not a StructuredError), the pipeline wraps it with the layer where the failure was detected:

    except Exception as e:
        wrapped = StructuredError(
            error_code="EXECUTION_ERROR",
            node_category=detected_layer,  # CT, CS, CC, or WF — set at the catch site
            message=str(e),
            cause=e,
        )

The `node_category` is set at the point where the exception is caught --- a CT_ atom failure is attributed to "CT", a CS_ runtime failure to "CS", a pipeline-level failure to "CC". No exception escapes the pipeline unclassified. Every failure --- structured or unstructured --- is normalized into the constitutional error model before it reaches the trace emitter.

## 8.4 --- Result Status Contracts

The CC_ artifact declares which result statuses are possible. This declaration is not documentation --- it is a constitutional contract that the builder validates and the pipeline enforces.

*(The full artifact is provided in Appendix B, Example 8.5.)*

**What the contract governs:**

1.  **Allowed statuses.** Only statuses in the `allowed` array may appear in the CC_ result. Each must be a member of the constitutional vocabulary. The builder rejects unknown statuses at compile time (Example 8.1).

2.  **Input failure routing.** When `resolve_inputs` fails, the pipeline returns the `on_input_failure` status. This status must be in the `allowed` array. The author declares how unresolvable inputs are classified --- VIOLATION, BACKEND_ERROR, or another appropriate status.

3.  **Per-step routing.** Each binding's `on_result` declaration maps result statuses to pipeline actions (continue or exit). Every status that a step can produce should have a declared route. Missing routes cause implicit exits --- a governance gap that the builder can detect.

4.  **Edge completeness.** The builder validates that every allowed result_status appears in at least one workflow edge or explicitly routes to an exit node. A CC_ that can produce BACKEND_ERROR but whose workflow declares no edge for that status is a governance deficiency --- flagged before runtime.

**Exit Reason Mapping:**

When a workflow reaches an exit node, the workflow runner maps the last `result_status` to an `exit_reason_code` through a frozen governance table:

  --------------------------------------
  Result Status    Exit Reason Code
  ---------------- ---------------------
  SUCCESS          COMPLETED

  ACK              COMPLETED

  VIOLATION        EXIT_VIOLATION

  BACKEND_ERROR    EXIT_BACKEND_ERROR

  NOT_FOUND        EXIT_NOT_FOUND

  ALREADY_EXISTS   EXIT_ALREADY_EXISTS

  NACK             EXIT_REJECTED
  --------------------------------------

This table is frozen in the workflow runner --- not configurable per workflow. If a result_status has no entry in the map, the exit reason is classified as GOVERNANCE_VIOLATION. An unmapped exit status is itself a failure --- the system does not invent classifications at runtime.

## 8.5 --- Validation and Failure Surface

This chapter's failure surface is meta: it concerns failures about failures --- incomplete failure handling in governance artifacts.

### Failure Path Validation Checks

  -------------------------------------------------------------------------------------------------------
  Step          Check                      Failure Condition
  ------------- -------------------------- --------------------------------------------------------------
  1             Result status vocabulary   Status string not in CONSTITUTION_VOCABULARY_V0

  2             on_result completeness     CC_ binding missing route for a status the step can produce

  3             Edge completeness          Workflow has no edge for a CC_ result status

  4             Exit reason mapping        Result status has no entry in _EXIT_REASON_MAP

  5             Error code conformance     StructuredError uses code not in SCHEMA_TRACE_EVENT_V0
  -------------------------------------------------------------------------------------------------------

### Broken Example: Incomplete Failure Routing

A CC_ binding declares `on_result` for SUCCESS and VIOLATION but omits BACKEND_ERROR *(see Appendix B, Example 8.6)*.

The CS_ runtime returns `result_status: "BACKEND_ERROR"`. The pipeline looks up the routing action:

    action = binding.get("on_result", {}).get("BACKEND_ERROR")
    # action is None — no declared route

The pipeline treats an undefined route as an implicit exit --- but this is a governance gap. The CC_ author did not declare what should happen on BACKEND_ERROR. The builder can detect this gap by comparing the CS_ runtime's possible statuses against the declared `on_result` keys.

    BUILD WARNING
      Phase:         validate
      Severity:      WARNING
      Artifact:      CC_PERSIST_WALLET_V0
      Step:          CS_WALLET_STATE_V0
      Check:         on_result completeness
      Detail:        CS_MUTABLE_JSON_V0 can return BACKEND_ERROR, but
                     CS_WALLET_STATE_V0 binding declares no on_result route
                     for this status. Pipeline will treat as implicit exit.
      Resolution:    Add "BACKEND_ERROR": "exit" to the on_result declaration
                     to make the failure path explicit.

**This section proves:** PGS validates its own failure paths. Incomplete failure routing is a governance deficiency --- detectable, classifiable, and correctable before runtime. The system does not wait for a production incident to discover that a failure path was never declared.

## 8.6 --- Structural Insight (Doctrine Moment)

The reader has seen four failure categories, each with distinct diagnostic signatures, classified error codes, and trace records. At no point did failure require reading source code, reproducing an environment, or guessing at hidden state. The trace identified the layer. The error code identified the class. The artifact identified the root cause.

This is Chapter 2's **Property 5 --- Observable Execution** extended to failure. Observability in PGS is not about logging --- it is about structural completeness. Every step is traced. Every failure is classified. Every classification is constitutional.

**Invariant I-F1 --- Deterministic Failure Signature:** Given identical governance artifacts, runtime bindings, and payload, the same failure occurs at the same step with the same classification. This is not a testing aspiration --- it is a structural consequence of deterministic execution (Chapter 5), pure computation (Chapter 6), and declared mutation (Chapter 7). If the artifacts do not change and the payload does not change, the execution path does not change --- and neither does the failure.

**Invariant I-F2 --- Trace Sufficiency:** The execution trace contains enough information to identify the failing artifact, the failing layer, the failure class, and the structural cause --- without source code inspection. The trace records: which node executed, what inputs were bound, what result_status was returned, what error_code was emitted, and what exit_reason_code terminated the workflow. This is not a log file that might contain useful information. It is a schema-validated record that must contain this information --- the trace schema is constitutional.

**Invariant I-F3 --- No Silent Repair:** The system may not auto-correct schema mismatches, substitute missing bindings, suppress failed CS_ operations, or retry without explicit declaration. Silent repair is the most dangerous failure mode in application-centric systems --- the system "fixes" a problem without telling anyone, creating the illusion of correctness while accumulating hidden divergence. PGS prohibits this constitutionally: every failure emits a structured event, is classified by error code, and terminates through a declared governance path. There is no catch-and-swallow. There is no fallback-to-default. There is no "close enough."

> **[DIAGRAM 5] --- The Failure Classification Chain**

     Failure Occurs
          |
          v
     Failure Origin Layer?
          |
          +-- Build-time ---------> Category 1: Governance Violation
          |                              (BuildError, no trace)
          |
          +-- Input Resolution ---> Category 2: Binding Resolution
          |                              (on_input_failure, trace records step)
          |
          +-- CT/CS Dispatch -----> Category 3: Execution Failure
          |                              (error_code + result_status, trace records op)
          |
          +-- DAG Traversal ------> Category 4: Structural Violation
                                         (exit_reason_code, trace records node)

> Every failure enters this chain at exactly one point. The layer determines the category. The category determines the diagnostic format. There is no "uncategorized" failure. An uncategorized failure is itself a structural violation --- Category 4.

**Structural impossibility:** The execution engine cannot swallow a failure, reclassify a failure into a different category, or repair a failure. Every exception is either a StructuredError (already classified) or is wrapped into one before reaching the trace emitter. The wrapping preserves the original cause while adding constitutional metadata. No failure exits the pipeline without a classification.

## 8.7 --- Solved Problems

### Problem 8.1 --- "Works on My Machine"

**Scenario:** A workflow succeeds in development but fails in staging. The teams spend three days comparing environment configurations.

**Application-Centric Approach:** The service reads configuration from environment variables, pulls secrets from a vault, connects to environment-specific databases, and loads feature flags from a remote service. The failure in staging is caused by a missing environment variable that the development environment provides through a .env file that is not committed to version control. Diagnosis requires comparing .env files, vault configurations, database schemas, and feature flag states across environments. The root cause is invisible because the dependency on that environment variable is implicit --- buried in a constructor that reads `os.getenv()`.

**PGS Approach:** 1. Governance artifacts are versioned and identical across environments. 2. Runtime bindings declare all external dependencies explicitly --- storage paths resolved through `{{module_data_root}}`, not implicit environment variables. 3. The same payload + the same artifacts = the same execution path on any machine. 4. If the binding references a path that does not exist in staging, the CS_ runtime returns BACKEND_ERROR at the exact step where the path was accessed. The trace names the step, the operation, and the storage path. The operator reads one trace event and knows: this path does not exist in staging.

**Eliminated pathology:** Environment-dependent failure behavior. Execution determinism is not a property of the environment --- it is a property of the architecture. The artifacts govern behavior. The environment provides only the parameters that the bindings explicitly declare.

### Problem 8.2 --- Ghost Failures (Non-Reproducible Bugs)

**Scenario:** A production workflow fails intermittently. The failure is logged, but running the same request again succeeds. The team cannot reproduce the failure in any environment.

**Application-Centric Approach:** The service depends on a cache that is populated by a background job. When the cache is warm, the request succeeds. When the cache entry expires between the lookup and the computation, the request fails. The failure is a race condition between the request thread and the cache eviction thread. Reproducing it requires exact timing that no test harness can reliably create. The team adds a retry loop and moves on. The race condition remains --- it just fails less often.

**PGS Approach:** 1. CT_ atoms are pure --- no caches, no background jobs, no race conditions. Given the same inputs, they produce the same outputs. Always. 2. CS_ runtimes operate on declared storage with atomic operations. There is no background eviction. There is no cache warming. The storage state at the time of execution is the storage state. 3. If a CS_ step fails (e.g., NOT_FOUND because a prior workflow has not yet registered the expected record), the trace records exactly which step failed, what key was looked up, and what status was returned. Replaying the same payload against the same storage state reproduces the same failure --- deterministically. 4. The "ghost" disappears because the conditions that create ghosts --- hidden mutable state, background jobs, cache timing --- do not exist in the execution model.

**Eliminated pathology:** Non-deterministic failure behavior (Heisenbugs). PGS execution is deterministic by construction. CT_ is pure. CS_ operates on declared state. The trace records the execution path. Replay with identical inputs and identical state produces identical results --- including identical failures.

### Problem 8.3 --- Silent Partial Mutation

**Scenario:** A service method writes to two databases in sequence. The first write succeeds. The second fails. The service catches the exception and returns an error --- but the first write has already committed. The system is in an inconsistent state that no one detects until a downstream consumer encounters the orphaned record.

**Application-Centric Approach:** The team adds a transaction wrapper. But the two databases are different systems --- distributed transactions are not supported. The team adds a cleanup job. The cleanup job has its own failure modes. The compensating logic is more complex than the original operation. Six months later, the cleanup job has a bug that deletes records it should not. The original problem --- silent partial mutation --- has metastasized into a secondary system with its own failure modes.

**PGS Approach:** 1. Each CS_ step in the CC_ pipeline is an independent, declared mutation with explicit result routing. 2. The trace records the result_status of every step. If step 1 succeeds (result_status: SUCCESS) and step 2 fails (result_status: BACKEND_ERROR), the trace shows both results. 3. The pipeline terminates at step 2 because the binding declares `"BACKEND_ERROR": "exit"`. Step 3 does not execute. The partial state is visible --- not hidden. 4. Compensating logic, if needed, is itself a declared workflow --- governed, traced, and auditable. It is not a background job with hidden failure modes.

**Eliminated pathology:** Undetected inconsistent state. Every CS_ step's outcome is traced. Partial mutation is visible by reading the trace. The system does not silently leave inconsistent state --- it explicitly records which mutations succeeded, which failed, and where execution stopped.

### Problem 8.4 --- Debugging by Guessing

**Scenario:** A production failure requires diagnosis. The on-call engineer has never seen this workflow before.

**Application-Centric Approach:** The engineer reads the stack trace. It points to a line in a service class. The engineer reads the service class --- it calls three other services. The engineer reads those services --- each has its own dependencies. The call chain is four levels deep. The engineer sets up a debugger, reproduces the request in a staging environment, and steps through the code. Two hours later, the engineer discovers that a helper function deep in the call chain is reading from a database table that was migrated last week. The migration changed a column name. The helper function's query was not updated.

**PGS Approach:** 1. The engineer opens the execution trace. The trace header shows `exit_reason_code: "EXIT_BACKEND_ERROR"`. 2. The engineer scans the trace for the last `node_end` event with a non-SUCCESS status. It shows: `node: N003, capability: CC_PERSIST_RECORD_V0, step: CS_RECORD_STATE_V0, result_status: BACKEND_ERROR`. 3. The engineer opens the RB_ artifact. CS_RECORD_STATE_V0 is bound to `MutableJsonRuntime` with path `{{module_data_root}}/record_state.json`. 4. The engineer checks the path. The file does not exist --- the data directory was not provisioned in this environment. 5. Total diagnosis time: five minutes. No source code reading. No debugger. No environment reproduction.

**Eliminated pathology:** Interpretive debugging. The trace provides structural diagnosis --- layer, step, operation, and status. The artifact provides the root cause --- the binding references a path that does not exist. The engineer does not guess. The engineer reads.

## 8.8 --- Generated Output: Trace-Based Diagnosis Workflow

The execution trace is the diagnostic instrument. This section demonstrates a complete diagnosis from trace to root cause.

### Failed Execution Trace: WF_REGISTER_ACTOR_UNVERIFIED_V0

A workflow execution fails during actor registration. The operator receives only the trace.

    TRACE: WF_REGISTER_ACTOR_UNVERIFIED_V0
      execution_id: exec_2026_02_23_001
      exit_condition: FAILURE
      exit_reason_code: EXIT_VIOLATION

      EVENT 1: execution_start
        workflow: WF_REGISTER_ACTOR_UNVERIFIED_V0
        timestamp: 2026-02-23T10:00:00.000Z
        payload: {actor_record: {first_name: "Ada", last_name: "Lovelace",
                  email_registration: "ada@example.com"}}

      EVENT 2: node_start
        node_id: N001
        node_type: intent
        capability_code: IN_REGISTER_ACTOR_V0

      EVENT 3: node_end
        node_id: N001
        result_status: ACK

      EVENT 4: node_start
        node_id: N002
        node_type: capability_contract
        capability_code: CC_GENERATE_ACTOR_ID_V0

      EVENT 5: node_end
        node_id: N002
        result_status: SUCCESS

      EVENT 6: node_start
        node_id: N003
        node_type: capability_contract
        capability_code: CC_REGISTER_ACTOR_KYC_V0

      EVENT 7: capability_dispatch
        cc_code: CC_REGISTER_ACTOR_KYC_V0
        step: CT_PURE_GENERATE_ID_V0
        op: GENERATE_ID

      EVENT 8: transform_end
        step: CT_PURE_GENERATE_ID_V0
        result_status: SUCCESS

      EVENT 9: capability_dispatch
        cc_code: CC_REGISTER_ACTOR_KYC_V0
        step: CS_ACTOR_ALIAS_INDEX_V0
        op: REGISTER

      EVENT 10: side_effect_end
        step: CS_ACTOR_ALIAS_INDEX_V0
        result_status: ALREADY_EXISTS

      EVENT 11: node_end
        node_id: N003
        result_status: ALREADY_EXISTS

      EVENT 12: node_start
        node_id: EXIT_FAILED
        node_type: exit
        exit_reason: FAILED

      EVENT 13: workflow_complete
        exit_condition: FAILURE
        exit_reason_code: EXIT_ALREADY_EXISTS

      EVENT 14: error
        error_code: CS_EXECUTION_FAILED
        node_category: CS
        node_id: N003
        message: "Registry key KYC_8a4c1d9e already exists"

### Diagnosis Walkthrough

**Step 1 --- Read the trace header.**

`exit_condition: FAILURE`, `exit_reason_code: EXIT_ALREADY_EXISTS`. The workflow failed because something already existed.

**Step 2 --- Locate the failing node.**

Scan for the last `node_end` with a non-SUCCESS status: Event 11 --- `node: N003, capability: CC_REGISTER_ACTOR_KYC_V0, result_status: ALREADY_EXISTS`.

**Step 3 --- Identify the failing step within the CC_ pipeline.**

Event 10 --- `step: CS_ACTOR_ALIAS_INDEX_V0, result_status: ALREADY_EXISTS`. The CT_ step succeeded (Event 8). The CS_ step failed with ALREADY_EXISTS.

**Step 4 --- Classify the failure.**

Layer: CS_ (side effect). Category: **Category 3 --- Execution Failure**. The CS_ runtime executed and returned a classified status.

**Step 5 --- Identify the structural root cause.**

The registry already contains key `KYC_8a4c1d9e`. This means: an actor with the same first_name, last_name, and email_registration was previously registered. The deterministic ID generation (CT_PURE_GENERATE_ID_V0 with prefix "KYC" and the same data) produces the same key every time. The duplicate is not a bug --- it is a re-registration attempt.

**Step 6 --- Determine the resolution.**

Two options, both governance-level: - If duplicate registration should be allowed: change the CC_ binding's `on_result` to route `ALREADY_EXISTS → continue`. - If duplicate registration should be prevented: add admission logic that checks for prior registration events before allowing the workflow.

**Diagnosis complete.** No source code was read. No debugger was attached. No environment was reproduced. The trace identified the layer (CS_), the step (CS_ACTOR_ALIAS_INDEX_V0), the operation (REGISTER), the key (KYC_8a4c1d9e), and the status (ALREADY_EXISTS). The resolution is a governance decision --- not a code fix.

### The Reconstructability Property

**Invariant I-F4 --- Runtime Independence:** Any execution --- success or failure --- can be reconstructed from governance artifacts (versioned), runtime bindings, payload, and trace. The original runtime instance is not required.

**Reconstruction procedure:**

1.  Copy the versioned governance artifacts to a clean environment.
2.  Apply the same RB_ bindings with equivalent storage.
3.  Replay the same payload.
4.  Observe: the same failure occurs at the same step with the same classification.

This is not a theoretical property. It is a structural consequence of three architectural guarantees:

- **Deterministic execution** (Chapter 5): the DAG traversal is determined by the workflow specification and the payload --- not by runtime state.
- **Pure computation** (Chapter 6): CT_ atoms produce identical outputs from identical inputs --- no hidden state, no ambient context.
- **Declared mutation** (Chapter 7): CS_ runtimes operate on declared storage with classified results --- no implicit transactions, no background state.

Together, these guarantees mean: the execution path is a function of (artifacts, bindings, payload). Remove any hidden variable from the equation and reconstructability follows by construction.

Reconstructability assumes identical storage state at replay time. If storage has evolved between the original execution and the replay (e.g., a registry entry was added by a subsequent workflow), the CS_ results may differ --- but the difference is explainable by trace-comparable state divergence, not by hidden runtime behavior. The failure category and diagnostic path remain deterministic; only the CS_ result values may change with storage state.

## 8.9 --- Boundary and Forward Pointer

This chapter proved that failure in PGS is a first-class architectural construct --- classified, deterministic, trace-complete, and reconstructable. It proved that the four failure categories (governance violations, binding resolution failures, execution failures, and structural violations) are exhaustive and mutually exclusive. It proved that the Reconstructability Property follows from the architectural guarantees established in Chapters 5 through 7.

Together with Chapters 5 through 7, this completes the execution model:

- **Chapter 5:** Semantic-agnostic execution --- the engine traverses a governed DAG
- **Chapter 6:** Pure computation --- atoms and molecules execute deterministically
- **Chapter 7:** Controlled mutation --- side effects are declared, bound, and traced
- **Chapter 8:** Governed failure --- every failure is classified, traced, and reconstructable

**What this chapter did not cover:**

- Observability dashboards and operational alerting infrastructure
- SRE practices and incident response procedures
- Distributed failure correlation across federated domains (Chapter 11)
- Compensating transactions and saga patterns for multi-step rollback
- Trace cryptographic chaining and tamper-evidence (Chapter 9)
- Trace schema structure and the trace examiner tool (Chapter 9)

**What comes next:** Chapter 9 --- Deterministic Traces as First-Class Artifacts. This chapter diagnosed failures by reading execution traces. Chapter 9 examines the trace itself --- its schema, its cryptographic chaining, its tamper-evidence properties, and why it is a governed artifact, not a log file. The trace that served as a diagnostic instrument in this chapter will be shown to be a constitutional artifact in its own right.

## 8.10 --- Review Questions

1.  **What distinguishes a governance violation (Category 1) from a binding resolution failure (Category 2)?**

- *A governance violation is detected at build time --- the artifact fails constitutional validation before any runtime execution occurs. No trace is generated. A binding resolution failure is detected at runtime during CC_ pipeline input resolution --- the artifact is valid, but the execution state does not satisfy the input bindings. A trace is generated. The key distinction is timing: build-time vs. runtime, and whether a trace exists.*

2.  **Why can PGS failures be replayed deterministically?**

- *Because execution is a function of (artifacts, bindings, payload) --- not of hidden runtime state. CT_ atoms are pure (same inputs, same outputs). CS_ runtimes operate on declared storage. DAG traversal follows the compiled graph. If none of these inputs change, the execution path does not change --- and neither does the failure. There are no caches, background jobs, race conditions, or thread-local variables that could alter the outcome.*

3.  **What enables runtime-independent failure reconstruction?**

- *The Reconstructability Property (I-F4): governance artifacts are versioned and immutable, runtime bindings are declarative, and the payload is the complete input. Copy the artifacts to a clean environment, apply equivalent bindings, replay the payload, and the same failure occurs at the same step with the same classification. The original runtime instance --- its JVM, its connection pool, its cached state --- is not needed.*

4.  **What does "no silent repair" (I-F3) prevent?**

- *It prevents the system from creating the illusion of correctness by hiding failures. Auto-correcting a schema mismatch, substituting a default for a missing binding, suppressing a CS_ error, or retrying without declaration --- each creates hidden divergence between governed intent and actual behavior. Silent repair is the most dangerous failure mode because it looks like success. I-F3 ensures that every failure is emitted, classified, and routed through a declared governance path.*

5.  **How does the result_status_contract ensure failure paths are complete?**

- *The CC_ artifact declares which result statuses are allowed. Each status must be in the constitutional vocabulary (validated at build time). Each binding's on_result declaration maps statuses to pipeline actions (continue or exit). The builder can detect gaps --- a CS_ runtime that can return BACKEND_ERROR but a binding that only routes SUCCESS and VIOLATION. Incomplete routing is a governance deficiency, not a runtime surprise.*

6.  **Why is failure classification an architectural property rather than an operational practice?**

- *Because the classification is determined by the layer at which the failure occurs --- build (Category 1), resolution (Category 2), dispatch (Category 3), or routing (Category 4). The layer is determined by the execution model's structure, not by operational tooling. The error codes are constitutional (defined in SCHEMA_TRACE_EVENT_V0). The exit reason codes are frozen in a governance table. Classification is a property of the architecture --- it exists whether or not anyone builds a dashboard to display it.*

7.  **True or False: A CT_ atom failure always terminates the workflow.**

- *False. A CT_ atom failure is mapped to a result_status via the binding's on_ct_result.on_failure declaration (typically VIOLATION). The CC_ pipeline then routes on this status via on_result. If on_result declares "VIOLATION": "exit", the pipeline exits and the workflow routes the CC_ result_status through the DAG. But the DAG may have an edge for VIOLATION that routes to another node --- not necessarily an exit node. The CT_ failure terminates the CC_ pipeline, but the workflow may continue on a different path. Whether the workflow terminates depends on the DAG structure, not on the CT_ failure alone.*
