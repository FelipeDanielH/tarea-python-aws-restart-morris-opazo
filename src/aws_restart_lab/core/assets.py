from pathlib import Path


def get_asset_path(*parts: str) -> Path:
    candidates = (
        Path.cwd() / "assets" / Path(*parts),
        Path(__file__).resolve().parents[3] / "assets" / Path(*parts),
        Path(__file__).resolve().parents[1] / "assets" / Path(*parts),
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]
