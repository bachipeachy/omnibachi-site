---
title: 'PGC #4 — When Code Becomes the Constitution'
date: '2026-08-25'
weight: 4
slug: when-code-becomes-the-constitution
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---

# When Code Becomes the Constitution

Every organization has a moment when the written policy says one thing, the people say another,
and the software quietly decides the matter.

The software usually wins.

Not because anyone voted for it, but because the code is what runs. A rule in a handbook can be
outdated. A diagram can be aspirational. A review comment can disappear. The branch condition in
production will still determine what happens at 2:00 a.m.

That is how code becomes a constitution without ever being declared one.

## The authority inversion

There is nothing wrong with implementation. A system needs code, data structures, interfaces, and
execution mechanisms. The problem begins when we infer the governing meaning from those mechanisms
and then treat the inference as authoritative.

A service has a module, so we call the module a governance boundary. A loader searches a directory,
so we assume whatever it finds is admitted. A check returns true, so we say the policy is enforced.
A pipeline has five stages, so we write a standard that requires five stages.

Each inference may be convenient. None is automatically valid.

The Protocol-Governed Computing (PGC) Standard draws a hard line: a realization may show how a property was obtained, but it does
not decide what the property means. The standard specifies semantics. The implementation realizes
them.

That direction of authority is the whole argument.

## Why I built first

This is why the PGC work began with a reference implementation rather than a blank document. I
needed to discover which distinctions survived contact with a working system.

The implementation was a laboratory, not a constitution. It forced questions that a conceptual
architecture can postpone:

- What exactly is being governed?
- Where does authority come from?
- When does a declaration become part of the system?
- What must be determined before execution?
- What does a refusal leave behind?
- What evidence would convince someone who was not there?

Then I worked backwards, not to copy the code into prose, but to separate semantic necessities
from artifacts of one design. A repository boundary might be useful without being a governance
boundary. A compiler stage might discharge an obligation without being a normative phase. A
particular serialization might carry identity without defining identity.

The code exposed candidate concepts. It did not get the final word.

## The hidden constitution problem

Consider a legacy authorization system. No single document says, "Managers may approve up to
$50,000, except during a regional holiday, unless the request came through the internal portal."
Instead, fragments of that rule live in a database flag, a middleware check, a default value, and
an emergency bypass added years ago.

The system may be perfectly stable. It may even be correct according to the behavior everyone has
learned to expect.

But where is the constitution?

If the answer is "read the code and see," then the code is not merely implementing authority. It is
the only place authority exists. Replacing a framework, moving a service, or asking an AI assistant
to refactor a function becomes a constitutional change that may be invisible in the change review.

PGC tries to make that change visible by putting governing meaning into explicit declarations.
Those declarations can determine what may be admitted, what may be constructed, and what may be
executed. The implementation must preserve the meaning, rather than silently inventing it.

## What survives abstraction

The first part of the standard separates concepts, semantics, and invariants.

The Conceptual Model defines distinctions such as declaration versus documentation, authority
versus ownership, admission versus presence, construction versus execution, and evidence versus
attestation.

The Semantic Model gives a governed change a general form. The Architectural Invariants state what
any realization must preserve regardless of how it is built.

Notice what is absent from all of it: no required package layout, process count, language, or
pipeline diagram. Those may be excellent techniques. They are not the semantics — and a standard
that confuses the two has written down one team's habits and called them a specification.

## A standard can be too specific

Over-specification often looks like rigor. A document that names every component and every step can
feel reassuring because it leaves little room for interpretation.

But it leaves no room for independent realization either.

If conformance means reproducing a reference architecture, then a second implementation can pass
by looking familiar while losing the property the architecture was meant to preserve. Conversely,
a different implementation can preserve the property and be rejected for using a different route.

That is not an open standard. It is a construction recipe.

The PGC test is therefore not, "Does this implementation resemble the reference?" It is, "Does it
preserve the observable semantic guarantee?" A different technique is not a deviation when it
preserves the invariant.

## What the Realization Map is for

The [Realization Map](https://github.com/protocol-governed-computing/standards/blob/main/doc/realization_map.md)
records where one realization demonstrates the requirements. It is deliberately non-normative.

Its value is diagnostic. A requirement may be declared but not implemented, implemented but unable
to refuse, enforced but never demonstrated, or demonstrated only by a test that cannot actually
fail. A map makes those differences harder to hide behind green output.

It can also expose defects in the standard. If two requirements cannot both be realized literally,
the implementation has found pressure in the model. The answer is not automatically to bend the
code until it matches the prose. The standard must be examined, and if necessary revised.

That is the reverse-engineering loop at its best: code reveals a question; semantics answer it;
the normative document governs the next implementation.

## The constitutional test

The reference implementation can show that the model is satisfiable. It cannot prove that the
model is independent of itself.

That test belongs to someone who did not write the code:

> Can an independent implementer read the standard, make the necessary semantic decisions, and
> build a conforming system without reverse-engineering the original?

If not, the code remains the hidden constitution. If so, the implementation has finally taken its
proper role: not the source of authority, but evidence that the authority can be realized.

The [PGC Standards repository](https://github.com/protocol-governed-computing/standards) is open
for that challenge. The goal is not to defend one codebase. It is to find out whether the meaning
can stand after the code that first revealed it is gone.

The next question is even less comfortable: what happens when a rule is written down, a check
exists, and the system still cannot actually enforce it?

---

**The standard is open, and I am looking for people to attack it — not endorse it.**

What it claims, what would prove it wrong, and what has *not* yet been established are all set out
in the [call for review](https://github.com/protocol-governed-computing/standards/blob/main/doc/call_for_review.md). If you have watched implementation quietly
become the real policy — and then watched someone try to replace it — that story is worth more to
me than agreement.

Objections, counter-examples, and serious technical criticism: **bachipeachy@gmail.com**
