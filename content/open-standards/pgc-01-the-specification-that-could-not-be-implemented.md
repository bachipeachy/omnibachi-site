---
title: 'PGC #1 — I Wrote a Rule Nobody Could Follow'
date: '2026-08-23'
weight: 1
slug: the-specification-that-could-not-be-implemented
series:
- PGC Open Standard
tags:
- PGC
- open-standard
---

I write specifications for long-lived business software. A few weeks ago I found out that two rules
in my own standard cancel each other out.

**Rule one:** when you replace something, the old version has to disappear completely. Nothing
anywhere may still point at it.

**Rule two:** the replacement has to record what it replaced, by name.

Rule two is a pointer at the old version. Rule one forbids pointers at the old version. Follow both
and nothing can ever be replaced.

That is not a hard rule. It is an impossible one. It sat in the document for months, and nobody
reading it noticed — including me.

---

## The code noticed before any human did

Someone was writing the check that enforces rule one. The check scans an artifact for anything that
still mentions the retired version.

The moment they ran it, it rejected everything, because every replacement carries the name of what it
replaced.

So they added a two-line exception, and wrote a comment explaining that without it nothing could ever
be replaced. Then they moved on and shipped.

Months later I compared the standard against the implementation line by line, found that exception,
and asked what it was working around. The answer was: my document.

**The code was right. The specification was wrong.** I changed the specification.

---

## Why this is worth your attention

We are good at one question: *does the implementation follow the specification?* That is what
conformance tests, audits and certification are for.

We almost never ask the other one: *can the specification be followed at all?*

That second question matters because this kind of defect never announces itself. An implementer hits
it, works around it, and ships. The workaround becomes tribal knowledge — the thing you have to know
that the document does not tell you. The next implementer either rediscovers it or gives up.

From the outside, nothing looks broken. You just end up with a standard that has exactly one working
implementation, and no one can say why.

---

## What PGC is

Protocol-Governed Computing is an attempt to write down what a business system *means* — its rules,
its authority, what it is allowed to do and refuse — separately from the code that implements it.

Not a framework. Not a language. A specification of meaning that any implementation can be checked
against.

The reason to bother: in a long-lived system, the meaning is the valuable part, and it is usually the
part that only exists inside the code. When the code has to be replaced, the meaning goes with it.

---

## I built it backwards on purpose

The working implementation came first. Then I went through it and asked, of every piece: is this a
real idea, or just how I happened to build it?

A class that exists in Python is not automatically a concept. A repository boundary is not
automatically an architectural one. A compiler stage is not automatically a required step.

Only what survived that question became part of the standard. The implementation was evidence for
finding the real ideas — not the authority for defining them.

Then I mapped the finished standard back onto the implementation, requirement by requirement, and
asked where each one actually lives. That comparison is what found the contradiction above. It found
other things too.

---

## The four words that are not synonyms

> **Declared ≠ implemented ≠ enforced ≠ demonstrated.**

- **Declared** — someone wrote the rule down.
- **Implemented** — code exists that is supposed to carry it.
- **Enforced** — that code can actually say no.
- **Demonstrated** — it has been seen saying no.

A system can be in any one of those states and look, from outside, like it is in the last one.

Here is what that looked like in my own build. Of eighty-seven checks that run on every build,
**fourteen had no way to fail**. No input could make them say no. Ten of them said as much in their
own comments — *"stub, real enforcement later."*

All fourteen were declared as governance. All fourteen ran every time and reported that they passed.
In the build log they were indistinguishable from the seventy-three that can actually refuse
something.

The rule *"every obligation has a check"* was satisfied — by checks that carry nothing.

The same shape showed up again elsewhere: one kind of declaration was validated against a rulebook
that required no fields and forbade nothing. Thirty-three declarations passed it, because everything
passes it. On any dashboard counting what was validated, it looked governed.

> **Coverage is not governance, and a count cannot tell the difference.**

---

## Why now

AI has made writing code cheap. It has not made *knowing what the code is allowed to do* any cheaper.

An AI can produce a working implementation in an afternoon. It cannot decide what that implementation
is permitted to mean. That has to be written down somewhere durable, by someone with the authority to
decide it, in a form something can check.

I think that is a specification problem, not a tooling problem, and I think we are about to need the
answer.

---

## What I want from you

The first open draft of the PGC Standard is published. It is a draft, not a launch.

The question I cannot answer myself:

> **Could a team that has never seen my implementation read this standard and build a working system
> — without having to guess at the parts I left out?**

I cannot judge that. I built the implementation, so I fill every gap in the document without
noticing.

So please try to break it:

- Find a rule that contradicts another one. There is at least one more; I have not found it.
- Find a rule that tells you *how* to build something instead of *what must be true*.
- Find an obligation that nothing could actually enforce.
- Find a place where you would have to guess.

Objections are more useful to me than agreement. A standard nobody attacked is a standard nobody
read.

- [PGC Open Standard — GitHub](https://github.com/protocol-governed-computing/standards)
- [PGC technical papers — OmniBachi](https://omnibachi.org/)
- Introduction, in short form:
  [blog #22](https://omnibachi.org/blog/open-protocol-governed-computing-standard/)

---

## What comes next in this series

**#2 — Meaning, Not Mechanism.** Why specifications drift into telling you how to build things, and
how to tell the two apart.

**#3 — Why I Wrote the Implementation First.** Building before specifying is supposed to be
backwards. It was the only way I found out which ideas were real.

**#4 — Checking a Standard Against Reality.** The comparison that found the contradiction, what else
it turned up, and why I retired it afterwards.

**#5 — Declared, Implemented, Enforced, Demonstrated.** Four words that look like synonyms. Most
governance failures are a system sitting in one and presenting as another.

**#6 — What AI Actually Changes.** Not code generation. The collapse in the cost of producing
implementations, and what that does to the value of knowing what they are allowed to do.

**#7 — Womb to Tomb.** Governing a system across decades of regulatory and organizational change —
and why replacement is the requirement everyone designs against and nobody designs for.

Comments, objections and serious technical criticism are welcome — bachipeachy@gmail.com