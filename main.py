from interfaces import ICommand
from ioc import IoC
from commands import InitCommand


class ExampleCommand:
    def __init__(self, a):
        self.a = a

    def execute(self):
        self.a = 1234


if __name__ == '__main__':
    # InitCommand().execute()
    # ioc = IoC
    # IoC[ICommand].resolve('IoC.Register', 'ExampleCommand', lambda a: ExampleCommand(a)).execute()
    # IoC[ICommand].resolve('IoC.Register', 'ExampleCommand2', lambda: {'a': 1, 'b': 2}).execute()
    # ex = IoC[ICommand].resolve('ExampleCommand', 1)
    # ex.execute()
    # print(IoC[ICommand].resolve('ExampleCommand2'))
    #
    # IoC[ICommand].resolve('IoC.Scope.Set').execute()
    # IoC[ICommand].resolve('IoC.Register', 'ExampleCommand3', lambda a: ExampleCommand(a)).execute()
    # print(IoC.strategy)
    # ex3 = IoC[ICommand].resolve('ExampleCommand3', 4)
    # ex3.execute()
    #
    # IoC[ICommand].resolve('IoC.Scopes.LocalScope.Empty').execute()
    # ex = IoC[ICommand].resolve('ExampleCommand', 1)
    # ex.execute()
    InitCommand().execute()

    # current_scope = IoC[ICommand].resolve('IoC.Scope.Create')

    scope1 = IoC[ICommand].resolve('IoC.Scope.Create')
    scope2 = IoC[ICommand].resolve('IoC.Scope.Create')

    IoC[ICommand].resolve('IoC.Scope.Set', scope1)
    IoC[ICommand].resolve('IoC.Register', 'ExampleCommand1', lambda a: ExampleCommand(a)).execute()
    ex_cmd1 = IoC[ICommand].resolve('ExampleCommand1', 1)

    IoC[ICommand].resolve('IoC.Scope.Set', scope2)
    IoC[ICommand].resolve('IoC.Register', 'ExampleCommand2', lambda a: ExampleCommand(a)).execute()
    ex_cmd2 = IoC[ICommand].resolve('ExampleCommand2', 5)
