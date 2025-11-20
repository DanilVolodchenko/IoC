from collections.abc import Callable

import pytest

from interfaces import ICommand
from commands import InitCommand
from ioc import IoC


@pytest.fixture(scope='function', autouse=True)
def initialize():
    cmd = InitCommand()
    cmd.execute()
    yield
    del cmd


def test_register_command(mock_example_command) -> None:
    """Проверка зарегистрированной зависимости."""

    IoC[ICommand].resolve(
        'IoC.Register', 'ExampleCommand', lambda a: mock_example_command(a)
    ).execute()
    example_command = IoC[ICommand].resolve('ExampleCommand', 1234)

    result = example_command.execute()
    expected_result = 1234

    assert isinstance(example_command,
                      mock_example_command), 'Полученный объект должен быть такой же, как зарегистрированный'
    assert result == expected_result, f'Некорректное значение, ожидалось - {expected_result}, результат - {result}'


def test_get_not_exists_dependency(mock_example_command) -> None:
    """Проверка на получение не зарегистрированной зависимости."""

    with pytest.raises(Exception):
        IoC[ICommand].resolve('NotExistsDependency', 1234)


def test_register_dependency_in_another_scope(mock_example_command) -> None:
    """Проверка регистрации зависимости в другой области видимости."""

    scope = IoC[Callable].resolve('IoC.Scope.Create')
    IoC[ICommand].resolve('IoC.Scope.Set', scope).execute()
    IoC[ICommand].resolve(
        'IoC.Register', 'ExampleCommand', lambda a: mock_example_command(a)
    ).execute()
    example_command = IoC[ICommand].resolve('ExampleCommand', 1234)

    result = example_command.execute()
    expected_result = 1234

    assert isinstance(example_command,
                      mock_example_command), 'Полученный объект должен быть такой же, как зарегистрированный'
    assert result == expected_result, f'Некорректное значение, ожидалось - {expected_result}, результат - {result}'


def test_register_dependency_in_parent_scopes(mock_example_command) -> None:
    """Проверка получения родительской зависимости из дочерней области видимости."""

    scope1 = IoC[Callable].resolve('IoC.Scope.Create')
    scope2 = IoC[Callable].resolve('IoC.Scope.Create', scope1)

    IoC[ICommand].resolve('IoC.Scope.Set', scope1).execute()
    IoC[ICommand].resolve(
        'IoC.Register', 'ExampleCommand', lambda a: mock_example_command(a)
    ).execute()
    IoC[ICommand].resolve('IoC.Scope.Set', scope2).execute()
    example_command = IoC[ICommand].resolve('ExampleCommand', 1234)

    result = example_command.execute()
    expected_result = 1234

    assert isinstance(example_command,
                      mock_example_command), 'Полученный объект должен быть такой же, как зарегистрированный'
    assert result == expected_result, f'Некорректное значение, ожидалось - {expected_result}, результат - {result}'
