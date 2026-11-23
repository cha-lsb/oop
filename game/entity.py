from abc import ABC, abstractmethod

class Entity(ABC):

    def __init__(self, name, description: str=""):
        self.name = name
        self.description = description

    @abstractmethod
    def summary(self):
        """Return a one-line summary, ready to display"""

