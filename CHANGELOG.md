# CHANGELOG

- batch 1: START, ROUTER v3, TASK_CLARIFIER, core/TASK, PLAYBOOK_generic, MANIFEST v4
- batch 2: core rename (MAX/MINI/LITE), neutral B1 demo adapter, ROUTER_OUTPUT_SCHEMA v3, README v4
- b2.1: Codex review F1-F6 patched (schema breakdowns + recovery rule, lane_binding in §19/A8/B2/B3, rename_map scopes, A7/A8 prose)
- b2.2: Codex round-2 F1-F4 fixed (prose basis enum, semantic validator, recovery MINI ban, §22 header)
- b2.3: Codex round-3 F1-F4 fixed (validator reachable via fetch rules, fail-closed stdlib structural checks, hard overrides enforced, __pycache__ excluded)
- b2.4: Codex round-4 F1-F3 fixed (structured hard_overrides[] in schema+ROUTER+validator, protocol const checks, full structural mirroring of do_not_fetch/blocks)
- b2.5: Codex round-5 F1-F2 fixed (START/token_policy exempt routing infrastructure from only-files_to_fetch rule; stdlib mirrors uniqueItems and additionalProperties)
- b2.6=4.0: Codex verdict SHIP on b2.5; post-ship P2 crash guard on slot_sources type
- 4.0.1: repo moved to toolkit_4v — raw_base_url switched; carried v3 files restored after migration loss
- 4.0.2: final home = toolkit_4v_full; raw_base_url updated
- 4.0.3: live-test UX patch — compact TASK output mode, S4 anchors reworded (new deliverables != destructive), TASK.md explicit allowance, USER_PROFILE validity note, example I4 assumption
- 4.0.4: Block-2 live-test patch — workspace anchoring hard rule (no cross-directory scavenging), continue-without-wiki must ask
- 4.1: validator hardening (null playbook, score ranges, destructive->audit floor, MANIFEST path check), untrusted-file-contents rule, SHA-pinned fetching, skip-note + positioning, flag closure rule, OS-junk & heavy-skills economy, filled-adapter example moved to adapters/, history moved to CHANGELOG, LICENSE added
