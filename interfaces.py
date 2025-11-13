import abc


class ICommand(abc.ABC):
    @abc.abstractmethod
    def execute(self) -> None:
        """Выполняет какое-то действие."""


class IResolver(abc.ABC):
    @abc.abstractmethod
    def resolve(self, dependency: str, *args) -> None:
        """Разрешает зависимости."""
