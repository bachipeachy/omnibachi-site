---
title: 'PGC #2 — Software Works—So Why Can’t We Explain It?'
date: '2026-08-25'
weight: 2
slug: software-works-so-why-cant-we-explain-it
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---

# Software Works—So Why Can't We Explain It?

There is a moment in every old software system when someone asks a reasonable question and the
room goes quiet.

Why was this request allowed?

Which rule made that route available?

What would happen if we replaced this service?

Usually, the system is still running. The dashboards are green. Customers are being served. The
question is not whether the software works. The question is whether anyone can explain what it is
doing, in terms that do not depend on remembering a particular codebase.

That gap is where PGC begins.

## Working is not the same as being intelligible

We often use successful behavior as a shortcut for understanding. If a payment went through, we
assume the authorization was correct. If a deployment passed, we assume the checks meant
something. If a workflow reached the expected screen, we assume its rules are still intact.

But an outcome tells us only what happened. It does not, by itself, tell us what was permitted,
which authority permitted it, or whether the same outcome would survive a change in implementation.

A system can produce the right answer for years while its governing meaning becomes scattered
across code paths, defaults, configuration, deployment order, and institutional memory. It may be
reliable in the narrow operational sense and unintelligible in the larger organizational sense.

That distinction matters whenever software must outlive its authors.

## The question behind the question

Suppose a loan application is approved. A conventional audit might collect logs, inspect a few
functions, and ask an engineer to explain the decision. That can establish that an approval
happened. It may not establish what the system was allowed to consider, what rules applied, or
whether a missing rule was silently treated as permission.

PGC asks a more demanding question:

> What makes this a governed decision rather than an event that happened to have a good result?

The answer is not a larger log file. It is a different model of the system.

In the PGC Standard, a governed system carries its governing semantics as explicit,
machine-consumable declarations. Those declarations determine what may be constructed and what
may be executed. The code still performs the work, but it is no longer the only place where the
system's authority is hidden.

The standard is trying to make meaning portable.

## Three questions that should not be collapsed

The first part of the standard separates three questions that ordinary software discussions often
mix together:

1. **What are the concepts?**
2. **What do those concepts mean when a system changes?**
3. **What must remain true of any implementation?**

The distinction is practical. A declaration is not documentation. Documentation describes a
decision made somewhere else; a declaration is the governed statement the system consumes.
Presence is not admission. A file sitting in a directory has not necessarily become part of the
system. Authority is not ownership, and neither is supplied by position or proximity.

Without stable distinctions, every later conversation becomes an argument over vocabulary. With
them, a team can ask where a decision belongs and what evidence could establish it.

## A small thought experiment

Imagine two teams implementing the same travel-booking protocol. One uses a monolith and a
relational database. The other uses services, immutable objects, and a different language.

If the protocol is only a description of the first system, the second team must reverse-engineer
meaning from behavior. It may reproduce the happy path while changing an edge case no one knew was
governed. The two systems look similar until a dispute arrives.

If the protocol defines the semantic obligations instead, both teams can choose different
mechanisms while preserving the same answer to the important questions: what is admitted, what
must be refused, what transitions are possible, and what evidence establishes the result.

This is why PGC insists that the standard specify meaning rather than mechanism. A component name,
repository layout, or processing stage may be useful in one realization. None is automatically a
semantic concept.

## The shape of a governed change

The Semantic Model gives every governed change the same basic shape. There is a current governed
state, a proposal, a governance closure that establishes which rules apply, a determination, a
resulting state, and evidence.

The proposal is not yet a change. It is a request for one.

The determination comes before the effect. Every applicable rule is evaluated. The result is
admit, constrain, or refuse. If the applicable governance cannot be established, the answer is
not "nothing applies." It is refusal. An unknown closure is not an empty closure.

That structure makes a change explainable without pretending that explanation is an after-the-fact
story. The evidence must carry enough information for someone who was not present to establish
which closure applied, which rules were evaluated, what they yielded, and what consequence
followed.

## Why the implementation is still important

None of this makes implementation irrelevant. The implementation is where semantics become
observable. It must construct the authorized representation, execute only what that
representation determines, and preserve the boundaries the standard names.

But the implementation is not allowed to become the meaning by default.

That is the difference between a system that happens to be understandable to its maintainers and
one whose governing identity can be examined by an independent party. The former depends on
context. The latter has something durable to point to.

PGC calls the required properties architectural invariants, but the phrase does not mean a
prescribed stack. It means truths such as: behavior originates in declaration; authority is not
ambient; determination precedes effect; nothing enters by discovery; a sealed representation
cannot change; and refused work leaves no governed residue.

These properties can be realized in many ways. The properties, not the techniques, are what matter.

## Why this becomes urgent with AI

AI-assisted development changes the economics of implementation. More code can be generated,
modified, and replaced than any one team can fully explain by reading line by line.

That makes the old assumption increasingly dangerous: that the code is the specification and
understanding will follow later.

A model can produce a plausible authorization path without knowing which authority it is supposed
to represent. It can add a fallback that keeps a demo running while turning an unknown condition
into permission. It can preserve visible behavior while quietly changing what the system is
allowed to mean.

An explicit semantic contract does not eliminate those risks. It gives them somewhere precise to
be found.

## Where to look next

Part I of the [PGC Standards](https://github.com/protocol-governed-computing/standards) develops
this foundation through the Conceptual Model, Semantic Model, and Architectural Invariants. The
documents are denser than this essay because the distinctions have to survive implementation,
inspection, and disagreement.

The question to carry forward is simple:

> When software works, can we explain not only what it did, but why it was allowed to do it?

That is the standard PGC is trying to make possible. And once that question is taken seriously,
the next danger becomes visible: code does not merely implement authority. Over time, it can begin
to impersonate it.
