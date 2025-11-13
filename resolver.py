import threading

from interfaces import IResolver


class DependencyResolver(IResolver):
    def __init__(self, scope: dict, local_scope: threading.local):
        self.scope = scope
        self.local_scope = local_scope

    def resolve(self, dependency: str, *args):
        try:
            if dependency.startswith('IoC.'):
                return self.scope[dependency](*args)
            try:
                self.local_scope.value
            except AttributeError:
                return self.scope[dependency](*args)

            return self.scope[self.local_scope.value][dependency](*args)


        except KeyError:
            raise Exception(f'Зависимость {dependency} не была найдена')
