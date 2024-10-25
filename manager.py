from abc import ABC, abstractclassmethod
class Manager(ABC):
    @classmethod
    @abstractclassmethod
    def saveSettings(self):
        pass
    @classmethod
    @abstractclassmethod
    def loadSettings(self):
        pass
    @classmethod
    @abstractclassmethod
    def getUi(self):
        pass
    @classmethod
    @abstractclassmethod
    def getBehavior(self):
        pass
