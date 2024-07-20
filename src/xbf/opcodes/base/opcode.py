import abc

from .return_ import OpCodeReturn


class BaseOpCode(abc.ABC):
    __slots__ = ()

    def __call__(self) -> OpCodeReturn:
        return self._execute()

    @abc.abstractmethod
    def _execute(self) -> OpCodeReturn:
        raise NotImplementedError
