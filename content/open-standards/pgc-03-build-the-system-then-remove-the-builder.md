---
title: 'PGC #3 — Build the System, Then Remove the Builder'
date: '2026-08-25'
weight: 3
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

There is an irony in the Protocol-Governed Computing (PGC) project: the implementation came first, but the standard cannot depend
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

## I ran a cheaper version of this test

Building a second implementation is expensive. There is a cheaper experiment that tests the same
thing, and I have now run it twice.

Give a competent reader the standard and nothing else. No source code. No architecture. No previous
attempt. No answers from me about what the standard requires — only logistics. Then ask them to
write a conformance profile: the document that decides everything the standard deliberately leaves
open.

The rules are strict because the value depends on them. The reader may not consult the
implementation. They may not see what an earlier reader produced. And when they get stuck, they may
not ask me to resolve it — they record the question and decide it themselves.

**That log of questions is the actual result.** The profile is just the reason to produce it.

Both readers produced profiles that hold up. Neither needed a concept the standard does not have.
Neither got stuck. That is the good news, and it is the weaker half of what I learned.

## The result I did not expect

Of the twenty-eight changes in the current revision, **eighteen came from readers who did not build
the system.** That alone would justify the exercise.

But the sharpest finding came from a reader who reported nothing wrong.

Their questions log ended with a clean bill of health: no missing decisions, nothing the standard
failed to answer. Then I read their profile against the documents — and six of those eighteen
changes came from gaps that reader had walked straight over. They had quietly invented an answer
each time, sensibly, and never noticed they were inventing.

The lesson is uncomfortable and worth stating plainly:

> **A reviewer reporting no problems is not evidence that a specification is complete. It may only
> be evidence that the specification does not signal where it is silent.**

Every one of those six was a place where the standard left something open and gave the reader no way
to tell whether the silence was deliberate. A confident reader fills it in. A specification that
depends on readers being unconfident is not finished.

That is why the profile has to be read against the documents, not just accepted. And it is why I
would rather have hostile readers than agreeable ones.

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

The test imposes a real cost on the author. A standard cannot hide behind familiar code, private
context, or "everyone knows what we meant." Terms must be stable. Negative properties must have a
way to fail.

That burden is the feature. It moves knowledge out of a founding team's memory and into something
that can be inspected, challenged, and rebuilt.

It also changes what maintenance means. A replacement runtime is not required to preserve an
internal design. It is required to preserve the governed consequences. A new construction method
is not suspicious because it is unfamiliar. It is suspicious only if it changes what the
declarations authorize.

## Removing the builder

The thought experiment ends where long-lived software begins. Imagine the original builder is
gone, the architecture is obsolete, and the system must be recreated.

If the only path is to excavate the old code, then the code remains the constitution. If the
standard lets a new team derive the same semantic decisions and build a different mechanism, then
the governed meaning has survived its first implementation.

That is the test I want PGC to face in public. The [open standard](https://github.com/protocol-governed-computing/standards)
is not finished merely because the reference realization runs. It becomes stronger when an
independent implementation can disagree about architecture and still agree about meaning.

The next article turns to what makes that hard in the first place — the way implementation quietly
becomes the real policy, until the code is the only place the rules actually live.

---

**The standard is open, and I am looking for people to attack it — not endorse it.**

What it claims, what would prove it wrong, and what has *not* yet been established are all set out
in the [call for review](https://github.com/protocol-governed-
computing/standards/blob/main/doc/call_for_review.md). **Read it and tell me where you would have
to invent something.** That is the most useful thing anyone can send me, and it takes an afternoon
rather than a project.

Objections, counter-examples, and serious technical criticism: **bachipeachy@gmail.com**
