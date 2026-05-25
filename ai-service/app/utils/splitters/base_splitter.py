from abc import ABC, abstractmethod

class BaseSplitter(ABC):

    @abstractmethod
    def split(self, text):

        pass
