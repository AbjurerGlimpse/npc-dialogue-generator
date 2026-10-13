"""Godot 4 exporter — emits .tres Resource files consumable by GDScript."""

from __future__ import annotations

from pathlib import Path

from npcdg.models.dialogue import DialoguePack


_HEADER = '[gd_resource type="Resource" script_class="NPCDialogueTree" load_steps=2 format=3]\n'


def export_godot(pack: DialoguePack, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for tree in pack.trees.values():
        lines = [_HEADER]
        lines.append(f'[resource]\nname = "{tree.name}"\nroot_id = "{tree.root}"\n')
        lines.append("nodes = [\n")
        for node in tree.nodes.values():
            escaped = node.text.replace('"', '\\"')
            lines.append(
                f'  {{"id":"{node.node_id}","speaker":"{node.speaker}",'
                f'"text":"{escaped}","next":{node.next!r}}},\n'
            )
        lines.append("]\n")
        (out_dir / f"{tree.name}.tres").write_text("".join(lines), encoding="utf-8")