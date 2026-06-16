---
title: '#05 — Protocol as Law: Behavioral Specification and Versioned Authority'
date: '2026-02-12'
draft: false
weight: 5
slug: protocol-as-law
tags:
- PGS
- paper
- working-paper
pdf: /papers/working_papers/techpaper_5_v0.pdf
---

> **Historic working paper.** An early, DOI-published draft preserved for
> historical reference. Its implementation terminology predates the current
> PGS compiler and runtime architecture and is **superseded by the
> [current Papers](/papers/)**. Figures survive only in the canonical PDF below.

[Download PDF (canonical, with figures)](/papers/working_papers/techpaper_5_v0.pdf)

Contact: bachipeachy@gmail.com

---

## Abstract

This paper formalizes the semantics of protocol artifacts in protocol-governed systems. Building on the structural taxonomy defined in Paper 3 [Bachi, 2026c] and the governance lifecycle established in Paper 4 [Bachi, 2026d], it specifies how behavioral law is represented in ratified protocol artifacts.

We define artifact identity, naming discipline, version immutability, coexistence rules, compatibility constraints, and cross-artifact referential integrity. We formalize the deep semantics of the core protocol-layer concerns: AC_, IN_, WF_, CC_, RB_, and EV_. Each concern is specified with its semantic components and governing invariants.

This paper does not address runtime execution (Paper 6), mutation boundaries (Paper 7), computational universality (Paper 2), or economic implications (Paper 9). Its purpose is definitional: to specify what constitutes lawful behavioral specification in a protocol-governed system.

**Categories:** Software Engineering (cs.SE), Programming Languages (cs.PL), Software Architecture

**Keywords:** protocol specification, behavioral law, artifact identity, version immutability, naming discipline, referential integrity, capability contracts, workflow semantics

---

## 1. Position in the Series

Paper 1 introduced the WHAT/HOW separation and established the foundational architecture [Bachi, 2026a]. Paper 2 demonstrated that constitutional constraint is compatible with universal computation [Bachi, 2026b]. Paper 3 formalized the eight layers and ten concerns as a structural taxonomy [Bachi, 2026c]. Paper 4 defined how artifacts traverse the legislative process from Authoring through Governance to Protocol [Bachi, 2026d].

This paper focuses on a single question:

> *What constitutes behavioral law in a protocol-governed system?*

Paper 4 established *how* artifacts become ratified. This paper defines *what* ratified artifacts mean structurally. Where Paper 4 addressed the legislative process, this paper addresses the legislative product.

The answer involves three concepts: **identity**, **semantics**, and **integrity**. An artifact is lawful when it possesses deterministic identity, carries well-defined behavioral semantics, and maintains referential integrity with respect to other artifacts.

---

## 2. Protocol Layer Responsibility

The Protocol layer occupies a unique position in the eight-layer architecture. It stands between Governance (which validates) and Execution (which enforces). Its responsibility is singular: to contain the authoritative declaration of behavioral law.

### 2.1 What the Protocol Layer Contains

The Protocol layer contains:

| Content Type | Description |
|--------------|-------------|
| **Ratified artifacts** | Artifacts that have passed Governance validation |
| **Versioned declarations** | Each artifact carries explicit version identity |
| **Immutable law** | Artifact content is fixed upon ratification |
| **Behavioral specifications** | Declarations of what the system may do |

### 2.2 What the Protocol Layer Does Not Contain

The Protocol layer explicitly excludes:

| Excluded Content | Proper Layer |
|------------------|--------------|
| Drafts and proposals | Authoring |
| Validation logic | Governance |
| Execution implementation | Execution |
| Structural substrate | Structure |
| Transform implementations | Capability Transforms |
| Side-effect implementations | Capability Side Effects |

### 2.3 The Declarative Property

The Protocol layer is purely declarative. It specifies *what* the system is permitted to do, never *how* the system does it. This declarative property is constitutional, not stylistic.

Formally:

$$\text{Protocol}: \text{Artifact} \rightarrow \text{BehavioralSpecification}$$

The Protocol layer does not contain implementation code, execution logic, or runtime behavior. It contains specifications that Execution interprets. This separation ensures that behavioral law can be reasoned about independently of enforcement mechanics.

---

## 3. Artifact Identity Model

Artifact identity in protocol-governed systems is not metadata. It is constitutional—the means by which behavioral law is addressed, versioned, and referenced.

### 3.1 Canonical Naming Discipline

Every protocol artifact follows a canonical naming convention:

$$\text{ArtifactName} = \text{PREFIX}_\text{IDENTIFIER}_\text{VERSION}$$

**Example:** `WF_CREATE_WALLET_V0`

The name decomposes into three components:

| Component | Purpose | Example |
|-----------|---------|---------|
| **Concern Prefix** | Identifies behavioral type | `WF_` |
| **Semantic Identifier** | Human-readable purpose | `CREATE_WALLET` |
| **Version Suffix** | Immutable version identity | `V0` |

This naming discipline is not a convention to be followed when convenient. It is a constitutional requirement enforced by Governance validation.

**I-P1 (Name Determinism)**
The name of an artifact uniquely identifies its behavioral type and version. Given an artifact name, the concern and version are mechanically extractable.

$$\text{Parse}(\text{Name}) = (\text{Concern}, \text{Identifier}, \text{Version})$$

No two artifacts may share the same canonical name. Name collision is a governance rejection condition.

### 3.2 Identity and Addressability

Let $a_v$ represent artifact $a$ at version $v$. Identity and addressability are governed by two invariants:

**I-P2 (Version Identity)**
Two artifacts with different version suffixes are distinct behavioral entities, even if they share the same concern prefix and semantic identifier.

$$a_{v} \neq a_{v+1}$$

`WF_CREATE_WALLET_V0` and `WF_CREATE_WALLET_V1` are not two names for the same artifact. They are two distinct artifacts with potentially different behavioral specifications.

**I-P3 (Immutable Addressability)**
An artifact's fully qualified identifier resolves to exactly one immutable content body. The resolution is deterministic and permanent.

$$\text{Resolve}(a_v, t_1) = \text{Resolve}(a_v, t_2) \quad \forall t_1, t_2 > t_{\text{ratified}}$$

Once ratified, the content addressed by an artifact identifier never changes. This invariant enables behavioral auditability: the system can prove what behavior was authorized at any point in time.

### 3.3 Identifier Constraints

Semantic identifiers must satisfy structural constraints:

1. **Character set:** Uppercase alphanumeric and underscore only
2. **No leading digits:** Identifiers begin with a letter
3. **No trailing underscore:** Identifiers do not end with underscore
4. **No consecutive underscores:** Underscores serve as delimiters, not content

These constraints ensure that artifact names are parseable, sortable, and displayable across all environments without encoding issues.

---

## 4. Core Protocol Concerns

This section defines the behavioral semantics of concerns that exist in the Protocol layer. Paper 3 established the structural definition of concerns [Bachi, 2026c]. This paper provides the semantic specification.

The Protocol layer contains six concerns:

| Prefix | Name | Semantic Category |
|--------|------|-------------------|
| AC_ | Actors | Authority and Identity |
| IN_ | Intents | Authority and Intent |
| WF_ | Workflows | Orchestration |
| CC_ | Capability Contracts | Capability Binding |
| RB_ | Runtime Bindings | Capability Binding |
| EV_ | Events | Observation |

CT_ and CS_ are execution-layer concerns defined in Paper 7. They do not appear as ratified artifacts in the Protocol layer—they appear as implementations bound through CC_ and RB_.

### 4.1 AC_ — Actors

Actors define authority-bearing principals in the system. An actor is not a user account or a session token. An actor is a declared entity with explicit permissions that can be validated without runtime inference.

**Semantic Components:**

| Component | Description |
|-----------|-------------|
| **Identity** | Unique actor identifier |
| **Role** | Categorical classification for permission grouping |
| **Permission Scope** | Explicit enumeration of permitted operations |
| **Governance Constraints** | Conditions under which permissions apply |

**Invariants:**

**I-P4 (Actor Determinacy)**
Actor permissions must be derivable from the artifact itself without runtime inference. Given an actor artifact, all permissions are statically determinable.

$$\text{Permissions}(\text{AC}_a) = \text{static_derivation}(\text{Content}(\text{AC}_a))$$

**I-P5 (No Ambient Authority)**
Actors may not implicitly inherit authority from execution context. An actor possesses exactly the permissions declared in its artifact—no more.

$$\text{EffectivePermissions}(\text{AC}_a, \text{context}) = \text{DeclaredPermissions}(\text{AC}_a)$$

This invariant prevents privilege escalation through execution-time authority accumulation. The execution context cannot grant permissions that were not declared at authoring time and ratified through governance.

### 4.2 IN_ — Intents

Intents declare requested state transitions without defining orchestration. An intent is what an actor wishes to accomplish; a workflow is how the system accomplishes it.

**Semantic Components:**

| Component | Description |
|-----------|-------------|
| **Initiating Actor Type** | The actor role permitted to raise this intent |
| **Target Workflow** | The workflow that fulfills this intent |
| **Input Schema** | Structural specification of required input |
| **Precondition Constraints** | Conditions that must hold before execution |

**Invariant:**

**I-P6 (Intent-Workflow Binding)**
Every intent must map to exactly one workflow. An intent cannot be fulfilled by multiple workflows, and it cannot be fulfilled by no workflow.

$$\forall \text{IN}_i: \exists! \text{WF}_w: \text{FulfilledBy}(\text{IN}_i) = \text{WF}_w$$

Intents are declarative requests, not procedural instructions. The intent artifact declares the behavioral goal; the workflow artifact declares the behavioral means. This separation enables intent-level governance (who may request what) independent of orchestration-level governance (how requests are fulfilled).

### 4.3 WF_ — Workflows

Workflows define the orchestration of capability invocations. A workflow is a directed acyclic graph (DAG) of steps, where each step invokes a capability contract.

**Semantic Components:**

| Component | Description |
|-----------|-------------|
| **Node Set** | The steps comprising the workflow |
| **Directed Edges** | Dependencies between steps |
| **Branch Conditions** | Explicit criteria for conditional paths |
| **Deterministic Ordering** | Unambiguous execution sequence |

**Invariants:**

**I-P7 (Closed Orchestration)**
All workflow steps must reference declared capability contracts. No step may invoke an undeclared capability.

$$\forall \text{node} \in \text{WF}_w: \text{Invokes}(\text{node}) \in \{\text{CC}_1, \ldots, \text{CC}_n\}_{\text{declared}}$$

**I-P8 (No Implicit Control Flow)**
All branches and transitions must be explicitly declared. There is no default control flow, no implicit sequencing, and no fallthrough behavior.

$$\forall \text{edge} \in \text{WF}_w: \text{Declared}(\text{edge})$$

These invariants ensure that workflow behavior is fully specified in the artifact. Given a workflow artifact, all possible execution paths are statically enumerable. There are no runtime-determined paths that were not declared at authoring time.

### 4.4 CC_ — Capability Contracts

Capability contracts define permissible computation or mutation. A contract is not an implementation; it is a specification of what an implementation may do.

**Semantic Components:**

| Component | Description |
|-----------|-------------|
| **Input Schema** | Structural specification of accepted input |
| **Output Schema** | Structural specification of produced output |
| **Side-Effect Declaration** | Explicit statement of world interaction |
| **Determinism Requirement** | Whether the capability must be deterministic |
| **Governance Constraints** | Conditions and permissions governing invocation |

**Invariant:**

**I-P9 (Declared Behavior)**
A capability contract must explicitly declare whether it is pure (CT_) or mutative (CS_). There is no default; ambiguity is a governance rejection condition.

$$\forall \text{CC}_c: \text{BehaviorType}(\text{CC}_c) \in \{\text{Pure}, \text{Mutative}\}$$

The distinction between pure computation and world-affecting mutation is constitutional. Pure capabilities (CT_) are replayable, cacheable, and safe to retry. Mutative capabilities (CS_) are traced, bounded, and irreversible. The contract must declare which category applies so that execution can enforce appropriate semantics.

### 4.5 RB_ — Runtime Bindings

Runtime bindings connect capability contracts to implementations at deployment time. A binding resolves the question: for this contract, which implementation executes?

**Semantic Components:**

| Component | Description |
|-----------|-------------|
| **Contract Reference** | The capability contract being bound |
| **Implementation Reference** | The concrete implementation selected |
| **Environment Constraints** | Conditions under which this binding applies |

**Invariant:**

**I-P10 (Semantic Non-Interference)**
Runtime binding may not alter contract semantics. The bound implementation must satisfy the contract's input/output schemas and behavioral constraints.

$$\text{Semantics}(\text{CC}_c, \text{RB}_r) = \text{Semantics}(\text{CC}_c)$$

Bindings resolve implementations; they do not redefine law. This invariant ensures that behavioral guarantees established at the contract level hold regardless of which implementation is bound. Different environments may bind different implementations (for testing, performance, or deployment reasons), but all implementations must satisfy the same contract.

### 4.6 EV_ — Events

Events are declared evidence structures. An event records that something happened; it does not cause anything to happen.

**Semantic Components:**

| Component | Description |
|-----------|-------------|
| **Event Schema** | Structural specification of event content |
| **Attribution Fields** | Required provenance information |
| **Ordering Guarantees** | Constraints on event sequence |

**Invariant:**

**I-P11 (Evidence Purity)**
Events represent facts of execution and cannot themselves invoke behavior. Events are observational, not causal.

$$\text{EV}_e \rightarrow \text{Observation} \quad \text{(not)} \quad \text{EV}_e \rightarrow \text{Invocation}$$

Events appear in traces as evidence of what occurred. They cannot trigger workflows, invoke capabilities, or modify state. This invariant ensures that the trace is a faithful record, not a secondary execution path. Events cannot be governed as actions because they cannot fail, be retried, or require authorization—they are evidence of actions already taken.

---

## 5. Referential Integrity

Protocol artifacts reference one another. A workflow references capability contracts. An intent references a workflow. A runtime binding references both a contract and an implementation. These references must satisfy referential integrity constraints.

### 5.1 Reference Requirements

If artifact $a$ references artifact $b$, then:

1. **Existence:** Artifact $b$ must exist in the Protocol layer
2. **Addressability:** Artifact $b$ must be version-addressable
3. **Version Explicitness:** The reference must specify version explicitly

### 5.2 The Explicit Reference Invariant

**I-P12 (Explicit Version Reference)**
No artifact may reference another artifact without version qualification.

$$\text{Reference}(a, b) \Rightarrow \text{VersionSpecified}(b)$$

This invariant prevents semantic drift. Consider the alternative: if `WF_CREATE_WALLET_V0` could reference `CC_HASH` without version qualification, then upgrading `CC_HASH` to `V1` would silently change the workflow's behavior. The workflow would now invoke different computation without any change to the workflow artifact itself.

Explicit version reference eliminates this failure mode. When `WF_CREATE_WALLET_V0` references `CC_HASH_V0`, the behavioral specification is complete. Upgrading to `CC_HASH_V1` requires creating `WF_CREATE_WALLET_V1` with an updated reference.

### 5.3 Reference Validation

Referential integrity is validated during Governance. An artifact with an unresolvable reference is rejected:

$$\neg\text{Exists}(\text{Referenced}(a)) \Rightarrow \text{Rejected}(a)$$

An artifact with a non-versioned reference is rejected:

$$\neg\text{VersionSpecified}(\text{Reference}(a, b)) \Rightarrow \text{Rejected}(a)$$

These validation rules are mechanical. Governance does not exercise judgment about whether a missing reference is acceptable. Missing or under-specified references are categorically inadmissible.

---

## 6. Compatibility Model

Behavioral evolution must not introduce ambiguity. When artifact versions change, the relationship between versions must be explicitly categorized.

### 6.1 Compatibility Categories

Three compatibility categories are defined:

| Category | Definition |
|----------|------------|
| **Backward Compatible** | New version accepts all inputs that old version accepted |
| **Forward Compatible** | Old version accepts all outputs that new version produces |
| **Breaking Change** | Neither backward nor forward compatible |

### 6.2 Machine-Determinable Compatibility

Compatibility must be machine-determinable. Human judgment about "conceptual compatibility" is insufficient for governance purposes.

Compatibility determination uses:

1. **Schema comparison:** Input/output schemas are compared structurally
2. **Reference analysis:** Referenced artifacts are compared for compatibility
3. **Behavioral declaration analysis:** Side-effect declarations are compared

For input schemas, backward compatibility requires:

$$\text{Schema}_{v+1}^{\text{in}} \supseteq \text{Schema}_v^{\text{in}}$$

The new version must accept all inputs the old version accepted (and may accept additional inputs).

For output schemas, forward compatibility requires:

$$\text{Schema}_{v+1}^{\text{out}} \subseteq \text{Schema}_v^{\text{out}}$$

The new version must produce outputs that old version consumers can process.

### 6.3 Compatibility Declaration

**I-P13 (Explicit Compatibility Declaration)**
New artifact versions must declare compatibility category relative to prior versions.

$$\text{Create}(a_{v+1}) \Rightarrow \text{DeclaredCompatibility}(a_{v+1}, a_v)$$

This declaration is subject to validation. If an artifact declares backward compatibility but schema analysis reveals incompatibility, Governance rejects the artifact. The declaration is not a claim to be trusted; it is a claim to be verified.

---

## 7. Immutability and Coexistence

Protocol artifacts never mutate in place. This immutability is not a design preference; it is a constitutional guarantee.

### 7.1 The Immutability Guarantee

Once ratified, an artifact's content is fixed for all time:

$$\text{Ratified}(a_v, t_0) \Rightarrow \forall t > t_0: \text{Content}(a_v, t) = \text{Content}(a_v, t_0)$$

There is no mechanism for in-place modification of ratified artifacts. The Governance layer does not provide an "update" operation. Behavioral change requires creation of a new version.

### 7.2 Version Coexistence

Multiple versions of an artifact may coexist simultaneously.

**I-P14 (Non-Override Rule)**
No new version may overwrite the identifier of a previous version.

$$\text{Create}(a_{v+1}) \Rightarrow \text{Exists}(a_v) \land \text{Addressable}(a_v)$$

Creating `WF_CREATE_WALLET_V1` does not delete, deprecate, or diminish `WF_CREATE_WALLET_V0`. Both versions exist, both are addressable, and both may be invoked.

### 7.3 Coexistence Benefits

Coexistence enables:

| Benefit | Description |
|---------|-------------|
| **Gradual migration** | Systems can adopt new versions incrementally |
| **Parallel deployment** | Different environments may use different versions |
| **Behavioral auditability** | Historical behavior is preserved and verifiable |
| **Rollback capability** | Previous versions remain available |

Coexistence is not merely tolerated; it is the architectural foundation for controlled evolution. The system does not assume that new versions are better. It permits old and new to coexist while governance processes determine appropriate adoption.

---

## 8. Behavioral Change Discipline

Behavioral change in protocol-governed systems follows a disciplined process. This discipline is not procedural guidance; it is constitutionally enforced.

### 8.1 Permitted Change Patterns

Behavioral change occurs through three permitted patterns:

| Pattern | Description |
|---------|-------------|
| **Version Introduction** | A new artifact version is created |
| **Reference Update** | Referencing artifacts are updated to point to new versions |
| **Deprecation Annotation** | Old versions are marked deprecated |

All three patterns preserve immutability. No pattern modifies existing artifact content.

### 8.2 Prohibited Change Patterns

The following change patterns are constitutionally prohibited:

| Prohibited Pattern | Violation |
|--------------------|-----------|
| **Silent semantic modification** | Violates I-P3 (Immutable Addressability) |
| **Implicit upgrade** | Violates I-P12 (Explicit Version Reference) |
| **Runtime reinterpretation** | Violates I-P10 (Semantic Non-Interference) |
| **Retroactive mutation** | Violates immutability guarantee |

There is no mechanism in the architecture to perform these operations. They are not merely discouraged; they are unimplementable.

### 8.3 Change Traceability

Every behavioral change is traceable:

1. **What changed:** The new artifact version documents the change
2. **When it changed:** Ratification timestamp is recorded
3. **Who authorized it:** Governance authority is attributed
4. **What references it:** Referencing artifacts are enumerable

This traceability is structural, not reconstructed from logs. The artifact graph itself constitutes the change record.

---

## 9. Separation from Execution

This paper defines protocol specification. It explicitly does not define protocol execution.

### 9.1 The Specification-Execution Boundary

Protocol artifacts declare behavior:

$$\text{Protocol}: \text{Artifact} \rightarrow \text{Specification}$$

Execution interprets behavior:

$$\text{Execution}: \text{Specification} \times \text{Input} \rightarrow \text{Trace}$$

These functions are independent. Protocol specification does not depend on execution mechanics. Execution mechanics do not alter protocol semantics.

### 9.2 What This Paper Does Not Address

| Topic | Addressed In |
|-------|--------------|
| DAG compilation | Paper 6 |
| Node routing | Paper 6 |
| Trace generation | Paper 6 |
| Transform execution | Paper 7 |
| Side-effect execution | Paper 7 |
| Determinism verification | Paper 6 |
| Cross-engine conformance | Paper 6 |

### 9.3 Protocol Contains No Implementation

Protocol artifacts never contain implementation code. A workflow specifies which capabilities to invoke in which order; it does not contain the code that executes those capabilities. A capability contract specifies input/output schemas and behavioral constraints; it does not contain the transformation logic.

This separation ensures that protocol artifacts can be:

1. **Analyzed statically:** All behavioral properties are derivable from specification
2. **Versioned independently:** Protocol versions and implementation versions evolve separately
3. **Governed uniformly:** The same governance process applies regardless of implementation language or platform

---

## 10. Structural Consequences

The specification model defined in this paper yields six structural consequences:

### 10.1 Deterministic Artifact Identity

Every artifact has exactly one canonical name. The name encodes concern, semantic purpose, and version. Given any artifact name, these components are mechanically extractable. There is no ambiguity about what an artifact is.

### 10.2 Explicit Behavioral Surface

The behavioral surface of the system is the set of ratified protocol artifacts. This surface is:

- **Finite:** The artifact set is bounded and enumerable
- **Explicit:** Every behavior corresponds to a declared artifact
- **Version-addressed:** Each behavior is tied to a specific version

There are no implicit behaviors. If a behavior is not declared in a protocol artifact, it cannot occur.

### 10.3 Version-Addressable History

The complete behavioral history of the system is preserved:

- Every artifact version that ever existed remains addressable
- Every reference relationship is explicit and versioned
- Every governance decision is attributable

This history is not an audit log reconstructed from events. It is the artifact graph itself.

### 10.4 Controlled Evolution

Behavioral evolution is controlled through:

- **Explicit versioning:** New behavior requires new versions
- **Explicit reference:** Adoption requires updated references
- **Compatibility declaration:** Version relationships are categorized

Evolution cannot be silent or implicit. Every change is declared, validated, and recorded.

### 10.5 Referential Integrity

Cross-artifact references are governed:

- References must resolve
- References must specify version
- Broken references are governance rejections

The artifact graph is always consistent. There are no dangling references or unversioned dependencies.

### 10.6 Absence of Implicit Semantics

Nothing is implicit:

- No implicit permissions (I-P5)
- No implicit control flow (I-P8)
- No implicit behavior types (I-P9)
- No implicit references (I-P12)

Every behavioral property is explicitly declared in artifacts. Execution interprets these explicit declarations; it does not infer unstated intent.

---

## 11. Limitations

This paper:

- **Does not define execution routing.** How the execution engine routes artifacts to implementations is addressed in Paper 6.

- **Does not define mutation boundaries.** The distinction between CT_ and CS_ at execution time is addressed in Paper 7.

- **Does not address security analysis.** The security implications of specification mechanics are addressed in Paper 8.

- **Does not quantify economic effects.** The cost-benefit analysis of specification discipline is addressed in Paper 9.

- **Does not restate universality claims.** Computational completeness was established in Paper 2 and is not revisited here.

Its scope is specification semantics only: what constitutes lawful behavioral specification and how specification artifacts relate to one another.

---

## 12. Conclusion

Protocol-governed systems treat behavioral artifacts as law. This treatment is not metaphorical; it is constitutional. Protocol artifacts declare what the system may do, and execution enforces those declarations without deviation.

This paper established fourteen invariants governing protocol specification:

| Invariant | Statement |
|-----------|-----------|
| I-P1 | The name of an artifact uniquely identifies its behavioral type and version |
| I-P2 | Two artifacts with different version suffixes are distinct behavioral entities |
| I-P3 | An artifact's fully qualified identifier resolves to exactly one immutable content body |
| I-P4 | Actor permissions must be derivable from the artifact itself without runtime inference |
| I-P5 | Actors may not implicitly inherit authority from execution context |
| I-P6 | Every intent must map to exactly one workflow |
| I-P7 | All workflow steps must reference declared capability contracts |
| I-P8 | All branches and transitions must be explicitly declared |
| I-P9 | A capability contract must explicitly declare whether it is pure or mutative |
| I-P10 | Runtime binding may not alter contract semantics |
| I-P11 | Events represent facts of execution and cannot themselves invoke behavior |
| I-P12 | No artifact may reference another artifact without version qualification |
| I-P13 | New artifact versions must declare compatibility category relative to prior versions |
| I-P14 | No new version may overwrite the identifier of a previous version |

These invariants are not design guidelines to be followed when convenient. They are constitutional constraints enforced by the architecture. Artifacts that violate these invariants are rejected by Governance; they never reach the Protocol layer.

The relationship between the papers establishes the full legislative model:

> **Governance (Paper 4) makes law admissible.**
> **Protocol (this paper) defines what law contains.**
> **Execution (Paper 6) enforces law.**

Specification is therefore constitutional, not descriptive. A protocol artifact is not documentation of intended behavior. It is the authoritative declaration of permitted behavior—behavioral law in the most literal sense.

---

## License and Use

This work is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).

You are free to share and redistribute this material in any medium or format, provided that: appropriate credit is given to the author, the material is not used for commercial purposes, and the material is not modified, transformed, or built upon.

The paper does not grant rights to implement patented methods, systems, or workflows that may be covered by pending or future patent claims.

For licensing inquiries or permissions beyond the scope of this license, contact the author.

---

## Author Information

**Bachi (aka Bhash Ganti)**
Contact: bachipeachy@gmail.com

**Conflict of Interest:** The author is developing commercial implementations of the described architecture.

---

## References

Bachi aka Bhash Ganti (2026a). Protocol-Governed Systems: An architectural foundation for the AI era. *Zenodo Working Paper. DOI: https://doi.org/10.5281/zenodo.18715516 *

Bachi aka Bhash Ganti (2026b). Protocol-Governed Systems: A constitutional realization of Turing-complete systems. *SZenodo Working Paper. DOI: https://doi.org/10.5281/zenodo.18718409 *

Bachi aka Bhash Ganti (2026c). The Layer-Concern Constitutional Model: A formal structural taxonomy for protocol-governed systems. *SZenodo Working Paper. DOI: https://zenodo.org/doi/10.5281/zenodo.18719589 *

Bachi aka Bhash Ganti (2026d). Governance and Authoring: The legislative process of behavioral law. *SZenodo Working Paper. DOI: https://zenodo.org/doi/10.5281/zenodo.18929868 *.

Dijkstra, E.W. (1974). On the role of scientific thought. EWD447.

Lamport, L. (2002). *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley.

Meyer, B. (1988). *Object-Oriented Software Construction*. Prentice Hall.

Parnas, D.L. (1972). On the criteria to be used in decomposing systems into modules. *Communications of the ACM*, 15(12):1053–1058.

Saltzer, J.H., and Schroeder, M.D. (1975). The protection of information in computer systems. *Proceedings of the IEEE*, 63(9):1278–1308.

Spivey, J.M. (1989). *The Z Notation: A Reference Manual*. Prentice Hall.
