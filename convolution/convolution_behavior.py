from convolution.convolution import ConvolutionWidget
from image_loader import ImageLoader
from image_processor import ImageProcessor
import numpy as np
from PySide6.QtWidgets import QMessageBox

class ConvolutionBehavior:
    def __init__(self, ui: ConvolutionWidget):
        self.image_loader = ImageLoader()
        self.ui = ui
        self.imageProcessor = None
        self.kernel = np.array([
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ])

    def pushLoadButton(self):
        self.tryLoadImage()

    def tryLoadImage(self):
        try:
            image = self.image_loader.load_image()
            self.imageProcessor = ImageProcessor(image)
            self.ui.showImage(self.imageProcessor.getRGBimage())
        except ValueError as e:
            QMessageBox.warning(self.ui, "Ошибка", "Не удалось загрузить изображение. Пожалуйста, попробуйте еще раз.", QMessageBox.Ok)

    def pushConvolutionButton(self):
        if self.isImageEmpty():
            QMessageBox.warning(self.ui, "Ошибка", "Сначала загрузите изображение.", QMessageBox.Ok)
            return
        self.tryConvolutionImage()

    def isImageEmpty(self):
        return self.imageProcessor is None

    def tryConvolutionImage(self):
        cmap = self.ui.getActiveCmap()
        try:
            bluredImage = self.imageProcessor.blurGaussian((5, 5), 0, 0)
            convolutedImage = self.imageProcessor.applyConvolution(bluredImage, self.kernel)
            self.ui.showImage(convolutedImage, cmap)
        except Exception as e:
            QMessageBox.critical(self.ui, "Ошибка", str(e), QMessageBox.Ok)