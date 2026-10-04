# Supplementary Material: Experiments and Reproduction Record

This folder holds the experiment scripts for *Behavioral Authority in Sealed Models*, their raw outputs, and the record of the run they measured.

## Evaluated composition

| Item | Value |
|---|---|
| Snapshot identity | `f8356d9c8938aea16ab7850d7bda964d8d16c42c64e5db9056d5fe58040ec1d0` |
| Profile | `GOVERNANCE_SURFACE_PROFILE_V0` |
| Domains | ai_governance, blockchain, book_library_mgmt, causal_language_model, inspection, platform, transformation, workload |
| Sealed constituents | 827 |
| Transformation design baseline | `cd8cc3e612f98d485d7f67540a473a32bb8e509251c9bd2a03384b694059ac9c` |
| Platform | macOS 27.0.1, Python 3.12.10 |

## Component revisions

The evaluated composition is published as release `v5`: https://doi.org/10.5281/zenodo.23129879. The
release seals snapshot `f8356d9c…`. Each repository is in the `protocol-governed-computing` GitHub
organization at tag `v5`, and each has its own version DOI.

| Repository | Tag `v5` commit | Version DOI |
|---|---|---|
| software_governance | `bcae826` | 10.5281/zenodo.23129781 |
| conformance_workloads | `89353eb` | 10.5281/zenodo.23129784 |
| business_domains | `b14f432` | 10.5281/zenodo.23129785 |
| protocol_compiler | `4c67325` | 10.5281/zenodo.23129786 |
| protocol_runtime | `2d8cd04` | 10.5281/zenodo.23129787 |
| snapshot_assembler | `48b6d3c` | 10.5281/zenodo.23129788 |
| protocol_transport | `565c06c` | 10.5281/zenodo.23129789 |
| snapshot_inspector | `dccdea1` | 10.5281/zenodo.23129791 |
| transformation | `0ad1f80` | 10.5281/zenodo.23129792 |
| .github | `370a8f1` | — |
| pgc_release | `9aec833` | 10.5281/zenodo.23129879 (the composition) |

The experiments ran on the development commits that became `v5`. Between those commits and the tag,
only version numbers and release notes changed. A clean rebuild at the tag reproduces snapshot
`f8356d9c…`, so the measured composition and the published one are the same composition.

## Prerequisite: the transformation design baseline

The transformation case runs its phase workflows against its own design baseline, not against the
composition. `run_experiments.py` reads that baseline from `/tmp/pgc_cr01_design_baseline`.

- **Who creates it.** The clean rebuild does. `regression.sh --all` runs
  `transformation/scripts/testbed/e2e_phases_test.py`, which reassembles the baseline from five
  compiled roots whenever any of them is newer than the copy in `/tmp`. The roots are
  `software_governance`, `conformance_workloads/workloads/collatz`,
  `business_domains/ai_governance`, `snapshot_inspector` and `transformation`. The profile is
  `GOVERNANCE_SURFACE_PROFILE_V0`.
- **How to check it.** Its identity must be
  `cd8cc3e612f98d485d7f67540a473a32bb8e509251c9bd2a03384b694059ac9c`:

  ```bash
  python3 -c "import json;print(json.load(open('/tmp/pgc_cr01_design_baseline/manifest.json'))['snapshot_id'])"
  ```

- **If it is missing or differs.** Run `regression.sh --all` again before the experiments. Do not
  run the attribution experiment against any other baseline.

## Procedure

Run these from the workspace root:

```bash
bash .github/process/regression.sh --all           # clean rebuild, every check, every workload
python <supplement>/run_experiments.py attribution # E1  → attribution.json
python <supplement>/run_experiments.py tamper      # E2  → tamper.json
bash   <supplement>/omission.sh                    # E3  → omission.out
python <supplement>/outcome_survey.py snapshot     # D1, D2 survey → outcome_survey.out
```

The regression run ends with `REGRESSION PASSED — every step as expected` (59 of 59). E4 reads the regression's own outputs for these steps: `differential`, `e2e_phases_test`, `construction_acceptance`, `supersession_agreement`, `clm_model_response`, `evidence_determinism` and `trace_schema_conformance`.

No script writes into the workspace. E2 alters copies of the snapshot in a temporary directory. E3 cases O1 and O2 alter copies of domain models in a temporary directory. Case O3 alters no model; it corrupts one store in its own temporary data root.

## Files

| File | Content |
|---|---|
| `run_experiments.py` | E1 attribution and E2 tampering |
| `omission.sh` | E3 omission cases O1 and O2, each with its control, and case O3 with the registry's own answer as its oracle |
| `attribution.json` | E1 output |
| `tamper.json` | E2 output |
| `omission.out` | E3 output |
| `outcome_survey.py` | static survey of the sealed composition: steps that list fewer outcomes than their operation declares, and act outcomes no workflow routes |
| `outcome_survey.out` | survey output: 14 step gaps, 11 workflow gaps, 0 gate gaps |
| `glossary.md` | terms used in the paper |
