---
title: Appendix C — pgs_runtime CLI Reference
date: '2026-06-18'
draft: false
weight: 23
slug: appendix-c-pgs-runtime-cli-reference
---

`pgs_runtime` is the command-line interface for the PGS runtime engine. It provides two subcommands: `run` executes a workflow or intent against a compiled snapshot, and `examine` inspects an execution trace.

## Global Usage

    pgs_runtime <subcommand> [options]

The CLI reads from `protocol_snapshot/` and writes traces to `traces/`. It does not modify snapshot artifacts.

## `pgs_runtime run`

Executes a workflow or intent against the compiled protocol snapshot.

### Synopsis

    pgs_runtime run \
      (--wf <FQDN> | --intent <FQDN>) \
      --payload <path> \
      [--rb <FQDN>] \
      [--mode <runtime|authoring>] \
      [--debug] \
      [--data-root <path>] \
      [--workspace <path>]

### Entry Point (mutually exclusive, one required)

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Flag           Argument                 Description
  -------------- ------------------------ -----------------------------------------------------------------------------------------------------------------------------------------------------
  `--wf`         `<FQDN>`                 Execute by workflow FQDN directly (e.g., `blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0`). Bypasses intent admission gate.

  `--intent`     `<FQDN>`                 Execute via intent FQDN (e.g., `blockchain::IN_ACTOR_REGISTERED_V0`). Admission check runs first; workflow is resolved from the intent declaration.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

`--wf` and `--intent` are mutually exclusive. Exactly one must be provided.

### Required Flags

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Flag           Argument                 Description
  -------------- ------------------------ ------------------------------------------------------------------------------------------------------------------------------
  `--payload`    `<path>`                 Path to a JSON file containing the execution payload. The payload must satisfy the schema declared by the workflow's intent.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Optional Flags

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Flag            Argument                   Default                   Description
  --------------- -------------------------- ------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------
  `--rb`          `<FQDN>`                   Resolved from snapshot    Runtime binding FQDN override. Overrides the default binding for the workflow. Used when testing an alternative implementation without recompiling.

  `--mode`        `runtime` \| `authoring`   `authoring`               Execution mode. `authoring` runs governance checks and produces full trace output. `runtime` is a leaner path for production execution.

  `--debug`       *(flag)*                   off                       Enable DEBUG-level logging. Outputs internal resolution steps, JSONPath evaluations, and capability dispatch events to stderr.

  `--data-root`   `<path>`                   `PGS_DATA_ROOT` env var   **Must be an absolute path.** Directory where CS_ side effects write runtime state (e.g., `registry/actors.json`, `events/*.jsonl`).

  `--workspace`   `<path>`                   `PGS_WORKSPACE` env var   Path to the `pgs_workspace` root. The runtime reads `protocol_snapshot/` from `{workspace}/protocol_snapshot/` and writes traces to `{workspace}/traces/`.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Environment Variables

  -----------------------------------------------------------------------------------------------------------
  Variable           Equivalent Flag               Description
  ------------------ ----------------------------- ----------------------------------------------------------
  `PGS_DATA_ROOT`    `--data-root`                 Default data root when `--data-root` is not passed.

  `PGS_WORKSPACE`    `--workspace`                 Default workspace root when `--workspace` is not passed.
  -----------------------------------------------------------------------------------------------------------

Flags take precedence over environment variables when both are set.

### Execution Behavior

1.  The runtime loads `protocol_snapshot/` from `{workspace}/protocol_snapshot/`.
2.  If `--intent` is used, the intent admission gate runs first. The payload must satisfy the intent's declared input schema. A failed admission gate exits without writing a trace.
3.  The workflow DAG is traversed: each CC_ node resolves its inputs via JSONPath, dispatches CT_ transforms and CS_ side effects through RB_ bindings, and routes to the next node based on the outcome.
4.  A trace is written to `{workspace}/traces/<TRACE_ID>/`:
    - `<TRACE_ID>.jsonl` --- append-only structured event log
    - `<TRACE_ID>.md` --- human-readable summary
    - `<TRACE_ID>.png` --- execution path visualization

### Exit Behavior

  -------------------------------------------------------
  Condition                                   Exit Code
  ------------------------------------------- -----------
  Workflow completed (any terminal outcome)   `0`

  Intent admission failed                     `1`

  Missing or unresolvable artifact            `1`

  Unresolved RB_ binding                     `1`

  Invalid payload JSON                        `1`
  -------------------------------------------------------

### Examples

    # Execute by workflow FQDN
    pgs_runtime run \
      --wf blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0 \
      --payload ~/pgs_blockchain/pgs_blockchain/testbed/identity/test_payloads/register_actor_unverified_payload.json \
      --data-root ~/pgs_workspace/data \
      --workspace ~/pgs_workspace

    # Execute via intent (admission gate enforced)
    pgs_runtime run \
      --intent blockchain::IN_ACTOR_REGISTERED_V0 \
      --payload ~/pgs_blockchain/pgs_blockchain/testbed/identity/test_payloads/register_actor_unverified_payload.json \
      --data-root ~/pgs_workspace/data \
      --workspace ~/pgs_workspace

    # Run with debug logging and explicit mode
    pgs_runtime run \
      --wf blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0 \
      --payload ~/pgs_blockchain/pgs_blockchain/testbed/identity/test_payloads/register_actor_unverified_payload.json \
      --mode authoring \
      --debug \
      --data-root ~/pgs_workspace/data \
      --workspace ~/pgs_workspace

    # Use environment variables instead of flags
    export PGS_DATA_ROOT=~/pgs_workspace/data
    export PGS_WORKSPACE=~/pgs_workspace
    pgs_runtime run \
      --wf blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0 \
      --payload ~/pgs_blockchain/pgs_blockchain/testbed/identity/test_payloads/register_actor_unverified_payload.json

## `pgs_runtime examine`

Inspects an execution trace produced by `pgs_runtime run`.

### Synopsis

    pgs_runtime examine <trace_file>

### Positional Arguments

  ---------------------------------------------------------------------------------------------------------------
  Argument                       Description
  ------------------------------ --------------------------------------------------------------------------------
  `trace_file`                   Path to a `.jsonl` trace file. Typically `traces/<TRACE_ID>/<TRACE_ID>.jsonl`.

  ---------------------------------------------------------------------------------------------------------------

### Behavior

The examiner reads the structured event log and prints a human-readable summary of the execution: - Workflow and intent resolved - Each CC_ node: inputs, outcome, outputs - Each CT_ and CS_ step within each node - Routing decisions at each node - Terminal state and exit outcome - Any failures, violations, or unexpected outcomes flagged with diagnostic hints

The examiner does not modify the trace file. It is read-only.

### Output Format

The examiner prints to stdout. Output includes: - A header with trace ID, workflow FQDN, and execution timestamp - A node-by-node walk of the execution path - A terminal summary (final outcome, nodes visited, capabilities invoked)

### Example

    # Examine a specific trace
    pgs_runtime examine ~/pgs_workspace/traces/abc123/abc123.jsonl

    # Examine the most recent trace
    pgs_runtime examine ~/pgs_workspace/traces/$(ls -t ~/pgs_workspace/traces/ | head -1)/$(ls -t ~/pgs_workspace/traces/ | head -1).jsonl

## Operational Notes

**Snapshot is read-only.** The CLI reads from `protocol_snapshot/` but never writes to it. Any change to behavior requires recompiling the protocol source.

**Data root must be absolute.** Relative paths for `--data-root` are not supported. Use an absolute path or set `PGS_DATA_ROOT` to an absolute path.

**Trace IDs are deterministic.** The same payload run twice under identical snapshot state produces the same trace structure. This is the basis of the idempotency guarantee: check for `ALREADY_EXISTS` outcomes in repeated runs.

**No interactive mode.** The CLI is non-interactive. All inputs are provided at invocation time.
