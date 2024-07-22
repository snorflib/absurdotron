from __future__ import annotations

import abc
import typing


class SingletonMeta(abc.ABCMeta):
    _instances: dict[SingletonMeta, SingletonMeta] = {}

    def __call__(cls: SingletonMeta, *args: typing.Any, **kwargs: typing.Any) -> SingletonMeta:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
