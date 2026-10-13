"""Pack tab: load a .npcpack, list characters, edit axes."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from npcdg.handlers.pack_loader import PackLoadError, load_pack
from npcdg.models.dialogue import DialoguePack


class PackEditorTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._pack: DialoguePack | None = None
        self._path = QLabel("no pack loaded")
        self._list = QListWidget()
        open_btn = QPushButton("Open .npcpack…")
        open_btn.clicked.connect(self._open)
        bar = QHBoxLayout()
        bar.addWidget(open_btn)
        bar.addWidget(self._path, 1)
        root = QVBoxLayout(self)
        root.addLayout(bar)
        root.addWidget(self._list, 1)

    def _open(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, "Select a .npcpack directory")
        if not chosen:
            return
        try:
            self._pack = load_pack(Path(chosen))
        except PackLoadError as exc:
            self._path.setText(f"load failed: {exc}")
            return
        self._path.setText(str(chosen))
        self._list.clear()
        for name, ch in sorted(self._pack.characters.items()):
            self._list.addItem(f"{name} — {ch.role or 'unroled'} [{ch.voice.register}]")
        self._list.setSortingEnabled(False)
        self._list.setFocusPolicy(Qt.FocusPolicy.StrongFocus)