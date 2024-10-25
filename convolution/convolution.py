from custom_loyauts import MatplotlibImageWidget, CmapLoyaut
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class ConvolutionWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.loadButton = QPushButton(text="Загрузить изображение")
        self.convolutionButton = QPushButton(text="Применить свертку")

        mainLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(self.convolutionButton)
        mainLayout.addLayout(buttonLayout)

        self.cmapLoyaut = CmapLoyaut()
        mainLayout.addLayout(self.cmapLoyaut)

        self.imageWidget = MatplotlibImageWidget()
        mainLayout.addWidget(self.imageWidget)

        self.setLayout(mainLayout)

    def setData(self, data):
        cmaps = data['cmaps']
        activeCMap = data['active_cmap']
        self.cmapLoyaut.setCMaps(cmaps)
        self.cmapLoyaut.setActiveCmap(activeCMap)

    def getData(self):
        cmaps = self.cmapLoyaut.getCMaps()
        activeCMap = self.cmapLoyaut.getActiveCmap()
        data = {
            'cmaps': cmaps,
            'active_cmap': activeCMap
        }
        return data

    def showImage(self, image, cmap=None):
        self.imageWidget.show_image(image, cmap)

    def getActiveCmap(self):
        return self.cmapLoyaut.getActiveCmap()