from __future__ import annotations

import abc

from src.ir import types


class BaseConstraint(abc.ABC):
    __slots__ = ("owner",)
    owner: types.Owner
