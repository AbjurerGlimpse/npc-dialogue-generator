"""Dialogue tree tab — flat list view with a run button for the local engine."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from npcdg.models.dialogue import DialogueTree
from npcdg.services.dialogue_engine import DialogueEngine


class DialogueEditorTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._engine: DialogueEngine | None = None
        self._transcript = QTextEdit(readOnly=True)
        self._choices = QListWidget()
        self._status = QLabel("no tree loaded")
        run = QPushButton("Advance")
        run.click