#!/usr/bin/env bash
# Omission experiments for "Behavioral Authority in Sealed Models".
#
#   O1  a declared outcome left without a route   (collatz: CC_COMPUTE_SEQUENCES_V0, VIOLATION)
#   O2  a route decided by a non-deterministic atom (language model: CC_WRITE_MODEL_RESPONSE_V0)
#   O3  an operation outcome a step leaves out      (blockchain: CC_RESOLVE_ACTOR_V0, BACKEND_ERROR)
#
# O1 and O2 edit a COPY of a domain's model, never the workspace. O3 edits no model: the gap is
# already in the sealed working snapshot, and the case corrupts only its own data root. Run after a clean
# `regression.sh --all`, so the platform and inspector domains are compiled.
#
#   bash omission.sh [workspace]          default workspace: ~/protocol-governed-computing
set -euo pipefail
W="${1:-$HOME/protocol-governed-computing}"
T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
PY="$W/.venv/bin/python"

compile() { (cd "$W/protocol_compiler" && ./compile_domain.sh "$1" 2>&1 | grep -E "Build Summary|E701" || true); }

echo "== O1 control: unmodified collatz model"
cp -R "$W/conformance_workloads/workloads/collatz" "$T/collatz_control"; rm -rf "$T/collatz_control/snapshot"
compile "$T/collatz_control"

echo "== O1: CC_COMPUTE_SEQUENCES_V0 declares VIOLATION; its route is removed"
cp -R "$W/conformance_workloads/workloads/collatz" "$T/collatz"; rm -rf "$T/collatz/snapshot"
"$PY" - "$T/collatz/registry/workflows/WF_COLLATZ_CONJECTURE_V0.md" <<'EOF'
import sys; p = sys.argv[1]; s = open(p).read()
a = "        SUCCESS: CC_VERIFY_TERMINATION_V0\n        VIOLATION: EXIT_ERROR\n"
assert a in s; open(p, "w").write(s.replace(a, "        SUCCESS: CC_VERIFY_TERMINATION_V0\n", 1))
EOF
echo "-- construction"
compile "$T/collatz"
PGC_SOURCE_ROOTS="$W/software_governance/snapshot/compiled:$T/collatz/snapshot/compiled:$W/snapshot_inspector/snapshot/compiled" \
PGC_SNAPSHOT_OUT="$T/snap" PGC_SNAPSHOT_PROFILE=GOVERNANCE_SURFACE_PROFILE_V0 \
  "$W/snapshot_assembler/assemble.sh" 2>&1 | grep -E "round-trip|composition:" || true
echo "-- execution with a payload whose numbers the capability refuses"
"$W/protocol_runtime/run.sh" run --wf workload::WF_COLLATZ_CONJECTURE_V0 \
  --payload "$W/conformance_workloads/workloads/collatz/test_payloads/03_invalid_nack.json" \
  --data-root "$T/data" --snapshot "$T/snap" 2>&1 | grep -E "Error|Status" || true
REF="$(cd "$T/data" && find traces -name '*.jsonl' | head -1)"
"$PY" -m inspector --snapshot "$T/snap" --trace-root "$T/data" --json execution explain "$REF" \
  | "$PY" -c "import json,sys; d=json.load(sys.stdin); print('ending:', d['ending']['kind'], 'at', d['ending'].get('at'))"

echo "== O2 control: unmodified language-model model"
cp -R "$W/business_domains/causal_language_model" "$T/clm_control"; rm -rf "$T/clm_control/snapshot"
compile "$T/clm_control"

echo "== O2: the contract invokes the non-deterministic atom as a step it routes on"
cp -R "$W/business_domains/causal_language_model" "$T/clm"; rm -rf "$T/clm/snapshot"
"$PY" - "$T/clm/registry/model_response/capability_contracts/CC_WRITE_MODEL_RESPONSE_V0.md" <<'EOF'
import sys; p = sys.argv[1]; s = open(p).read()
a = "  - step: write_response\n    transform: causal_language_model::CT_WRITE_RESPONSE_V0\n"
b = ("  - step: offer_directly\n    transform: causal_language_model::CT_IMPURE_OFFER_NEXT_WORDS_V0\n"
     "    inputs:\n      reading: $.inputs.reading\n      text: $.inputs.reading\n"
     "      finished: $.inputs.reading\n      stopped_by: $.inputs.reading\n"
     "    outputs:\n      candidates: $.capability_result.candidates\n"
     "    result_surface:\n    - SUCCESS\n    - VIOLATION\n"
     "    on_result:\n      SUCCESS: continue\n      VIOLATION: exit\n") + a
assert a in s; open(p, "w").write(s.replace(a, b, 1))
EOF
compile "$T/clm"
echo "-- files left by the refused build: $(find "$T/clm/snapshot" -type f 2>/dev/null | wc -l | tr -d ' ')"

echo "== O3: CC_RESOLVE_ACTOR_V0's lookup step omits BACKEND_ERROR, which its operation declares"
P="$W/business_domains/blockchain/testbed/identity/test_payloads"
run() { "$W/protocol_runtime/run.sh" run --wf "$1" --payload "$2" --data-root "$T/o3" --snapshot "$W/snapshot" 2>&1 | grep -E "Error|Status" || true; }
echo "-- register the person"
run blockchain::WF_REGISTER_ACTOR_V0 "$P/01_register_actor.json"
REG="$T/o3/blockchain/identity/contact_address_registry.jsonl"
echo '{corrupt' >> "$REG"
echo "-- oracle: the registry's own answer to the lookup on the corrupted store"
"$PY" -c "
import sys
from capability_side_effects.implementation.CS_REGISTRY_V0.impl.executor import RegistryExecutor
print('RESOLVE:', RegistryExecutor({'path': sys.argv[1]}).resolve({'key_or_address': 'ada@example.test'})['result_status'])
" "$REG"
echo "-- accept the person"
run blockchain::WF_ACCEPT_ACTOR_V0 "$P/04_accept_actor.json"
"$PY" -c "import json,sys; print('actor state:', json.load(open(sys.argv[1]))['ada@example.test']['state'])" \
  "$T/o3/blockchain/identity/actors.json"
REF="$(cd "$T/o3" && find traces -path '*WF_ACCEPT_ACTOR_V0*' -name '*.jsonl' | head -1)"
"$PY" -c "
import json, sys
for line in open(sys.argv[1]):
    r = json.loads(line)
    if r.get('event_type') == 'CC_STEP' and r.get('step_op') in ('RESOLVE', 'READ'):
        print('trace step:', r['step_op'], 'result_status =', r['result_status'])
" "$T/o3/$REF"
"$PY" -m inspector --snapshot "$W/snapshot" --trace-root "$T/o3" --json execution explain "$REF" \
  | "$PY" -c "import json,sys; d=json.load(sys.stdin); print('ending:', d['ending']['kind'], d['ending'].get('ending'), '| undeclared routes:', len(d['undeclared_routes']))"
