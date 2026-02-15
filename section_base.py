from abc import ABC, abstractmethod

class GameSection(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def end(self):
        pass