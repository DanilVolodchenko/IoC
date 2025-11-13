import threading

from interfaces import ICommand
from commands import InitCommand
from ioc import IoC

result_first_thread = None
result_second_thread = None


def first_thread(mock_command):
    global result_first_thread

    IoC[ICommand].resolve('IoC.Scope.Set').execute()
    IoC[ICommand].resolve('IoC.Register', 'ExampleCommand', lambda a: mock_command(a)).execute()
    cmd = IoC[ICommand].resolve('ExampleCommand', 4)
    cmd.execute()
    result_first_thread = cmd.b


def second_thread(mock_command):
    global result_second_thread

    IoC[ICommand].resolve('IoC.Scope.Set').execute()
    IoC[ICommand].resolve('IoC.Register', 'ExampleCommand', lambda a: mock_command(a)).execute()
    cmd = IoC[ICommand].resolve('ExampleCommand', 8)
    cmd.execute()
    result_second_thread = cmd.b


def test_ioc_in_diff_threads(mock_command_thread) -> None:
    """Тестирование запуска IoC в разных потоках, чтобы одна и та же команда возвращала разный результат."""

    InitCommand().execute()
    IoC[ICommand].resolve('IoC.Register', 'ExampleCommand', lambda a: mock_command_thread(a)).execute()

    for target in [first_thread, second_thread]:
        threading.Thread(target=target, args=(mock_command_thread,)).start()

    assert result_first_thread == 4
    assert result_second_thread == 8
