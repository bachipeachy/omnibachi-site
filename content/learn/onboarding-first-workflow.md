---
title: 'Onboarding: Build Your First Workflow'
date: '2026-01-15'
draft: false
weight: 1
slug: onboarding-first-workflow
tags:
- PGS
- tutorial
---

---

## Why PGS Exists

Traditional systems:
- embed behavior in code
- are difficult to audit and reproduce
- require changes across multiple layers

PGS:
- declares behavior in protocol artifacts
- compiles it into an execution graph
- executes deterministically with a full trace

This onboarding shows how to work within that model.

---

## 1. What You Already Did

If you followed the `pgs_workspace` README, you ran this:

```bash
./scripts/bootstrap_pgs.sh
source .venv/bin/activate
./scripts/demo_sample_workflow.sh
```

You saw a workflow execute twice. The first run registered an actor. The second run produced `ALREADY_EXISTS` on one node — and still wrote to the event stream. You examined a trace.

You did not write code. You did not configure a framework. You ran a governed execution system.

This document explains just enough to let you build your own.

---

## 2. The 30-Second Mental Model

Every PGS execution follows this path:

```
IN → WF → CC → (CT / CS) → Trace
```

| Concern | What it does |
|---------|-------------|
| `IN_` Intent | Admission gate — validates the incoming payload before anything runs |
| `WF_` Workflow | The execution graph — declares which CCs run and in what order |
| `CC_` Capability Contract | A named node in the graph — declares inputs, outputs, and routing outcomes |
| `CT_` Capability Transform | Pure computation — deterministic, no side effects |
| `CS_` Capability Side Effect | Controlled state change — registry write, event append, email, etc. |
| `RB_` Runtime Binding | Connects declared capabilities to their implementations at build time |
| Trace | Append-only execution record — the ground truth of what happened |

The runtime traverses this graph exactly as declared. It does not interpret or alter behavior. It does not own behavior. Behavior lives in the compiled snapshot.

---

## 3. What Actually Happened in the Demo

Run #1 succeeded end-to-end:

```
CC_GENERATE_ACTOR_ID_V0     → SUCCESS
CC_REGISTER_ACTOR_KYC_V0    → SUCCESS      ← actor written to registry
CC_APPEND_ACTOR_EVENT_V0    → SUCCESS      ← event appended to stream
```

Run #2 hit the idempotency guard:

```
CC_GENERATE_ACTOR_ID_V0     → SUCCESS      ← same ID derived from same input
CC_REGISTER_ACTOR_KYC_V0    → ALREADY_EXISTS  ← registry rejected duplicate
CC_APPEND_ACTOR_EVENT_V0    → SUCCESS      ← event still appended
```

Two things to notice:

- **State is constrained** — the registry enforced uniqueness. `CS_REGISTRY_V0` is declared to be idempotent; this is a protocol property, not application logic.
- **History is not constrained** — the event stream appended regardless. `CS_APPENDONLY_JSONL_V0` never rejects. Both runs are recorded.

The routing from `ALREADY_EXISTS` to the next CC was declared in the workflow DAG. The runtime followed it. No code branch was evaluated. No exception was caught.

---

## 4. Build Your First Workflow

### 4.1 Understand the snapshot

All runnable artifacts live in `protocol_snapshot/artifacts/`. This directory is **read-only** — it is compiled output. You do not edit it by hand.

The runtime only executes snapshots marked as VALID. If the snapshot was not built successfully, execution will fail.

Browse what is available:

```bash
ls protocol_snapshot/artifacts/workflows/
ls protocol_snapshot/artifacts/capability_contracts/
ls protocol_snapshot/artifacts/capability_transforms/
ls protocol_snapshot/artifacts/capability_side_effects/
ls protocol_snapshot/artifacts/runtime_bindings/
```

### 4.2 Run an existing workflow with a different payload

The fastest way to build intuition is to run the same workflow with different input:

```bash
# Edit the payload
cp scripts/payloads/register_actor.json /tmp/my_payload.json
# change the actor fields in my_payload.json

# Run it
pgs_runtime run \
  --wf blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0 \
  --payload /tmp/my_payload.json \
  --data-root $(pwd)/data \
  --workspace $(pwd)
```

### 4.3 Examine the trace

```bash
pgs_runtime examine ./traces/<TRACE_ID>/<TRACE_ID>.jsonl
```

Every node execution is recorded: which artifact ran, what inputs it received, what output it produced, what outcome it returned. This is the execution record — not a log, a proof.

### 4.4 Try a different workflow

```bash
pgs_runtime run \
  --wf blockchain::WF_CREATE_WALLET_V0 \
  --payload <path-to-wallet-payload.json> \
  --data-root $(pwd)/data \
  --workspace $(pwd)
```

List all available workflows:

```bash
ls protocol_snapshot/artifacts/workflows/
```

At this point, you have run and observed multiple workflows. The next step is to modify or create your own to understand how behavior is declared and compiled.

---

## 5. Modify Behavior Safely

To change what a workflow does, change the protocol artifacts — not the runtime.

| To change... | Modify... |
|-------------|-----------|
| Execution flow (which CCs run, in what order) | `WF_` workflow artifact |
| Inputs, outputs, or routing outcomes of a node | `CC_` capability contract |
| The computation inside a node | `CT_` capability transform implementation |
| The storage/IO semantics of a node | `CS_` capability side effect implementation |

All behavior changes must flow through protocol artifacts. Direct changes to runtime or snapshot will be ignored or rejected.

> **Critical rule: never modify the runtime to change behavior.**
>
> The runtime is generic. It has no domain knowledge. Injecting behavior into the runtime breaks the governance model — execution would no longer be constrained by compiled protocol.

After modifying protocol source (in `pgs_compiler`), you must recompile and rebuild the snapshot before the runtime will see the change. The `protocol_snapshot/` directory in this workspace reflects the last compiled state.

---

## 6. Add a New Capability

When the existing CT and CS library does not cover what you need, you add a new capability.

**To add a pure computation (CT):**

1. Implement a deterministic function with no side effects in `pgs_capabilities`
2. Declare a `CT_` artifact in `pgs_compiler` that names and describes it
3. Add an `RB_` binding entry that maps the CT declaration to your implementation
4. Reference the CT in a `CC_` capability contract inside a workflow

**To add a stateful operation (CS):**

1. Implement the storage/IO operation in `pgs_capabilities`
2. Declare a `CS_` artifact in `pgs_compiler` that defines its semantics
3. Add an `RB_` binding entry that maps the CS declaration to your implementation
4. Reference the CS in a `CC_` capability contract inside a workflow

In both cases the pattern is the same: declare in protocol, implement in library, bind via RB, invoke via CC.

For a complete walkthrough of domain construction, see **Chapter 13 — Constructing a Protocol-Governed Domain** in the Practitioner's Guide.

---

## 7. Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ExecutionError: no binding for CT_...` | CT declared in protocol but no RB_ entry wires it to an implementation | Add the RB_ binding for that CT |
| `ValidationError: payload rejected at IN_...` | Input does not satisfy the Intent's admission rules | Check the IN_ artifact schema and fix the payload |
| `BuildError: conformance check failed` | Protocol artifact violates a declared invariant | Run the compiler with `--verbose` and read the assertion output |
| Trace shows `ALREADY_EXISTS` unexpectedly | CS_REGISTRY_V0 found a duplicate key | This is correct behavior — registry is idempotent by design |
| Editing `protocol_snapshot/` has no effect | Snapshot is the compiled output — the runtime reads what is already there | Modify protocol source and recompile |

---

## 8. The Build Lifecycle

```
compile → build → run
```

| Phase | What happens | Where |
|-------|-------------|-------|
| **compile** | Protocol source artifacts are validated against invariants and assertions | `pgs_compiler` |
| **build** | Validated artifacts are materialized into a closed execution snapshot | `pgs_compiler` → `pgs_workspace/protocol_snapshot/` |
| **run** | Runtime reads the snapshot and executes against it | `pgs_workspace` (pgs_runtime CLI) |

The snapshot is sealed at build time. The runtime consumes it unchanged. No behavior enters at execution time that was not present in the snapshot.

---

## 9. Where to Go Deeper

| Resource | What it covers |
|----------|---------------|
| **Chapter 13** — Constructing a Protocol-Governed Domain | End-to-end domain construction: the Seven Architectural Acts from domain spec to running execution |
| **Chapter 14** — AI Agent Governance Domain | A complete worked example applying the model to AI governance |
| **`pgs_compiler` repo** | Authoring protocol artifacts, compiler rules, invariants |
| **`pgs_capabilities` repo** | Writing CT and CS implementations within declared contracts |
| **TechRxiv paper** | Formal model, security proofs, scalability analysis |
| **ORCID working papers** | Background theory and intellectual lineage (https://orcid.org/0009-0007-3810-6520) |

---

## 10. Final Takeaway

You did not write execution code.

You declared behavior, compiled it, and ran it.

The runtime did not know what domain it was executing. It did not know what "actor registration" means. It traversed a graph defined by governance artifacts, invoked capabilities through declared bindings, and wrote a verifiable trace.

That is the PGS model. Governance is not applied after the fact — it is compiled into the execution structure before the first instruction runs.

If behavior changes, it is because the protocol changed — not because the runtime decided differently.
