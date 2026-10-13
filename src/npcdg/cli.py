"""Command-line surface for headless pack validation, export, and linting."""

from __future__ import annotations

import sys
from pathlib import Path

import typer
from rich.console import Console

from npcdg.handlers.pack_loader import PackLoadError, load_pack
from npcdg.handlers.tree_validator import validate_tree
from npcdg.services.exporters.unity_export import export_unity
from npcdg.services.exporters.godot_export import export_godot

app = typer.Typer(add_completion=False, help="npc-dialogue-generator CLI")
console = Console()


@app.command()
def validate(pack_dir: Path) -> None:
    """Validate a pack directory. Exit 1 on any structural error."""
    try:
        pack = load_pack(pack_dir)
    except PackLoadError as exc:
        console.print(f"[red]load failed:[/red] {exc}")
        raise typer.Exit(1)
    problems = validate_tree(pack)
    if problems:
        for p in problems:
            console.print(f"[yellow]{p.node_id}[/yellow]: {p.message}")
        raise typer.Exit(1)
    console.print(f"[green]ok[/green] {pack.name} · {len(pack.characters)} chars · {len(pack.trees)} trees")


@app.command()
def export(pack_dir: Path, target: str = typer.Option("unity", "--target", "-t")) -> None:
    """Export a validated pack to a runtime format."""
    pack = load_pack(pack_dir)
    out = pack_dir / "export" / target
    if target == "unity":
        export_unity(pack, out)
    elif target == "godot":
        export_godot(pack, out)
    else:
        console.print(f"[red]unknown target:[/red] {target}")
        raise typer.Exit(2)
    console.print(f"[green]exported[/green] {target} -> {out}")


def main() -> int:
    try:
        app()
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


if __name__ == "__main__":
    sys.exit(main())