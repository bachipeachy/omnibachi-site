---
title: Chapter 12 — Linear Scalability Through Compositional Isolation
date: '2026-04-16'
draft: false
weight: 14
slug: chapter-12-linear-scalability-through-compositional-isolation
---

Chapter 10 proved that no undeclared execution can occur. Chapter 11 proved that no undeclared structure can exist. But a system can have perfect security and perfect federation and still collapse under its own complexity. If every new domain introduces coupling to every existing domain, the interaction surface grows quadratically. If every version upgrade cascades through dependent artifacts, the migration cost grows with the dependency graph.

This chapter completes the structural arc. It answers: **Why does complexity in a protocol-governed system grow linearly with the number of declared artifacts --- rather than polynomially with the interactions between them?**

The answer is compositional isolation. Domains compose through declared contracts, not shared mutable state. Version coexistence is structural --- V0 and V1 of the same workflow coexist as independent artifacts, not as branches in a migration strategy. Environment variability is deterministic --- runtime bindings and environment facts route execution without altering governance semantics. The chapter proves these properties formally, shows why each follows from the architectural decisions of Chapters 3 through 11, and demonstrates that linear scaling is not an aspiration but a structural consequence of the PGS model. By the end, the reader will understand why the third domain on a governed platform costs less to add than the second --- and why the tenth costs less still.

## 12.1 --- The Engineering Objective

Chapter 10 proved that no undeclared execution can occur. Chapter 11 proved that no undeclared structure can exist. This chapter completes the structural arc by proving that complexity growth is controlled --- that adding domains and versions increases artifact count linearly without increasing interaction surface polynomially.

The distinction matters. A system can have perfect security (Chapter 10) and perfect federation (Chapter 11) and still collapse under its own complexity. If every new domain introduces coupling to every existing domain, the interaction surface grows quadratically. If every version upgrade cascades through dependent services, the migration cost grows with the dependency graph. If every environment introduces behavioral variation, the testing surface grows combinatorially. These are not security failures or federation failures. They are scaling failures --- and they are the dominant cost driver in mature software systems.

**The Task:** Prove that in PGS, domains compose without semantic entanglement, version coexistence is structural, environment variability is deterministic, and complexity grows proportionally to declared artifacts --- not to interactions between artifacts.

**The Constraint:** PGS does not permit shared mutable state across domains, in-place artifact mutation, implicit version resolution, or environment-specific behavioral branching in governance artifacts. Scaling constraints are structural --- not policy-based.

In the application-centric approach, scaling is an operational problem. More users require more instances. More features require more services. More services require more integration points. In unconstrained service architectures, any service may call any other service unless explicitly restricted. Over time, this freedom tends toward dense inter-service coupling --- the integration surface grows as O(n²), or to be precise O(n(n-1)/2). A system with 5 microservices has 10 potential integration paths. A system with 50 has 1,225. A system with 500 has 124,750. Each integration path is a potential coupling point --- a place where a change in one service can cause a failure in another. Teams spend more time managing interactions than building features. The system does not scale linearly. It scales polynomially --- and the polynomial wins.

In PGS, scaling is a structural consequence. Domains interact only along declared dependencies --- and the FQDN tree (Chapter 11) enforces that domain packs do not depend on each other. Three domain packs sharing a common reusable substrate have three dependency declarations --- not six pairwise integrations. Adding a fourth domain pack adds one dependency declaration --- not three new integration paths. The interaction surface grows linearly with the number of domains, because interactions are bounded by the dependency graph, and the dependency graph is governed.

## 12.2 --- Compositional Isolation

**Definition:** Compositional isolation is the structural property that each domain pack is a self-contained governance unit --- with its own registries, its own materialized artifacts, its own runtime data root, and its own runtime bindings --- that composes with other domains only through declared dependencies on shared substrate.

**Key Properties:**

1.  **No peer-to-peer domain dependencies.** Domain packs depend on the governance and reusable substrate. They do not depend on each other. The blockchain domain cannot reference ai_licensing artifacts. The ai_licensing domain cannot reference blockchain artifacts. Each domain's governance registries are scoped to its own package in the FQDN tree.
2.  **Module-scoped data roots.** Each domain's runtime state --- traces, registries, event logs --- is stored in a module-specific data root. Blockchain traces go to `blockchain/testbed/outputs/`. AI licensing traces go to `ai_licensing/testbed/outputs/`. There is no shared mutable state across domains.
3.  **Independent materialization.** Each domain pack materializes to its own `protocol/artifacts/` directory. The builder processes domains in build_order, but each domain's artifacts are self-contained. Removing a domain pack removes its artifacts. Adding a domain pack adds its artifacts. No other domain's artifacts change.

### Example 12.1 --- Compositional Isolation Structure

Three domain packs, each independently governed, sharing a common substrate:

    SHARED SUBSTRATE:
      governance/         (constitutions, vocabulary, schemas)
      reusable/           (24 shared CT_ atoms, 8 CS_ side effects)
        protocol/artifacts/capability_transforms/
        protocol/artifacts/capability_side_effects/

    DOMAIN PACK: blockchain (build_order 4)
      blockchain/governance/registry/
        identity/         (actors, intents, workflows, events, CCs)
        wallet/           (intents, workflows, CCs, CTs, RBs)
        transaction/      (intents, workflows, CCs, CTs)
      blockchain/protocol/artifacts/    (materialized: 43 artifacts)
      blockchain/testbed/outputs/       (isolated data root)

    DOMAIN PACK: ai_licensing (build_order 5)
      ai_licensing/governance/registry/
        (intents, workflows, CCs, CTs, events, actors, RBs)
      ai_licensing/protocol/artifacts/  (materialized: 20 artifacts)
      ai_licensing/testbed/outputs/     (isolated data root)

    DOMAIN PACK: book (build_order 6)
      book/{policy,fee,access,audit,entitlement,compliance}/
        governance/registry/
      book/protocol/artifacts/          (materialized: 28 artifacts)
      book/testbed/outputs/             (isolated data root)

**Analysis:**

- Three domain packs. Zero peer-to-peer domain dependencies. Each depends on `governance` and `reusable` --- shared substrate that is built before any domain pack. The blockchain team can add workflows without affecting ai_licensing. The ai_licensing team can add capability contracts without affecting blockchain. The book team can add pedagogical examples without affecting either.
- Each domain materializes to its own artifact directory. The builder writes blockchain artifacts to `blockchain/protocol/artifacts/` and ai_licensing artifacts to `ai_licensing/protocol/artifacts/`. There is no shared artifact directory that could create collision or coupling.
- Each domain has its own data root. Runtime state --- wallet registries, actor event logs, license registries, audit logs --- is scoped to the module's data root by the `{{module_data_root}}` parameter in runtime bindings. One domain cannot accidentally read or write another domain's state.

### Example 12.2 --- Complexity Growth Comparison

The complexity growth difference between application-centric and protocol-governed systems:

    APPLICATION-CENTRIC (Microservices):
      n services → up to n(n-1)/2 pairwise integration paths

      5 services   →    10 potential integrations
      10 services  →    45 potential integrations
      50 services  →  1225 potential integrations
      100 services →  4950 potential integrations

      Growth: O(n²)
      Any service may call any other unless explicitly restricted.
      Integration surface is bounded by combinatorics, not by architecture.

    PGS (Compositional Isolation):
      n domain packs → n declared dependencies (each to shared substrate)

      5 domains   →   5 dependency declarations
      10 domains  →  10 dependency declarations
      50 domains  →  50 dependency declarations
      100 domains → 100 dependency declarations

      Growth: O(n)
      Each new domain depends on shared substrate only.
      Interaction surface is bounded by the dependency graph.

**Analysis:**

- The difference is architectural, not organizational. Application-centric systems grow polynomially because any service *can* call any other service --- and over time, many do. PGS grows linearly because domain packs *cannot* depend on each other --- the FQDN tree's dependency graph does not permit horizontal domain-to-domain dependencies.
- The constant factor is governance-determined. Each domain pack declares dependencies on `governance` and `reusable`. These are the only interaction paths. The shared substrate is built first (lower build_order) and is immutable once materialized. Adding a new domain pack adds one package declaration and one set of dependency declarations --- not new edges to every existing domain.
- This is not a process discipline. It is a structural invariant. Even if a team *wanted* to create a dependency from blockchain to ai_licensing, the FQDN tree would reject it --- ai_licensing (order 5) has a higher build order than blockchain (order 4). Forward-only dependencies and no horizontal domain dependencies are enforced by the same mechanism that enforces federation (Chapter 11, I-F1).

### A Concrete Illustration

Consider an organization with 10 domain packs, each exposing an average of 5 workflows. In a traditional microservices architecture, each workflow may integrate with 3 other services on average. The realized integration surface is approximately 10 × 5 × 3 = 150 integration points --- each requiring implementation, testing, and maintenance. When the organization adds an 11th domain, that domain integrates with an average of 3 existing services per workflow, adding roughly 15 new integration points. Each integration point costs roughly 2 engineering-days to implement and 1 engineering-day per year to maintain.

**Traditional: 10 domains × 15 integration points per domain = 150 integration points.** **Annual maintenance: 150 × 1 day = 150 engineering-days.** **Adding domain 11: +15 integration points, +15 days maintenance per year.**

In PGS, the same 10 domain packs each declare one dependency on shared substrate. Adding the 11th domain adds one dependency declaration. The governance authoring cost for each workflow is roughly 2 engineering-days. The integration cost is zero --- integration is declared in governance artifacts and validated by the builder. Maintenance cost per domain is bounded by the artifact count, not the interaction graph.

**PGS: 10 domains × 1 dependency = 10 dependency declarations.** **Annual maintenance: proportional to artifact count, not integration density.** **Adding domain 11: +1 dependency declaration, +0 integration points.**

The numbers are hypothetical but the scaling law is structural. The gap widens with every domain added.

## 12.3 --- Version Coexistence

In application-centric systems, version upgrades are migrations. The old version is replaced by the new version. Dependent services must update their integrations. The upgrade cascades through the dependency graph. If the old version must remain operational during migration, the team must maintain two code paths, two configurations, two deployment targets. Version coexistence is an operational burden --- not an architectural property.

In PGS, version coexistence is structural. Versions are encoded in artifact codes. WF_CREATE_WALLET_V0 and WF_CREATE_WALLET_V1 are distinct artifacts --- distinct governance registries, distinct materialized protocols, distinct traces, distinct entries in the workflow-to-module mapping. They coexist by construction. Neither replaces the other.

### Example 12.3 --- Version Coexistence

Two versions of a wallet creation workflow coexisting in the same system:

*(The full artifact is provided in Appendix B, Example 12.3.)*

**Analysis:**

- V0 is not modified. It is not deprecated. It is not migrated. It continues to exist with its original governance artifacts, its original capability contracts, and its original behavior. V0's hash in the build manifest is unchanged. Any trace produced by V0 execution references V0 artifacts --- and can be replayed against V0 artifacts indefinitely.
- V1 is a new artifact chain. It has its own WF_ specification, its own CC_ contracts, and its own CT_ references. The builder validates V1 independently. If V1 fails constitutional validation, V0 is unaffected. V1 does not inherit V0's governance --- it declares its own.
- Runtime routing distinguishes versions by code. The env_facts `workflow_to_module` mapping contains separate entries for V0 and V1. A request for WF_CREATE_WALLET_V0 routes to V0's artifact chain. A request for WF_CREATE_WALLET_V1 routes to V1's. There is no "latest" resolution. There is no implicit upgrade. The version the caller requests is the version that executes.
- Migration is optional. If all callers switch to V1 and V0 is no longer needed, it can be removed from the governance registry --- a governance change, not a code change. Governance may explicitly deprecate V0, but deprecation is a governance act --- not an in-place mutation. V0 can also remain indefinitely. Version coexistence is not a transitional state. It is a stable architectural property.

### Immutability as the Foundation of Coexistence

Version coexistence depends on artifact immutability. If V0 could be silently modified, coexistence would be meaningless --- a request for V0 might receive modified-V0 behavior. PGS enforces immutability structurally:

1.  **Content hashing.** Every materialized artifact is hashed (SHA-256) during the builder's materialization phase. The hash is recorded in the build manifest. Any modification to an artifact's content produces a different hash --- a detectable governance change.
2.  **Code-filename matching.** The builder validates that every artifact's code matches its canonical filename. CT_PURE_GENERATE_ID_V0 must live in `ct_pure_generate_id_v0.md`. A renamed file with modified content fails the identity check.
3.  **Version is part of the code.** V0 and V1 are not metadata tags --- they are part of the artifact code itself. WF_CREATE_WALLET_V0 and WF_CREATE_WALLET_V1 are structurally distinct codes with distinct filenames, distinct registrations, and distinct hashes. There is no mechanism to "update V0 to V1" --- they are different artifacts.

## 12.4 --- Environment Facts as Deterministic Context

Workflows execute in environments --- development, testing, production. In application-centric systems, environments introduce behavioral variation through feature flags, configuration files, environment variables, and conditional logic. The same code behaves differently in different environments. Testing in dev does not prove correctness in production. The environment is a hidden input to every operation.

In PGS, environments change routing --- not semantics.

### Example 12.4 --- Environment Facts

The env_facts file provides the runtime's environmental context:

*(The full artifact is provided in Appendix B, Example 12.4.)*

**Analysis:**

- The `environment` field is metadata --- not a behavioral branch. No governance artifact references it. No workflow DAG contains conditional edges based on environment. No CC_ pipeline selects different transforms for dev versus production. The governance artifacts are environment-invariant.
- The `disable_external_side_effects` flag controls whether external runtimes are activated or replaced with disabled stubs. In dev, external API calls are suppressed. In production, they execute. But the governance artifacts --- the workflow specification, the capability contracts, the result_status routing --- are identical. The workflow follows the same DAG, traverses the same nodes, produces the same structural trace. The difference is operational (which runtime class handles the CS_ step), not semantic (what the workflow does).
- The `module_data_roots` mapping determines where traces and runtime state are stored. In dev, blockchain traces go to `blockchain/testbed/outputs/`. In production, they might go to `/var/data/blockchain/`. The governance artifacts do not reference these paths --- the runtime bindings use `{{module_data_root}}` parameter substitution, resolved at load time from env_facts. The artifacts are portable across environments without modification.

### The Routing/Semantics Separation

This separation is critical for scaling:

    WHAT CHANGES ACROSS ENVIRONMENTS:
      - Module data roots (where traces are stored)
      - External side-effect activation (enabled/disabled)
      - Runtime binding paths (parameter substitution)

    WHAT DOES NOT CHANGE:
      - Governance artifacts (WF_, IN_, CC_, CT_, CS_, AC_, EV_)
      - Vocabulary (prefixes, keywords, operation verbs)
      - DAG structure (nodes, edges, routing)
      - Result status contracts (allowed outcomes)
      - Failure classification (same taxonomy)
      - Trace schema (same structure)

Governance artifacts are portable. The same WF_CREATE_WALLET_V0 specification, the same CC_PERSIST_WALLET_V0 contract, the same CT_PURE_GENERATE_ID_V0 atom --- all execute identically in dev, test, and production. What changes is where the data goes and whether external systems are reached. The behavioral surface --- what the workflow does, what outcomes are possible, what failures are classified --- is environment-invariant.

## 12.5 --- Validation and Failure Surface

### Scaling Validation Checks

  -----------------------------------------------------------------------------------------------------------
  Step          Check                          Failure Condition
  ------------- ------------------------------ --------------------------------------------------------------
  1             Module data root isolation     Two modules resolve to overlapping data paths

  2             Version integrity              Artifact content modified without version increment

  3             Runtime binding scope          RB_ artifact appears in shared registry (not domain-scoped)

  4             Cross-domain state access      CS_ binding references another module's data root

  5             Environment semantic leakage   Governance artifact contains environment-conditional logic
  -----------------------------------------------------------------------------------------------------------

### Broken Example 12.5 --- Version Shadowing

A developer modifies CT_PURE_SIGN_MESSAGE_V0 to fix a bug --- changing the signing algorithm --- without creating a new version:

    Before modification:
      ct_pure_sign_message_v0.md  →  hash: sha256:a1b2c3...

    After modification:
      ct_pure_sign_message_v0.md  →  hash: sha256:d4e5f6...

The build manifest records the new hash. Any comparison between builds reveals the change:

    INTEGRITY WARNING
      Artifact:       CT_PURE_SIGN_MESSAGE_V0
      Previous hash:  sha256:a1b2c3...
      Current hash:   sha256:d4e5f6...
      Detail:         Content of versioned artifact has changed.
                      Versioned artifacts are structurally immutable.
                      Behavioral changes require a new version suffix.
      Resolution:     Create CT_PURE_SIGN_MESSAGE_V1 with the new
                      algorithm. Leave V0 unchanged for existing
                      consumers.

**Analysis:**

- The hash change is detectable. Every build manifest records artifact hashes. A CI pipeline that compares manifest hashes between builds can flag the modification as a governance violation. The content-addressing mechanism that enables trace replay (Chapter 9) also enables version integrity verification.
- The violation is semantic, not syntactic. The file still parses. The schema is valid. The vocabulary is conformant. But the artifact's behavior has changed while its version code has not. This is the definition of version shadowing --- a silent behavioral change disguised as an unchanged version. In application-centric systems, this is how "bug fixes" introduce regressions. In PGS, the hash difference makes the change visible.
- The correction is structural: create V1. CT_PURE_SIGN_MESSAGE_V1 gets a new governance artifact, a new hash, and new consumers can reference it explicitly. V0 remains unchanged for existing CC_ pipelines that depend on it. No cascade. No forced migration.

### Broken Example 12.6 --- Cross-Domain State Leakage

A developer configures a blockchain runtime binding to write to the ai_licensing module's data root:

*(The full artifact is provided in Appendix B, Example 12.6.)*

**Analysis:**

- The binding hard-codes another module's data root instead of using `{{module_data_root}}` parameter substitution. At runtime, blockchain wallet state would be written to ai_licensing's output directory --- violating module data isolation.
- The FQDN tree's global rule states: "Runtime bindings, where declared, MUST be domain-scoped and SHALL NOT appear in shared registries." A binding that reaches into another module's data root violates domain scoping.
- The structural remedy is `{{module_data_root}}` parameter substitution. Runtime bindings declare paths relative to the module's data root --- resolved at load time from env_facts. This ensures that each module's storage is isolated by construction, not by convention.

## 12.6 --- Structural Insight (Doctrine Moment)

The reader has now seen compositional isolation (Example 12.1), complexity growth comparison (Example 12.2), version coexistence (Example 12.3), environment facts (Example 12.4), and structural rejection of version shadowing and cross-domain state leakage (Examples 12.5--12.6). At no point did scaling depend on infrastructure capacity, operational procedures, or team coordination. At every point, scaling was a structural consequence of architectural properties --- domain isolation, artifact immutability, dependency graph acyclicity, and environment/semantics separation.

This is a new invariant:

**Invariant I-C1 --- Compositional Isolation:** No domain pack may introduce semantic coupling to another domain pack except through declared dependency on shared substrate and version-bound artifacts. Adding a domain increases artifact count proportionally to that domain's declarations, without introducing new peer interaction edges.

I-C1 completes the structural arc established by I-S2 and I-F1:

- **I-S2 (No Ambient Authority, Chapter 10):** No undeclared execution. The vocabulary bounds the behavioral surface.
- **I-F1 (Declarative Federation, Chapter 11):** No undeclared structure. The FQDN tree bounds the federation topology.
- **I-C1 (Compositional Isolation, Chapter 12):** No uncontrolled complexity growth. The dependency graph bounds the interaction surface.

Together, these three invariants establish that execution is bounded, structure is bounded, and complexity growth is bounded. The system can scale by adding domains, adding versions, and adding environments --- without any of these additions creating coupling to what already exists.

**What the system cannot do:**

- **Retroactively alter another domain's behavior.** Domain packs do not depend on each other. A change to blockchain's governance artifacts cannot affect ai_licensing's execution. The dependency graph is acyclic and forward-only --- changes flow from shared substrate to consumers, never between peers.
- **Overwrite a prior version.** Artifact codes include version suffixes. V0 and V1 are distinct artifacts with distinct hashes, distinct registrations, and distinct governance chains. There is no mechanism to "update V0" --- there is only "create V1 alongside V0."
- **Alter semantic execution through environment configuration.** Environment facts change routing (where data goes, which runtime class handles a CS_ step). They do not change governance artifacts (which workflows exist, what outcomes are possible, which transforms execute). The same governance artifacts produce the same DAG, the same trace structure, and the same failure classification in every environment.
- **Introduce cross-domain coupling without governance change.** Cross-domain interaction requires a dependency declaration in the FQDN tree, a version-bound artifact reference, and a build that validates the reference. Implicit coupling --- shared databases, shared message queues, shared configuration files --- is structurally absent because domains have isolated data roots, isolated artifact directories, and isolated runtime bindings.

**Scale emerges from isolation.** This is the chapter's doctrinal claim. In application-centric systems, scale is achieved by adding capacity --- more servers, more instances, more bandwidth. But capacity does not reduce complexity. A system with 500 microservices on 5,000 servers has the same integration complexity as the same system on 500 servers. In PGS, scale is achieved by adding domains --- and each domain is compositionally isolated. The complexity of the system is the sum of its domains' complexities, not the product of their interactions.

## 12.7 --- Solved Problems

### Problem 12.1 --- "Cascade Upgrade Failure"

**Scenario:** A platform team upgrades a shared authentication library from v2 to v3. The upgrade changes the token format. Seven services depend on the library. Each service must update its token parsing, its test fixtures, its deployment configuration, and its integration tests. The upgrade takes three sprints. During migration, some services use v2 tokens and some use v3. Inter-service calls fail when a v3 service receives a v2 token. The team rolls back, schedules a coordinated big-bang upgrade, and blocks all other feature work for the release window.

**Application-Centric Approach:** The shared library is a coupling point. Every consumer inherits the upgrade obligation. The upgrade cascades through the dependency graph. Services that are "not ready" block the upgrade. Services that upgrade first break compatibility with services that haven't. The migration window becomes a coordination problem --- not a technical problem.

**PGS Approach:**

1.  The shared transform is CT_PURE_VALIDATE_TOKEN_V0. The platform team creates CT_PURE_VALIDATE_TOKEN_V1 with the new format. V0 remains unchanged --- same artifact, same hash, same behavior.
2.  Services that want the new token format update their CC_ pipelines to reference V1. Services that are not ready continue referencing V0. Both versions coexist. There is no coordination window. There is no cascade.
3.  When all consumers have migrated to V1 and V0 has no remaining references, V0 can be removed from the governance registry --- a deliberate governance action, not a forced migration.

**Eliminated pathology:** Forced cascade upgrade across dependency graph. In PGS, version coexistence is structural. Migration is optional and incremental. No service is forced to upgrade by another service's decision.

### Problem 12.2 --- "Environment Drift"

**Scenario:** An e-commerce platform behaves differently in development and production. In dev, a feature flag enables a "skip payment verification" shortcut. In production, the flag is disabled. A developer tests a checkout workflow in dev --- it succeeds. The same workflow fails in production because the payment verification step discovers a data format mismatch that the shortcut bypassed. The bug existed in dev all along --- but the feature flag masked it.

**Application-Centric Approach:** Feature flags create environment-specific behavioral branches. The code contains `if (environment === 'dev') { skipVerification() }`. Dev and production execute different code paths. Testing in dev does not prove correctness in production because the code path is literally different.

**PGS Approach:**

1.  Governance artifacts are environment-invariant. The WF_ specification, the CC_ contracts, the CT_ transforms, the result_status routing --- all are identical across environments. There is no `if dev` branch in the DAG.
2.  The `disable_external_side_effects` flag in env_facts controls whether external runtimes are active or stubbed --- but the governance pipeline is the same. The workflow traverses the same nodes, executes the same transforms, produces the same result_status routing. The stub conforms to the same result_status contract as the production runtime --- it returns a synthetic response within the declared outcome space, preserving structural execution identity.
3.  A data format mismatch would be caught in dev because the same CT_ transform processes the same input schema in both environments. The transform is pure --- it does not know what environment it runs in. If it fails, it fails identically in dev and production.

**Eliminated pathology:** Environment-specific behavioral drift through feature flags and configuration branching. In PGS, environments change routing --- not semantics. A workflow that succeeds in dev succeeds in production because it follows the same governed artifact chain.

### Problem 12.3 --- "Hidden Shared State"

**Scenario:** Two microservices --- Order Service and Inventory Service --- write to the same database table. Order Service writes a row when an order is placed. Inventory Service reads the row to reserve stock. A schema change in Order Service (adding a new column) breaks Inventory Service's read query. Neither team knew the other was using the table directly. The coupling was implicit --- hidden in database connection strings and ORM configurations.

**Application-Centric Approach:** Services share mutable state through a common database. The coupling is invisible at the service interface level --- it exists in the data layer. Schema changes in one service cascade to every service that touches the same table. The integration surface is the database schema --- unbounded and ungovernered.

**PGS Approach:**

1.  Each domain pack has its own module data root. Blockchain side effects write to `blockchain/testbed/outputs/`. AI licensing side effects write to `ai_licensing/testbed/outputs/`. There is no shared database table.
2.  Runtime bindings use `{{module_data_root}}` parameter substitution. CS_WALLET_STATE_V0 writes to `{{module_data_root}}/wallet_state.json` --- resolved to the blockchain module's data root. CS_LICENSE_REGISTRY_V0 writes to `{{module_data_root}}/license_registry.json` --- resolved to the ai_licensing module's data root. The paths are structurally isolated.
3.  Cross-domain data sharing, if needed, would be mediated through an explicit CC_ pipeline --- a governed artifact chain with declared inputs, outputs, and result statuses. There is no "direct table access" because there are no shared tables. The data isolation is structural --- enforced by the path registry's derivation from env_facts module data roots.

**Eliminated pathology:** Implicit coupling through shared mutable state. In PGS, each domain's state is isolated by the module data root. Cross-domain interaction requires explicit governance artifacts --- not shared database connections.

### Problem 12.4 --- "Scaling Through Duplication"

**Scenario:** A team needs to add a new business domain --- loyalty rewards. The existing codebase has no clean extension point. The team copies the order management module, renames classes, rewrites business logic, and deploys. Six months later, a security fix in the order management module must be applied to the loyalty module --- but the code has diverged. The team must manually port the fix, re-test, and re-deploy. Every duplicated module is a maintenance liability.

**Application-Centric Approach:** Scaling by duplication creates maintenance debt. Each copy diverges. Shared fixes must be manually ported. The system's complexity is proportional to the number of copies, and each copy is a full-weight maintenance obligation.

**PGS Approach:**

1.  A new domain pack is a new FQDN tree entry --- not a copy of an existing module. The loyalty domain declares its own package, registries, and governance artifacts. It depends on `governance` and `reusable` --- the same shared substrate that every other domain depends on.
2.  Shared capability transforms (CT_ atoms) live in the reusable package. The loyalty domain references CT_PURE_GENERATE_ID_V0, CT_PURE_EXTRACT_V0, and other shared atoms --- the same atoms that blockchain and ai_licensing reference. A security fix to a shared atom is fixed once, in the reusable package. Every domain that references the atom receives the fix on the next build.
3.  Domain-specific logic lives in domain-specific governance artifacts --- not in copied code. The loyalty domain's WF_, CC_, and IN_ artifacts are authored for loyalty concerns. They are not copies of order management artifacts. There is no divergence because there was no duplication.

**Eliminated pathology:** Scaling through duplication and the maintenance debt it creates. In PGS, new domains extend the system through new governance declarations --- referencing shared substrate rather than copying it.

## 12.8 --- Generated Output: Compositional Isolation Report

This section demonstrates the system-generated output that makes compositional isolation verifiable.

### Compositional Isolation Report

Given the FQDN tree, the builder's discovery results, and the env_facts module mapping, the system produces a compositional isolation report:

    COMPOSITIONAL ISOLATION REPORT
    ============================================================
    FQDN Tree: STRUCTURE_DISCOVERY_V0
    Build Manifest: 2026-02-22T14:36:34Z

    DOMAIN PACKS (3):
      blockchain     artifacts: 43   registries: 3   data_root: blockchain/testbed/outputs
      ai_licensing   artifacts: 20   registries: 1   data_root: ai_licensing/testbed/outputs
      book           artifacts: 28   registries: 6   data_root: book/testbed/outputs

    SHARED SUBSTRATE:
      reusable       CT atoms: 24    CS specs: 8

    ISOLATION CHECKS:
      Peer-to-peer domain dependencies:  0 (no domain→domain)
      Shared mutable state paths:       0 (all {{module_data_root}} scoped)
      Cross-domain artifact references: 0 (domains reference reusable only)
      Version coexistence conflicts:    0 (all versions explicit)

    COMPLEXITY METRICS:
      Domain count (n):                 3
      Dependency declarations:          3 (each → [governance, reusable])
      Interaction surface:              O(n) = 3
      Theoretical max (O(n²)):          3 (3×2/2 pairwise)
      Relative density:                  Actual edges grow linearly (n);
                                        unconstrained edges grow quadratically
                                        (n(n-1)/2). Density decreases as n increases.

    ENVIRONMENT INVARIANCE:
      Governance artifacts:             environment-independent
      DAG structure:                    environment-independent
      Trace schema:                     environment-independent
      Module data roots:                environment-specific (routing only)
      External side effects:            environment-specific (disabled in dev)

    ARTIFACT IMMUTABILITY:
      Total artifacts:                  91 (across all domain packs)
      Content hashes recorded:          91/91
      Version integrity:                ALL artifacts version-suffixed
      FQDN tree hash:                   sha256:2aadb729...
    ============================================================

### What the Output Proves

**1. Compositional isolation is verified.** Zero peer-to-peer domain dependencies, zero shared mutable state paths, zero cross-domain artifact references. Each domain pack is structurally isolated from every other domain pack.

**2. Complexity growth is linear.** Three domain packs produce three dependency declarations --- not six pairwise integrations. The interaction surface equals the domain count. As domains increase, the ratio of actual interactions to theoretical maximum decreases --- the system becomes *relatively simpler* as it grows.

**3. Environment invariance is structural.** Governance artifacts, DAG structure, and trace schema are environment-independent. Only routing metadata (data roots, external side-effect activation) varies. The behavioral surface is identical across all environments.

**4. Artifact immutability is total.** Every artifact is content-hashed. Every artifact carries a version suffix. The FQDN tree hash anchors the entire governance topology. Any change --- to any artifact, any registry, any dependency --- produces a new hash and a governance-visible change.

**WHAT/HOW separation:** The author declared domains with isolated registries, explicit dependencies, and version-bound artifacts (WHAT). The system verified isolation, computed complexity metrics, and confirmed environment invariance (HOW). The compositional isolation report is a structural proof --- not a test result.

**Structural impossibility:** The system cannot introduce peer-to-peer dependencies between domain packs --- because the FQDN tree prohibits them and the builder validates dependency acyclicity. It cannot share mutable state across domains --- because runtime bindings are domain-scoped and resolve through module-specific data roots. It cannot silently modify versioned artifacts --- because content hashing makes every change detectable. Scaling by adding domains is structurally guaranteed to be linear --- because the dependency graph is acyclic and domain-to-domain edges are prohibited by construction.

## 12.9 --- Boundary and Forward Pointer

This chapter proved that scaling in PGS is a structural property. Compositional isolation guarantees that domains compose without semantic entanglement. Version coexistence guarantees that upgrades do not cascade. Environment facts guarantee that routing changes without altering governance semantics. Complexity grows linearly with domains --- not polynomially with interactions.

Together with Chapters 10 and 11, this completes the structural arc:

- **Chapter 10:** Governed authority --- the vocabulary defines the total executable surface
- **Chapter 11:** Governed federation --- the FQDN tree defines the total structural topology
- **Chapter 12:** Governed scaling --- compositional isolation defines the total interaction surface

Chapter 10 bounded behavior. Chapter 11 bounded topology. Chapter 12 bounded growth.

**What this chapter did not cover:**

- Throughput scaling and horizontal compute capacity
- Performance benchmarking and optimization techniques
- Infrastructure orchestration (Kubernetes, container scaling, load balancing)
- Database sharding and distributed storage strategies
- Cross-organizational governance processes and institutional scaling
- Real-time system requirements and latency constraints

**What comes next:** Chapter 13 --- Constructing a Protocol-Governed Domain. Chapters 3--12 established the complete architectural framework: authoring, compilation, execution, transforms, side effects, failure, traces, security, federation, and scaling. Chapter 13 compresses this framework into a practitioner's construction method --- seven architectural acts that take an implementor from empty structure to deterministic execution.

**Layer movement:** Federation and scaling axes completed. Moving to construction method synthesis.

## 12.10 --- Review Questions

1.  **Why do microservice architectures tend toward polynomial complexity growth?**

- *Because any service can potentially interact with any other service. In a system of n services, the maximum pairwise integration surface is n(n-1)/2 --- which grows as O(n²). Over time, services accumulate cross-service calls, shared databases, and implicit dependencies. Each new service adds integration paths to multiple existing services. The growth is driven by combinatorics, not by architecture.*

2.  **What structural property guarantees version coexistence in PGS?**

- *Artifact immutability combined with version-encoded codes. WF_CREATE_WALLET_V0 and WF_CREATE_WALLET_V1 are distinct artifacts with distinct governance registries, distinct hashes, and distinct entries in the workflow-to-module mapping. V0 is never modified --- V1 is created alongside it. Both coexist because they are structurally independent artifacts that happen to address the same business concern at different version levels.*

3.  **Can environment facts alter workflow semantics?**

- *No. Environment facts change routing --- where traces are stored, whether external side effects are active, which module data root is used. They do not change governance artifacts --- which workflows exist, what capabilities they invoke, what result statuses they route on, what transforms they execute. The same governance artifacts produce the same DAG, the same trace structure, and the same failure classification in every environment. Environments are operational contexts, not semantic branches.*

4.  **What prevents cross-domain state leakage?**

- *Module-scoped data roots enforced through parameter substitution. Runtime bindings use* `\{\{module_data_root\}\}` *as a placeholder --- resolved at load time from env_facts to the module's specific data directory. Each domain's traces, registries, and event logs are stored in its own data root. There is no shared mutable state across domains. Cross-domain data access would require an explicit CC_ pipeline --- a governed artifact chain, not a direct storage path.*

5.  **What invariant governs scaling in PGS?**

- *I-C1 --- Compositional Isolation: No domain pack may introduce semantic coupling to another domain pack except through declared dependency on shared substrate and version-bound artifacts. Adding a domain increases artifact count linearly without increasing interaction surface polynomially. This completes the structural arc: I-S2 bounds execution, I-F1 bounds structure, I-C1 bounds complexity growth.*

6.  **How does adding a new domain affect the interaction surface?**

- *It adds one set of dependency declarations (to governance and reusable substrate) --- a constant-factor increase. It does not add edges to existing domain packs because horizontal domain-to-domain dependencies are prohibited by the FQDN tree. The interaction surface grows as O(n) with the number of domains, not as O(n²) with pairwise interactions.*

7.  **Why is artifact immutability essential for scaling?**

- *Because version coexistence depends on it. If V0 artifacts could be silently modified, then "coexistence" would be meaningless --- V0 would not be V0 anymore. Content hashing makes every modification detectable. Code-filename matching ensures identity integrity. The version suffix is part of the artifact code, not metadata. These structural guarantees ensure that adding V1 does not retroactively alter V0's behavior --- which is the foundation of non-cascading upgrades and linear scaling.*
