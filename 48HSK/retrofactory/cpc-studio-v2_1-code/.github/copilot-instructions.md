# Copilot Instructions for cpc-studio-v2_1-code

For requests related to CPCtelera game generation, game fixing, or scene_agent pipeline runs:

1. Use the skill `scene-agent-game-workflow` first.
2. Use the skill `scene-agent-master-review` before any promotion to `scene_agent/outputs/master`.
3. Treat `doc/technical/` as the primary source of technical truth.
4. Do not promote outputs to `scene_agent/outputs/master` until build, run, and visual checks pass.
5. Prefer targeted patches over full rewrites.
6. Keep final code free of temporary debug-only static rendering modes.

When a request conflicts with these rules, ask for explicit override before proceeding.
