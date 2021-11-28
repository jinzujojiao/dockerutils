from abc import abstractmethod, ABC


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass