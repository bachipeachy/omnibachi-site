---
title: 'PGC #7 — Build the System, Then Remove the Builder'
date: '2026-08-25'
weight: 7
slug: build-the-system-then-remove-the-builder
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---

# Build the System, Then Remove the Builder

Here is a severe test for a software standard:

Take away the people who built the reference system. Take away its source code. Leave another team
with the standard and ask them to build a conforming implementation.

Could they do it?

If not, the standard may be useful documentation, but it has not escaped the implementation that
gave it birth.

This is not an abstract concern. Every long-lived system eventually loses its original builders.
People change jobs. Vendors disappear. Frameworks are retired. The organization still needs to know
what the system means and how to replace the machinery without replacing that meaning.

## Resemblance is a weak test

The easiest way to make a second implementation is to copy the first one. Match its directories,
names, serialization, process boundaries, and tests. The result may be compatible. It may also
inherit every accidental assumption of the original.

A stronger standard asks for semantic guarantees rather than resemblance.

Two conforming realizations may share no code, language, architecture, or vocabulary beyond the
standard's own terms. One may be centralized; another distributed. One may retain a materialized
representation; another may seal in memory. One may determine a candidate in a single operation;
another may do so incrementally.

The question is not whether the systems look alike. It is whether they preserve the same governed
consequences.

## The independent implementer test

An independent implementer should be able to determine, from the standard:

- what the concepts mean;
- what activities have authority to decide;
- what must be true before execution;
- how refusal behaves;
- what evidence must establish a determination;
- how conformance is evaluated; and
- which choices remain open.

The standard does not need to prescribe every engineering decision. In fact, prescribing those
decisions would make the test weaker. The implementer needs enough semantic precision to know which
decisions are theirs and which would change the meaning.

For example, "determination precedes effect" is a semantic obligation. "Use a compiler process
with three phases" is an implementation recipe. "Nothing enters by discovery" is a property.
"Use static imports" is one technique that may help obtain it.

The distinction is what lets an independent team build differently without guessing what "different"
is allowed to mean.

## How the discovery loop really works

There is an irony in the PGC project: the implementation came first, but the standard cannot depend
on it.

Building the first realization exposed the questions. Intellectual reverse engineering then
separated the concepts the system required from the mechanisms it happened to use. Those concepts
became semantic statements. The statements became normative requirements. The implementation was
then checked back against them.

That is a discovery loop, not a process diary:

```text
realization -> candidate concepts -> semantics -> requirements
      ^                                      |
      |                                      v
      +----------- implementation checked ---
```

The important direction is the return path. Once the standard exists, the realization is evidence
about whether the semantics are satisfiable. It is not the authority that decides what the standard
means.

## What independent implementation reveals

An independent builder is likely to find ambiguity faster than the original team because the
original team carries assumptions the text does not state.

What counts as a complete closure? Is a missing reference refusal or a default? Which evidence is
determinative? Does a profile constrain the environment or the governance? What exactly is included
in a sealed identity? When may a distributed construction claim that its parts compose?

If the standard answers those questions differently in different places, the independent
implementation will expose the conflict. That is valuable. The goal is not to protect the
appearance of completeness. It is to locate the semantics an implementer would otherwise have to
invent.

The [Realization Map](https://github.com/protocol-governed-computing/standards/blob/main/doc/realization_map.md)
supports the same discipline from the other direction. It maps normative requirements to evidence
in one realization, while remaining outside the normative family. A requirement with no convincing
demonstration may be an implementation gap, an unimplementable requirement, or a misunderstanding
of the abstraction. The map does not settle which; it makes the question visible.

## The standard must survive disagreement

An implementation-first discovery loop is not a license to say, "We built it this way, therefore
the standard requires it." That would turn the code into a hidden constitution.

The right response to disagreement is slower:

1. Identify the semantic concept at issue.
2. State what the concept means independently of representation.
3. Ask what requirement follows.
4. Ask how an evaluator could discharge it.
5. Check whether the realization preserves it.

If the implementation fails, the implementation has work to do. If the requirement cannot be
realized without contradiction, the standard has work to do. Neither answer is obtained by
silently changing the other.

## Why this is a useful burden

The independent implementer test imposes a cost on the author. A standard cannot hide behind
familiar code, private context, or "everyone knows what we meant." Terms must be stable. Boundaries
must be semantic. Negative properties must have a way to fail. Claims must name their subject,
profile, revision, and claimant.

That burden is a feature. It moves knowledge from the memories of a founding team into something
that can be inspected, challenged, and re-realized.

It also changes what maintenance means. A replacement runtime is not required to preserve an
internal design. It is required to preserve the governed consequences. A new construction method
is not suspicious because it is unfamiliar. It is suspicious only if it changes what the
declarations authorize.

## AI makes the test more important

AI can already produce a plausible second implementation by copying patterns from the first. That
is not the same as understanding the standard.

A semantics-first specification gives a model, a human team, or both a better target. It says what
must not be inferred, where refusal is required, what evidence must carry, and which mechanisms are
merely examples. It makes it possible to review generated code against meaning rather than against
surface similarity.

The standard still needs human judgment. Independent implementation is not automatic proof of
completeness. But disagreement becomes productive when the text is the object being challenged,
instead of an unwritten intention behind the code.

## Removing the builder

The thought experiment ends where long-lived software begins. Imagine the original builder is
gone, the architecture is obsolete, and the system must be recreated.

If the only path is to excavate the old code, then the code remains the constitution. If the
standard lets a new team derive the same semantic decisions and build a different mechanism, then
the governed meaning has survived its first implementation.

That is the test I want PGC to face in public. The [open standard](https://github.com/protocol-governed-computing/standards)
is not finished merely because the reference realization runs. It becomes stronger when an
independent implementation can disagree about architecture and still agree about meaning.

And that leads to the payoff: one meaning should be able to live in many implementations without
becoming many different systems.
