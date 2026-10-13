"""Local LLM bridge — talks to an Ollama-compatible endpoint for line drafts."""

from __future__ import annotations

from dataclasses import dataclass

import httpx

from npcdg.config.settings import get_settings
from npcdg.models.character import Character


@dataclass
class DraftRequest:
    character: Character
    context: str
    max_tokens: int = 160
    temperature: float = 0.8


@dataclass
class DraftResponse:
    text: str
    model: str
    prompt_tokens: int
    completion_tokens: int


class LLMBridgeError(RuntimeError):
    """Raised when the local model endpoint is unreachable or returns junk."""


def _axes_block(character: Character) -> str:
    a = character.axes
    return (
        f"warmth={a.warmth:.2f} aggression={a.aggression:.2f} "
        f"formality={a.formality:.2f} verbosity={a.verbosity:.2f} deception={a.deception:.2f}"
    )


def draft_line(req: DraftRequest, *, model: str = "llama3.1:8b-instruct-q5_K_M") -> DraftResponse:
    s = get_settings()
    prompt = (
        f"You are {req.character.name}, {req.character.role or 'an NPC'}. "
        f"Register: {req.character.voice.register}. Axes: {_axes_block(req.character)}.\n"
        f"Backstory: {req.character.backstory}\n"
        f"Scene context: {req.context}\n"
        f"Write ONE line of dialogue. No narration, no quotes."
    )
    try:
        r = httpx.post(
            f"{s.ollama_endpoint}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": req.temperature, "num_predict": req.max_tokens},
            },
            timeout=60.0,
        )
        r.raise_for_status()
    except httpx.HTTPError as exc:
        raise LLMBridgeError(f"local model endpoint unreachable at {s.ollama_endpoint}: {exc}") from exc
    payload = r.json()
    return DraftResponse(
        text=payload.get("response", "").strip(),
        model=payload.get("model", model),
        prompt_tokens=int(payload.get("prompt_eval_count", 0)),
        completion_tokens=int(payload.get("eval_count", 0)),
    )