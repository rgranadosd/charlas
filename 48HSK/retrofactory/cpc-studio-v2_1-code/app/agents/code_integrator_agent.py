from app.schemas.outputs import IntegrationOutput


def run() -> IntegrationOutput:
    return IntegrationOutput(
        files_to_create=[
            "inc/game.h",
            "inc/input.h",
            "inc/player.h",
            "src/main.c",
            "src/systems/input.c",
            "src/entities/player.c",
            "src/scene_game.c",
        ],
        files_to_modify=[],
        integration_notes="Creates a real starter workspace and can later evolve to patch existing CPCtelera projects."
    )
