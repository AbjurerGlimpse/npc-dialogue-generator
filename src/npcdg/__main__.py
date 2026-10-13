"""``python -m npcdg`` bootstrap — routes to the GUI by default, CLI with args."""

from __future__ import annotations

import sys

from npcdg.cli import main as cli_main


def main() -> int:
    if len(sys.argv) > 1:
        return cli_main()
    from npcdg.gui.app import run

    return run()


if __name__ == "__main__":
    raise SystemExit(main())