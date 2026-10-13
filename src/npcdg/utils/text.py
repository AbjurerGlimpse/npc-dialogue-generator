"""Text utilities: smart-quote normalization, RTL/CJK detection, token estimate."""

from __future__ import annotations

import unicodedata

_SMART_MAP = {
    "\u2018": "'", "\u2019": "'",
    "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "--",
    "\u2026": "...",
}


def normalize_quotes(text: str) -> str:
    for src, dst in _SMART_MAP.items():
        text = text.replace(src, dst)
    return text


def is_rtl(text: str) -> bool:
    for ch in text:
        bidi = unicodedata.bidirectional(ch)
        if bidi in ("R", "AL"):
            return True
        if bidi == "L":
            return False
    return False


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~0.75 tokens per ASCII char, 1.5 per CJK char."""
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    wide_chars = len(text) - ascii_chars
    return int(ascii_chars * 0.75 + wide_chars * 1.5) + 1