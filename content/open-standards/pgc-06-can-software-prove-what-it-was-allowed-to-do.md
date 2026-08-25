---
title: 'PGC #6 — Can Software Prove What It Was Allowed to Do?'
date: '2026-08-25'
weight: 6
slug: can-software-prove-what-it-was-allowed-to-do
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---

# Can Software Prove What It Was Allowed to Do?

After an incident, the first question is usually, "What happened?"

That is a useful question. It is not the only one.

The harder question is, "What was the system allowed to do, and what establishes that answer?"

A log can tell us that an account was upgraded. It may not tell us which governance applied, which
rules were evaluated, whether the representation had been altered, or whether the upgrade happened
without a determination at all. A record of behavior is not automatically evidence of permission.

PGC treats that distinction as foundational.

## An event is not a determination

Imagine a package arriving at a warehouse. The receiving clerk records that it was accepted. That
record establishes an event. It does not, by itself, establish that the package was authorized,
that the right inspection rules were applied, or that the clerk had the authority to accept it.

Software has the same problem. "The request succeeded" is an observation. A governed transition
requires more: a closure was established, every applicable rule was evaluated, the dominant
consequence was determined, the resulting state matched what that consequence permitted, and the
whole account can be checked afterward.

Evidence is what makes those claims distinguishable.

## Evidence is constitutive

In ordinary systems, evidence is often treated as an audit byproduct. The operation happens first;
someone adds logging so investigators can reconstruct it later.

PGC makes a stronger claim: evidence is part of what makes a transition governed. If a
determination cannot be established by a party that did not observe it, then the transition was
not governed merely because the result looked correct.

This changes the design question. Instead of asking, "What should we log?" we ask, "What would an
independent party need in order to re-establish what was determined?"

For any determination, the evidence must make it possible to establish:

1. which governance closure applied, and by what authority;
2. which rules that closure supplied;
3. what each predicate yielded;
4. what dominant consequence followed; and
5. that the resulting state was what the consequence permitted.

For execution, the evidence must also make the path checkable against the sealed representation.

An outcome without that basis is a report of activity, not proof of governed activity.

## Provenance answers a different question

PGC keeps evidence, provenance, and attestation separate because they answer different questions.

- **Evidence**: what was determined, and what occurred?
- **Provenance**: where did this governed thing come from, and by what derivation?
- **Attestation**: who asserts something about this record or artifact?

These distinctions are easy to lose inside a single "audit trail." A snapshot may have provenance
showing that it was derived from a particular baseline. An attesting party may vouch for its
integrity. Execution evidence may show which path was taken. None of those records substitutes for
the others.

Known provenance does not prove correctness. An attestation does not become proof merely because
the signer is trusted. Evidence that an operation occurred does not establish that it was allowed.
Each record has a job, and authority does not arise from any of them.

## The closure must travel with the evidence

Suppose an evaluator checks yesterday's decision by asking today's system which rules currently
apply. That may seem practical. It is also the wrong question.

The closure may have changed. An authority may have been superseded. A reference may resolve
differently. A current environment may no longer resemble the one in which the decision occurred.
Re-discovering governance after the fact can produce a different answer from the one that governed
the transition.

PGC therefore requires the evidence to carry the closure and rules that were used. A checker
re-evaluates what the evidence supplies; it does not reconstruct authority from a live system.
That is how a past determination remains checkable after the producing system, its environment, or
its maintainers have changed.

## Determinative and observational content

Not every byte of evidence must be identical across two executions. A timestamp, duration, node
identifier, or measured environment may vary without changing what the system determined.

PGC separates:

- **determinative content**: closure, authority, rules, predicate results, consequence, resulting
  state, and execution path;
- **observational content**: when and where something occurred, how long it took, and other
  observations that do not determine the governed consequence.

For the same governed input, state, and closure, determinative content must be identical.
Observational content may differ. The distinction must be declared rather than guessed by a checker.

This prevents two opposite mistakes. Comparing every field makes every timestamp look like a
semantic change. Comparing only the fields that happen to look stable lets a real change hide in
the record.

## What "allowed" means

There is an important asymmetry in the phrase "what was allowed."

A successful result can be what governance would have permitted and still be ungoverned if no
determination established it. Conversely, a refusal can be a governed and successful result even
though no business state changed.

Evidence must therefore establish permission, not infer it from the outcome. The fact that a
transfer completed does not prove that a rule admitted it. The fact that a snapshot executed does
not prove that it was verified. The fact that an implementation has a check does not prove that
the check was supplied by the applicable closure.

The proof is the re-derivable relationship among proposal, closure, rules, determination, and
result.

## Evidence is output, never authority

A system may read evidence for inspection, analysis, or a later human decision. It may not feed the
record of past determinations into the next determination as though history were governance.

If withholding an old trace changes what a new proposal is allowed to do, the trace has become an
undeclared source of authority. Protocol_Governed Computing (PGC) calls for evidence to remain output only.

This does not make history irrelevant. A person may examine evidence and propose a governed
transformation. What is forbidden is allowing the record to silently decide.

## How conformance uses evidence

The Conformance Model distinguishes several ways obligations are discharged.

Observation can establish what happened. Structural analysis can establish that a forbidden path
does not exist. Comparison can show that replacing a runtime or environment does not change a
governed consequence. Derivation can re-compute a determination from supplied evidence and compare
it with the recorded result.

The choice matters. A successful execution cannot prove that no undeclared path exists. A
signature cannot replace a derivation when the claim is about semantic correctness. A test of one
runtime says nothing about substitutability unless another genuinely independent runtime is used.

Evidence is powerful because it supports the right kind of check, not because it makes every claim
true.

## The question an audit should ask

When reviewing a system, I would now ask less often, "Do we have logs?" and more often:

> Could someone who did not observe this transition establish what was allowed, under which
> authority, and why the resulting state was permitted?

If the answer is no, the system may still be useful. But it has not demonstrated governed
behavior. It has recorded an event and asked us to trust the explanation around it.

The [PGC Standards repository](https://github.com/protocol-governed-computing/standards) develops
these distinctions in the Evidence, Attestation & Provenance and Conformance documents. They are
not bookkeeping details. They are the difference between remembering what software did and being
able to establish why it was allowed to do so.

The next challenge is larger still: can another team build the system from the standard alone?
