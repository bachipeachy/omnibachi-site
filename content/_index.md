---
title: "omnibachi"
description: "Protocol-Governed Systems — governing agentic AI and software through compiled, declarative protocol."
---

# Protocol-Governed Systems (PGS)

> Governed by Protocol. Constructed by Compiler. Proven by Trace.
>
> A reference architecture for building deterministic, inspectable, AI-era software systems.

## Why this exists

Modern software has a governance problem.

As systems become distributed, event-driven, AI-assisted, and increasingly machine-generated, the gap between what engineers *intended* and what software is actually *allowed to do* keeps widening.

Behavior hides in orchestration code, runtime conditionals, framework conventions, implicit routing, service glue — and increasingly, in AI-generated implementation details no human reviewed.

PGS explores a different model:

> What if behavior was governed *before execution* instead of inferred *during execution*?

## What is PGS?

PGS is a **Protocol-Governed Execution Architecture** where:

- behavior is declared in governed protocol artifacts
- admissible execution paths are compiled ahead of time
- runtime traversal is deterministic
- undeclared behavior is unreachable
- every execution produces structured evidence

The runtime does not "figure out" what to do. It traverses a precompiled execution graph.

## What makes this different?

Most workflow systems orchestrate code. PGS governs behavior itself.

Traditional systems still allow hidden routing, implicit side effects, undeclared execution paths, runtime interpretation, and logic spread across services.

PGS moves those concerns into protocol declarations, compiler-enforced invariants, federated governance boundaries, and deterministic execution topology.

This is not a framework abstraction. It is a different execution model.

## Why this matters in the AI era

AI can generate software faster than humans can reliably govern it.

PGS was designed around a simple premise:

> AI-generated behavior should not bypass architectural admissibility.

In PGS:

- execution legality is compiled before runtime
- side effects are explicitly declared
- routing surfaces are closed
- execution traces are immutable
- runtime is intentionally semantic-agnostic

The system cannot invent undeclared behavior at execution time.

## What you are looking at

This is the **reference ecosystem** for Protocol-Governed Systems.

It demonstrates:

- governed workflow execution
- compile-time admissibility construction
- federated governance boundaries
- deterministic runtime traversal
- immutable execution traces
- semantic-agnostic execution infrastructure

This is not a toy mockup. The workflows execute end-to-end against real state and produce real traces.

## Core architectural idea

PGS separates software into two distinct spaces:

| Space | Responsibility |
|---|---|
| Human Governance Space | Defines what behavior is admissible |
| Machine Execution Space | Executes only what has already been declared and compiled |

This inversion matters. The runtime is not trusted to "do the right thing." The compiler constrains what the runtime is even capable of doing.

## What happens when you run this?

You will execute real workflows against persistent state.

You will observe:

- deterministic routing
- compile-time constrained behavior
- immutable structured traces
- different outcomes from the same workflow without code changes
- runtime execution without orchestration logic embedded in services

The protocol — not handwritten runtime branching — governs outcomes.

## What PGS is NOT

PGS is not:

- a low-code workflow builder
- a BPM engine
- an orchestration DSL
- a rules engine
- an agent framework
- or another event bus abstraction

It is a governed execution substrate.

## Who is this for?

- Engineers building high-integrity systems
- Teams integrating AI-generated code safely
- Architects exploring deterministic execution models
- Researchers interested in governed computation
- Anyone curious what software looks like when protocol becomes the source of truth

## Architecture highlights

- Compile-time admissibility enforcement
- Federated governance boundaries (FB_*)
- Semantic-agnostic runtime execution
- Deterministic execution graphs
- Immutable execution evidence
- Fully declared side-effect surfaces
- Protocol-first system evolution
- FQDN-based artifact identity
- Governance-constrained compiler behavior
- Governance-first change management — every change is a governed Change Request → Authoring Mandate dossier; authoring is interchangeable, authority is not ([`pgs_change_mgmt`](https://github.com/bachipeachy/pgs_change_mgmt#readme))

## Open source

PGS is released under Apache-2.0.

The goal is not to create a closed platform. The goal is to explore whether software systems can become more governable, more inspectable, and more deterministic — without sacrificing extensibility.

## Evolving the system — governed change

PGS does not stop at governing execution; it governs **how the system itself changes**. Every protocol change travels a governed, gated pipeline — from a plain-language Change Request to an Authoring Mandate — producing a complete, reviewable dossier *before* any artifact is authored.

The pipeline is **governance-first and authority-invariant**: a stage may be drafted by a human or an automated agent, but authority resides in the governed artifacts, structural validation, approval gates, and the compiler — never in the author. *The actor proposes; governance disposes.*

## One-line summary

> PGS explores what software looks like when protocol — not runtime code — becomes the governing authority of execution.

---

*Explore the ecosystem from the menu above — Blog, Papers, Book, Learn, and Open Source.*
