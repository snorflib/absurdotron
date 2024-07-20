from __future__ import annotations

import attrs

from src.ir import types


@attrs.frozen
class BFToken:
    owner: types.Owner | None = None
