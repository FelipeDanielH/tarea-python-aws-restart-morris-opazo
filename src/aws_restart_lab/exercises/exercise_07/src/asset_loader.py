from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageTk
except ImportError:  # pragma: no cover - exercised only when optional dependency is absent.
    Image = None
    ImageTk = None

from .config import SPRITE_SCALE


class AssetLoader:
    def __init__(self, assets_dir: Path | None = None, scale: float = SPRITE_SCALE) -> None:
        self.assets_dir = assets_dir or Path(__file__).resolve().parents[1] / "assets"
        self.scale = scale
        self._image_cache: dict[tuple[str, tuple[int, int], bool], Any] = {}
        self._missing: set[Path] = set()

    def get_path(self, *parts: str) -> Path:
        return self.assets_dir.joinpath(*parts)

    def image(
        self,
        *parts: str,
        size: tuple[int, int],
        exact_size: bool = False,
    ) -> Any | None:
        if Image is None or ImageTk is None:
            return None

        path = self.get_path(*parts)
        scaled_size = self._scaled_size(size)
        cache_key = (str(path), scaled_size, exact_size)
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]
        if path in self._missing or not path.exists():
            self._missing.add(path)
            return None

        try:
            with Image.open(path) as source:
                image = source.convert("RGBA")
                bbox = image.getbbox()
                if bbox is not None:
                    image = image.crop(bbox)
                if path.name == "floor.png":
                    image = self._center_crop_to_ratio(image, scaled_size)
                image = self._resize(image, scaled_size, exact_size)
                photo = ImageTk.PhotoImage(image)
        except (OSError, ValueError):
            self._missing.add(path)
            return None

        self._image_cache[cache_key] = photo
        return photo

    def load_placeholder_assets(self) -> dict[str, str]:
        return {
            "tile": "#253242",
            "tile_alt": "#2a394a",
            "tile_outline": "#3f5267",
        }

    def _scaled_size(self, size: tuple[int, int]) -> tuple[int, int]:
        width, height = size
        return (max(1, round(width * self.scale)), max(1, round(height * self.scale)))

    def _resize(self, image: Any, size: tuple[int, int], exact_size: bool) -> Any:
        if exact_size:
            return image.resize(size, Image.Resampling.LANCZOS)

        max_width, max_height = size
        ratio = min(max_width / image.width, max_height / image.height)
        target_size = (max(1, round(image.width * ratio)), max(1, round(image.height * ratio)))
        return image.resize(target_size, Image.Resampling.LANCZOS)

    def _center_crop_to_ratio(self, image: Any, size: tuple[int, int]) -> Any:
        target_width, target_height = size
        target_ratio = target_width / target_height
        image_ratio = image.width / image.height

        if image_ratio > target_ratio:
            crop_width = round(image.height * target_ratio)
            left = max(0, (image.width - crop_width) // 2)
            return image.crop((left, 0, left + crop_width, image.height))

        crop_height = round(image.width / target_ratio)
        top = max(0, (image.height - crop_height) // 2)
        return image.crop((0, top, image.width, top + crop_height))
