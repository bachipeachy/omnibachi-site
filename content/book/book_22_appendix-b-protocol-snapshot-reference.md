---
title: Appendix B — Protocol Snapshot Reference
date: '2026-06-11'
draft: false
weight: 22
slug: appendix-b-protocol-snapshot-reference
---

The canonical set of compiled protocol artifacts is maintained in the `protocol_snapshot/` directory of the `pgs_workspace` repository.

> **Why a live pointer instead of a static appendix?** Prior editions included artifact listings in this appendix. Protocol artifacts are versioned, evolving artifacts --- a static copy ages immediately. The live snapshot is always authoritative.

## Location

    pgs_workspace/
    └── protocol_snapshot/
        └── artifacts/
            ├── workflows/
            ├── capability_contracts/
            ├── capability_transforms/
            ├── capability_side_effects/
            ├── runtime_bindings/
            ├── intents/
            ├── assertions/
            ├── events/
            ├── actors/
            ├── layers/
            └── invariants/

## How to Browse

    # List all workflows
    ls protocol_snapshot/artifacts/workflows/

    # List all capability side effects
    ls protocol_snapshot/artifacts/capability_side_effects/

    # Read a specific artifact
    cat protocol_snapshot/artifacts/workflows/blockchain__WF_REGISTER_ACTOR_UNVERIFIED_V0.json

## Naming Convention

All artifact filenames follow FQDN format:

    <domain>::<ARTIFACT_CODE>.json

Examples: - `blockchain__WF_REGISTER_ACTOR_UNVERIFIED_V0.json` - `ai_governance__AC_AGENT_V0.json` - `capability_transforms__CT_PURE_GENERATE_ID_V0.json`

## Current Artifact Counts

  ---------------------------------------------------------------------------------------
  Type                              Directory                        Count
  --------------------------------- -------------------------------- --------------------
  Workflows (`WF_`)                 `workflows/`                     See snapshot

  Capability Contracts (`CC_`)      `capability_contracts/`          See snapshot

  Capability Transforms (`CT_`)     `capability_transforms/`         See snapshot

  Capability Side Effects (`CS_`)   `capability_side_effects/`       6

  Runtime Bindings (`RB_`)          `runtime_bindings/`              7

  Intents (`IN_`)                   `intents/`                       See snapshot

  Actors (`AC_`)                    `actors/`                        7

  Assertions (`AS_`)                `assertions/`                    See snapshot
  ---------------------------------------------------------------------------------------

Counts marked "See snapshot" vary as domains evolve. The six CS_ runtime types and seven RB_ artifacts are stable as of this edition.

## Source

Protocol artifacts are compiled from source across the `pgs_governance` and `pgs_compiler` repositories. The workspace snapshot represents the last successful compilation. To see how artifacts are authored, see `pgs_governance/`. To understand the compilation process, see Chapter 4 --- The Builder as Constitutional Compiler.
