---
title: 'Chapter 14 — Use Case: AI Agent Governance Domain'
date: '2026-04-30'
draft: false
weight: 16
slug: chapter-14-use-case-ai-agent-governance-domain
---

Chapter 13 defined the construction method --- Act 0 through Act VII. The method is precise, the gates are structural, and the sequence is topologically determined. But a method without an industrial proof is a theory.

This chapter is the proof. It answers: **Can the eight-act construction method produce a non-trivial enterprise domain --- from business thesis to running, traced, verified execution --- without modifying the core engine or any existing domain?**

The proof domain is AI agent governance: a system that constitutionally mediates agent-proposed actions through license-tier authority binding, enforces a closed tool surface that no agent can circumvent, and records every authorization and denial in an append-only audit trail. This is not a toy example. It involves seven capability contracts, five denial paths, cross-domain reads against the blockchain module's actor registry, and a governance pipeline that must handle quota exhaustion, unauthorized tool access, suspended licenses, and expired authorizations. The chapter follows the construction method exactly as Chapter 13 described it, executes seven scenarios with trace evidence for each, and concludes with a structural inventory of what did not change --- proving that a new domain composes with existing domains through federation, not modification.

## 14.1 --- The Engineering Objective

Chapter 13 established the construction method --- Act 0 through Act VII. The reader knows the sequence. This chapter proves it works.

The proof domain is not a toy. It is not a synthetic compliance example. It is a complete AI agent governance system --- a domain that constitutionally mediates agent-proposed actions through license-tier authority binding, records every authorization and denial in an append-only audit trail, and enforces a closed tool surface that no agent can circumvent.

**The Task:** Build the `ai_governance` domain from business thesis to running, traced, verified workflows --- following the construction method exactly as described in Chapter 13. Execute seven scenarios including five denial paths. Confirm that zero changes were required to the core engine or any existing domain.

**The Domain Inventory (current):** The `ai_governance` domain comprises four workflows, five actor types, and two runtime binding artifacts:

  ----------------------------------------------------------------------------------------------------
  Workflow                                        Purpose
  ----------------------------------------------- ----------------------------------------------------
  `ai_governance::WF_GOVERN_AGENT_ACTION_V0`      Mediate and authorize agent-proposed actions

  `ai_governance::WF_PROVISION_AI_LICENSING_V0`   Provision license tiers for AI agents

  `ai_governance::WF_AUTO_RECLAIM_V0`             Automatically reclaim expired or inactive licenses

  `ai_governance::WF_DENY_PROVISION_V0`           Explicitly deny provisioning requests
  ----------------------------------------------------------------------------------------------------

  -------------------------------------------------------------------------
  Actor                        Role
  ---------------------------- --------------------------------------------
  `AC_AGENT_V0`                AI agent requesting governed action

  `AC_EMPLOYEE_V0`             Human employee initiating provisioning

  `AC_ENTERPRISE_RUNTIME_V0`   Enterprise runtime environment

  `AC_SYSTEM_GOVERNOR_V0`      Governance authority principal

  `AC_SYSTEM_V0`               Background system processes (auto-reclaim)
  -------------------------------------------------------------------------

**The Constraint:** The execution engine must not know it is governing AI. It routes nodes by prefix, dispatches capabilities by pipeline, records traces by schema. The domain semantics --- license tiers, tool surfaces, parameter constraints --- live entirely in governance artifacts. The engine is blind to meaning. The governance artifacts carry all authority.

**Why this domain:** AI agent governance is among the hardest enterprise problems in production today. Agents propose actions. Those actions must be bounded --- not by hope, not by prompt engineering, not by model selection, but by structural authority that is declared, versioned, and traceable. If PGS can govern agentic AI without engine modification, it can govern anything.

This chapter is not about AI features. It is about structural authority.

## 14.2 --- From Business Thesis to Domain Specification (Act 0)

### The Business Problem

The business thesis is stated in one sentence:

> AI agents propose actions on behalf of users. Those actions must be mediated through declared authority before execution.

The business requirements elaborate this into five structural concerns:

1.  **Closed Tool Surface.** An agent may only invoke tools that are explicitly declared. There is no wildcard. There is no fallback. An undeclared tool is structurally unreachable.

2.  **License-Tier Authority Binding.** Each user holds a license tier (none, standard, enterprise). Each tier grants access to a specific set of tools. A standard-tier user cannot invoke premium tools --- not because the agent is told "no," but because the governance pipeline structurally excludes the tool from the allowed set.

3.  **Parameter-Bound Execution.** Even when a tool is authorized, its parameters are constrained. A standard-tier user can provision licenses --- but not more than 100. The constraint is declared in governance, not enforced in application code.

4.  **Symmetric Audit.** Every governance decision --- authorization or denial --- produces an append-only audit record. There is no "silent deny." The audit trail is symmetric: the same persistence mechanism records both outcomes.

5.  **No Engine Modification.** The governance domain must compose with existing domains (blockchain, ai_licensing) without changing the execution engine, the builder, the trace machinery, or any prior domain's artifacts.

### Translating Business Requirements to Specification

The architect translates these five concerns into PGS structural decisions. This is Act 0 --- the phase that is knowledge-dependent and human-guided.

**Concern 1 (Closed Tool Surface)** becomes a capability contract --- CC_CHECK_TOOL_DECLARED_V0 --- that uses CT_PURE_VALIDATE_SET_MEMBERSHIP_V0 to verify the requested tool against a constant allowed set declared in the CC's bindings. The allowed set is governance data, not code.

**Concern 2 (License-Tier Authority)** becomes two capability contracts in sequence --- CC_RESOLVE_LICENSE_TIER_V0 reads the user's license facts, then CC_BIND_LICENSE_TO_TOOL_SURFACE_V0 maps the tier to an allowed tool set and validates the request. The tier-to-tool mapping is a constant declared in the CC's bindings --- a lookup table governed as data.

**Concern 3 (Parameter Constraints)** becomes CC_VALIDATE_TOOL_PARAMETERS_V0 --- a two-step pipeline that looks up per-tool parameter rules, then validates the request's parameters against those rules. The rules are declared in the CC's bindings. The validation atom (CT_PURE_VALIDATE_PARAMETER_RULES_V0) is generic --- it knows nothing about licenses or tools. It evaluates rules against parameters.

**Concern 4 (Symmetric Audit)** becomes two capability contracts --- CC_RECORD_GOVERNED_ACTION_V0 for authorization and CC_RECORD_DENIED_ACTION_V0 for denial. Both use the same persistence stores: CS_GOVERNANCE_ACTIONS_V0 (registry) and CS_GOVERNANCE_AUDIT_V0 (append-only log). Every workflow exit path routes through one of these contracts before reaching an EXIT node.

**Concern 5 (No Engine Modification)** is not a contract --- it is a structural constraint on the specification itself. The spec must compose using existing execution primitives. Any new CT atoms must be domain-agnostic and placed in `reusable/`.

### The Specification Output

The domain specification (domain_genesis_v0.md) declares:

  ----------------------------------------------------------------------------------------------------------------------------------------------------------
  Category                      Count                Items
  ----------------------------- -------------------- -------------------------------------------------------------------------------------------------------
  Workflow                      1                    WF_GOVERN_AGENT_ACTION_V0

  Intent                        1                    IN_AGENT_ACTION_REQUESTED_V0

  Capability Contracts          7                    Normalize, Check Tool, Resolve License, Bind License, Validate Params, Record Governed, Record Denied

  Actors                        3                    AC_AGENT_V0, AC_SYSTEM_GOVERNOR_V0, AC_ENTERPRISE_RUNTIME_V0

  Events                        2                    EV_AGENT_ACTION_AUTHORIZED_V0, EV_AGENT_ACTION_DENIED_V0

  Runtime Bindings              1                    RB_AGENT_GOVERNANCE_BINDINGS_V0

  New CT Atoms                  3                    CT_PURE_VALIDATE_SET_MEMBERSHIP_V0, CT_PURE_LOOKUP_V0, CT_PURE_VALIDATE_PARAMETER_RULES_V0

  Persistence Stores            3                    CS_LICENSE_FACTS_V0, CS_GOVERNANCE_ACTIONS_V0, CS_GOVERNANCE_AUDIT_V0

  Test Scenarios                7                    2 happy paths, 5 denial paths

  Domain Invariants             6                    I-A1 through I-A6
  ----------------------------------------------------------------------------------------------------------------------------------------------------------

**Total governance artifacts:** 15

The specification also declares six domain invariants with enforcement mapping:

  ------------------------------------------------------------------------------------------------------------------
  Invariant                        Enforced By
  -------------------------------- ---------------------------------------------------------------------------------
  I-A1 No Ambient Authority        Single normalized intent; no direct tool invocation

  I-A2 Closed Tool Surface         CC_CHECK_TOOL_DECLARED_V0 with constant allowed_set

  I-A3 License-Bound Authority     CC_BIND_LICENSE_TO_TOOL_SURFACE_V0 with tier→tools mapping

  I-A4 Parameter-Bound Execution   CC_VALIDATE_TOOL_PARAMETERS_V0 with per-tool rule sets

  I-A5 Domain Isolation            CS_LICENSE_FACTS_V0 is READ-ONLY; no cross-domain mutation

  I-A6 Deterministic Trace         Symmetric audit via CC_RECORD_GOVERNED_ACTION_V0 and CC_RECORD_DENIED_ACTION_V0
  ------------------------------------------------------------------------------------------------------------------

**Gate passed:** The specification was reviewed and approved. Every workflow path is traceable from intent to exit. Every CC pipeline is fully specified with step-level input/output bindings. Every denial path terminates in an audit record before reaching EXIT. The specification is structurally sufficient for mechanical construction (Invariant I-SPEC1).

**Analysis:**

The specification concentrates all design decisions into a single reviewable artifact. The architect decided: - What tools are declared (three: READ_RECORD, PROVISION_STANDARD_LICENSE, PROVISION_PREMIUM_LICENSE) - What tiers map to what tools (a three-row lookup table) - What parameter constraints apply per tool (declared rule sets) - How denial paths route (through CC_RECORD_DENIED_ACTION_V0 with constant denial_reason per path)

None of these decisions will be made during Acts I--VII. The implementor translates --- not designs.

## 14.3 --- Domain Construction: Act I Through Act VII

### Act I --- Structure

**Action:** Register the domain in the FQDN tree and update environment facts.

FQDN tree entry:

    - package: agent_governance
      role: domain_pack
      authority: delegated
      build_order: 7
      physical_root: ./agent_governance
      contains:
        - governance
        - protocol
        - testbed
      registries:
        - path: agent_governance/governance/registry
          artifact_types:
            - capability_contracts
            - intents
            - workflows
            - events
            - actors
            - runtime_bindings
      depends_on:
        - governance
        - reusable

Environment facts update:

    {
      "module_data_roots": {
        "agent_governance": "agent_governance/testbed/outputs"
      },
      "workflow_to_module": {
        "WF_GOVERN_AGENT_ACTION_V0": "agent_governance"
      }
    }

**Analysis:**

- `build_order: 7` --- built after governance (1), reusable (2), blockchain (4), ai_licensing (5), and book (6). The builder discovers and processes packages in this order.
- `depends_on: [governance, reusable]` --- the only permitted upstream references. No dependency on blockchain or ai_licensing. Horizontal domain-to-domain coupling is structurally prohibited (Chapter 12, Invariant I-C1).
- `role: domain_pack` --- this is a business domain, not shared substrate. The FQDN tree distinguishes governance packs (constitutional), reusable packs (shared substrate), and domain packs (business logic).

**Gate passed:** The builder discovers the domain at build_order 7. The directory scaffold exists: `agent_governance/governance/registry/`, `agent_governance/protocol/`, `agent_governance/testbed/`.

### Act II --- Govern

**Action:** Author the 15 governance artifacts. No implementations --- governance only.

The artifacts authored:

  -------------------------------------------------------------------------------------------------------------
  Type                 Code                                 Purpose
  -------------------- ------------------------------------ ---------------------------------------------------
  Actor                AC_AGENT_V0                          Probabilistic intent emitter --- proposes actions

  Actor                AC_SYSTEM_GOVERNOR_V0                Governance execution authority

  Actor                AC_ENTERPRISE_RUNTIME_V0             Isolated side-effect executor

  Intent               IN_AGENT_ACTION_REQUESTED_V0         Normalized entry point for all agent requests

  Event                EV_AGENT_ACTION_AUTHORIZED_V0        Emitted on authorization

  Event                EV_AGENT_ACTION_DENIED_V0            Emitted on denial

  CC                   CC_NORMALIZE_AGENT_REQUEST_V0        Validate schema, generate intent hash

  CC                   CC_CHECK_TOOL_DECLARED_V0            Verify tool in closed registry

  CC                   CC_RESOLVE_LICENSE_TIER_V0           Read license facts, validate active

  CC                   CC_BIND_LICENSE_TO_TOOL_SURFACE_V0   Map tier to tools, verify authorization

  CC                   CC_VALIDATE_TOOL_PARAMETERS_V0       Enforce parameter constraints

  CC                   CC_RECORD_GOVERNED_ACTION_V0         Record authorization + audit

  CC                   CC_RECORD_DENIED_ACTION_V0           Record denial + audit

  Workflow             WF_GOVERN_AGENT_ACTION_V0            DAG connecting all nodes

  RB                   RB_AGENT_GOVERNANCE_BINDINGS_V0      CS runtime declarations
  -------------------------------------------------------------------------------------------------------------

**Example 14.1 --- CC_CHECK_TOOL_DECLARED_V0 Machine Block**

This is the capability contract that enforces the closed tool surface --- Invariant I-A2:

    cc_code: CC_CHECK_TOOL_DECLARED_V0
    version: v0
    governed_by: CONSTITUTION_CAPABILITY_CONTRACTS_V0

    core:
      summary: Verify requested tool exists in closed tool registry

      inputs:
        tool_name:
          type: string
          required: true

      outputs:
        is_declared:
          type: boolean

      result_status_contract:
        allowed: [SUCCESS, VIOLATION]
        on_input_failure: VIOLATION

      pipeline:
        - CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

      bindings:
        CT_PURE_VALIDATE_SET_MEMBERSHIP_V0:
          inputs:
            value: $.inputs.tool_name
            allowed_set:
              - READ_RECORD
              - PROVISION_STANDARD_LICENSE
              - PROVISION_PREMIUM_LICENSE
          outputs:
            is_declared: $.capability_result.value.is_member
          on_result:
            SUCCESS: continue
            VIOLATION: exit

**Analysis:**

- The `allowed_set` is a constant declared in governance --- not in code. The three declared tools are the entire executable surface. Adding a tool requires a governance artifact change, a version increment, a rebuild, and a redeployment. There is no back door.
- The CT atom (`CT_PURE_VALIDATE_SET_MEMBERSHIP_V0`) knows nothing about tools. It checks whether a value is in a set. The domain semantics --- which tools are allowed --- live in the CC's binding data.
- `on_input_failure: VIOLATION` --- if the input cannot be resolved, the contract reports VIOLATION. No silent failure. No default.
- The `result_status_contract` declares exactly two outcomes: SUCCESS and VIOLATION. The workflow must route on both (enforced by the WF-CC link validator at Act IV).

**Example 14.2 --- CC_BIND_LICENSE_TO_TOOL_SURFACE_V0 Machine Block**

This contract demonstrates multi-step pipeline composition --- the tier-to-tool mapping that enforces Invariant I-A3:

    cc_code: CC_BIND_LICENSE_TO_TOOL_SURFACE_V0
    version: v0
    governed_by: CONSTITUTION_CAPABILITY_CONTRACTS_V0

    core:
      summary: Map license tier to allowed tool set and verify tool authorization

      inputs:
        tool_name:
          type: string
          required: true
        license_tier:
          type: string
          required: true

      outputs:
        allowed_tools:
          type: array
        is_authorized:
          type: boolean

      result_status_contract:
        allowed: [SUCCESS, VIOLATION]
        on_input_failure: VIOLATION

      pipeline:
        - CT_PURE_LOOKUP_V0
        - CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

      bindings:
        CT_PURE_LOOKUP_V0:
          inputs:
            key: $.inputs.license_tier
            map:
              none:
                - READ_RECORD
              standard:
                - READ_RECORD
                - PROVISION_STANDARD_LICENSE
              enterprise:
                - READ_RECORD
                - PROVISION_STANDARD_LICENSE
                - PROVISION_PREMIUM_LICENSE
          outputs:
            allowed_tools: $.capability_result.value.result
          on_result:
            SUCCESS: continue
            VIOLATION: exit

        CT_PURE_VALIDATE_SET_MEMBERSHIP_V0:
          inputs:
            value: $.inputs.tool_name
            allowed_set: $.results.CT_PURE_LOOKUP_V0.allowed_tools
          outputs:
            is_authorized: $.capability_result.value.is_member
            allowed_tools: $.results.CT_PURE_LOOKUP_V0.allowed_tools
          on_result:
            SUCCESS: continue
            VIOLATION: exit

**Analysis:**

- **Step 1** (CT_PURE_LOOKUP_V0): Maps `license_tier` to an array of allowed tools. The mapping is a constant declared in the CC binding --- `none` gets one tool, `standard` gets two, `enterprise` gets three. This is the complete authority surface for each tier.
- **Step 2** (CT_PURE_VALIDATE_SET_MEMBERSHIP_V0): Checks whether the requested `tool_name` is in the allowed set produced by Step 1. The cross-step binding `$.results.CT_PURE_LOOKUP_V0.allowed_tools` passes the lookup result to the membership check.
- **CC output forwarding:** The last step's output bindings explicitly forward `allowed_tools` from Step 1 via `$.results.CT_PURE_LOOKUP_V0.allowed_tools`. Without this forwarding, the workflow would not receive the allowed tools list --- only the `is_authorized` boolean from Step 2 (Chapter 13, Section 13.9.2).
- **The entire authority policy** --- which tiers get which tools --- is declared data in a governance artifact. Changing the policy requires editing this YAML, incrementing the version, and rebuilding. The CT atoms that execute the lookup and membership check are reusable and domain-blind.

**Example 14.3 --- CC_RECORD_GOVERNED_ACTION_V0 Machine Block (CT + CS Pipeline)**

This contract demonstrates a mixed pipeline --- a CT step followed by two CS steps --- that records the authorization decision:

    cc_code: CC_RECORD_GOVERNED_ACTION_V0
    version: v0
    governed_by: CONSTITUTION_CAPABILITY_CONTRACTS_V0

    core:
      summary: Record authorized governance decision and emit audit trail

      pipeline:
        - CT_PURE_GENERATE_ID_V0
        - CS_GOVERNANCE_ACTIONS_V0
        - CS_GOVERNANCE_AUDIT_V0

      bindings:
        CT_PURE_GENERATE_ID_V0:
          inputs:
            prefix: "AGOV"
            data:
              tool_name: $.inputs.tool_name
              requesting_user_id: $.inputs.requesting_user_id
              intent_hash: $.inputs.intent_hash
          outputs:
            action_id: $.capability_result.value
          on_result:
            SUCCESS: continue
            VIOLATION: exit

        CS_GOVERNANCE_ACTIONS_V0:
          op: REGISTER
          inputs:
            key: $.results.CT_PURE_GENERATE_ID_V0.action_id
            target_ref: $.inputs.tool_name
            metadata:
              requesting_user_id: $.inputs.requesting_user_id
              license_tier: $.inputs.license_tier
              parameters: $.inputs.parameters
              domain_context: $.inputs.domain_context
              intent_hash: $.inputs.intent_hash
              decision: "AUTHORIZED"
          outputs:
            result_status: $.capability_result.result_status
          on_result:
            SUCCESS: continue
            ALREADY_EXISTS: continue
            BACKEND_ERROR: exit

        CS_GOVERNANCE_AUDIT_V0:
          op: APPEND
          inputs:
            record:
              event_code: "EV_AGENT_ACTION_AUTHORIZED_V0"
              action_id: $.results.CT_PURE_GENERATE_ID_V0.action_id
              tool_name: $.inputs.tool_name
              requesting_user_id: $.inputs.requesting_user_id
              license_tier: $.inputs.license_tier
              parameters: $.inputs.parameters
              decision: "AUTHORIZED"
              timestamp: "{{timestamp}}"
          outputs:
            result_status: $.capability_result.result_status
            action_id: $.results.CT_PURE_GENERATE_ID_V0.action_id
          on_result:
            SUCCESS: continue
            VIOLATION: exit
            BACKEND_ERROR: exit

**Analysis:**

- **Three-step pipeline:** CT generates ID → CS registers action → CS appends audit. This is the mixed CT/CS pattern --- pure computation followed by side effects.
- **Output forwarding in action:** The last step (CS_GOVERNANCE_AUDIT_V0) explicitly forwards `action_id` from Step 1 via `$.results.CT_PURE_GENERATE_ID_V0.action_id`. Without this line, the workflow would receive only `result_status` --- the `action_id` would be silently lost at the CC boundary.
- **Binding grammar distinctions:** Step 1 (CT) uses `$.capability_result.value` for its output binding --- the CT result is wrapped. Steps 2 and 3 (CS) use `$.capability_result.result_status` --- the CS result is direct. This distinction is codified in Chapter 13, Section 13.9.3.
- **Nested dict binding:** The `metadata` field in Step 2 and the `record` field in Step 3 are nested dictionaries with expression bindings at each leaf. The resolver recursively resolves these --- a pattern that avoids the need for a dedicated "assemble record" CT atom.

**Gate passed:** 15 governance artifacts authored. All EXIT nodes explicit. All denial paths route through CC_RECORD_DENIED_ACTION_V0 before reaching EXIT. The denial audit wiring is symmetric --- every authorization produces an EV_AGENT_ACTION_AUTHORIZED_V0 record, every denial produces an EV_AGENT_ACTION_DENIED_V0 record.

### Act III --- Validate

**Action:** Constitutional conformance checking.

The builder's validation phase verified:

- All 15 governance artifacts conform to their constitutional schemas
- All `result_status` values (`SUCCESS`, `VIOLATION`, `NOT_FOUND`, `BACKEND_ERROR`, `ALREADY_EXISTS`) appear in the constitutional vocabulary
- All `node_type` values (`IN`, `CC`, `EXIT`) are recognized
- All governance fields (`version`, `governed_by`) are present
- Intent naming uses past-tense verb: `IN_AGENT_ACTION_REQUESTED_V0`

**Gate passed:** Zero ERROR findings. Zero FATAL findings. All artifacts constitutionally conformant.

### Act IV --- Compile

**Action:** Run the builder. Materialize governance artifacts into execution-ready protocol artifacts.

    [builder] Discovery: 7 packages, 136 artifacts (133 existing + 3 new CTs)
    [builder] Validation: 136 artifacts, 0 errors, 0 warnings
    [builder] Materialized: 136 artifacts to protocol/artifacts/
    [builder] BUILD SUCCEEDED

The builder enforced:

- **Code-filename matching:** `CC_CHECK_TOOL_DECLARED_V0` matches `CC_CHECK_TOOL_DECLARED_V0.md`
- **Referential integrity:** Every CC_ referenced in the workflow exists as a materialized artifact. Every CT_ referenced in a CC pipeline has a registered implementation.
- **WF-CC link validation:** The workflow routes on every result_status declared by each CC. No silent drops. CC_CHECK_TOOL_DECLARED_V0 declares `[SUCCESS, VIOLATION]` --- the workflow handles both.

**Critical observation:** The builder materialized 136 artifacts total --- 133 existing from prior domains plus 3 new CT governance specs from `reusable/`. The 15 agent_governance artifacts were new. No existing artifact was modified. This is append-only vocabulary evolution (Chapter 12).

**Gate passed:** All artifacts materialized with content hashes. Build manifest updated.

### Act V --- Bind

**Action:** Resolve runtime bindings. Create the three new CT atoms. Unit test them.

**Runtime Binding --- RB_AGENT_GOVERNANCE_BINDINGS_V0:**

    rb_code: RB_AGENT_GOVERNANCE_BINDINGS_V0
    version: v0
    governed_by: CONSTITUTION_RUNTIME_BINDINGS_V0

    parameters:
      - module_data_root

    core:
      summary: Runtime binding of agent governance capability side effects

      bindings:
        CS_LICENSE_FACTS_V0:
          host: MutableJsonRuntime
          policy:
            path: "{{module_data_root}}/license_facts.json"
            strict: true

        CS_GOVERNANCE_ACTIONS_V0:
          host: RegistryRuntime
          policy:
            path: "{{module_data_root}}/governance_actions.json"
            strict: true

        CS_GOVERNANCE_AUDIT_V0:
          host: AppendOnlyJsonlRuntime
          policy:
            path: "{{module_data_root}}/governance_audit.jsonl"
            strict: true

**Analysis:**

- Three CS bindings, three host classes --- one for each persistence pattern:
  - `MutableJsonRuntime` for license facts (READ-ONLY in this domain)
  - `RegistryRuntime` for governance action registration (key-value with uniqueness)
  - `AppendOnlyJsonlRuntime` for audit records (immutable append)
- `{{module_data_root}}` resolves to `agent_governance/testbed/outputs` via env_facts. Each domain's data is structurally isolated.
- CS_LICENSE_FACTS_V0 is READ-ONLY. The governance artifact does not enforce this --- the builder does not check operation permissions. The enforcement is structural: no CC pipeline declares a WRITE operation against this store. The specification's Invariant I-A5 is enforced by omission --- the write path does not exist.

**New CT Atoms:**

Three domain-agnostic atoms were implemented in `reusable/capability_transforms/atoms/`:

**Example 14.4 --- CT_PURE_VALIDATE_SET_MEMBERSHIP_V0**

    """
    CT_PURE_VALIDATE_SET_MEMBERSHIP_V0

    Pure Capability Transform (Atom)

    Purpose:
        Validate that a value is a member of a declared set.
    """

    from typing import Dict, Any
    from execution.machine.transforms.ct_executor import CTExecutionError

    def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        if "value" not in inputs:
            raise CTExecutionError(
                "CT_PURE_VALIDATE_SET_MEMBERSHIP_V0: missing required input 'value'"
            )
        if "allowed_set" not in inputs:
            raise CTExecutionError(
                "CT_PURE_VALIDATE_SET_MEMBERSHIP_V0: missing required input 'allowed_set'"
            )

        value = inputs["value"]
        allowed_set = inputs["allowed_set"]

        if not isinstance(allowed_set, list):
            raise CTExecutionError(
                f"CT_PURE_VALIDATE_SET_MEMBERSHIP_V0: allowed_set must be array, "
                f"got {type(allowed_set).__name__}"
            )

        is_member = value in allowed_set

        if not is_member:
            raise CTExecutionError(
                f"CT_PURE_VALIDATE_SET_MEMBERSHIP_V0: value '{value}' not in allowed set"
            )

        return {
            "result_status": "SUCCESS",
            "is_member": True,
        }

**Analysis:**

- **Domain-blind.** The atom knows nothing about tools, licenses, or agents. It checks set membership. The domain semantics --- which values are in which sets --- are declared in CC bindings, not in this code.
- **Exception-based VIOLATION signaling.** When the value is not in the set, the atom throws `CTExecutionError`. The engine's `_execute_ct` wrapper catches this and maps it to the `on_failure` branch (Chapter 13, Section 13.9.1). The atom never returns `{"result_status": "VIOLATION"}`.
- **Reusable across domains.** This atom can be used by any domain that needs set membership validation --- compliance rule checking, permission verification, category validation. It is placed in `reusable/`, not in `agent_governance/`.

**Atom Unit Testing (Layer 1):**

24 unit tests were written for the three new atoms, verifying: - Correct return shape on success - `CTExecutionError` raised on violation - Missing input handling - Type validation (array required for sets, object required for maps) - Edge cases (empty set, empty map, null parameters)

All 24 tests passed before proceeding to Act VI.

**Gate passed:** All CT atoms registered. All CS runtimes resolve to closed registry entries. Atom unit tests passing.

### Act VI --- Execute

**Action:** Author test payloads and execute all seven scenarios.

This is where the governance pipeline meets real data. The specification declared seven test scenarios --- two happy paths and five denial paths. Each scenario exercises a different path through the workflow DAG.

The workflow is executed via:

    python transport/command_line/cli_adapter.py run \
      --wf WF_GOVERN_AGENT_ACTION_V0 \
      --rb RB_AGENT_GOVERNANCE_BINDINGS_V0 \
      --payload agent_governance/testbed/test_payloads/<scenario>.json

The full execution results are presented in Section 14.5 (Execution Scenarios). This section documents the five authoring defects identified during Act VI and how each was corrected.

### Execution Contract Enforcement

Act VI is where governance artifacts meet runtime enforcement.

Seven scenarios were authored. The workflow was executed against real payloads. The engine behaved deterministically in every case. Where failures occurred, they surfaced immediately at declared enforcement boundaries.

Five authoring defects were identified and corrected before all seven scenarios passed. None were engine defects. None were race conditions. None were edge cases. Each was a misalignment between governance artifacts and the execution contract defined in Chapter 13.

The system did not misbehave. It enforced its rules.

**Defect 1 --- CT Governance Shape Misalignment**

*Symptom:* All three newly authored CT atoms received empty input dictionaries and immediately raised `CTExecutionError` for missing required inputs.

*Observed behavior:* Despite correct bindings in CC pipelines, the CT atoms were invoked with `{}` as their input argument.

*Root Cause:* The three new CT governance `.md` Machine blocks declared `inputs` nested under `core:` --- following the Capability Contract template. However, the `ct_ir_loader` reads `inputs`, `outputs`, and `implementation` from the top level of a CT artifact. The governance template used for CTs diverged from the loader's contract. This was not a runtime failure. It was a specification--loader contract violation.

*Violated Rule:* Chapter 13, Section 13.9.5 --- *CT governance Machine block shape (top-level inputs, not nested under core:).*

*Fix:* Restructured all three CT governance Machine blocks to declare `inputs:`, `outputs:`, and `implementation:` at the top level, matching existing CT artifacts.

*Architectural Meaning:* The engine strictly enforces artifact shape. If the governance artifact does not conform to the loader's contract, the transform receives no inputs. The failure was deterministic and immediate. This confirms: artifact shape is part of the execution contract.

**Defect 2 --- Incorrect VIOLATION Signaling in CT Atoms**

*Symptom:* CT atoms returned `{"result_status": "VIOLATION"}` when validation failed. The workflow treated these as successful steps and continued execution incorrectly.

*Observed behavior:* A failed validation did not route to the VIOLATION branch in the workflow DAG.

*Root Cause:* The execution engine's `_execute_ct` wrapper sets VIOLATION status only when a `CTExecutionError` is raised. Returning a dictionary with `"result_status": "VIOLATION"` does not signal failure --- it is treated as a successful CT execution that happened to contain that field. The atom violated the CT exception signaling doctrine.

*Violated Rule:* Chapter 13, Section 13.9.1 --- *CT exception signaling rule: throw CTExecutionError, do not return result_status.*

*Fix:* Modified all three CT atoms to `raise CTExecutionError(...)` when validation fails. Removed any manual `"result_status": "VIOLATION"` returns.

*Architectural Meaning:* CT atoms are pure computation. They do not declare workflow state transitions. VIOLATION is not data --- it is structural control flow. Only the engine may set it. The engine enforced this strictly. The misalignment was exposed immediately. This confirms: structural state transitions are centralized. Capability transforms cannot self-assign workflow outcome.

**Defect 3 --- Invalid Cross-Step Binding Grammar**

*Symptom:* Several CC bindings failed to resolve prior step outputs. Bindings used expressions like `$.allowed_tools` instead of `$.results.CT_PURE_LOOKUP_V0.allowed_tools`.

*Observed behavior:* The resolver failed to find referenced values. Downstream CT atoms received incorrect inputs.

*Root Cause:* The binding grammar requires explicit reference to prior step outputs using `$.results.STEP_NAME.field`. Bare `$.field` is invalid unless referencing current inputs or payload. This was not a resolver defect. It was incorrect binding syntax.

*Violated Rule:* Chapter 13, Section 13.9.3 --- *Binding grammar reference card.*

*Fix:* Updated five CC bindings to use the fully qualified syntax: `$.results.CT_PURE_LOOKUP_V0.allowed_tools`.

*Architectural Meaning:* Binding resolution is deterministic and strict. There is no implicit step-scoped variable leakage. This confirms: data flow between pipeline steps must be explicit. Implicit scope does not exist.

**Defect 4 --- Incorrect Payload Mutation Model Assumption**

*Symptom:* A workflow node attempted to access `$.payload.context.license_tier`. This field did not exist at runtime.

*Observed behavior:* Binding resolution failed during execution of downstream nodes.

*Root Cause:* The payload mutation model was misunderstood. The engine merges CC outputs directly into the flat payload using `ctx.update_payload(result)`. There is no nested `context` wrapper. The correct reference was `$.payload.license_tier`.

*Violated Rule:* Chapter 13, Section 13.9.4 --- *Payload mutation semantics (flat accumulator, no context wrapper).*

*Fix:* Updated binding expressions to reference the flat payload structure.

*Architectural Meaning:* Payload structure is part of the execution contract. The accumulator model is explicit and deterministic. This confirms: there is no hidden execution context. All state mutation is flat and traceable.

**Defect 5 --- CC Output Forwarding Omission**

*Symptom:* `action_id` generated in Step 1 of CC_RECORD_GOVERNED_ACTION_V0 was not available to the workflow after the CC completed.

*Observed behavior:* Downstream nodes did not receive `action_id`.

*Root Cause:* Only the final pipeline step's resolved output bindings become the CC result. Prior step outputs do not automatically propagate. The final CS step did not explicitly forward `action_id: $.results.CT_PURE_GENERATE_ID_V0.action_id`. As a result, the value was lost at the CC boundary.

*Violated Rule:* Chapter 13, Section 13.9.2 --- *CC output forwarding rule (only last step's outputs become CC result).*

*Fix:* Added explicit forwarding of `action_id` in the final pipeline step's output bindings.

*Architectural Meaning:* CC boundaries are strict. Data does not "leak forward." The final step defines the contract surface of the capability. This confirms: capability contracts expose only what they explicitly declare. Nothing more.

**What These Enforcement Events Prove**

None of these defects were: - Race conditions - Timing anomalies - Cross-domain leakage - Authority bypass - Hidden engine behavior - Trace inconsistencies

All were violations of explicitly documented execution semantics introduced in Chapter 13.

The engine enforced: - Artifact shape - Exception-based signaling - Binding grammar strictness - Payload mutation rules - CC output forwarding discipline

Each defect was surfaced deterministically at a declared enforcement boundary. The runtime did not guess. It did not compensate. It did not silently recover. It rejected misaligned artifacts.

This is not debugging. This is contract enforcement.

**Architectural Conclusion of Act VI**

PGS-OB does not produce edge cases. It produces explicit execution contract violations when governance artifacts deviate from declared doctrine. Every defect identified during Act VI reinforced: - CT purity - Explicit data flow - Strict binding grammar - Deterministic payload mutation - Explicit capability boundaries

The engine behaved exactly as specified. Once the artifacts aligned with the declared execution contract, all seven scenarios executed deterministically, with identical traces across repeated runs.

Act VI did not reveal instability. It validated enforcement.

### Act VII --- Diagnose & Stabilize

**Action:** Verify trace integrity. Confirm CS mutation outcomes. Integrate into regression suite.

**Trace Verification:**

Every scenario's execution trace was verified for structural completeness: - Every node that started also ended - Every exit has a reason code - Every CS mutation produced the expected state change - Deterministic replay: same payload → same trace → same outputs

**CS State Verification:**

After executing all seven scenarios: - `governance_actions.json` contains two registered actions (from the two happy paths) - `governance_audit.jsonl` contains seven records --- two EV_AGENT_ACTION_AUTHORIZED_V0 and five EV_AGENT_ACTION_DENIED_V0 - `license_facts.json` is unchanged --- no writes occurred (Invariant I-A5 confirmed)

**Regression Integration:**

The domain's test suite was added to `pgs_compiler/tooling/testbed/run_all_tests.sh`. Running the full regression suite confirms: - All agent_governance scenarios pass - All blockchain scenarios pass - All ai_licensing scenarios pass - Zero cross-domain breakage

**Gate passed:** The domain is locked. All seven scenarios execute deterministically. Same payload plus same artifacts produces the same trace.

## 14.4 --- The Workflow DAG: Governing Agent Action

The complete workflow DAG for WF_GOVERN_AGENT_ACTION_V0:

                        IN_AGENT_ACTION_REQUESTED_V0
                             │           │
                            ACK        NACK
                             │           │
                             ▼           ▼
                CC_NORMALIZE_AGENT_REQUEST_V0    EXIT_REJECTED
                      │            │
                    SUCCESS     VIOLATION
                      │            │
                      ▼            ▼
             CC_CHECK_TOOL_DECLARED_V0      EXIT_ERROR
                  │            │
                SUCCESS     VIOLATION
                  │            │
                  ▼            ▼
          CC_RESOLVE_LICENSE_TIER_V0    CC_AUDIT_UNDECLARED_TOOL
             │      │      │     │              │
           SUCC  NOT_FND  VIOL  BE_ERR         SUCC
             │      │      │     │              │
             ▼      ▼──────▼     ▼              ▼
      CC_BIND_LICENSE_V0  CC_AUDIT_UNAUTH_ACTOR  EXIT_UNDECLARED_TOOL
          │          │           │         EXIT_ERROR
        SUCCESS   VIOLATION     SUCC
          │          │           │
          ▼          ▼           ▼
    CC_VALIDATE_TOOL_PARAMS_V0  CC_AUDIT_UNAUTH_TOOL  EXIT_UNAUTHORIZED_ACTOR
          │          │              │
        SUCCESS   VIOLATION        SUCC
          │          │              │
          ▼          ▼              ▼
    CC_RECORD_GOVERNED_ACTION_V0  CC_AUDIT_PARAM_VIOL  EXIT_UNAUTHORIZED_TOOL
          │                           │
        SUCCESS                     SUCC
          │                           │
          ▼                           ▼
      EXIT_SUCCESS             EXIT_PARAMETER_VIOLATION

**Key structural properties:**

1.  **Single entry point.** All agent requests enter through IN_AGENT_ACTION_REQUESTED_V0. There is no alternative entry. The intent normalizes the request before any governance evaluation begins.

2.  **Five governance gates.** Normalize → Check Tool → Resolve License → Bind License → Validate Parameters. Each gate produces SUCCESS (continue) or VIOLATION/NOT_FOUND (deny). The gates are sequential --- each depends on the output of its predecessor.

3.  **Four denial paths.** Each denial routes through a dedicated audit node (CC_AUDIT_UNDECLARED_TOOL, CC_AUDIT_UNAUTHORIZED_ACTOR, CC_AUDIT_UNAUTHORIZED_TOOL, CC_AUDIT_PARAMETER_VIOLATION) before reaching an EXIT node. All four audit nodes use the same capability contract --- CC_RECORD_DENIED_ACTION_V0 --- with a different constant `denial_reason` per instance.

4.  **Symmetric audit.** Authorization exits through CC_RECORD_GOVERNED_ACTION_V0. Denial exits through CC_RECORD_DENIED_ACTION_V0. Both write to CS_GOVERNANCE_AUDIT_V0. Every governance decision is recorded before the workflow terminates.

5.  **No silent paths.** Every node routes on every declared result_status. There are no unhandled branches. The WF-CC link validator enforced this at Act IV.

### Cross-Step Data Flow

The workflow payload accumulates data as nodes execute:

    Initial payload:
      tool_name, parameters, requesting_user_id, domain_context

    After CC_NORMALIZE_AGENT_REQUEST_V0:
      + intent_hash

    After CC_RESOLVE_LICENSE_TIER_V0:
      + license_tier, license_status, org_unit, is_active

    After CC_BIND_LICENSE_TO_TOOL_SURFACE_V0:
      + allowed_tools, is_authorized

    After CC_RECORD_GOVERNED_ACTION_V0:
      + action_id, result_status

Each CC's outputs are merged into the flat payload via `ctx.update_payload(result)`. Subsequent nodes access prior results via `$.payload.field`. The payload is a flat, mutable accumulator --- not a nested object (Chapter 13, Section 13.9.4).

## 14.5 --- Execution Scenarios

Seven scenarios validate the governance pipeline --- two happy paths and five denial paths. Each scenario shows the entry payload, the execution path, and the outcome.

### Scenario 1 --- Standard License, Standard Tool (Happy Path)

**Payload:**

    {
      "tool_name": "PROVISION_STANDARD_LICENSE",
      "parameters": { "tier": "standard", "quantity": 50 },
      "requesting_user_id": "EMP_STD_001",
      "domain_context": "ai_licensing",
      "request_id": "REQ_TEST_001"
    }

**Execution path:**

    IN_AGENT_ACTION_REQUESTED_V0  → ACK
    CC_NORMALIZE_AGENT_REQUEST_V0 → SUCCESS  (intent_hash generated)
    CC_CHECK_TOOL_DECLARED_V0     → SUCCESS  (PROVISION_STANDARD_LICENSE ∈ declared set)
    CC_RESOLVE_LICENSE_TIER_V0    → SUCCESS  (EMP_STD_001 → tier=standard, status=active)
    CC_BIND_LICENSE_TO_TOOL_SURFACE_V0 → SUCCESS  (standard → [READ_RECORD, PROVISION_STANDARD_LICENSE])
    CC_VALIDATE_TOOL_PARAMETERS_V0    → SUCCESS  (tier=standard ✓, quantity=50 ≤ 100 ✓)
    CC_RECORD_GOVERNED_ACTION_V0      → SUCCESS  (action registered, audit appended)
    EXIT_SUCCESS                       → emit EV_AGENT_ACTION_AUTHORIZED_V0

**What this proves:** A standard-tier user requesting a standard-tier tool with valid parameters passes all five governance gates. The action is authorized, registered, and audited. The trace records every node traversal with timing.

### Scenario 2 --- Enterprise License, Premium Tool (Happy Path)

**Payload:**

    {
      "tool_name": "PROVISION_PREMIUM_LICENSE",
      "parameters": { "tier": "premium", "quantity": 25 },
      "requesting_user_id": "EMP_ENT_001",
      "domain_context": "ai_licensing",
      "request_id": "REQ_TEST_004"
    }

**Execution path:**

    IN_AGENT_ACTION_REQUESTED_V0  → ACK
    CC_NORMALIZE_AGENT_REQUEST_V0 → SUCCESS
    CC_CHECK_TOOL_DECLARED_V0     → SUCCESS  (PROVISION_PREMIUM_LICENSE ∈ declared set)
    CC_RESOLVE_LICENSE_TIER_V0    → SUCCESS  (EMP_ENT_001 → tier=enterprise, status=active)
    CC_BIND_LICENSE_TO_TOOL_SURFACE_V0 → SUCCESS  (enterprise → [READ_RECORD, PROV_STD, PROV_PREMIUM])
    CC_VALIDATE_TOOL_PARAMETERS_V0    → SUCCESS  (tier=premium ✓, quantity=25 ≤ 50 ✓)
    CC_RECORD_GOVERNED_ACTION_V0      → SUCCESS
    EXIT_SUCCESS                       → emit EV_AGENT_ACTION_AUTHORIZED_V0

**What this proves:** Enterprise-tier users access the full tool surface. The tier-to-tool mapping is declarative --- the enterprise tier's allowed set includes all three tools. Parameter constraints are per-tool --- premium licenses allow up to 50, not 100.

### Scenario 3 --- Undeclared Tool (Denial)

**Payload:**

    {
      "tool_name": "DELETE_DATABASE",
      "parameters": {},
      "requesting_user_id": "EMP_STD_001",
      "domain_context": "ai_licensing",
      "request_id": "REQ_TEST_005"
    }

**Execution path:**

    IN_AGENT_ACTION_REQUESTED_V0  → ACK
    CC_NORMALIZE_AGENT_REQUEST_V0 → SUCCESS
    CC_CHECK_TOOL_DECLARED_V0     → VIOLATION  (DELETE_DATABASE ∉ declared set)
    CC_AUDIT_UNDECLARED_TOOL       → SUCCESS   (denial_reason: UNDECLARED_TOOL recorded)
    EXIT_UNDECLARED_TOOL           → emit EV_AGENT_ACTION_DENIED_V0

**What this proves:** The closed tool surface is absolute. `DELETE_DATABASE` does not appear in the allowed set `[READ_RECORD, PROVISION_STANDARD_LICENSE, PROVISION_PREMIUM_LICENSE]`. The CT atom throws `CTExecutionError`. The engine maps this to VIOLATION. The workflow routes to the denial audit path. The denial is recorded before exit. The agent never gets close to executing the tool --- the governance pipeline rejects it at the second gate.

### Scenario 4 --- No License (Denial)

**Payload:**

    {
      "tool_name": "PROVISION_STANDARD_LICENSE",
      "parameters": { "tier": "standard", "quantity": 50 },
      "requesting_user_id": "EMP_NONE_001",
      "domain_context": "ai_licensing",
      "request_id": "REQ_TEST_002"
    }

**Execution path:**

    IN_AGENT_ACTION_REQUESTED_V0  → ACK
    CC_NORMALIZE_AGENT_REQUEST_V0 → SUCCESS
    CC_CHECK_TOOL_DECLARED_V0     → SUCCESS  (PROVISION_STANDARD_LICENSE ∈ declared set)
    CC_RESOLVE_LICENSE_TIER_V0    → NOT_FOUND  (EMP_NONE_001 not in license_facts)
    CC_AUDIT_UNAUTHORIZED_ACTOR    → SUCCESS   (denial_reason: UNAUTHORIZED_ACTOR recorded)
    EXIT_UNAUTHORIZED_ACTOR        → emit EV_AGENT_ACTION_DENIED_V0

**What this proves:** The tool is declared but the user has no license record. The workflow routes on NOT_FOUND --- a distinct status from VIOLATION --- indicating absence rather than invalidity. Denial is audited before exit.

### Scenario 5 --- Standard Tier Requests Premium Tool (Denial)

**Payload:**

    {
      "tool_name": "PROVISION_PREMIUM_LICENSE",
      "parameters": { "tier": "premium", "quantity": 25 },
      "requesting_user_id": "EMP_STD_001",
      "domain_context": "ai_licensing",
      "request_id": "REQ_TEST_003"
    }

**Execution path:**

    IN_AGENT_ACTION_REQUESTED_V0  → ACK
    CC_NORMALIZE_AGENT_REQUEST_V0 → SUCCESS
    CC_CHECK_TOOL_DECLARED_V0     → SUCCESS  (PROVISION_PREMIUM_LICENSE ∈ declared set)
    CC_RESOLVE_LICENSE_TIER_V0    → SUCCESS  (EMP_STD_001 → tier=standard, status=active)
    CC_BIND_LICENSE_TO_TOOL_SURFACE_V0 → VIOLATION
        (standard → [READ_RECORD, PROVISION_STANDARD_LICENSE])
        (PROVISION_PREMIUM_LICENSE ∉ standard tier's allowed set)
    CC_AUDIT_UNAUTHORIZED_TOOL     → SUCCESS  (denial_reason: UNAUTHORIZED_TOOL recorded)
    EXIT_UNAUTHORIZED_TOOL         → emit EV_AGENT_ACTION_DENIED_V0

**What this proves:** Gates 2 and 3 pass --- the tool is declared and the user has a valid license. Gate 4 fails --- the standard tier's allowed set does not include PROVISION_PREMIUM_LICENSE. The tier-to-tool mapping is a governance constant, not a runtime decision. This is structural enforcement of Invariant I-A3 --- License-Bound Authority.

### Scenario 6 --- Parameter Violation (Denial)

**Payload:**

    {
      "tool_name": "PROVISION_STANDARD_LICENSE",
      "parameters": { "tier": "standard", "quantity": 200 },
      "requesting_user_id": "EMP_STD_001",
      "domain_context": "ai_licensing",
      "request_id": "REQ_TEST_006"
    }

**Execution path:**

    IN_AGENT_ACTION_REQUESTED_V0  → ACK
    CC_NORMALIZE_AGENT_REQUEST_V0 → SUCCESS
    CC_CHECK_TOOL_DECLARED_V0     → SUCCESS
    CC_RESOLVE_LICENSE_TIER_V0    → SUCCESS
    CC_BIND_LICENSE_TO_TOOL_SURFACE_V0 → SUCCESS
    CC_VALIDATE_TOOL_PARAMETERS_V0    → VIOLATION
        (quantity=200, rule: quantity ≤ 100 → FAILED)
    CC_AUDIT_PARAMETER_VIOLATION   → SUCCESS  (denial_reason: PARAMETER_VIOLATION recorded)
    EXIT_PARAMETER_VIOLATION       → emit EV_AGENT_ACTION_DENIED_V0

**What this proves:** The deepest governance gate --- four gates pass before the fifth rejects. PROVISION_STANDARD_LICENSE allows quantity up to 100; the request specifies 200. Parameter rules are declared in CC_VALIDATE_TOOL_PARAMETERS_V0's binding data, not in application code.

### Scenario 7 --- Shell Command Absent (Denial)

**Payload:**

    {
      "tool_name": "EXECUTE_SHELL_COMMAND",
      "parameters": { "command": "rm -rf /" },
      "requesting_user_id": "EMP_ENT_001",
      "domain_context": "system",
      "request_id": "REQ_TEST_007"
    }

**Execution path:**

    IN_AGENT_ACTION_REQUESTED_V0  → ACK
    CC_NORMALIZE_AGENT_REQUEST_V0 → SUCCESS
    CC_CHECK_TOOL_DECLARED_V0     → VIOLATION  (EXECUTE_SHELL_COMMAND ∉ declared set)
    CC_AUDIT_UNDECLARED_TOOL       → SUCCESS   (denial_reason: UNDECLARED_TOOL recorded)
    EXIT_UNDECLARED_TOOL           → emit EV_AGENT_ACTION_DENIED_V0

**What this proves:** This is the most important scenario. An enterprise-tier user --- the highest authority level --- requests a tool that does not exist in the declared tool surface. It does not matter that the user is enterprise-tier. It does not matter what the parameters contain. The tool is structurally absent. It was never declared. It cannot be invoked, authorized, or denied-with-exception. It is unreachable.

This is not a denial based on insufficient authority. This is a denial based on structural absence. `EXECUTE_SHELL_COMMAND` does not exist in the governance vocabulary. The closed tool surface (Invariant I-A2) is enforced before tier binding (Invariant I-A3) is even evaluated. The gate ordering matters --- undeclared tools are rejected before any authority check occurs.

## 14.6 --- Cross-Domain Composition

The agent governance domain consumes license facts from the ai_licensing domain. This is cross-domain composition --- and it demonstrates federation without coupling.

### The Pattern

CS_LICENSE_FACTS_V0 is a MutableJsonRuntime store pre-populated with license data:

    {
      "EMP_STD_001": {
        "license_status": "active",
        "license_tier": "standard",
        "org_unit": "engineering"
      },
      "EMP_ENT_001": {
        "license_status": "active",
        "license_tier": "enterprise",
        "org_unit": "engineering"
      }
    }

CC_RESOLVE_LICENSE_TIER_V0 reads this store via a CS READ operation. The operation is one-directional --- agent governance reads license facts but never writes them.

### What This Proves

- **No cross-domain mutation.** Agent governance does not modify ai_licensing state. The READ-ONLY constraint (Invariant I-A5) is enforced structurally --- no CC pipeline declares a WRITE operation against CS_LICENSE_FACTS_V0.
- **No ambient authority introduced.** The license facts are consumed as declared input. The workflow's CC_RESOLVE_LICENSE_TIER_V0 explicitly binds `requesting_user_id` to the CS READ key. There is no implicit data access.
- **No engine modification.** The execution engine does not know it is performing a cross-domain read. It dispatches a CS READ operation against a MutableJsonRuntime at a configured path. The path happens to contain data that originated from the licensing domain. The engine is blind to this provenance.

### The V1 Evolution Path

The specification notes that V0 uses pre-populated local data to simulate the cross-domain fact feed. The ideal pattern --- declared cross-domain CC invocation via a read-only CC in the licensing domain --- is deferred to V1. The structural boundary is already clean. The evolution is additive --- replacing a local data copy with a declared cross-domain read.

This cross-domain pattern ties directly to: - **Chapter 11 (Declarative Federation):** The FQDN tree declares `depends_on: [governance, reusable]` --- not `depends_on: ``[ai_licensing]`. The cross-domain data flow is explicit but structurally decoupled. - **Chapter 12 (Compositional Isolation):** Adding agent_governance did not modify ai_licensing's governance artifacts, protocol artifacts, or test suite.

## 14.7 --- Trace Examination

An abbreviated execution trace for Scenario 1 (Standard License, Standard Tool):

    execution_start  WF_GOVERN_AGENT_ACTION_V0  exec_001
      node_start     IN_AGENT_ACTION_REQUESTED_V0  intent
      node_end       IN_AGENT_ACTION_REQUESTED_V0  ACK  8ms
      node_start     CC_NORMALIZE_AGENT_REQUEST_V0  capability
        step_start   CT_PURE_GENERATE_ID_V0  SUCCESS
      node_end       CC_NORMALIZE_AGENT_REQUEST_V0  SUCCESS  15ms
      node_start     CC_CHECK_TOOL_DECLARED_V0  capability
        step_start   CT_PURE_VALIDATE_SET_MEMBERSHIP_V0  SUCCESS
      node_end       CC_CHECK_TOOL_DECLARED_V0  SUCCESS  6ms
      node_start     CC_RESOLVE_LICENSE_TIER_V0  capability
        step_start   CS_LICENSE_FACTS_V0  READ  SUCCESS
        step_start   CT_PURE_VALIDATE_SET_MEMBERSHIP_V0  SUCCESS
      node_end       CC_RESOLVE_LICENSE_TIER_V0  SUCCESS  12ms
      node_start     CC_BIND_LICENSE_TO_TOOL_SURFACE_V0  capability
        step_start   CT_PURE_LOOKUP_V0  SUCCESS
        step_start   CT_PURE_VALIDATE_SET_MEMBERSHIP_V0  SUCCESS
      node_end       CC_BIND_LICENSE_TO_TOOL_SURFACE_V0  SUCCESS  9ms
      node_start     CC_VALIDATE_TOOL_PARAMETERS_V0  capability
        step_start   CT_PURE_LOOKUP_V0  SUCCESS
        step_start   CT_PURE_VALIDATE_PARAMETER_RULES_V0  SUCCESS
      node_end       CC_VALIDATE_TOOL_PARAMETERS_V0  SUCCESS  11ms
      node_start     CC_RECORD_GOVERNED_ACTION_V0  capability
        step_start   CT_PURE_GENERATE_ID_V0  SUCCESS
        step_start   CS_GOVERNANCE_ACTIONS_V0  REGISTER  SUCCESS
        step_start   CS_GOVERNANCE_AUDIT_V0  APPEND  SUCCESS
      node_end       CC_RECORD_GOVERNED_ACTION_V0  SUCCESS  18ms
      node_start     EXIT_SUCCESS  exit
    workflow_complete  SUCCESS  exit_reason=COMPLETED  84ms

**What the trace proves:**

1.  **Complete node coverage.** Every node that started also ended. Every result_status is recorded. The trace is structurally complete.

2.  **Capability invocation sequence.** The seven CC nodes executed in DAG order. Each CC's pipeline steps are visible --- CT and CS operations with their individual result statuses. The pipeline is not a black box.

3.  **Authority boundary verification.** CS_LICENSE_FACTS_V0 was accessed via READ --- no WRITE, DELETE, or other mutation. CS_GOVERNANCE_ACTIONS_V0 was accessed via REGISTER. CS_GOVERNANCE_AUDIT_V0 was accessed via APPEND. The operation types are traceable.

4.  **Structural proof of non-execution.** Only declared nodes appear in the trace. There is no evidence of undeclared capability invocation, no untraced side effect, no hidden computation. What is not in the trace did not execute. This is the trace's negative proof --- the absence of evidence is evidence of absence.

An abbreviated trace for Scenario 3 (Undeclared Tool):

    execution_start  WF_GOVERN_AGENT_ACTION_V0  exec_003
      node_start     IN_AGENT_ACTION_REQUESTED_V0  intent
      node_end       IN_AGENT_ACTION_REQUESTED_V0  ACK  7ms
      node_start     CC_NORMALIZE_AGENT_REQUEST_V0  capability
      node_end       CC_NORMALIZE_AGENT_REQUEST_V0  SUCCESS  14ms
      node_start     CC_CHECK_TOOL_DECLARED_V0  capability
        step_start   CT_PURE_VALIDATE_SET_MEMBERSHIP_V0  VIOLATION
      node_end       CC_CHECK_TOOL_DECLARED_V0  VIOLATION  5ms
      node_start     CC_AUDIT_UNDECLARED_TOOL  capability
        step_start   CT_PURE_GENERATE_ID_V0  SUCCESS
        step_start   CS_GOVERNANCE_AUDIT_V0  APPEND  SUCCESS
      node_end       CC_AUDIT_UNDECLARED_TOOL  SUCCESS  16ms
      node_start     EXIT_UNDECLARED_TOOL  exit
    workflow_complete  SUCCESS  exit_reason=COMPLETED  47ms

**What this trace proves:** The denial path is fully traced. The VIOLATION at CC_CHECK_TOOL_DECLARED_V0 is recorded with the specific step that failed (CT_PURE_VALIDATE_SET_MEMBERSHIP_V0). The audit node fires and appends the denial record. The workflow exits cleanly --- `exit_reason=COMPLETED`, not `FAILED`. Denial is a governed outcome, not an error.

This proves Chapter 9 (Deterministic Traces) and Chapter 10 (Inverted Security) in practice.

## 14.8 --- What Did Not Change

This is the most architecturally significant section of this chapter.

When the agent_governance domain was merged into the system, the following did **not** change:

**Execution engine:** Zero modifications to the workflow executor, DAG builder, node router, capability contract pipeline, CC resolution logic, trace machinery, or federation logic.

**Builder:** Zero modifications to the builder's discovery, validation, materialization, or molecule compilation phases.

**Prior domains:** Zero modifications to blockchain governance artifacts, ai_licensing governance artifacts, or any prior domain's protocol artifacts.

**Prior test suites:** Zero modifications to existing test payloads or expected outcomes. All prior scenarios continue to pass.

**What did change:**

  -------------------------------------------------------------------------------------------------------------------------------------
  Changed                         What                                 Why
  ------------------------------- ------------------------------------ ----------------------------------------------------------------
  FQDN tree                       +1 package entry                     Domain registration (Act I)

  env_facts                       +1 data root, +4 workflow mappings   Module wiring (Act I)

  Actors                          +5 AC artifacts                      Agent, Employee, Enterprise Runtime, Governor, System (Act II)

  Workflows                       +4 WF artifacts                      Govern, Provision, Auto-reclaim, Deny (Act II)

  Runtime bindings                +2 RB artifacts                      CT/CS bindings for agent_governance + licensing (Act V)

  Reusable substrate              new CT atoms (code + governance)     Domain-agnostic transforms (Act V)

  Regression script               +1 domain in run_all_tests.sh        Test integration (Act VII)
  -------------------------------------------------------------------------------------------------------------------------------------

**The merge diff:**

    47 files changed, 3063 insertions(+), 19 deletions(-)

47 files --- all additions. The 19 deletions are in env_facts reformatting and the FQDN tree entry insertion point. No prior governance artifact was modified. No prior protocol artifact was regenerated with different content.

**What this proves:**

**I-C1 --- Compositional Isolation:** Agent governance is a consumer of the platform, not a contaminant of it. Adding the domain did not mutate any prior domain's governance, protocol artifacts, or test outcomes.

**I-F1 --- Declarative Federation:** The FQDN tree accepted the new domain entry. The builder discovered and processed it at build_order 7. All 136 artifacts (133 existing + 3 new CTs) materialized without conflict.

**I-S2 --- No Ambient Authority:** The new domain introduced no undeclared capabilities. Every CT atom is registered. Every CS binding resolves to a closed registry entry. Every CC pipeline uses declared CT and CS codes.

**Implicit Invariant --- Domain Addition Without Engine Mutation:** A full AI governance domain was added without changing the engine or prior domains. The platform accepted a completely new governance domain without requiring architectural surgery. The engine did not know it was governing AI. It simply executed declared authority.

This is the strongest possible proof of compositional power. Most systems require middleware patches, feature flags, special cases, or conditional branching in the engine to support new domains. PGS required none.

## 14.9 --- Structural Insight (Doctrine Moment)

This chapter proved something precise:

> AI actions can be structurally bounded by declared authority --- without the engine understanding what it is bounding.

The execution engine dispatched seven capability contracts across five governance gates. It resolved license tiers. It mapped tiers to tool surfaces. It validated parameter constraints. It recorded authorizations and denials in an append-only audit trail.

And the engine did not know any of this was happening.

It loaded a compiled DAG. It followed edges. It dispatched to capabilities by prefix. It recorded a trace. The semantic content --- license tiers, tool surfaces, parameter rules, denial reasons --- lived entirely in governance artifacts.

**This is not a feature of AI governance. This is a property of the architecture.**

Any domain that can be expressed as a sequence of governed capabilities with declared authority surfaces can be composed into PGS without engine modification. Agent governance proved it for a domain that is among the hardest in enterprise software today.

**The derived insight:**

> Governance domains compose without destabilizing substrate.

The evidence: - Zero engine changes for a 15-artifact, 7-CC, 5-denial-path domain - Zero cross-domain breakage across 136 total artifacts - Zero modification to prior test suites - Vocabulary extended append-only --- no retroactive changes - Regression suite extended, not altered

**Connection to prior chapters:**

  -----------------------------------------------------------------------------------------------------------------------------------
  Chapter       Invariant                            How This Chapter Proved It
  ------------- ------------------------------------ --------------------------------------------------------------------------------
  Ch10          I-S2 --- No Ambient Authority        No undeclared capability invoked in any scenario

  Ch11          I-F1 --- Declarative Federation      FQDN tree accepted domain; builder discovered at build_order 7

  Ch12          I-C1 --- Compositional Isolation     Zero cross-domain mutation; all prior tests pass

  Ch13          I-SPEC1 --- Structural Sufficiency   Specification referenced in every act; no design decisions during construction
  -----------------------------------------------------------------------------------------------------------------------------------

This domain is not a demo. It stress-tested: - Multi-stage CC pipelines (up to 3 steps) - Mixed CT/CS pipelines - Exception-based control flow - Cross-step binding semantics - CC output forwarding - Payload mutation across 7 nodes - Cross-domain data consumption - Symmetric audit (authorization + denial)

And the system held.

## 14.10 --- Boundary and Forward Pointer

This chapter proved that the construction method from Chapter 13 works on an enterprise-grade domain. Act 0 produced a specification that was referenced in every subsequent act. Acts I--VII executed mechanically against that specification. Five authoring defects were identified at Act VI --- each surfaced deterministically at a declared enforcement boundary. None were engine defects. The domain was stabilized and integrated without changing the core engine or any prior domain.

**What this chapter proved:** - AI actions can be structurally bounded --- not by hope, but by declared authority - Authority can be declared, versioned, and traced --- not inferred at runtime - Denial is first-class --- every denial path is governed, audited, and traceable - Governance composes --- new domains add to the platform without destabilizing it - The construction method works --- Act 0 through Act VII produced a verified domain

**What this chapter did not cover:** - AI reasoning internals --- how the agent decides which tool to request - Model selection --- which LLM drives the agent - Prompt engineering --- how the agent formulates requests - Infrastructure scaling --- horizontal deployment of the governance pipeline - Performance benchmarks --- latency and throughput characteristics

These are implementation concerns. They live below the governance boundary. PGS governs what the agent is allowed to do. It does not govern how the agent thinks.

**What comes next:** Chapter 15 examines enterprise integration patterns and multi-domain expansion --- how organizations adopt PGS across teams, how governance evolves across versions, and how the construction method scales to dozens of domains.

**Layer movement:** End-to-end construction and execution completed for a high-stakes governance domain. Moving to organizational patterns and enterprise adoption.

## 14.11 --- Review Questions

1.  **Why does the closed tool surface (Invariant I-A2) use a governance constant rather than a configuration file or database lookup?**

- *Because a governance constant is versioned, compiled, and traceable. Changing the allowed tool set requires a governance artifact change, a version increment, a builder run, and a redeployment. This makes the change auditable and deterministic. A configuration file or database lookup introduces runtime variability --- the tool surface could change between executions without a governance change, violating deterministic reconstructability (Chapter 9, Invariant I-G8). The tool surface is authority data --- it belongs in governance, not in configuration.*

2.  **In Scenario 7, why does the enterprise-tier user's request for EXECUTE_SHELL_COMMAND fail at gate 2 rather than gate 4?**

- *Because the governance gates execute in sequence, and gate 2 (closed tool surface) precedes gate 4 (license-tier binding). EXECUTE_SHELL_COMMAND is not in the declared tool set --- it is structurally absent, not merely unauthorized. The system does not evaluate whether the enterprise tier would have access to this tool because the tool does not exist in governance. This ordering is deliberate: structural absence is checked before authority evaluation. You cannot authorize what does not exist.*

3.  **Why does CC_RECORD_DENIED_ACTION_V0 appear four times in the workflow DAG with different node names?**

- *Because each denial path has a different constant denial_reason: UNDECLARED_TOOL, UNAUTHORIZED_ACTOR, UNAUTHORIZED_TOOL, PARAMETER_VIOLATION. The workflow instantiates the same CC four times --- CC_AUDIT_UNDECLARED_TOOL, CC_AUDIT_UNAUTHORIZED_ACTOR, CC_AUDIT_UNAUTHORIZED_TOOL, CC_AUDIT_PARAMETER_VIOLATION --- each with different input bindings. This is a WF node pattern, not a CC pattern. The CC is reusable. The WF nodes are specialized by constant inputs. This follows the principle: CCs are domain-blind capabilities; WF nodes are governance-specific invocations.*

4.  **What would happen if the last step of CC_RECORD_GOVERNED_ACTION_V0 did not forward action_id?**

- *The workflow would receive only result_status from the CC --- the action_id generated in Step 1 would be silently lost at the CC boundary. The CC output forwarding rule (Chapter 13, Section 13.9.2) states that only the last pipeline step's resolved output bindings become the CC result. Prior step outputs do not automatically propagate. This was Defect 5 during construction --- the most subtle execution semantic for domain authors. The fix is explicit forwarding: the last step's output bindings must reference* `$.results.CT_PURE_GENERATE_ID_V0.action_id`*.*

5.  **How does the symmetric audit pattern enforce Invariant I-A6 (Deterministic Trace)?**

- *Every workflow exit path routes through either CC_RECORD_GOVERNED_ACTION_V0 (authorization) or CC_RECORD_DENIED_ACTION_V0 (denial) before reaching an EXIT node. Both contracts append to CS_GOVERNANCE_AUDIT_V0. This means every governance decision --- regardless of outcome --- produces an immutable audit record. The symmetry is structural: there is no exit path that bypasses audit. The WF-CC link validator enforced this at Act IV --- every CC_ node's result statuses are handled, and every handled path routes to either the next gate or a denial audit node. Silent exit is structurally impossible.*

6.  **What evidence in the merge diff proves compositional isolation (I-C1)?**

- *47 files changed, 3063 insertions, 19 deletions. All substantive changes are additions --- new domain files, new reusable atoms, new vocabulary entries, new test registrations. No prior governance artifact was modified. No prior protocol artifact was regenerated. No prior test payload was changed. No prior test expected outcome was altered. The 19 deletions are formatting changes in shared configuration files (env_facts, FQDN tree). Zero semantic changes to any existing domain. The agent governance domain is additive --- it composes with the platform without mutating it.*

7.  **Why must new CT atoms be placed in** `reusable/` **rather than in the domain directory?**

- *Because CT atoms must be domain-agnostic (Chapter 6, Semantic Isolation). CT_PURE_VALIDATE_SET_MEMBERSHIP_V0 checks set membership --- it does not know about tools. CT_PURE_LOOKUP_V0 looks up keys in maps --- it does not know about license tiers. CT_PURE_VALIDATE_PARAMETER_RULES_V0 evaluates declarative rules against parameters --- it does not know about provisioning limits. Placing these atoms in* `reusable/` *enforces domain-blindness structurally. Any future domain can use these atoms for different semantic purposes. If the atoms were in* `agent_governance/`*, they would be structurally scoped to one domain and invisible to others --- violating the reuse guarantee of the shared substrate.*

8.  **Act 0 declared six domain invariants. How are these invariants enforced --- by the specification, by governance artifacts, or by the engine?**

- *By the governance artifacts. The specification is advisory and generative (Chapter 13, Act 0) --- it guides authoring but is not authoritative. The governance artifacts are sovereign. Each invariant is enforced by a specific governance artifact: I-A1 by the single intent (IN_AGENT_ACTION_REQUESTED_V0), I-A2 by CC_CHECK_TOOL_DECLARED_V0's constant allowed_set, I-A3 by CC_BIND_LICENSE_TO_TOOL_SURFACE_V0's tier-to-tool mapping, I-A4 by CC_VALIDATE_TOOL_PARAMETERS_V0's per-tool rule sets, I-A5 by the structural absence of WRITE operations against CS_LICENSE_FACTS_V0, and I-A6 by the symmetric routing of all exit paths through audit CCs. The engine enforces execution --- it follows edges and dispatches capabilities. But the authority structure --- what is allowed, what is denied, what is traced --- lives in governance.*
