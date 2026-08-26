---
title: 'PGC #8 — One Meaning, Many Implementations'
date: '2026-08-25'
weight: 8
slug: one-meaning-many-implementations
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---

# One Meaning, Many Implementations

Every long-lived software system eventually faces the same bargain.

Keep the old machinery because nobody can prove what may change, or replace it and hope the new
machinery means the same thing.

That is a poor bargain. It confuses a system's identity with the tools that first realized it.

The central promise of Protocol-Governed Computing (PGC) is more ambitious: one semantic meaning, many
implementations.

## The recipe is not the meal

Imagine two kitchens preparing the same dish. One uses a gas range and cast iron. The other uses
induction and stainless steel. Their tools, timing, and internal arrangement differ. What matters
for the shared recipe is the resulting dish and the conditions that define it.

Software standards often make the opposite mistake. They describe the kitchen and call it the
recipe. A framework, data layout, process topology, or reference codebase becomes the thing a
replacement must resemble.

That makes change expensive and conformance shallow. A team can copy the shape without preserving
the governing property, while a team that preserves the property through a different architecture
can be rejected for being unfamiliar.

PGC starts from semantics instead.

## What remains fixed

The PGC Standard does not require every implementation to share a stack. It requires the meaning
to survive the change in stack.

A conforming realization must preserve properties such as:

- behavior originates in declaration;
- authority does not come from position, containment, or load order;
- determination precedes effect;
- every applicable rule in a bounded closure is evaluated;
- an unknown closure refuses rather than becoming permission;
- refusal leaves no governed residue;
- execution consumes a sealed, verified representation;
- nothing enters by discovery;
- evidence can establish what was determined and what occurred.

These are properties of governed computation, not a preferred repository arrangement. One
implementation may obtain them with a compiler and immutable snapshot. Another may use a
distributed service or an in-memory representation, provided the semantic obligations still hold.

The architecture is allowed to vary. The meaning is not.

## Conformance by properties

This is why the Conformance Model says conformance is over observable semantic guarantees, never
over resemblance to a realization.

A second runtime need not copy the first runtime's internal modules. It must consume an accepted
snapshot, make no governing determination of its own, add no undeclared behavior, and produce the
same governed consequences for the same governed inputs.

A second construction method need not use the same stages. It must determine admissibility,
resolve what execution depends on, produce a complete authorized representation, and refuse without
usable output when it cannot establish those facts.

The evaluator picks the method that suits the property — and for substitutability there is only one
that works: run the same snapshot somewhere else and compare. **Nothing you can observe about a
single implementation establishes that a second one would agree with it.**

This is a more demanding form of openness than publishing source code. It lets implementations
differ while making their differences answerable to the same semantic test.

## Why snapshots matter

The snapshot is the practical bridge between stable meaning and changing machinery. It is a sealed,
complete, content-identified representation of a governed system. Execution consumes it after
integrity, identity, totality, and profile have been verified.

That does not mean a snapshot contains every physical resource an execution might use. The
environment still supplies compute, storage, and scheduling. It means governed behavior and
declared dependencies are not smuggled in from that environment.

A replacement runtime can therefore be judged against the same sealed representation. If the
governed consequence changes, at least one realization has failed the claim. If only timing,
placement, or other observational details change, the semantic result may still be equivalent.

This gives "portability" a precise meaning. What travels is not just code. It is a representation
whose governed content can be identified, inspected, and re-used.

## Why this matters for AI

AI-generated software makes implementation cheap and semantic continuity expensive.

A model can translate a service from one language to another, split a process into several, or
replace a database. It can also add a default, discover an unlisted plugin, interpret an
unexpected outcome, or move an authority decision into runtime code while preserving the visible
happy path.

Without an explicit semantic contract, those changes are difficult to distinguish from ordinary
refactoring. With one, the questions become sharper:

Did the declarations change?

Did the applicable closure change?

Did the determination move or acquire a new input?

Can the same evidence establish the same governed consequence?

Did a new implementation preserve the invariant, or merely imitate the old files?

PGC does not assume AI will answer these questions correctly. It makes them explicit enough to
ask.

## Long-lived systems need substitutability

A system that cannot replace its runtime, construction method, or external capability without
changing governed meaning is tied to an implementation, whether or not its documentation says
otherwise.

PGC approaches substitutability through declared surfaces and contracts. A capability exposes an
enumerated interface and outcomes; execution does not see the mechanism beneath it. A domain
boundary declares what is reachable. Effects occur only through declared surfaces.

This does not make every implementation interchangeable in cost, speed, or operational behavior.
It makes the relevant question narrower and more useful: do they produce the same governed
consequences under the same profile, revision, snapshot, inputs, and initial state?

Equivalence is about what is determined, not how the determination was obtained.

## The discipline of one meaning

One meaning does not mean one frozen interpretation. The standard itself can be revised, and a
revision is declared against a named predecessor. A conformance claim names the revision and
profile against which it was evaluated.

That discipline keeps semantic change visible. A representation can change without changing
meaning. An implementation can change without changing conformance. But when meaning changes, the
governed transformation and its consequences must be acknowledged.

Otherwise a "replacement" is quietly a new constitution.

## The open question

PGC is an open standard because the hardest test is outside the reference implementation. Can a
different team, using different tools, construct a system whose behavior is governed by the same
meaning? Can an evaluator establish that without trusting resemblance? Can the system refuse when
governance is unknown, and prove what it was allowed to do when it proceeds?

Those questions are intentionally larger than a code sample.

The [PGC Standards repository](https://github.com/protocol-governed-computing/standards) contains
the normative documents. The broader work and technical papers are available at
[OmniBachi](https://omnibachi.org/). The documents are dense because an open standard has to say
where interpretation ends and invention begins.

The payoff is simple to state:

> A system should be able to change its architecture without changing what it means to be
> governed.

That is the possibility PGC is trying to make real: one semantic meaning, many architectures,
many languages, many teams, and enough evidence to tell the difference between a new mechanism and
a new system.

---

**The standard is open, and I am looking for people to attack it — not endorse it.**

What it claims, what would prove it wrong, and what has *not* yet been established are all set out
in the [call for review](https://github.com/protocol-governed-
computing/standards/blob/main/doc/call_for_review.md). If you have replaced a runtime, a
framework, or a database and could not prove the governed meaning survived, that is the problem
this standard exists to make tractable.

Objections, counter-examples, and serious technical criticism: **bachipeachy@gmail.com**
