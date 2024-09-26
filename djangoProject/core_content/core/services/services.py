from abc import ABC, abstractmethod
from core.models import Graph

class ServiceBase(ABC):
    @abstractmethod
    def identifier(self):
        pass

    @abstractmethod
    def name(self):
        pass


class LoadBase(ServiceBase):

    @abstractmethod
    def load_data(self, source) -> Graph:
        pass


class ViewBase(ServiceBase):

    @abstractmethod
    def load_view(self, graph) -> str:
        pass