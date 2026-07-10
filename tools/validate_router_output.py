#!/usr/bin/env python3
"""Semantic validator for Agent Wiki Router output v3 (protocol_version 4).

Fail-closed: full stdlib structural checks always run (protocol constants,
required fields, exact S/I key sets, score/basis enums, path patterns for
files_to_fetch / do_not_fetch / blocks), so a missing `jsonschema` library
never weakens validation. Then cross-field semantics JSON Schema cannot do:
breakdown sums vs aggregates, tier/role cuts, ROUTER hard overrides
(structured `hard_overrides[]`), safety floor, mode/file coherence.

Usage:
    python3 tools/validate_router_output.py output.json [schema.json]

Exit 0 = pass, exit 1 = findings printed, exit 2 = usage/IO error.
"""
import json, sys, os, re

CONSTS = {"router_version": 3, "protocol_version": 4}
BASIS = ["stated", "inferred", "asked", "assumed", "profile"]
RUBRIC_S = {"S1": [0, 5, 10], "S2": [0, 8, 15], "S3": [0, 5, 12, 20],
            "S4": [0, 10, 25], "S5": [0, 10, 25], "S6": [0, 10, 20],
            "S7": [0, 10, 20], "S8": [0, 8, 15], "S9": [0, 5, 10]}
RUBRIC_I = {"I1": [0, 10, 25], "I2": [0, 15, 25], "I3": [0, 15, 35],
            "I4": [0, 10, 15], "I5": [0, 5, 10], "I6": [-15, 0, 10]}
HARD_KINDS = ["destructive_ops", "high_stakes", "db_api_writes_or_expensive",
              "huge_corpus", "user_strict_audit"]
DERIVABLE = {"destructive_ops": ("S4", 25), "high_stakes": ("S5", 25),
             "db_api_writes_or_expensive": ("S7", 20), "huge_corpus": ("S3", 20)}
STRICT_AUDIT_RX = re.compile(r"strict[ _-]?audit|строг\w*\s+аудит", re.I)
REQUIRED_TOP = ["router_version", "protocol_version", "entry_mode", "task_type",
                "task_type_confidence", "playbook", "blocks", "bootstrap_mode",
                "bootstrap_tier", "daily_loop_file", "role_mode",
                "hard_overrides", "strictness_score", "independence_score",
                "strictness_breakdown", "independence_breakdown",
                "clarified_task", "assumptions", "corpus_size_hint",
                "files_to_fetch", "do_not_fetch", "reason",
                "independence_gap", "next_action"]
ENUMS = {"entry_mode": ["questionnaire", "file_driven"],
         "task_type": ["build", "analyze", "research", "write", "review", "operate", "plan", "other"],
         "task_type_confidence": ["high", "medium", "low"],
         "bootstrap_mode": ["new_project", "existing_agent_wiki", "recovery_needed"],
         "bootstrap_tier": ["TASK", "LITE", "MAX", None],
         "role_mode": ["SOLO", "DUAL", "FULL"],
         "corpus_size_hint": ["unknown", "small", "medium", "large", "huge"]}
SLOTS = ["goal", "inputs", "outputs", "format", "constraints", "done_criteria"]
FETCHABLE = re.compile(r"^(core|intake|playbooks|blocks|scenarios|orchestration|adapters|schemas|tools)/[A-Za-z0-9_./-]+\.(md|json|py)$|^USER_PROFILE\.md$")
BLOCK_RX = re.compile(r"^blocks/[A-Za-z0-9_-]+\.md$")
PLAYBOOK_RX = re.compile(r"^playbooks/PLAYBOOK_[A-Za-z0-9_-]+\.md$")

TIER_CUTS = [(0, 14, "TASK"), (15, 39, "LITE"), (40, 10**6, "MAX")]
ROLE_CUTS = [(-10**6, 24, "SOLO"), (25, 59, "DUAL"), (60, 10**6, "FULL")]
TIER_CORE = {"TASK": "core/TASK.md", "LITE": "core/LITE.md", "MAX": "core/PRINCIPLES_MAX.md"}
RANK_T = {"TASK": 0, "LITE": 1, "MAX": 2}
RANK_R = {"SOLO": 0, "DUAL": 1, "FULL": 2}
MINI = "core/PRINCIPLES_MINI.md"


def implied(score, cuts):
    for lo, hi, name in cuts:
        if lo <= score <= hi:
            return name


TOP_ALLOWED = set(REQUIRED_TOP) | {"task_type_secondary"}


def _str_list(o, key, f, pattern=None, allow_empty=True, what="path", unique=False):
    v = o.get(key)
    if not isinstance(v, list) or (not allow_empty and not v):
        f.append(f"STRUCT: {key} must be a {'non-empty ' if not allow_empty else ''}array")
        return
    if unique and len(set(map(str, v))) != len(v):
        f.append(f"STRUCT: {key} entries must be unique")
    for x in v:
        if not isinstance(x, str):
            f.append(f"STRUCT: {key} entry {x!r} is not a string")
        elif pattern and not pattern.match(x):
            f.append(f"STRUCT: {key} entry {x!r} is not a valid {what}")


def structural(o):
    """Stdlib structural checks — always run, independent of jsonschema."""
    f = []
    if not isinstance(o, dict):
        return ["STRUCT: output is not a JSON object"]
    for k in REQUIRED_TOP:
        if k not in o:
            f.append(f"STRUCT: missing required field '{k}'")
    for k in o:
        if k not in TOP_ALLOWED:
            f.append(f"STRUCT: unexpected top-level field '{k}' (additionalProperties=false)")
    for k, want in CONSTS.items():
        if k in o and o[k] != want:
            f.append(f"STRUCT: {k}={o[k]!r} must be {want}")
    for k, allowed in ENUMS.items():
        if k in o and o[k] not in allowed:
            f.append(f"STRUCT: {k}={o[k]!r} not in {allowed}")
    ho = o.get("hard_overrides")
    if not isinstance(ho, list):
        f.append("STRUCT: hard_overrides must be an array (possibly empty)")
    else:
        if len(set(map(str, ho))) != len(ho):
            f.append("STRUCT: hard_overrides entries must be unique")
        for x in ho:
            if x not in HARD_KINDS:
                f.append(f"STRUCT: hard_overrides entry {x!r} not in {HARD_KINDS}")
    if "task_type_secondary" in o:
        v = o["task_type_secondary"]
        if not isinstance(v, list) or any(x not in ENUMS["task_type"] for x in v):
            f.append("STRUCT: task_type_secondary must be an array of task_type values")
        elif len(set(v)) != len(v):
            f.append("STRUCT: task_type_secondary entries must be unique")
    for name, rubric in (("strictness_breakdown", RUBRIC_S), ("independence_breakdown", RUBRIC_I)):
        b = o.get(name)
        if not isinstance(b, dict):
            f.append(f"STRUCT: {name} missing or not an object")
            continue
        if set(b) != set(rubric):
            f.append(f"STRUCT: {name} keys {sorted(b)} != required {sorted(rubric)}")
        for k, v in b.items():
            if not isinstance(v, dict) or set(v) != {"score", "basis"}:
                f.append(f"STRUCT: {name}.{k} must be exactly {{score, basis}}")
                continue
            if k in rubric and v["score"] not in rubric[k]:
                f.append(f"STRUCT: {name}.{k}.score={v['score']} not in rubric {rubric[k]}")
            if v["basis"] not in BASIS:
                f.append(f"STRUCT: {name}.{k}.basis={v['basis']!r} not in {BASIS}")
    ct = o.get("clarified_task")
    if not isinstance(ct, dict):
        f.append("STRUCT: clarified_task missing or not an object")
    else:
        for k in SLOTS:
            if not isinstance(ct.get(k), str) or not ct[k].strip():
                f.append(f"STRUCT: clarified_task.{k} missing/empty")
        ss = ct.get("slot_sources")
        if not isinstance(ss, dict):
            f.append("STRUCT: slot_sources missing or not an object")
        else:
            for k in SLOTS:
                if ss.get(k) not in ("stated", "inferred", "asked", "assumed"):
                    f.append(f"STRUCT: slot_sources.{k}={ss.get(k)!r} invalid")
            extra_ss = set(ss) - set(SLOTS)
            if extra_ss:
                f.append(f"STRUCT: slot_sources unexpected fields {sorted(extra_ss)} (additionalProperties=false)")
        extra_ct = set(ct) - set(SLOTS) - {"slot_sources"}
        if extra_ct:
            f.append(f"STRUCT: clarified_task unexpected fields {sorted(extra_ct)} (additionalProperties=false)")
    _str_list(o, "files_to_fetch", f, FETCHABLE, allow_empty=False, what="fetchable path", unique=True)
    _str_list(o, "do_not_fetch", f, FETCHABLE, allow_empty=True, what="fetchable path", unique=True)
    _str_list(o, "blocks", f, BLOCK_RX, allow_empty=True, what="blocks/ path", unique=True)
    _str_list(o, "assumptions", f)
    _str_list(o, "reason", f)
    if not (isinstance(o.get("playbook"), str) and PLAYBOOK_RX.match(o["playbook"])):
        f.append(f"STRUCT: playbook={o.get('playbook')!r} invalid — must be a playbooks/PLAYBOOK_*.md path")
    if "independence_gap" in o and not isinstance(o["independence_gap"], bool):
        f.append("STRUCT: independence_gap must be boolean")
    if "next_action" in o and (not isinstance(o["next_action"], str) or not o["next_action"].strip()):
        f.append("STRUCT: next_action must be a non-empty string")
    return f


def manifest_paths():
    """Try to locate MANIFEST.json near CWD/script; return set of known file paths or None."""
    import os
    for cand in ("MANIFEST.json", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "MANIFEST.json")):
        try:
            with open(cand, encoding="utf-8") as fh:
                m = json.load(fh)
            if isinstance(m.get("files"), dict):
                return set(m["files"].keys())
        except Exception:
            continue
    return None


def semantic(o):
    f = []
    sb, ib = o.get("strictness_breakdown", {}), o.get("independence_breakdown", {})

    def sc(d, k):
        v = d.get(k)
        return v.get("score") if isinstance(v, dict) else None

    # sums
    ssum = sum(v.get("score", 0) for v in sb.values() if isinstance(v, dict))
    isum = sum(v.get("score", 0) for v in ib.values() if isinstance(v, dict))
    if ssum != o.get("strictness_score"):
        f.append(f"SUM: strictness_breakdown={ssum} != strictness_score={o.get('strictness_score')}")
    if isum != o.get("independence_score"):
        f.append(f"SUM: independence_breakdown={isum} != independence_score={o.get('independence_score')}")
    smax = sum(max(v) for v in RUBRIC_S.values()); imax = sum(max(v) for v in RUBRIC_I.values())
    smin = sum(min(v) for v in RUBRIC_S.values()); imin = sum(min(v) for v in RUBRIC_I.values())
    if not (isinstance(o.get("strictness_score"), int) and smin <= o["strictness_score"] <= smax):
        f.append(f"RANGE: strictness_score must be int {smin}..{smax}")
    if not (isinstance(o.get("independence_score"), int) and imin <= o["independence_score"] <= imax):
        f.append(f"RANGE: independence_score must be int {imin}..{imax}")

    known = manifest_paths()
    if known is not None:
        for path in (list(o.get("files_to_fetch", [])) + list(o.get("do_not_fetch", []))
                     + list(o.get("blocks", []))
                     + ([o["playbook"]] if isinstance(o.get("playbook"), str) else [])):
            if isinstance(path, str) and path not in known:
                f.append(f"PATH: {path} not present in MANIFEST files map")
    else:
        f.append("PATH: MANIFEST.json not found — cannot verify paths (fail closed)")

    # destructive requires audit lane or an explicit gap flag
    for crit, label in (("S4", "destructive"), ("S5", "high stakes")):
        if sc(sb, crit) == 25 and (sc(ib, "I3") or 0) < 15 and o.get("independence_gap") is not True:
            f.append(f"FLOOR: {crit}=25 ({label}) requires I3>=15 or independence_gap:true")
    for crit in ("S4", "S5"):
        v = sb.get(crit) if isinstance(sb.get(crit), dict) else {}
        if v.get("score") == 0 and v.get("basis") not in ("stated", "asked"):
            f.append(f"FLOOR: {crit}=0 requires basis stated|asked (got {v.get('basis')!r}) — risk absence must be stated or asked, never inferred")

    # safety floor
    for k in ("S4", "S5"):
        if isinstance(sb.get(k), dict) and sb[k].get("basis") == "assumed":
            f.append(f"SAFETY FLOOR: {k}.basis='assumed' is forbidden")

    mode, tier, role = o.get("bootstrap_mode"), o.get("bootstrap_tier"), o.get("role_mode")
    fetch = o.get("files_to_fetch") or []
    reason = o.get("reason") or []
    ho = [x for x in (o.get("hard_overrides") or []) if x in HARD_KINDS]

    # hard_overrides <-> breakdown consistency (four machine-derivable kinds)
    for kind, (crit, val) in DERIVABLE.items():
        derived = sc(sb, crit) == val
        declared = kind in ho
        if derived and not declared:
            f.append(f"OVERRIDE: breakdown implies '{kind}' ({crit}={val}) but hard_overrides does not declare it")
        if declared and not derived:
            f.append(f"OVERRIDE: '{kind}' declared but {crit}!={val} — inconsistent with breakdown")
    # strict-audit heuristic: free text must not replace the structured flag
    if "user_strict_audit" not in ho:
        for x in reason + (o.get("assumptions") or []):
            if isinstance(x, str) and STRICT_AUDIT_RX.search(x):
                f.append("OVERRIDE: strict audit mentioned in free text — declare 'user_strict_audit' in hard_overrides[]")
                break

    # mode coherence
    if mode == "existing_agent_wiki":
        if tier is not None: f.append("MODE: existing_agent_wiki requires bootstrap_tier=null")
        if o.get("daily_loop_file") != MINI: f.append("MODE: existing_agent_wiki requires daily_loop_file=MINI")
        if MINI not in fetch: f.append("MODE: existing_agent_wiki must fetch MINI")
    else:
        if o.get("daily_loop_file") is not None: f.append("MODE: daily_loop_file must be null outside existing_agent_wiki")
        if MINI in fetch: f.append("MODE: MINI must not be fetched for new_project/recovery")
    if mode == "recovery_needed" and tier != "MAX":
        f.append("MODE: recovery_needed requires bootstrap_tier=MAX")

    # tier vs score + overrides (new_project only; recovery is MAX by rule)
    if mode == "new_project":
        req = implied(o.get("strictness_score", 0), TIER_CUTS) or "TASK"
        if ho:
            req = "MAX"
        if tier not in RANK_T:
            f.append(f"TIER: invalid bootstrap_tier={tier!r} for new_project")
        elif RANK_T[tier] < RANK_T[req]:
            why = f" (hard_overrides: {', '.join(ho)})" if ho else ""
            f.append(f"TIER: declared {tier} below required {req}{why} — downgrades are forbidden")
        elif RANK_T[tier] > RANK_T[req] and not reason:
            f.append(f"TIER: declared {tier} above required {req} needs a non-empty reason[]")
        if not any(isinstance(x, str) and x.startswith("playbooks/") for x in fetch):
            f.append("FETCH: new_project must fetch a playbook")
        if o.get("playbook") and o["playbook"] not in fetch:
            f.append("FETCH: selected playbook missing from files_to_fetch")

    # tier core file present
    if tier in TIER_CORE and TIER_CORE[tier] not in fetch:
        f.append(f"FETCH: tier {tier} requires {TIER_CORE[tier]} in files_to_fetch")

    # role vs score + overrides + engine cap
    req_r = implied(o.get("independence_score", 0), ROLE_CUTS) or "SOLO"
    if sc(sb, "S4") == 25 and sc(ib, "I5") == 10 and RANK_R[req_r] < RANK_R["FULL"]:
        req_r = "FULL"
    uncapped = req_r
    if sc(ib, "I4") == 0:
        req_r = "SOLO"
        if RANK_R[uncapped] > RANK_R["SOLO"] and o.get("independence_gap") is not True:
            f.append(f"ROLE: one engine caps role to SOLO while {uncapped} is needed — independence_gap must be true")
    if role in RANK_R:
        if RANK_R[role] < RANK_R[req_r]:
            f.append(f"ROLE: declared {role} below required {req_r} — downgrades are forbidden")
        elif RANK_R[role] > RANK_R[req_r] and sc(ib, "I4") == 0:
            f.append(f"ROLE: declared {role} impossible with one engine (I4=0) — cap is SOLO")
        elif RANK_R[role] > RANK_R[req_r] and not reason:
            f.append(f"ROLE: declared {role} above required {req_r} needs a non-empty reason[]")
    return f


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    try:
        o = json.load(open(sys.argv[1]))
    except Exception as e:
        print(f"IO: cannot read/parse {sys.argv[1]}: {e}"); sys.exit(2)

    findings = structural(o)
    print("structural (stdlib): " + ("PASS" if not findings else "FAIL"))

    schema_path = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "schemas", "ROUTER_OUTPUT_SCHEMA.json")
    try:
        import jsonschema
        jsonschema.validate(o, json.load(open(schema_path)))
        print("schema (jsonschema): PASS")
    except ImportError:
        print("schema (jsonschema): unavailable — stdlib structural checks above are authoritative")
    except FileNotFoundError:
        print("schema (jsonschema): schema file not found — stdlib structural checks above are authoritative")
    except Exception as e:
        print(f"schema (jsonschema): FAIL — {getattr(e, 'message', e)}")
        findings.append("SCHEMA: jsonschema validation failed")

    findings += semantic(o)
    sem = [x for x in findings if not x.startswith("STRUCT")]
    print("semantic: " + ("PASS" if not sem else "FAIL"))
    if findings:
        for x in findings: print("  -", x)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
