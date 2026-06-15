---
title: Chapter 3 — Constitutional Authoring
date: '2026-02-12'
draft: false
weight: 5
slug: chapter-3-constitutional-authoring
---

Chapter 1 diagnosed the pathology --- structural governance debt. Chapter 2 defined the cure --- Protocol-Governed Systems --- and laid out the eight-layer architecture with its ten canonical concerns. The paradigm is established. The vocabulary is defined. But paradigms do not build systems. Artifacts do.

This chapter is where the reader picks up a pen. It answers the central question of PGS authoring: **How do you express system behavior as governance artifacts --- and how does the system guarantee that those artifacts are structurally complete before any execution occurs?**

The stakes are practical. In the application-centric model, the distance between writing code and discovering its governance failures is measured in weeks --- sometimes months, sometimes production incidents. In PGS, that distance is zero. Constitutional authoring means that incomplete, inconsistent, or structurally invalid behavior is rejected at the moment of declaration, not at the moment of failure. The chapter walks through the complete authoring lifecycle --- Draft, Validation, Ratification --- using a concrete User Registration flow as the running example. By the end, the reader will have authored five governance artifacts (an Intent, a Workflow, and three Capability Contracts), seen the five constitutional validation checks that every artifact must pass, and witnessed the system generate a complete execution graph from those declarations alone.

Every engineer has experienced the moment when a simple feature request turns into an archaeological expedition. "Add a new field to the user profile" becomes three days of tracing code paths, discovering undocumented dependencies, and testing interactions that no one can fully enumerate. The fear is not that the change is hard --- it is that the consequences are unknowable. Constitutional authoring exists to make those consequences knowable. The artifacts in this chapter are not bureaucratic overhead. They are the structural mechanism that replaces "I think this is safe" with "the system proves this is safe." The formalism that follows is the engineering response to the human experience of working in systems whose rules exist only in people's heads.

## 3.1 --- The Engineering Objective

In the application-centric model, implementing "User Registration" means writing code: a controller receives the request, a service validates the input, a repository writes to a database, an event publisher emits a message. The business rules --- what constitutes a valid registration, what identifier scheme to use, how to handle duplicates --- are distributed across these components and discoverable only by reading the code.

**The Task:** Implement a User Registration flow that:

1.  Accepts a user record (first name, last name, email)
2.  Generates a deterministic user identifier
3.  Registers the user's credentials in a lookup index
4.  Emits an immutable audit event

**The Constraint:** No application code may be written. All behavior must be defined in declarative, versioned governance artifacts that pass constitutional validation before execution.

In the application-centric approach, this task produces a codebase --- a set of files containing business logic, infrastructure plumbing, and implicit behavioral contracts, all intertwined. In PGS, this task produces a set of governance artifacts and a system-generated execution graph. The artifacts are authored as YAML, embedded in human-readable markdown files, and organized into governance registries. They declare what the system does. The graph proves that declaration is structurally complete. These artifacts are not yet executable --- they must first pass through a compilation step (Chapter 4) that transforms them into the machine-readable protocol artifacts the engine loads.

## 3.2 --- Artifact 1: The Intent (IN_)

In practice, authors write these artifacts as YAML files in a standard IDE. A CLI validator or IDE plugin performs the five validation checks described in Section 3.5 before ratification. The experience is closer to compiling code than submitting a document for review.

**Definition:** An Intent is a formal declaration of a requested state transition --- what the author wants the system to do.

**Key Properties:**

1.  **Schema-Bound.** Inputs are validated against a declared schema. A request missing a required field is rejected before any logic executes.
2.  **Outcome-Bounded.** The set of possible results (ACK, NACK) is finite and declared in the artifact. No other outcomes can occur.
3.  **Workflow-Bound.** The intent names the specific workflow responsible for fulfillment. Multiple intents may be fulfilled by a single workflow. The binding is structural, not discovered at runtime.

### Example 3.1 --- Authoring IN_USER_REGISTERED_V0

*(The full artifact is provided in Appendix B, Example 3.1.)*

**Analysis:**

- **Input validation is pre-execution.** A request missing `email` or providing an invalid format is rejected by the governance layer --- not by a try/catch block in application code. The validation is deterministic and occurs before the workflow begins.
- **The workflow binding is a hard structural link.** `workflow: WF_REGISTER_USER_UNVERIFIED_V0` means this intent can only be fulfilled by that workflow. The binding is declared in the artifact, not computed by a router.
- **The artifact does not contain logic.** No branching, no computation, no side effects. The intent declares the interface --- what goes in and what comes out. How the request is processed is the workflow's concern.

### What the Header Declares

The header fields carry architectural meaning:

- `governed_by: CONSTITUTION_INTENTS_V0` --- this artifact must conform to the constitutional schema for intents. The validation system uses this reference to select the correct schema.
- `version: v0` --- this is a behavioral version, not a release version. If registration requirements change, a new version (v1) is authored. Version v0 remains immutable and addressable. Both versions can coexist.

## 3.3 --- Artifact 2: The Workflow (WF_)

**Definition:** A Workflow is a directed acyclic graph of capability invocations --- the governed sequence of steps that fulfills an intent.

**Key Properties:**

1.  **Step-Wise.** Execution proceeds node by node through the graph.
2.  **Explicitly Branched.** Every possible outcome of every step must have a declared edge. No implicit fallthrough paths.
3.  **Capability-Bound.** Steps reference Capability Contracts (CC_) by code, not implementations. The workflow does not know what programming language will execute it.

### Example 3.2 --- Authoring WF_REGISTER_USER_UNVERIFIED_V0

*(The full artifact is provided in Appendix B, Example 3.2.)*

**Analysis:**

- **Data flow is structural.** `$.payload.user_id` references a specific location in the execution context. The workflow declares what data each step needs; the engine resolves the references. Data dependencies are visible from the artifact alone.
- **Branching is explicit.** CC_REGISTER_USER_KYC_V0 has four outcomes. Both SUCCESS and ALREADY_EXISTS proceed to the event step --- duplicate registration is a valid, non-terminal state. VIOLATION and BACKEND_ERROR terminate the workflow. These rules are behavioral law, not conditional logic.
- **Completeness is verifiable.** Every outcome of every node has a `next` target. If one were missing, the artifact would fail validation --- the system rejects incomplete graphs before they can execute.

## 3.4 --- Artifact 3: The Capability Contract (CC_)

**Definition:** A Capability Contract defines the permission boundary of a single workflow step --- what it is allowed to do, what it receives, and what it produces.

**The CT/CS Split:**

This is where the paradigm's most fundamental execution boundary becomes visible. Every pipeline step in a capability contract is classified by prefix:

- **CT_ (Capability Transform):** Pure computation. No side effects. Cannot write to a database, call an API, or mutate any external state. This is constitutional, not conventional.
- **CS_ (Capability Side Effect):** Governed world interaction. Can persist data, emit events, or modify external state --- but only within the scope declared in the artifact.

### Example 3.3 --- Pure Computation (CC_GENERATE_USER_ID_V0)

*(The full artifact is provided in Appendix B, Example 3.3.)*

**Analysis:**

- **The pipeline is CT-only.** This contract is constitutionally guaranteed to be side-effect-free. It cannot write to a database, not because of a code review rule, but because the CT_ prefix structurally prohibits I/O operations.
- **The result status contract is bounded.** Only SUCCESS and VIOLATION are permitted outcomes. The engine will reject any result not in this list.
- **Bindings declare data flow.** The `inputs` block maps contract inputs to transform arguments. The `outputs` block maps transform results back to the contract's output surface. Both are declared --- not computed by the engine.

### Example 3.4 --- Mixed Pipeline (CC_REGISTER_USER_KYC_V0)

*(The full artifact is provided in Appendix B, Example 3.4.)*

**Analysis:**

- **The CT/CS boundary is visible in the pipeline.** Step 1 computes (CT_). Step 2 persists (CS_). The reader can see, from the artifact alone, where computation ends and world interaction begins.
- **Step 2 references Step 1's output.** `$.results.CT_PURE_GENERATE_ID_V0.kyc_key` chains the pipeline --- the KYC key computed by the pure transform becomes the registry key for the side effect. Data flows through declared expressions, not function calls.
- **The result status contract is wider.** Four outcomes are permitted, including ALREADY_EXISTS (duplicate) and BACKEND_ERROR (storage failure). The engine grants world-interaction permission only within the declared scope of CS_USER_ALIAS_INDEX_V0 --- nowhere else.

### Example 3.5 --- Side-Effect Only (CC_APPEND_USER_EVENT_V0)

*(The full artifact is provided in Appendix B, Example 3.5.)*

**Analysis:**

- **The pipeline is CS-only.** This contract's sole purpose is to append a record to an immutable event log. No computation precedes it.
- **The operation is APPEND.** The underlying runtime (CS_APPENDONLY_JSONL) is an append-only log: records can be added but never modified or deleted. This is a constitutional property of the runtime, not a developer choice.
- **The record is assembled from declared expressions.** The engine resolves `$.inputs.event_type`, `$.inputs.user_id`, and `$.inputs.data` and assembles the record. The engine does not know this record represents a user registration event. It sees a structured input to a side-effect operation.

**A note on bindings.** The reader may wonder: how does `CT_PURE_GENERATE_ID_V0` map to an actual function? The answer is runtime bindings --- a separate artifact type (RB_) that maps abstract capability codes to concrete implementations at build time. Bindings are not authored in capability contracts; they are resolved independently. Chapter 5 covers this mechanism. For now, it is sufficient to understand that the contract declares *what* is permitted; the binding resolves *how* it executes.

## 3.5 --- Validation and Failure Surface

In PGS, you do not run code to find errors. You submit artifacts for constitutional validation. The Governance layer acts as a strict compiler --- it enforces structural rules deterministically, before any execution cost is incurred.

Every artifact must traverse the following enforcement pipeline before ratification. Failure at any stage terminates the pipeline with rejection.

> **[DIAGRAM 4] --- Governance Enforcement Pipeline**

    Authored Artifact (DRAFT)
            ↓
    Prefix Validation
            ↓
    Schema Validation
            ↓
    Referential Integrity
            ↓
    Layer–Concern Consistency
            ↓
    Ratification (Hash Recorded)
            ↓
    Protocol Layer Promotion

> *Each stage is a gate. Success at all stages produces a ratified, immutable, enforceable artifact.*

### The Five Validation Checks

  -------------------------------------------------------------------------------------------------------
  Step     Check              What It Verifies          Failure Condition
  -------- ------------------ ------------------------- -------------------------------------------------
  1        **Schema**         Artifact structure        Missing field, wrong type, malformed YAML

  2        **Vocabulary**     Prefix registration       Unregistered prefix (e.g., `XY_`)

  3        **Prefix**         Kind/prefix match         Intent artifact with CC_ prefix

  4        **Integrity**      Reference resolution      `next: CC_MISSING_V0` --- target does not exist

  5        **Completeness**   Outcome coverage          A node outcome has no declared edge
  -------------------------------------------------------------------------------------------------------

**Rule:** An artifact is ratified if and only if it passes all five checks. There is no partial admissibility. Failure at any step rejects the artifact entirely.

Vocabulary enforcement is evaluated during validation, not during execution. By the time the engine runs, every artifact has passed vocabulary checks. The engine never encounters an unrecognized prefix --- not because it rejects them at runtime, but because the validation pipeline structurally prevents them from reaching the engine.

### A Deliberate Failure

Suppose an author references a capability transform that does not exist *(see Appendix B, Example 3.6)*:

The validation system produces a deterministic diagnostic:

    VALIDATION FAILURE
      Artifact:   CC_GENERATE_USER_ID_V0
      Check:      Referential Integrity
      Rule:       Pipeline references must resolve to registered capabilities
      Location:   core.pipeline[0]
      Detail:     CT_MAGIC_HASH_V0 is not a registered capability transform
      Resolution: Use a registered CT_ artifact or register CT_MAGIC_HASH_V0

The failure identifies the artifact, the check that failed, the location, and the correction path. This is not a runtime stack trace. It is a structural diagnostic at authoring time. The distance between authoring and failure is zero.

## 3.6 --- Structural Insight (Doctrine Moment)

The reader has now seen five governance artifacts authored and a validation pipeline that enforces constitutional rules. This section connects the example to the paradigm.

What the reader witnessed is a legislative process --- not metaphorically, but structurally:

  -----------------------------------------------------------------
  Legislative Concept   PGS Equivalent
  --------------------- -------------------------------------------
  **Proposal**          Drafted artifact (Tooling layer)

  **Examination**       Governance validation (5 checks)

  **Ratification**      Promotion to Protocol layer

  **Law**               Ratified, immutable, enforceable artifact
  -----------------------------------------------------------------

A proposal becomes law through ratification. No proposal becomes law without passing governance. No law may be created directly in the Protocol layer.

**Ratification transfers behavioral authority from author to system.** Before ratification, the author has discretion --- they can modify, restructure, or discard the artifact. After ratification, the artifact is version-locked. Its content is immutable. It carries behavioral authority that the execution engine will enforce. The author's discretion is consumed. Behavioral law evolves by addition --- new versions --- not by mutation of existing ones.

This is Chapter 2's **Property 2** made visible: *Authoring is constitutionally constrained and validated against formal protocol definitions.* The five validation checks are the constitutional constraint. The lifecycle progression --- Draft → Validation → Ratified --- is the mechanism that prevents ungoverned artifacts from reaching execution.

**Structural impossibility (Invariant I-G8 --- No Execution-Level Law Creation):** The execution engine cannot create, modify, or bypass ratified artifacts. It enforces law; it does not make law. Execution is constitutionally subordinate to Protocol. The Execution layer has no authority over the Protocol layer.

This separation becomes especially consequential as AI accelerates code generation. If AI generates the implementation --- the HOW --- then humans must explicitly govern the WHAT. The artifacts authored in this chapter are that explicit governance. They are the laws. Code --- whether written by humans or generated by machines --- must obey them. Under this model, compliance is not bolted on after implementation. It is embedded at authoring time, enforced at validation time, and provable at any time thereafter.

## 3.7 --- Solved Problems

### Problem 3.1 --- Adding a New Requirement

**Scenario:** The product manager requires that registration also captures the user's phone number.

**Application-Centric Approach:** A developer adds a column to the database, updates the controller, the service, and the repository. Frontend and backend must coordinate. The specification --- if one exists --- is updated manually, if at all.

**PGS Approach:**

1.  Author `IN_USER_REGISTERED_V1` --- add `phone_number` to the input schema
2.  Author `WF_REGISTER_USER_UNVERIFIED_V1` --- bind to the new intent version
3.  Author `CC_REGISTER_USER_KYC_V1` --- update inputs to accept the new field
4.  Submit all three for validation. The system ensures V1 artifacts reference each other correctly
5.  V0 remains immutable and active for existing clients. Both versions coexist

**Eliminated pathology:** Version drift. The old behavior is preserved structurally, not abandoned implicitly. No client breaks because V0 is unchanged.

### Problem 3.2 --- Preventing Shadow Logic

**Scenario:** A developer wants to add a "quick hack" --- send a welcome email directly inside the ID generation step.

**Application-Centric Approach:** The developer adds an email call inside the hash function. Code review might catch it. Might not.

**PGS Approach:**

1.  CC_GENERATE_USER_ID_V0 declares a CT_-only pipeline
2.  The developer attempts to add CS_SEND_EMAIL_V0 to the pipeline
3.  **Validation failure:** CT_ pipelines cannot contain CS_ artifacts. The constitutional boundary between pure computation and world interaction is enforced structurally
4.  **Resolution:** The developer must add a new workflow step (CC_SEND_WELCOME_EMAIL_V0) with its own capability contract. The email logic becomes visible in the graph --- explicit, governed, auditable

**Eliminated pathology:** Semantic drift. The side effect cannot hide inside a pure computation. It must be declared, validated, and visible in the workflow graph.

### Problem 3.3 --- Detecting Vocabulary Drift

**Scenario:** A team creates a new artifact type `XY_SPECIAL_LOGIC_V0` to bypass standard constraints.

**Application-Centric Approach:** There is no mechanism to prevent it. The code compiles. The tests pass. The artifact proliferates.

**PGS Approach:**

1.  **Validation failure:** Prefix `XY_` is not in the constitutional vocabulary registry
2.  The artifact is rejected. It cannot enter the Protocol layer. It cannot be referenced by workflows or capability contracts
3.  **Resolution:** The team must use standard artifact types (CC_, WF_, CT_, CS_) or propose a constitutional amendment to add `XY_` --- a governed process requiring vocabulary registration, schema definition, and execution semantics

**Eliminated pathology:** Vocabulary drift. Ungoverned artifact types cannot proliferate because the vocabulary is constitutionally bounded.

## 3.8 --- Generated Output: The Execution Graph

The artifacts are authored. They are validated. They are ratified. Now the system generates the execution graph --- a DAG derived from the ratified artifacts.

This is the chapter's proof reveal. The graph is not hand-drawn. It is not coded. It is a structural consequence of what was declared.

> **[DIAGRAM 3] --- System-Generated DAG for WF_REGISTER_USER_UNVERIFIED_V0**

    IN_USER_REGISTERED_V0 [intent]
        ├─ ACK ──→ CC_GENERATE_USER_ID_V0 [capability_contract]
        │              ├─ SUCCESS ──→ CC_REGISTER_USER_KYC_V0 [capability_contract]
        │              │                  ├─ SUCCESS ──→ CC_APPEND_USER_EVENT_V0 ──→ EXIT
        │              │                  ├─ ALREADY_EXISTS ──→ CC_APPEND_USER_EVENT_V0 ──→ EXIT
        │              │                  ├─ VIOLATION ──→ EXIT
        │              │                  └─ BACKEND_ERROR ──→ EXIT
        │              └─ VIOLATION ──→ EXIT
        └─ NACK ──→ EXIT

**Node classification.** Each node carries a concern prefix that determines how the engine handles it. The engine does not read the node's content to determine its type --- the prefix is sufficient. IN_ is admitted. CC_ executes a pipeline. EXIT terminates.

**Edge classification.** Every edge is a declared outcome from a result status contract: SUCCESS, VIOLATION, ALREADY_EXISTS, BACKEND_ERROR, ACK, NACK. Every edge in the DAG is declared --- there are no implicit fallthrough paths.

**Failure classification.** The graph makes failure types structurally visible. VIOLATION edges are governance failures. BACKEND_ERROR edges are infrastructure failures. ALREADY_EXISTS is a domain condition. An operator can determine the failure category from the edge traversed --- without logs, without stack traces, without forensic analysis. Chapter 8 develops this into the full Failure Taxonomy.

**Completeness.** The graph is total: every possible outcome of every node has a declared edge. An incomplete graph --- a node with an undeclared outcome --- fails validation and cannot be ratified. Graph completeness is a structural guarantee, not a testing outcome.

**What the graph proves:** The behavioral surface of user registration is entirely visible from artifacts. An architect can audit the graph without reading code. The execution engine cannot add, remove, or reinterpret edges in the graph. It traverses the law. It does not extend it.

You authored the artifacts. The system generated the graph.

## 3.9 --- Boundary and Forward Pointer

This chapter proved that governance artifacts can be authored, validated, and ratified through a structural lifecycle --- and that the system generates a complete execution graph from those artifacts alone.

**What this chapter did not cover:**

- Runtime execution --- how the engine traverses the graph (Chapter 5)
- DAG compilation mechanics --- how artifacts are compiled into executable protocol (Chapter 4)
- Capability transform internals --- how CT_ steps execute (Chapter 6)
- Capability side-effect internals --- how CS_ steps interact with the world (Chapter 7)
- Execution traces --- what the engine records as it runs (Chapter 9)
- No new artifact types were introduced --- all concern prefixes (IN_, WF_, CC_, CT_, CS_, EV_) were defined in Chapter 2

**What comes next:** The artifacts are ratified. The graph is generated. But between ratification and execution, there is a compilation step. The governance YAML the reader authored in this chapter is not what the execution engine loads. A builder pipeline transforms governance artifacts into compiled protocol JSON --- normalized, machine-readable, and deterministically reproducible. Chapter 4 shows how that compilation works, what the FQDN tree governs about build order and federation, and what happens when artifacts pass governance validation but fail compilation constraints.

We are moving from the Tooling and Governance layers to the boundary between Governance and Execution.

## 3.10 --- Review Questions

1.  **True or False:** An Intent (IN_) contains the logic for how to fulfill a registration request.

- *False. An Intent declares the interface --- inputs, outcomes, and workflow binding. The Workflow (WF_) declares the orchestration. The Capability Contracts (CC_) declare the step-level behavior.*

2.  **Which artifact type is permitted to perform a database write?**

- *Only a Capability Side Effect (CS_). CT_ artifacts are constitutionally prohibited from performing I/O.*

3.  **If a workflow node has 3 possible outcomes but only 2 are mapped in the** `next` **block, what happens?**

- *The artifact fails validation (Completeness Check) and cannot be ratified. The graph must be total --- every outcome must have a declared edge.*

4.  **A developer modifies a ratified V0 workflow to add a new step. What is wrong with this approach?**

- *Ratified artifacts are immutable. The developer must author a new version (V1), which undergoes its own validation and ratification. V0 remains unchanged and addressable.*

5.  **Explain why vocabulary enforcement during validation (not execution) matters.**

- *If vocabulary is checked at runtime, invalid artifacts can enter the Protocol layer and cause failures during execution --- when the cost is highest. By enforcing vocabulary at validation time, the system guarantees that the execution engine never encounters an unrecognized prefix. Invalid artifacts are rejected before they can cause runtime harm.*

6.  **In Example 3.4, why does the pipeline order matter (CT_ before CS_)?**

- *The CT_ step generates the KYC key that the CS_ step uses as a registry key. The CS_ step's input (*`$.results.CT_PURE_GENERATE_ID_V0.kyc_key`*) references the CT_ step's output. The pipeline is a composition chain --- data flows through declared expressions in declared order.*

7.  **What is the structural difference between ALREADY_EXISTS and VIOLATION in the workflow graph?**

- *ALREADY_EXISTS is a domain condition --- the user's credentials are already registered. The workflow treats it as continuable (it proceeds to the event step). VIOLATION is a governance failure --- invalid inputs or a broken contract. The workflow terminates. Both are declared outcomes, but they carry different structural meaning and follow different edges.*
