from manager import Manager
from vertical_slices_with_step.vertical_slices_with_step import VerticalSlicesWithStepWidget
from vertical_slices_with_step.vertical_slices_with_step_behavior import VerticalSlicesWithStepBehavior

class VerticalSlicesWithStepManager(Manager):
    def __init__(self):
        self.ui = VerticalSlicesWithStepWidget()
        self.behavior = VerticalSlicesWithStepBehavior(self.ui)
        self.connectButton()

    def getUi(self):
        return self.ui

    def getBehavior(self):
        return self.behavior

    def saveSettings(self):
       pass

    def loadSettings(self):
        pass

    def connectButton(self):
        self.ui.loadButton.clicked.connect(self.behavior.pushLoadButton)
        self.ui.slicesButton.clicked.connect(self.behavior.pushSlicesButton)