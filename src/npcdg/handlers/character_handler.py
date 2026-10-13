"""Character CRUD and archetype application for the GUI and CLI."""

from __future__ import annotations

from npcdg.models.character import Character, PersonalityAxes, VoiceProfile

ARCHETYPES: dict[str, PersonalityAxes] = {
    "merchant": PersonalityAxes(warmth=0.7, aggression=0.1, formality=0.5, verbosity=0.7, deception=0.4),
    "guard": PersonalityAxes(warmth=0.3, aggression=0.6, formality=0.6, verbosity=0.3, deception=0.1),
    "sage": PersonalityAxes(warmth=0.6, aggression=0.05, formality=0.8, verbosity=0.9, deception=0.2),
    "thief": PersonalityAxes(warmth=0.2, aggression=0.4, formality=0.2, verbosity=0.4, deception=0.9),
    "warlord": PersonalityAxes(warmth=0.1, aggression=0.95, formality=0.4, verbosity=0.5, deception=0.3),
}


def apply_archetype(character: Character, archetype: str) -> Character:
    if archetype not in ARCHETYPES:
        raise KeyError(f"unknown archetype: {archetype} (have: {', '.join(sorted(ARCHETYPES))})")
    return character.model_copy(update={"axes": ARCHETYPES[archetype]})


def make_stub(name: str, archetype: str = "sage") -> Character:
    return Character(
        name=name,
        role="",
        axes=ARCHETYPES[archetype],
        voice=VoiceProfile(),
    )