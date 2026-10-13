"""Runtime dialogue engine — walks a DialogueTree and yields picked lines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from npcdg.models.dialogue import DialogueNode, DialogueTree


@dataclass
class TurnResult:
    node_id: str
    speaker: str
    text: str
    choices: list[tuple[str, str]]  # (label, next_node_id)


class DialogueEngine:
    """Walks one tree. Holds no global state; one engine per active conversation."""

    def __init__(self, tree: DialogueTree) -> None:
        if tree.root not in tree.nodes:
            raise ValueError(f"tree '{tree.name}' has no root node '{tree.root}'")
        self._tree = tree
        self._current: str = tree.root

    @property
    def current_node_id(self) -> str:
        return self._current

    def _node(self, node_id: str) -> DialogueNode:
        try:
            return self._tree.nodes[node_id]
        except KeyError as exc:
            raise KeyError(f"node '{node_id}' not in tree '{self._tree.name}'") from exc

    def advance(self, choice_index: int = 0) -> TurnResult:
        node = self._node(self._current)
        if node.kind == "line":
            if node.next:
                self._current = node.next[0]
        elif node.kind == "choice":
            if not (0 <= choice_index < len(node.next)):
                raise IndexError(f"choice_index {choice_index} out of range for node {node.node_id}")
            self._current = node.next[choice_index]
        elif node.kind in ("jump", "end"):
            if node.next:
                self._current = node.next[0]
        nxt = self._node(self._current)
        choices: list[tuple[str, str]] = []
        if nxt.kind == "choice":
            for i, edge in enumerate(nxt.next):
                label = self._node(edge).text[:48] or f"option {i}"
                choices.append((label, edge))
        return TurnResult(node_id=nxt.node_id, speaker=nxt.speaker, text=nxt.text, choices=choices)

    def walk(self, max_turns: int = 512) -> Iterator[TurnResult]:
        for _ in range(max_turns):
            result = self.advance()
            yield result
            if self._node(result.node_id).kind == "end":
                return
        raise RuntimeError("walk exceeded max_turns — tree likely has an unintended cycle")