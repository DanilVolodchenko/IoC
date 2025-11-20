import pytest


@pytest.fixture
def mock_example_command():
    class ExampleCommand:
        def __init__(self, a):
            self.a = a

        def execute(self):
            return self.a

    return ExampleCommand


@pytest.fixture
def mock_command_thread():
    class ExampleCommand:
        def __init__(self, a):
            self.a = a

        def execute(self):
            self.b = self.a

    return ExampleCommand
