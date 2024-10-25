from manager import Manager
from convolution.convolution import ConvolutionWidget
from convolution.convolution_behavior import ConvolutionBehavior
from data_handler import DataHandler

class ConvolutionManager(Manager):
    def __init__(self):
        self.ui = ConvolutionWidget()
        self.behavior = ConvolutionBehavior(self.ui)
        self.loadSettings()
        self.connectButton()

    def getUi(self):
        return self.ui

    def getBehavior(self):
        return self.behavior

    def saveSettings(self):
        data = self.ui.getData()
        dataHandler = DataHandler()
        dataHandler.write('convolution', data)

    def loadSettings(self):
        dataHandler = DataHandler()
        group = 'convolution'
        default_data = {'cmaps': ['viridis', 'gray', 'plasma', 'inferno', 'magma', 'cividis'], 'active_cmap': 'viridis'}
        try:
            data = dataHandler.load(group)
        except Exception as e:
            dataHandler.write(group, default_data)
            data = dataHandler.load(group)
        if not data:
            data = default_data
        self.ui.setData(data)

    def connectButton(self):
        self.ui.loadButton.clicked.connect(self.behavior.pushLoadButton)
        self.ui.convolutionButton.clicked.connect(self.behavior.pushConvolutionButton)