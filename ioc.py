from typing import TypeVar, Generic, Any
from collections.abc import Callable

from interfaces import ICommand

T = TypeVar('T')


class UpdateIocStrategyCommand(ICommand):
    def __init__(self, strategy: Callable[[str, Any], Any]):
        self.strategy = strategy

    def execute(self) -> None:
        IoC.strategy = self.strategy


class IoC(Generic[T]):
    strategy: Callable[[str, Any], T]

    @classmethod
    def resolve(cls, dependency: str, *args) -> T:
        if dependency == 'UpdateStrategy':
            return UpdateIocStrategyCommand(args[0])
        return cls.strategy(dependency, *args)
