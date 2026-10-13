"""Character profile model — the authored personality of one NPC."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Axis = Annotated[float, Field(ge=0.0, le=1.0)]  # noqa: F821 — declared below


from typing import Annotated  # noqa: E402


class PersonalityAxes(BaseModel):
    """Five-axis personality vector. All values in [0.0, 1.0]."""

    warmth: float = Field(default=0.5, ge=0.0, le=1.0)
    aggression: float = Field(default=0.3, ge=0.0, le=1.0)
    formality: float = Field(default=0.4, ge=0.0, le=1.0)
    verbosity: float = Field(default=0.5, ge=0.0, le=1.0)
    deception: float = Field(default=0.1, ge=0.0, le=1.0)


class VoiceProfile(BaseModel):
    """Surface-level voice — how the character sounds regardless of content."""

    register: Literal["plain", "archaic", "clinical", "street", "noble", "soldier"] = "plain"
    tics: list[str] = Field(default_factory=list, max_length=16)
    banned_phrases: list[str] = Field(default_factory=list, max_length=64)


class Character(BaseModel):
    """A single authored NPC. Names are unique within a pack."""

    name: str = Field(min_length=1, max_length=64)
    role: str = Field(default="", max_length=128)
    faction: str = Field(default="", max_length=64)
    axes: PersonalityAxes = Field(default_factory=PersonalityAxes)
    voice: VoiceProfile = Field(default_factory=VoiceProfile)
    backstory: str = Field(default="", max_length=4096)
    greeting: str = Field(default="", max_length=512)

    @field_validator("name")
    @classmethod
    def _name_no_path_chars(cls, v: str) -> str:
        if any(c in v for c in "/\\:*?\"<>|"):
            raise ValueError("character name contains filesystem-reserved characters")
        return v.strip()