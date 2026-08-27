---
title: 'PGC #5 — The Rule That Was There but Did Nothing'
date: '2026-08-25'
weight: 5
slug: the-rule-that-was-there-but-did-nothing
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---
Imagine opening a compliance report and seeing a rule listed as passed.

Now imagine asking a simpler question: when did this rule ever stop anything?

That question is uncomfortable because software has several ways to look governed without being
governed. A policy can be written down. Code can exist that appears to implement it. A check can
run on every build. Yet no violation may be capable of producing a refusal.

The rule is present. The system is green. Nothing is actually being enforced.

## Four states that look like one

The [Realization Map](https://github.com/protocol-governed-computing/standards/blob/main/doc/realization_map.md)
made me take four words seriously:

- **Declared**: someone stated the requirement.
- **Implemented**: a mechanism exists that is supposed to carry it.
- **Enforced**: the mechanism can refuse a violating case.
- **Demonstrated**: evidence shows the refusal, or otherwise establishes the required property.

These are not stages of confidence. They are different conditions.

A declared rule may have no implementation. An implemented check may always return success. An
enforced rule may never have been tested against a violating fixture. A demonstration may exercise
the wrong subject and prove nothing about the rule that matters.

Collapsing the four creates a dangerous sentence: "the policy is covered."

Covered by what?

## A familiar example

Suppose a build system says every artifact must identify its source. The requirement is written in
the standard. A validator has a function named `check_provenance`. The build invokes it, and every
build passes.

That sounds reassuring until we ask what happens when provenance is absent.

If the validator reports an empty value as acceptable, it is implemented but not enforcing the
obligation. If the test fixtures all contain valid provenance, the test suite has not demonstrated
the refusal. If the validator checks a derived file while the governed subject is the source
artifact, the result may be rigorous and irrelevant.

The green build is not false exactly. It is answering a smaller question than the report implies.

## Enforcement is a chain

Protocol-Governed Computing (PGC) describes enforcement as a chain rather than a single check:

```text
obligation -> assertion -> rule -> determination
```

An obligation says what must hold. An assertion is its evaluable form. The rule is supplied by the
applicable governance closure and evaluated over a governed state and proposal. The determination
produces admit, constrain, or refuse.

Every link matters.

An obligation never rendered as an assertion is an intention. An assertion that no closure can
supply is unreachable. An assertion that cannot refuse is vacuous. In each case the system can
appear organized while the requirement has no force.

This is why PGC treats an obligation with no capable enforcement as a finding, not as a weaker
level of compliance.

## The test that changes the question

The right test is not "does the check run?" It is:

> Can this rule encounter an admissible input for which its consequence is refusal?

That is a capability question, not a historical one. A rule that has never refused may still be
sound if its domain has never contained a violation. A rule that has refused once may still fail to
cover the obligation in another applicable closure.

The Realization Map is useful precisely because it forces those distinctions into the open. It
does not merely point from a requirement to a function. It asks what the function can establish,
where it applies, and whether the apparent realization is stronger, weaker, or simply different
from the normative requirement.

## Why "implemented" is not "enforced"

Engineers naturally prefer positive evidence. A file exists. A branch is covered. A command exits
zero. These are easy to count.

Refusal is harder because it requires a case the system must reject. It also requires checking that
nothing partly proceeded, that the grounds were recorded, and that the cause was distinguished.
Otherwise a crash, a missing result, and a governed refusal can look identical from the outside.

That difference matters operationally. A rule refusal says the proposal was understood and found
unacceptable. A closure failure says the system could not establish which governance applied. The
remedies are not the same.

## Demonstration is its own obligation

Even an enforceable rule is not automatically demonstrated. PGC's Conformance Test Specification
requires each demonstration to name the obligation, the subject, the discharge class, what must be
shown, and what counts as failure.

Some properties are observational: exercise a case and observe the refusal. Some are structural:
show that no path exists by which a forbidden effect can occur. Some are comparative: substitute
another runtime or environment and compare governed consequences. Some are derivational: recompute
the determination from supplied evidence.

The method must match the claim. Observation cannot prove that a path does not exist. Ten tests of
one obligation do not cover ten obligations. A test that cannot fail is not reassuring; it is
vacuous.

## Why negative properties are the trap

Many important software promises are negative:

- an unknown artifact cannot enter execution;
- a non-effecting capability cannot produce an external effect;
- inspection cannot trigger execution;
- a refusal cannot be overridden;
- an environment cannot change a governed consequence.

A system can run successfully forever while violating any of these. The forbidden path simply
waits for the right condition.

That is why PGC says negative properties require structural or comparative discharge. A successful
run proves only that the path was not taken in that run. It does not prove the path is absent.

## The practical payoff

This may sound severe, but it improves ordinary engineering questions. When a rule fails, the team
can ask which condition failed:

Was the obligation declared?

Was it rendered into an assertion?

Could the applicable closure supply it?

Could the assertion refuse?

Was the refusal actually demonstrated with a violating fixture?

The answers identify different kinds of work. They prevent a missing check from being hidden inside
a test count, and prevent a test result from being mistaken for proof of a system-wide property.

## A rule that does something

The point is not to maximize the number of rules. More governance is not automatically better
governance. A badly chosen rule can be faithfully enforced and still express the wrong intent.

The point is to make every claimed rule honest about its status.

Declared is valuable, but it is not enforced. Implemented is progress, but it is not demonstrated.
Demonstrated is evidence about a stated subject, not a license to generalize beyond it.

That discipline is one reason the PGC Standard separates governance from conformance. The system
must enforce what applies; an evaluator must establish whether it did so.

The next article follows the most surprising consequence of this model: sometimes the successful
result is not admission, but refusal.

---

**The standard is open, and I am looking for people to attack it — not endorse it.**

What it claims, what would prove it wrong, and what has *not* yet been established are all set out
in the [call for review](https://github.com/protocol-governed-computing/standards/blob/main/doc/call_for_review.md). Here is a question worth asking on Monday:
**name one rule in your system that has actually refused something.** If that is hard to answer,
you have found the thing this article is about.

Objections, counter-examples, and serious technical criticism: **bachipeachy@gmail.com**
