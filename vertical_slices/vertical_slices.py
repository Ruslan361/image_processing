from custom_loyauts import MatplotlibImageWidget, ErrorDialog
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from multi_thumb_slider import MultiThumbSlider
import numpy as np

class VerticalSlicesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.loadButton = QPushButton(text="Загрузить изображение")
        self.slicesButton = QPushButton(text="Найти среднее по срезам")
        mainLayout = QVBoxLayout()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(self.slicesButton)
        mainLayout.addLayout(buttonLayout)

        self.slider = MultiThumbSlider(0, 100, 2)  # Initial range 0-100, 2 thumbs
        self.slider.valuesChanged.connect(self.update_slider_labels)  # Connect to update labels
        mainLayout.addWidget(self.slider)

        self.slider_labels_layout = QHBoxLayout()  # Layout for slider value labels
        self.slider_labels = []  # List to hold slider value labels
        mainLayout.addLayout(self.slider_labels_layout)

        self.imageWidget = MatplotlibImageWidget()
        mainLayout.addWidget(self.imageWidget)
        self.setLayout(mainLayout)
        self.update_slider_labels(self.slider.get_values())

    def update_slider_labels(self, values):
        # Clear existing labels
        for label in self.slider_labels:
            self.slider_labels_layout.removeWidget(label)
            label.deleteLater()
        self.slider_labels.clear()
        # Add new labels
        for value in values:
            label = QLabel(str(value))
            self.slider_labels_layout.addWidget(label)
            self.slider_labels.append(label)



    def setData(self, data):
        pass #  пока что не нужно

    def getData(self):
        return {}  # пока что не нужно

    def set_slider_range(self, min_val, max_val):
        self.slider.minimum = min_val
        self.slider.maximum = max_val
        self.slider.update_thumb_positions()
        self.slider.values = self.slider.calculate_initial_positions(min_val, max_val, self.slider.num_thumbs, self.slider.min_distance)
        self.update_slider_labels(self.slider.get_values()) # Обновляем лейблы ползунков сразу, чтобы отразить новые значения
        self.slider.update()


    def plot(self, x, y):
        self.imageWidget.clear()
        self.imageWidget.set_xlabel("Номер среза")
        self.imageWidget.set_ylabel("Среднее значение")
        self.imageWidget.plot(x, y)
        self.imageWidget.Draw()
    def getSliceValues(self):
        return self.slider.get_values()







