from image_loader import ImageHandler
from image_processor import ImageProcessor
import numpy as np
from PySide6.QtWidgets import QMessageBox
from custom_loyauts import ErrorDialog, TableWidget
from vertical_slices_with_step.vertical_slices_with_step import VerticalSlicesWithStepWidget

class VerticalSlicesWithStepBehavior:
    def __init__(self, ui: VerticalSlicesWithStepWidget):
        self.image_handler = ImageHandler()
        self.imageProcessor = None
        self.ui = ui

    def pushLoadButton(self):
        self.tryLoadImage()

    def tryLoadImage(self):
        try:
            image = self.image_handler.load_image()
            self.imageProcessor = ImageProcessor(image)
            blured = self.imageProcessor.blurGaussian((3, 3), 0, 0)
            self.ui.set_image(blured)

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
        step = self.ui.get_step()
        image_width = self.imageProcessor.image.shape[1]
        slice_values = list(range(step, image_width, step))
        if slice_values[-1] != image_width:  # Ensure the last slice covers the full image
            slice_values.append(image_width)


        self.ui.clear_table()
        means = self.imageProcessor.calculateMeanRelativeToPartition(slice_values[:-1]) # Exclude last slice which is just the whole image

        self.remove_lines()
        # Updating vertical lines on the plot
        if step >= 10:
            self.update_vertical_lines(slice_values[:-1]) # Exclude last slice


        end_pixel = 0
        image_height = self.imageProcessor.image.shape[0]
        for i, (x, mean) in enumerate(zip(slice_values, means)):
            interval_str = f"{end_pixel}-{x}"
            self.ui.ax.axhline(int((mean / 256) * image_height), end_pixel / image_width, x/image_width, color='red', linewidth=1)
            self.ui.add_column_to_table(interval_str, mean)  # Add column to table
            end_pixel = x

        self.ui.imageWidget.canvas.draw()

    def update_vertical_lines(self, values):  # values are now pixel positions

        image_width = self.imageProcessor.image.shape[1] # Assuming imageProcessor is set
        for value in values:
            self.ui.ax.axvline(value, color='red')

        self.ui.imageWidget.canvas.draw()

    def remove_lines(self):
        for line in self.ui.ax.lines:
            line.remove()