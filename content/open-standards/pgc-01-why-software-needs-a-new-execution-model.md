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
We have never been better at building software. We have never been worse at saying what it is
allowed to do.

Languages, frameworks, cloud platforms, CI/CD, observability, and now AI assistants that write code
faster than anyone can review it — and maintaining a large business system over decades remains
extraordinarily difficult.

The problem is not that we cannot write algorithms. The problem is everything surrounding the
algorithms. Business software accumulates rules, policies, workflows, authorizations, constraints,
interfaces, exceptions, regulatory requirements, and institutional knowledge — and over time, much
of that meaning becomes embedded in implementation code.

The software works. But understanding **what it is allowed to do, and proving that it still does
what it is supposed to do, becomes progressively harder.**

I think we need to approach that problem differently.

> **What if the software's governing meaning came first?**

That is the premise behind **Protocol-Governed Computing (PGC)**: an architectural approach in which
the governing semantics of a system are expressed explicitly as a protocol, and separated from the
mechanisms that realize them.

> **The standard specifies what must be true. The implementation decides how to make it true.**

This sounds obvious. In practice it is surprisingly difficult. Specifications routinely drift toward
describing architectures, components, data structures, and implementation conventions — and once
that happens, an implementation quietly becomes the de facto specification.

PGC exists to prevent that inversion.

## PGC is not another way to write algorithms

This qualification matters, because a model presented as *how all software should be written* is
correctly judged as overreach.

PGC is not about making computational functions easier to write. It is aimed at the larger and far
more expensive problem of long-lived business software: systems that evolve through years of
organizational, regulatory, and operational change.

Think of the lifecycle as:

**intent → requirements → governance → design → implementation → execution → inspection → change → retirement**

The goal is to make the governing semantics explicit across all of it. The computational function
still has to exist — but it should not be the place where the system's authority, policy, and
governance quietly hide.

## Why this becomes urgent with AI

If an AI system can generate large amounts of implementation code, then generating code is no longer
the hard part. The harder questions arrive right after:

- What was the AI allowed to build?
- What rules govern the resulting system?
- How do we know the implementation still corresponds to those rules?
- Can another implementation replace it without changing the governed meaning?

Those questions need something more durable than source code. They need an explicit semantic
contract — which is what PGC attempts to provide.

## Machine-processable, but written for humans

The PGC Standard occupies an unusual middle ground. It is **human-centric**: the concepts and
distinctions are meant to be understood and argued about by people. It is also
**machine-processable**: every normative requirement is structured and numbered so it can become an
object of traceability, analysis, and eventually automated conformance checking.

The objective is not to turn a standard into code. It is to make the semantics precise enough that
machines can help enforce them without replacing human understanding.

## The standard came after the implementation

Here is the unusual part of the project: the PGC reference implementation existed before the
standard did.

Rather than simply documenting what I had built, I used **intellectual reverse engineering** to
separate the abstractions that were genuinely fundamental from the mechanisms that merely happened
to be there. Only those abstractions became the basis for the normative standard.

Why go to that trouble? Because of a specific danger:

> **You end up standardizing the implementation rather than the idea.**

A component that happens to exist in Python is not necessarily a semantic concept. A repository
boundary is not necessarily an architectural boundary. An encoding is not necessarily part of the
protocol. A compiler stage is not necessarily a normative phase.

PGC tries to draw every one of those lines explicitly.

## The test: can a standard escape its own implementation?

Which leads to the most important test of the whole effort.

Suppose the reference implementation disappeared tomorrow. Could an independent team read the PGC
Standard and build a conforming system without ever seeing the original code?

If the answer is no, the standard has not escaped its implementation — it is documentation wearing a
specification's clothes.

I have since run a cheaper version of that test on real readers, and it changed the standard in
eighteen places. That story is article #3, including the part I did not enjoy writing.

## The open draft

The **Protocol-Governed Computing Standard** is open, and at a frozen revision you can cite:

- **The standard** — <https://github.com/protocol-governed-computing/standards>
- **Where to start** — the [call for review](https://github.com/protocol-governed-computing/standards/blob/main/doc/call_for_review.md),
  which states what is claimed, what would prove it wrong, and what has *not* yet been established
- **The technical papers** — <https://omnibachi.org/>

This is deliberately a draft, not a declaration that the work is finished. I would like to see it
challenged — not merely edited. **Challenged.**

- Can you find a semantic distinction that does not hold?
- Can you find a place where the standard accidentally dictates an implementation?
- Can you derive something from it that I did not intend?
- Can you find a missing semantic obligation?

Those are the criticisms that make this work better, and they are worth considerably more to me than
agreement. The call for review is deliberately blunt about the standard's own weak points — including
the one thing this project structurally cannot supply for itself.

## A Series, Not a Finished Argument

This is the first article in a series exploring the questions behind PGC and the assumptions it asks us to reconsider.

In the next articles, I plan to explore questions such as:

### #2 — Software Works—So Why Can't We Explain It?

How a system can function correctly while its rules, authority, and limits become increasingly
difficult to understand.

### #3 — Build the System, Then Remove the Builder

I gave the standard to readers who had never seen the code and asked them to use it. What came back
changed the standard — and one clean bill of health turned out to be the most useful failure of all.

### #4 — When Code Becomes the Constitution

How implementation quietly becomes the real specification—and why that makes long-lived systems
difficult to govern or replace.

### #5 — The Rule That Was There but Did Nothing

Why declared, implemented, enforced, and demonstrated are four different conditions, not four words
for the same thing.

### #6 — What If Refusal Is Success?

Why rejection and fail-hard behavior can be correct outcomes rather than failures of the system.

### #7 — Can Software Prove What It Was Allowed to Do?

What evidence, provenance, determination, and conformance add to the meaning of a governed system.

### #8 — One Meaning, Many Implementations

How a semantics-first standard can allow architectures, languages, tools, and teams to change
without losing the system's governed identity.

---

Comments, objections, and serious technical criticism are welcome.

**bachipeachy@gmail.com**
