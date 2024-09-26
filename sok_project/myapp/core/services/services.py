from abc import ABC, abstractmethod
from core.models import Graph

class AbstractService(ABC):
    @abstractmethod
    def get_identifier(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

class DataLoader(AbstractService):
    
    @abstractmethod
    def import_data(self, source) -> Graph:
        pass

class ViewRenderer(AbstractService):
    
    @abstractmethod
    def render_view(self, graph) -> str:
        pass
