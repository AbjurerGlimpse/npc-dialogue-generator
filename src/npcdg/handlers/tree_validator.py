"""Structural validation of dialogue trees before export."""

from __future__ import annotations

from dataclasses import dataclass

from npcdg.models.dialogue import DialoguePack, DialogueTree


@dataclass(frozen=True)
class ValidationProblem:
    node_id: str
    message: str


def _validate_tree(tree: DialogueTree, pack: DialoguePack) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    if tree.root not in tree.nodes:
        problems.append(ValidationProblem(tree.root, "root node missing"))
    for node_id, node in tree.nodes.items():
        if node.speaker not in pack.characters:
            problems.append(ValidationProblem(node_id, f"unknown speaker '{node.speaker}'"))
        for edge in node.next:
            if edge not in tree.nodes:
                problems.append(ValidationProblem(node_id, f"dangling next -> {edge}"))
        if node.kind == "end" and node.next:
            problems.append(ValidationProblem(node_id, "end node has outgoing edges"))
        if node.kind == "line" and len(node.next) > 1:
            problems.append(ValidationProblem(node_id, "line node has multiple successors"))
    return problems


def validate_tree(pack: DialoguePack) -> list[ValidationProblem]:
    out: list[ValidationProblem] = []
    for tree in pack.trees.values():
        out.extend(_validate_tree(tree, pack))
    return out