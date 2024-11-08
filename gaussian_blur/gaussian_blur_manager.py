from manager import Manager
from gaussian_blur.gaussian_blur import GaussianBlurWidget
from gaussian_blur.gaussian_blur_behavior import GaussianBlurBehavior
from data_handler import DataHandler

class GaussianBlurManager(Manager):
    def __init__(self):
        self.ui = GaussianBlurWidget()
        self.behavior = GaussianBlurBehavior(self.ui)
        self.loadSettings()
        self.connectButton()
    def getUi(self):
        return self.ui
    def getBehavior(self):
        return self.behavior
    def saveSettings(self):
        data = self.ui.getData()
        dataHandler = DataHandler()
        dataHandler.write('gaussian blur', data)
    def loadSettings(self):
        dataHandler = DataHandler()
        group = 'gaussian blur'
        default_data = {'sigmaX': 0, 'sigmaY': 0, 'kernel': (15, 15), 'cmaps': ['viridis','gray', 'plasma', 'inferno', 'magma', 'cividis'], 'active_cmap': 'viridis'}
        try:
            data = dataHandler.load("gaussian blur")
        except Exception as e:
            dataHandler.write(group, default_data)
            data = dataHandler.load(group)
        if not data:
            data = default_data
        self.ui.setData(data)
    def connectButton(self):
        self.ui.loadButton.clicked.connect(self.behavior.pushLoadButton)
        self.ui.blurButton.clicked.connect(self.behavior.pushBlurButton)
        self.ui.saveImageButton.clicked.connect(self.behavior.pushSaveImageButton)
        self.ui.saveSettingsButton.clicked.connect(self.behavior.pushSaveSettingsButton)

