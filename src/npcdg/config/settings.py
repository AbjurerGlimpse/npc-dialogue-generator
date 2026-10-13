"""Process-wide settings, loaded once and cached."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    cache_dir: Path = Field(default_factory=lambda: Path(os.getenv("NPCDG_CACHE", Path.home() / ".npcdg" / "cache")))
    weights_dir: Path = Field(default_factory=lambda: Path(os.getenv("NPCDG_WEIGHTS", Path.home() / ".npcdg" / "weights")))
    max_pack_bytes: int = 64 * 1024 * 1024
    max_nodes_per_tree: int = 50_000
    default_temperature: float = 0.8
    default_max_tokens: int = 160
    ollama_endpoint: str = "http://127.0.0.1:11434"
    log_level: str = "INFO"

    def ensure_dirs(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.weights_dir.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    s = Settings()
    s.ensure_dirs()
    return s