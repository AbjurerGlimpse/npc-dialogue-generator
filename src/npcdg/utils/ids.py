"""Stable IDs for nodes, characters, and cache keys."""

from __future__ import annotations

import hashlib
import uuid


def new_node_id() -> str:
    return str(uuid.uuid4())


def short_id(seed: str, length: int = 8) -> str:
    return hashlib.blake2b(seed.encode("utf-8"), digest_size=length).hexdigest()