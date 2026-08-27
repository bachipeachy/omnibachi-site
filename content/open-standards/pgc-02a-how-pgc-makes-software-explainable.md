---
title: 'PGC #2A — How PGC Makes Software Explainable'
date: '2026-08-27'
weight: 2.1
slug: pgc-02a-how-pgc-makes-software-explainable
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---

A trace can show that a branch ran. It cannot show that the branch was allowed to decide.

That gap is why software can work for years and still get harder to explain. The PGC Standard sets
out to close it. This is not a summary of the standard — it is a test of whether its central
picture earns the confidence it invites.

![The PGC Standard from declared meaning to governed behavior](https://raw.githubusercontent.com/protocol-governed-computing/standards/main/spec/0d_visual_representation_of_the_standard.svg)

*The figure is non-normative. It is useful precisely because it makes several claims easy to see
and therefore easy to challenge.*

## Start with the picture, then distrust it

The diagram divides a governed system into two halves.

Before the seal, declarations, governance, and construction meet. The system resolves what applies,
projects the candidate, and verifies it. The seal is the boundary: the snapshot becomes fixed,
complete, and accepted.

After the seal, the runtime is deliberately smaller than the machinery that built the snapshot. It
accepts the sealed content, evaluates declared obligations, traverses declared structure, and
produces a result with evidence. Inspection can read the snapshot without executing it.
Transformation can produce a successor snapshot.

That is an attractive architecture. It also hides the questions that decide whether the architecture
means anything:

- Who gets to say that the snapshot is complete?
- Complete with respect to which profile and which authority?
- What happens when a declaration is missing, ambiguous, or unknown?
- How can an outsider distinguish evidence of a determination from a description written afterward?
- What stops the runtime from smuggling in a decision the snapshot never made?

If the standards cannot answer those questions, the seal is a graphic device, not a governance
boundary.

## Explainability is not a better explanation

There is a common but weak idea of explainability: keep enough logs that an engineer can reconstruct
what happened. That is valuable operationally, but it is retrospective. The explanation depends on
someone knowing which services, defaults, feature flags, and deployment facts matter.

PGC is reaching for something stricter. A governed result should be explainable from the content
that authorized it, the determination that applied that content, and evidence that connects the two.
The explanation is not a story added after the event. It is a property of the path from declaration
to effect.

This creates a useful distinction:

> A system is explainable when an independent reader can establish why the result was permitted,
> not merely when a maintainer can narrate how it happened.

That is a high bar. It is also the part worth reading the standard for, because ordinary
observability tooling does not settle authority. It records what happened, and authority is a
question about what was permitted to happen.

## The seal is where the argument lives

The visual gives the seal the most important job in the entire model. Before it, candidates and
rules may be assembled. After it, execution is constrained by a fixed snapshot.

But “fixed” is not the same as “correct,” and “verified” is not self-explanatory. A snapshot can be
immutable and still encode the wrong authority. It can be complete according to one unstated
assumption and incomplete according to the system's actual obligations. It can be internally
consistent while omitting a rule that should have applied.

This is where a reader should resist the temptation to praise the diagram and instead look for
normative answers:

1. What exact conditions permit sealing?
2. Is a failed or unknown governance closure a refusal, a default, or an implementation error?
3. Is completeness a structural property, a semantic property, or both?
4. Can two different authorities seal materially different snapshots from the same proposal?
5. What identity does the evidence bind: the proposal, the closure, the snapshot, the determination,
   or all of them?

A standard that answers these questions gives the seal consequences. A standard that gestures at
them leaves the most important boundary to local interpretation.

## Why the runtime must be boring

The lower half of the figure makes a deliberately unfashionable claim: the runtime adds no behavior.
It applies what the sealed structure determines.

That constraint is stronger than “the runtime follows the configuration.” Configuration is usually
allowed to be incomplete, overridden, discovered, or interpreted by the code that consumes it. PGC
tries to make those escape routes visible. If the declaration does not authorize an action, the
runtime must not invent permission from proximity, convention, or a convenient fallback.

The relevant failure is not a crashed process. It is a successful process that did something the
snapshot did not authorize.

That is why refusal matters. If the runtime cannot establish the governing closure, treating the
closure as empty would turn ignorance into permission. Refusal preserves the boundary. It also
creates a testable question for an implementation: can we show that the same unknown condition is
refused rather than quietly normalized into a usable default?

This is one of the places where the standards should be read against real systems. Search-based
loaders, plugin registries, dependency injection, feature flags, and AI-generated fallbacks all have
a natural tendency to discover more behavior than a declaration explicitly names. The standard's
claim is not that discovery is always bad. It is that discovery cannot acquire authority merely by
happening.

## Three ways the picture can fail

The figure helps separate three failures that are often reported as one vague problem.

**The meaning may be underspecified.** The documents may use terms such as authority, obligation,
closure, or evidence without fixing the distinctions a second implementer needs. In that case, the
implementation is not the only problem. The standard is asking readers to supply semantics.

**The meaning may be clear but unrealized.** An implementation may seal content that is not complete,
execute an undeclared path, or emit evidence that cannot establish the determination. Here the
standard may be adequate and the realization may be nonconforming.

**The meaning may be clear and realized but not independently checkable.** A property may hold in
the reference system while no evaluator can obtain convincing evidence of it. That is a conformance
problem, not merely a documentation problem.

The distinction matters because each failure demands a different remedy. More prose will not repair
an implementation that violates a clear invariant. More tests will not repair a requirement that
has no stable meaning. And a correct implementation is not proof that an external evaluator could
verify the claim.

## Read the documents in the uncomfortable order

The easiest route through a standards repository is usually the most flattering one: read the
conceptual overview, follow the happy-path example, and inspect the reference implementation. That
route encourages recognition. It makes the system feel coherent before you have asked where it can
fail.

For PGC, I recommend a more hostile route:

- Read the conceptual and semantic documents until you can state what is being governed without
  borrowing names from the implementation.
- Find every requirement about refusal, completeness, authority, and evidence.
- Ask what observable fact would disprove each one.
- Read the execution model looking specifically for behavior that could be added by accident.
- Use the realization map as evidence about one implementation, not as an authority on the
  standard's meaning.
- Record every place where you had to choose an interpretation.

That last step is the important one. A reader who never feels uncertain may simply be carrying in
assumptions the documents do not state. An independent implementation or profile is valuable partly
because it exposes those silent choices.

## The claim is narrower than it sounds

PGC does not claim that software can explain every business outcome in ordinary language. It does
not remove the need for domain experts, good tests, operational telemetry, or judgment about whether
a rule is wise. It does not make an invalid policy valid by sealing it.

The narrower claim is more defensible: the governing meaning of a system can be made explicit,
portable, and subject to independent inspection, instead of being inferred from whichever mechanism
happens to run.

Even that claim is unfinished until someone can demonstrate it without access to the builder's
private context.

The figure is therefore not a conclusion. It is a map of the burden of proof. Each arrow asks what
crosses the boundary. Each box asks what is authoritative. The seal asks whether the result is fixed
for a reason that can be established later. The final line promises that a governed system can
explain what it contains, what it did, and what it refused.

I want readers to attack that promise at its weakest point. Pick one box. Pick one arrow. Show me
where the standards leave a decision implicit, where the implementation adds behavior, or where the
evidence cannot carry the claim.

That is a more useful response than agreement. It tells us whether PGC has made software
explainable, or only made its explanation easier to draw.

## Where to read next

The [PGC Standards repository](https://github.com/protocol-governed-computing/standards) contains
the normative documents, the non-normative visual materials, and the supporting realization
artifacts. Start with the [call for review](https://github.com/protocol-governed-computing/standards/blob/main/doc/call_for_review.md)
for the claims, open questions, and criteria for useful criticism.

Then try to break the seal.

---

**The standard is open, and I am looking for people to attack it — not endorse it.**

If you would have to invent a rule to implement or evaluate PGC, please say exactly where. Objections,
counter-examples, and serious technical criticism: <bachipeachy@gmail.com>
