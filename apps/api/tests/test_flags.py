"""Feature-flag behaviour."""
from __future__ import annotations

from app.core import flags


def test_unset_flag_uses_default(monkeypatch) -> None:
    monkeypatch.delenv("FLAG_LEDGER", raising=False)
    assert flags.is_enabled("ledger") is False
    assert flags.is_enabled("ledger", default=True) is True


def test_truthy_values(monkeypatch) -> None:
    for value in ("1", "true", "TRUE", "yes", "on", " On "):
        monkeypatch.setenv("FLAG_LEDGER", value)
        assert flags.is_enabled("ledger") is True, value


def test_falsy_values(monkeypatch) -> None:
    for value in ("0", "false", "no", "off", ""):
        monkeypatch.setenv("FLAG_LEDGER", value)
        assert flags.is_enabled("ledger") is False, value


def test_name_is_normalised(monkeypatch) -> None:
    monkeypatch.setenv("FLAG_MANAGED_WORKFORCE", "1")
    assert flags.is_enabled("managed-workforce") is True
