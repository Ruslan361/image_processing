from gaussian_blur.gaussian_blur import GaussianBlurWidget
from data_handler import DataHandler
from image_loader import ImageHandler
from image_processor import ImageProcessor
import numpy as np
from PySide6.QtWidgets import QMessageBox

class GaussianBlurBehavior:
    def __init__(self, ui: GaussianBlurWidget):
        self.image_handler = ImageHandler()
        self.ui = ui
        self.kernel = (3, 3)
        self.sigma = 0
        self.imageProcessor = None

    def pushLoadButton(self):
        self.tryLoadImage()
        self.showMean()

    def tryLoadImage(self):
        try:
            image = self.image_handler.load_image()
            self.imageProcessor = ImageProcessor(image)
            self.ui.showImage(self.imageProcessor.getRGBimage())
            self.showMean()
        except ValueError as e:
            QMessageBox.warning(self.ui, "Ошибка", "Не удалось загрузить изображение. Пожалуйста, попробуйте еще раз.", QMessageBox.Ok)

    def pushSaveSettingsButton(self):
        settings = self.ui.getData()
        datahandler = DataHandler()
        datahandler.write("gaussian blur", settings)

    def pushSaveImageButton(self):
        if self.isImageEmpty():
            QMessageBox.warning(self.ui, "Ошибка", "Сначала загрузите изображение.", QMessageBox.Ok)
            return
        self.image_handler.save_figure(self.ui.imageWidget.fig)


    def pushBlurButton(self):
        if self.isImageEmpty():
            QMessageBox.warning(self.ui, "Ошибка", "Сначала загрузите изображение.", QMessageBox.Ok)
            return
        self.tryBlurImage()
        

    def tryBlurImage(self):
        cmap = self.ui.getActiveCmap()
        try:
            kernel = self.ui.getKernel()
            sigmas = self.ui.getSigmas()
            self.validateKernel(kernel, sigmas)
            bluredImage = self.imageProcessor.blurGaussian(kernel, sigmas[0], sigmas[1])
            self.ui.showImage(bluredImage, cmap)
        except Exception as e:
            QMessageBox.critical(self.ui, "Ошибка", str(e), QMessageBox.Ok)

    def validateKernel(self, kernel, sigmas):
#  σ = 0.3*((ksize-1)*0.5 - 1) + 0.8
        kernel = np.array(kernel, dtype=int)
        if np.any(kernel % 2 == 0) or np.any(kernel <= 0):
            raise Exception("Размер ядра должен быть положительным нечетным числом.")
        if sigmas[0] < 0 or sigmas[1] < 0:
            raise Exception("Значения σx и σy должны быть положительными числами.")

    def showMean(self):
        if not self.imageProcessor is None:
            mean = self.imageProcessor.calculateMeanL()
            self.ui.meanLabelSetText(mean)

    def isImageEmpty(self):
        return self.imageProcessor is None