# PGC papers submitted for publication

Five papers, five publishers, five distinct questions. This note records what each one claims so that
overlap can be checked rather than assumed.

## 1. IEEE *Computer* — Who Authorizes Software Behavior? Governing the AI-Native SDLC

link to privare website allowed by IEEE:

https://omnibachi.org/papers/who-authorizes-software-behavior/

No preprint, and **not eligible for Zenodo.** IEEE's *Article Sharing and Posting Policies* permit a
preprint only on the author's personal or employer website, on TechRxiv, or on arXiv. Zenodo is not
an approved server at any stage. arXiv cs.SE is gated on an endorsement not yet obtained and TechRxiv
has been closed for site renovation, so the available route is **omnibachi.org**, which the policy
permits both before submission and while under review. On acceptance, any posted version must be
replaced by a full citation with DOI or by the accepted version with DOI, carrying an IEEE copyright
notice.

**Question: who authorizes what a system may do, once agents write the code?** The paper argues that
implicit authorization fails under agent-mediated development. A conventional lifecycle gates at
merge, release and deployment, and assumes those disjoint approvals compose — a composition that
lives in reviewers' heads and depends on producers being few, known and sharing tacit context. Agents
break all three conditions. The paper proposes authorization as an explicit, independently checkable
property established during governed construction and carried in sealed state, then reports three
tests: a reference implementation over seven governed domains, an independent realization built from
a frozen specification, and mutation testing that exposed two required guards whose removal left the
demonstrations unaffected. Its subject is the *problem* and the evidence that the problem is real.

## 2. Springer *Automated Software Engineering* — Protocol-Governed Human–AI Software Engineering: Autonomy Without Authority

Preprint: [10.5281/zenodo.22650863](https://doi.org/10.5281/zenodo.22650863) · also Research Square
[10.21203/rs.3.rs-10963678](https://doi.org/10.21203/rs.3.rs-10963678/v1)

**Question: can an agent perform the full engineering work of a lifecycle without becoming the
authority over what the result may do?** An autonomous worker carried a business change through a
nine-phase lifecycle against a frozen baseline, and a risk-directed mutation study tested whether the
required guards actually discriminate. Two of six demonstrations did not; four did. The paper is an
empirical study of one agent-mediated transformation. It evaluates an architecture's treatment of
agency — not model capability, productivity or output quality — and its conclusions are bounded to
the boundaries the study exercised.

## 3. Elsevier *Journal of Systems and Software* — Protocol-Governed Computing: A Software Development Lifecycle Architecture for Deterministic Declarative Execution and Governed Transformation

Preprint: https://doi.org/10.5281/zenodo.22758703

Synthesizes three deposited preprints
([21879516](https://doi.org/10.5281/zenodo.21879516),
[21879948](https://doi.org/10.5281/zenodo.21879948),
[21880155](https://doi.org/10.5281/zenodo.21880155)), each cited as prior disclosure.

**Question: what is the lifecycle architecture, and how is conformance to it specified and checked?**
The paper applies one semantic schema to three activities usually treated separately — changing what
a system is, constructing an executable representation, and executing it — and shows they compose
through a governed predecessor-to-successor transition while keeping their authorities distinct. It
derives a conformance view from the PGC specification family (closure, reachability, inspection,
refusal, evidence, externally authored profiles) and assesses a named reference realization against
the obligations its specification and runbook make checkable. Its subject is the *specification and
conformance* layer.

## 4. Wiley *Software: Practice and Experience* — Protocol-Governed Computing: Architectural Inversion, Its Consequences, and a Scaling Claim

Preprint: [10.5281/zenodo.22736531](https://doi.org/10.5281/zenodo.22736531) · supersedes
[10.5281/zenodo.20497732](https://doi.org/10.5281/zenodo.20497732)

**Question: what changes architecturally when governed declarations, rather than implementation,
determine behavior?** The paper stipulates five properties established in prior work, sets them
against six assumptions conventional architecture commonly holds, and derives the reversals the
conflicts force across governance, orchestration, engineering and scale. Two results are derived
rather than assumed: execution preserves authority rather than creating it, and worker identity does
not determine authorization. It closes with the Governance Dividend as a conditional scaling claim,
with a figure of merit and the study design that would settle it, and reports no measurement. Its
subject is the *conceptual consequence* of the architecture.

## 5. Oxford University Press *The Computer Journal* — Protocol-Governed Computing: Business Software That Runs on a Domain-Neutral Substrate

Preprint: [10.5281/zenodo.22779384](https://doi.org/10.5281/zenodo.22779384) · submitted 2026-09-15,
manuscript ID **COMPJ-2026-09-1249**

**Question: can a shared substrate admit and execute a governed business domain without acquiring
that domain's behavior?** The paper separates two conditions ordinarily conflated — C1, admission
without substrate modification, and C2, no domain-specific behavior in the substrate — under a
criterion that asks where a domain-visible outcome is determined rather than where it is written. It
then reports an architectural case study: four heterogeneous domains compiled into sealed snapshots
and executed by one traversal engine, measured by read-only inspection of the deposited composition.
No admission introduced domain-specific behavior into the substrate; all 22 domain-specific
capability implementations are namespaced to their domains; no domain vocabulary participates in an
execution decision; an injected cross-domain reference is refused during construction. The substrate
did change at each admission, always at a shared contract boundary, so literal C1 is reported as not
demonstrated and the weaker C1′ as demonstrated. Its subject is the *substrate boundary*.

## Why these do not overlap

| Paper | Asks | Method | Answers about |
| --- | --- | --- | --- |
| IEEE *Computer* | Why does agent-mediated development break authorization? | Position plus three tests | The problem |
| Springer *ASE* | Can an agent do the work without gaining the authority? | Empirical study of one transformation | The agent |
| Elsevier *JSS* | What is the lifecycle architecture and how is conformance checked? | Specification and conformance assessment | The standard |
| Wiley *SPE* | What follows architecturally from adopting the properties together? | Derivation from stated premises | The consequences |
| OUP *Computer Journal* | Can one substrate carry a governed domain without acquiring its behavior? | Architectural case study with falsification tests | The substrate |

Three separations hold the set apart.

**Different questions.** Each paper's central question appears in no other paper as a question. Where
one paper's answer is needed by another, it enters as a cited premise or as positioning, never as a
restated contribution.

**Different methods.** A position paper with tests, an empirical study, a conformance assessment, a
derivation from premises and an architectural case study are five genres. No two share an evidentiary
basis, so none can be read as a reworking of another.

**Explicit citation in place of reuse.** The SPE paper cites the ASE paper for positioning and
derives worker independence independently, never importing it as a premise — assuming it would make
the two mutually supporting rather than independently argued. The JSS paper cites the ASE paper as a
concurrent submission and states that no text, argument, data or evidence is reused. The SPE paper
states that it supersedes an earlier preprint rather than extending it. The Computer Journal paper
carries this separation inside the manuscript: its §1.3 reproduces the table above and states that no
text, argument, data or evidence from the other four is reused, so an editor can check the
non-overlap without this note.

## 6. Springer *Software and Systems Modeling* — Behavioral Authority in Sealed Models: Execution Semantics and Governed Evolution

No preprint DOI; posted on omnibachi.org as the Author's Original Version.

**Question: can behavioral determination be closed at the model boundary, so that construction and
execution realize a sealed model without adding domain-visible behavior?** The paper defines six
classes of domain-visible decision, gives a step-level execution semantics that refuses where the
model is silent, and reduces three properties to five checkable obligations. It evaluates one
reference realization across four application domains, and reports the obligations the realization
does not yet meet. Its subject is the *semantics*.

**The one-paper-per-publisher rule is retired.** It conflated publisher with editorial desk. Springer
publishes ASE, EMSE, REJ and SoSyM with separate boards, scopes and reviewer pools, so a SoSyM
submission is not a repeat of the ASE one. Choosing a venue for novelty rather than fit costs
reviewers who understand the work, which is the largest single factor in review quality. What remains
is narrower and worth keeping: **avoid two concurrent submissions at one desk.**

**Venue validation**, from SoSyM's own state-of-the-journal editorials: rolling submission with
online-first publication and six issues a year; 466 submissions in 2025; acceptance 23.96% in 2025
(26.45% in 2024, 22.22% in 2023); 114 days to a final decision in 2025, down from 162 in 2022; hybrid
access with a no-fee subscription route. One caveat carried into the plan — volume 24 ran 17 regular
papers against 44 special-section and 11 theme-section papers, so the regular track is narrower than
the headline rate suggests, and open theme sections are worth checking first.

**Venues considered and set aside.** *Empirical Software Engineering* is the wrong paper but the right
journal for the Governance Dividend measurement the Wiley paper predicts and does not measure — hold
it for that. *Requirements Engineering* fits the completeness half but not the transformation half,
which became the larger half once the scope was combined. *IEEE Software* is a practitioner magazine
at roughly a third of the series' usual length; the conditions-and-measurements shape would not
survive the word limit, and it would be a second IEEE magazine.

## Preprint policy differs by publisher

No single deposit strategy serves all five. The approved-server lists do not overlap.

| Publisher | Preprint servers permitted | Consequence here |
| --- | --- | --- |
| IEEE | Personal or employer website, TechRxiv, arXiv | Zenodo not permitted; use omnibachi.org |
| Springer | Broad; Research Square is native to its In Review service | Research Square used |
| Elsevier (JSS) | Broad, non-commercial preferred | No preprint of its own |
| Wiley (SPE) | Non-commercial servers only — arXiv, bioRxiv, psyArXiv, SocArXiv, engrXiv | Zenodo qualifies; Research Square does not |
| OUP (Computer Journal) | Author's Original Version anywhere, any time, commercial repositories included | Zenodo used; update the record with the Version of Record DOI on publication |

Zenodo is right for Wiley and wrong for IEEE. Research Square is right for Springer and wrong for
Wiley. Check the venue's list before depositing, not after.

## Shared material, and how it is handled

All five rest on the same architecture and the same reference realization, which is unavoidable and
disclosed in each. What differs is the role that material plays: the problem it creates (IEEE), the
agent behavior it permits (ASE), the obligations it must satisfy (JSS), the architectural
consequences it forces (SPE), and the substrate boundary it establishes (OUP). The reference
realization appears in four of the five, each time bounded to what that paper's argument needs and
each time with its limits stated.

The nine earlier preprints remain frozen as dated prior disclosure. Normalizing them to current
architecture would destroy the priority record, so they are cited for what they established when they
were written and are not revised.
