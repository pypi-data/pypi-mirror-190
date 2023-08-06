import inspect
import typing
from typing import Callable, Type, Generic, List

from .abstraction import TService, ServiceFactory, AbstractServiceProvider

ServiceCtor = Callable[[...], TService]


class DepResolver(Generic[TService]):
    def __init__(self, service_type: Type[TService], fallback: TService | None = None, required=True):
        self.service_type = service_type
        self.fallback = fallback
        self.required = required

    def __call__(self, sp: AbstractServiceProvider):
        if self.required:
            return sp.get_required_service(self.service_type)

        return sp.get_service(self.service_type) or self.fallback


class DerivedServiceFactory(Generic[TService], ServiceFactory[TService]):
    """
    Attempts to automatically derive a service factory from a callable using the type annotations in
    its signature.
    :param ctor: function that accepts dependencies for a service which can be resolved from a service provider
                 and returns an instance of the service.
    :return: a service factory that can be registered with a container.
    """

    def __init__(self, ctor: ServiceCtor[TService]):
        self.ctor = ctor
        self.dep_resolvers: List[DepResolver] = []

        for p in inspect.signature(ctor).parameters.values():
            if p.name == 'self':
                continue

            if p.annotation is None:
                raise AttributeError(f'auto service factory generator failed because parameter {p.name} of '
                                     f'{ctor.__name__} does not have a type annotation.')

            if p.default != inspect.Parameter.empty:
                # has default
                self.dep_resolvers.append(DepResolver(p.annotation, p.default, False))
            elif type(None) in typing.get_args(p.annotation):
                # optional
                type_args = typing.get_args(p.annotation)
                if len(type_args) > 2:
                    raise TypeError(f'auto service factory generator failed because parameter {p.name} of '
                                    f'{ctor.__name__} has an optional type annotation that is a union of too many '
                                    f'types.')
                self.dep_resolvers.append(DepResolver(type_args[0], None, False))
            else:
                # required
                self.dep_resolvers.append(DepResolver(p.annotation))

    def __call__(self, t: Type[TService], sp: AbstractServiceProvider) -> TService:
        return self.ctor(*(f(sp) for f in self.dep_resolvers))


def auto(ctor: ServiceCtor, lifetime=None) -> ServiceFactory:
    """
    Automatically derive a ServiceFactory for the service constructor.
    :param ctor: callable which creates the service. Can be a function or class, which uses the __init__ method.
    :param lifetime: optional lifetime (singleton, scoped). Default is None (transient)
    :return:
    """
    factory = DerivedServiceFactory(ctor)
    if lifetime:
        factory = lifetime(factory)
    return factory
