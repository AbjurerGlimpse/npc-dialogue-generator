"""Loads a .npcpack directory into a validated DialoguePack."""

from __future__ import annotations

import json
from pathlib import Path

from ruamel.yaml import YAML

from npcdg.config.settings import get_settings
from npcdg.models.character import Character
from npcdg.models.dialogue import DialoguePack, DialogueTree


class PackLoadError(RuntimeError):
    """Raised when a pack is missing, oversized, or malformed."""


_yaml = YAML(typ="safe")


def _read_manifest(pack_dir: Path) -> dict:
    manifest = pack_dir / "pack.json"
    if not manifest.is_file():
        raise PackLoadError(f"missing pack.json in {pack_dir}")
    if manifest.stat().st_size > get_settings().max_pack_bytes:
        raise PackLoadError("pack.json exceeds max_pack_bytes")
    try:
        return json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PackLoadError(f"pack.json is not valid JSON: {exc}") from exc


def load_pack(pack_dir: Path) -> DialoguePack:
    pack_dir = pack_dir.resolve()
    raw = _read_manifest(pack_dir)

    characters: dict[str, Character] = {}
    for profile in sorted((pack_dir / "characters").glob("*.yaml")):
        try:
            data = _yaml.load(profile.read_text(encoding="utf-8"))
            ch = Character.model_validate(data)
        except Exception as exc:  # noqa: BLE001 — surfaced as PackLoadError on purpose
            raise PackLoadError(f"{profile.name}: {exc}") from exc
        characters[ch.name] = ch

    trees: dict[str, DialogueTree] = {}
    for tree_file in sorted((pack_dir / "trees").glob("*.json")):
        try:
            tree = DialogueTree.model_validate_json(tree_file.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            raise PackLoadError(f"{tree_file.name}: {exc}") from exc
        trees[tree.name] = tree

    return DialoguePack(
        npcpack_version=raw.get("npcpack_version", 1),
        name=raw.get("name", pack_dir.name),
        authors=raw.get("authors", []),
        characters=characters,
        trees=trees,
        default_locale=raw.get("default_locale", "en-US"),
    )