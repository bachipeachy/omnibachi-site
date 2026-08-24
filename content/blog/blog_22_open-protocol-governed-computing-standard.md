---
title: '#22 — A Draft Open Standard for Protocol-Governed Computing'
date: '2026-08-23'
weight: 22
slug: open-protocol-governed-computing-standard
series:
- Protocol-Governed Systems
tags:
- PGS
- PGC
cover:
  image: /assets/blog_22.jpg
  alt: A Draft Open Standard for Protocol-Governed Computing
---

The first open draft of the Protocol-Governed Computing (PGC) Standard is now available for public
scrutiny. It is an attempt to address a problem that becomes increasingly expensive as business
software grows older: how to preserve the governing meaning of a system while allowing its
implementation to change.

![One protocol, many implementations — a standard that fixes what must be true and leaves open how to
make it true](/assets/blog_22.jpg)

That picture is the whole idea in one frame. On the left, the governed meaning of a system: stable,
explicit, written down. On the right, every language and runtime anyone might choose to realize it
in. The protocol is the bridge, and it is deliberately narrow — it says *what must be true*, and says
nothing about which road you take to make it true.

It is a draft on purpose. I am not looking for applause. I am looking for people who can find where
the ideas are wrong, incomplete, ambiguous, or more complicated than they need to be.

## Why another software standard?

PGC is aimed at a different problem from writing algorithms.

The hard systems are long-lived business systems whose value accumulates over years: business rules,
workflows, policies, authorizations, interfaces, operational constraints, regulatory requirements,
exceptions, institutional knowledge. Over time most of that meaning ends up embedded in
implementation code.

The result is familiar. The system works, and becomes progressively harder to understand, verify,
change, and eventually replace.

PGC starts somewhere else:

> The governing meaning of a software system should be explicit, machine-processable, and independent
> of the mechanism that implements it.

The ambition is not to replace algorithms or programming languages. It is to give long-lived business
software a different foundation for being built, governed, executed, inspected and evolved.

## A standard about semantics, not implementation

The central design decision is that the standard does not say how an implementation must be built. It
says what things mean and what must be true.

That sounds simple and is surprisingly hard to hold. A specification drifts easily into architecture —
*use this component, this database, this serialization, this pipeline* — and once it does, you have an
implementation recipe rather than an open standard.

So PGC specifies semantic obligations and leaves technique open. It defines governed state, authority,
governance, closure, determination, refusal, execution, capabilities, snapshots, profiles, inspection
and conformance, while deliberately declining to make today's implementation structure normative.

## Machine-processable, still written for humans

The normative requirements are explicitly structured and numbered, so each requirement can be
identified, traced, analyzed, and eventually processed by conformance machinery.

The numbering is not there to replace human reasoning. The objective is the opposite:

> Make the semantics precise enough that machines can participate in the reasoning without removing
> humans from it.

This matters most in AI-assisted development. If AI is going to construct and modify substantial
software, code generation is no longer the hard part. The hard part is expressing what the resulting
system is *allowed to mean and do*, independently of whatever code an AI happens to produce.

## The unusual part: the implementation came first

There is another aspect of how PGC was developed that I think matters, because it is the opposite of
how standards are usually written.

The standard was not invented in isolation and then followed by an implementation. **The Reference
Implementation came first.**

It was then intellectually reverse-engineered to separate the abstractions that were actually
fundamental from those that were artifacts of one implementation. Only those became normative.

In other words, the standard was not designed by simply documenting the codebase. The implementation
was treated as evidence from which candidate abstractions could be extracted, challenged, and
separated from accidental implementation structure.

```
Reference implementation
        ↓
Intellectual reverse engineering
        ↓
Semantic abstractions
        ↓
Normative standard
        ↓
Reference implementation mapped back
        ↓
Gaps and anomalies exposed
        ↓
Standard / implementation refined
```

This was deliberate, and it guards against the classic standards failure: **mistaking an
implementation technique for a fundamental concept.** A component that happens to exist in Python is
not necessarily a semantic concept. A repository boundary is not necessarily an architectural
boundary. A compiler stage is not necessarily a normative phase.

## The Realization Map

That loop produced the project's most interesting artifact: a structured correspondence between each
normative requirement and where the Reference Implementation actually realizes it.

It goes further than traceability, because an apparent mismatch can turn out to be an implementation
gap, an implementation *stronger* than the standard requires, an intentional exception, a false
positive — or a defect in the standard itself.

So it is not a coverage checklist. It is a way of testing the abstraction boundary from both sides.

It therefore provides a form of implicit validation: the implementation is continually challenged
against the semantics of the standard, even where no conventional conformance test was written for
the discrepancy.

## What it actually found

The map covered 25 normative documents and classified 298 invariants. Sixty percent were demonstrated
cleanly. The interesting part is the other forty percent, and before the numbers, here is what they
mean in plain terms.

A rule can exist in four different states, and they are easy to mistake for one another:

- **Declared** — somebody wrote the rule down.
- **Implemented** — code exists that is supposed to carry it.
- **Enforced** — that code can actually refuse something.
- **Demonstrated** — it has been observed refusing something.

A system can sit in any one of those states and still present itself as though it were in the last.
The rule is written, a check exists,
the build reports it passed — and nothing anywhere has ever been turned away by it. From the outside
that is indistinguishable from working governance.

> **Declared ≠ implemented ≠ enforced ≠ demonstrated.**

Four instances, all measured rather than suspected:

**Checks that could not refuse.** Of 87 compile-time checks, **14 had no path that produces a
refusal**. Ten said so in their own source comments — *"Phase 1 stub — full enforcement in Phase 3"* —
enforcement described and never written. All fourteen declared that a violation fails the build
immediately. All fourteen ran on every build and reported passed, indistinguishable in the record from
the seventy-three that can refuse. The guarantee that every obligation has a check was satisfied by a
check that carries nothing.

**An identity that measured the clock.** A composition's identity is computed over the bytes of
everything it carries, so that tampering and relocation are detectable. Two builds of unchanged source
wrote ninety-one files each; ninety were byte-identical. The ninety-first differed in one field: a
microsecond timestamp recording when the build ran, which nothing reads. **Every pin in the workspace
expired on the next rebuild** — twenty of twenty-two could not be verified — and a genuine alteration
was indistinguishable from a no-op recompile.

**A conformance profile nobody read.** Twenty-three of its thirty-five required artifacts no longer
resolved. A second profile resolved all thirty-five. **Nothing distinguished them, because nothing read
either one.**

**Coverage that was not governance.** A third of the composition was validated against no schema at
all. Worse, one artifact kind *was* dispatched to a schema — one that required no field and closed no
surface. Thirty-three declarations passed it because everything passes it, and the kind read as
governed to anyone counting dispatched kinds.

That last one is the general lesson. **More coverage is not automatically more governance**, and a
count cannot tell the difference.

## The part that justifies the whole exercise

The map also found defects in the standard.

`4e` requires that a superseded identity be referenced by nothing — *"the requirement is strict: no
reference, not no executable reference."* It also requires the supersession relation to be declared on
the successor, in the form `supersedes: <predecessor identity>`.

Read together and literally, **a conforming supersession is impossible**: one rule mandates the single
reference the other forbids.

This was not found by reading the two rules in isolation. The contradiction surfaced when the
implementation attempted to realize them literally: it carved out exactly the necessary exception in
code and wrote down why — because without it nothing can ever be superseded. The map found the
exception afterwards.

The conclusion was that the realization needed no change. **The document did.** Three normative
revisions followed.

That is what makes the map worth having. Not the checklist — the pressure.

## Implicit validation

Conformance testing asks: *does the implementation pass the prescribed tests?*

The map asks a different question: *does the implementation actually correspond to the semantics the
standard claims to define?*

Those are not the same question. Conformance testing checks whether known obligations have been
discharged. The Realization Map additionally asks whether the abstraction embodied by the
implementation actually corresponds to the semantics claimed by the standard.

That second question is what exposed the discrepancies described above. Running probes
against the realization repeatedly overturned findings that had looked convincing from document or
source inspection alone — including one where a reported fifty-one violations turned out to be the
character count of a string.

## Why publish now

Because the standard is not finished.

A standard of this kind cannot be validated by its authors. The dangerous defects are not obvious
omissions; they are semantic distinctions that look reasonable individually and break when someone
tries to implement them independently.

So the real test is:

> **Can someone who did not build the Reference Implementation read the standard and independently
> build a conforming system without having to invent missing semantics?**

That is ultimately the test of whether PGC is a standard rather than a description of one
implementation.

That question has not been answered. It needs independent eyes.

## What I would like challenged

Please don't stop at grammar. I am after harder objections:

- Is a semantic distinction actually necessary, or are two concepts conflated?
- Does a rule specify meaning, or prescribe an implementation technique?
- Is an obligation actually enforceable — and by what?
- Can an independent implementation derive the intended behaviour?
- Is something claimed as governance really governance?
- Are there hidden assumptions about execution environments?
- Does the standard accidentally privilege the Reference Implementation?
- Is there a place where an implementer must invent semantics to proceed?

In short: **try to break the abstractions.** If they survive, the standard gets stronger.

## The draft

- [PGC Open Standard — GitHub](https://github.com/protocol-governed-computing/standards)
- [PGC technical papers — OmniBachi](https://omnibachi.org/)

This is where I need people who know software architecture, programming languages, distributed
systems, governance, formal methods, AI-assisted development — or who have simply spent years keeping
a large business system alive.

Read it critically. Try to find the holes.

The objective is not to prove PGC right. It is to find out whether the underlying ideas are strong
enough to become an open, implementation-independent standard for building software that has to
outlive the people who wrote it.

Comments, questions, objections and serious criticism are very welcome — bachipeachy@gmail.com
