---
title: 'Protocol-Governed Computing: The Design and Construction Compilers'
weight: 75
slug: design-and-construction-compilers
---

**(c) 2026 Bhash Ganti**

Contact: [mailto:bachipeachy@gmail.com](mailto:bachipeachy@gmail.com)

ORCID Profile: <https://orcid.org/0009-0007-3810-6520>

## Preface

This paper is part of the Protocol-Governed Computing (PGC) technical paper series. [*An Architecture for Closed-Loop Governed Transformation*](https://doi.org/10.5281/zenodo.21879516) established that software evolution is transformation rather than authoring, that meaning has a single producer, and that a compiler-like activity performs the derivation from a business problem to protocol artifacts. That paper names two compilers in a single sentence and does not develop them. This paper develops them.

A governed change begins as a business problem and ends as protocol artifacts in a sealed composition. Two compilers stand between those points. The first judges a design and produces verdicts, findings, a quality rating, and --- where a document is uniquely determined by its prior --- a projection of it. The second renders artifacts from an approved mandate. A third authority, outside both, admits what the second produces; that authority is the subject of [*Compiler Conceptual Model*](https://doi.org/10.5281/zenodo.20471804) and is not re-argued here.

This paper is about why the first two are separate, and about a class of failure that becomes visible only once they are. No prior knowledge of Protocol-Governed Computing is assumed. The argument concerns staged governance generally --- any process in which a proposal is judged at several checkpoints before it is built. The reference implementation is where the argument was found and where its evidence comes from, but the finding is not an artifact of that implementation.

> **A note on terminology.** *Transformation* is the name of the lifecycle --- the passage from business problem to sealed composition --- and of the repository that houses the tooling for it. It is not a third compiler. The compilers are two: **Design** and **Construction**. The **Protocol Compiler** is the external admission authority. Nothing in this paper introduces a fourth.

## Abstract

Protocol-Governed Computing derives protocol artifacts from a business problem through a governed sequence of phases. This paper defines the conceptual model of the two compilers that perform that derivation: the **Design Compiler**, which judges whether a design is admissible, and the **Construction Compiler**, which renders artifacts from an approved mandate.

The central claim is that these are two compilers rather than one because they answer questions that differ in kind. A design failure is a mandate that is incomplete or contradictory; a phase rule set catches it and an author repairs a register. A construction failure is a mandate that was valid and did not uniquely determine an artifact; only the thing that renders can expose it, and the repair amends the design language itself. Collapsing the two would blur failure classes whose legitimate repair surfaces differ.

The paper states and defends a general result: **success at one semantic boundary does not imply success at the next.** A governed lifecycle has three such boundaries --- a design judged admissible, a mandate that determines its artifacts, and a composition admitted to the platform --- and passing the first establishes nothing about whether the design determines its artifacts. The result is developed on the boundary where it is sharpest, using a measured case in which a design admissible across nine phases and 793 rules would still have rendered six artifacts without a fact each of them requires.

Four subsidiary results follow: determinacy must be measured before rendering rather than discovered after it; a rule that has never been shown to fail is evidence of nothing; a governed design language invalidates its own corpus as it grows; and a declared refusal has more than one site at which it can be discharged, not all of which a design language can express.

## 1. Introduction --- three boundaries, two compilers

A governed change passes three checkpoints, and each asks a different question.

The first asks whether a **design is admissible**: does the proposal, as written, satisfy the rules that govern proposals of its kind? The second asks whether that design **determines its artifacts**: given an admissible design, is there exactly one thing to build, or has the design left a choice to whoever builds it? The third asks whether the resulting composition can be **admitted** to the platform: do the artifacts, taken together with everything already in the system, form a valid whole?

The first two questions are owned by the two compilers this paper describes. The third belongs to the Protocol Compiler and is prior work.

It is tempting to treat these as three stages of one process, and most software lifecycles do. A specification is reviewed, then implemented, then integrated, and the reviewing is understood as a weaker, earlier form of the same activity as the integrating. This paper argues the opposite: they are different activities that happen to occur in sequence, and treating them as one is what allows a design to be approved by everyone and still be unbuildable.

The distinction has a practical consequence that motivates the whole paper. If the questions are the same in kind, then a design that passes the first checkpoint is *probably* fine at the second, and the second is a formality. If the questions differ in kind, then passing the first establishes nothing about whether the design determines its artifacts, and a lifecycle that omits the second check will ship the failure. The evidence in Section 7 supports the second reading.

## 2. The gap a design language cannot see

A governed design language is a rule set over registers. A register is a table with declared columns; a rule judges the rows. Rules ask whether a required column is populated, whether a cited identity resolves, whether a value belongs to a controlled vocabulary, whether a row present upstream survived into the current phase.

Every one of those rules judges **what is present**. That is not a limitation of any particular rule set; it is what a rule over a table can do. A rule can require that a row exist, that a cell be non-empty, that a reference resolve. What no such rule can ask is the question that matters at the second boundary: *what would a renderer need in order to produce this artifact?*

It cannot ask because the language contains no renderer. The design language describes a design. The knowledge of what an artifact requires --- which fields a workflow document must carry, which of them have defaults, which are mandatory and would render as empty --- lives in the thing that produces artifacts, not in the thing that describes them.

This is a structural gap, not an oversight. One could attempt to close it by encoding artifact requirements into the design language, so that a phase rule could check them. That attempt fails for a reason worth stating: the requirements would then exist in two places, the language and the renderer, and the two would drift. The moment they drift, the design language is checking a stale model of what artifacts need, and it is reporting success against it.

The alternative is to leave the question where the answer is, and to ask it there. That is the second boundary, and asking it requires something that renders.

## 3. The Design Compiler

The Design Compiler judges documents. It consumes a phase document and the upstream documents that phase declares, applies a sealed rule set, and returns a judgement.

**Phases are a sequence, not a document set.** The distinction is load-bearing. A document set is judged as a body: every document is available to every rule, and consistency is checked globally. A sequence is judged one handoff at a time: each phase reads only the phases it declares as priors, and a rule may only compare what those priors contain.

The mechanism that makes this real is the **declared prior**. Each phase names, in its own rule module, the upstream phases it is entitled to read. A phase run without a prior it declares does not quietly pass; it reports that the handoff was unchecked. This distinction matters more than it first appears. A silent pass and a verified pass produce the same output --- an admissible verdict --- and only the declaration distinguishes them. Without it, a missing input looks exactly like a satisfied one.

Declared priors also bound what a phase may know. A phase cannot reach for a document it has not declared, and so cannot acquire meaning from a source no one authorized. The bound is inspectable: the declaration is in the phase's own rule set, sealed into the composition, and readable by anyone.

**What a phase produces is a judgement, not a document.** The output is a verdict, the number of rules evaluated, and the findings --- each naming the rule that fired, where, and why. A quality rating accompanies the verdict and is deliberately independent of it: a design can be admissible and rate poorly for carrying declared open questions, and can be inadmissible and rate well when a single misspelled citation is fatal to admissibility but cheap in quality. Conflating the two would let quality argue with admissibility, and admissibility is not a matter of degree.

There is one place the Design Compiler writes rather than judges. Where a document is **uniquely determined** by its prior --- where every row of it follows mechanically from what came before --- it may be projected rather than authored. Projection is narrow by design. It is available exactly when there is no decision to make, which is the only condition under which generating a governed document does not amount to inventing meaning.

**The rule set is read from the composition, not from a working tree.** A design is validated against a named baseline, and that baseline carries the rules that were in force when it was pinned. Judging a document by the rules on someone's disk judges it by rules written after it was approved. This is the difference between a governed pipeline and a linter.

## 4. The Construction Compiler

The Construction Compiler renders artifacts from an approved mandate. It reads the design's terminal registers, resolves the generators the design declares, and writes the artifacts the mandate schedules.

**Rendering is whole, not incremental.** An artifact is produced from the design in its entirety, never edited in place. This is the property from which everything else in this section follows.

Consider an amendment: a change that modifies an artifact already in the composition. Under whole rendering, the artifact is re-produced from the current design. Every fact the artifact holds must therefore be present somewhere in that design, including facts the change does not touch. A design that is silent about an existing property does not preserve it --- it drops it, because the renderer has nothing to preserve it from.

This is counterintuitive and it is the correct behaviour. The alternative, patching an artifact in place, preserves unstated facts by accident. It also makes the artifact's content a function of its history rather than of its design, which means no one can read the design and know what the artifact says.

Whole rendering has a cost, and the cost is precisely what makes the second boundary necessary. Because every required fact must come from the design, the design's completeness with respect to the artifact becomes a property that can be **measured before anything is written**. That measurement is the subject of Section 8.

## 5. Why two compilers and not one

The argument for separation is not about components. It is about the questions.

A **design failure** is a mandate that is incomplete or contradictory. A required register is empty; a citation resolves to nothing; a row declared upstream did not survive. A phase rule set catches it, the finding names the register and the row, and an author repairs the design. The repair is local and the author has everything needed to make it.

A **construction failure** is a mandate that was valid and did not uniquely determine an artifact. Nothing about the design is contradictory. Every rule passes. The design simply does not say something that the artifact requires. Only the thing that renders can expose this, because only it knows what the artifact requires. The repair is not local: it amends the **design language**, adding a register or a column so that the missing fact has somewhere to be stated. A different person makes that change, under a different kind of authority.

An **admission failure** is a composition the platform will not accept --- a reference that does not resolve across domains, an invariant the whole violates. It belongs to a third authority for the same reason: only something holding the entire composition can ask it.

Merging any two of these obscures which boundary failed. Worse, it obscures **which layer is authorized to repair it**. A construction failure reported as a design failure invites an author to patch a register, which will make the symptom go away for one artifact and leave the language still unable to state the fact. The next design will hit it again.

This is the substance of the claim that the compilers differ in kind rather than in degree. They do not check the same thing with different thoroughness. They check different things, and each failure has its own legitimate repair surface --- the design, the design language, or the composition. Which surface is authorized is a property of the boundary that failed, not of who happens to be assigned the work; the same person may own two layers without the boundary between them dissolving.

## 6. Gates --- the only human acts

Between the phases there are gates, and a gate is a person.

The gates are few and their placement is deliberate. One confirms that the seed --- the template-conformant restatement of a business problem --- says what the business meant. One approves the design as a body, after every phase has judged it and before any mandate is drafted. One freezes the mandate's scope before authoring begins.

What a gate approves is a design **against a named composition**. It is not an approval of the artifacts that follow, and it cannot be, because the artifacts do not exist yet and the design may not determine them. This is easy to state and easy to forget, and forgetting it is how a lifecycle comes to treat design approval as a warrant of buildability.

A gate is placed where changing one's mind is still cheap. Approving a design costs an author a re-authored register; approving artifacts costs a rebuild, a re-pin, and an amendment to delivered evidence. The asymmetry is the reason gates sit before construction rather than after it.

One property of gates deserves emphasis because it constrains what a gate can legitimately freeze. A gate freezes **scope** --- the set of artifacts a change may touch and the means by which it touches them. It does not and cannot freeze consequences that the design does not state. A change that amends a shared declaration may move artifacts no register names; the gate did not approve that, because the gate could not see it. Section 15 returns to this as an open problem.

## 7. The central result

**Success at one semantic boundary does not imply success at the next.**

The principle applies across the three boundaries; the paper demonstrates it empirically at the first-to-second transition, where it takes the sharp form: *phase admissibility does not imply construction determinacy.*

The measured case is a change to a library catalog. Six existing acts were to be amended so that each announced the business moments it completed. The design inventoried the six acts and the six moments. It was judged at nine phases against 793 rules across 53 check kinds, and it was **admissible at every one of them**. No phase reported a finding. The design was gated and approved as a body.

It would have rendered all six acts without their required actor.

Every one of those acts carries an actor --- the authorization context under which the act runs. The design did not mention it. Under whole rendering, an amendment re-produces an act from the design, so a design silent about the actor produces six acts with no actor, dropping the authorization binding from every catalog operation. The preceding change had named the actor in its inventory as an unchanged, carried-forward row. This one had not.

Construction measured the design at **98.2% complete** and named the missing fact **six times**, once per act.

Three observations follow, and they are the load of the paper.

**First, nothing in the phase rule sets was wrong.** They asked whether the design was complete and consistent as a design, and it was. There is no rule one could add to a rule set over registers that would have caught this, because the fact that was missing is not a fact about the design --- it is a fact about what the artifact requires, and the design language does not contain the artifact's requirements.

**Second, the failure was silent in every signal available before construction.** Admissible at nine phases; no findings; a gate approved by a person reading a complete and coherent document. A lifecycle that treated design approval as sufficient would have shipped it.

**Third, the number 98.2% is doing real work.** It is not a warning or a quality score. It is a measurement of determinacy: the fraction of the facts the artifacts require that the design determines. Below 100%, some fact would have to be chosen by the renderer, and a renderer choosing is a renderer inventing.

The result generalizes beyond this instance. Any staged governance process in which the stages judge the proposal, and a later stage produces the thing, will exhibit it --- because the stages judge what the proposal says and the producer needs what the product requires, and those are different inventories.

## 8. Determination and realization

Determinacy is measured, not inferred.

Before an artifact is written, the Construction Compiler resolves every fact that artifact requires against the design that schedules it. Facts the design determines are counted; facts it does not are named, with the artifact and the field. The result is a fraction.

The threshold is 100%, and the reason is worth stating plainly. Any lower threshold means that some fact is chosen by the generator. The artifact that results is then partly authored by a program, and it enters a registry where nothing distinguishes it from an artifact a person wrote deliberately. The evidence trail is intact and it is describing something untrue: the design does not say what the artifact says.

This is the distinction between **determination** and **realization**. Determination asks whether the design fixes the artifact's content. Realization is the act of writing it. Separating them puts a measurable, refusable check between an approved design and a written file, and it makes the failure mode observable at the moment it can still be repaired cheaply.

A useful consequence: because determinacy is measured against a design rather than against a previous artifact, it does not degrade as artifacts accumulate. A design that determines its artifacts today will determine them after ten amendments, or it will fail at the point where it stops doing so.

## 9. A rule that has never failed has been shown nothing

This section concerns evidence rather than architecture, and it constrains what any claim in the preceding sections is worth.

When a rule is added to a governed language, it is added to judge a condition that documents may exhibit. If no document in the corpus exhibits that condition, the rule reports clean on every document --- and its clean report is indistinguishable from the clean report of a rule that is working.

The reference implementation supplied a stark case. Five rules were authored to govern a newly added register. No document in the corpus had ever populated that register, because it had not existed. All five rules reported clean on their first run, across every document, while checking nothing whatever. The rule set's count rose; its coverage did not.

The remedy is a **probe**: a document constructed to violate exactly one rule, retained in the corpus, and asserted to produce exactly that finding. A rule with a passing probe has been shown to fire. A rule with only clean reports has been shown nothing.

The asymmetry generalizes. **A passing check is evidence about its subject, never about the check.** It becomes evidence about the check only when the check has been observed to fail on a case constructed to make it fail. This applies to the determinacy measurement of Section 8 as much as to any phase rule: a completeness figure of 100% means something only if a design known to be incomplete produces a figure below it.

The practice has a cost, and it is the right cost. Every rule requires a companion document built to break it, and that document must be maintained as the language evolves. A language whose rules are cheap to add and whose probes are optional will accumulate rules that assert coverage they do not have.

## 10. A design language invalidates its own corpus as it grows

A governed design language is versioned by its rule set, and its rule set grows. Each addition --- a register, a column, a rule --- makes documents that were admissible under the previous version inadmissible under the current one.

This is not a defect. A register added because designs were silent about something important *should* make silent designs inadmissible; that is the point of adding it. But the consequence must be stated, because it shapes what a corpus of past designs can be used for.

Two populations diverge. **Delivered evidence** --- the dossiers that governed changes already made --- is never edited. A delivered design is the record of what was approved, and amending it to satisfy a rule written afterwards would falsify the record. So delivered designs go inadmissible as the language grows, and they stay that way. That red is correct.

**Maintained fixtures** --- copies retained to exercise the current rule set --- are carried forward deliberately. They are updated as the language changes, because their purpose is to demonstrate the language as it now stands.

A reader of either population must be told which they are holding. A delivered dossier reading INADMISSIBLE is a historical document judged by a later standard; a fixture reading INADMISSIBLE is a defect. The same verdict means opposite things, and only provenance distinguishes them.

There is a design consequence for anyone building such a language: the cost of adding a register is not the rule that reads it. It is the corpus that must be reclassified, and the discipline of never repairing history to make a metric green.

## 11. What a declared refusal costs

A business states operations it refuses to perform and the conditions under which it refuses them. *We will not register a book whose title, author and year match a book we already hold.* Such statements are declarative, they are business facts, and they are among the most consequential things a business says --- a refusal that is not performed is a promise the system silently breaks.

For a governed design to account for a refusal, it must say what carries the refusal out. There are three sites, and they are not interchangeable.

The first is a **step of an act**: the operation is attempted, a step detects the condition, and its outcome routes to an ending that refuses. This is the ordinary case, and it is checkable in full. The design already states its acts, their steps, the outcomes each step reports, and the type of each ending. A rule can therefore verify that the named step exists, that it reports the named outcome, and that the outcome routes to an ending that refuses rather than to one that completes.

The second is **absence**: the business refuses an operation the system simply does not offer. There is no act, no step, and no outcome, because there is nothing to attempt. This site is real and a design language that knows only the first site cannot express it. Expressing it requires naming the operation that must not exist and asserting that nothing resolves to it --- a negative declaration, whose satisfaction is proven by an empty search, with all the vacuity risk that implies.

The third is the **governance surface**: the refusal is carried out by a rule of the pipeline, which makes the offending declaration inadmissible before anything runs. Here a design can cite the rule that refuses. But note the asymmetry: it is checkable that the cited rule exists and is in force in the composition the design is pinned to. It is **not** checkable that the rule actually refuses the stated condition. That judgement remains with the human at the gate, and a design language that pretends otherwise is asserting coverage it cannot verify.

The third site carries a further constraint. A design cannot discharge a refusal by citing a rule that its own change is adding, because that rule is not in the composition the design is pinned to. The citation would resolve to nothing at the moment it is judged.

## 12. Relationship to the Protocol Compiler

Design and construction stop before admission.

The Construction Compiler produces candidate artifacts. The Protocol Compiler judges the composition those candidates would form together with everything already present, and admits or refuses it. This separation is the subject of prior work and is not re-argued here.

One point of contact deserves statement. No phase and no construction step may infer admission from the fact that its own output is locally valid. A design that is admissible has satisfied the rules governing designs; artifacts that render completely have satisfied determinacy; neither establishes that the composition is admissible. The Protocol Compiler remains the single correctness authority for the whole, and its judgement is not a formality that earlier success anticipates. This is the same claim as Section 7, applied at the third boundary.

The compiler conceptual model predates this separation and speaks of a single compiler, which was accurate when it was written --- there was no design compiler and no construction compiler to distinguish it from. Its revision does not disturb the admission principle. It requires only that the pre-admission boundaries be named, so that a reader does not take "the compiler" to mean everything between a problem statement and a snapshot.

## 13. Evidence

The claims in this paper come from a reference implementation that is open and inspectable. This section states what was measured and what the measurements do not establish.

**By boundary:**

1. *Design.* Phases enforce their declared priors: a phase run without a declared prior reports the handoff as unchecked rather than returning a verdict. Rule sets are read from the composition a design is pinned to, and a differential harness judges every corpus document by both the sealed rule set and the working declaration, asserting that the two agree.

2. *Construction.* Determinacy is measured before rendering and refuses below threshold. An acceptance harness re-renders every delivered artifact from its design of record and compares field by field against what is on disk.

3. *Admission.* Independent conformance over the assembled composition, unchanged by this work.

**Negative results are part of the evidence, and are the more informative part:**

- Five rules reported clean while checking nothing, because no document exhibited the condition they judged. This was found by constructing probes, not by review.
- A design remained admissible across nine phases and 793 rules while failing to determine six required facts. This was found by measurement at the second boundary, not by inspection at the first.
- A classification of certain declarations as inert --- reached by reading one field and generalizing to the artifact containing it --- was contradicted by a test when acting on it broke three cases. An artifact is not a unit of liveness; a field is.

**What the evidence does not establish.** The measurements come from one implementation of one design language over a small number of domains. The general result --- that success at one boundary does not imply success at the next --- is argued from the structure of the questions rather than from the sample, and the sample illustrates it rather than proving it. A different design language might close the specific gap of Section 7 by encoding artifact requirements; Section 2 argues why that trade is unattractive, but it is a trade rather than an impossibility.

## 14. Architectural properties

The properties any conforming implementation must exhibit, stated so they can be checked rather than admired.

- Each phase declares the priors it reads, and a missing declared prior is reported rather than passed.
- Rule sets are judged from the governed composition, not from an ambient working tree.
- A design is validated against a named baseline, and the baseline names the rules in force.
- Determinacy is measured before artifact realization is accepted, and the threshold admits no partial determination.
- Every fact a rendered artifact requires has an identifiable source in the design that schedules it.
- Every enforcement rule is paired with a demonstration that it can fail.
- Quality rating is independent of admissibility in both directions.
- Admission remains independent of design and construction, and neither may infer it.

## 15. Consequences, and what remains open

**What the separation buys.** Failures are attributable to a boundary, and each boundary has an authorized repairer. A design failure is repaired by an author; a determinacy failure is repaired by whoever owns the design language; an admission failure is repaired by whoever owns the composition. Without the separation, all three arrive as "the build is broken" and the repair defaults to whoever is nearest.

**What it costs.** Two compilers, two rule surfaces, and a measurement between them. A change must satisfy both, and the second can refuse a design the first approved --- which is the point, and which is also work. The corpus discipline of Section 10 is a standing cost that grows with the language.

**Open questions.**

*Refusal by absence.* Section 11's second site has no form in the language studied. Giving it one requires a negative declaration whose satisfaction is an empty result, and a negative that nothing can falsify is not an enforcement.

*Completeness of an amendment set.* A design declares the artifacts it amends. Nothing checks that the declaration is complete. A change that amends a shared declaration may move artifacts no register names, and the gate that froze scope could not have seen them. The failure is the same class as Section 7 --- a design that is admissible and does not determine its consequences --- at a different granularity.

*Declared-prior utilization.* A phase's semantic boundary is defined by the priors it declares, and undeclared priors are forbidden. Whether a future implementation should additionally report which declared priors actually influenced a verdict remains open. Such a diagnostic would improve observability, but it is not required by the compiler model presented here --- and defining *influenced* precisely is harder than it appears, since the unit of use is a field or a row rather than a document.

## 16. Conclusion

Two compilers stand between a business problem and a set of protocol artifacts. The first judges whether a design is admissible. The second measures whether that design determines what to build, and renders it if it does. A third authority admits the result.

They are separate because the questions differ in kind, not in thoroughness. A design language reasons over what a design says; a renderer requires what an artifact needs; and those are different inventories, held by different things, and repaired at different layers. Any process that assumes the first question subsumes the second will eventually approve a design that everybody agrees with and nobody can build.

The general form of the result is worth carrying beyond this architecture: **success at one semantic boundary does not imply success at the next.** Governance arranged as a sequence of checkpoints is only as strong as its willingness to ask each checkpoint's own question --- and to accept that an earlier success, however thorough, was an answer to something else.

---

## Appendix A: Key Terms

**Design Compiler.** The component that judges whether a phase document is admissible against the rule set sealed in a named composition. Produces verdicts, findings, and a quality rating; writes only where a document is uniquely determined by its prior.

**Construction Compiler.** The component that measures whether an approved design determines its artifacts and renders them if it does.

**Protocol Compiler.** The external authority that admits a candidate composition. Prior work.

**Phase.** One checkpoint of the design sequence, with its own rule set and its own declared priors.

**Declared prior.** An upstream phase document that a phase is entitled to read. A phase run without one reports the handoff as unchecked rather than returning a verdict.

**Register.** A table with declared columns within a phase document. The unit a rule judges.

**Gate.** A human approval between phases. Approves a design against a named composition; does not approve artifacts.

**Mandate.** The terminal design output that schedules artifacts for construction.

**Determinacy.** The property that an admissible design fixes every fact its artifacts require. Measured as a fraction before rendering.

**Whole rendering.** Producing an artifact from its design in its entirety rather than editing it in place.

**Probe.** A document constructed to violate exactly one rule, retained to demonstrate that the rule can fail.

**Baseline.** The named composition a design is validated against, carrying the rules in force when it was pinned.

## Appendix B: Reference Implementation Notes

The implementation places the Design Compiler and the Construction Compiler in one repository named for the lifecycle rather than for either compiler, with separate rule surfaces and separate registries. The design sequence has nine phases; the terminal two produce the design of record and the mandate.

Determinacy is measured by resolving each scheduled artifact's required fields against the registers that schedule it, reported as a percentage with the undetermined fields named by artifact and field. The threshold is 100%; below it, nothing is written.

The case in Section 7 is a catalog change in a business domain. The figures quoted --- nine phases, 793 rules, 53 check kinds, 98.2% completeness, six named occurrences of one missing fact --- are from that change as recorded at the time it was gated. Rule counts move as the language grows and should be read as a measurement of that moment, not as a property of the architecture.

Probes are retained as corpus documents and asserted by an end-to-end harness that pins, per document, the rules that must fire. A differential harness judges every corpus document by both the sealed and the declared rule set and requires agreement.

## Appendix C: References

**Companion papers**

Ganti, B. (2026). *Protocol-Governed Computing: An Architecture for Closed-Loop Governed Transformation.* DOI: [https://doi.org/10.5281/zenodo.21879516](https://doi.org/10.5281/zenodo.21879516)

Ganti, B. (2026). *Protocol-Governed Computing: An Architecture for Deterministic Declarative Execution.* Companion paper.

Ganti, B. (2026). *Protocol-Governed Computing: Realizing the Normative Platform and Its Governed Transformation.* Companion paper.

**Prior work**

Ganti, B. (2026). *Protocol-Governed Systems: Conceptual Model.* DOI: [https://doi.org/10.5281/zenodo.20300611](https://doi.org/10.5281/zenodo.20300611)

Ganti, B. (2026). *Protocol-Governed Systems: Compiler Conceptual Model.* DOI: [https://doi.org/10.5281/zenodo.20471804](https://doi.org/10.5281/zenodo.20471804)

Ganti, B. (2026). *Protocol-Governed Systems: Runtime Conceptual Model.* DOI: [https://doi.org/10.5281/zenodo.20478471](https://doi.org/10.5281/zenodo.20478471)

Ganti, B. (2026). *Protocol-Governed Systems: Architecture Inversion Concepts.* DOI: [https://doi.org/10.5281/zenodo.20497732](https://doi.org/10.5281/zenodo.20497732)

Ganti, B. (2026). *Protocol-Governed Systems: A Constitutionally Constrained Architecture.* Prior work.