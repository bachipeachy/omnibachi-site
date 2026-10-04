#!/usr/bin/env python3
"""Experiments for "Behavioral Authority in Sealed Models".

Run from the PGC workspace root, after a clean `regression.sh --all`:

    python <this file> attribution   # RQ1: attribute every recorded decision to a sealed declaration
    python <this file> tamper        # RQ1/RQ4: alter a sealed snapshot, one constituent class at a time

Each experiment prints a JSON result to stdout. Neither writes into the workspace: the tamper
experiment works on a copy of the snapshot in a temporary directory.
"""
from __future__ import annotations

import collections
import json
import shutil
import sys
import tempfile
from pathlib import Path

WORKSPACE = Path.cwd()
SNAPSHOT = WORKSPACE / "snapshot"
DATA = WORKSPACE / "data"

# The transformation case executes its phase workflows against its own design baseline, a separate
# composition the transformation testbed assembles. Its traces name that snapshot, so they are
# explained against it. Named here, never discovered.
SNAPSHOT_FOR = {"transformation": Path("/tmp/pgc_cr01_design_baseline")}


# ── RQ1: attribution ─────────────────────────────────────────────────────────

def attribution() -> dict:
    """Explain every trace, classify each recorded decision, and test it against the sealed model."""
    from inspector.api import query

    by_class: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    endings = collections.Counter()
    statuses = collections.Counter()
    refused = collections.Counter()
    per_domain = collections.Counter()
    traces = 0

    for root in sorted(p for p in DATA.iterdir() if (p / "traces").is_dir()):
        for trace in sorted((root / "traces").rglob("*.jsonl")):
            reference = trace.relative_to(root).as_posix()
            snapshot = SNAPSHOT_FOR.get(root.name, SNAPSHOT)
            status, answer = query("si.execution.explain", {"trace": reference}, snapshot,
                                   trace_root=root)
            if status != "SUCCESS":
                refused[answer.get("reason", status)[:80]] += 1
                continue
            traces += 1
            per_domain[answer["domain"]] += 1
            endings[answer["ending"]["kind"]] += 1
            statuses[answer["status"]] += 1
            indexed = {a["fqdn"]: a["indexed"] for a in answer["artifacts"]}

            for visit in answer["visits"]:
                joined = visit["snapshot"]
                determination = visit.get("determination") or {}
                if determination.get("basis") == "recorded admission checks":
                    by_class["admission"][joined["declared"]] += 1
                if visit.get("result") is not None:
                    by_class["outcome"][joined["declared"] and bool(joined.get("capability"))] += 1
                if visit.get("route") is not None:
                    by_class["route"][visit["route"]["snapshot"]["declared_edge"]] += 1
                for step in visit["steps"]:
                    if step["op"] and step["op"] != "ADMIT":
                        by_class["effect"][indexed.get(step["step"], False)] += 1
                for event in visit["events"]:
                    by_class["event"][indexed.get(event, False)] += 1
                for atom in visit["atoms"]:
                    if atom.get("captured"):
                        by_class["captured_input"][indexed.get(atom["atom"], False)] += 1

    table = {
        cls: {"observed": c[True] + c[False], "attributed": c[True], "unattributed": c[False]}
        for cls, c in sorted(by_class.items())
    }
    total = sum(r["observed"] for r in table.values())
    attributed = sum(r["attributed"] for r in table.values())
    return {
        "snapshot_id": json.loads((SNAPSHOT / "manifest.json").read_text())["snapshot_id"],
        "traces_explained": traces,
        "traces_refused": dict(refused),
        "traces_per_domain": dict(per_domain),
        "endings": dict(endings),
        "statuses": dict(statuses),
        "snapshots": {name: json.loads((path / "manifest.json").read_text())["snapshot_id"]
                      for name, path in [("composition", SNAPSHOT), *SNAPSHOT_FOR.items()]},
        "decisions": table,
        "decisions_total": total,
        "decisions_attributed": attributed,
    }


# ── tamper: alter one constituent class of a sealed snapshot ────────────────

def _first(root: Path, pattern: str) -> Path:
    return sorted(root.glob(pattern))[0]


def _edit_json(path: Path, change) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    change(doc)
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def _route(root: Path) -> str:
    path = root / "tokenized/workload/dispatch.json"
    raw = path.read_text(encoding="utf-8")
    path.write_text(raw.replace('"addr": ', '"addr": 1', 1), encoding="utf-8")
    return "a routing target in the compiled dispatch table"


def _constituent(root: Path) -> str:
    path = _first(root, "canonical/workload/capability_contracts/*.json")
    _edit_json(path, lambda d: d.setdefault("frontmatter", {}).update({"tampered": True}))
    return f"a canonical artifact ({path.name})"


def _graph(root: Path) -> str:
    path = _first(root, "behavior_logic/workload/*/*.graph.json")
    _edit_json(path, lambda d: d["edges"].append({"from": d["entry"], "to": "EXIT_X",
                                                  "condition": "SUCCESS"}))
    return f"a published workflow graph ({path.name}): one added edge"


def _effect(root: Path) -> str:
    path = _first(root, "canonical/*/capability_side_effects/*.json")
    _edit_json(path, lambda d: d.setdefault("frontmatter", {}).update({"tampered": True}))
    return f"a side-effect declaration ({path.parent.parent.name}/{path.name})"


def _reference(root: Path) -> str:
    path = root / "artifact_index/index.json"

    def change(doc):
        fqdn = sorted(doc["artifacts"])[0]
        doc["artifacts"][fqdn]["canonical_path"] = "canonical/elsewhere.json"
    _edit_json(path, change)
    return "a reference in the artifact index"


def _profile(root: Path) -> str:
    _edit_json(root / "manifest.json", lambda d: d.update({"profile": "SOME_OTHER_PROFILE_V0"}))
    return "the profile the manifest claims"


def _identity(root: Path) -> str:
    _edit_json(root / "manifest.json",
               lambda d: d.update({"snapshot_id": "0" * 64}))
    return "the identity the manifest states"


def _extra(root: Path) -> str:
    (root / "canonical/workload/undeclared.json").write_text("{}", encoding="utf-8")
    return "an added file no constituent list declares"


def _removed(root: Path) -> str:
    path = _first(root, "canonical/workload/capability_transforms/*.json")
    path.unlink()
    return f"a removed constituent ({path.name})"


TAMPERS = [("route", _route), ("constituent", _constituent), ("graph", _graph),
           ("effect", _effect), ("reference", _reference), ("profile", _profile),
           ("identity", _identity), ("added_file", _extra), ("removed_file", _removed)]


def tamper() -> dict:
    from runtime.boot import boot

    results = []
    with tempfile.TemporaryDirectory() as tmp:
        control = Path(tmp) / "control"
        shutil.copytree(SNAPSHOT, control)
        try:
            boot(control)
            results.append({"class": "control", "altered": "nothing", "refused": False})
        except Exception as exc:  # the control must boot; report it if it does not
            results.append({"class": "control", "altered": "nothing", "refused": True,
                            "reason": str(exc)[:200]})

        for name, alter in TAMPERS:
            copy = Path(tmp) / name
            shutil.copytree(SNAPSHOT, copy)
            altered = alter(copy)
            try:
                boot(copy)
                results.append({"class": name, "altered": altered, "refused": False})
            except Exception as exc:
                results.append({"class": name, "altered": altered, "refused": True,
                                "reason": str(exc).splitlines()[0][:200]})
    return {"snapshot_id": json.loads((SNAPSHOT / "manifest.json").read_text())["snapshot_id"],
            "results": results}


if __name__ == "__main__":
    experiments = {"attribution": attribution, "tamper": tamper}
    name = sys.argv[1] if len(sys.argv) > 1 else ""
    if name not in experiments:
        sys.exit(f"usage: run_experiments.py {{{'|'.join(experiments)}}}")
    print(json.dumps(experiments[name](), indent=2))
