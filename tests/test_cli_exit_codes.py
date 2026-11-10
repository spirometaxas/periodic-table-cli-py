"""Exit codes for the periodic-table-cli entry point (offline)."""

import sys

import pytest

from periodic_table_cli import cli


def test_non_tty_interactive_mode_exits_nonzero(monkeypatch, capsys):
    """Refusing to run interactively without a tty must exit nonzero."""
    monkeypatch.setattr(sys, "argv", ["periodic-table-cli"])
    assert not sys.stdout.isatty()
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code == 1
    assert "only supported within a terminal" in capsys.readouterr().out


def test_help_still_exits_zero(monkeypatch, capsys):
    """--help keeps its success exit code."""
    monkeypatch.setattr(sys, "argv", ["periodic-table-cli", "--help"])
    with pytest.raises(SystemExit) as exc:
        cli.main()
    assert exc.value.code in (None, 0)
    assert "Usage:" in capsys.readouterr().out
