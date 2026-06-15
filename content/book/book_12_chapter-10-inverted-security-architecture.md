---
title: Chapter 10 — Inverted Security Architecture
date: '2026-04-02'
draft: false
weight: 12
slug: chapter-10-inverted-security-architecture
---

Chapters 5 through 9 proved that PGS execution is deterministic, that failures are classified, and that traces provide tamper-evident records of everything the system did. But one claim remains unproven: that the system cannot do what it was not told to do.

This chapter completes the security axis. It answers: **How does a protocol-governed system achieve security not by defending against unauthorized behavior, but by making unauthorized behavior structurally inexpressible?**

Conventional security is additive --- firewalls, access control lists, runtime guards, penetration testing. Each defense is a layer added on top of a system that is, by default, permissive. PGS inverts this model. The system is, by default, inert. It has no behavior until governance artifacts declare behavior. The attack surface is not the code --- it is the vocabulary. A finite set of governed prefixes (`IN_`, `CC_`, `CT_`, `CS_`, `WF_`, `EV_`) defines the total executable surface. No ambient authority exists --- the machine, the network zone, the operating system user grant no capabilities. The chapter walks through the vocabulary-bounded attack surface, shows why dynamic symbol admission is structurally impossible, and demonstrates that security is a consequence of governance, not a discipline applied after implementation.

## 10.1 --- The Engineering Objective

Chapter 8 proved that failures are classified and deterministic. Chapter 9 proved that execution records are tamper-evident and that executed capabilities cannot be concealed. This chapter completes the security axis by proving the remaining claim: undeclared capabilities cannot be invoked at all.

The distinction is precise. Chapter 9 proved that the trace records what happened --- faithfully and immutably. This chapter proves that what happens is bounded --- structurally, constitutionally, and before any runtime begins.

**The Task:** Demonstrate that the governance vocabulary defines a finite, enumerable executable surface, and that no behavior outside this surface can occur --- not because defensive guards prevent it, but because the architecture cannot express it.

**The Constraint:** PGS does not permit ambient authority, implicit capability invocation, dynamic symbol admission, or runtime-only access checks. Authority derives from ratified governance artifacts. Execution context --- the machine, the network zone, the deployment environment, the operating system user --- grants no capabilities.

In the application-centric approach, security is a defensive discipline. The system is built first, then secured. Firewalls restrict network access. Role-based access control restricts user operations. Input validation prevents injection attacks. Code reviews catch vulnerabilities. Penetration tests probe for gaps. Each layer is a defense against the assumption that the layer below it might fail. The result is defense in depth --- concentric rings of protection around an unbounded execution surface. The attack surface grows with every line of code, every library, every framework, every runtime. Any component that can affect execution is a potential attack vector. Security teams spend their careers defending a surface they cannot fully enumerate.

In PGS, security is inverted. The system does not defend against undeclared behavior. It eliminates the structural possibility of undeclared behavior. The vocabulary is finite --- eight prefixes governing eight concerns. The artifacts are ratified --- immutable once they pass constitutional validation. The execution engine interprets what governance declares --- it cannot invent, discover, or infer additional behavior. The attack surface is not the sum of all code paths. It is the sum of all declared mutation primitives (CS_), authority artifacts (AC_), and binding declarations (RB_). This surface is finite, enumerable, and inspectable. Security is not a layer applied after construction. It is a consequence of the construction itself.

## 10.2 --- The Vocabulary as Security Perimeter

**Definition:** A vocabulary constraint is the constitutionally enumerated, finite set of artifact prefixes, structural keywords, and operation verbs that bound all expressible behavior in the system.

**Key Properties:**

1.  **Prefix-bound registration.** Every artifact in the system carries a recognized prefix: WF_, IN_, CC_, CT_, CS_, AC_, EV_, RB_. An artifact without a recognized prefix cannot be loaded, cannot be compiled, and cannot execute. The prefix is not a naming convention --- it is a structural gate.
2.  **No dynamic symbol admission.** The vocabulary is fixed at constitutional ratification. Expanding it requires a constitutional amendment --- a governance process, not a configuration change. No runtime operation, no deployment script, no environment variable can introduce a new prefix or a new structural keyword.
3.  **Enforcement at authoring and compilation.** Vocabulary violations are caught by the builder before any artifact reaches the execution engine. An unknown prefix, an unrecognized operation verb, a forbidden keyword --- each produces a build-time rejection. The runtime never sees the violation because the artifact never reaches the runtime.

### Example 10.1 --- The Vocabulary Boundary

PGS defines three constitutional vocabulary files that together bound all expressible behavior:

    VOCAB_PROTOCOL_KINDS_V0
      artifact_kinds:   workflow, intent, capability_contract,
                        capability_transform, capability_side_effect,
                        event, actor, runtime_binding, governance
      node_types:       AC, CC, CS, CT, EV, EXIT, IN, WF, RB, ...

    VOCAB_EXECUTION_STATES_V0
      result_status:    SUCCESS, VIOLATION, BACKEND_ERROR, NOT_FOUND,
                        ALREADY_EXISTS, ACK, NACK, TIMEOUT, ...
      exit_reasons:     COMPLETED, FAILED, HALTED, TIMEOUT, ...

    VOCAB_LANGUAGE_CONSTRAINTS_V0
      structural_keys:  bindings, code, next, pipeline, type, ...
      binding_verbs_cs: APPEND, DELETE, EXISTS, READ, READ_ALL,
                        REGISTER, RESOLVE, WRITE, ...
      forbidden:        TERM, TERMINAL, TERMINATE

**Analysis:**

- The vocabulary is finite and enumerable. There are eight artifact prefixes, not an open-ended namespace. There are fourteen CS_ operation verbs, not arbitrary method names. There are seven result statuses in the constitutional core, not application-defined error codes. An architect can read these three files and know the total behavioral surface of the system.
- The `forbidden` list is a hard prohibition. Words like TERMINATE cannot appear in any authoring artifact. This is not a linting rule --- it is a constitutional constraint enforced by the builder. A forbidden word in a governance artifact produces a build-time rejection.
- Casing is constitutional. Node types are UPPER_SNAKE. Artifact kinds are lower_snake. Structural keys are lower_snake. The builder validates casing and rejects mismatches. Casing is not style --- it is a structural classifier that enables deterministic routing.

### Example 10.2 --- Capability Contract as Authority Declaration

Viewed through a security lens, the CC_ artifact is not merely an execution contract --- it is an authority declaration. It declares which CT_ transforms and CS_ side effects may be invoked for a given workflow node *(see Appendix B, Example 10.2)*.

**Analysis:**

- The `pipeline` array is a closed declaration. CS_WALLET_STATE_V0 and CS_WALLET_INDEX_V0 are the only side effects this contract may invoke. A third CS_ step cannot be added at runtime. It cannot be injected through payload manipulation. It cannot be discovered through reflection. The pipeline is ratified --- it is what the governance declares and nothing else.
- The `result_status_contract` bounds the outcome space. This contract may produce SUCCESS, VIOLATION, or BACKEND_ERROR. No other result status can emerge from this pipeline. The workflow that references this contract can reason about a closed set of outcomes --- there are no surprise statuses.
- Version binding is structural. CC_PERSIST_WALLET_V0 is immutable. A behavioral change requires CC_PERSIST_WALLET_V1 --- a new artifact that must pass constitutional validation, be registered in the governance registry, and be referenced explicitly by a workflow. Silent behavioral modification is structurally impossible.

### Example 10.3 --- Rejected Undeclared Capability

A workflow references a capability contract that declares a CT_ transform not present in the registry.

*(The full artifact is provided in Appendix B, Example 10.3.)*

CT_PURE_CUSTOM_CIPHER_V0 does not exist in any governance registry. The builder rejects:

    BUILD ERROR
      Phase:         discover
      Severity:      FATAL
      Artifact:      CC_CUSTOM_ENCRYPT_V0
      Check:         Referential integrity
      Detail:        Pipeline references CT_PURE_CUSTOM_CIPHER_V0,
                     which is not registered in any governance registry.
                     All CT_ artifacts must exist as ratified governance
                     entries before they can be referenced.
      Violated Rule: CONSTITUTION_VOCABULARY_V0.referential_integrity
      Resolution:    Register CT_PURE_CUSTOM_CIPHER_V0 in the appropriate
                     governance registry, or reference an existing CT_ code.

Even if the builder were bypassed and the artifact somehow reached the execution engine, the protocol loader would reject it:

    PROTOCOL LOAD ERROR
      Artifact:      CC_CUSTOM_ENCRYPT_V0
      Check:         CT artifact loading
      Detail:        CT_PURE_CUSTOM_CIPHER_V0 not found in materialized
                     CT artifacts directory.
      Error Code:    CT_ARTIFACT_NOT_FOUND
      Resolution:    Run the builder to materialize all referenced CT_
                     artifacts, or correct the CC_ pipeline reference.

**Analysis:**

- The rejection is layered but not redundant. The builder catches the violation at authoring time. The protocol loader catches it at load time. The capability pipeline would catch it at dispatch time. Each layer enforces the same invariant independently: no undeclared capability may execute. An attacker who bypasses one layer encounters the next.
- The failure is structural, not conditional. The system does not check a permission table or consult an access control list. It attempts to load an artifact that does not exist. Existence is binary --- the artifact is registered or it is not. There is no "almost registered" or "temporarily authorized."
- The engine remains semantic-agnostic. It does not know what CT_PURE_CUSTOM_CIPHER_V0 would do if it existed. It does not evaluate whether encryption is a permitted operation. It simply cannot load what governance has not declared. The security boundary is the vocabulary --- not a policy engine that reasons about operations.

## 10.3 --- The Closed Runtime Registry

The vocabulary bounds what artifacts may be declared. The closed runtime registry bounds what implementations may execute.

The execution engine maintains a fixed set of runtime classes:

    RUNTIME_CLASSES:
      MutableJsonRuntime      (read, write, delete, exists, list_keys)
      RegistryRuntime         (register, resolve, exists, deregister)
      AppendOnlyJsonlRuntime  (append, read_all)

This set is defined in the engine codebase --- not in configuration, not in artifacts, not in environment variables. An RB_ artifact that references a runtime class not in this set fails at binding resolution --- before any workflow executes.

### Example 10.4 --- Runtime Binding to Unknown Implementation

An RB_ artifact declares a binding to a runtime class that does not exist *(see Appendix B, Example 10.4)*.

The runtime loader rejects:

    BINDING RESOLUTION ERROR
      Phase:          runtime_loading
      CS Code:        CS_EXTERNAL_API_V0
      Runtime Class:  HttpClientRuntime
      Detail:         HttpClientRuntime is not a registered runtime class.
                      Available: MutableJsonRuntime, RegistryRuntime,
                      AppendOnlyJsonlRuntime
      Resolution:     Use a registered runtime class, or extend the engine
                      codebase to add HttpClientRuntime as a new runtime.

**Analysis:**

- The runtime surface is bounded by codebase modification, not by configuration. Adding a new runtime class requires changing engine source code --- a development and governance activity. It cannot be done through an RB_ artifact, a deployment script, or a payload. This is a deliberate authority boundary: runtime bindings configure which instances are used; only the engine codebase determines which classes are available.
- The set of available operations per runtime is fixed. MutableJsonRuntime supports `read`, `write`, `delete`, `exists`, `list_keys` --- and nothing else. An RB_ artifact cannot add methods to a runtime. A CS_ binding that specifies `op: "EXECUTE_SQL"` on a MutableJsonRuntime fails at dispatch --- there is no `execute_sql` method to call.
- This is the deepest authority boundary in PGS. Vocabulary bounds what may be declared. The builder bounds what may be compiled. The protocol loader bounds what may be loaded. The closed runtime registry bounds what may execute. Each boundary narrows the executable surface. By the time a CS_ operation reaches a runtime, it has passed through four gates --- and the runtime itself exposes only its declared operations.

## 10.4 --- The Protocol Boundary Chain

Execution in PGS flows through a mandatory chain. Every link in the chain is a structural gate that rejects undeclared behavior:

  --------------------------------------------------------------------------------------------------------------------------------------------------------
  Gate                      What It Enforces                                           What Cannot Pass
  ------------------------- ---------------------------------------------------------- -------------------------------------------------------------------
  1. Vocabulary            Prefix recognition, keyword validation, casing             Unknown prefixes, forbidden words, casing violations

  2. Builder               Schema conformance, referential integrity, WF-CC linking   Malformed artifacts, broken references, unhandled result statuses

  3. Protocol Loader       Artifact existence, code-to-filename matching              Artifacts not in registry, code mismatches

  4. Admission Gate        Pre-DAG event preconditions                                Workflows with unmet admission requirements

  5. Capability Pipeline   CC_ contract validation, binding resolution               Undeclared CC_ codes, unresolvable bindings

  6. Runtime Registry      Closed implementation set, operation dispatch              Unknown runtime classes, undeclared operations
  --------------------------------------------------------------------------------------------------------------------------------------------------------

No gate trusts the output of the preceding gate. Each validates independently. This is not defense in depth --- it is structural enforcement at every architectural boundary.

These gates are not redundant protective layers around the same surface. Each gate constrains a different dimension of execution: vocabulary constrains expressibility; the builder constrains artifact validity; the loader constrains materialization; admission constrains traversal; the pipeline constrains authority; the runtime registry constrains implementation. They do not defend the same surface repeatedly --- they progressively narrow it.

### The WF-CC Link Validator

The builder enforces three linking rules between workflow specifications and capability contracts:

**Rule 1 --- CC Exists.** Every CC_ code referenced by a workflow node must exist in the governance registry. A workflow that references CC_PHANTOM_V0 is rejected if no such contract exists.

**Rule 2 --- Result Status Alignment.** Every result_status that the workflow routes on must be declared in the CC_'s `result_status_contract.allowed` array. A workflow edge labeled BACKEND_ERROR on a CC_ that only declares SUCCESS and VIOLATION is a governance error --- the workflow references a status the contract cannot produce.

**Rule 3 --- No Silent Drop.** Every result_status the CC_ declares in its `allowed` array must be handled by the workflow --- either routed to another node or explicitly routed to an exit. A CC_ that declares BACKEND_ERROR as a possible outcome, but whose workflow has no edge for that status, is flagged as an unhandled capability outcome. No result may silently vanish.

These three rules ensure that the workflow and its contracts form a closed system. The workflow cannot reference undeclared contracts. It cannot route on undeclared statuses. It cannot ignore declared outcomes. The governance surface is complete --- every declared possibility has a declared response.

## 10.5 --- Validation and Failure Surface

### Security Validation Checks

  -------------------------------------------------------------------------------------------------------------
  Step          Check                            Failure Condition
  ------------- -------------------------------- --------------------------------------------------------------
  1             Vocabulary admission             Unknown prefix, forbidden keyword, casing violation

  2             Contract binding                 CT_ or CS_ referenced in CC_ not registered in governance

  3             Version integrity                Artifact references unratified or non-existent version

  4             Ingress enforcement              Execution attempted without WF_ binding

  5             Result status completeness       CC_ outcome not handled in workflow edges

  6             Runtime class validation         RB_ references implementation not in closed registry

  7             Constitutional code separation   Engine source code contains hardcoded contract literals
  -------------------------------------------------------------------------------------------------------------

### Broken Example 10.5 --- Ambient Authority Attempt

A developer attempts to invoke a CS_ runtime directly from application code, bypassing the workflow and CC_ pipeline:

    # Developer writes this in a utility script:
    from reusable.capability_side_effects.persistent.mutable_json import (
        MutableJsonRuntime
    )

    runtime = MutableJsonRuntime(storage_path="/data/wallet_state.json")
    runtime.write(key="WALLET_001", value={"balance": 999999})

This code compiles. Python does not prevent it. The import succeeds. The write method exists. The file is modified.

But:

1.  **No workflow governed this execution.** There is no WF_ artifact, no IN_ intent, no CC_ contract. The mutation is ungoverned.
2.  **No trace was emitted.** The trace emitter is part of the workflow executor's execution path. A direct runtime invocation bypasses the executor entirely. There is no `execution_start`, no `side_effect_end`, no `workflow_complete`. The mutation is invisible.
3.  **No admission check occurred.** The admission gate validates preconditions before DAG traversal begins. A direct invocation skips admission entirely.
4.  **No result routing occurred.** The CC_ pipeline routes on result_status. A direct invocation returns a Python dict --- no governance classification, no exit reason mapping.

The constitutional validator detects this class of violation at the engine level. The rule EngineNoContractLiterals scans runtime engine source code for hardcoded CC_ references --- ensuring that the engine treats contracts opaquely. But the deeper defense is architectural: the only execution path that produces governed, traced, auditable results flows through the workflow executor. Everything else is ungoverned --- it does not correspond to any ratified artifact chain, and therefore falls outside the system's defined authority model.

**Correction Required:** Declare the mutation in a CC_ artifact, bind it through a WF_ specification, and execute through the workflow engine. There is no authorized shortcut.

**This section proves:** Security violations are eliminated at the authoring and compilation boundary --- not mitigated at runtime. The protocol boundary chain enforces six independent gates. An undeclared capability must bypass all six to execute. Even if it does (through direct code execution outside the engine), the result is ungoverned, untraced, and structurally illegitimate.

## 10.6 --- Structural Insight (Doctrine Moment)

The reader has now seen the vocabulary boundary (Example 10.1), the capability contract as authority declaration (Example 10.2), the structural rejection of undeclared capabilities (Example 10.3), the closed runtime registry (Example 10.4), the protocol boundary chain, and the failure of ambient authority attempts (Example 10.5). At no point did security depend on a firewall, a role check, an access control list, or a runtime guard. At every point, security was a structural consequence of the architecture --- the vocabulary, the builder, the loader, the registry, the pipeline.

This is Chapter 2's **Property 6 --- No Ambient Authority** rendered as an architectural enforcement chain.

**Invariant I-S2 --- No Ambient Authority:** Authority must be derivable from explicit governance artifacts and workflow declarations. Execution context does not grant capabilities. An operation has exactly the authority declared in its artifacts --- no more.

In conventional systems, ambient authority is pervasive. Running as root grants root permissions. Running in a network zone grants network access. Running with credentials grants credentialed operations. Environment variables grant configuration authority. A function call inherits the caller's permissions. An object inherits the permissions of the process that instantiated it. Authority is implicit, contextual, and cumulative.

In PGS, authority is explicit, declared, and bounded:

1.  **Actor declaration.** AC_ artifacts declare actors and their scope.
2.  **Intent authorization.** IN_ artifacts declare what may be requested.
3.  **Workflow authorization.** WF_ artifacts declare what operations may occur and in what order.
4.  **Capability declaration.** CC_ artifacts declare which transforms and side effects may execute.

At any point, the authority an operation possesses is derivable from artifact inspection. No runtime context --- no environment variable, no network zone, no operating system user, no deployment configuration --- grants additional authority. The confused deputy problem, which requires ambient authority to exploit, is structurally eliminated. The deputy has nothing implicit to be confused about.

**What the engine cannot do:**

- **Invoke undeclared capabilities.** The protocol loader rejects unregistered artifacts. The capability pipeline rejects unknown CC_ codes. The runtime registry rejects unknown implementation classes. Three independent mechanisms enforce the same invariant.
- **Accept dynamic runtime permissions.** There is no API to grant a workflow additional capabilities at runtime. The pipeline reads the CC_ artifact's declared pipeline. It does not accept runtime extensions.
- **Expand vocabulary during execution.** The vocabulary is loaded at bootstrap. The builder validates against it at compile time. The execution engine does not modify, extend, or query the vocabulary during execution. Vocabulary expansion requires a constitutional amendment --- a governance process with deliberate friction.

**The trust inversion:** In conventional systems, trust is distributed across developers, reviewers, runtime guards, and operational monitoring. In PGS, trust is concentrated in governance artifacts. The execution engine is a low-trust utility --- it faithfully interprets what governance declares. Compromise of the execution engine can disrupt availability and corrupt data. It cannot grant new behaviors, authorize new operations, or alter protocol meaning. The attacker can break the system. The attacker cannot cause the engine to execute behavior not representable in the loaded governance vocabulary. Governance artifacts are immutable, version-bound, and validated at load time; modification requires re-build and re-load under constitutional validation, not runtime mutation.

> **[DIAGRAM 7] --- The Protocol Boundary Chain**

      Governance Artifacts (Trust Root)
          |
          v
      GATE 1: Vocabulary
        Prefix recognition, keyword validation
          |
          v
      GATE 2: Builder
        Schema, referential integrity, WF-CC linking
          |
          v
      GATE 3: Protocol Loader
        Artifact existence, code matching
          |
          v
      GATE 4: Admission Gate
        Pre-DAG precondition enforcement
          |
          v
      GATE 5: Capability Pipeline
        CC_ contract validation, binding resolution
          |
          v
      GATE 6: Runtime Registry
        Closed implementation set, operation dispatch
          |
          v
      Execution (Low-Trust Utility)

> Each gate validates independently. No gate trusts the output of the preceding gate. Undeclared behavior must bypass all six gates to execute --- and even then produces no trace, no governance classification, and no audit record. The structural impossibility: no behavior outside the declared vocabulary can produce a governed, traced, auditable execution.

## 10.7 --- Solved Problems

### Problem 10.1 --- "Privilege Escalation via Hidden Code Path"

**Scenario:** A junior developer discovers that a service class has a method `resetAllBalances()` that is not exposed through any public API. The method was written during testing and never removed. The developer realizes that any code in the same process can call this method --- no authorization check protects it. The method runs with the service's database credentials. It can zero every account balance in the system.

**Application-Centric Approach:** The method exists in the codebase. It compiles. It is callable from any code with access to the class instance. The application's security depends on no one calling it --- but the method's existence is an ambient authority. Any new feature that imports the class gains the ability to call `resetAllBalances()`. Code review might catch intentional invocations, but an accidental invocation (auto-complete in an IDE, copy-paste error) could trigger it. The method is a loaded gun in the codebase, accessible to anyone who opens the drawer.

**PGS Approach:**

1.  There is no `resetAllBalances()` method. There are CS_ side effects with declared operations. CS_WALLET_STATE_V0 supports `WRITE`, `READ`, `DELETE`, `EXISTS`, `LIST_KEYS`. There is no `RESET_ALL` operation --- it is not in the vocabulary.
2.  Even if a developer wrote a CT_ atom that computed zero balances, it could not persist the result without a CS_ step declared in a CC_ pipeline, bound through a WF_ workflow, and admitted through an IN_ intent.
3.  The capability chain is: IN_ declares what may be requested. WF_ declares what operations may execute. CC_ declares which CS_ side effects may fire. Each is a governance artifact. Adding "reset all balances" requires authoring artifacts, passing constitutional validation, and being ratified. The governance process makes the authorization visible and deliberate --- not hidden in a utility method.

**Eliminated pathology:** Implicit privilege escalation. In application-centric systems, any callable code path is a potential privilege. In PGS, only declared and ratified artifact chains constitute authorized behavior. Undeclared code paths have no governance backing, produce no traces, and carry no structural authority.

### Problem 10.2 --- "Security Drift Over Deployment Cycles"

**Scenario:** A financial services application undergoes quarterly security audits. Each audit certifies the application as compliant. Between audits, the team deploys 47 patches. Some patches modify input validation. Some add new API endpoints. Some change database queries. The next audit discovers that three patches introduced behaviors not covered by the original security assessment. The application has been operating with undeclared capabilities for four months.

**Application-Centric Approach:** Each patch is a code change. Code changes may alter behavior. Altered behavior may introduce security-relevant capabilities. But the security audit certified code --- not behavior. The 47 patches each modified code without triggering a security review because the change management process classifies patches as "minor." Security drift accumulates silently between audits. The audit cycle is too slow to catch per-patch behavioral drift.

**PGS Approach:**

1.  Behavioral changes require new artifact versions. Adding an API endpoint requires a new IN_ artifact. Changing database queries requires modifying a CC_ pipeline (new CS_ step or different CS_ operation). Each change produces a new versioned artifact --- visible, inspectable, and auditable.
2.  The builder validates every artifact against the constitution on every build. A patch that introduces an undeclared CS_ operation, an unrecognized result_status, or a broken WF-CC link is rejected at build time. The governance boundary does not wait for the quarterly audit.
3.  Traces bind artifact versions. To answer "what changed between audit Q1 and audit Q2?" --- compare the artifact registries. The version diff is the behavioral diff. Traces from each period reference the specific artifact versions that governed execution. The audit compares artifacts, not code.
4.  Security assessment can target the delta: which new artifacts were introduced? Which existing artifacts changed versions? What new CS_ operations appeared? The assessment surface is the governance change set --- finite and enumerable --- not the code diff of 47 patches.

**Eliminated pathology:** Silent security erosion. Behavioral changes are artifact version changes. Artifact version changes are visible at the governance layer. The builder enforces constitutional conformance on every build --- not on an audit schedule. Security posture is defined at artifact ratification, not certified retroactively.

### Problem 10.3 --- "Expanding Attack Surface via Plugin"

**Scenario:** A platform supports plugins. A plugin author writes a plugin that registers a new "analytics" capability that reads user data, computes metrics, and posts results to an external API. The platform's plugin system loads the plugin at runtime, registers its capabilities in a discovery registry, and makes them available to workflows. The security team did not review the plugin. The external API endpoint is controlled by the plugin author.

**Application-Centric Approach:** The plugin system is designed for extensibility. It discovers plugins by scanning a directory, loads their code, and registers their capabilities dynamically. Each plugin expands the executable surface. The platform's security perimeter now includes the plugin author's code --- and the plugin author's external API. The attack surface has expanded at runtime through a mechanism designed for convenience.

**PGS Approach:**

1.  The vocabulary is fixed at constitutional ratification. There is no plugin discovery mechanism because there is no dynamic symbol admission. A new CS_ type requires a new runtime class in the engine codebase. A new CT_ requires a governance artifact registered through the builder.
2.  The protocol loader does not scan directories for unknown artifacts. It loads artifacts by explicit code reference from governance registries. Dropping a file into a directory does not register it. The loader's constitutional rule is: "No directory scanning. No discovery. No inference. Canonical filenames only. Missing or mismatched artifact equals hard failure."
3.  The closed runtime registry contains a fixed set of implementation classes. Adding HttpClientRuntime (to post to an external API) requires modifying engine source code --- a development decision, not a configuration action. The RB_ artifact system cannot introduce new runtime classes.
4.  The external API call is structurally impossible without a CS_ runtime that supports HTTP operations. No such runtime exists in the closed registry. No amount of artifact authoring can create one. The plugin's desired behavior is outside the vocabulary.

**Eliminated pathology:** Unbounded execution expansion. In application-centric systems, extensibility mechanisms (plugins, hooks, middleware, interceptors) expand the executable surface at runtime. In PGS, the executable surface is bounded by vocabulary, enforced by the builder, and closed at the runtime registry. Expansion requires governance action --- not deployment configuration.

### Problem 10.4 --- "Perimeter Collapse in Distributed Systems"

**Scenario:** A microservices architecture relies on network segmentation for security. The payment service runs in a restricted network zone. The user service runs in a public zone. The boundary is enforced by firewall rules. A new feature requires the user service to call the payment service. The team adds a firewall rule allowing the connection. Six months later, the user service is compromised. The attacker uses the firewall opening to reach the payment service directly --- bypassing the API gateway, the authentication middleware, and the rate limiter.

**Application-Centric Approach:** Security was infrastructure-dependent. The firewall rule was the security boundary. When the rule was relaxed for a legitimate feature, the security boundary weakened. The attacker did not need to compromise the payment service's code --- only its network accessibility. The perimeter collapsed because the boundary was defined by network topology, not by behavioral authority.

**PGS Approach:**

1.  The protocol boundary is structural, not topological. A workflow on the user service can only invoke capabilities declared in its WF_ specification, bound through its CC_ contracts, and executed through its declared CS_ side effects. The workflow does not "call the payment service" --- it executes a governed pipeline that may include CS_ steps bound to payment-related storage.
2.  Network access does not grant capability. Even if an attacker gains network access to a PGS execution engine, the engine only executes workflows declared in its loaded governance artifacts. The attacker cannot craft a request that invokes undeclared capabilities because the protocol loader has not loaded them.
3.  The execution engine does not expose arbitrary endpoints. It exposes a workflow execution interface: given a WF_ code and a payload, traverse the compiled DAG. The DAG is fixed at load time. The nodes are fixed. The edges are fixed. The capabilities are fixed. Network access to the engine grants the ability to invoke declared workflows --- not arbitrary operations.
4.  Compromise of the execution engine is bounded. The attacker can disrupt availability (prevent workflow execution). The attacker can observe data (read payloads and trace events). The attacker cannot define new behaviors because behavioral authority resides in governance artifacts --- which the engine interprets but does not author.

**Eliminated pathology:** Security dependent on infrastructure perimeter. Network segmentation is valuable for availability and data protection. But behavioral security in PGS does not depend on it. The protocol boundary chain enforces six structural gates between a request and a mutation. Each gate is independent of network topology. The system's behavioral authority is the same whether it runs behind a firewall, on a public endpoint, or on an attacker-controlled machine.

## 10.8 --- Generated Output: Vocabulary-Bounded Attack Surface Map

This section demonstrates the system-generated output that makes the attack surface visible and enumerable.

### Attack Surface Formula

The attack surface of a PGS module is structurally quantifiable:

    |Attack Surface| = |CS_ mutation primitives| + |AC_ authority declarations|
                       + |RB_ binding declarations|

No other vector is structurally admissible. The formula is not an approximation --- it is a structural enumeration derived from governance artifacts.

### Attack Surface Enumeration: Blockchain Module

Given the governance artifacts for the blockchain module, the system produces an attack surface map --- the complete set of behaviors the module can exhibit:

    VOCABULARY-BOUNDED ATTACK SURFACE MAP
    ============================================================
    Module: blockchain

    REGISTERED WORKFLOWS (3):
      WF_CREATE_WALLET_V0
      WF_REGISTER_ACTOR_UNVERIFIED_V0
      WF_VERIFY_ACTOR_V0

    REGISTERED INTENTS (3):
      IN_CREATE_WALLET_V0
      IN_REGISTER_ACTOR_V0
      IN_VERIFY_ACTOR_V0

    CAPABILITY CONTRACTS (6):
      CC_GENERATE_WALLET_ID_V0        pipeline: [CT x1]
      CC_DERIVE_WALLET_ADDRESS_V0     pipeline: [CT x2]
      CC_PERSIST_WALLET_V0            pipeline: [CS x2]
      CC_GENERATE_ACTOR_ID_V0         pipeline: [CT x1]
      CC_REGISTER_ACTOR_KYC_V0        pipeline: [CT x1, CS x2]
      CC_VERIFY_ACTOR_V0              pipeline: [CT x1, CS x2]

    MUTATION SURFACE (CS_ operations):
      CS_WALLET_STATE_V0       WRITE      (MutableJsonRuntime)
      CS_WALLET_INDEX_V0       REGISTER   (RegistryRuntime)
      CS_ACTOR_STATE_V0        WRITE      (MutableJsonRuntime)
      CS_ACTOR_ALIAS_INDEX_V0  REGISTER   (RegistryRuntime)
      CS_ACTOR_EVENT_LOG_V0    APPEND     (AppendOnlyJsonlRuntime)
      CS_ACTOR_KYC_STATE_V0    WRITE      (MutableJsonRuntime)

    TRANSFORM SURFACE (CT_ invocations):
      CT_PURE_GENERATE_ID_V0
      CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
      CT_PURE_PUBLIC_KEY_TO_ADDRESS_V0
      CT_PURE_SIGN_MESSAGE_V0

    RUNTIME CLASSES IN USE (3):
      MutableJsonRuntime         (ops: write, read, delete, exists)
      RegistryRuntime            (ops: register, resolve, exists)
      AppendOnlyJsonlRuntime     (ops: append, read_all)

    ATTACK SURFACE METRICS:
      Mutation primitives (CS_ ops):    6
      Authority artifacts (AC_ refs):   2
      Binding declarations (RB_ refs):  1
      Total attack surface:             9 enumerable points

    STRUCTURALLY IMPOSSIBLE (without new runtime class + governance artifact):
      - HTTP outbound calls        (no HttpClientRuntime)
      - SQL execution              (no SqlRuntime)
      - File system traversal      (no FsTraversalRuntime)
      - Dynamic code execution     (no EvalRuntime)
      - Message queue publish      (no MqRuntime)
    ============================================================

### What the Output Proves

**1. The attack surface is finite and enumerable.** Nine points --- six CS_ operations, two AC_ references, one RB_ declaration. This is the total set of operations that can change state or declare authority in this module. A security assessment can evaluate every point individually.

**2. The mutation surface is explicit.** Six CS_ operations across three runtime types. Each operation is named, typed, and bound to a specific runtime class. There are no hidden write paths, no implicit state mutations, no side effects buried in utility functions.

**3. Structurally impossible operations are declarable.** The map does not merely list what the module can do --- it lists what the module cannot do. No HTTP calls, no SQL execution, no filesystem traversal, no dynamic code execution, no message queue publishing. These are not capabilities that are disabled by configuration. They are capabilities that do not exist in the vocabulary or the runtime registry. They are structurally absent.

**4. WHAT/HOW separation is manifest.** The author declared WF_ workflows, IN_ intents, CC_ contracts, and the CT_ and CS_ governance artifacts. The system generated an attack surface map that enumerates every behavioral possibility and every structural impossibility. The author defined the vocabulary. The system enforces the boundary.

**Structural impossibility:** The engine cannot execute behavior not representable in the registered vocabulary and not bound through the closed runtime registry. The attack surface map is not an approximation or a best-effort scan. It is a structural enumeration derived from governance artifacts. Adding a new mutation pathway requires authoring new governance artifacts, passing constitutional validation, modifying the engine codebase (if a new runtime class is needed), and re-building. Each step is visible, auditable, and governed.

## 10.9 --- Boundary and Forward Pointer

This chapter proved that security in PGS is a structural property --- not a defensive overlay. The vocabulary bounds expressible behavior. The builder enforces constitutional conformance. The protocol loader rejects unregistered artifacts. The closed runtime registry bounds implementation execution. The protocol boundary chain enforces six independent gates between a request and a mutation. Ambient authority is structurally eliminated. The attack surface is finite, enumerable, and inspectable.

Together with Chapters 8 and 9, this completes the Failure and Security mode:

- **Chapter 8:** Governed failure --- every failure is classified, deterministic, and reconstructable
- **Chapter 9:** Governed observability --- execution records are tamper-evident and machine-verifiable
- **Chapter 10:** Governed authority --- the vocabulary defines the total executable surface

Chapter 9 proved that executed behavior cannot be concealed. Chapter 10 proved that undeclared behavior cannot be expressed. Together, these form a duality: the system can only do what governance declares, and everything it does is structurally recorded.

**What this chapter did not cover:**

- Specific cryptographic primitives and encryption schemes
- Network transport security (TLS, mTLS, certificate management)
- Penetration testing methodologies
- Infrastructure hardening (OS, container, cloud configuration)
- Authentication mechanisms (identity verification is orthogonal to behavioral governance)
- Insider threats with governance authority (governance capture is a process risk, not an architectural gap)
- Economic analysis of security tradeoffs

**What comes next:** Chapter 11 --- Federation and cross-domain boundary resolution. This chapter proved that a single module's attack surface is bounded by its vocabulary. Chapter 11 addresses what happens when multiple modules --- each with their own governance artifacts --- compose into a federated system. How do vocabulary boundaries interact across domain boundaries? How are cross-module references validated? How does the attack surface scale under composition?

**Layer movement:** Security axis completed. Moving to federation and scaling.

## 10.10 --- Review Questions

1.  **True or False: Runtime role checks are sufficient to eliminate ambient authority in PGS.**

- *False. Runtime role checks restrict which users may perform operations, but they do not restrict which operations exist. Ambient authority is the problem of capabilities inherited from execution context --- not user identity. PGS eliminates ambient authority structurally: capabilities exist only as declared governance artifacts. No execution context grants additional capabilities. Role checks may complement this model but cannot substitute for it.*

2.  **What defines the executable attack surface in PGS?**

- *The vocabulary --- the constitutionally enumerated set of artifact prefixes, structural keywords, and operation verbs. All behavior must be expressible within this vocabulary. The attack surface equals the sum of mutation primitives (CS_ operations), authority artifacts (AC_ references), and binding declarations (RB_ artifacts). This surface is finite, enumerable, and inspectable.*

3.  **If a developer adds a CT_ atom to the codebase but does not register it in the governance registry, can it execute?**

- *No. The builder will not compile a CC_ pipeline that references it (referential integrity check). The protocol loader will not load it (artifact existence check). The capability pipeline will not dispatch to it (CT artifact not found). Three independent gates enforce the same invariant. The code exists on disk, but it has no governance backing --- it is structurally inert.*

4.  **Why is the closed runtime registry a security boundary rather than a design limitation?**

- *Because it bounds the implementation surface. The vocabulary bounds what may be declared. The builder bounds what may be compiled. The closed runtime registry bounds what may execute. Adding a new runtime class requires modifying engine source code --- a deliberate governance decision, not a configuration change. This means: no RB_ artifact, no deployment script, and no payload can introduce new execution capabilities. The set of possible operations is fixed until the engine codebase is deliberately extended.*

5.  **What is the structural difference between PGS security and defense-in-depth?**

- *Defense-in-depth places concentric defensive layers around an unbounded execution surface. Each layer defends against the failure of the layer below. PGS does not defend against undeclared behavior --- it eliminates the structural possibility of undeclared behavior. The vocabulary is finite. The artifacts are ratified. The runtime registry is closed. There is no unbounded surface to defend. The six gates of the protocol boundary chain are not redundant defenses --- they are independent structural enforcement points at different architectural boundaries.*

6.  **Can vocabulary expand during runtime execution?**

- *No. The vocabulary is loaded at bootstrap and validated at build time. There is no API, no configuration mechanism, and no runtime operation that can introduce a new prefix, a new structural keyword, or a new operation verb during execution. Vocabulary expansion requires a constitutional amendment --- a governance process that produces new vocabulary artifacts, passes validation, and triggers a rebuild. This deliberate friction is architectural: it ensures that vocabulary changes are visible, reviewed, and ratified.*

7.  **Where does the trust root reside in PGS?**

- *In governance artifacts. The execution engine is a low-trust utility that interprets what governance declares. Compromise of the execution engine can disrupt availability and corrupt data, but it cannot grant new behaviors or authorize new operations. Security guarantees derive from protocol artifacts, not from execution implementations (Invariant I-S6). Protecting the system means protecting the governance artifacts and the governance process that ratifies them --- not defending every execution pathway.*
