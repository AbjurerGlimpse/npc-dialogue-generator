"""Structured logger — one console handler, one rotating file handler."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from npcdg.config.settings import get_settings

_CONFIGURED = False


def configure_logging() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    s = get_settings()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    root = logging.getLogger("npcdg")
    root.setLevel(s.log_level)
    fh = RotatingFileHandler(s.cache_dir / "npcdg.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    fh.setFormatter(fmt)
    root.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    root.addHandler(sh)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    configure_logging()
    return logging.getLogger(f"npcdg.{name}")