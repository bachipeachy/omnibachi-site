---
title: Appendix D — Artifact Schema Reference
date: '2026-06-15'
draft: false
weight: 25
slug: appendix-d-artifact-schema-reference
---

Every PGS artifact is a declarative unit of governance. Each artifact type has a fixed schema --- a set of fields that the builder validates before compilation. This appendix documents the schema for each artifact type, drawn from the compiled artifacts in `protocol_snapshot/`.

Artifacts are authored as Markdown files with a YAML `machine:` block. The builder extracts the `machine:` block and compiles it into a JSON artifact. The field definitions here describe the YAML schema --- the same fields appear in the compiled JSON under `frontmatter`.

## Common Fields

All artifact types share the following top-level fields:

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field           Type        Required            Description
  --------------- ----------- ------------------- -------------------------------------------------------------------------------------------------------------------------------
  `<type>_code`   string      yes                 The artifact code, matching the filename (e.g., `WF_REGISTER_ACTOR_UNVERIFIED_V0`). Code format: `<TYPE_PREFIX>_<NAME>_V<N>`.

  `version`       string      yes                 Version string (e.g., `v0`, `V0`). Immutable --- changes require a new artifact code.

  `governed_by`   string      yes                 FQDN of the constitutional layer that governs this artifact type (e.g., `governance.layers::CONSTITUTION_WORKFLOWS_V0`).
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

All artifact file names follow FQDN format: `<namespace>__<ARTIFACT_CODE>.json` (note double underscore between namespace and code).

## Intent (`IN_`)

An intent is the admission gate for a workflow. It declares what inputs are required, what actor context is permitted, and what workflow executes on success.

**Governed by:** `governance.layers::CONSTITUTION_INTENTS_V0`

### Schema

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                                Type             Required            Description
  ------------------------------------ ---------------- ------------------- -------------------------------------------------------------------------------------------------------------------
  `in_code`                            string           yes                 Intent artifact code (e.g., `IN_ACTOR_REGISTERED_V0`).

  `version`                            string           yes                 Artifact version.

  `governed_by`                        string           yes                 Constitutional layer FQDN.

  `core.summary`                       string           yes                 Human-readable description of the intent's purpose.

  `core.workflow`                      string           yes                 Artifact code of the workflow this intent triggers (e.g., `WF_REGISTER_ACTOR_UNVERIFIED_V0`).

  `core.inputs`                        object           yes                 Declared input fields. Keys are field names; values are field definitions (see below).

  `core.inputs.<field>.type`           string           yes                 JSON type: `string`, `object`, `array`, `integer`, `boolean`.

  `core.inputs.<field>.required`       boolean          yes                 Whether the field must be present in the payload.

  `core.inputs.<field>.description`    string           no                  Human-readable field description.

  `core.inputs.<field>.fields`         object           no                  Nested field definitions (for `type: object`). Each nested field has `type`, `required`, and optionally `format`.

  `core.inputs.<field>.format`         string           no                  Format constraint (e.g., `email`). Applied when the field is a primitive type.

  `core.outcomes`                      object           yes                 Named outcomes of the intent admission check.

  `core.outcomes.<name>.description`   string           yes                 What this outcome means (e.g., `ACK` = accepted, `NACK` = rejected).

  `extensions.domain`                  string           no                  Domain label for categorization (e.g., `pgs.identity.actor`).

  `extensions.notes`                   list[string]   no                  Free-text notes about the intent's behavior or constraints.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Example

    in_code: IN_ACTOR_REGISTERED_V0
    version: v0
    governed_by: governance.layers::CONSTITUTION_INTENTS_V0

    core:
      summary: Register a new actor (Unverified)
      workflow: WF_REGISTER_ACTOR_UNVERIFIED_V0
      inputs:
        actor_record:
          type: object
          required: true
          description: Proposed actor registration payload
          fields:
            first_name:
              type: string
              required: true
            last_name:
              type: string
              required: true
            email_registration:
              type: string
              required: true
              format: email
      outcomes:
        ACK:
          description: Actor record accepted for verification
        NACK:
          description: Actor record rejected

## Workflow (`WF_`)

A workflow declares the execution graph (DAG) of Capability Contract nodes. It defines the start node, all nodes, and the routing between them.

**Governed by:** `governance.layers::CONSTITUTION_WORKFLOWS_V0`

### Schema

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                         Type        Required            Description
  ----------------------------- ----------- ------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  `wf_code`                     string      yes                 Workflow artifact code (e.g., `WF_REGISTER_ACTOR_UNVERIFIED_V0`).

  `version`                     string      yes                 Artifact version.

  `governed_by`                 string      yes                 Constitutional layer FQDN.

  `runtime_binding`             string      yes                 FQDN of the RB_ artifact that resolves all CT_ and CS_ capabilities for this workflow.

  `core.summary`                string      yes                 Human-readable description of what this workflow does.

  `core.start_node`             string      yes                 Artifact code of the first node (typically the IN_ intent).

  `core.nodes`                  object      yes                 All nodes in the DAG. Keys are node codes.

  `core.nodes.<code>.type`      string      yes                 Node type: `IN` (intent), `CC` (capability contract), or `EXIT`.

  `core.nodes.<code>.code`      string      yes (IN/CC)         Artifact code of the node (same as the key).

  `core.nodes.<code>.fqdn_id`   string      yes (IN/CC)         FQDN of the artifact.

  `core.nodes.<code>.inputs`    object      no                  JSONPath expressions binding workflow state to node inputs. Keys are the node's declared input field names; values are JSONPath strings (e.g., `$.payload.actor_record`).

  `core.nodes.<code>.next`      object      yes (IN/CC)         Routing table: maps outcome names to the next node code. All declared outcomes must have a route; routes must point to valid node codes or `EXIT`.

  `core.nodes.EX``IT.type`      string      yes                 Must be `EXIT`.

  `core.nodes.EXIT.reason`      string      yes                 Reason label for the terminal state (e.g., `EXITED`).
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### JSONPath Conventions

  ----------------------------------------------------------------------------------------------
  Expression                             Resolves To
  -------------------------------------- -------------------------------------------------------
  `$.payload.<field>`                    A field from the original execution payload.

  `$.results.<CC_CODE>.<output_field>`   An output field from a previously-executed CC_ node.
  ----------------------------------------------------------------------------------------------

### Example (abbreviated)

    wf_code: WF_REGISTER_ACTOR_UNVERIFIED_V0
    version: v0
    governed_by: governance.layers::CONSTITUTION_WORKFLOWS_V0
    runtime_binding: blockchain::RB_REGISTER_ACTOR_UNVERIFIED_V0

    core:
      summary: Register an unverified actor
      start_node: IN_ACTOR_REGISTERED_V0
      nodes:
        IN_ACTOR_REGISTERED_V0:
          type: IN
          code: IN_ACTOR_REGISTERED_V0
          fqdn_id: blockchain::IN_ACTOR_REGISTERED_V0
          next:
            ACK: CC_GENERATE_ACTOR_ID_V0
            NACK: EXIT
        CC_GENERATE_ACTOR_ID_V0:
          type: CC
          code: CC_GENERATE_ACTOR_ID_V0
          fqdn_id: blockchain::CC_GENERATE_ACTOR_ID_V0
          inputs:
            actor_record: $.payload.actor_record
          next:
            SUCCESS: CC_REGISTER_ACTOR_KYC_V0
            VIOLATION: EXIT
        EXIT:
          type: EXIT
          reason: EXITED

## Capability Contract (`CC_`)

A CC_ is a named node in the workflow DAG. It declares its inputs, outputs, pipeline of CT_ and CS_ steps, outcome routing, and result status contract.

**Governed by:** `governance.layers::CONSTITUTION_CAPABILITY_CONTRACTS_V0`

### Schema

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                                            Type             Required            Description
  ------------------------------------------------ ---------------- ------------------- -----------------------------------------------------------------------------------------------------------------------------------------------------
  `cc_code`                                        string           yes                 CC artifact code (e.g., `CC_GENERATE_ACTOR_ID_V0`).

  `version`                                        string           yes                 Artifact version.

  `governed_by`                                    string           yes                 Constitutional layer FQDN.

  `core.summary`                                   string           yes                 Human-readable description of what this CC does.

  `core.inputs`                                    object           yes                 Declared input fields. Keys are field names; values have `type` and `required`.

  `core.outputs`                                   object           yes                 Declared output fields. Keys are field names; values have `type`.

  `core.result_status_contract.allowed`            list[string]   yes                 The set of outcome codes this CC may return. All outcomes appearing in any `next:` table in the workflow must be in this list.

  `core.result_status_contract.on_input_failure`   string           yes                 Outcome to emit if input validation fails (typically `VIOLATION`).

  `core.pipeline`                                  list[object]   yes                 Ordered steps that this CC executes.

  `core.pipeline[].step`                           string           yes                 Internal step identifier (snake_case label).

  `core.pipeline[].transform`                      string           yes (CT steps)      FQDN of the CT_ or CS_ artifact to invoke.

  `core.pipeline[].op`                             string           yes (CS steps)      Operation name declared by the CS_ artifact (e.g., `REGISTER`, `APPEND`).

  `core.pipeline[].inputs`                         object           yes                 Input bindings for this step. Keys are the capability's declared input fields; values are JSONPath expressions or literal values.

  `core.pipeline[].outputs`                        object           yes                 Output bindings from this step. Keys are local output field names; values are JSONPath into the capability result (e.g., `$.capability_result.id`).

  `core.pipeline[].on_result`                      object           yes                 Per-outcome routing within the pipeline. Maps outcome codes to `exit` (finish pipeline) or another step name.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Example

    cc_code: CC_GENERATE_ACTOR_ID_V0
    version: v0
    governed_by: governance.layers::CONSTITUTION_CAPABILITY_CONTRACTS_V0

    core:
      summary: Generate deterministic actor ID
      inputs:
        actor_record:
          type: object
          required: true
      outputs:
        actor_id:
          type: string
      result_status_contract:
        allowed: [SUCCESS, VIOLATION]
        on_input_failure: VIOLATION
      pipeline:
        - step: generate_actor_id
          transform: capability_transforms::CT_PURE_GENERATE_ID_V0
          op: GENERATE_ID
          inputs:
            data: $.inputs.actor_record
            prefix: AC
          outputs:
            actor_id: $.capability_result.id
          on_result:
            SUCCESS: exit
            VIOLATION: exit

## Capability Transform (`CT_`)

A CT_ is a pure computational unit --- deterministic and side-effect free. It can be an atom (single function) or a molecule (composition of atoms).

**Governed by:** `governance.layers::CONSTITUTION_CAPABILITY_TRANSFORMS_V0`

### Schema

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                               Type        Required            Description
  ----------------------------------- ----------- ------------------- ---------------------------------------------------------------------------------------------------------------------------
  `ct_code`                           string      yes                 CT artifact code (e.g., `CT_PURE_GENERATE_ID_V0`).

  `version`                           string      yes                 Artifact version.

  `governed_by`                       string      yes                 Constitutional layer FQDN.

  `core.summary`                      string      yes                 One-line description of what this transform computes.

  `core.description`                  string      no                  Extended description.

  `core.inputs`                       object      yes                 Declared input fields. Keys are field names; values have `type`, `required`, and optionally `description`.

  `core.outputs`                      object      yes                 Declared output fields. Keys are field names; values have `type` and optionally `description`.

  `machine.ct_kind`                   string      yes                 `atom` (single function) or `molecule` (composition of atoms).

  `machine.ct_purity`                 string      yes                 Always `ct_pure` --- declares the no-side-effects invariant.

  `machine.operation`                 string      yes                 Canonical operation name used to invoke this transform (e.g., `GENERATE_ID`).

  `machine.implementation.module`     string      yes (atoms)         Python module path to the implementation (e.g., `pgs_transforms.implementation.transforms.atoms.ct_pure_generate_id_v0`).

  `machine.implementation.callable`   string      yes (atoms)         Callable within the module (e.g., `execute`).
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Example

    ct_code: CT_PURE_GENERATE_ID_V0
    version: V0
    governed_by: governance.layers::CONSTITUTION_CAPABILITY_TRANSFORMS_V0

    core:
      summary: Generate deterministic ID
      description: Generates a deterministic unique identifier based on input data using Keccak-256 hashing.
      inputs:
        data:
          type: any
          required: true
          description: Input data to hash for ID generation
        prefix:
          type: string
          required: true
          description: Identifier prefix (e.g., AC, WF, IN)
      outputs:
        id:
          type: string
          required: true
          description: The generated deterministic ID

    machine:
      ct_kind: atom
      ct_purity: ct_pure
      operation: GENERATE_ID
      implementation:
        module: pgs_transforms.implementation.transforms.atoms.ct_pure_generate_id_v0
        callable: execute

## Capability Side Effect (`CS_`)

A CS_ artifact declares a bounded, controlled interface to external state. The CS_ schema defines operations, properties, guarantees, and configuration --- not implementation. Implementation is resolved at runtime via RB_.

**Governed by:** `governance.layers::CONSTITUTION_CAPABILITY_SIDE_EFFECTS_V0`

### Schema

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                                         Type             Required            Description
  --------------------------------------------- ---------------- ------------------- ---------------------------------------------------------------------------------------------------------------------------
  `cs_code`                                     string           yes                 CS artifact code (e.g., `CS_REGISTRY_V0`).

  `version`                                     string           yes                 Artifact version.

  `governed_by`                                 string           yes                 Constitutional layer FQDN.

  `core.summary`                                string           yes                 Description of the side-effect capability.

  `core.category`                               string           yes                 Capability category (e.g., `storage`).

  `core.policy.operations`                      list[string]   yes                 Declared operations this CS_ supports (e.g., `[REGISTER, RESOLVE, EXISTS, DEREGISTER]`).

  `core.operations.<OP>.summary`                string           yes                 One-line description of the operation.

  `core.operations.<OP>.handler`                string           yes                 Handler method name in the runtime class.

  `core.operations.<OP>.input`                  list[string]   yes                 Input field names for this operation.

  `core.operations.<OP>.output`                 list[string]   yes                 Output field names from this operation.

  `core.operations.<OP>.idempotent`             boolean          yes                 Whether repeated calls with same input produce the same state.

  `core.operations.<OP>.result_status_values`   list[string]   yes                 Possible outcome codes for this operation.

  `extensions.cs_kind`                          string           yes                 Kind of side effect (e.g., `registry`, `mutable_json`, `appendonly_jsonl`, `email`, `workflow_gateway`, `name_registry`).

  `extensions.side_effect_type`                 string           yes                 `persistent` or `transient`.

  `extensions.properties`                       object           yes                 Runtime properties: `durability`, `idempotent`, `replay_policy`, `transactional`, `concurrent_safe`.

  `extensions.configuration_schema`             object           yes                 Fields required when this CS_ is configured via an RB_ binding.

  `implementation.module`                       string           yes                 Python module path to the runtime class.

  `implementation.callable`                     string           yes                 Runtime class name (e.g., `RegistryRuntime`).
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Closed Runtime Types

The set of CS_ runtime types is closed. The six declared types are:

  ----------------------------------------------------------------------------------------------------
  CS Code                    Runtime Class              Side-Effect Kind
  -------------------------- -------------------------- ----------------------------------------------
  `CS_REGISTRY_V0`           `RegistryRuntime`          Stable key→address indirection (append-only)

  `CS_MUTABLE_JSON_V0`       `MutableJsonRuntime`       Last-write-wins JSON document

  `CS_APPENDONLY_JSONL_V0`   `AppendOnlyJsonlRuntime`   Append-only event log

  `CS_SEND_EMAIL_V0`         `SendEmailRuntime`         Email delivery

  `CS_WORKFLOW_GATEWAY_V0`   `WorkflowGatewayRuntime`   Cross-workflow invocation

  `CS_NAME_REGISTRY_V0`      `NameRegistryRuntime`      Human-readable name→FQDN binding
  ----------------------------------------------------------------------------------------------------

Extending this set requires a change to the runtime engine, not an RB_ artifact.

## Runtime Binding (`RB_`)

An RB_ artifact maps CT_ and CS_ capability codes to their concrete implementations. It is the bridge between protocol declarations and executable code. The same binding mechanism applies symmetrically to both transform and side-effect capabilities.

**Governed by:** `governance.layers::CONSTITUTION_RUNTIME_BINDINGS_V0`

### Schema

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                                  Type        Required              Description
  -------------------------------------- ----------- --------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  `rb_code`                              string      yes                   RB artifact code (e.g., `RB_REGISTER_ACTOR_UNVERIFIED_V0`).

  `version`                              string      yes                   Artifact version.

  `governed_by`                          string      yes                   Constitutional layer FQDN.

  `core.summary`                         string      yes                   Human-readable description of what this binding resolves.

  `core.description`                     string      no                    Extended description.

  `core.bindings`                        object      yes                   Map from capability FQDN to binding policy. Keys are capability FQDNs (e.g., `capability_side_effects::CS_REGISTRY_V0`).

  `core.bindings.<FQDN>.policy`          object      yes                   Binding policy for this capability.

  `core.bindings.<FQDN>.policy.path`     string      yes (CS_ storage)    Filesystem path for storage-backed CS_ types. Supports `{{module_data_root}}` template variable, resolved at runtime to the `--data-root` value scoped to the domain.

  `core.bindings.<FQDN>.policy.module`   string      yes (CT_ bindings)   Module path for CT_ implementations (when overriding default resolution).
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Template Variables in `policy.path`

  ---------------------------------------------------------------------------------------------------------------------
  Variable                       Resolves To
  ------------------------------ --------------------------------------------------------------------------------------
  `{{module_data_root}}`         `{data_root}/{domain_name}` --- the domain-scoped subdirectory of the `--data-root`.

  ---------------------------------------------------------------------------------------------------------------------

### Example

    rb_code: RB_REGISTER_ACTOR_UNVERIFIED_V0
    version: v0
    governed_by: governance.layers::CONSTITUTION_RUNTIME_BINDINGS_V0

    core:
      summary: Runtime binding for actor registration workflow
      description: Binds capability side effects to concrete runtime implementations for actor registration.
      bindings:
        capability_side_effects::CS_REGISTRY_V0:
          policy:
            path: "{{module_data_root}}/registry/actors.json"
        capability_side_effects::CS_APPENDONLY_JSONL_V0:
          policy:
            path: "{{module_data_root}}/events/identity_events.jsonl"

## Actor (`AC_`)

An AC_ artifact declares an authority principal --- an identity type that participates in execution. Actors bind identity, role, and attribute schema to a named type.

**Governed by:** `governance.layers::CONSTITUTION_ACTORS_V0`

### Schema

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                                Type        Required            Description
  ------------------------------------ ----------- ------------------- ----------------------------------------------------------------------------------------------------
  `ac_code`                            string      yes                 Actor artifact code (e.g., `AC_AGENT_V0`).

  `version`                            string      yes                 Artifact version.

  `governed_by`                        string      yes                 Constitutional layer FQDN.

  `core.summary`                       string      yes                 One-line description of the actor's role.

  `core.description`                   string      no                  Extended description of the actor's governance role.

  `core.type`                          string      yes                 Actor kind (e.g., `agent`, `human`, `system`).

  `core.attributes`                    object      yes                 Attribute schema for this actor type. Keys are attribute names; values have `type` and `required`.

  `core.attributes.<field>.type`       string      yes                 JSON type of the attribute (`string`, `integer`, etc.).

  `core.attributes.<field>.required`   boolean     yes                 Whether the attribute must be present on instantiation.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Example

    ac_code: AC_AGENT_V0
    version: v0
    governed_by: governance.layers::CONSTITUTION_ACTORS_V0

    core:
      summary: Probabilistic intent emitter
      description: Autonomous agent that proposes actions through governance protocol
      type: agent
      attributes:
        agent_id:
          type: string
          required: true
        requesting_user_id:
          type: string
          required: true

## Event (`EV_`)

An EV_ artifact declares an observable fact that execution emits. Events contribute to the execution trace, enable cross-boundary signaling, and participate in governance decisions.

**Governed by:** `governance.layers::CONSTITUTION_EVENTS_V0`

### Schema

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                            Type        Required            Description
  -------------------------------- ----------- ------------------- --------------------------------------------------------------------------------------------------------------------
  `ev_code`                        string      yes                 Event artifact code (e.g., `EV_AGENT_ACTION_AUTHORIZED_V0`).

  `version`                        string      yes                 Artifact version.

  `governed_by`                    string      yes                 Constitutional layer FQDN.

  `core.summary`                   string      yes                 One-line description of the fact this event records.

  `core.description`               string      no                  Extended description.

  `core.schema`                    object      yes                 Field schema for the event payload. Keys are field names; values have `type`, `required`, and optionally `format`.

  `core.schema.<field>.type`       string      yes                 JSON type of the field.

  `core.schema.<field>.required`   boolean     yes                 Whether the field must be present when the event is emitted.

  `core.schema.<field>.format`     string      no                  Format constraint (e.g., `date-time`).
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Example

    ev_code: EV_AGENT_ACTION_AUTHORIZED_V0
    version: v0
    governed_by: governance.layers::CONSTITUTION_EVENTS_V0

    core:
      summary: Agent action authorized by governance
      description: Emitted when an agent-proposed action passes all governance checks and is authorized for execution
      schema:
        action_id:
          type: string
          required: true
        tool_name:
          type: string
          required: true
        requesting_user_id:
          type: string
          required: true
        license_tier:
          type: string
          required: true
        decision:
          type: string
          required: true
        timestamp:
          type: string
          format: date-time
          required: true

## Assertion (`AS_`)

An AS_ artifact declares a compile-time invariant check. Assertions run during the build phase (Act III/IV) and cause a hard build failure if violated. They are not runtime checks.

**Governed by:** `governance.invariants::INVARIANT_<NAME>_V0` (varies by assertion type)

### Schema

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Field                             Type             Required            Description
  --------------------------------- ---------------- ------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------
  `artifact_code`                   string           yes                 Assertion artifact code (e.g., `ASSERT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0`).

  `artifact_type`                   string           yes                 Always `ASSERT`.

  `artifact_kind`                   string           yes                 Always `ASSERT`.

  `version`                         integer          yes                 Artifact version number.

  `governed_by`                     list[string]   yes                 List of invariant FQDNs this assertion enforces.

  `scope.applies_to`                list[string]   yes                 Domain layer codes this assertion applies to (e.g., `[BLOCKCHAIN]`).

  `implementation.module`           string           yes                 Python module path to the assertion handler.

  `implementation.callable`         string           yes                 Callable within the module (e.g., `execute`).

  `allowed_capability_transforms`   list[string]   no (CT closure)     For CT surface closure assertions: the explicit list of all permitted CT_ FQDNs within the scope. Any CT_ not in this list causes a build failure.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Assertion Phase

Assertions run at build phase 5 (ASSERT). A failing assertion produces a hard build stop --- the snapshot is not updated. This is how behavioral admissibility is enforced: if a CT_ is not in the closure assertion's allowlist, it cannot exist in the compiled snapshot.

### Example

    artifact_code: ASSERT_CT_SURFACE_CLOSED_BLOCKCHAIN_V0
    artifact_type: ASSERT
    artifact_kind: ASSERT
    version: 0

    governed_by:
      - governance.invariants::INVARIANT_CT_SURFACE_CLOSED_V0

    scope:
      applies_to:
        - BLOCKCHAIN

    implementation:
      module: pgs_governance.registry.handlers.assert_ct_surface_closed_v0
      callable: execute

    allowed_capability_transforms:
      - blockchain::CT_PURE_BUILD_ETH_TRANSACTION_V0
      - blockchain::CT_PURE_DERIVE_WALLET_KEYPAIRS_V0
      - blockchain::CT_PURE_EXTRACT_WALLET_TX_FIELDS_V0
      - blockchain::CT_PURE_INCREMENT_WALLET_NONCE_V0

## Field Type Reference

All artifact schemas use the following type vocabulary:

  -----------------------------------------------------------------------------------------------
  Type                   Description
  ---------------------- ------------------------------------------------------------------------
  `string`               UTF-8 string.

  `integer`              Integer number.

  `boolean`              `true` or `false`.

  `object`               JSON object (nested fields).

  `array`                JSON array.

  `any`                  Any JSON value (used sparingly in CT_ inputs for generic transforms).
  -----------------------------------------------------------------------------------------------

Format constraints (`format:`) follow JSON Schema conventions: `email`, `date-time`, `uri`.

## Reading Compiled Artifacts

The compiled JSON artifacts in `protocol_snapshot/` have additional envelope fields added by the builder:

  --------------------------------------------------------------------------------------------------------------------------
  Envelope Field                          Description
  --------------------------------------- ----------------------------------------------------------------------------------
  `fqdn_id`                               Fully-qualified identifier: `<namespace>::<ARTIFACT_CODE>`.

  `artifact_code`                         Short code without namespace.

  `artifact_type`                         Two-letter type prefix (`WF`, `CC`, `CT`, etc.).

  `namespace`                             Domain namespace (e.g., `blockchain`, `ai_governance`, `capability_transforms`).

  `version`                               Version string.

  `frontmatter`                           The parsed YAML machine block --- the source of the field schemas above.

  `content`                               Raw Markdown source of the artifact.

  `content_hash`                          SHA-256 hash of the content for integrity verification.

  `source_path`                           Absolute path to the source file in the tooling repo.

  `references`                            List of FQDNs this artifact references (resolved at compile time).

  `layer_code`                            Governance layer this artifact belongs to.

  `module_path`                           Python module path within the source repo.
  --------------------------------------------------------------------------------------------------------------------------

The `frontmatter` field is authoritative for runtime dispatch. All other envelope fields are compiler metadata.
