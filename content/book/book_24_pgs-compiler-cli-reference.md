---
title: pgs_compiler CLI Reference
date: '2026-06-15'
draft: false
weight: 24
slug: pgs-compiler-cli-reference
---

`pgs_compiler` is the command-line interface for the PGS compiler pipeline. It provides three subcommands: `compile` runs a single-structure build, `build` runs the full workspace build, and `inspect` queries compiled evidence without recompiling.

## Global Usage

    python -m pgs_compiler.cli <subcommand> [options]

## `compile`

Runs the full 9-stage pipeline (S1--S9) for a single STRUCTURE_ artifact (Phase Type A).

    python -m pgs_compiler.cli compile --structure <STRUCTURE_NAME>

  -------------------------------------------------------------------------------------------------------------------------
  Flag                   Description
  ---------------------- --------------------------------------------------------------------------------------------------
  `--structure`          Name of the STRUCTURE_ build artifact to compile (e.g., `STRUCTURE_BUILD_BLOCKCHAIN_CONFIG_V0`)

  -------------------------------------------------------------------------------------------------------------------------

Phase Type A structures must be compiled before any Phase Type B aggregation that depends on them.

**Examples:**

    python -m pgs_compiler.cli compile --structure STRUCTURE_BUILD_PLATFORM_CONFIG_V0
    python -m pgs_compiler.cli compile --structure STRUCTURE_BUILD_BLOCKCHAIN_CONFIG_V0
    python -m pgs_compiler.cli compile --structure STRUCTURE_BUILD_AI_GOVERNANCE_CONFIG_V0

    # Phase Type B — run after all Phase Type A builds complete
    python -m pgs_compiler.cli compile --structure STRUCTURE_BUILD_VOCABULARY_AGGREGATE_V0

## `build`

Runs the full workspace build: compiles all structures, syncs artifacts to `protocol_snapshot/`, runs conformance tests, and marks the snapshot valid.

    python -m pgs_compiler.cli build --workspace <absolute-path>

  -----------------------------------------------------------------------------------------------------------------------------------
  Flag                   Description
  ---------------------- ------------------------------------------------------------------------------------------------------------
  `--workspace`          Absolute path to the `pgs_workspace` root. Snapshot output is written to `{workspace}/protocol_snapshot/`.

  -----------------------------------------------------------------------------------------------------------------------------------

`--workspace` must be an absolute path.

## `inspect`

Queries the compiled evidence graph for a structure without recompiling. Reads from `evidence_snapshot/` only --- no pipeline stages run.

    python -m pgs_compiler.cli inspect --structure <STRUCTURE_NAME> [--artifact <FQDN> | --upstream <FQDN> | --family <FAMILY>]

  -----------------------------------------------------------------------------------------------------------------------
  Flag                   Description
  ---------------------- ------------------------------------------------------------------------------------------------
  `--structure`          STRUCTURE_ artifact that produced the evidence to query

  `--artifact`           Show the full compilation record for a specific artifact FQDN

  `--upstream`           Show all upstream causality events for a specific artifact FQDN

  `--family`             Show all events belonging to a specific compilation family (e.g., `CONSTRUCTION`, `DISCOVERY`)
  -----------------------------------------------------------------------------------------------------------------------

**Examples:**

    # Show compilation record for a specific workflow
    python -m pgs_compiler.cli inspect \
      --structure STRUCTURE_BUILD_BLOCKCHAIN_CONFIG_V0 \
      --artifact blockchain::WF_REGISTER_ACTOR_UNVERIFIED_V0

    # Show upstream causality for a capability contract
    python -m pgs_compiler.cli inspect \
      --structure STRUCTURE_BUILD_BLOCKCHAIN_CONFIG_V0 \
      --upstream blockchain::CC_GENERATE_ACTOR_ID_V0

    # Show all CONSTRUCTION-family events
    python -m pgs_compiler.cli inspect \
      --structure STRUCTURE_BUILD_BLOCKCHAIN_CONFIG_V0 \
      --family CONSTRUCTION

## Compiler Operational Notes

**Compile order matters.** Phase Type A structures are independent and may be compiled in any order relative to each other. Phase Type B structures depend on Phase Type A outputs --- they must run after all contributing structures complete.

**Snapshot is write-only during build.** The compiler writes to `protocol_snapshot/` and `evidence_snapshot/`. Never edit these by hand. To change an artifact, change the protocol source and recompile.

**Admission gate.** `assert_snapshot_valid()` runs at S8 VERIFY before S9 ATTEST. If the gate fails, the snapshot is not attested and the runtime will not load it. Rerun the full build to resolve.
