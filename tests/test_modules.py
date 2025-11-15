

# def test_set_local_scope_command(mock_command) -> None:
#     InitCommand().execute()
#
#     scope1 = IoC[Callable].resolve('IoC.Scope.Create')
#
#     IoC[ICommand].resolve('IoC.Register', 'ExampleCommand', lambda a: mock_command(a)).execute()
#     ex_cmd = IoC[ICommand].resolve('ExampleCommand1', 1234)
#
#     assert ex_cmd == 1234

# def test_empty_local_scope_command() -> None:
#     InitCommand().execute()
#
#     IoC[ICommand].resolve('IoC.Scope.Set').execute()
#     local_scope = IoC[threading.local].resolve('IoC.Scopes.LocalScope')
#
#     assert local_scope.value
#
#     IoC[ICommand].resolve('IoC.Scopes.LocalScope.Empty').execute()
#
#     with pytest.raises(AttributeError):
#         local_scope.value
