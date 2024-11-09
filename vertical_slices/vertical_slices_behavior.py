from image_loader import ImageHandler
from image_processor import ImageProcessor
import numpy as np
from PySide6.QtWidgets import QMessageBox
from custom_loyauts import ErrorDialog, TableWidget
from vertical_slices.vertical_slices import VerticalSlicesWidget

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
            width = self.imageProcessor.image.shape[1]
            self.ui.set_slider_range(1, width - 2)
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
        self.ui.clear_table()  # Clear the table before adding new data
        # means = []

        if not slice_values:
            return
        
        means = self.imageProcessor.calculateMeanRelativeToPartition(slice_values)


        end_pixel = 0
        slice_values.append(int(self.ui.slider.get_maximum()))
        for i, (x, mean) in enumerate(zip(slice_values, means)):
            interval_str = f"{end_pixel}-{x}"
            self.ui.add_column_to_table(interval_str, mean)  # Add column to table
            end_pixel = x