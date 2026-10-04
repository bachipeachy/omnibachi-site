# ASE paper — tables

## Table 1 · Related work by locus of authority

The cut is *who performs* against *who authorizes*, not lifecycle stage. **Carried in the artifact**
has the sense given in §2.2: the authorization decision is represented in the executable state
itself, so a party absent when the decision was made can read it from what the system carries. A
"no" does not mean an approach lacks policy or provenance; it means the decision is not part of what
executes.

| Approach | Who performs the engineering | Who authorizes the resulting state | Carried in the artifact? |
|---|---|---|---|
| AI as assistant (Vaithilingam et al. 2022) | human specifies, agent generates | human, implicitly at acceptance | no |
| AI as collaborator (Ross et al. 2023) | human and agent iterate | human, implicitly and continuously | no |
| AI as autonomous engineer (Jimenez et al. 2024) | agent, from a goal | unstated — acceptance is the only gate | no |
| Agentic software engineering (Yang et al. 2024) | agent plans, invokes tools, edits, tests, iterates | unstated — repository write access *is* authority | no |
| Supply-chain provenance (OpenSSF 2026), (Torres-Arias et al. 2019), (Newman et al. 2022), (Reproducible Builds 2026) | either | not addressed — attests production, not permission | provenance only |
| Admission and policy (Kubernetes 2026), (OPA 2026), (SPIFFE 2026) | either | policy engine, at a boundary, per request | no — policy is external |
| Model-driven engineering (OMG 2014), (OMG 2011) | either | not addressed — models are generation inputs | no |
| Change and release management | either | an approval event, recorded beside the system | no |
| **PGC** (Ganti 2026) | agent may perform every open step | established at scope, authorized at promotion, declared | **yes — in the sealed snapshot** |

The first four rows are the analytical patterns of §2.1, each cited to one representative instance
rather than to a settled taxonomy. The remaining rows name mechanism families.

---

## Table 2 · Research questions, and what each can establish

| RQ | Unit of analysis | Procedure | Claimed boundary | Evidence artifact | Achieved rung | Non-claim |
|---|---|---|---|---|---|---|
| RQ1 | one governed change | worker performs P0–P8 and construction; candidate compiled and sealed | the worker-performable path ends at candidate production | the G4 run dossier; successor `48fd5a4d…` | **observed** | that a different author obtains the same result |
| RQ2 | four authority boundaries | see 5b | authority does not move with the authoring actor | carried artifact identities; refusal records | **observed** ×2, **declared** ×2 | external effects; the profile selects no interaction boundary |
| RQ3 | the retained record set | enumerate what a holder of the artifacts alone can establish | the successor and authority relation is reconstructable | snapshot identity, evidence records, inspection surface | **reachable** | that a third party performed the reconstruction; sealing is integrity, not signature |
| RQ4 | demonstration–guard pair | disable the guard, re-run its demonstrations | the evidence discriminates against the guard's absence | the mutation ledger, Table 6 | **discriminating** ×4, **reachable** ×2 | a mutation score; selection was risk-directed and not preregistered |

---

## Table 3 · The collaboration model

Three questions are kept apart in every row: who holds authority, who performs the work, and what
the machine determines or enforces.

| Activity | Human authority | Agent activity | Machine determination |
|---|---|---|---|
| Scope | authoritative | cannot establish | recorded in the profile |
| Business problem | authoritative | may elaborate, may not decide | constrained by the P0 rule set |
| Analysis | may inspect | performs | checked — P2–P4 rule sets, grounding at P2 |
| Design derivation | may inspect | performs | checked — P5–P7, 93 rules |
| Construction | none required — the act confers nothing | performs | checked — material is refused, not repaired |
| Admission | none required | produces the candidate that is judged, but does not decide | **enforced** — compilation admits or refuses |
| Promotion | authoritative — an operator act | cannot perform; no promotion operation exists | **not enforced at a promotion call** — the separation is structural, §5.5 |
| Sealing | none required | cannot perform | **enforced against admission** — only compiled, attested projections are sealed |
| Execution | no intervention required | absent | enforced — traversal only, no new determination |
| Evolution | authorizes the successor | performs the transformation | checked — identity derived from content, carried artifacts comparable |

Two cells are read wrongly if taken alone. The human authorizes *promotion of the result*, never the
construction act — construction requires no authorization because it produces nothing authoritative.
And *may inspect* is an available action, not a required one: the architecture does not depend on a
human reading agent output.

---

## Table 4 · The P0–P8 rule sets

Every column is read from `transformation/transformation/design/p*/rules.py` and the phase templates
at one pinned revision of each repository. Registers are the numbered template sections only; rules
are counted by distinct identifier.

| Phase | Registers | Rules | Priors consumed | Inspector operations |
|---|---:|---:|---|---|
| P0 Change Seed | 20 | 3 | — | — |
| P1 Change Request | 19 | 3 | P0 | — |
| P2 Domain Model Verification | 8 | 5 | P1 | `si.artifact.list` |
| P3 Analysis Loop | 7 | 10 | P2 | `si.artifact.list`, `si.snapshot.summary` |
| P4 Business Model | 7 | 8 | P3 | `si.artifact.list` |
| P5 Business Intent | 8 | 12 | **P0** | `si.artifact.list` |
| P6 Governance Intent | 6 | 11 | P5, **P0** | `si.artifact.list` |
| P7 Design Intent | 20 | **70** | P5, P6, **P0** | `si.artifact.list`, `si.capability.surface`, `si.rule_set.list`, `si.store.list` |
| P8 Authoring Mandate | 7 | 12 | P7 | `si.artifact.list` |

Three readings the table supports, and one it does not.

- **P7 carries seventy rules** against three to twelve everywhere else. That locates the
  implementation's weight in the design concern; it does not make that concern more important.
- **Only P2 declares `GROUNDING_RULES`.** The grounding boundary is a specific phase, not a posture.
  `BASELINE_IDENTITY_UNRESOLVED` fires when a cited artifact does not resolve against the baseline.
- **The priors are not a chain.** P5 consumes **P0**, not P4; P6 consumes P5 and P0; P7 consumes P5,
  P6 and P0. The intent phases ground in the stated problem rather than in the analysis of it.
- **What it does not support:** that a phase reads only its declared priors. The relation is
  declared, not enforced as a closed input surface — §5.2.

---

## Table 5 · RQ2 boundary matrix

| Boundary | Stimulus applied | Attempted | Refusal observed | Discriminating | Rung | Untested |
|---|---|---|---|---|---|---|
| Baseline integrity | carried-identity comparison; `snapshot:wrong` fixture | yes | yes — `baseline_identity_mismatch` | yes, after the §8.4 repair | **observed** | a direct write to a sealed baseline |
| Behavioural determination | runtime built only from the sealed snapshot; duplicate-loan case | yes | yes — `copy_already_on_loan` | yes | **observed**, for the exercised capability and read operation | absent route; undeclared state; runtime governance change |
| Scope | none | no | — | — | **declared** | every scope-change path |
| Promotion | none — no promotion operation exists, §5.5 | no | — | — | **declared**, no enforcement point | whether an agent with operator access could seal a successor |

Two boundaries reached *observed*, and only for the stimuli applied. Two remain *declared*. An absent
attempt is not a boundary that held.

---

## Table 6 · The mutation ledger

Six mutation instances across five guard families — the refusal family contributes two, counted
separately. Fig. 14 carries the discrimination logic; this carries the data. The two centre columns
are separate datasets — the suite as delivered, and the same mutation re-run against the repaired suite. The
second does not validate the first.

| Mutation | Demonstrations at delivery | First delivery | After repair | What it establishes |
|---|---:|---|---|---|
| required SHA-256 digest replaced with MD5 | 6 | all passed | **failed** (7 demonstrations) | non-discriminating at delivery; discriminating once a digest demonstration was added |
| baseline-grounding guard disabled | 21 | all passed | **failed** (22 demonstrations) | non-discriminating at delivery; discriminating once a negative demonstration was added |
| declared routing replaced with an equivalent hard-coded branch | 22 | **failed** | — | discriminating — behaviour demonstrably read from sealed state |
| declared routes map emptied | 22 | **failed** | — | declared routing is load-bearing, not incidental |
| declared refusal removed — `copy_already_on_loan` | 22 | **failed** | — | refusal is demonstrated rather than asserted |
| declared refusal removed — `unknown_check_kind` | 22 | **failed** | — | the closed check-kind set is demonstrated, not asserted |

The first two guards were **present** in the implementation and **required by the profile**; whether
each is correct was not separately established. What the mutation shows is that the demonstrations
offered for them would have passed had the guards been absent. Each row's suite is the scope the
mutation was applied to: the digest mutation is non-discriminating within the realization suite that
claimed the property, and the grounding mutation within the full G4 suite. Selection was
risk-directed, made by the evaluating side after delivery, and not preregistered; no mutation score
over a seeded population is reported. This measures the adequacy of specific demonstrations, not
coverage of the suite.

---

## Table 7 · Limitations

| Limitation | Bounds which surface | What this bounds, and what remains supported |
|---|---|---|
| One worker model | all of §7 — three profile-authoring runs, the realization, the transformation | nothing in this study varies the producer; a second worker against the same scaffold is the single change that would most strengthen the result |
| One authoring run independent of prior context | the sufficiency finding; the other two shared a context | future work |
| No actor outside the scaffold | worker independence is examined *within* a governance scaffold, not against one bypassed | future work |
| **No firewall at the transformation gate** | RQ1 and every RQ2 observation drawn from G4 — the worker had built the subject | deliberate: the gate asks whether governed *state* carries what evolution requires, not whether a specification suffices to build from |
| **Refusals exercised by fixtures** | the three demonstrated refusal paths — none was a candidate the worker produced and governance rejected | supports *the refusal is reachable and discriminating*; not *a worker provoked it* |
| **Promotion has no enforcement point** | RQ2's promotion row — no callable promotes, no actor check gates one | promotion lies outside the agent's reach by deployment, not by an enforced transition |
| **Evaluator degrees of freedom** | RQ4 and the mutation ledger — instruments, classification and selection all sit on the evaluating side | model separation is not evaluator independence; nothing preregistered, selection and outcomes recorded, not blinded |
| **No blind reconstruction** | RQ3 — sufficiency of the retained surface was enumerated, not exercised by a third party | independent inspectability is *reachable*, not *observed* |
| Comparative conformance did not run | the profile excludes the reference implementation by construction | a design question, not a failed run |
| No external effect exercised | the capability surface; the profile selects no interaction boundary | untested, not failed |
| One binding is implementation-specific | the execution claim — dispatch on declared effect value, no declared binding artifact | a known deviation |
| Single-node, unsigned, locally sealed | integrity through content-derived identity, not signature | distributed and multi-party governance unexercised |
| Environment unpinned, governance anchor unversioned | the reproducibility claim | reproduced in the authors' environment with the anchor at `software_governance` `v3`; the build does not enforce that pairing, and independent reproducibility is not demonstrated |
| **One retained record superseded and not regenerated** | RQ3 — `transformation_evidence.md` carries a transformation identity the retained code does not reproduce | the relation is stated (`superseded_by`) and the artifacts still reconstruct to `48fd5a4d…`; the retained set is not internally consistent |
| Overhead unmeasured | no cost reported for compilation, sealing or governed traversal | future work |
| Conditional, cascading, revocable authorization | outside the exercised surface | **not claimed**, not absent |
| Governance is not quality | what a model-backed capability is authorized to do, not what it returns | out of scope by construction |
| Adoption not evaluated | migration cost, operational suitability, comparative economics | out of scope |

---

## Table 8 · Threat model

| Party | Trusted for | Not trusted for, or not established | Capability in this realization |
|---|---|---|---|
| **Worker** (the agent) | nothing — the design assumes it may emit inadmissible, ungrounded or self-serving material | authorship of the profile; scope; promotion; writing a sealed baseline | full read of the baseline through the inspection surface; authors phase artifacts and construction inputs; submits candidates |
| **Commissioning side** (evaluating model) | writing instruments and classifying findings | independence from the operator — the same operator directed both roles | devises and runs mutations; does not author or promote |
| **Operator** (the human) | establishing scope and the profile; adopting a sealed successor as the next baseline | honesty — sealing is local and unsigned, so a record altered before sealing is indistinguishable from an honest one; no actor check gates adoption | full filesystem and repository access; runs the toolchain; performs promotion by act, not by callable |
| **Compiler** | refusing material that violates the governing surface, and emitting the projection metadata sealing consumes | its own integrity — a modified compiler is not detectable from the artifacts it emits | admits or refuses candidates; resolves the governance surface by location |
| **Assembler** | consuming only compiled projections, and failing hard on a missing, empty or self-inconsistent hash | its own integrity, for the same reason | seals; computes the content-derived identity |
| **Runtime** | traversing only declared nodes, bindings, routes and outcomes | correctness of what was declared; behaviour of any effect outside the system | reads the sealed snapshot; writes only what a declared effect declares |
| **Repository / governance surface** | carrying the declarations the compiler resolves | immutability — the anchor is identified by location, not revision, so a later surface can govern an unchanged source build | supplies the governance surface at build time |

**Excluded from the model.** A malicious operator; a modified toolchain; a compromised host; network
adversaries — the exercised profile selects no interaction boundary; multi-party or distributed
governance; key compromise, since nothing is signed; and denial of service. Content-derived identity
detects alteration of retained content; it is not authentication, and it cannot distinguish an honest
operator from one who altered a record before sealing.

---
