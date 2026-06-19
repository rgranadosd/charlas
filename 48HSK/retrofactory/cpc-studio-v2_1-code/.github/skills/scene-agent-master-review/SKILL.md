---
name: scene-agent-master-review
description: "Use when reviewing a generated CPCtelera game before promoting to outputs/master. Runs technical, gameplay, HUD, collision, and visual validation gates with pass/fail verdict."
---

# Scene Agent Master Review

## Purpose
Provide a strict pre-promotion review for generated CPCtelera games.

This skill is used after implementation and before promoting any output directory to `scene_agent/outputs/master`.

## Inputs
- Candidate output directory under `scene_agent/outputs/<run_id>/`
- Generated gameplay code (`src/main.c`)
- Technical rules in `doc/technical/`

## Required Review Flow
1. Confirm candidate directory exists and build artifacts are present.
2. Review `src/main.c` for required mechanics and state handling.
3. Compile candidate output.
4. Run in Caprice32.
5. Validate visual and gameplay behavior.
6. Produce a pass/fail report with blocking findings.
7. Promote to `master` only when all blocking checks pass.

## Blocking Checks (must pass)
- Build passes without compiler errors.
- Runtime launches in emulator.
- Mode 0 coordinate discipline is correct:
  - X and widths in bytes.
  - Y and heights in scanlines.
- Palette initialized with `cpct_setPALColour`.
- Entity colors generated with `cpct_px2byteM0`.
- Runtime state initialized in `init_game` (no hidden default dependency).
- Collision logic uses full AABB (`right`, `bottom` with width/height).
- Ball launch flow is valid for breakout-like games:
  - attached to paddle before launch
  - launch by Space
  - no floor/paddle collision checks while not launched
- HUD layout is stable and non-overlapping.
- No debug static mode left enabled in final candidate.

## Preferred Evidence to Collect
- Build command and result summary.
- Emulator launch result summary.
- One clean visual capture or equivalent visual confirmation.
- List of key constants used for physics and HUD.

## Review Output Contract
Return a concise report with:
- `candidate`: output path reviewed
- `status`: `pass` or `fail`
- `blocking_findings`: list of failures
- `non_blocking_findings`: optional improvements
- `promotion_decision`: `promote` or `do_not_promote`
- `next_actions`: concrete steps to resolve failures

## Promotion Rule
Only allow promotion when:
- `status = pass`
- `blocking_findings` is empty

If not, keep candidate in timestamped folder and request fixes.
