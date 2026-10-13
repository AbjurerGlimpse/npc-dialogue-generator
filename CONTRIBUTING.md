# Contributing to npc-dialogue-generator

`npc-dialogue-generator` is a Windows desktop tool for authoring AI character
and NPC dialogue trees — pack files, personality profiles, state machines, and
runtime renderers that plug into Unity, Godot, Unreal, and bare Python hosts.

This is a hobbyist open-source project. Contributions are welcome from writers,
gameplay engineers, and modders who want better NPCs in their games.

## Getting set up

```bat
git clone https://github.com/npc-dialogue-generator/npc-dialogue-generator
cd npc-dialogue-generator
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m npcdg.gui.app
```

Python 3.10+ on Windows 10/11. The desktop UI is PySide6. The runtime
exporters are pure Python and have no GUI dependency.

## What to work on

Check the `good first issue` and `help wanted` labels. Areas that always
need hands:

- New personality archetypes under `models/personalities/`
- Dialogue-tree validators under `handlers/`
- Runtime exporters under `services/exporters/`
- Tokenizer edge cases for CJK and RTL scripts

## Dialogue pack format

Packs are JSON manifests with a `characters/` directory of YAML profiles and
a `trees/` directory of dialogue graphs. Every pack must pass
`python -m npcdg.cli validate <pack_dir>` before a PR is merged. The
validator enforces:

- Every node has a stable `node_id` (uuid4 string)
- Every `next` edge points at an existing node
- Every character referenced in a tree exists in `characters/`
- Personality axes are in `[0.0, 1.0]`

## Style

- Python: PEP 8, type hints everywhere, `ruff` + `mypy --strict` clean
- Commit messages: imperative mood, one logical change per commit
- Tests: `pytest -q` must pass; new features need coverage under `tests/`

## Pull requests

Fork, branch off `main`, one feature per PR. Include a short clip or
screenshot if you touched the GUI. If you added a personality archetype,
attach a sample 20-line dialogue showing its voice.

## Code of conduct

Be decent. No harassment, no slurs, no targeting other contributors.
Moderation is a single maintainer with a ban hammer and a strong
preference for not using it.