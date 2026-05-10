from app.schemas.outputs import BuildValidationOutput
from app.schemas.outputs import BuildOutput


def run(build_output: BuildOutput | None) -> BuildValidationOutput:
    if build_output is None:
        return BuildValidationOutput(
            expected_entrypoints=[],
            expected_headers=[],
            validation_notes="No build output received from build_agent."
        )

    expected_artifacts = {".cdt", ".dsk"}
    found_artifacts = set()

    for artifact in build_output.artifacts or []:
        if artifact.endswith(".cdt"):
            found_artifacts.add(".cdt")
        elif artifact.endswith(".dsk"):
            found_artifacts.add(".dsk")

    missing = sorted(expected_artifacts - found_artifacts)

    if build_output.success and not missing:
        notes = "Build validation passed: CPCtelera produced the expected final artifacts (.cdt and .dsk)."
    elif build_output.success and missing:
        notes = (
            "Build command finished successfully, but some expected final artifacts are missing: "
            + ", ".join(missing)
        )
    else:
        notes = (
            f"Build validation failed. Return code: {build_output.return_code}. "
            f"stderr: {(build_output.stderr or '')[:500]}"
        )

    return BuildValidationOutput(
        expected_entrypoints=["src/main.c"],
        expected_headers=[],
        validation_notes=notes,
    )
