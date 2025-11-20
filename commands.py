from typing import NoReturn
import threading
from collections.abc import Callable

from interfaces import ICommand
from ioc import IoC
from resolver import DependencyResolver


class InitCommand(ICommand):
    main_scope = {}
    current_scope = threading.local()
    _lock = threading.RLock()
    _is_executed = False

    def execute(self) -> None:
        if self._is_executed:
            return

        with self._lock:
            self.main_scope['IoC.Scope.Empty'] = lambda *args: {}
            self.main_scope['IoC.Scope.Create'] = lambda *args: self.create_new_scope(*args)
            self.main_scope['IoC.Scope.Parent'] = lambda *args: self.get_parent_scope()
            self.main_scope['IoC.Scope.Set'] = lambda *args: SetCurrentScopeCommand(args[0])
            self.main_scope['IoC.Scope.Current'] = lambda *args: self.get_current_scope()
            self.main_scope['IoC.Register'] = lambda *args: RegisterDependencyCommand(args[0], args[1])
            self.main_scope['IoC.Scopes.Main.Scope'] = lambda *args: self.main_scope
            self.main_scope['IoC.Scopes.Current.Scope'] = lambda *args: self.current_scope

            IoC[ICommand].resolve(
                'UpdateStrategy', DependencyResolver(self).resolve
            ).execute()

            self._is_executed = True

    def create_new_scope(self, *args) -> dict:
        new_scope = IoC[dict].resolve('IoC.Scope.Empty')

        if args:
            parent_scope = args[0]
        else:
            parent_scope = IoC[dict].resolve('IoC.Scope.Current')
        new_scope['IoC.Scope.Parent'] = lambda *args: parent_scope

        return new_scope

    def set_current_scope(self, scope: dict) -> None:
        self.current_scope.value = scope

    def get_parent_scope(self) -> NoReturn:
        raise AttributeError('Root scope has not parent scope')

    def get_current_scope(self):
        try:
            return self.current_scope.value
        except AttributeError:
            return self.main_scope


class SetCurrentScopeCommand(ICommand):
    def __init__(self, scope: dict) -> None:
        self.scope = scope

    def execute(self) -> None:
        InitCommand.current_scope.value = self.scope


class RegisterDependencyCommand(ICommand):
    def __init__(self, dependency: str, strategy: Callable) -> None:
        self.dependency = dependency
        self.strategy = strategy

    def execute(self) -> None:
        current_scope = IoC[threading.local].resolve('IoC.Scopes.Current.Scope')
        main_scope = IoC[dict].resolve('IoC.Scopes.Main.Scope')

        try:
            current_scope.value[self.dependency] = self.strategy
        except AttributeError:
            main_scope[self.dependency] = self.strategy
