"""Dialogue tree model — nodes, edges, and the pack that contains them."""

from __future__ import annotations

import uuid
from typing import Literal

from pydantic import BaseModel, Field

from npcdg.models.character import Character

NodeKind = Literal["line", "choice", "condition", "jump", "end"]


class DialogueNode(BaseModel):
    node_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    kind: NodeKind = "line"
    speaker: str = Field(min_length=1, max_length=64)
    text: str = Field(default="", max_length=2048)
    next: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)


class DialogueTree(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    root: str
    nodes: dict[str, DialogueNode] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list, max_length=32)


class DialoguePack(BaseModel):
    npcpack_version: int = 1
    name: str = Field(min_length=1, max_length=64)
    authors: list[str] = Field(default_factory=list, max_length=16)
    characters: dict[str, Character] = Field(default_factory=dict)
    trees: dict[str, DialogueTree] = Field(default_factory=dict)
    default_locale: str = "en-US"