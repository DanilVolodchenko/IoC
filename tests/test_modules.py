import threading
import pytest

from interfaces import ICommand
from commands import InitCommand
from ioc import IoC


def test_strategy() -> None:
    InitCommand().execute()

    assert callable(IoC.strategy)


def test_register_command(mock_command) -> None:
    InitCommand().execute()
    IoC[ICommand].resolve('IoC.Register', 'ExampleCommand', lambda a: mock_command(a)).execute()
    example_command = IoC[ICommand].resolve('ExampleCommand', 1)
    example_command.execute()

    assert example_command.a == 1234


def test_set_local_scope_command(mock_command) -> None:
    InitCommand().execute()

    local_scope = IoC[threading.local].resolve('IoC.Scopes.LocalScope')

    with pytest.raises(AttributeError):
        local_scope.value

    IoC[ICommand].resolve('IoC.Scope.Set').execute()

    assert local_scope.value


def test_empty_local_scope_command() -> None:
    InitCommand().execute()

    IoC[ICommand].resolve('IoC.Scope.Set').execute()
    local_scope = IoC[threading.local].resolve('IoC.Scopes.LocalScope')

    assert local_scope.value

    IoC[ICommand].resolve('IoC.Scopes.LocalScope.Empty').execute()

    with pytest.raises(AttributeError):
        local_scope.value
