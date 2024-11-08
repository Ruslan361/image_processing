from custom_loyauts import KernelSizeInput, MatplotlibImageWidget, SigmaLoyaut, CmapLoyaut
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
import numpy as np

class GaussianBlurWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.loadButton = QPushButton(text="Загрузить изображение")
        self.blurButton = QPushButton(text="Применить размытие")
        self.saveImageButton = QPushButton(text="Сохранить изображение")
        self.saveSettingsButton = QPushButton(text="Сохранить настройки")

        mainLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(self.blurButton)
        buttonLayout.addWidget(self.saveImageButton)
        buttonLayout.addWidget(self.saveSettingsButton)
        mainLayout.addLayout(buttonLayout)

        self.kernelInput = KernelSizeInput("Размер ядра")
        mainLayout.addLayout(self.kernelInput)
        self.sigmaLoyaut = SigmaLoyaut()
        mainLayout.addLayout(self.sigmaLoyaut)
        self.cmapLoyaut = CmapLoyaut()
        mainLayout.addLayout(self.cmapLoyaut)
        self.meanLabel = QLabel("Среднее значение")
        mainLayout.addWidget(self.meanLabel)

        self.imageWidget = MatplotlibImageWidget()
        mainLayout.addWidget(self.imageWidget)

        self.setLayout(mainLayout)
    

    def meanLabelSetText(self, text):
        return self.meanLabel.setText(f'Средняя светимость у.е. {text}')
    def setData(self, data):
        #print(data)
        kernel = data['kernel']
        sigmaX = data['sigmaX']
        sigmaY = data['sigmaY']
        cmaps = data['cmaps']
        activeCMap = data['active_cmap']
        self.kernelInput.setKernel(kernel)
        self.sigmaLoyaut.setSigmas(sigmaX, sigmaY)
        self.cmapLoyaut.setCMaps(cmaps)
        self.cmapLoyaut.setActiveCmap(activeCMap)
    def getData(self):
        kernel = self.getKernel()
        sigmaX = self.getSigmas()[0]
        sigmaY = self.getSigmas()[1]
        cmaps = self.cmapLoyaut.getCMaps()
        activeCMap = self.cmapLoyaut.getActiveCmap()
        data = {
            'kernel': kernel,
            'sigmaX' : sigmaX,
            'sigmaY' : sigmaY,
            'cmaps' : cmaps,
            'active_cmap' : activeCMap
        }
        return data
    def showImage(self, image: np.ndarray, cmap: str = None) -> None:
        self.imageWidget.show_image(image, cmap)
    def getKernel(self):
        return self.kernelInput.getKernel()
    def getSigmas(self):
        return self.sigmaLoyaut.getSigmas()
    def getActiveCmap(self):
        return self.cmapLoyaut.getActiveCmap()







