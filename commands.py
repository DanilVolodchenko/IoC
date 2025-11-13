from typing import NoReturn
import threading
from collections.abc import Callable

from interfaces import ICommand
from ioc import IoC
from resolver import DependencyResolver


class InitCommand(ICommand):
    scope = {}
    local_scope = threading.local()
    _lock = threading.RLock()
    _is_executed = False

    def execute(self) -> None:
        if self._is_executed:
            return

        with self._lock:
            self.scope['IoC.Scope.Empty'] = lambda: {}
            self.scope['IoC.Scope.Create'] = lambda *args: self.create_scope(args)
            self.scope['IoC.Scope.Parent'] = lambda *args: self.parent_scope()
            self.scope['IoC.Scope.Set'] = lambda *args: SetScopeCommand(args[0])
            self.scope['IoC.Scope.Current'] = lambda *args: SetScopeCommand(args[0])
            self.scope['IoC.Register'] = lambda *args: RegisterDependencyCommand(args[0], args[1])
            self.scope['IoC.Scopes.Scope'] = lambda *args: self.scope
            self.scope['IoC.Scopes.LocalScope'] = lambda *args: self.local_scope
            self.scope['IoC.Scopes.LocalScope.Empty'] = lambda: EmptyLocalScopeCommand()

            IoC[ICommand].resolve(
                'UpdateStrategy', DependencyResolver(self.scope, self.local_scope).resolve
            ).execute()

            print(IoC.strategy)
            self._is_executed = True

    def create_scope(self, *args) -> dict:
        new_scope = IoC[dict].resolve('IoC.Scope.Empty')

        if args:
            parent_scope = args[0]
        else:
            parent_scope = IoC[dict].resolve('IoC.Scope.Current')
        new_scope['IoC.Scope.Parent'] = parent_scope

        return new_scope

    def get_parent_scope(self) -> NoReturn:
        raise ValueError('Root scope has not parent scope')

    def get_current_scope(self):
        try:
            return IoC[threading.local].resolve('IoC.Scopes.LocalScope').value
        except AttributeError:
            return IoC[dict].resolve('IoC.Scopes.Scope')


class RegisterDependencyCommand(ICommand):
    def __init__(self, dependency: str, strategy: Callable) -> None:
        self.dependency = dependency
        self.strategy = strategy

    def execute(self) -> None:
        local_scope = IoC[threading.local].resolve('IoC.Scopes.LocalScope')
        scope = IoC[dict].resolve('IoC.Scopes.Scope')

        try:
            scope[local_scope.value] = {}
            scope[local_scope.value][self.dependency] = self.strategy
        except AttributeError:
            scope[self.dependency] = self.strategy


class SetScopeCommand(ICommand):
    def __init__(self, scope: dict) -> None:
        self.scope = scope

    def execute(self) -> None:
        local_scope = IoC[threading.local].resolve('IoC.Scopes.LocalScope')
        local_scope.value = self.scope


class EmptyLocalScopeCommand(ICommand):
    def execute(self) -> None:
        local_scope = IoC[threading.local].resolve('IoC.Scopes.LocalScope')
        del local_scope.value


# нужно чтобы в local_scope (лучше в current_scope) находились текущие зависимости и ссылка на родительский scope
# а в самом scope все зависимости который регаются при запуске InitCommand.execute()
# и когда приходится искать зависимости, то по цепочке проходить текущий и вложенные скопы