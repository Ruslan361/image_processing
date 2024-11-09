from image_loader import ImageHandler
from image_processor import ImageProcessor
import numpy as np
from PySide6.QtWidgets import QMessageBox
from custom_loyauts import ErrorDialog, TableWidget
from vertical_slices.vertical_slices import VerticalSlicesWidget # исправленный импорт

class VerticalSlicesBehavior:
    def __init__(self, ui: VerticalSlicesWidget):
        self.image_handler = ImageHandler()
        self.imageProcessor = None
        self.ui = ui
    def pushLoadButton(self):
        self.tryLoadImage()

    def tryLoadImage(self):
        try:
            image = self.image_handler.load_image()
            self.imageProcessor = ImageProcessor(image)
            width = self.imageProcessor.image.shape[1] # image width
            self.ui.set_slider_range(0, width - 1)
            rgbImage = self.imageProcessor.getRGBimage()
            self.ui.imageWidget.show_image(rgbImage) 

        except ValueError as e:
            QMessageBox.warning(self.ui, "Ошибка", "Не удалось загрузить изображение. Пожалуйста, попробуйте еще раз.", QMessageBox.Ok)
        except Exception as e:
            dialog = ErrorDialog(str(e))
            dialog.exec()


    def pushSlicesButton(self):
        if self.isImageEmpty():
            QMessageBox.warning(self.ui, "Ошибка", "Сначала загрузите изображение.", QMessageBox.Ok)
            return
        try:
            self.calculate_and_plot_means()
        except Exception as e:
            QMessageBox.critical(self.ui, "Ошибка", str(e), QMessageBox.Ok)

    def isImageEmpty(self):
        return self.imageProcessor is None

    def calculate_and_plot_means(self):
        slice_values = self.ui.getSliceValues()
        means = []
        for i, x in enumerate(slice_values):
            slice = self.imageProcessor.image[:, x] # берем срез
            mean = np.mean(slice) # считаем среднее
            means.append(mean)
        self.ui.plot(np.arange(len(means)), means)