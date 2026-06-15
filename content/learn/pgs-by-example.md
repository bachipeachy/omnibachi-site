---
title: PGS by Example
date: '2026-01-22'
draft: false
weight: 2
slug: pgs-by-example
tags:
- PGS
- tutorial
---

**Author:** Bhash Ganti (Bachi)
**Goal:** Teach PGS by building something real, not by describing an abstraction.

---

## Before You Start

This document assumes you have run the bootstrap and seen at least one workflow execute. You do not need to understand everything yet — that is the point of an example.

We will build a complete domain from scratch, following the same steps used to build the actual `collatz_conjecture` domain in `pgs_ai_governance`. By the end, you will understand how a real spec becomes a running, traceable, transport-accessible PGS domain.

**Minimal Domain Philosophy:** This example intentionally minimizes business complexity so architectural structure remains visible. The goal is not to demonstrate mathematics — it is to demonstrate protocol-governed execution. The math is just simple enough that nothing distracts from the architecture.

---

## 1. What We Are Building

**The Collatz Conjecture** is a famously simple open problem in mathematics:

> Given any positive integer n:
> - If n is **even** → divide by 2
> - If n is **odd** → multiply by 3 and add 1
> - Repeat until you reach 1
>
> The conjecture: **every positive integer eventually reaches 1.**

Example — start with **6**:
```
6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
```

Example — start with **7**:
```
7 → 22 → 11 → 34 → 17 → 52 → 26 → 13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
```

**What our system does:**
1. Accept a list of numbers from a user
2. Compute the full sequence for each number
3. Verify every sequence terminates at 1
4. Store the results
5. Serve all of this through a web UI

Simple enough that anyone can follow it. Rich enough to demonstrate every layer of PGS.

---

## 2. Why This Example Matters Architecturally

This is not just a Collatz tutorial. This example demonstrates every core PGS property simultaneously:

> **Note on domain placement:** This example lives inside `pgs_ai_governance` — not because Collatz has anything to do with AI governance, but to illustrate a key PGS property: **domain separation is for human cognition only.** PGS is domain-agnostic and does not discriminate between domains at execution time. The runtime that executes blockchain identity, AI governance enforcement, and Collatz math is identical. Domains are organizational boundaries in the artifact registry; they are invisible to the execution engine.

| Property Demonstrated | How Collatz Shows It |
|----------------------|---------------------|
| **Semantic-agnostic execution** | The same runtime that runs blockchain identity runs this math problem — unchanged |
| **DAG traversal without loops** | Sequences computed declaratively; no runtime `while` loop in the graph |
| **Transport orthogonality** | CLI and HTTP both run the exact same workflow, same trace |
| **Snapshot-driven execution** | Zero behavior in the runtime; everything in compiled artifacts |
| **Trace as proof** | Every execution is recorded; replay is deterministic |
| **VIOLATION as first-class outcome** | If the conjecture failed, it would be a protocol outcome, not an exception |
| **Pure separation of CT and CS** | Computation (CT) cleanly separated from storage (CS) |
| **No enterprise distraction** | No security policy, no permissions, no business rules — just structure |

And critically: **it has a web UI.** We will wire the whole thing to a browser form.

---

## 3. The Final Architecture (Read This First)

Before touching a single artifact, understand what we are building:

```
Browser Form
     ↓
  TI_ (HTTP transport ingress — normalizes POST body)
     ↓
  IN_COLLATZ_INPUT_VALIDATED_V0
  (admission gate — rejects invalid numbers)
     ↓ ACK                      ↓ NACK
     ↓                          → EXIT_REJECTED
  CC_COMPUTE_SEQUENCES_V0
  (invokes CT_PURE_COLLATZ_STEP_V0 — pure math)
     ↓ SUCCESS                  ↓ VIOLATION
     ↓                          → EXIT_ERROR
  CC_VERIFY_TERMINATION_V0
  (invokes CT_PURE_TERMINATION_CHECK_V0 — checks all reached 1)
     ↓ SUCCESS                  ↓ VIOLATION
     ↓                          → EXIT_CONJECTURE_VIOLATED
  CC_STORE_RESULTS_V0
  (invokes CS_MUTABLE_JSON_V0 — writes to data/)
     ↓ SUCCESS
     → EXIT_CONJECTURE_PROVEN
```

**Artifact inventory** (what we will build):

| Artifact | Code | Role |
|----------|------|------|
| Intent | `IN_COLLATZ_INPUT_VALIDATED_V0` | Admission gate |
| Workflow | `WF_DEMO_COLLATZ_CONJECTURE_V0` | The full DAG |
| Capability Contract | `CC_COMPUTE_SEQUENCES_V0` | Invokes the Collatz math |
| Capability Contract | `CC_VERIFY_TERMINATION_V0` | Checks termination |
| Capability Contract | `CC_STORE_RESULTS_V0` | Persists results |
| Capability Transform | `CT_PURE_COLLATZ_STEP_V0` | Pure: computes sequences |
| Capability Transform | `CT_PURE_TERMINATION_CHECK_V0` | Pure: checks sequences end at 1 |
| Runtime Binding | `RB_COLLATZ_V0` | Wires CS to its implementation |

**What we do NOT build:** the runtime, the compiler, the trace writer, the HTTP server, the governance framework. Those already exist. We only declare behavior.

All authored artifacts compile into immutable snapshot state before execution begins. The runtime never executes raw markdown artifacts directly — it reads only the compiled JSON snapshot.

### 3.1 Visual References

Two compiled visuals accompany this document:

**Compiled DAG (from snapshot)** — the admissibility graph as constructed by the compiler from protocol artifacts:
[`doc/assets/WF_DEMO_COLLATZ_CONJECTURE_V0.projection.png`](/figures/WF_DEMO_COLLATZ_CONJECTURE_V0.projection.png)

**Execution trace — happy path** — the actual path taken during the first test case (10 numbers, all converge to 1):
[`doc/assets/collatz_conjecture_happy_flow_execution.png`](/figures/collatz_conjecture_happy_flow_execution.png)

The compiled DAG shows all possible paths. The execution trace shows the one path that was actually taken. Comparing the two illustrates how the static graph constrains dynamic execution.

---

## 4. Start With a Spec

PGS philosophy: **protocol emerges from declared behavior, not from code.**

So before writing a single artifact, write a human-readable spec. This spec becomes the source of truth for every artifact that follows.

---

### Collatz Conjecture — Domain Spec

**Purpose:** Compute and verify Collatz sequences for a user-supplied list of positive integers.

**Inputs:** A list of positive integers, each in the range [1, 1000000].

**What happens:**
1. Validate the input (reject anything outside range, reject empty lists, reject non-integers)
2. For each number, iterate the Collatz rule until reaching 1. Record every step.
3. Verify that every sequence ended at 1. If not, the conjecture is violated — report which numbers failed.
4. Store the sequences and verdict to durable storage.

**Outcomes:**
- `CONJECTURE_PROVEN` — all sequences terminated at 1 (normal case)
- `CONJECTURE_VIOLATED` — at least one sequence did not reach 1 (historically: this has never happened)
- `REJECTED` — input was invalid; execution never started
- `ERROR` — computation or storage failed

**Constraints:**
- No application code should contain the Collatz rule. It lives in a declared transform.
- Termination verification is a separate step from computation. Each has a single responsibility.
- Results must be stored under a declared storage contract, not written directly by business logic.
- The runtime must not know this is a math problem.

---

This spec is not code. It is not a class diagram. It is not a framework config. It is a statement of behavior that the PGS compiler will validate and enforce.

Every section of the spec maps directly to an artifact:

| Spec Requirement | PGS Artifact |
|-----------------|--------------|
| "Validate the input" | `IN_COLLATZ_INPUT_VALIDATED_V0` |
| "For each number, compute the sequence" | `CT_PURE_COLLATZ_STEP_V0` |
| "Verify termination" | `CT_PURE_TERMINATION_CHECK_V0` |
| "Store results" | `CS_MUTABLE_JSON_V0` (reused from platform) |
| "The full execution path" | `WF_DEMO_COLLATZ_CONJECTURE_V0` |
| "Declared outcomes" | Edge labels in the WF DAG |

---

## 5. Building the Domain — One Artifact at a Time

We build from the inside out: computation first, then contracts, then workflow, then admission, then binding.

---

### 5.1 The Pure Computation: CT_PURE_COLLATZ_STEP_V0

A Capability Transform is pure computation with no side effects. Given input, return output. No storage, no network, no state.

**What it does:** Takes a list of numbers. Returns the full Collatz sequence for each.

```yaml
ct_code: CT_PURE_COLLATZ_STEP_V0
version: v0
governed_by: governance.layers::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  summary: Compute full Collatz sequence for each input number

  inputs:
    numbers:
      type: array
      required: true

  outputs:
    sequences:
      type: object          # mapping: "6" → [6, 3, 10, 5, 16, 8, 4, 2, 1]

machine:
  ct_kind: atom             # does exactly one thing
  ct_purity: ct_pure        # zero side effects — compiler enforces this
  operation: PURE_COLLATZ_STEP
  implementation:
    module: pgs_ai_governance.implementation.capability_transforms.atoms.ct_pure_collatz_step_v0
    callable: execute
```

The Python implementation (`execute(numbers) → sequences`) runs the Collatz iteration. The artifact declares its contract; the implementation fulfills it. The compiler checks both.

**Why an atom?** Atoms do exactly one thing. Molecules compose atoms. Here, one transform does one computation — atom is correct.

---

### 5.2 The Termination Check: CT_PURE_TERMINATION_CHECK_V0

A second pure transform, completely separate from computation:

```yaml
ct_code: CT_PURE_TERMINATION_CHECK_V0
version: v0
governed_by: governance.layers::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

core:
  inputs:
    sequences:
      type: object           # the sequences dict from CT_PURE_COLLATZ_STEP_V0
      required: true

  outputs:
    all_terminate:
      type: boolean          # true if every sequence ends at 1
    non_terminating:
      type: array            # seeds that didn't reach 1 (empty in normal case)

machine:
  ct_kind: atom
  ct_purity: ct_pure
  operation: PURE_TERMINATION_CHECK
  implementation:
    module: pgs_ai_governance.implementation.capability_transforms.atoms.ct_pure_termination_check_v0
    callable: execute
```

**Why separate?** The spec said so: "Termination verification is a separate step." Single responsibility. Each artifact does one thing, is testable independently, is auditable independently.

---

### 5.3 First CC: CC_COMPUTE_SEQUENCES_V0

A Capability Contract wraps a CT (or CS) and declares the full contract: inputs in, outputs out, all possible outcomes. It is the node in the workflow graph.

```yaml
cc_code: CC_COMPUTE_SEQUENCES_V0
version: v0
governed_by: governance.layers::CONSTITUTION_CAPABILITY_CONTRACT_V0

core:
  inputs:
    numbers:
      type: array
      required: true

  outputs:
    sequences:
      type: object

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]

  pipeline:
    - step: compute_sequences
      transform: ai_governance::CT_PURE_COLLATZ_STEP_V0    # FQDN required
      inputs:
        numbers: $.inputs.numbers                          # JSONPath: pull from CC inputs
      outputs:
        sequences: $.capability_result.sequences           # JSONPath: pull from CT output
      on_result:
        SUCCESS: exit
        VIOLATION: exit
```

Key things to notice:
- `pipeline` lists the steps. Each step invokes one CT or CS via FQDN.
- `$.inputs.numbers` is JSONPath — declarative data wiring, not code.
- The `result_status_contract` declares all outcomes the DAG must handle. If the workflow does not handle them, the compiler rejects it.

#### Why CC Exists

You might ask: why not invoke `CT_PURE_COLLATZ_STEP_V0` directly from the workflow?

CTs and CSs expose primitive computational and side-effect capabilities. CCs exist to:
- declare contracts (inputs, outputs, allowed outcomes)
- normalize outcomes into named protocol results
- compose multi-step pipelines
- evaluate admissibility conditions on results
- isolate execution semantics from primitive implementation details

Workflows orchestrate CCs, not raw implementations. The CC is the declared node. The CT is the declared computation inside it.

---

### 5.4 Second CC: CC_VERIFY_TERMINATION_V0

```yaml
cc_code: CC_VERIFY_TERMINATION_V0

core:
  inputs:
    sequences:
      type: object
      required: true

  outputs:
    all_terminate:
      type: boolean
    non_terminating:
      type: array

  result_status_contract:
    allowed: [SUCCESS, VIOLATION]

  pipeline:
    - step: check_termination
      transform: ai_governance::CT_PURE_TERMINATION_CHECK_V0
      inputs:
        sequences: $.inputs.sequences
      outputs:
        all_terminate: $.capability_result.all_terminate
        non_terminating: $.capability_result.non_terminating
      on_result:
        SUCCESS: evaluate_conjecture
        VIOLATION: exit

  evaluation:
    evaluate_conjecture:
      condition: $.capability_result.all_terminate == true
      on_true: SUCCESS
      on_false: VIOLATION
```

Note the `evaluation` block — after the CT runs, we check the result to decide the CC outcome. This is purely declarative. No imperative branching logic is authored in runtime code — the runtime traverses declared evaluation conditions as specified.

---

### 5.5 Third CC: CC_STORE_RESULTS_V0

This CC invokes a CS (side effect), not a CT. That is the only structural difference:

```yaml
cc_code: CC_STORE_RESULTS_V0

core:
  inputs:
    sequences:       { type: object, required: true }
    all_terminate:   { type: boolean, required: true }
    non_terminating: { type: array }

  outputs:
    result_status: { type: string }

  result_status_contract:
    allowed: [SUCCESS, VIOLATION, BACKEND_ERROR]

  pipeline:
    - step: store_results
      side_effect: capability_side_effects::CS_MUTABLE_JSON_V0   # CS, not transform
      op: WRITE
      store: COLLATZ_RESULTS
      inputs:
        key: "collatz_results"
        value:
          sequences: $.inputs.sequences
          all_terminate: $.inputs.all_terminate
          non_terminating: $.inputs.non_terminating
      outputs:
        result_status: $.result_status
      on_result:
        SUCCESS: exit
        VIOLATION: exit
        BACKEND_ERROR: exit
```

`CS_MUTABLE_JSON_V0` is a platform-level side effect. It already exists. We reuse it. We do not implement a new storage layer — we declare usage of an existing declared side effect.

**Three outcomes** here instead of two — CS_ artifacts can produce `BACKEND_ERROR` (infrastructure failure). The CC declares all three. The workflow must route all three.

---

### 5.6 The Admission Gate: IN_COLLATZ_INPUT_VALIDATED_V0

Intents are the admission gate. Nothing enters the execution graph without passing the intent.

```yaml
in_code: IN_COLLATZ_INPUT_VALIDATED_V0
version: v0
governed_by: governance.layers::CONSTITUTION_INTENT_V0

core:
  summary: Validate Collatz input — list of positive integers < 1000000
  workflow: WF_DEMO_COLLATZ_CONJECTURE_V0

  inputs:
    numbers:
      type: array
      required: true

  outcomes:
    ACK:
      description: Input valid — execution proceeds
    NACK:
      description: Input invalid — execution rejected before graph entry

extensions:
  admission_rules:
    - "numbers must be a non-empty array"
    - "each element must be a positive integer"
    - "each element must be < 1000000"
```

The `workflow` field binds this intent to one workflow. One intent → one workflow. The intent is the protocol entry point. Payload rejection happens here, before any CC runs.

---

### 5.7 The Workflow: WF_DEMO_COLLATZ_CONJECTURE_V0

The workflow is the DAG. It declares every node, every edge, every routing decision:

```yaml
wf_code: WF_DEMO_COLLATZ_CONJECTURE_V0
version: v0
governed_by: governance.layers::CONSTITUTION_WORKFLOW_V0

runtime_binding: ai_governance::RB_COLLATZ_V0       # which binding to use
structure: governance.layers::STRUCTURE_RUNTIME_EXECUTION_V0

core:
  start_node: IN_COLLATZ_INPUT_VALIDATED_V0

  nodes:
    IN_COLLATZ_INPUT_VALIDATED_V0:
      type: IN
      code: IN_COLLATZ_INPUT_VALIDATED_V0
      next:
        ACK:  CC_COMPUTE_SEQUENCES_V0
        NACK: EXIT_REJECTED

    CC_COMPUTE_SEQUENCES_V0:
      type: CC
      code: CC_COMPUTE_SEQUENCES_V0
      inputs:
        numbers: $.payload.numbers             # from the admission-validated payload
      next:
        SUCCESS:   CC_VERIFY_TERMINATION_V0
        VIOLATION: EXIT_ERROR

    CC_VERIFY_TERMINATION_V0:
      type: CC
      code: CC_VERIFY_TERMINATION_V0
      inputs:
        sequences: $.results.CC_COMPUTE_SEQUENCES_V0.sequences   # from previous CC
      next:
        SUCCESS:   CC_STORE_RESULTS_V0
        VIOLATION: EXIT_CONJECTURE_VIOLATED

    CC_STORE_RESULTS_V0:
      type: CC
      code: CC_STORE_RESULTS_V0
      inputs:
        sequences:       $.results.CC_COMPUTE_SEQUENCES_V0.sequences
        all_terminate:   $.results.CC_VERIFY_TERMINATION_V0.all_terminate
        non_terminating: $.results.CC_VERIFY_TERMINATION_V0.non_terminating
      next:
        SUCCESS:       EXIT_CONJECTURE_PROVEN
        VIOLATION:     EXIT_ERROR
        BACKEND_ERROR: EXIT_ERROR

    EXIT_CONJECTURE_PROVEN:  { type: EXIT, reason: COMPLETED }
    EXIT_CONJECTURE_VIOLATED:{ type: EXIT, reason: COMPLETED }
    EXIT_REJECTED:           { type: EXIT, reason: EXITED }
    EXIT_ERROR:              { type: EXIT, reason: FAILED }
```

Read this like a routing table:
- Each `next:` block shows what happens for every possible outcome of that node
- JSONPath expressions (`$.results.CC_COMPUTE_SEQUENCES_V0.sequences`) wire outputs of one CC as inputs to the next
- The runtime follows this exactly. No interpretation. No imperative branching logic outside the declared edges.

Once admitted through the IN node, execution ownership transfers entirely to the workflow graph. Transport may no longer reinterpret or mutate execution semantics.

**The static DAG, not a loop:** The workflow graph is statically declared and immutable during execution. Notice there is no `while` loop. The Collatz iteration (which conceptually runs until convergence) is entirely inside `CT_PURE_COLLATZ_STEP_V0`. The graph has no cycles. PGS graphs are always DAGs.

Computational iteration may still exist inside declared transforms — what PGS eliminates is runtime graph mutation and imperative orchestration loops at the execution substrate level. The computation *expands* inside a CT; the graph structure itself is static.

---

### 5.8 The Runtime Binding: RB_COLLATZ_V0

The binding connects `CS_MUTABLE_JSON_V0` (the declared side effect) to `MutableJsonRuntime` (the concrete Python class that performs the actual file write):

```yaml
rb_code: RB_COLLATZ_V0
version: v0
governed_by: governance.layers::CONSTITUTION_RUNTIME_BINDING_V0

core:
  storage_structure: ai_governance::STRUCTURE_COLLATZ_STORAGE_V0

  bindings:
    capability_side_effects::CS_MUTABLE_JSON_V0:
      type: CS
      host: MutableJsonRuntime
      operation: READ_WRITE
```

This is the only place where protocol declarations touch implementation reality. Authority originates from protocol declarations. Runtime bindings resolve implementation locality only — they provide execution mapping, not behavioral authority.

---

## 6. The Test Payloads

Three scenarios, three files:

**01_happy_path.json** — normal case, all numbers converge:
```json
{ "numbers": [3, 6, 7, 11, 17, 999990, 42, 63, 97, 99] }
```

**02_single_number.json** — minimal valid input:
```json
{ "numbers": [27] }
```

**03_invalid_nack.json** — invalid input, admission gate fires:
```json
{ "numbers": [0, 98, -5] }
```

Note: `0` is not a positive integer. `-5` is negative. Both trigger NACK at the intent gate. Nothing else runs.

---

## 7. Build and Run

### 7.1 Compile and sync

```bash
# Clean
pgs_compiler/scripts/clean_pycache.sh
pgs_compiler/scripts/clean_outputs_dir.sh
pgs_compiler/scripts/clean_compiled_artifacts.sh

# Compile (domain includes ai_governance which includes collatz_conjecture)
python -m pgs_compiler.compiler.cli --structure STRUCTURE_BUILD_AI_GOVERNANCE_CONFIG_V0

# Sync snapshot to workspace
python pgs_compiler/scripts/pgs_build.py --workspace pgs_workspace
```

### 7.2 Run via CLI

```bash
# Happy path — 10 numbers, all converge
pgs_runtime run \
  --wf ai_governance::WF_DEMO_COLLATZ_CONJECTURE_V0 \
  --payload pgs_ai_governance/pgs_ai_governance/testbed/collatz_conjecture/test_payloads/01_happy_path.json \
  --data-root pgs_workspace/data \
  --workspace pgs_workspace

# NACK case — invalid input
pgs_runtime run \
  --wf ai_governance::WF_DEMO_COLLATZ_CONJECTURE_V0 \
  --payload pgs_ai_governance/pgs_ai_governance/testbed/collatz_conjecture/test_payloads/03_invalid_nack.json \
  --data-root pgs_workspace/data \
  --workspace pgs_workspace
```

### 7.3 Examine the trace

```bash
pgs_runtime examine pgs_workspace/traces/<TRACE_ID>/<TRACE_ID>.jsonl
```

Each node appears in the trace with: artifact ID, inputs, outputs, outcome, timestamp. The trace for the happy path shows:

```
IN_COLLATZ_INPUT_VALIDATED_V0  → ACK
CC_COMPUTE_SEQUENCES_V0        → SUCCESS     (sequences computed)
CC_VERIFY_TERMINATION_V0       → SUCCESS     (all terminate at 1)
CC_STORE_RESULTS_V0            → SUCCESS     (results stored)
```

The trace for the NACK case shows:

```
IN_COLLATZ_INPUT_VALIDATED_V0  → NACK        (0 and -5 are invalid)
```

Nothing else. Execution stopped at the gate.

### 7.4 What the Compiler Validated

Before the runtime ran a single node, the compiler validated:

| Validation | What Was Checked |
|-----------|-----------------|
| Artifact schemas | All fields present, correct types, no unknown fields |
| FQDN references | Every `ai_governance::CT_*` and `capability_side_effects::CS_*` reference resolves |
| Workflow routing completeness | Every declared CC outcome has a `next:` edge in the WF |
| CT purity constraints | `ct_purity: ct_pure` — compiler enforces zero side effects |
| CC outcome coverage | Every outcome in `result_status_contract` handled in `on_result:` |
| Runtime binding integrity | Every CS invoked in a CC pipeline has a binding in the RB |
| Governance invariants | `ASSERT_CT_SURFACE_CLOSED_V0`, `ASSERT_IN_WORKFLOW_BINDING_V0`, etc. |
| Admissibility structure | The DAG has a valid start node, no dangling edges, no unreachable exits |

The runtime assumes these guarantees already hold. It does not re-validate at execution time.

### 7.5 Run via Web UI

```bash
~/pgs_workspace/scripts/start_http_server.sh
# → open http://localhost:8000
# → select "collatz_conjecture"
# → enter numbers, submit
# → see sequence output in browser
```

The HTTP server loads routes from the snapshot. No hardcoded routes. The collatz_conjecture domain appears automatically because it is registered as a `--domain` flag in the start script.

The HTTP layer performs admission and projection only. Execution semantics remain entirely inside the workflow graph and compiled protocol state. The same compiled workflow graph executes through CLI, HTTP, queue, agent, or future transports without workflow modification.

---

## 8. What We Did NOT Write

This is the most important section. Here is what we **did not** write:

| What We Skipped | Why |
|----------------|-----|
| A `while` loop for Collatz iteration | That lives inside the CT implementation. The protocol graph is acyclic. |
| Runtime routing logic | Outcomes in `next:` are routing declarations, not `if` statements |
| Transport orchestration | HTTP and CLI share the exact same workflow |
| A controller or service class | There is no controller. The workflow is the admissible orchestration graph. |
| Middleware that branches | Transport only normalizes. No branching in TI/TE. |
| Exception handling for admission | NACK is a first-class protocol outcome, not an exception |
| Dynamic dispatch | The runtime resolves every binding from the compiled snapshot |
| A database adapter | CS_MUTABLE_JSON_V0 is declared; its implementation is bound in RB |
| Storage path logic | Storage paths come from the STRUCTURE artifact, not from code |
| Web routes | Routes loaded from snapshot; no hardcoded route table |
| Test mocks | The artifacts are the spec; the runtime runs the real implementation |
| Runtime schema validation logic | Validation already performed during compilation; runtime assumes guarantees hold |

**Total new application code written:** Two Python functions — `ct_pure_collatz_step_v0.py` and `ct_pure_termination_check_v0.py`. Both are pure math. Both have zero side effects. That is the entire domain-specific implementation.

---

## 9. What the Runtime Knows

Here is exactly what the `pgs_runtime` runtime knows when it runs this workflow:

```
The runtime knows:
  - There is a DAG with 4 active nodes
  - Each node has a declared type (IN / CC / EXIT)
  - Each node produces outcomes from its declared contract
  - Each outcome maps to a next node (or exit)
  - Inputs are resolved via JSONPath from prior node outputs
  - CT calls are pure; CS calls have side effects
  - Both are resolved via the runtime binding

The runtime does NOT know:
  - What "Collatz" is
  - What integers are
  - What convergence means
  - That sequences should end at 1
  - What "conjecture" means
  - What "sequences" are
  - Anything about math
  - Anything about the web UI
  - Anything about what the user submitted
```

The same runtime executed this:
- `blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0` — actor identity registration
- `ai_governance::WF_GOVERN_AGENT_ACTION_V0` — AI governance enforcement
- `ai_governance::WF_DEMO_COLLATZ_CONJECTURE_V0` — this

The engine is identical for all three. The behavior difference is entirely in the compiled artifacts.

---

## 10. Architectural Proofs

These are things we proved by building this, not by arguing about it:

**Proof 1: Transport is orthogonal.** We ran the same workflow from CLI and HTTP with zero changes to the workflow, CCs, CTs, or CS. Only the transport adapter changed.

**Proof 2: DAGs replace loops.** The Collatz iteration is computationally iterative but the protocol graph is acyclic. Iteration lives inside a declared transform. The graph structure is always deterministic.

**Proof 3: Reuse without coupling.** `CS_MUTABLE_JSON_V0` is a platform-level side effect. It was declared once and reused in Collatz without modification. The Collatz domain has no dependency on how it is implemented.

**Proof 4: VIOLATION is a domain concept.** If the Collatz conjecture ever failed (a number didn't reach 1), `VIOLATION` would be a meaningful, routed, traced outcome — not an exception, not an error, not a log message. The protocol handles it correctly.

**Proof 5: Adding a domain required no runtime changes.** The HTTP server, the runtime, the compiler — none changed. A new domain is new artifacts plus a new `--domain` flag at startup.

---

## 11. Bugs We Found Building This

Real learning comes from mistakes. Here are the actual bugs encountered building this subdomain:

### Bug 1: Atoms in the Wrong Repo

**What happened:** The CT atoms (`CT_PURE_COLLATZ_STEP_V0`, `CT_PURE_TERMINATION_CHECK_V0`) were initially placed in `pgs_capabilities` — the shared library repo — and compiled with the `capability_transforms::` namespace instead of `ai_governance::`.

**Why it's wrong:** These CTs are domain-specific. They implement the Collatz rule, not a reusable platform capability. Shared library is for reusable primitives. Domain-specific implementations belong in the domain repo.

**Fix:** Moved Python implementations to `pgs_ai_governance/implementation/capability_transforms/atoms/`. Moved `.md` registry files to `pgs_ai_governance/registry/collatz_conjecture/capability_transforms/`. FQDNs corrected to `ai_governance::CT_PURE_COLLATZ_STEP_V0`.

**Collateral fix required:** The two CCs referencing those CTs still had the old `capability_transforms::` prefix in their `pipeline.transform:` field. Both needed updating. The platform assertion `ASSERT_CT_SURFACE_CLOSED_V0` also needed updating — the old `capability_transforms::` entries were removed and new `ai_governance::` entries added.

**Lesson:** FQDN namespace is determined by which registry folder the artifact lives in. Move the artifact → FQDN changes → all references must be updated.

---

### Bug 2: A Second IN Artifact That Should Not Exist

**What happened:** A second intent artifact, `IN_CONJECTURE_HELD_V0`, was created to verify that the conjecture held after computation. It attempted to bind to `WF_DEMO_COLLATZ_CONJECTURE_V0` — but the workflow already had `IN_COLLATZ_INPUT_VALIDATED_V0` bound to it.

**Build error:**
```
ASSERT_IN_WORKFLOW_BINDING_V0: Two IN artifacts claim the same workflow (WF_DEMO_COLLATZ_CONJECTURE_V0)
```

**Why it's wrong:** IN artifacts are **admission gates only** — they fire before the execution graph starts. They cannot be used as mid-graph verification steps. The post-execution termination check belongs in `CC_VERIFY_TERMINATION_V0`, which already exists.

**Fix:** Deleted `IN_CONJECTURE_HELD_V0`. The verification logic was already correct in `CC_VERIFY_TERMINATION_V0`.

**Lesson:** One workflow, one IN. IN is always the first node. If you need to verify something mid-graph, use a CC with an evaluation step.

---

### Bug 3: YAML Error Masking a Logic Error

**What happened:** A malformed YAML artifact caused the AI Governance build to crash during parse. After fixing the YAML, a separate assertion error (`ASSERT_IN_WORKFLOW_BINDING_V0`) became visible — the YAML crash had been hiding it.

**Lesson:** Fix parse errors first. Compiler phases run in order: discover → parse → validate → assert. An error in an early phase stops later phases from running. You cannot see all your bugs at once.

---

## 12. The Governance Dividend in Practice

After the subdomain was complete and the bugs fixed, we added the HTTP web UI. Here is what we did **not** have to change:

- The workflow — unchanged
- The CCs — unchanged
- The CTs — unchanged
- The CS — unchanged (we reused `CS_MUTABLE_JSON_V0`)
- The runtime — unchanged
- The compiler — unchanged

What we added:
- `static/index.html` — the browser form
- `static/js/collatz_bridge.js` — the API call from browser to server
- A `--domain collatz_conjecture=...` flag in the startup script

The governance surface was already mature. Adding transport cost almost nothing. This is the Governance Dividend: as the governance surface matures, the cost of extending it decreases rather than increasing.

---

## 13. Quick Reference — Artifact Skeleton

If you are building your own domain, here is the minimal structure:

```
pgs_<domain>/pgs_<domain>/registry/<domain>/
  intents/
    IN_<NAME>_V0.md
  workflows/
    WF_<NAME>_V0.md
  capability_contracts/
    CC_<STEP_1>_V0.md
    CC_<STEP_2>_V0.md
    ...
  capability_transforms/         ← if you need custom pure computation
    CT_PURE_<NAME>_V0.md
  runtime_bindings/
    RB_<DOMAIN>_V0.md

pgs_<domain>/pgs_<domain>/implementation/capability_transforms/atoms/
  ct_pure_<name>_v0.py           ← the only code you write
```

**Checklist:**

- [ ] Write the spec first (human-readable behavior statement)
- [ ] Identify which CTs you need (pure computation only)
- [ ] Identify which CSs you need (from platform library or new)
- [ ] Build CCs to wrap CTs/CSs — one CC per logical step
- [ ] Build the workflow DAG — wire CC outputs to next CC inputs via JSONPath
- [ ] Build the IN admission gate — declare rules, bind to workflow
- [ ] Build the RB — wire CS declarations to runtime implementations
- [ ] Compile — fix errors in order (parse first, then validate, then assert)
- [ ] Sync snapshot and run
- [ ] Examine the trace — verify the execution path matches your spec

---

*End of PGS BY EXAMPLE — Collatz Conjecture Worked Domain*
