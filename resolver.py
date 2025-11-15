from typing import TYPE_CHECKING

from interfaces import IResolver

if TYPE_CHECKING:
    from commands import InitCommand


class DependencyResolver(IResolver):
    def __init__(self, init_command: 'InitCommand') -> None:
        self.init_command = init_command

    def resolve(self, dependency: str, *args):
        try:
            scope: dict = self.init_command.current_scope.value
        except AttributeError:
            scope: dict = self.init_command.main_scope

        while True:
            depend = scope.get(dependency)
            if depend:
                return depend(*args)

            try:
                scope = scope['IoC.Scope.Parent'](*args)
            except AttributeError:
                raise Exception(f'Зависимость {dependency} не была найдена')
