---
name: scene-agent-game-workflow
description: "Use when generating, fixing, or validating CPCtelera games with scene_agent pipeline. Enforces technical doc retrieval from doc/technical, compile/run validation, visual checks, and safe promotion to master."
---

# Scene Agent Game Workflow

## Purpose
Standardize CPCtelera game generation in this repository so outputs are playable,
verifiable, and do not repeat known failures.

## Inputs
- User prompt for gameplay requirements.
- Technical knowledge from `doc/technical/`.
- Existing project context under `scene_agent/`.

## Mandatory Steps
1. Read technical docs in `doc/technical/` before code generation.
2. Build and use TECH-RAG context from those docs.
3. Define an explicit implementation contract before writing code.
4. Generate or patch code according to the contract.
5. Compile the generated output.
6. Run the build in Caprice32.
7. Validate visuals and controls.
8. Promote to `outputs/master` only if checks pass.

## Hard Constraints
- Mode 0 coordinate discipline:
  - X and widths in bytes.
  - Y and heights in scanlines.
- Palette via `cpct_setPALColour`.
- Entity colors via `cpct_px2byteM0`.
- Runtime state initialized in `init_game`.
- AABB collisions use full entity box (`w`, `h`), not a single point.
- HUD uses fixed byte layout and no overlap.
- Debug static modes must be disabled in final output.

## Breakout-Specific Rules
- Ball starts attached to paddle.
- Space launches ball.
- Paddle, wall, floor, and brick collisions validated at runtime.
- Life loss resets ball to attached state.

## Validation Checklist
- Build succeeds.
- Emulator launch succeeds.
- Ball, paddle, bricks, and HUD visible.
- Controls respond correctly.
- Core collisions are correct.
- No temporary diagnostics left enabled.

## Output Contract
Return:
- Paths of changed files.
- Build/run status.
- Validation summary.
- Promotion decision (`master` or `not ready`).

## Failure Recovery
If build passes but gameplay is wrong:
1. Add temporary visual diagnostics.
2. Re-test with capture.
3. Apply targeted fix.
4. Remove diagnostics before finalizing.
