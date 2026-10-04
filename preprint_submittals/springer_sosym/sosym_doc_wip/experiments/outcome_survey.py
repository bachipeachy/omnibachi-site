"""Survey the pinned snapshot for undecided outcomes: step surfaces narrower than their
operation, and workflow acts whose surfaced outcomes have no route."""
import json, sys
from pathlib import Path

root = Path(sys.argv[1]) / "canonical"
arts = {}
for p in root.rglob("*.json"):
    if p.name == "metadata.json":
        continue
    d = json.loads(p.read_text())
    if "fqdn_id" in d:
        arts[d["fqdn_id"]] = d

def fm(f): return arts[f]["frontmatter"]

steps, flows, gates = [], [], []
surfaced = {}
for f, d in sorted(arts.items()):
    m = d["frontmatter"]
    if m.get("artifact_kind") != "CAPABILITY_CONTRACT":
        continue
    core = m["core"]
    out = set()
    rsc = core.get("result_status_contract", {})
    if rsc.get("on_input_failure"):
        out.add(rsc["on_input_failure"])
    for s in core.get("pipeline", []):
        for code, act in s.get("on_result", {}).items():
            if act == "exit":
                out.add(code)
        cs = s.get("side_effect")
        if cs and cs in arts:
            op = fm(cs)["core"]["operations"].get(s["op"], {})
            declared = set(op.get("result_status_values", []))
            surface = set(s.get("result_surface", []))
            missing = sorted(declared - surface)
            if missing:
                steps.append((f, s["step"], s["op"], cs, sorted(surface), missing, s.get("on_result", {})))
    surfaced[f] = out

for f, d in sorted(arts.items()):
    m = d["frontmatter"]
    if m.get("artifact_kind") != "WORKFLOW":
        continue
    nodes = m["core"]["nodes"]
    sup = bool(m.get("superseded_by"))
    start = m["core"]["start_node"]
    for name, n in nodes.items():
        if n["type"] == "IN" and name == start:
            routed = set(n.get("next", {}))
            if not {"ACK", "NACK"} <= routed:
                gates.append((f, name, sorted(routed)))
        if n["type"] != "CC":
            continue
        cc = n.get("fqdn_id")
        miss = sorted(surfaced.get(cc, set()) - set(n.get("next", {})))
        if miss:
            flows.append((f, sup, name, miss, n.get("next", {})))

print(f"STEP GAPS {len(steps)}")
for s in steps: print("  ", s[0], s[1], s[2], s[3].split('::')[1], "surface", s[4], "missing", s[5], "on_result", s[6])
print(f"WORKFLOW GAPS {len(flows)}")
for w in flows: print("  ", w[0], "(superseded)" if w[1] else "", w[2], "missing", w[3], "routes", w[4])
print(f"GATE GAPS {len(gates)}")
for g in gates: print("  ", g)
