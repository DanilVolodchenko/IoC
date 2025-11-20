from unittest.mock import patch, Mock

from commands import SetCurrentScopeCommand


def test_set_current_scope_command() -> None:
    """Тестирование команды SetCurrentScopeCommand."""

    mock_scope_value = Mock()

    with patch('commands.InitCommand.current_scope') as mock_init_command:
        mock_init_command.value = mock_scope_value

        scope = {'Dep1': 1234, 'Dep2': 4321}
        SetCurrentScopeCommand(scope).execute()

        result = mock_init_command.value

        assert result == scope, f'Ожидаемый результат - {scope}, пришло - {result}'


def test_register_dependency_command() -> None:
    """Тестирование команды RegisterDependencyCommand."""
