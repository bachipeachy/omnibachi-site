---
title: 'Protocol-Governed Computing: Architectural Inversion, Its Consequences, and a Scaling Claim'
date: '2026-09-14'
weight: 40
slug: architectural-inversion
aliases:
  - /papers/architectural-inversion/
publisher: 'Wiley Software: Practice and Experience'
status: 'Under review'
---
**Author:** Bhash Ganti (aka Bachi)

**(c) 2026 Bhash Ganti. All rights reserved. Released under the Apache-2.0 License.**

bachipeachy@gmail.com · ORCID [0009-0007-3810-6520](https://orcid.org/0009-0007-3810-6520)

**Preprint:** [https://doi.org/10.5281/zenodo.22736531](https://doi.org/10.5281/zenodo.22736531) — this page is the frozen rendition of that deposit.

**Submitted to:** Wiley Software: Practice and Experience — under review.

---

## Abstract

Conventional software architecture spreads behavioral authority across several sources. Declarations
govern some behavior. Implementation, build tooling and runtime decide the rest. Protocol-Governed
Computing reverses that arrangement. Governed declarations determine authorized behavior, business
process rules included. Construction, implementation and execution realize that determination and add
nothing to it.

This paper derives the reversal rather than proposing it. Five properties serve as premises, each
established in prior work: declarations determine authorized behavior before execution; sealed state
carries authority; construction admits or refuses but never repairs; change derives a named successor
from a named predecessor; and obligations stay inspectable, refusable and evidenced whoever performs
the activity. Conventional architecture assumes the contrary in each case, and the contradictions
force reversal.

Two results follow that the paper never assumes. Execution preserves authority rather than creating
it. Workers stay independent of authority, so a human, an AI system or a hybrid may perform governed
activity without acquiring it. The same derivation runs through governance, orchestration, engineering
and scale, and the paper catalogues what it buys: an enumerable governed behavioral
surface, implementation-free business rules, and machine-speed generation without wider authority.

The scale domain yields the Governance Dividend, a structural scaling claim stated with an
evaluation design rather than measured results. Declared dependencies, not incidental ones, bound an
artifact's governed change surface. Adding an artifact need not enlarge the change surface of
artifacts that do not depend on it. The claim is conditional and names what falsifies it: unstable
governance accumulates coordination debt through the same mechanism.

**Keywords:** software architecture; architectural style; behavioral authority; declarative
execution; governed construction; software evolution; protocol-governed computing

## 1. Introduction

Software behavior rarely comes from one place. Requirements, policies, workflow descriptions and
configuration state part of it. Implementation code determines another part directly. Build tooling,
deployment conventions, runtime defaults and recovery paths supply the rest. Each source is
legitimate in conventional practice. Together they leave a system in which no single artifact
determines everything the system may do.

Protocol-Governed Computing (PGC) reverses that arrangement. Governed declarations determine
authorized behavior. Construction, implementation and execution become mechanisms that realize the
determination. They stop being sources of it. The lifecycle paper argues this baseline at length [3];
this paper states it compactly and moves on.

The reversal is not offered here as a design preference. This paper derives it. Five properties of
PGC serve as premises. Prior work establishes each one. Conventional architecture assumes the
contrary in each case. Hold both and a contradiction appears, and only the reversal resolves it.

The contribution is the joint implication. Taken singly, each property is already published. Taken
together, they contradict foundational assumptions of conventional architecture across four domains,
and the contradictions resolve in one direction. That is the argument, and it closes.

An earlier deposit introduced the inversion as a set of architectural observations [4], building on a
conceptual model of the same family [6]. This paper supersedes that treatment. It does not extend it.
The observations are re-derived here from stated premises, several collapse into one derivation, and
the reader needs no prior paper in the series to follow the argument.

Two results deserve early notice because the paper derives them rather than assuming them. First,
execution preserves authority. A runtime that answers an omitted question would originate behavior
that no declaration authorized. Second, workers stay independent of authority. Changing who performs
a governed activity does not change what the resulting system may do. Both follow from the premises
in Section 5.

Section 2 gives the minimum architecture the derivation needs. Section 3 stipulates the five
properties and cites their grounding. Section 4 states the conventional baseline. Section 5 defines
the derivation rule and works the two results. Sections 6 through 9 derive consequences across the
four domains. Section 10 states the Governance Dividend as a scaling claim and gives the design that
would settle it. Section 11 states what the inversion makes possible. Section 12 separates
derivation from evidence. Section 13 positions PGC against neighboring work. Section 14 concludes.

## 2. Protocol-Governed Computing in brief

### 2.1 What "governance" names here

Software engineering usually reads "governance" as oversight of engineering work. Review boards,
approval gates, access control, audit trails and release sign-off all fit that reading. This paper
does not mean that.

In PGC, governed declarations carry the behavior itself. They state the business process rules, the
workflows, the domain constraints and the capability contracts [3, 6]. They determine what the system
does, not merely what people may do to the system. Compliance governance is a small subset of this, not the
whole of it.

The distinction matters for reading everything that follows. When this paper says governance
determines authorized behavior, it means the business rules live in governed declarations. It does
not mean a policy layer wraps an otherwise conventional application.

One further clarification prevents a common misreading. Implementation still computes. Capability
implementations run algorithms, transform data, call services and hold control logic. What
implementation cannot do is independently determine authorized behavior. The claim concerns the
location of authority, not the absence of computation in code. Without this distinction, a reader may
reasonably conclude that PGC merely relocates business logic into a declaration format.

### 2.2 The functional sequence

PGC composes four functions.

1. **Governed declarations** determine authorized behavior. They hold protocols, rules, profiles,
   constraints, workflows and domain declarations. They fix what may happen before execution begins.
2. **Transformation** derives the next declarations [2]. It starts from a named predecessor and a stated
   purpose, then proceeds through staged derivation. It never starts from a blank space. The current
   baseline supplies evidence, reusable structure and the boundary against which the transformation
   checks its claims.
3. **Governed construction** [3] compiles declarations into verified projections, assembles them under a
   manifest and seals the result as an immutable snapshot. It admits or refuses. It never repairs. A
   generator may materialize a declared design; it may not turn an omission into a decision.
4. **Execution** realizes the sealed snapshot [1]. The runtime verifies integrity, then traverses the
   structure the snapshot contains. The snapshot binds capabilities; the runtime does not discover
   them. Declared data carries routing; runtime logic does not compute it. Where the snapshot is
   silent, execution refuses.

One constraint spans the fourth function. The runtime emits traces as evidence, and those traces
never become a hidden input to later behavior. An evidence channel that fed back into execution would
reintroduce an ungoverned source of decisions.

Figure 1 shows the functional architecture. Each property appears where it arises rather than in a
separate list. The two shaded results are derived in Section 5, not assumed.

**Figure 1. Functional architecture of Protocol-Governed Computing.**

![Functional architecture of Protocol-Governed Computing](/figures/wiley/fig1_wiley_functional_architecture_pgc.svg)

Repository names, command names, languages and deployment substrates may all vary. The functional
boundaries are what this paper argues about.

## 3. Architectural properties

Five properties carry the derivation. This paper does not establish them. It stipulates them as the
architecture's design commitments and cites where prior work establishes each one.

None of the five is novel in isolation. Determinism before execution, content-identified immutable
build products, and authority bounded by what an actor is given are long-established ideas, developed
in reproducible builds [11], capability security [13, 14] and declarative deployment [9, 10]. What the
PGC series contributes is the particular formulation used here, and what this paper contributes is the
consequence of adopting all five together.

### P1. Declarative determination

Governed declarations determine authorized behavior before execution. A compiled protocol is complete
with respect to the behavior it permits. It never requires a runtime to infer a branch, fill a
default, discover a handler or construct a missing graph. *An Architecture for Deterministic
Declarative Execution* establishes this property [1].

Two terms stay distinct throughout this paper. *Authorized* names where behavioral authority resides.
*Admissible* names what construction decides about a candidate declaration. The paper never
interchanges them.

P1 does not forbid response to changing input or state. Different initial states may select different
declared paths. What P1 forbids is a runtime inventing an undeclared path.

### P2. Authorization carried by state

Construction establishes authority, and the sealed result carries it. The snapshot is not a cache or
a build by-product. It is the content-identified, immutable state that execution is authorized to
realize. The runtime never reconstructs that authority from its environment. Reference [1] grounds
P2, and [3] makes it operational.

In this paper, *behavioral authority* means authority to select or introduce a system behavior. It is
not identity, access-control privilege, confidentiality, integrity or resistance to compromise. A
worker may hold operational credentials while holding no behavioral authority, and an admitted
capability may still contain security defects.

An authored baseline differs from a sealed snapshot. Transformation produces the baseline.
Compilation seals it into the object that execution addresses. The snapshot is the boundary between
governed construction and execution.

### P3. Governed construction

Construction determines admissibility and refuses. It never repairs, completes or supplies authority.
A design must determine the artifacts it schedules. A missing field, an unresolved question, an
unrecognized rule mechanism or an underdetermined artifact each triggers refusal. Reference [3]
grounds this property.

A build that succeeds by supplying omitted semantics has created a second producer of meaning beneath
the governing process. That is the failure P3 excludes.

### P4. Successor evolution

Change derives a named successor from a named predecessor. It does not mutate an uncontrolled
baseline. The current baseline participates in its own transformation in three ways: it supplies
reusable structure, it bounds admissibility, and it anchors claims about what already exists.
References [2] and [3] ground this property.

Transformation is relative to a pinned predecessor. It may produce a candidate, and promotion may
make that candidate the successor. Until promotion, the running system is unchanged. Amending an
existing artifact requires whole redeclaration, because an implicit merge with current state would
make the output depend on material the design never determined.

### P5. Checkable governance

Governing obligations stay inspectable, refusable and evidenced, independently of whoever performs
the activity. Rules are declared as data with named evaluation mechanisms. An unknown mechanism fails
rather than being skipped. A refusal names the governing rule and its location. Execution emits
evidence of path and effect. The composition answers questions about its own governed structure.
Reference [3] grounds this property.

P5 asks more than reviewability. A system must apply the obligation. Exposing a document that a
person could inspect does not satisfy it.

### Minimality

None of the five derives from the others. P1 does not imply that authority persists in state. P2 does
not imply refusal over repair. P3 does not imply named successor evolution. P4 does not imply
independently checkable obligations. P5 does not imply that declarations fix behavior before
execution.

Two properties that readers often expect are deliberately absent. Execution authority-preservation
and worker independence are results. Section 5 derives them.

## 4. The conventional baseline

An inversion needs something to invert. The baseline below is not a caricature. It states assumptions
that mainstream architecture and engineering practice commonly hold, at the level the derivation
needs.

**A1. Behavioral authority is legitimately distributed.** Explicit governance artifacts carry some of
it. Implementation carries the rest. Neither is required to be the sole authoritative source. This
assumption governs the other four.

**A2. Runtime may resolve what construction left open.** A runtime may select a handler, plan a
route, infer a missing relation, retry an operation, apply a default or enter a degraded mode. These
behaviors are often useful. Their authority is created at execution time.

**A3. Build and deployment mechanisms may supply defaults.** Configuration, code generation,
dependency resolution, reconciliation and deployment controllers routinely complete an artifact from
information spread across design, environment and current state. The governing declaration alone need
not determine final behavior.

**A4. Change is modification of an existing artifact.** A developer edits a file, applies a patch,
merges a branch or reconciles desired state against current state. The existing artifact is a
starting point. It is not necessarily a named participant whose identity, evidence and admissibility
boundary belong to the transformation.

**A5. Governance is supervisory and external.** Reviews, approvals, policies and audits examine
engineering activity or its outputs. They may block a release. The executable system itself need not
carry or enforce the governing obligation.

**A6. Coordination cost grows with system size.** Components acquire dependencies. Changes cross
boundaries. The number of parties who must understand or approve a change grows with the number of
artifacts and relationships. Modularity slows this growth. It does not establish that adding a
component leaves existing change surfaces untouched.

These are not universal laws. They are the conventional poles against which the PGC properties stand,
and they set the direction of each reversal.

## 5. The inversion imperative

The derivation rule is short.

> A PGC property, together with a conventional assumption that contradicts it, forces that assumption
> to reverse.

The results that follow are conditional propositions over the PGC model. They state what follows if
P1 through P5 hold. They do not establish that an implementation satisfies those properties, nor that
the properties are preferable to a conventional arrangement. Whether an implementation satisfies them
is a separate question, addressed only for the reference realization in Section 12.2.

"Forces" is structural. Retain the conventional assumption and the property is either violated or
rendered inert. The reversal is not a preference chosen from a menu. It is the arrangement that
preserves the premise.

### 5.1 Execution preserves authority

Take **P1 (declarative determination)** with **P2 (authorization carried by state)**. P1 fixes
authorized behavior before execution. P2 puts that authority in sealed state.

Now suppose execution meets an omitted behavioral decision, and the runtime answers it. That answer
was never determined before execution, which violates P1 (declarative determination). The snapshot
does not carry it, which violates P2 (authorization carried by state). Within this architecture, the
answer holds no authority at all.

Execution must therefore preserve authority. The runtime realizes a decision the snapshot carries. Or
it refuses where the snapshot is silent. It cannot infer, default, plan, discover or repair its way
past the omission. Reference [1] develops this closure for the execution partition in detail.

This result says more than "keep the runtime thin." A thin runtime may still hold an implicit fallback
or a dynamic dispatch rule that adds behavior. The result concerns authority, not size. A large
runtime preserves authority as long as sealed state selects everything it does. A small runtime
violates the result the moment it creates one undeclared branch.

The result also sharpens what determinism means here. Give the runtime the same sealed protocol, the
same inputs and the same initial state, and it produces the same declared behavior and the same
trace. A different state may select a different path, but the protocol still selects it. Determinism
is not the claim that every invocation ends the same way. It is the claim that the runtime adds no
choice of its own, under the declared execution model: a fixed evaluation order, controlled clocks and
randomness, and a declared failure model.

The closure claim ranges over behavior represented in the declared capability and orchestration model.
It does not claim that the architecture determines physical timing, availability, third-party
behavior or every implementation-level failure mode.

### 5.2 Workers stay independent of authority

Take **P2 (authorization carried by state)** with **P5 (checkable governance)**. P2 locates
authority in governed state. P5 makes obligations and evidence checkable without reference to the
actor. Now consider two workers performing the same governed activity — a human engineer, an
automated model, or the two working together.

Suppose changing the worker changed what the system was authorized to do. Then authority would reside
partly in the worker, and P2 (authorization carried by state) fails. Suppose instead that changing the
worker changed whether an obligation applied. Then the obligation was not independently checkable, and
P5 (checkable governance) fails.

Worker independence follows. A worker may exercise judgment where the architecture assigns judgment.
A worker may produce a proposal and carry out a governed stage. A worker does not thereby authorize
an artifact, widen its scope or alter the authority of sealed state. Workers are substitutable with
respect to authorization, because the governing machinery admits, seals and evidences the output
rather than trusting it on the strength of its author.

This is not a claim that all workers are equally capable or equally reliable. It is a claim that the
guarantees do not rest on the worker's identity.

The point matters for AI-assisted engineering. An AI system can be a worker without becoming an
architectural authority. Its proposals face the same staged derivation, admission, validation and
promotion that a person's proposals face. The independence is mechanical, not rhetorical. A companion
study examines agent-mediated transformation under this architecture in detail [5]; this paper cites
it for positioning and never uses it as a premise.

### 5.3 The derivation table

Table 1 states the derived inversions. Each row corresponds to exactly one subsection of Sections 6
through 9, and the section number appears in the first column. The scale rows stop at the structural
consequence; Section 10 takes up the prediction that follows from them.

**Table 1. Inversions derived from the five properties.**

| Section | Conventional assumption | Property | Derivation and inversion | Consequence |
| --- | --- | --- | --- | --- |
| §6.1 Governance | A1: authority is distributed across declarations and implementation. | P1 declarative determination; P2 authorization carried by state | If declarations determine authorized behavior and sealed state carries it, implementation cannot hold a second share of authority. | Behavioral determination moves wholly into governed declarations; implementation realizes. |
| §6.2 Governance | Authority belongs to actors, roles or review events. | P2 authorization carried by state; P5 checkable governance | If sealed state holds authority and obligations are checkable without the actor, acting cannot transfer authority. | Authorization becomes a property of governed state and evidence. |
| §6.3 Governance | A5: governance supervises from outside and admissibility is judged after construction. | P3 governed construction; P5 checkable governance | If construction admits or refuses under declared obligations, admissibility settles before executable state exists. | Governance becomes executable and refusal-producing rather than supervisory. |
| §6.4 Governance | Identity attaches to actors and resources. | P2 authorization carried by state; P4 successor evolution | If predecessor and successor carry authority, identity must attach to governed states and their relation. | A transformation audits as a relation between named states. |
| §7.1 Orchestration | A2: the runtime decides what happens next. | P1 declarative determination; P2 authorization carried by state | A runtime decision adds behavior that sealed state does not carry. | Orchestration becomes traversal of a declared graph; a missing route refuses. |
| §7.2 Orchestration | Discovery and fallback improve resilience. | P1 declarative determination; P3 governed construction | Discovery or fallback supplies an omitted decision and repairs the artifact at execution time. | Resilience is declared as capability and outcome, not invented by the interpreter. |
| §7.3 Orchestration | Workers coordinate by holding local authority. | P2 authorization carried by state; P5 checkable governance | Substituting a worker cannot alter governed authority or obligations. | Workers become governed participants, replaceable without changing authorization. |
| §8.1 Engineering | A3: construction completes an artifact and succeeds when it produces a build. | P3 governed construction | A build that fills omissions has made an unapproved design decision. | Construction measures determination and refuses below completeness. |
| §8.2 Engineering | A green build reports that the tooling produced an output. | P3 governed construction | Under refusal, the same signal reports that the declarations determined the output. | A build result becomes a claim about the design rather than about the tooling. |
| §8.3 Engineering | Implementation is a source of behavior. | P1 declarative determination; P2 authorization carried by state; P3 governed construction | If declarations fix behavior and construction binds authority, implementation realizes a contract. | Code becomes replaceable realization beneath governed contracts. |
| §8.4 Engineering | Testing is a separate oracle maintained against the system. | P3 governed construction; P5 checkable governance | A separately authored oracle drifts from the declarations it judges. | Conformance evidence derives from governed declarations and execution. |
| §8.5 Engineering | Deployment is the moment correctness is decided. | P3 governed construction; P4 successor evolution | Promotion installs an admitted and validated candidate; it does not re-judge it. | Construction, validation and installation become distinct events and authorities. |
| §9.1 Scale | Behavior is dispersed across implementation and must be read where it hides. | P1 declarative determination; P2 authorization carried by state | If declarations determine behavior and sealed state carries it, the governed structure holds what code once held. | Understanding the system becomes reading declarations and their relations. |
| §9.2 Scale | A6: each new artifact enlarges the change surface of existing artifacts. | P2 authorization carried by state; P4 successor evolution; P5 checkable governance | Independently bounded artifacts carry their own authority and declared dependencies. | Coordination follows the declared neighborhood of a change rather than total artifact count. |
| §9.3 Scale | A4: change is mutation of an existing artifact. | P4 successor evolution | Named predecessor and successor make mutation an insufficient description. | Evolution becomes successor recursion, with promotion as the state change. |

Three pairs collapse into single derivations. Sections 7.1 and 7.2 are both manifestations of
execution authority-preservation. Sections 6.2 and 7.3 both collapse under worker independence.
Section 8.2 is a corollary of Section 8.1 rather than an independent result. Each stays visible
because practitioners meet these as separate assumptions, and none is presented here as a separate
theoretical result.

## 6. Governance inversions

### 6.1 From distributed behavioral authority to governed determination

This inversion carries the paper's thesis, and the rest of the section follows from it.

Conventional practice splits behavioral authority. A workflow description states part of a business
process. Implementation code states another part. A configuration file states a third. Each is
authoritative over its own share, and no artifact is authoritative over the whole.

P1 and P2 remove the split. Governed declarations determine authorized behavior, and sealed state
carries that determination into execution. The business rules move into the declarations. They do not
remain in implementation with a policy layer wrapped around them.

Implementation does not disappear under this inversion, and it does not stop computing. It loses one
thing only: the authority to determine what the system is permitted to do. A capability implementation
may compute a result through any algorithm it likes. It may not decide that a workflow has an extra
branch.

### 6.2 From actor authority to state authority

Conventional systems attach authorization to actors. A user holds a role. A service account holds a
permission. A reviewer approves a release. An operator invokes a privileged command. These describe
how authority enters a system. They leave open where authority lives once the decision is made.

P2 answers that question. Sealed state holds authority. P5 makes the obligation checkable without
consulting the actor. Together they mean an actor cannot transfer authority simply by acting. The
governed state is the authority, and evidence of admission is what a later reader consults.

### 6.3 From supervisory governance to executable governance

Under A5, governance sits outside and looks in. It reviews, approves and audits. It can block a
release. It does not travel inside the artifact.

P3 and P5 place the obligation inside the construction boundary. Construction applies the rule. A
violation produces a refusal that names the rule and its location. Governance stops being a document
that a person consults and becomes a mechanism the system runs.

### 6.4 From actor identity to state lineage

Conventional audit traces who did what. P4 makes the predecessor-successor relation the primary
record. A transformation becomes a relation between two named states. The worker appears in the
evidence, but the lineage does not depend on the worker's identity to be meaningful.

## 7. Orchestration inversions

### 7.1 From decision-making to traversal

A conventional orchestrator decides. It evaluates a gateway expression, selects a branch, resolves a
handler and plans a route. Section 5.1 forbids all of it. The snapshot carries the graph. The runtime
walks it. Where the graph has no edge, the runtime refuses rather than choosing one. Reference [1]
develops this traversal form in detail.

### 7.2 From runtime resilience to declared resilience

Retries, fallbacks, circuit breakers and degraded modes look like operational virtues. Each supplies
behavior that no declaration authorized. P1 and P3 push them into the declarations. Resilience
survives the inversion; it changes authorship. The protocol declares the retry, the fallback path and
the degraded outcome, and the runtime realizes what the protocol declares.

### 7.3 From worker orchestration to worker substitution

Conventional pipelines assign trust to particular workers. A senior engineer may merge; a junior may
not. Under Section 5.2, the governing machinery admits the output rather than trusting the author.
Workers become substitutable with respect to authorization. Capability still differs between workers.
Authority does not.

## 8. Engineering inversions

### 8.1 From construction as completion to construction as admission

A conventional build completes an artifact. It resolves dependencies, generates missing scaffolding
and applies defaults. Success means the build produced an output. Reference [3] develops admission as
a construction obligation.

P3 reverses the measure. Construction asks whether the declarations determine the artifact. If they
do, it admits and produces. If they do not, it refuses and produces nothing usable. A build that
quietly filled a gap has made a design decision that no one approved.

This inversion is easy to state and hard to hold. Every convenience a construction mechanism offers is
a candidate violation.

### 8.2 From build success to determination

The previous inversion changes what a green build means. Under A3, a green build means the machinery
managed to produce an output. Under P3, it means the declarations determined the output. The second
is a claim about the design. The first is a claim about the tooling.

### 8.3 From implementation authority to contract realization

Under A1, implementation decides behavior. Under P1 and P3, implementation realizes a contract that
governed declarations fix.

The inversion does not empty the code. Capability implementations still hold algorithms, data
transformations and control logic. They compute. What they no longer do is determine what the system
is permitted to do. Two implementations that satisfy the same declared contract are
substitutable with respect to the observations that contract specifies. They may still differ in
performance, resource use, failure timing and behavior outside the contract. Adequacy remains a
separate question that this architecture does not settle.

### 8.4 From separate tests to derived evidence

A conventional test suite is a second artifact, authored separately and maintained against the system.
It drifts. P3 and P5 generate conformance evidence from the declared obligations and from
observed execution. The declarations state the obligation. Execution emits the evidence. This removes
one class of oracle drift. It does not establish that the obligations are complete or substantively
correct.

### 8.5 From deployment to promotion

Under A4, deployment is where correctness gets decided. Something is built, tested, then shipped, and
shipping is the moment of truth.

P3 and P4 split that moment into three events with separate authority:

- **Construction** decides admissibility — whether the declarations determine the artifact.
- **Validation** decides whether the candidate behaves as declared.
- **Promotion** installs an already admitted and validated candidate. It re-judges nothing. It changes
  which named state is current.

## 9. Scale inversions

### 9.1 From dispersed behavior to governed structure

When behavior lives in code, understanding a system means reading code across the places behavior
hides. P1 and P2 concentrate behavioral determination in governed structure. Understanding the system
becomes reading the declarations and their relations.

### 9.2 From global coordination to declared-neighborhood coordination

Under A6, adding an artifact adds to everyone's coordination burden. P2, P4 and P5 bound each
artifact by its declared dependencies. Coordination can therefore be bounded by the declared
neighborhood of a change rather than by the total artifact count.

### 9.3 From cumulative change to successor recursion

Each successor derives from its predecessor, compiles into a snapshot and becomes the pinned
predecessor of the next transformation [2]. This differs from a long-lived mutable baseline. It preserves
historical identity, and it makes every transition a governed object.

Some properties persist through the recursion. A closed capability surface persists once the
governing declarations establish it. Other properties must be re-established at every step:
admissibility, evidence for current execution and factual claims about the pinned predecessor.
Recomputing them stops history from becoming an authority that bypasses current governance.

## 10. The Governance Dividend: A Scaling Claim and Its Evaluation

The Governance Dividend is the terminal prediction of the scale inversion. An earlier deposit named
it and described its mechanism [4]. That treatment stated no figure of merit, which left the claim
open to an economic reading it could not support. This section supplies the missing definition before
restating the prediction.

### 10.1 The figure of merit

"Dividend" is an economic word. The quantity it names here is structural. Stating that quantity
precisely is part of the claim, because an undefined dividend invites a reading about cost that this
paper does not support.

Let a composition hold *n* governed artifacts. Let a transformation *T* directly change a set *S* of
them. Two quantities follow.

**Ripple, ρ(T).** The number of artifacts that *T* forces to be re-declared, re-admitted or
re-validated. Under PGC, ρ(T) counts *S* together with the artifacts whose declared dependencies
reach *S*. It counts nothing else.

**Coordination breadth, κ(T).** The number of governed boundaries — domains, ownership units,
separately governed surfaces — that *T* must cross.

The two are distinct. A transformation can touch many artifacts inside one boundary, or few artifacts
across several boundaries. Conventional architecture expects both to climb as *n* grows.

Transformations must be classified before either quantity means anything, because three kinds behave
differently by construction.

- **Local.** The transformation changes artifacts within one declared neighborhood. The dividend
  claim applies to this class and to no other.
- **Cross-cutting.** The transformation changes the governing vocabulary, the constitution or the
  profile in force. Reaching every artifact it governs is intended behavior here. A large ρ is
  correct, not evidence against the dividend.
- **Mechanical.** The transformation performs release bookkeeping — a version bump, a manifest
  refresh, a synchronized packaging edit. It touches the whole composition by construction and
  carries no behavioral coupling.

The claim does not range over the mechanical class. Section 12.2 reports such transformations
separately rather than setting them aside.

Ripple and coordination breadth are the figures of merit. They are not themselves the dividend. The
Governance Dividend is the structural property they expose: how each quantity relates to the size of
the composition.

> For local transformations in a stabilized governed system, ρ and κ are functions of the declared
> dependency neighborhood of *S*. Where those neighborhoods remain bounded as the system grows, ρ and
> κ remain bounded rather than growing with *n*.

The condition matters, and an earlier formulation of this claim omitted it. Nothing in P2, P4 or P5
prevents a declared dependency graph from growing denser as artifacts accumulate. A denser graph
enlarges the transitive neighborhood of a local change, and ρ would then climb with *n* even though
every dependency was declared. Bounded declared neighborhoods are therefore a condition of the
prediction, not a consequence of the properties.

Conventional architecture offers no corresponding containment. Incidental dependencies accumulate as
a system grows, and nothing in the arrangement prevents ρ and κ from growing with *n*. This is a
statement about what the conventional arrangement permits, not an empirical law about how software
systems in general behave.

The dividend is therefore a claim about marginal dependence. Under the stated conditions, the
marginal dependence of ρ and κ on *n* approaches zero. It is not a claim that either quantity is
small. This paper defines no growth model and derives no rate, and it makes no claim that would
require one.

What the figure of merit does not measure deserves equal emphasis. It says nothing about engineering
effort, elapsed time, monetary cost, staffing or defect rate. Those quantities depend on people,
tooling and organization, and they require a study of a kind this paper does not undertake. The merit
claimed here is structural containment of change, and the economic reading of "dividend" remains
unestablished.

### 10.2 The prediction

Its mechanism is artifact sovereignty. An artifact's governed change surface is determined by its
declared dependencies rather than by incidental dependencies embedded in implementation. Adding a new
artifact therefore need not enlarge the governed change surface of artifacts that do not depend on
it. Coordination attaches to the transformation's declared neighborhood rather than to the total
artifact count. This paper does not claim the equivalence as a formal result.

The prediction follows:

> In a protocol-governed system whose governance structure has stabilized, growth in artifact count
> need not carry the growth in coordination cost and change ripple that conventional architecture
> may exhibit.

This is an architectural prediction with stated conditions. It is not a measured economic result. It
does not assert that adding artifacts is free, that compilation time cannot grow, or that every
transformation stays local. It predicts a changed relationship between system size and the change
surface of already-governed artifacts.

### 10.3 Conditions

The conditions are explicit. Declared dependency neighborhoods must remain bounded as the system
grows; Section 10.1 states why this condition cannot be dropped. Artifact identity and ownership
must be explicit. Dependencies must be declared and inspectable. Construction must refuse hidden or
underdetermined coupling. The governing vocabulary and capability surface must stay stable, or
change through governed substrate transformation. Inspection must distinguish an empty answer from
unknown evidence. Transformations must pin to the predecessor they actually judge.

### 10.4 When the prediction fails

The prediction fails when governance is unstable. Redraw boundaries repeatedly, add obligations
without migration, hide dependencies or report inspection inaccurately, and every new artifact raises
questions that existing artifacts cannot answer. The result is coordination debt, not dividend. The
same mechanism produces both outcomes: an unclear or expanding dependency surface enlarges the
neighborhood that must be understood and revalidated.

### 10.5 Falsification

The prediction is falsifiable, and stating how it would be falsified is part of the claim. A suitable
study holds a stabilized governed architecture constant and grows *n* by adding artifacts with
independently bounded dependency surfaces. It then classifies each transformation and evaluates ρ and
κ for the local class, reporting cross-cutting and mechanical transformations separately rather than
setting them aside.

The dividend survives if ρ and κ stay bounded as *n* rises. It fails if either climbs with *n* while
the governing structure holds still and declared neighborhoods stay bounded. Observing growth in ρ
while neighborhoods themselves are growing falsifies nothing; it confirms that the stated condition
was not met. The expected result is not zero ripple. It is a weaker relationship between
artifact count and the change surface of unaffected artifacts than a comparable conventional
arrangement may show.

This paper reports no such measurement.

## 11. What the inversion makes possible

The preceding sections derive what changes. This section catalogues what those changes are worth.
Nothing here introduces new evidence. Every entry follows from a derivation already made and carries
the section that derives it. Entries citing Section 10 inherit its status as a prediction with stated
conditions rather than a derived consequence; Section 12.1 assigns the classes. Section 11.7 states
what the catalogue excludes. Table 2 summarizes the catalogue; the subsections that follow state each
entry with its justification.

**Table 2. Capabilities the inversion makes available.**

| Group | Capability | Derived in | Class |
| --- | --- | --- | --- |
| Scale | Governed change scope tracks the declared neighborhood rather than total system size. | §9.2 | Derived |
| Scale | Growth need not compound. | §10 | Predicted |
| Scale | Comprehension is reading, not archaeology. | §9.1 | Derived |
| Scale | History does not accumulate as sediment. | §9.3 | Derived |
| Security | Undeclared behavior has no execution path. | §5.1, §7.1 | Derived |
| Security | The governed behavioral surface is enumerable from the snapshot. | §7.1, §9.2 | Derived |
| Security | Untrusted input cannot become a governed route. | §7.1 | Derived |
| Security | Acting does not change behavioral authority. | §6.2 | Derived |
| Security | Environment cannot supply authority. | §2.2, §7.2 | Derived |
| Asset | The valuable asset is separated from its implementation. | §2.1, §6.1 | Derived |
| Asset | That asset is implementation-free. | §8.3 | Derived |
| Asset | Replacing an implementation does not put the governed determination at risk. | §8.3 | Derived |
| Asset | The governed asset can outlive a particular execution substrate. | §2.2 | Derived |
| Asset | The runtime need not acquire domain-specific logic as domains are added. | §5.1, §7.1 | Derived |
| Asset | Vendors and tools become substitutable. | §5.2, §7.3 | Derived |
| Reuse | Capabilities compose through declared contracts. | §8.3 | Derived |
| Reuse | Reuse does not import hidden coupling. | §8.1 | Derived |
| Reuse | One governed base can serve many admitted surfaces. | §6.3 | Derived |
| Change | Governed blast radius is computed from declared dependencies rather than estimated. | §9.2, §10 | Predicted |
| Change | Underdetermined designs fail at construction. | §8.1, §8.2 | Derived |
| Change | A green build becomes a claim about the design. | §8.2 | Derived |
| Change | The same snapshot eliminates drift from independently reconstructed deployment state. | §2.2 | Derived |
| Change | A class of conformance evidence becomes a by-product of construction and execution. | §6.3, §8.4 | Derived |
| Change | The system can state what it is permitted to do. | §6.1, §9.1 | Derived |
| Engineering | Generation speed is decoupled from authorization. | §5.2 | Derived |
| Engineering | Agents become admissible participants. | §5.2 | Derived |
| Engineering | Trust attaches to evidence rather than authorship. | §6.2, §8.4 | Derived |

### 11.1 Scale and complexity

**Governed change scope tracks the declared neighborhood rather than total system size.** An
artifact's governed change surface is its declared dependency surface (§9.2). Understanding a change
means understanding its neighborhood rather than the whole composition.

**Growth need not compound.** Adding an artifact need not enlarge the change surface of artifacts
that do not depend on it (§10). Where declared neighborhoods stay bounded, the cost of a local change stays
bounded as the system grows.

**Comprehension is reading, not archaeology.** Behavior lives in governed structure rather than
dispersed through implementation (§9.1). A newcomer reads declarations and their relations instead of
reconstructing intent from code.

**History does not accumulate as sediment.** Each successor derives from a named predecessor and
compiles to a fresh snapshot (§9.3). The system carries a lineage of governed states rather than
layers of unremoved past decisions.

### 11.2 Security

**Undeclared behavior has no execution path.** Execution realizes only what the sealed snapshot
carries (§5.1, §7.1). A capability the snapshot did not bind cannot be reached, because no mechanism
exists to reach it.

**The governed behavioral surface is enumerable from the snapshot.** Only admitted topology executes
(§7.1, §9.2). The question "what behavior can this system reach" has a bounded answer a reader can
compute from the snapshot.

**Untrusted input cannot become a governed route.** Routing is declared data, not computed logic
(§7.1). The runtime has no path that turns text into a route. Such input may still affect data, invoke
an admitted capability, or exploit an implementation defect.

**Acting does not change behavioral authority.** Authority resides in governed state rather than in
the actor (§6.2), applying to behavioral authority an intuition long established for access authority
[13, 14]. Access control and credential compromise remain separate concerns. A compromised worker, agent or credential does not gain authority over what the system
may do.

**Environment cannot supply authority.** The snapshot binds capabilities; the runtime does not
discover them (§2.2, §7.2). A hostile or misconfigured environment cannot introduce a capability that
construction did not admit.

This is a structural bound, not a claim of security. Implementation defects, capability misuse within
an admitted surface, and operational compromise remain. The architecture bounds the governed
behavioral surface exposed by a breach. It does not bound what an admitted capability can reach, and
it does not prevent a breach.

### 11.3 Asset value and portability

**The valuable asset is separated from its implementation.** Business rules, workflows and domain
constraints live in governed declarations (§2.1, §6.1). The organization's accumulated determination
of what its systems do is an artifact it holds, not a property distributed through code.

**That asset is implementation-free.** Declarations determine behavior; code realizes a contract
(§8.3). The asset does not encode a language, framework or runtime, so it does not depreciate when any
of them does.

**Replacing an implementation does not put the governed determination at risk.** Two implementations
that satisfy the same declared contract are substitutable with respect to the observations that
contract specifies (§8.3). A rewrite changes the realization beneath the contract, not the
determination the contract carries.

**The governed asset can outlive a particular execution substrate.** A sealed snapshot is
content-identified and self-describing (§2.2). A conforming runtime that did not exist when it was
sealed can read, inspect and re-execute it. This holds only where such a runtime exists.

**The runtime need not acquire domain-specific logic as domains are added.** All routing and binding
arrive in the sealed snapshot, so the runtime holds no domain logic (§5.1, §7.1). Admitting a new
domain produces a new snapshot, not a new runtime. The runtime may still grow for other reasons — new
capability classes, storage mechanisms, failure models, observability. What stays invariant is its
generic traversal machinery. That invariant substrate is what makes auditing the runtime tractable and
porting it to another substrate a bounded task.

**Vendors and tools become substitutable.** Workers hold no authority (§5.2, §7.3). Changing a
contractor, a team or a model changes who builds, not what the system may do.

### 11.4 Reuse and composition

**Capabilities compose through declared contracts.** Implementation realizes contracts rather than
determining behavior (§8.3). A capability admitted in one domain is reusable in another by
declaration, not by copying.

**Reuse does not import hidden coupling.** Construction refuses underdetermined or undeclared
dependency (§8.1). What a reused capability depends on is declared or it does not compile.

**One governed base can serve many admitted surfaces.** Profiles select what a composition admits
(§6.3). Different deployments narrow the same governed base rather than forking it.

### 11.5 Change, assurance and compliance

**Governed blast radius is computed from declared dependencies rather than estimated from
implementation.** Declared dependencies make a change's governed neighborhood calculable before anyone
makes it (§9.2, §10). Release scoping and risk assessment become computation over governed structure.
Implementation coupling, external services and operational dependencies lie outside the computed
neighborhood.

**Underdetermined designs fail at construction.** Construction refuses and produces nothing usable
(§8.1, §8.2). One class of production defect cannot arise: behavior that shipped because some
mechanism filled a gap on its own.

**A green build becomes a claim about the design.** Under refusal, build success reports that the
declarations determined the output rather than that the tooling managed to produce one (§8.2).

**The same snapshot eliminates drift caused by independently reconstructed deployment state.** One
sealed snapshot executes everywhere, and the runtime discovers nothing (§2.2). That removes one class
of environment divergence by construction rather than by discipline. External services, clocks,
infrastructure and implementation defects still differ between environments.

**A class of conformance evidence becomes a by-product of governed construction and execution.**
Obligations are declared as data, refusals name the rule they enforced, and execution emits its path
(§6.3, §8.4), which places provenance [15] inside the construction boundary rather than alongside
it. It does not follow that the obligations are complete or substantively correct. Compliance
artifacts stop being a separately maintained program that drifts from the system it describes.

**The system can state what it is permitted to do.** Authorized behavior is determined before
execution and carried in one content-identified artifact (§6.1, §9.1). Certification, audit and
regulatory attestation answer their central question by reading rather than by investigation.

### 11.6 Human and AI engineering

This consequence bears most directly on current practice.

AI systems generate implementation at machine speed. Review runs at human speed. Conventional
governance closes that gap two ways: review faster, or generate less. Neither scales, because both
treat review as the place where authority is exercised.

Worker independence removes the gap rather than closing it. Section 5.2 derives it. Authority resides
in governed state, and obligations stay checkable without reference to the actor. A worker that never
held authority cannot enlarge what the system may do, however fast it works.

A companion study evaluates this arrangement under agent-mediated transformation [5]. The
architecture moves a portion of acceptance control from human review into machine-checkable admission.
Generation throughput can then rise without granting the worker additional behavioral authority. It
does not remove the need to review the declarations, the capability implementations or the quality of
the evidence.

Two further entries follow from the same result. **Agents become admissible participants**, because a
governed activity performed by a model faces the same admission, validation and promotion as one
performed by a person (§5.2). And **trust attaches to evidence rather than to authorship**, because
the governing machinery admits and evidences the output instead of trusting it on the strength of who
produced it (§6.2, §8.4).

This is a claim about authority, not quality. Fast generation may still produce poor implementations.
The architecture bounds what those implementations are permitted to do. It does not make them good.

### 11.7 What the inversion does not buy

The value catalogued above is structural. It concerns what a system can state, what it refuses, what a
breach can reach, and what can be computed about a change before making it.

The inversion does not establish that governed development is cheaper, faster or less error-prone than
conventional development. It makes no claim about staffing, delivery time, defect rate or total cost
of ownership. It does not establish that business rules expressed as governed declarations are easier
to author than the same rules expressed in code. It does not claim security, only a bounded and
enumerable surface. Each of those is an empirical question about people, tooling and organizations,
and answering it requires studies this paper does not offer.

The architecture also does not remove judgment. Someone must decide what the system should do. The
inversion governs where that decision is recorded and what may act on it. It does not make the
decision.

## 12. Evidence and limits

### 12.1 Three classes of claim

Every claim in this paper belongs to exactly one class, and the text names the class wherever it makes
the claim.

- **Derived (Sections 5–9, 11).** The claim follows from P1 through P5 together with a stated
  conventional assumption.
- **Exercised (Section 12.2).** The reference realization exhibits the mechanism. The scope of that
  realization bounds the claim.
- **Predicted (Section 10).** The claim follows from the architecture but requires broader empirical
  evaluation. The Governance Dividend is the paper's only predicted claim, and the entries in Section
  11 that cite Section 10 rest on it.

Confusing these classes would make the paper claim more than its evidence supports.

### 12.2 What the reference realization exercises

The composition described here is deposited and citable [18]. A reader can obtain the sealed snapshot,
its manifest and its runbook, and can re-run the build and the workloads. No independent party has
done so, and this paper makes no claim that anyone has reproduced the results.

The reference realization [3] composes governance artifacts, conformance workloads and business
domains under a profile. It compiles them into a sealed snapshot, exposes a governed boundary,
provides an inspection surface and emits execution evidence. Its transformation tooling carries a
business problem through staged derivation, construction, admission, validation and promotion.

Realization exposed defects that architectural review had not. An artifact family could not declare a
reserved field empty. Nested payloads flattened incorrectly. Prose arrived where a value belonged.
Declared events wrote to a field that no consumer read. Rules were declared but not enforced. Copies
of one artifact identity diverged. An inspection query returned a confident but incomplete empty
answer. These findings illustrate why realization is a distinct epistemic activity. Architecture
establishes invariants. Construction and execution establish whether a particular implementation
instantiates them.

One observation runs against the scale inversion and belongs in the record. Release mechanics touch
every repository regardless of declared dependencies. A version bump is a synchronized edit across
the whole composition, and it is not artifact-local. Section 10.1 classifies such transformations as
mechanical and excludes them from the figure of merit, on the grounds that they carry bookkeeping
rather than behavioral coupling. That exclusion is a modelling decision, and a reader may reasonably
contest it. This paper therefore reports the observation rather than omitting it.

A structural pre-filter that guessed relevance disagreed with the worker's later judgment. That is
consistent with the architecture's separation of knowledge from execution: relevance depends on the
purpose of a change and need not be present in the existing graph. It does not prove that relevance
can never be computed from structure.

### 12.3 Limits

A single practitioner directed the reference work, and that practitioner also designed the
architecture. AI workers performed parts of the construction under that direction, which is disclosed
after Section 14; the arrangement exercises worker independence but does not establish it. The
reference domain and profile are limited. No controlled comparison with a conventional development
process exists, so this paper claims nothing about speed, cost, defect rate
or engineering effort. No second, independently built runtime has established portability
experimentally. Worker independence follows from the architecture and appears in limited worker
substitutions, but adversarial worker behavior and broad replication remain open. The Governance
Dividend remains a conditional prediction with no measurement behind it.

### 12.4 Threats to validity

**Construct validity.** The definitions of authorized behavior, governed behavioral surface, ripple
and coordination breadth may not capture operational complexity.

**Internal validity.** The same practitioner designed the premises, the implementation, the workload
and the interpretation. Confirmation bias and selective reporting are possible.

**External validity.** One reference domain, one runtime family, one profile and limited worker
substitutions do not establish generality.

**Comparison validity.** No matched conventional baseline exists, so every relative claim
remains unestablished.

**Adversarial validity.** The paper does not test malicious declarations, compromised capabilities,
hostile environments or incorrect governance.

**Temporal validity.** The scale results assume a stable governing vocabulary. Evolving schemas and
frequent cross-cutting transformation may dominate in practice.

## 13. Related work

PGC shares concerns with several traditions. It reverses a different assumption in each.

**Model-driven engineering** moves models closer to execution and generates substantial parts of an
implementation [7, 8]. PGC shares the preference for explicit models and generated artifacts. The
difference lies in what maintains agreement. A model-driven system often relies on human diligence to
keep model, requirement and generated implementation aligned. PGC makes the governed transformation
and its provenance the enduring relation, and construction refuses artifacts that the relation does
not determine.

**Policy-as-code** makes policy executable and testable, moving governance toward computation. PGC
extends the move in two ways. Admissibility becomes part of the construction boundary, and sealed
state carries authorization. A policy engine that evaluates at runtime still holds runtime decision
authority. Under P1 and P2, the protocol must already carry authorized behavior, and the runtime may
only realize it.

**Declarative deployment and infrastructure-as-code** separate desired state from imperative
mechanism [9, 10]. They share the declarative impulse. Reconciliation, however, plans a path to the
desired state at runtime. PGC treats that planning as behavioral authority unless the plan is itself
governed and sealed beforehand. The question is not whether a desired state is declared. It is whether
the engine may choose the path.

**Reproducible builds** seek identical outputs from identical source and pinned inputs [11]. PGC
depends on that discipline for snapshot identity. Reproducibility alone does not establish that source
fully determines authorized behavior. A build can reproducibly include a default, a hidden dependency
or an ungoverned construction rule. PGC adds refusal for underdetermination and makes the sealed
artifact the authority that execution addresses.

**Virtual machines and bytecode** offer a close analogy. A bytecode artifact outlives its virtual
machine, and a query outlives its database engine. Those engines nonetheless retain dynamic
dispatch, planning, type resolution and evaluation strategy. PGC makes a stronger closure
requirement:: the interpreter needs no behavioral inference, so it cannot originate behavior through
those mechanisms.

**Workflow and business-process engines** execute declared graphs [12] and come closest to PGC's
orchestration form. The gap matters. Gateways, expressions, embedded scripts and runtime handlers can
still decide behavior during traversal. PGC requires the sealed protocol to represent all behavior
relevant to admissibility before traversal begins. This is also where the difference in the word
"governance" shows most clearly: a process engine governs process execution, while PGC governs the
determination of behavior itself, business rules included.

**Capability security** limits authority by controlling what an object can access [13, 14]. PGC
applies a related intuition to behavioral authority: a runtime cannot exercise authority over behavior
that sealed state never gave it. **Provenance models** supply languages for recording what produced
what [15]; PGC makes provenance part of the admissibility and transformation boundary. **Formal
specification and model checking** supply rigorous description and verification [16, 17], but they do
not remove the distinction between an authored specification and the implementation it judges. PGC's
claim is narrower: governed declarations, sealed state and transformation provenance form one chain
rather than two artifacts kept in agreement.

## 14. Conclusion

Protocol-Governed Computing reverses the conventional location of behavioral authority. This paper
does not introduce that reversal as a design preference. It derives it from five stipulated
properties: governed declarations determine authorized behavior before execution; sealed state
carries authority; construction admits or refuses without repairing; evolution derives a named
successor from a named predecessor; and governing obligations remain inspectable, refusable and
evidenced independently of the actor.

Taken together, these properties contradict familiar assumptions of conventional software
architecture, and the resulting inversions are systematic. Authority to determine behavior moves into
governed declarations, business rules included. Runtime orchestration becomes traversal of declared
structure. Construction becomes admission rather than completion. Implementation retains computation
but loses independent authority to determine authorized behavior. Promotion installs an
already-governed result rather than becoming a new source of correctness or authorization. Governance
is therefore no longer a supervisory layer around execution. It is part of the executable state that
execution is required to realize.

Two consequences are derived rather than assumed. Execution preserves authority, because supplying
omitted behavior at runtime would create a second source of unauthorized decisions. Worker identity
likewise does not determine authorization, because authority resides in governed state and the
governing obligations are independently checkable. Human, AI and hybrid workers can therefore differ
in capability and judgment without becoming different sources of architectural authority.

The same structure produces the conditional Governance Dividend. When governance has stabilized and
dependency surfaces remain bounded and declared, increasing the number of governed artifacts need not
increase the change surface of artifacts outside the affected neighborhood. This is a structural
prediction, not a claim about cost, speed, staffing or defect rates. The failure case matters as
much: unstable governance enlarges dependency surfaces and produces coordination debt through the
same mechanism.

The broader consequence is a change in what software can make explicit. Authorized behavior can be
inspected as governed state rather than reconstructed from implementation and surrounding process.
Underdetermined behavior can be refused during construction rather than supplied later by a build
mechanism or a runtime. Business rules can remain authoritative independently of the implementation
technology that realizes them. And machine-speed engineering can increase activity without
transferring architectural authority to the worker performing it.

The central result is therefore not that PGC eliminates judgment, implementation, state or change. It
is that each has a bounded architectural role. **Behavior is determined by protocol, authority is
carried by state, construction and evolution are governed transitions, and execution realizes rather
than extends what has been authorized.** A later mechanism cannot quietly acquire an authority that
an earlier governed transition was required to establish.

## Declaration of generative AI use

During the preparation of this work the author used Claude/Opus (Anthropic) in the four supporting
capacities listed below. After using this tool the author reviewed, revised and edited the content as
needed, and takes full responsibility for the content of the publication.

The author is the sole author. The author conceived and wrote the research content — the
architectural argument, the derivation, the figures of merit, the claims made and the limits placed
on them. No generative AI tool is an author, and none could be: a tool cannot hold the accountability
that authorship entails. The tool generated no research data, performed no derivation and conducted
no analysis of its own.

1. **Drafting assistance under the author's direction.** The assistant drafted and restructured prose
   from the author's outline, argument and decisions. The author reviewed, revised and accepted every
   passage. No text entered the manuscript without that review.
2. **Rendering Figure 1.** The author supplied the figure's content: the functional decomposition,
   the partitions, the properties and the placement of each property at its point of origin. The
   assistant produced the drawing and refined its layout. Figure 1 is a conceptual schematic. It
   presents no research data, no experimental results and no data visualization, and no data,
   results or figure presenting data was generated or altered by any AI tool.
3. **Extracting material from the reference implementation.** Observations reported in Section 12
   were read from the repositories, build outputs and execution traces of the reference realization
   and transcribed into the manuscript. The implementation, not the manuscript, is the record.
4. **Proofreading and copy-editing.**

A separate disclosure belongs to the reference realization itself, because it bears on Section 12.
Parts of that realization were constructed by AI workers performing governed activity under the
author's direction, within the architecture this paper describes. The author held scope, admission
and promotion authority throughout; the workers held none. The relevant property for this paper is
worker independence, derived in Section 5.2, and the realization exercises it rather than
establishing it. A companion study examines that arrangement directly [5].

## References

[1] Ganti, B. (2026). *Protocol-Governed Computing: An Architecture for Deterministic Declarative Execution*. Zenodo. DOI: [10.5281/zenodo.21879516](https://doi.org/10.5281/zenodo.21879516).

[2] Ganti, B. (2026). *Protocol-Governed Computing: An Architecture for Closed-Loop Governed Transformation*. Zenodo. DOI: [10.5281/zenodo.21879948](https://doi.org/10.5281/zenodo.21879948).

[3] Ganti, B. (2026). *Protocol-Governed Computing: Realizing the Normative Platform and Its Governed Transformation*. Zenodo. DOI: [10.5281/zenodo.21880155](https://doi.org/10.5281/zenodo.21880155).

[4] Ganti, B. (2026). *Protocol-Governed Systems: Architecture Inversion Concepts*. Zenodo. DOI: [10.5281/zenodo.20497732](https://doi.org/10.5281/zenodo.20497732).

[5] Ganti, B. (2026). *Protocol-Governed Human-AI Software Engineering: Autonomy Without Authority*. Manuscript under review. DOI: [10.5281/zenodo.22650863](https://doi.org/10.5281/zenodo.22650863).

[6] Ganti, B. (2026). *Protocol-Governed Systems: A Conceptual Model*. Zenodo. DOI: [10.5281/zenodo.20300611](https://doi.org/10.5281/zenodo.20300611).

[7] Schmidt, D. C. (2006). Model-driven engineering. *IEEE Computer*, 39(2), 25–31. DOI: [10.1109/MC.2006.58](https://doi.org/10.1109/MC.2006.58).

[8] France, R., & Rumpe, B. (2007). Model-driven development of complex software: A research roadmap. In *Future of Software Engineering*, 37–54. DOI: [10.1109/FOSE.2007.14](https://doi.org/10.1109/FOSE.2007.14).

[9] Burns, B., Grant, B., Oppenheimer, D., Brewer, E., & Wilkes, J. (2016). Borg, Omega, and Kubernetes. *ACM Queue*, 14(1), 70–93. DOI: [10.1145/2890784](https://doi.org/10.1145/2890784).

[10] Morris, K. (2016). *Infrastructure as Code: Managing Servers in the Cloud*. O'Reilly Media. ISBN 978-1-4919-2435-8.

[11] Lamb, C., & Zacchiroli, S. (2022). Reproducible builds: Increasing the integrity of software supply chains. *IEEE Software*, 39(2), 62–70. DOI: [10.1109/MS.2021.3073045](https://doi.org/10.1109/MS.2021.3073045).

[12] van der Aalst, W. M. P. (2013). Business process management: A comprehensive survey. *ISRN Software Engineering*, 2013, Article 507984. DOI: [10.1155/2013/507984](https://doi.org/10.1155/2013/507984).

[13] Dennis, J. B., & Van Horn, E. C. (1966). Programming semantics for multiprogrammed computations. *Communications of the ACM*, 9(3), 143–155. DOI: [10.1145/365230.365252](https://doi.org/10.1145/365230.365252).

[14] Miller, M. S. (2006). *Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control*. PhD thesis, Johns Hopkins University.

[15] Moreau, L., & Missier, P. (Eds.). (2013). *PROV-DM: The PROV Data Model*. W3C Recommendation, 30 April 2013. https://www.w3.org/TR/2013/REC-prov-dm-20130430/

[16] Lamport, L. (2002). *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley. ISBN 978-0-321-14306-8.

[17] Jackson, D. (2006). *Software Abstractions: Logic, Language, and Analysis*. MIT Press. ISBN 978-0-262-10114-1.

[18] Ganti, B. (2026). *Protocol-Governed Computing: v4 composition deposit*. Zenodo. DOI: [10.5281/zenodo.22714911](https://doi.org/10.5281/zenodo.22714911).
