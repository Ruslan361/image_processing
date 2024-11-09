from manager import Manager
from vertical_slices.vertical_slices import VerticalSlicesWidget
from vertical_slices.vertical_slices_behavior import VerticalSlicesBehavior

class VerticalSlicesManager(Manager):
    def __init__(self):
        self.ui = VerticalSlicesWidget()
        self.behavior = VerticalSlicesBehavior(self.ui)
        self.connectButton()
        self.ui.slider.valuesChanged.connect(self.behavior.update_vertical_lines) # Connect slider to update lines
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