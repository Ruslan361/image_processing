from custom_loyauts import MatplotlibImageWidget, ErrorDialog
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
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

        self.slider = MultiThumbSlider(1, 100, 2, 1)
        self.slider.valuesChanged.connect(self.update_slider_labels)
        mainLayout.addWidget(self.slider)

        self.slider_labels_layout = QHBoxLayout()
        self.slider_labels = []
        mainLayout.addLayout(self.slider_labels_layout)

        self.imageWidget = MatplotlibImageWidget()
        mainLayout.addWidget(self.imageWidget)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Интервал", "Среднее"])
        mainLayout.addWidget(self.tableWidget)


        self.setLayout(mainLayout)
        self.update_slider_labels(self.slider.get_values())

    def update_slider_labels(self, values):
        for label in self.slider_labels:
            self.slider_labels_layout.removeWidget(label)
            label.deleteLater()
        self.slider_labels.clear()

        for value in values:
            label = QLabel(str(value))
            self.slider_labels_layout.addWidget(label)
            self.slider_labels.append(label)


    def setData(self, data):
        pass

    def getData(self):
        return {}

    def set_slider_range(self, min_val, max_val):
        self.slider.minimum = min_val
        self.slider.maximum = max_val
        self.slider.update_thumb_positions()
        self.slider.values = self.slider.calculate_initial_positions()
        self.update_slider_labels(self.slider.get_values())
        self.slider.update()


    def getSliceValues(self):
        values = self.slider.get_values()
        return [int(val) for val in values]

    def add_row_to_table(self, interval, mean):
        row_count = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_count)
        self.tableWidget.setItem(row_count, 0, QTableWidgetItem(str(interval)))
        self.tableWidget.setItem(row_count, 1, QTableWidgetItem(str(mean)))

    def clear_table(self):
        self.tableWidget.setRowCount(0)