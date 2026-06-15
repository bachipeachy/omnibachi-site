---
title: Chapter 9 — Deterministic Traces as First-Class Artifacts
date: '2026-03-26'
draft: false
weight: 11
slug: chapter-9-deterministic-traces-as-first-class-artifacts
---

Chapter 8 diagnosed failures by reading execution traces --- inspecting which node failed, what result status was returned, and what exit reason terminated the workflow. At no point did diagnosis require source code or environment reproduction. But Chapter 8 treated the trace as a given. It used the trace without examining the trace itself.

This chapter examines the trace as an artifact. It answers: **What makes an execution trace more than a log file --- and how does its construction guarantee that audit, replay, and forensic diagnosis are architectural properties rather than operational aspirations?**

In application-centric systems, logs are best-effort. They are unstructured, mutable, selectively emitted, and frequently incomplete under stress --- precisely when they matter most. In PGS, the trace is a constitutional obligation: every execution must emit a schema-validated, append-only, cryptographically hash-chained record. The trace cannot be partial. It cannot be tampered with silently. It cannot be omitted. The chapter shows how trace records are structured, how hash chaining creates tamper evidence, and how the Trace Examiner --- a structural introspection tool --- diagnoses failures without re-executing workflows. By the end, the reader will understand why replayability and audit follow from trace construction, not from organizational discipline.

## 9.1 --- The Engineering Objective

Chapter 8 diagnosed failures by reading execution traces. The trace showed which node failed, what step returned a non-SUCCESS status, what error code was emitted, and what exit reason terminated the workflow. At no point did diagnosis require reading source code, reproducing an environment, or guessing at hidden state.

But Chapter 8 treated the trace as a given --- something the engine produced, available for reading. This chapter examines the trace itself. How is it structured? What governs its schema? What prevents tampering? What makes it more than a log file?

**The Task:** Construct a deterministic trace artifact from a workflow execution, validate its structural integrity and tamper evidence, examine it using a structural introspection tool, and prove that replayability and audit guarantees follow from its construction --- not from operational discipline.

**The Constraint:** PGS does not permit narrative logs, partial capture, or mutable execution history. The trace is not an optional debugging aid. It is a constitutional obligation. The governance layer mandates that every execution emits a schema-validated, append-only trace record. The execution engine cannot run a workflow without producing one.

In the application-centric approach, logging is observational, optional, and mutable. A developer adds `logger.info("processing user request")` where it seems useful and removes it when the console gets noisy. Log formats vary by team. Log levels are adjusted at runtime. Log storage is a retention policy decision --- thirty days, ninety days, whatever compliance requires. The logs describe behavior but cannot prove it. A production incident occurs. The team searches logs. Some entries are missing because the log level was set to WARN. Some entries are misleading because the format changed in a deployment three weeks ago. Some entries were never written because the service crashed between the database write and the log call. Logs are side effects of code execution --- they inherit every fragility of the code that emits them.

In PGS, the trace is not a side effect. It is a constitutional artifact. Its schema is governed by SCHEMA_TRACE_EVENT_V0. Its emission is mandated by CONSTITUTION_TRACE_EXECUTION_V0. Its format is JSONL --- one JSON object per line, append-only, no multi-line events. Its integrity is cryptographically chained under the ADVANCED policy. The trace does not describe what happened. It is the structural record of what happened --- machine-verifiable, tamper-evident, and sufficient for deterministic replay.

## 9.2 --- The Execution Trace Record

**Definition:** A trace record is a schema-bound, immutable event emitted during workflow execution, containing structural metadata sufficient for classification, verification, and replay.

**Key Properties:**

1.  **Schema-validated at emission.** Every trace event is validated against SCHEMA_TRACE_EVENT_V0 before it reaches the sink. An event that fails schema validation is not emitted --- it is a constitutional violation. The emitter does not write first and validate later.
2.  **Monotonically sequenced.** Each event carries an integer `sequence` field that increments by one. Gaps are detectable. Reordering is detectable. The sequence is not a timestamp --- it is an ordinal position in the execution history.
3.  **Policy-governed granularity.** The trace depth is controlled by execution policy: MINIMAL emits only structural boundaries (execution start, node start, node end, workflow complete). FULL emits every dispatch, transform, side effect, and context snapshot. The policy is declared in governance --- not chosen at debug time.

### Example 9.1 --- Minimal Trace Record (BASIC Event)

*(The full artifact is provided in Appendix B, Example 9.1.)*

**Analysis:**

- The record is self-describing. `event_type` classifies the event. `sequence` positions it in the chain. `payload` carries exactly the fields that SCHEMA_TRACE_EVENT_V0 requires for a `node_end` event --- no more, no less.
- The record carries no business data. It records that N002 completed with SUCCESS in 12 milliseconds. What N002 computed, what inputs it received, what domain meaning the result carries --- none of this appears. The trace is structurally complete and semantically agnostic.
- The timestamp is ISO-8601 UTC. It is informational --- useful for human readers and operational dashboards. The ordering authority is `sequence`, not `timestamp`. Two events with identical timestamps are still ordered by their sequence numbers.

### Example 9.2 --- ADVANCED Trace Record with Hash Chain

Under the FULL trace depth policy, every event carries a `prev_hash` field that links it to its predecessor *(see Appendix B, Example 9.2)*.

**Analysis:**

- `prev_hash` is the SHA-256 hash (truncated to 16 hex characters) of the previous event's complete JSON serialization. The first event's `prev_hash` is derived from the `execution_id` itself. Every subsequent event hashes its predecessor. The chain is mechanical --- not policy-based.
- `outputs_hash` records a hash of the transform's output, not the output itself. The trace proves that computation occurred and what its structural fingerprint was --- without embedding business data in the trace record.
- Under BASIC policy, the `prev_hash` field is absent. The trace still records structural boundaries but does not provide cryptographic tamper evidence. Hash continuity is a capability of the trace infrastructure that FULL policy activates; BASIC policy omits internal step events and their chaining. The policy choice is a governance decision --- declared in the runtime binding or workflow specification, not toggled at debug time.

## 9.3 --- The Trace Chain

**Definition:** A trace chain is the ordered sequence of all trace records emitted during a single workflow execution, forming a tamper-evident linked structure under ADVANCED policy.

**Key Properties:**

1.  **Deterministic ordering.** Events are sequenced by emission order. The `sequence` field provides the canonical ordering. There is no out-of-order emission --- the trace emitter is synchronous within a single execution.
2.  **Hash continuity (ADVANCED).** Each event's `prev_hash` equals the SHA-256 hash of the preceding event's JSON serialization. Breaking any record in the chain invalidates every subsequent hash. Tampering with a single field in a single record produces a detectable discontinuity.
3.  **Complete coverage.** Every node traversal, every capability dispatch, every transform execution, every side effect operation, and every error is emitted as a trace event. There are no silent steps. The engine cannot execute a node without emitting `node_start` and `node_end`. This is structural --- the emission calls are part of the execution path, not decorators that can be removed.

### Example 9.3 --- Three-Step Trace Chain (Condensed)

A workflow with three nodes produces the following chain under FULL policy:

    Event 1: execution_start
      seq: 1, prev_hash: hash(execution_id)
      payload: {workflow_code: "WF_REGISTER_ACTOR_UNVERIFIED_V0"}

    Event 2: node_start
      seq: 2, prev_hash: hash(Event 1)
      payload: {node_id: "N001", node_type: "intent",
                capability_code: "IN_REGISTER_ACTOR_V0"}

    Event 3: node_end
      seq: 3, prev_hash: hash(Event 2)
      payload: {node_id: "N001", status: "ACK", duration_ms: 1}

    Event 4: node_start
      seq: 4, prev_hash: hash(Event 3)
      payload: {node_id: "N002", node_type: "capability_contract",
                capability_code: "CC_GENERATE_ACTOR_ID_V0"}

    Event 5: capability_dispatch
      seq: 5, prev_hash: hash(Event 4)
      payload: {cc_code: "CC_GENERATE_ACTOR_ID_V0", node_id: "N002"}

    Event 6: transform_end
      seq: 6, prev_hash: hash(Event 5)
      payload: {ct_code: "CT_PURE_GENERATE_ID_V0",
                duration_ms: 2, outputs_hash: "7d1e9f3a2c5b4806"}

    Event 7: node_end
      seq: 7, prev_hash: hash(Event 6)
      payload: {node_id: "N002", status: "SUCCESS", duration_ms: 5}

      ... (N003 events) ...

    Event 14: workflow_complete
      seq: 14, prev_hash: hash(Event 13)
      payload: {status: "SUCCESS", duration_ms: 23,
                exit_condition: "NORMAL",
                exit_reason_code: "COMPLETED"}

**Analysis:**

- The chain forms a linked list through `prev_hash`. Modifying Event 3's `status` from "ACK" to "NACK" changes its JSON serialization, which invalidates Event 4's `prev_hash`. The tampering cascades forward. Removing any event breaks the chain at the next record.
- BASIC events (execution_start, node_start, node_end, workflow_complete) are always emitted. ADVANCED events (capability_dispatch, transform_end, side_effect_end) appear only under FULL policy. A BASIC trace captures the structural skeleton. A FULL trace captures internal mechanics --- transforms, side effects, and output hashes.
- The chain is persisted as JSONL --- one JSON object per line, appended to a file named by execution_id (e.g., `T_20260225_143000_a1b2c3d4.jsonl`). The format is append-only. The file is never rewritten, never truncated, never edited. The trace sink's interface exposes no mutation operations.

## 9.4 --- The Trace Examiner

**Definition:** The Trace Examiner is a structural introspection tool that reads a trace chain and produces a deterministic diagnostic report --- without re-executing the workflow, without accessing runtime state, and without interpreting business logic.

**Key Properties:**

1.  **Deterministic classification.** The examiner applies a fixed ruleset to the trace's structural fields (error_code, node_category, exit_reason_code). The rules are ordered and exhaustive. The same trace always produces the same classification.
2.  **Artifact locator.** When a failure is classified, the examiner maps the failing node to the governance artifact responsible --- the workflow specification, the capability contract, the transform, or the runtime binding. The operator knows which file to open.
3.  **Prescriptive hints.** The examiner generates actionable fix suggestions referencing specific artifacts and fields. Not "check your configuration" --- but "add missing field `employee_id` to payload, or fix expression `$.inputs.employee_id` in CC_ONBOARD_EMPLOYEE_V0."

### Example 9.4 --- Trace Examiner Diagnostic Report

Given the failed trace from Example 8.5 (Chapter 8 --- the actor registration that encountered ALREADY_EXISTS), the examiner produces:

    TRACE DIAGNOSTIC REPORT
    ============================================================
    Execution ID:    T_20260225_143000_a1b2c3d4
    Workflow:        WF_REGISTER_ACTOR_UNVERIFIED_V0
    Structural Failure: YES

    Failure Class:   CS_RUNTIME_ERROR
    Failing Node:    N003 (CC_REGISTER_ACTOR_KYC_V0)
    Reason:          Side-effect CS_ACTOR_ALIAS_INDEX_V0 returned
                     ALREADY_EXISTS during REGISTER operation

    Artifact Path:   blockchain/governance/registry/
                     capability_contracts/cc_register_actor_kyc_v0.md

    Fix Hint:        CS execution returned ALREADY_EXISTS. If
                     duplicate registration is expected, update
                     on_result routing for ALREADY_EXISTS in the
                     CC_ binding. If duplicates should be
                     prevented, add admission logic to check for
                     prior registration.

    Side Effect Outcomes:
      CS_ACTOR_ALIAS_INDEX_V0  REGISTER  -> ALREADY_EXISTS
    ============================================================

**Analysis:**

- The examiner did not re-execute the workflow. It read the trace --- a JSONL file --- and applied classification rules. The error event's `node_category: CS` triggered the CS_RUNTIME_ERROR classification. The `exit_reason_code: EXIT_ALREADY_EXISTS` confirmed the failure's structural origin.
- The artifact path points the operator to the specific governance file. This is not a stack trace pointing to a line of Python code. It is a governance reference pointing to the CC_ artifact that declared the capability. The fix is a governance change --- modifying the `on_result` routing --- not a code patch.
- The side effect outcomes section summarizes every CS_ invocation and its result. In a pipeline with multiple CS_ steps, this summary tells the operator which mutations succeeded and which failed --- the partial state visibility that Chapter 8's Problem 8.3 required.

### The Examiner Pipeline

The Trace Examiner operates as a five-stage pipeline:

  -----------------------------------------------------------------------------------------------------
  Stage           Component               Input                          Output
  --------------- ----------------------- ------------------------------ ------------------------------
  1               Parser                  JSONL file                     ParsedTrace (indexed events)

  2               Classifier              ParsedTrace                    FailureClass + failing node

  3               Locator                 FailureClass + node            Artifact file path

  4               Hint Engine             FailureClass + error details   Prescriptive fix string

  5               Reporter                All above                      DiagnosticReport
  -----------------------------------------------------------------------------------------------------

Each stage is deterministic. The parser validates event structure against the schema. The classifier applies ordered rules --- not heuristics. The locator uses the path registry to resolve artifact locations. The hint engine generates concrete suggestions from structured error fields. The reporter formats the output.

### Example 9.5 --- Classification Rules (Excerpt)

The classifier applies rules in priority order. The first matching rule determines the classification:

    Rule 1: error_code == EXPRESSION_RESOLUTION_FAILED
            → EXPRESSION_ERROR

    Rule 2: error_code == SCHEMA_VALIDATION_FAILED
            → SCHEMA_ERROR

    Rule 3: node_end.status == NACK on intent node
            → BUSINESS_VIOLATION

    Rule 4: node_category == CT
            → CT_STRUCTURE_ERROR

    Rule 5: node_category == CS
            → CS_RUNTIME_ERROR

    Rule 6: exit_reason_code in {NO_TRANSITION, NO_ENTRY_NODE,
            NODE_NOT_FOUND}
            → GRAPH_STRUCTURE_ERROR

    Rule 7: error_code == BINDING_RESOLUTION_FAILED
            → BINDING_ERROR

**Analysis:**

- The rules are structural --- they match on constitutional fields (error_code, node_category, exit_reason_code), not on message strings. "Registry key KYC_8a4c1d9e already exists" is a human-readable message. The classifier ignores it. It classifies on `node_category: CS` --- Rule 5.
- The ordering matters. An EXPRESSION_RESOLUTION_FAILED error with node_category CT would match Rule 1 (expression error), not Rule 4 (CT structure error). The expression error is the root cause; the CT attribution is incidental.
- The classifier also detects "unhappy paths" --- CC_ nodes that return non-SUCCESS statuses followed by exit routing. These are not necessarily failures. A workflow that routes ALREADY_EXISTS to an exit node may be operating correctly --- the examiner distinguishes structural failures (broken traces, missing transitions) from business violations (domain rejections that the governance anticipated).

The Examiner is not observability tooling. It is a constitutional verifier. Its authority derives from governance artifacts, not runtime introspection. It reads only what the constitution mandates must exist --- schema-validated trace events with constitutional field vocabularies. Its classifications are governance judgments, not operational heuristics.

## 9.5 --- Validation and Failure Surface

### Trace Validation Checks

  ----------------------------------------------------------------------------------------------
  Step          Check                    Failure Condition
  ------------- ------------------------ -------------------------------------------------------
  1             Schema conformance       Required field missing or wrong type in trace event

  2             Sequence monotonicity    `sequence` does not increment by 1

  3             Hash integrity           `prev_hash` does not match SHA-256 of preceding event

  4             Event type vocabulary    `event_type` not in SCHEMA_TRACE_EVENT_V0

  5             Error code vocabulary    `error_code` not in constitutional error code enum

  6             Exit reason vocabulary   `exit_reason_code` not in constitutional enum

  7             Payload completeness     Event-specific required payload fields missing
  ----------------------------------------------------------------------------------------------

### Broken Example 9.6 --- Tampered Trace Record

An operator --- or an attacker --- modifies a trace record to change a failure into a success. Event 11 originally recorded `status: "ALREADY_EXISTS"`. The modified trace is shown in Appendix B, Example 9.6.

The `status` field has been changed from `ALREADY_EXISTS` to `SUCCESS`. But the `prev_hash` of Event 12 was computed from the original Event 11 --- which contained `"status": "ALREADY_EXISTS"`. The modified Event 11 has a different JSON serialization. Its hash no longer matches Event 12's `prev_hash`.

**Deterministic Diagnostic:**

    TRACE INTEGRITY VIOLATION
      Execution ID:   T_20260225_143000_a1b2c3d4
      Break Point:    Between sequence 11 and sequence 12
      Expected Hash:  b8d2f41a7c3e9506
      Computed Hash:  4e7a1f9c3d5b2801
      Detail:         SHA-256 of event at sequence 11 does not match
                      prev_hash of event at sequence 12.
                      Trace chain is broken. Records at or after
                      sequence 11 may have been modified.
      Status:         CHAIN INTEGRITY FAILED

**Correction Required:** Trace artifacts are immutable. A broken chain cannot be repaired by adjusting hashes --- that would require recomputing every subsequent event's hash, which requires the exact JSON serialization of every subsequent event. The correct response to a broken chain is: re-execute the workflow from the original artifacts and payload. The original trace is flagged as compromised. It cannot serve as an audit record.

**This section proves:** Execution history cannot be silently altered under ADVANCED policy. Modifying any field in any record produces a detectable hash discontinuity. The distance between tampering and detection is zero --- the next record's `prev_hash` fails verification.

## 9.6 --- Structural Insight (Doctrine Moment)

The reader has now seen trace records (Example 9.1), hash chains (Example 9.2), a complete trace chain (Example 9.3), the Trace Examiner's diagnostic output (Example 9.4), and what happens when a record is tampered with (Example 9.6). At no point was the trace optional. At no point was the trace format chosen by the developer. At no point was the hash chain toggled in a debug session.

This is Chapter 2's **Property 5 --- Observable Execution** rendered as a constitutional artifact. Observability in PGS is not instrumentation added to code. It is a governance obligation that the execution engine fulfills structurally.

**Invariant I-G8 --- Deterministic Reconstructability:** Given ratified governance artifacts, a runtime binding, a payload, and a complete trace chain, any execution can be replayed deterministically. This invariant was previewed in Chapter 8. This chapter demonstrates the mechanism: the trace chain records every structural event in emission order, with schema-validated fields, monotonic sequencing, and (under ADVANCED policy) cryptographic hash continuity. Replay does not require the original runtime. It requires the artifacts that governed the execution and the trace that recorded it.

**What the engine cannot do** (consequences of the Structural Invariance Principle):

- **Modify trace records post-emission.** The trace sink is append-only --- no update, no delete, no rewrite.
- **Omit intermediate events.** Emission calls are embedded in the execution path. The engine cannot execute a node without emitting `node_start` and `node_end`.
- **Conceal executed capabilities.** Every dispatch is bounded by trace events. There is no silent execution channel. Whether undeclared capabilities can be invoked at all is an authority question --- addressed in Chapter 10.

**Authority transfer:** At the moment of emission, authority transfers from the runtime process to the immutable artifact. The engine produced the event. Once written to the sink, the engine cannot retract it. The trace becomes the sovereign record --- it may be examined, verified, and audited independently of the engine that produced it. The engine is a witness. The trace is the testimony.

> **[DIAGRAM 6] --- Trace Chain Structure**

      execution_id
          |
          v
      hash(execution_id) = H0
          |
          v
      Event 1: execution_start
        prev_hash: H0
        payload: {workflow_code, ...}
          |
          v
      hash(Event 1) = H1
          |
          v
      Event 2: node_start
        prev_hash: H1
        payload: {node_id, node_type, ...}
          |
          v
      hash(Event 2) = H2
          |
          v
      Event 3: node_end
        prev_hash: H2
        payload: {node_id, status, ...}
          |
          ...
          v
      Event N: workflow_complete
        prev_hash: H(N-1)
        payload: {exit_condition, exit_reason_code, ...}

> Each event's `prev_hash` is computed from the full JSON serialization of the preceding event. The chain is tamper-evident: modifying any event invalidates every subsequent hash. Verification is linear --- walk the chain, recompute each hash, compare. The structural impossibility: an event cannot be inserted, removed, or modified without breaking the chain.

## 9.7 --- Solved Problems

### Problem 9.1 --- "The Log Gap"

**Scenario:** A production incident occurs. The operations team searches logs. The service processed 10,000 requests that hour. The logs show 9,847 entries. Where are the other 153?

**Application-Centric Approach:** The service writes logs from application code. Some paths have logging; others do not. The error handler logs exceptions, but a particular code path returns early without logging. Another path logs at DEBUG level, which is disabled in production. A third path logs to stdout, but the log aggregator only collects from the structured logger. The 153 missing entries are distributed across three different causes --- none of which are visible without reading the source code of every request handler.

**PGS Approach:**

1.  Every workflow execution emits `execution_start` and `workflow_complete` events. These are BASIC events --- emitted regardless of trace depth policy. There is no execution without these two events.
2.  The `sequence` field provides monotonic ordering within each execution. A gap in the sequence is detectable mechanically --- if Event 5 is followed by Event 7, Event 6 is missing.
3.  Under FULL policy, hash chaining makes gaps unforgeable. Event 7's `prev_hash` would reference Event 6. If Event 6 is absent, the chain is broken.
4.  The trace sink is append-only JSONL. Events are not buffered and flushed periodically --- they are appended at emission. A crash between emission and the next step does not lose the emitted event.

**Eliminated pathology:** Observability ambiguity. In PGS, the question "how many executions occurred?" is answered by counting `execution_start` events. The question "did execution N complete?" is answered by the presence of `workflow_complete` at the end of its chain. There are no missing entries because emission is structural --- not optional.

### Problem 9.2 --- "The Silent Production Patch"

**Scenario:** A production hotfix modifies a service's behavior. The deployment succeeds. The service processes requests differently than before. But the logs look the same --- same format, same messages, same levels. Three weeks later, an audit asks: "What changed in production on February 10th?" No one can answer with certainty.

**Application-Centric Approach:** The deployment log shows that version 2.3.7 was deployed. But version 2.3.7 is a Git tag --- it tells you what code was deployed, not what behavior changed. To determine behavioral change, someone must diff the code between 2.3.6 and 2.3.7, understand the diff, and reason about its impact. If the diff is large, this is a multi-day exercise. If the diff touches shared utilities, the blast radius is unclear.

**PGS Approach:**

1.  Governance artifacts are version-bound. CC_REGISTER_ACTOR_KYC_V0 is version "v0" --- structurally frozen. A behavioral change requires a new artifact version: CC_REGISTER_ACTOR_KYC_V1.
2.  Every trace records the artifact versions that governed the execution. The `capability_code` field in `node_start` events references the versioned artifact. The workflow code in `execution_start` is versioned.
3.  To answer "what changed on February 10th?" --- compare traces before and after. If the workflow code changed from WF_REGISTER_ACTOR_UNVERIFIED_V0 to WF_REGISTER_ACTOR_UNVERIFIED_V1, the change is visible in the trace. If the workflow code is the same but a CC_ version changed, the `capability_dispatch` events show the new CC_ code.
4.  Replay confirms: execute the old artifacts with the same payload, execute the new artifacts with the same payload, compare traces structurally. The behavioral difference is the structural difference between two deterministic trace chains.

**Eliminated pathology:** Undetected semantic drift. Behavioral changes are artifact version changes. Artifact version changes are visible in traces. Traces are immutable records. The audit trail is not reconstructed from memory --- it is read from governed artifacts.

### Problem 9.3 --- "The Compliance Audit"

**Scenario:** A financial regulator asks: "Prove that transaction T-4492 was processed according to your declared procedures, that no unauthorized steps were executed, and that the execution record has not been modified since the transaction occurred."

**Application-Centric Approach:** The compliance team manually reconstructs the execution from logs, database records, and code reviews. They identify the relevant log entries (hoping the log retention policy has not expired them). They trace the execution through multiple services (hoping the correlation IDs are consistent). They verify that the code deployed at the time of the transaction matches the code in the repository (hoping the deployment records are accurate). The reconstruction takes two weeks. The regulator asks clarifying questions. The process repeats.

**PGS Approach:**

1.  Retrieve the trace file for execution T-4492. It is a single JSONL file, append-only, stored at the declared trace path.
2.  Run the Trace Examiner. The parser validates schema conformance. The hash chain verifier confirms integrity --- every `prev_hash` matches the SHA-256 of its predecessor. If the chain is intact, no record has been modified since emission.
3.  The trace records every node traversal, every capability dispatch, every transform execution, every side effect operation. Each references a versioned governance artifact. The examiner confirms: every capability invoked in the trace is declared in the CC_ artifacts. No undeclared capabilities appear.
4.  Provide the regulator with: (a) the trace file, (b) the versioned governance artifacts, (c) the examiner's verification report. The regulator can independently verify: run the examiner on the trace, confirm hash integrity, confirm artifact version bindings, confirm no undeclared capabilities.

**Eliminated pathology:** Interpretive audit risk. The audit does not depend on human reconstruction. It does not depend on log completeness. It does not depend on deployment records. The trace is the execution record. The artifacts are the declared procedures. The hash chain is the integrity proof. The examiner is the verification tool. The entire audit is structural --- machine-verifiable, independently reproducible, and non-interpretive.

### Problem 9.4 --- "Retroactive Log Editing"

**Scenario:** An operator modifies historical log entries to conceal an operational error that caused a service disruption. The modification is performed directly on the log storage system. No one notices for six months --- until an external audit cross-references the logs against a downstream system's records and finds inconsistencies.

**Application-Centric Approach:** Logs are mutable files or database records. An administrator with storage access can edit, truncate, or delete entries. Without WORM (Write Once, Read Many) storage or external attestation services, tampering is undetectable. Even with WORM storage, the protection is infrastructure-dependent --- it works only if the storage system is correctly configured and the administrator does not have override access. The integrity guarantee lives in the infrastructure, not in the record.

**PGS Approach:**

1.  The trace is append-only JSONL. The trace sink exposes no mutation operations. Modifying a trace requires direct file system access --- bypassing the execution engine entirely.
2.  Under FULL policy, every trace event carries a `prev_hash` computed from the SHA-256 of its predecessor's JSON serialization. Modifying any field in any record changes that record's serialization. The next record's `prev_hash` no longer matches. The chain breaks.
3.  Chain verification is mechanical and independent. Any party with access to the trace file can recompute the hash chain. A broken chain is not an ambiguous signal --- it is a deterministic proof of modification.
4.  A broken chain is itself a classified constitutional event. The trace is not merely damaged --- it is compromised. It cannot serve as an audit record. Re-execution from original artifacts and payload is the only path to a valid trace.

**Eliminated pathology:** Undetectable historical tampering. The hash chain transforms trace integrity from an infrastructure concern (correctly configured WORM storage) into a structural property (cryptographic linkage embedded in the record itself). Tampering is not prevented by access controls --- it is made structurally evident regardless of who performs it.

## 9.8 --- Generated Output: Trace Examination Report

This section demonstrates the full output of the Trace Examiner on a successful execution --- proving that the examiner is not only a failure diagnosis tool but a structural verification instrument.

### Successful Execution: WF_CREATE_WALLET_V0

A wallet creation workflow executes successfully. The operator runs the Trace Examiner on the resulting trace file.

### Examiner Verification Output

    TRACE DIAGNOSTIC REPORT
    ============================================================
    Execution ID:    T_20260225_150000_d4c3b2a1
    Workflow:        WF_CREATE_WALLET_V0
    Structural Failure: NO

    Chain Integrity:  VALID (14 events, 0 hash breaks)
    Sequence:         MONOTONIC (1..14, no gaps)
    Schema:           CONFORMANT (all events pass SCHEMA_TRACE_EVENT_V0)

    Node Traversal:
      N001  IN_CREATE_WALLET_V0         intent     ACK        1ms
      N002  CC_GENERATE_WALLET_ID_V0    cc         SUCCESS    4ms
      N003  CC_DERIVE_WALLET_ADDRESS_V0 cc         SUCCESS    7ms
      N004  CC_PERSIST_WALLET_V0        cc         SUCCESS    3ms
      EXIT  —                           exit       COMPLETED  —

    Capability Dispatches:
      N002: CT_PURE_GENERATE_ID_V0          -> SUCCESS
      N003: CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0 -> SUCCESS
            CT_PURE_PUBLIC_KEY_TO_ADDRESS_V0 -> SUCCESS
      N004: CS_WALLET_STATE_V0 (WRITE)      -> SUCCESS
            CS_WALLET_INDEX_V0 (REGISTER)   -> SUCCESS

    Side Effect Outcomes:
      CS_WALLET_STATE_V0    WRITE     -> SUCCESS
      CS_WALLET_INDEX_V0    REGISTER  -> SUCCESS

    Undeclared Capabilities: NONE
    Version Mismatches:      NONE

    Exit Condition:   NORMAL
    Exit Reason Code: COMPLETED
    Total Duration:   23ms
    ============================================================

### What the Output Proves

**1. Chain integrity is verified.** Fourteen events, zero hash breaks. Every `prev_hash` matches the SHA-256 of its predecessor. No record has been modified, inserted, or removed since emission.

**2. Node traversal is complete.** Every node declared in the workflow specification appears in the trace. The traversal path --- N001 through N004 to EXIT --- matches the compiled DAG. No nodes were skipped. No undeclared nodes were visited.

**3. Capability dispatches match declarations.** Every CT_ and CS_ invocation recorded in the trace corresponds to a declaration in the CC_ artifacts. The examiner checks: does CT_PURE_GENERATE_ID_V0 appear in CC_GENERATE_WALLET_ID_V0's pipeline? Yes. Does CS_WALLET_STATE_V0 appear in CC_PERSIST_WALLET_V0's pipeline? Yes. No capability was invoked that was not declared in governance.

**4. Side effect outcomes are visible.** Both CS_ operations succeeded. The operator can see --- at a glance --- what mutations were performed and what their results were. If CS_WALLET_INDEX_V0 had returned ALREADY_EXISTS, it would appear here. The state of the world after execution is structurally described.

**5. WHAT/HOW separation is manifest.** The author wrote WF_CREATE_WALLET_V0, IN_CREATE_WALLET_V0, CC_GENERATE_WALLET_ID_V0, CC_DERIVE_WALLET_ADDRESS_V0, CC_PERSIST_WALLET_V0, and the CT_ and CS_ governance artifacts. The system generated an immutable, hash-chained trace that proves: these artifacts governed this execution, these capabilities were dispatched, these results were produced, and the chain has not been broken.

**Structural impossibility:** The engine cannot execute capabilities outside the ratified artifacts, nor can it conceal that execution. Every dispatch is traced. Every trace event is schema-validated. Every chain is hash-linked. An execution that bypasses governance would either fail to emit valid trace events (detectable by schema validation) or break the hash chain (detectable by integrity verification). There is no silent execution path.

## 9.9 --- Boundary and Forward Pointer

This chapter proved that the execution trace is a first-class governed artifact --- schema-bound, append-only, cryptographically chained, and machine-verifiable. It proved that the Trace Examiner can diagnose failures and verify successful executions from the trace alone --- without re-executing workflows, without accessing runtime state, and without interpreting business logic. It proved that replayability and audit are architectural consequences of the trace structure, not operational aspirations.

Together with Chapter 8, this completes the observability model:

- **Chapter 8:** Governed failure --- every failure is classified, deterministic, trace-complete, and reconstructable
- **Chapter 9:** Governed observability --- the trace itself is a constitutional artifact with structural integrity guarantees

**What this chapter did not cover:**

- Log aggregation tools and operational dashboards
- APM (Application Performance Monitoring) metrics and alerting systems
- Performance instrumentation and profiling
- Distributed trace correlation across federated domains (Chapter 11)
- Long-term trace storage, archival, and retention policies
- **Compiler evidence graph** --- the compiler emits its own governed observability artifact (`evidence_graph.json`) per structure during S7, applying the same constitutional obligations to compilation events that this chapter applies to execution events: typed events, hash integrity, append-only semantics, and a stable consumer contract. The compiler evidence graph is to compilation what the execution trace is to runtime. See Field Manual Section 6.5 for the Evidence Semantics Doctrine governing that artifact.

This chapter proves trace integrity. It does not yet prove execution impossibility --- that undeclared capabilities cannot be invoked at all. That proof belongs to Chapter 10.

**What comes next:** Chapter 10 --- Inverted Security Architecture. This chapter proved that execution records are tamper-evident and that executed capabilities cannot be concealed. Chapter 10 takes the next step: proving that the governance artifact vocabulary defines the total executable surface --- that security is structural, not perimeter-based. The vocabulary-bounded attack surface is not defended by firewalls. It is enforced by the impossibility of executing what governance has not declared.

**Layer movement:** Execution observability formalized within the Security axis. Moving to security architecture proper.

## 9.10 --- Review Questions

1.  **True or False: A trace record may be modified after emission if the hash chain is recomputed.**

- *False. While recomputing the hash chain from the point of modification forward would restore chain continuity, this requires access to the exact JSON serialization of every subsequent event and the ability to rewrite the trace file. The trace sink is append-only --- it does not support in-place modification. More fundamentally, a modified trace with a recomputed chain is a different trace --- it no longer records what actually happened. The original trace is the sovereign record. A "corrected" trace is a fabrication.*

2.  **What is the difference between BASIC and FULL trace depth policy?**

- *BASIC (MINIMAL) emits only structural boundary events: execution_start, node_start, node_end, and workflow_complete. FULL emits all event types including capability_dispatch, transform_start, transform_end, side_effect_start, side_effect_end, context_snapshot, and audit_event. Additionally, FULL enables cryptographic hash chaining via the prev_hash field. The policy is declared in governance --- the runtime binding or workflow specification --- not chosen at debug time.*

3.  **Why is the sequence field the ordering authority, not the timestamp?**

- *The sequence field is a monotonically increasing integer set by the trace emitter at emission time. It provides a canonical, gap-detectable ordering. Timestamps depend on system clocks, which can drift, repeat (NTP adjustments), or collide (sub-millisecond events). Two events with identical timestamps are still unambiguously ordered by sequence. The sequence is structural; the timestamp is informational.*

4.  **What structural guarantee does the Trace Examiner's classifier provide?**

- *Deterministic classification. The classifier applies an ordered, exhaustive ruleset to constitutional fields (error_code, node_category, exit_reason_code). The same trace always produces the same FailureClass. The rules are structural --- they match on schema-defined enums, not on message strings. Classification does not depend on the examiner operator's interpretation or the engineer's domain knowledge.*

5.  **Can the execution engine omit intermediate trace events?**

- *No. Trace emission calls are embedded in the execution path --- node_start is emitted before node dispatch, node_end is emitted after. The engine cannot execute a node without emitting both boundary events. Under FULL policy, capability_dispatch, transform, and side_effect events are similarly embedded. This is structural --- emission is part of execution, not a decorator applied to it.*

6.  **What makes the trace a constitutional artifact rather than a log file?**

- *Three properties: (1) Its schema is governed --- SCHEMA_TRACE_EVENT_V0 defines the required fields, allowed event types, and valid vocabularies for error codes and exit reasons. (2) Its emission is mandated --- CONSTITUTION_TRACE_EXECUTION_V0 requires trace production for every execution. (3) Its integrity is cryptographically verifiable --- the hash chain (under ADVANCED policy) provides tamper evidence. A log file is optional, unschematized, and mutable. A trace artifact is mandated, schema-validated, and append-only.*

7.  **How does the Trace Examiner support compliance audits?**

- *The examiner provides three audit capabilities: (1) Hash chain verification --- confirms no trace records have been modified since emission. (2) Capability declaration verification --- confirms every invoked CT_ and CS_ matches a governance artifact declaration. (3) Structural completeness verification --- confirms the trace covers the full execution from start to completion with no sequence gaps. An auditor can independently run the examiner on the trace file and governance artifacts to verify execution integrity without accessing the runtime environment.*
