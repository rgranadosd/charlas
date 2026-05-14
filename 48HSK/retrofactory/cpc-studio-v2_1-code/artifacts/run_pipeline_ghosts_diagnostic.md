# run_pipeline_ghosts Diagnostic (refreshed)

- refreshed_at_utc: 2026-05-13T20:27:10Z
- source_pipeline_output: /Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code/pipeline_ghosts_output.json
- source_pipeline_stderr: /Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code/pipeline_ghosts_stderr.log
- generated_project_path: /Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code/generated_projects/run99692
- note: This report intentionally replaces stale diagnostics that still showed the old contract_validation fail.

## 1) Current status

- contract_validation_status: pass
- pipeline_reaches_build_output: yes
- build_output_success: no
- build_return_code: 2
- build_validation_status: fail
- qa_status: fail

## 2) Route observed in latest stderr

~~~text
orchestrator_node -> narrative_node -> design_node -> art_node -> tech_node
-> contractvalidationnode (status: pass)
-> integration_node -> build_node -> build_validation_node -> qa_node -> compose_node
~~~

## 3) font_gothic include reconciliation

- src/systems/hud.c includes: systems/hud.h, data/hud/elements.h
- hud.c includes font_gothic.h: no
- font_gothic.h exists in generated run99692 tree: no
- search for font_gothic.h/fontgothic.h in run99692: no matches

Conclusion: the old blocker MISSING_LOCAL_INCLUDE(font_gothic.h) is not present in the latest run.

## 4) Current blocker (latest run)

- Link error in build_output: Multiple definition of _tileset_ruins_data
- Duplicate tileset symbols: tileset_ruins.c vs tilesetruins.c
- Missing module from validation: src/entities/projectile.c
- Missing/invalid build reference: src/data/sprites/itesgargoyle.c

## 5) Summary machine-readable

~~~json
{
  "run_completed": true,
  "stuck_node": "",
  "contract_validation_status": "pass",
  "build_success": false,
  "build_return_code": 2,
  "enemy_sanitized": false,
  "enemydefs_present": false,
  "current_blocker": "build_output link failure: duplicate symbol _tileset_ruins_data; missing projectile.c/itesgargoyle.c",
  "generated_project_path": "/Users/rafagranados/Develop/charlas/48HSK/retrofactory/cpc-studio-v2_1-code/generated_projects/run99692"
}
~~~