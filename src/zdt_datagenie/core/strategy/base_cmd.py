from abc import ABC, abstractmethod
from importlib import resources as impresources
from zdt_datagenie.core import sql
from zdt_datagenie.core import templates


class Command(ABC):
    """
    The Strategy interface declares operations common to all API calls
    The Context uses this interface to call the algorithm defined by Concrete
    Strategies
    """

    @staticmethod
    def sql(command):
        file = impresources.files(sql) / f"{command}.sql"
        with file.open("rt") as f:
            return f.read()

    @staticmethod
    def template(command):
        file = impresources.files(templates) / f"{command}.jinja"
        with file.open("rt") as f:
            return f.read()

    @abstractmethod
    def execute(self):
        pass
