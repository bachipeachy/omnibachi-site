---
title: Chapter 11 — Declarative Package Federation
date: '2026-04-09'
draft: false
weight: 13
slug: chapter-11-declarative-package-federation
---

Chapters 5 through 10 treated each domain as a self-contained governance unit --- one vocabulary, one set of artifacts, one execution surface. But real systems are not single domains. The blockchain module references crypto transforms from the reusable package. The AI licensing module uses the same shared side-effect runtimes. The transport layer wraps workflow execution in HTTP semantics. Every production system is a federation.

This chapter answers: **How do independently authored domains discover, reference, and compose each other's artifacts --- and how is that federation itself governed rather than emergent?**

In application-centric systems, system structure is discovered: build tools scan filesystems, resolve imports, and infer module boundaries. The result is implicit coupling --- dependencies that exist because a file happened to be on a path, not because a governance artifact declared the relationship. PGS replaces discovery with declaration. The FQDN tree --- a constitutional artifact loaded before any build phase executes --- declares every package, every registry, every dependency, and every artifact resolution path in the system. A package not declared in the tree does not exist. A dependency not declared cannot be resolved. The chapter shows how cross-domain artifact resolution works, how build ordering is governed rather than computed, and why federation is a governance property rather than a deployment convenience.

## 11.1 --- The Engineering Objective

Chapter 10 proved that a single module's attack surface is bounded by its vocabulary and enforced through the protocol boundary chain. That chapter treated each module as a self-contained governance unit --- one vocabulary, one set of artifacts, one attack surface map. But real systems are not single modules. They are compositions. The blockchain module references crypto transforms authored in the reusable package. The ai_licensing module references side-effect runtimes defined in the same shared substrate. The transport layer wraps workflow execution in HTTP semantics. Every production system is a federation of independently governed packages.

This chapter proves that the federation itself is governed.

**The Task:** Demonstrate that system structure --- the complete topology of packages, registries, dependencies, and artifact resolution paths --- is derivable from ratified governance artifacts alone. No filesystem convention, no runtime scanning, no directory inference, no deployment topology contributes to structural discovery.

**The Constraint:** PGS does not permit implicit filesystem discovery, dynamic registry mutation, or undeclared package admission. A package that exists on disk but is not declared in the governance tree does not exist in the system. A directory that contains artifacts but is not registered as a governance registry is invisible to the builder.

In the application-centric approach, federation is emergent. Packages discover each other through filesystem scanning, classpath discovery, plugin registries, or import resolution. A Python package exists because it has an `__init__.py` file. A Java service exists because it is on the classpath. A microservice exists because a service registry has discovered it. In each case, structural presence is inferred from physical artifacts rather than declared through governance. The result is fragile: rename a directory and the package vanishes. Add a directory and an unintended package appears. Move a service and its registry entry drifts. Federation by inference produces systems whose structural topology is unknowable without executing the discovery mechanism itself.

In PGS, federation is declarative. A single constitutional document --- the FQDN tree --- declares every package, its role, its authority level, its registries, its dependencies, and its build order. The builder reads this document first. It does not scan the filesystem. It does not infer package existence from directory structure. It iterates the declared packages in declared order, discovers artifacts in declared registries, and rejects anything undeclared. The structural topology is readable, auditable, and deterministic --- because it is authored, not inferred.

## 11.2 --- The FQDN Tree as Governance Topology

**Definition:** The FQDN tree (Fully Qualified Domain Name tree) is a constitutional governance artifact that declares the complete package topology of a PGS system --- every participating package, its role, its authority level, its registries, its dependencies, and its position in the build order.

**Key Properties:**

1.  **Constitutional authority.** The FQDN tree is not a configuration file. It is a governance artifact governed by CONSTITUTION_GOVERNANCE_V0. Changes to it constitute governance-visible changes. It is hashed (SHA-256) and the hash is embedded in every build manifest. Any modification --- adding a package, reordering build dependencies, registering a new artifact type --- produces a new hash, a new manifest, and a traceable governance change.
2.  **Exhaustive declaration.** Every package that participates in the build must appear in the FQDN tree. Every registry that contains governance artifacts must be declared within its owning package. Every artifact type that a registry provides must be enumerated. Omission is a build error, not a silent absence.
3.  **Explicit dependency ordering.** Dependencies between packages are declared as an acyclic, forward-only graph. Package `blockchain` (build_order 4) depends on `reusable` (build_order 3) and `governance` (build_order 1). The builder validates that every dependency reference points to a package with a lower build order. Cycles are structurally impossible.

### Example 11.1 --- The FQDN Tree (Excerpt)

The FQDN tree declares packages with three roles --- `core` (protocol infrastructure), `capability_pack` (shared implementations), and `domain_pack` (domain-specific workflows) --- and two authority levels --- `sovereign` (root authority) and `delegated` (authority derived from sovereign):

*(The full artifact is provided in Appendix B, Example 11.1.)*

**Analysis:**

- The topology is explicit. Four packages with declared roles, authority levels, build orders, registry paths, and dependency relationships. An architect can read this artifact and know the complete structural composition of the system --- without executing anything.
- The `blockchain` package has three registries (identity, wallet, transaction) --- each scoped to a subdomain concern. The `ai_licensing` package has a single flat registry. Both patterns are valid because registries are declarative. The FQDN tree does not prescribe internal organization --- it declares what exists and where to find it.
- Dependencies are acyclic and forward-only. `blockchain` (order 4) depends on `reusable` (order 3). `reusable` depends on `governance` (order 1) and `execution` (order 2). No package can depend on a package with equal or higher build order. The builder validates this constraint at load time and rejects cycles before any artifact is discovered.

### Example 11.2 --- The Build Contract

The FQDN tree includes an explicit build contract that governs builder behavior:

*(The full artifact is provided in Appendix B, Example 11.2.)*

**Analysis:**

- The build contract is constitutional --- it governs the builder's behavior, not advisory guidance. A builder that scans a directory to discover an undeclared package violates the FQDN tree's explicit prohibition.
- The `forbidden` list names three operations that are structurally impossible within the build process: implicit discovery, dynamic mutation, and undeclared execution. These are not features that were considered and rejected. They are capabilities that the architecture cannot express.
- The contract's positive requirements are equally structural: load the FQDN tree first, validate dependencies, resolve paths explicitly. The builder's first action is constitutional --- it reads the governance document that defines the system's structure.

## 11.3 --- The Path Registry as Constitutional Source of Truth

The FQDN tree declares what exists. The path registry resolves where it lives. The FQDN tree declares structural intent; the path registry derives concrete filesystem paths from that declaration. The former is governance; the latter is deterministic projection.

**Definition:** The path registry is the constitutional source of truth for all filesystem paths in a PGS system. It derives paths from the FQDN tree and env_facts --- never from filesystem inspection.

The path registry bootstraps in a deterministic sequence:

1.  Find project root (upward walk from a `.project_root` marker file)
2.  Load env_facts from `structure/env_facts/default.json`
3.  Load FQDN tree from `pgs_governance/registry/FB_CONSTITUTION/structures/STRUCTURE_DISCOVERY_V0.md`
4.  Derive all paths from these two governance sources

### Example 11.3 --- Path Resolution for Federated Modules

When the system needs to locate artifacts for the blockchain module, the path registry resolves through the FQDN tree --- not through directory scanning:

    Path Resolution Chain:
      1. FQDN tree declares: blockchain.physical_root = ./blockchain
      2. Path registry derives: blockchain artifacts at
           blockchain/protocol/artifacts/
      3. Module-specific artifact lookup:
           blockchain/protocol/artifacts/workflows/wf_create_wallet_v0.json
           blockchain/protocol/artifacts/capability_contracts/cc_persist_wallet_v0.json

    Runtime Resolution Chain:
      1. env_facts declares: workflow_to_module["WF_CREATE_WALLET_V0"] = "blockchain"
      2. env_facts declares: module_data_roots["blockchain"] = "blockchain/testbed/outputs"
      3. Path registry derives: trace output at
           blockchain/testbed/outputs/<trace_id>/<trace_id>.jsonl

**Analysis:**

- Path resolution is derived, not discovered. The path registry does not walk the filesystem to find blockchain artifacts. It reads the FQDN tree's `physical_root` declaration and constructs the canonical path. If the directory does not exist at the declared location, the system fails loudly --- it does not search elsewhere.
- Runtime module mapping is explicit. The `workflow_to_module` mapping in env_facts declares which module owns each workflow. When WF_CREATE_WALLET_V0 executes, the system does not scan for it --- it looks up the mapping and resolves the module's data root. Adding a new module requires a governance change to env_facts, not a filesystem reorganization.
- Each module is isolated by path. Blockchain traces go to `blockchain/testbed/outputs/`. AI licensing traces go to `ai_licensing/testbed/outputs/`. Module isolation is not enforced by permissions --- it is a structural consequence of the path registry's derivation from the FQDN tree.

## 11.4 --- Cross-Domain Artifact Resolution

Domains in PGS are authored independently. The blockchain team authors wallet workflows. The reusable package provides shared transform atoms. Neither team coordinates with the other during authoring. But at build time, the artifacts must compose --- blockchain CC_ pipelines reference CT_ atoms defined in the reusable package. How does cross-domain resolution work without prior coordination?

The answer is the builder's discovery phase, governed by the FQDN tree's build order.

### Example 11.4 --- Cross-Domain Reference Map

The blockchain module's CC_DERIVE_WALLET_KEYS_V0 references a capability transform that is defined in the blockchain domain's own registry but depends on atoms implemented in the reusable package:

    Domain: blockchain
      CC_DERIVE_WALLET_KEYS_V0
        pipeline:
          - CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
              (declared in blockchain/governance/registry/wallet/
               capability_transforms/)
              (implementation: reusable/capability_transforms/atoms/
               or blockchain/capability_transforms/atoms/)

      CC_PERSIST_WALLET_V0
        pipeline:
          - CS_WALLET_STATE_V0   (op: WRITE, MutableJsonRuntime)
          - CS_WALLET_INDEX_V0   (op: REGISTER, RegistryRuntime)
              (runtime classes: defined in reusable/capability_side_effects/)
              (governance specs: defined in reusable/governance/registry/
               capability_side_effects/)

    Domain: ai_licensing
      CC_CHECK_LICENSE_QUOTA_V0
        pipeline:
          - CT_PURE_CHECK_QUOTA_AVAILABLE_V0
              (declared in reusable/governance/registry/
               capability_transforms/)

**Analysis:**

- Cross-domain references resolve through build order, not explicit import declarations. The reusable package (build_order 3) is built before blockchain (build_order 4). When the builder discovers blockchain artifacts, the reusable package's transforms and side effects are already validated and materialized. The blockchain domain's CC_ pipelines can reference reusable CT_ atoms because the builder has already confirmed they exist.
- There is no import statement, no include directive, no cross-package reference file. The FQDN tree's dependency declaration (`depends_on: [governance, reusable]`) and the build order create the resolution scope: anything built at a lower order is eligible for reference --- provided the referencing package declares the dependency in its `depends_on` list. The builder validates referential integrity across this scope.
- The ai_licensing module (build_order 5) independently references the same reusable atoms. Neither domain coordinates with the other. Both depend on the same shared substrate. The reusable package functions as a governed commons --- a set of validated, versioned, constitutionally compliant capabilities available to all domain packs.

### The Builder's Discovery Phase

The builder processes packages strictly in build_order:

    Build Order Execution:
      Order 1: governance    → Load constitutions, vocabulary, schemas
      Order 2: execution     → No registries (engine code only)
      Order 3: reusable      → Discover and validate shared CT_, CS_ artifacts
                                Materialize to reusable/protocol/artifacts/
      Order 4: blockchain    → Discover domain artifacts in 3 registries
                                Validate cross-references (CT_ exists in
                                reusable or blockchain registry)
                                Materialize to blockchain/protocol/artifacts/
      Order 5: ai_licensing  → Discover domain artifacts in 1 registry
                                Validate cross-references
                                Materialize to ai_licensing/protocol/artifacts/

Each package materializes to its own `protocol/artifacts/` directory. The federation is structural --- each domain owns its artifact output space. At runtime, the protocol loader reads from a specific module's artifact directory. It does not search across modules. The workflow-to-module mapping in env_facts determines which artifact root to load from.

## 11.5 --- Validation and Failure Surface

### Federation Validation Checks

  --------------------------------------------------------------------------------------------------------------------------
  Step          Check                                Failure Condition
  ------------- ------------------------------------ -----------------------------------------------------------------------
  1             Package existence                    Package in `depends_on` not declared in FQDN tree

  2             Dependency acyclicity                Package depends on equal or higher build_order

  3             Registry declaration                 Artifact found outside declared registry path

  4             Code-filename match                  Artifact code does not match canonical filename

  5             Cross-domain referential integrity   CC_ pipeline references CT_ not registered in any declared registry

  6             FQDN tree hash consistency           Build manifest references different FQDN tree hash than current

  7             Duplicate authority                  Two packages declare the same registry path
  --------------------------------------------------------------------------------------------------------------------------

### Broken Example 11.5 --- The Phantom Domain

A workflow in the blockchain module references a capability contract from a domain that does not exist in the FQDN tree:

*(The full artifact is provided in Appendix B, Example 11.5.)*

The domain `quantum_trading` does not appear in the FQDN tree. It has no package declaration, no registries, no build order. The builder rejects:

    BUILD ERROR
      Phase:         discover
      Severity:      FATAL
      Artifact:      WF_FAST_SETTLEMENT_V0
      Check:         Cross-domain reference validation
      Detail:        Workflow references module 'quantum_trading'
                     which is not declared in STRUCTURE_DISCOVERY_V0.
                     Only declared packages participate in the build.
      Violated Rule: STRUCTURE_DISCOVERY_V0.global_rules.package_existence
      Resolution:    Register 'quantum_trading' in the FQDN tree with
                     appropriate role, authority, build_order, and
                     registries — or reference an existing domain.

**Analysis:**

- The rejection is constitutional, not heuristic. The builder does not check whether a `quantum_trading/` directory exists on disk. It checks whether the domain is declared in the FQDN tree. A directory with governance artifacts, materialized protocols, and test payloads --- all sitting on the filesystem --- is structurally invisible if it is not declared. Directory presence does not equal domain existence.
- The error message names the violated rule: `STRUCTURE_DISCOVERY_V0.global_rules.package_existence`. This is not a generic error code. It is a constitutional citation --- traceable to the specific governance clause that the artifact violates.
- The recovery path requires a governance action: register the domain in the FQDN tree. This means declaring a package role, authority level, build order, registries, and dependencies. The registration is a constitutional amendment --- visible, auditable, and deliberate. Domains do not slip into existence through filesystem proximity.

### Broken Example 11.6 --- Dependency Cycle

A developer reorganizes the FQDN tree so that the reusable package depends on blockchain:

*(The full artifact is provided in Appendix B, Example 11.6.)*

The builder rejects at FQDN tree load time:

    FQDN ERROR
      Package:       reusable (build_order: 3)
      Dependency:    blockchain (build_order: 4)
      Detail:        Package 'reusable' (order 3) depends on
                     'blockchain' (order 4). Dependencies must
                     reference packages with strictly lower
                     build_order.
      Violated Rule: STRUCTURE_DISCOVERY_V0.global_rules.acyclic_dependencies

**Analysis:**

- The constraint is mathematical, not policy-based. Build order is a strict partial order. Dependencies must be forward-only --- lower order to higher order. A dependency cycle would imply mutual structural authority --- which contradicts the delegated authority hierarchy. This is not a convention that teams must remember. It is a structural property validated at FQDN tree load time, before any artifact is discovered.
- The error is caught early --- before the builder begins discovery, validation, or materialization. A dependency cycle means the build cannot start. There is no partial build, no "build what you can" heuristic. The structural precondition is unsatisfied. The builder halts.

## 11.6 --- Structural Insight (Doctrine Moment)

The reader has now seen the FQDN tree as governance topology (Example 11.1), the build contract (Example 11.2), federated path resolution (Example 11.3), cross-domain artifact composition (Example 11.4), and structural rejection of phantom domains and dependency cycles (Examples 11.5--11.6). At no point did federation depend on filesystem scanning, runtime service discovery, or deployment configuration. At every point, federation was a structural consequence of governance artifacts --- the FQDN tree, the build contract, the path registry, and the env_facts module mapping.

This is a new invariant:

**Invariant I-F1 --- Declarative Federation:** System structure must be derivable exclusively from ratified governance metadata present at build time. No implicit discovery, filesystem scanning, or runtime reflection may contribute to structural topology.

I-F1 extends the authority model established in Chapter 10. Where I-S2 (No Ambient Authority) proved that no execution context grants capabilities, I-F1 proves that no physical context grants structural existence. A domain does not exist because its directory exists. It exists because governance declares it.

**What the system cannot do:**

- **Admit undeclared packages.** The builder iterates the FQDN tree's declared packages. A directory on the filesystem that contains governance artifacts but is not declared in the FQDN tree is invisible. The builder will never discover it. The runtime will never load it.
- **Import undeclared peers.** Cross-domain references resolve through build order and registry declarations. A domain cannot reference artifacts from a package it does not depend on. The dependency graph is declared and validated --- not inferred from import statements.
- **Derive structure from scanning.** The `forbidden` list in the FQDN tree's machine contract explicitly prohibits `implicit_filesystem_discovery`. This is not a lint rule --- it is a constitutional constraint. The builder's build contract requires loading the FQDN tree first and iterating only declared registries.

**Federation as constitutional alignment:** The word "federation" in conventional systems implies runtime coordination --- service meshes, load balancers, API gateways. In PGS, federation is constitutional alignment. Two domain packs that both declare `depends_on: [governance, reusable]` are federated --- they share a common constitutional substrate, a common vocabulary, and a common set of shared capabilities. They compose at build time, not at runtime. Their structural relationship is declared in the FQDN tree, validated by the builder, and immutable until the governance artifact is amended.

> **[DIAGRAM 8] --- The FQDN Federation Topology**

      GOVERNANCE (Order 1)
      Sovereign authority, constitutions, vocabulary
          |
          v
      EXECUTION (Order 2)        REUSABLE (Order 3)
      Engine, runtime              Shared CT_, CS_ atoms
          |                            |
          +----------------------------+
          |              |             |
          v              v             v
      BLOCKCHAIN     AI_LICENSING     BOOK
      (Order 4)      (Order 5)       (Order 6)
      Identity,      Licensing,       Pedagogical
      Wallet,        Provisioning,    examples
      Transaction    Reclamation
          |              |             |
          v              v             v
      TOOLING (Order 7)       TRANSPORT (Order 8)
      Builder, validator      CLI, HTTP gateway

> Each arrow represents a declared dependency. Dependencies flow strictly downward (lower build_order to higher). No horizontal dependencies between domain packs. Each domain pack depends on the same governance and reusable substrate but not on each other. Federation is determined at build time through shared constitutional foundation; runtime coordination operates within that pre-declared topology.

## 11.7 --- Solved Problems

### Problem 11.1 --- "Filesystem as Authority"

**Scenario:** A platform infers package structure from filesystem layout. A `services/payments/` directory is treated as a payments service. A developer creates `services/test-payments/` for debugging. The framework discovers both directories, registers both as services, and routes traffic to the test service. Production data flows through a debugging stub.

**Application-Centric Approach:** The framework scans the `services/` directory to discover service implementations. Directory presence is service existence. The test directory was never intended to be a service --- but it occupies the correct filesystem location, so the framework treats it as one. The developer's intent is invisible. The filesystem layout is the authority.

**PGS Approach:**

1.  The FQDN tree declares exactly which packages participate in the build. A `test-payments/` directory on the filesystem is not declared --- it does not exist in the system's structural topology.
2.  The builder does not scan `services/` or any other directory. It reads the FQDN tree and iterates declared registries. The test directory is invisible to the builder --- no artifacts are discovered, no protocols are materialized, no workflows can reference it.
3.  Adding a new domain requires a governance amendment to the FQDN tree: declaring a package name, role, authority, build order, registries, and dependencies. The amendment is visible, auditable, and deliberate. A debugging directory cannot accidentally become a production service.

**Eliminated pathology:** Implicit structural authority derived from filesystem layout. In PGS, existence is declared, not inferred.

### Problem 11.2 --- "Implicit Package Discovery"

**Scenario:** A plugin-based architecture scans a directory for JARs at startup. A developer drops a logging utility JAR into the plugin directory. The plugin framework loads it, discovers a class that implements the plugin interface, and registers it. The logging utility begins intercepting HTTP requests --- a capability the original developer never intended to expose.

**Application-Centric Approach:** The plugin system is designed for extensibility. It discovers plugins by scanning, loads their code, and registers their capabilities. Each scanned artifact expands the executable surface. The logging utility's accidental capability registration is a feature of the discovery mechanism --- not a bug.

**PGS Approach:**

1.  There is no plugin directory. There is no scanning mechanism. The FQDN tree declares all registries. Artifact discovery operates within declared registry paths using declared file patterns. Dropping a file into a directory does not register it unless that directory is a declared registry for the artifact's type.
2.  The build contract prohibits `implicit_filesystem_discovery`. This is not a convention --- it is a constitutional constraint. A builder that scans outside declared registries violates the FQDN tree's build contract.
3.  The closed runtime registry (Chapter 10) provides a second gate. Even if an artifact were somehow discovered and materialized, it could only reference runtime classes in the closed registry. New execution capabilities require engine codebase modification --- not file placement.

**Eliminated pathology:** Runtime-expanding executable surface through implicit discovery. In PGS, the executable surface is declared at governance time and closed at build time.

### Problem 11.3 --- "Namespace Collision in Multi-Team Systems"

**Scenario:** Two development teams independently create a `wallet/` module. Team A builds a cryptocurrency wallet. Team B builds a customer loyalty wallet. Both modules are deployed. Namespace collision causes the framework to load one and silently ignore the other. Which one loads depends on classpath ordering --- a deployment detail that changes between environments.

**Application-Centric Approach:** The framework uses a flat namespace. Two packages with the same name collide. The resolution depends on load order --- which is environment-specific and often nondeterministic. The collision is discovered in production when the wrong module handles requests.

**PGS Approach:**

1.  The FQDN tree enforces unique package names with explicit physical_root paths. Package `blockchain` maps to `./blockchain`. If a second team creates a wallet module, it must be declared as a distinct package --- `loyalty` or `customer_wallet` --- with its own physical_root, its own registries, and its own build order position.
2.  Registry paths are per-package. `blockchain/governance/registry/wallet/` and `loyalty/governance/registry/wallet/` are distinct registries in distinct packages. The builder discovers each within its declared scope. There is no flat namespace to collide in.
3.  Materialized artifacts go to separate output directories: `blockchain/protocol/artifacts/` and `loyalty/protocol/artifacts/`. Runtime loads from a specific module's artifact root (determined by workflow-to-module mapping). There is no ambiguity about which module's artifacts are loaded.

**Eliminated pathology:** Namespace collision resolved by deployment order. In PGS, package identity is constitutionally declared, and artifact resolution is deterministic.

### Problem 11.4 --- "Cross-Organization Drift"

**Scenario:** Organization A and Organization B share a governance substrate. Organization A modifies a shared capability transform without notifying Organization B. Organization B's workflows begin producing different results --- but the failure is silent because the transform's interface did not change, only its internal computation.

**Application-Centric Approach:** Shared libraries are versioned, but the version lock is managed by dependency managers (npm, pip, Maven) that allow implicit upgrades. Organization B's build pulls the latest version of the shared library without realizing the behavior has changed. The drift is semantic --- invisible to version checks that only compare interface signatures.

**PGS Approach:**

1.  CT_ atoms are versioned and immutable. CT_PURE_GENERATE_ID_V0 is a structural fact. Organization A cannot modify it --- they must create CT_PURE_GENERATE_ID_V1. Organization B's CC_ pipelines still reference V0, which is unchanged.
2.  The FQDN tree hash is embedded in every build manifest. If Organization A modifies the FQDN tree (adding a new package, changing a registry), the hash changes. Organization B's build produces a different manifest hash --- a visible governance change, even if no artifact code changed.
3.  Cross-domain references are versioned explicitly. A CC_ pipeline that references CT_PURE_GENERATE_ID_V0 will always reference V0 until the governance artifact is amended. There is no "latest" resolution. There is no implicit upgrade path. Version binding is structural --- part of the ratified artifact, not a dependency manager configuration.

**Eliminated pathology:** Silent semantic drift across organizational boundaries. In PGS, behavioral changes require new artifact versions, and federation topology changes are visible through FQDN tree hash changes.

## 11.8 --- Generated Output: Federation Topology Map

This section demonstrates the system-generated output that makes the federation topology visible and auditable.

### Federation Topology Report

Given the FQDN tree and the builder's discovery results, the system produces a federation topology map --- the complete structural composition of the system:

    FEDERATION TOPOLOGY MAP
    ============================================================
    FQDN Tree: STRUCTURE_DISCOVERY_V0
    FQDN Hash: sha256:a7b3c9d1...

    PACKAGE TOPOLOGY (8 packages, 3 roles):

      CORE PACKAGES:
        governance        (order 1, authority: sovereign)
          registries: 2 (layers, concerns)
          artifacts:  constitutions, governance docs

        execution         (order 2, authority: delegated)
          registries: 0 (engine code only)
          depends_on: governance

        tooling           (order 7, authority: delegated)
          registries: 0 (builder tools)
          depends_on: governance, execution

        transport         (order 8, authority: delegated)
          registries: 1 (http_gateway)
          depends_on: governance, execution

      CAPABILITY PACK:
        reusable          (order 3, authority: delegated)
          registries: 1 (shared CT_, CS_)
          artifacts:  24 capability_transforms, 8 capability_side_effects
          depends_on: governance, execution

      DOMAIN PACKS:
        blockchain        (order 4, authority: delegated)
          registries: 3 (identity, wallet, transaction)
          artifacts:  3 workflows, 6 capability_contracts,
                      4 domain CT_, 3 intents, 3 events, 2 actors
          depends_on: governance, reusable

        ai_licensing      (order 5, authority: delegated)
          registries: 1 (unified)
          artifacts:  3 workflows, 4 capability_contracts,
                      3 domain CT_, 3 intents, 3 events, 2 actors
          depends_on: governance, reusable

        book              (order 6, authority: delegated)
          registries: 6 (policy, fee, access, audit, entitlement,
                         compliance)
          depends_on: governance, reusable

    DEPENDENCY GRAPH:
      governance  ← execution, reusable, blockchain, ai_licensing,
                    book, tooling, transport
      execution   ← reusable, tooling, transport
      reusable    ← blockchain, ai_licensing, book

    CYCLE DETECTION:    NONE
    UNREGISTERED DIRS:  NONE (builder does not scan)
    BUILD ORDER VALID:  YES (strictly ascending dependencies)
    ============================================================

### What the Output Proves

**1. The federation is finite and enumerable.** Eight packages. Three roles. Fourteen registries. Every package, registry, and dependency is declared and visible. There are no undiscovered packages, no hidden registries, no implicit dependencies.

**2. The dependency graph is acyclic.** Every dependency arrow points from a higher build_order to a lower one. The graph is a DAG --- no cycles, no mutual dependencies, no circular resolution paths.

**3. Domain packs are structurally independent.** `blockchain`, `ai_licensing`, and `book` share the same governance and reusable substrate but do not depend on each other. Each can be developed, built, and tested independently. Adding a new domain pack does not affect existing domain packs --- it requires only a FQDN tree amendment and a new entry in env_facts.

**4. WHAT/HOW separation is manifest.** The author declared packages, registries, dependencies, and artifact types in the FQDN tree (WHAT). The builder discovered, validated, and materialized artifacts according to the declared topology (HOW). The federation topology map is a system-generated proof that the declared structure is consistent, complete, and buildable.

**Structural impossibility:** The builder cannot discover packages not declared in the FQDN tree --- because discovery iterates declared registries only, and declared registries are finite. It cannot resolve dependencies that violate build order, and cannot materialize artifacts from unregistered directories. The federation topology is not a best-effort scan of the filesystem. It is a structural derivation from governance artifacts. Changing the federation requires amending the FQDN tree --- a constitutional change with a new hash, a new manifest, and a governance-visible audit trail.

## 11.9 --- Boundary and Forward Pointer

This chapter proved that federation in PGS is a governance property --- not a deployment concern. The FQDN tree declares the complete structural topology: packages, roles, authorities, registries, dependencies, and build order. The builder discovers artifacts within declared registries only. The path registry derives all paths from the FQDN tree and env_facts. Cross-domain references resolve through build order --- no import directives, no classpath scanning, no runtime discovery. The federation topology is finite, enumerable, acyclic, and auditable.

**What this chapter did not cover:**

- Runtime scaling strategies and performance optimization
- Network topology and distributed deployment
- Container orchestration and cross-cluster routing
- Version coexistence within a single domain (multiple versions of the same workflow)
- Environment-specific configuration (dev, test, production)
- Cross-organizational governance processes (how organizations agree on shared substrate changes)

**What comes next:** Chapter 12 --- Linear Scalability Through Compositional Isolation. This chapter proved that federation produces a stable structural topology. Chapter 12 addresses what happens when that topology must scale --- how version coexistence, environment facts, and compositional isolation enable systems to grow linearly without polynomial complexity increase.

**Layer movement:** Federation axis established. Moving to scaling and compositional isolation.

## 11.10 --- Review Questions

1.  **True or False: A directory containing governance artifacts is automatically discovered by the builder.**

- *False. The builder discovers artifacts only in registries declared in the FQDN tree. A directory that exists on the filesystem but is not declared in the FQDN tree is invisible to the builder. Directory presence does not equal domain existence --- governance declaration does.*

2.  **What is the FQDN tree and what does it declare?**

- *The FQDN tree (STRUCTURE_DISCOVERY_V0) is a constitutional governance artifact that declares the complete package topology of the system: every package's name, role, authority level, build order, physical root path, registries, and dependencies. It is the single source of truth for federation structure. It is hashed and the hash is embedded in every build manifest for immutability tracking.*

3.  **How do cross-domain artifact references resolve without import statements?**

- *Through build order and registry declarations. The builder processes packages in strict build_order. A domain pack (e.g., blockchain at order 4) depends on packages with lower build order (e.g., reusable at order 3). When the builder discovers blockchain artifacts, all reusable artifacts are already validated and materialized. The builder checks referential integrity --- if a CC_ pipeline references a CT_ atom, that atom must exist in a registry discovered at equal or lower build order. No explicit import directive is required because the dependency graph determines the resolution scope.*

4.  **What happens if two packages declare the same name in the FQDN tree?**

- *The FQDN tree requires unique package names. Each package has a distinct physical_root and distinct registry paths. Duplicate package names would be caught at FQDN tree parse time. Even if two packages use similar internal directory names (e.g., both have a wallet/ subdirectory), their registries are scoped to their package --- blockchain/governance/registry/wallet/ and loyalty/governance/registry/wallet/ are distinct, declared registries.*

5.  **Why does the FQDN tree prohibit implicit filesystem discovery?**

- *Because filesystem presence is not governance authority. A directory on disk is a physical artifact that anyone can create --- accidentally, for testing, or through deployment error. Structural existence in PGS requires constitutional declaration. The prohibition ensures that the federation topology is derivable exclusively from governance metadata --- readable, auditable, and deterministic --- rather than from filesystem state that can change between builds.*

6.  **Where does federation authority reside?**

- *In the FQDN tree. The FQDN tree is governed by CONSTITUTION_GOVERNANCE_V0 and carries sovereign authority. Packages derive their authority (delegated) from the FQDN tree's declaration. The builder derives its behavior from the FQDN tree's build contract. The path registry derives all paths from the FQDN tree's physical_root declarations. Every structural decision --- what exists, where it lives, what it depends on --- traces back to this single governance artifact.*

7.  **What invariant governs federation in PGS?**

- *I-F1 --- Declarative Federation: System structure must be derivable exclusively from ratified governance metadata present at build time. No implicit discovery, filesystem scanning, or runtime reflection may contribute to structural topology. This extends I-S2 (No Ambient Authority) from execution to structure: just as no execution context grants capabilities, no physical context grants structural existence.*
