from custom_loyauts import MatplotlibImageWidget, ErrorDialog
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QSpinBox
from multi_thumb_slider import MultiThumbSlider
import numpy as np

class VerticalSlicesWithStepWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.loadButton = QPushButton(text="Загрузить изображение")
        self.slicesButton = QPushButton(text="Найти среднее по срезам")
        mainLayout = QVBoxLayout()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.loadButton)
        buttonLayout.addWidget(self.slicesButton)
        mainLayout.addLayout(buttonLayout)

        stepLayout = QHBoxLayout()
        stepLayout.addWidget(QLabel("Шаг разбиения (px):"))
        self.stepSpinBox = QSpinBox()
        self.stepSpinBox.setMinimum(1)
        self.stepSpinBox.setMaximum(1000)  # Set a reasonable maximum
        self.stepSpinBox.setValue(10) # Default step value
        stepLayout.addWidget(self.stepSpinBox)
        mainLayout.addLayout(stepLayout)


        self.imageWidget = MatplotlibImageWidget()
        mainLayout.addWidget(self.imageWidget)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setVerticalHeaderLabels(["Интервал", "Среднее"])
        self.tableWidget.setMinimumSize(200, 100)
        mainLayout.addWidget(self.tableWidget)

        self.setLayout(mainLayout)
        self.ax = self.imageWidget.ax  # Get the axes

    def set_image(self, image):
        self.imageWidget.show_image(image, "viridis")

    def get_step(self):
        return self.stepSpinBox.value()

    def add_column_to_table(self, interval, mean):
        column_count = self.tableWidget.columnCount()
        self.tableWidget.insertColumn(column_count)
        self.tableWidget.setItem(0, column_count, QTableWidgetItem(str(interval)))
        self.tableWidget.setItem(1, column_count, QTableWidgetItem(str(mean)))

    def clear_table(self):
        self.tableWidget.setColumnCount(0)

