"""PySide6 desktop entry for npc-dialogue-generator."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from npcdg.gui.pack_editor import PackEditorTab
from npcdg.gui.dialogue_editor import DialogueEditorTab
from npcdg.utils.logging import get_logger

log = get_logger("gui")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("npc-dialogue-generator 0.9.3")
        self.resize(1280, 820)
        tabs = QTabWidget(self)
        tabs.addTab(PackEditorTab(), "Pack")
        tabs.addTab(DialogueEditorTab(), "Dialogue Tree")
        self.setCentralWidget(tabs)


def run() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    win = MainWindow()
    win.show()
    log.info("main window shown")
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())