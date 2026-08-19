"""'Override without overwrite': manual corrections layered on top of raw
CRM data without ever mutating the original export.

Every override is stored alongside its original value and an author/
reason, so the raw CRM data stays intact for audit while the dashboard
can still reflect manually-corrected figures.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Override:
    deal_id: str
    field: str
    original_value: Any
    new_value: Any
    author: str
    reason: str
    created_at: _dt.datetime = field(default_factory=lambda: _dt.datetime.now(_dt.timezone.utc))


class OverrideStore:
    def __init__(self) -> None:
        self._overrides: dict[tuple, Override] = {}

    def set_override(
        self, deal_id: str, field_name: str, original_value: Any, new_value: Any, author: str, reason: str
    ) -> Override:
        override = Override(deal_id, field_name, original_value, new_value, author, reason)
        self._overrides[(deal_id, field_name)] = override
        return override

    def resolve(self, deal_id: str, field_name: str, raw_value: Any) -> Any:
        """Return the overridden value if one exists, else the raw CRM value."""
        override = self._overrides.get((deal_id, field_name))
        return override.new_value if override else raw_value

    def get_override(self, deal_id: str, field_name: str) -> Override | None:
        return self._overrides.get((deal_id, field_name))

    def __len__(self) -> int:
        return len(self._overrides)
