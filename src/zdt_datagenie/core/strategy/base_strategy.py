from abc import ABC, abstractmethod


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all API calls
    The Context uses this interface to call the algorithm defined by Concrete
    Strategies
    """

    @abstractmethod
    def execute(self):
        pass
