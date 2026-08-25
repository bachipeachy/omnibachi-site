---
title: 'PGC #1 — Why Software Needs a New Execution Model'
date: '2026-08-23'
weight: 1
slug: a-different-way-to-specify-software-development-standard
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---

# Why Software Needs a New Execution Model

For decades, we have become very good at writing software.

We have programming languages, frameworks, databases, cloud platforms, DevOps, CI/CD, microservices, containers, orchestration, observability, and now increasingly capable AI coding assistants.

And yet, maintaining a large business system over decades remains extraordinarily difficult.

The problem is not that we cannot write algorithms.

The problem is everything surrounding the algorithms.

Business software accumulates rules, policies, workflows, authorizations, constraints, interfaces, exceptions, regulatory requirements, and institutional knowledge. Over time, much of that meaning becomes embedded in implementation code.

The software works.

But understanding **what it is allowed to do—and proving that it continues to do what it is supposed to do—becomes increasingly difficult.**

I think we need to approach that problem differently.

> **What if the software's governing meaning came first?**

That is the premise behind **Protocol-Governed Computing (PGC)**.

PGC is an architectural approach in which the governing semantics of a system are expressed explicitly as a protocol and separated from the mechanisms that realize them.

The distinction is fundamental:

> **The standard specifies what must be true. The implementation decides how to make it true.**

This sounds obvious.

In practice, it is surprisingly difficult.

Specifications routinely drift toward describing architectures, components, data structures, programming techniques, and implementation conventions. Once that happens, an implementation can become the de facto specification.

PGC attempts to prevent that inversion.

## PGC Is Not Another Way to Write Algorithms

This is an important qualification.

PGC is not primarily about making computational functions easier to write.

It is aimed at the much larger—and more expensive—problem of long-lived business software: systems that evolve through years of organizational, regulatory, and operational change.

Think of the lifecycle as:

**intent → requirements → governance → design → implementation → execution → inspection → change → retirement**

The objective is to make the governing semantics explicit across that lifecycle.

The computational function still needs to exist.

But the function should not be the place where the system's authority, policy, or governance semantics quietly hide.

## A Different Relationship Between Humans, Machines, and Specifications

There is another premise behind PGC that becomes particularly important in the age of AI-assisted software development.

If an AI system can generate large amounts of implementation code, generating code is no longer the hardest part.

The harder questions become:

- What was the AI allowed to build?
- What rules govern the resulting system?
- How do we know that the implementation corresponds to those rules?
- Can another implementation replace it without changing the governed meaning?

Those questions require something more durable than source code.

They require an explicit semantic contract.

That is what PGC attempts to provide.

## Machine-Processable, but Still Written for Humans

The PGC Standard is deliberately written to occupy an unusual middle ground.

It is **human-centric**: the concepts and distinctions are intended to be understandable and reasoned about by people.

But it is also **machine-processable**: normative requirements are explicitly structured and numbered so that they can become objects of traceability, analysis, validation, and eventually automated conformance mechanisms.

The objective is not to turn a standard into code.

It is to make the semantics precise enough that machines can participate in enforcing and validating them without replacing human understanding.

That distinction is central to PGC.

## The Standard Came After the Implementation

There is another unusual aspect of the project.

The PGC Reference Implementation existed before the standard.

Rather than simply documenting the implementation, I deliberately used **intellectual reverse engineering** to identify the abstractions that were fundamental to the system and separate them from implementation-specific mechanisms.

Only then did those abstractions become the basis for the normative standard.

Why?

Because otherwise there is a serious danger:

> **You end up standardizing the implementation rather than the idea.**

A component that happens to exist in Python is not necessarily a semantic concept.

A repository boundary is not necessarily an architectural boundary.

A particular encoding is not necessarily part of the protocol.

A compiler stage is not necessarily a normative phase.

PGC tries to draw those lines explicitly.

## The Test: Can the Standard Escape Its Own Implementation?

This leads to perhaps the most important test of the entire effort.

Suppose the Reference Implementation disappeared.

Could an independent team read the PGC Standard and build a conforming implementation without access to the original code?

If the answer is no, then the standard is not really independent of its implementation.

That is the standard I am trying to build.

And this is why I am releasing the draft now.

## The First Open Draft

The first open-source draft of the **Protocol-Governed Computing Standard** is now available.

**PGC Standards — GitHub**  
https://github.com/protocol-governed-computing/standards

The deeper technical papers and background are available here:

**PGC technical papers — OmniBachi**  
https://omnibachi.org/

This is deliberately a draft, not a declaration that the work is finished.

In fact, I would like to see the standard challenged.

Not merely edited.

**Challenged.**

Can you find a semantic distinction that does not hold?

Can you find a place where the standard accidentally dictates an implementation?

Can an independent implementer derive something that the standard's authors did not intend?

Can you find a missing semantic obligation?

Those are the criticisms that will make this work better.

## A Series, Not a Finished Argument

This is the first article in a series exploring the questions behind PGC and the assumptions it asks us to reconsider.

In the next articles, I plan to explore questions such as:

### #2 — Software Works—So Why Can’t We Explain It?

How a system can function correctly while its rules, authority, and limits become increasingly difficult to understand.

### #3 — When Code Becomes the Constitution

How implementation quietly becomes the real specification—and why that makes long-lived systems difficult to govern or replace.

### #4 — The Rule That Was There but Did Nothing

Why declared, implemented, enforced, and demonstrated are four different conditions, not four words for the same thing.

### #5 — What If Refusal Is Success?

Why rejection and fail-hard behavior can be correct outcomes rather than failures of the system.

### #6 — Can Software Prove What It Was Allowed to Do?

What evidence, provenance, determination, and conformance add to the meaning of a governed system.

### #7 — Build the System, Then Remove the Builder

Why the real test of a standard is whether an independent team can implement it without access to the original code.

### #8 — One Meaning, Many Implementations

How a semantics-first standard can allow architectures, languages, tools, and teams to change without losing the system’s governed identity.

---

Comments, objections, and serious technical criticism are welcome.

**bachipeachy@gmail.com**
