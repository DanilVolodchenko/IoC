import pytest


@pytest.fixture
def mock_command():
    class ExampleCommand:
        def __init__(self, a):
            self.a = a

        def execute(self):
            self.a = 1234

    return ExampleCommand


@pytest.fixture
def mock_command_thread():
    class ExampleCommand:
        def __init__(self, a):
            self.a = a

        def execute(self):
            self.b = self.a

    return ExampleCommand
