---
title: "omnibachi"
description: "Protocol-Governed Computing — governing agentic AI and software through compiled, declarative protocol."
---

# Protocol-Governed Computing (PGC)

> Governed by Protocol. Constructed by Compiler. Proven by Trace.
>
> A reference architecture for deterministic, inspectable, AI-era software systems.

## Why this exists

Modern software has a governance problem.

Systems are distributed, event-driven and increasingly machine-generated. The gap keeps widening
between what engineers *intended* and what the software is actually *allowed to do*.

Behavior hides in orchestration code, runtime conditionals, framework conventions, implicit routing
and service glue — and now in AI-generated implementation no human reviewed.

PGC asks a different question:

> What if behavior were governed *before execution* instead of inferred *during execution*?

## What PGC is

PGC is an execution architecture in which behavior originates from a compiled, governed artifact.

- Behavior is declared in governed protocol artifacts.
- A compiler admits or refuses those artifacts and emits domain projections.
- An assembler composes what was admitted into a sealed, content-identified snapshot.
- A runtime reads that snapshot and traverses it. It adds nothing.
- Every run emits a structured trace.

The runtime does not work out what to do. It traverses a graph the compiler already fixed.

## The lifecycle

```
protocol artifacts → compiler → domain projections → assembler
    → sealed snapshot → runtime → execution → trace and evidence
```

The snapshot is sealed at build time and the runtime consumes it unchanged. No behavior enters at
execution time that was not present in the snapshot. Change is a governed transition from one sealed
snapshot to its named successor; the predecessor is retained, never edited in place.

## What makes this different

Most workflow systems orchestrate code. PGC governs behavior itself.

Conventional systems still permit hidden routing, implicit side effects, undeclared execution paths
and logic spread across services. PGC moves those concerns into protocol declarations,
compiler-enforced invariants, closed capability surfaces and a deterministic execution topology.

This is not a framework abstraction. It is a different execution model.

## Why this matters in the AI era

AI generates software faster than humans can reliably govern it.

PGC was designed around one premise:

> AI-generated behavior must not bypass architectural admissibility.

Execution legality is compiled before runtime. Side effects are declared. Routing surfaces are
closed. Traces are immutable. The runtime is deliberately semantic-agnostic, so it cannot invent
undeclared behavior at execution time.

A worker — human or agent — proposes. Governance disposes. Authority sits in the governed artifacts,
the structural validation, the approval gates and the compiler, never in whoever did the authoring.

## The governance space and the execution space

| Space | Responsibility |
|---|---|
| Human Governance Space | Defines what behavior is admissible |
| Machine Execution Space | Executes only what has been declared and compiled |

The inversion is the point. The runtime is not trusted to do the right thing. The compiler constrains
what the runtime is capable of doing at all.

## Evolving the system — governed change

PGC does not stop at governing execution. It governs how the system itself changes.

A change travels a gated pipeline: a plain-language problem statement becomes a design mandate, the
mandate becomes authored artifacts, and the artifacts face the same admission the compiler applies to
everything else. A refused change produces no snapshot and names the rule that refused it. The refusal
is itself an artifact, recorded like an admission.

## What you are looking at

This is the reference ecosystem for Protocol-Governed Computing, and it runs.

- **[Open Standards](/open-standards/)** — the PGC Standard, in the open and under construction,
  argued one claim at a time against a real system.
- **[Papers](/papers/)** — preprints under review at peer-reviewed journals, and the deposited
  foundations they rest on. DOI-published except where a publisher's policy forbids it.
- **[Blog](/blog/)** and **[Learn](/learn/)** — where the ideas are introduced and worked through.
- **[Open Source](https://github.com/protocol-governed-computing)** — the compiler, assembler,
  runtime, inspector, governance surface and business domains, each its own repository. Apache-2.0.

Every published composition is sealed, deposited and citable by DOI, so a claim about what a system
does can be checked against the artifact rather than against a description of it.

## What PGC is not

PGC is not a low-code workflow builder, a BPM engine, an orchestration DSL, a rules engine, an agent
framework or another event bus abstraction.

It is a governed execution substrate.

## Who this is for

- Engineers building high-integrity systems
- Teams integrating AI-generated code safely
- Architects exploring deterministic execution models
- Researchers interested in governed computation
- Anyone curious what software looks like when protocol becomes the source of truth

## One-line summary

> PGC explores what software looks like when protocol — not runtime code — becomes the governing
> authority of execution.

---

*Explore the ecosystem from the menu above.*
