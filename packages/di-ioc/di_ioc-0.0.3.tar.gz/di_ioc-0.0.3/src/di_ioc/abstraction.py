from abc import ABC, abstractmethod
from typing import Callable, Type, TypeVar, Optional, ContextManager, Generator, \
    Hashable, Self, MutableMapping, List, Mapping, Sequence

TService = TypeVar('TService')


class MissingServiceError(Exception):
    def __init__(self, service_type: Type):
        self.service_type = service_type
        super().__init__()


class AbstractServiceProvider(Hashable, ContextManager[Self], ABC):
    @abstractmethod
    def get_service(self, service_type: Type[TService]) -> Optional[TService]:
        """
        Try to get a service instance if it exists.
        :param service_type:
        :return: the service instance or None.
        """

    @abstractmethod
    def get_required_service(self, service_type: Type[TService]) -> TService:
        """
        Get a service instance or fail with an exception.
        :param service_type:
        :return: the service instance.
        :raises: MissingServiceError - there is not a service registered under the service_type.
        """

    @abstractmethod
    def get_services(self, service_type: Type[TService]) -> List[TService]:
        """
        Produce a list of all services that satisfy the service_type.
        :param service_type:
        :return: list of all service instances that match the service_type.
        """

    @abstractmethod
    def create_scope(self) -> Self:
        """
        Create a new provider that inherits all the service factories and
        causes scoped factories to produce a new instance. Singleton factories
        will return the same instance the parent provider does.
        :return:
        """


DisposableServiceInstance = Generator[TService, None, None]
ServiceFactory = Callable[[Type[TService], AbstractServiceProvider], TService]
ServiceFactoryGenerator = Callable[[Type[TService], AbstractServiceProvider], DisposableServiceInstance[TService]]


class AbstractServiceContainer(MutableMapping[Type | Sequence[Type], ServiceFactory],
                               Mapping[Type, List[ServiceFactory]],
                               ABC):

    @abstractmethod
    def register(self, *other: 'AbstractServiceContainer'):
        """
        'Mount' other service containers into this one and make their services available from this one. Each mounted
        container is still distinct from this one.
        :param other:
        :return:
        """
