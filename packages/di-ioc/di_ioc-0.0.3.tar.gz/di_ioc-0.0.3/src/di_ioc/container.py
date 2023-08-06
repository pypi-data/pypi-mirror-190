import itertools
import logging
from typing import Type, Optional, Mapping, Iterator, ChainMap, Self, List, Sequence

from .abstraction import AbstractServiceContainer, AbstractServiceProvider, ServiceFactory, TService, \
    MissingServiceError
from .scope import ServiceScope

log = logging.getLogger(__name__)


class ServiceContainer(AbstractServiceContainer, AbstractServiceProvider, ServiceScope):

    def __init__(self, *factories: Mapping[Type, List[ServiceFactory]]):
        super().__init__()
        self._registry = ChainMap[Type, List[ServiceFactory]]({}, *factories)

    def __hash__(self) -> int:
        return id(self)

    def __getitem__(self, service_type: Type[TService]) -> Sequence[ServiceFactory[TService]]:
        return self._registry[service_type]

    def __setitem__(self, service_type: Type | Sequence[Type], service_factory: ServiceFactory) -> None:
        head = self._registry.maps[0]
        if isinstance(service_type, Sequence):
            for t in service_type:
                self._add_factory(head, t, service_factory)
        else:
            self._add_factory(head, service_type, service_factory)

    def __delitem__(self, service_type: Type) -> None:
        del self._registry[service_type]

    def __len__(self) -> int:
        return len(self._registry)

    def __iter__(self) -> Iterator[Type]:
        return iter(self._registry)

    def __enter__(self) -> Self:
        log.debug('entered service scope')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
        log.debug('exited service scope')

    def get_service(self, service_type: Type[TService]) -> Optional[TService]:
        if issubclass(service_type, AbstractServiceProvider):
            return self.create_scope()
        service_factory = self._registry.get(service_type, None)
        if not service_factory:
            return None
        return service_factory[0](service_type, self)

    def get_required_service(self, service_type: Type[TService]) -> TService:
        service = self.get_service(service_type)
        if service is None:
            raise MissingServiceError(service_type)
        return service

    def get_services(self, service_type: Type[TService]) -> List[TService]:
        if issubclass(service_type, AbstractServiceProvider):
            return [self.create_scope()]
        factories = itertools.chain(*(m.get(service_type, []) for m in self._registry.maps))
        return [f(service_type, self) for f in factories]

    def register(self, *other: AbstractServiceContainer):
        self._registry.maps.extend(other)

    def create_scope(self) -> Self:
        return ServiceContainer(self._registry)

    @staticmethod
    def _add_factory(map, key, factory: ServiceFactory):
        if not (factories := map.get(key)):
            factories = []
            map[key] = factories
        factories.append(factory)
