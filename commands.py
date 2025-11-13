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
            self.scope['IoC.Scope.Set'] = lambda: SetLocalScopeCommand()
            self.scope['IoC.Register'] = lambda *args: RegisterDependencyCommand(args[0], args[1])
            self.scope['IoC.Scopes.Scope'] = lambda: self.scope
            self.scope['IoC.Scopes.LocalScope'] = lambda: self.local_scope
            self.scope['IoC.Scopes.LocalScope.Empty'] = lambda: EmptyLocalScopeCommand()

            IoC[ICommand].resolve(
                'UpdateStrategy', DependencyResolver(self.scope, self.local_scope).resolve
            ).execute()

            print(IoC.strategy)
        self._is_executed = True


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


class SetLocalScopeCommand(ICommand):
    def execute(self) -> None:
        local_scope = IoC[threading.local].resolve('IoC.Scopes.LocalScope')
        local_scope.value = threading.get_ident()


class EmptyLocalScopeCommand(ICommand):
    def execute(self) -> None:
        local_scope = IoC[threading.local].resolve('IoC.Scopes.LocalScope')
        del local_scope.value
