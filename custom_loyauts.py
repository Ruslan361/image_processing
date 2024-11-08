from PySide6.QtWidgets import QDialogButtonBox, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QDialog, QComboBox, QTableWidget
from PySide6.QtGui import QDoubleValidator, QIntValidator, QImage
import numpy as np
import cv2
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
# Требования python 3.11.10
class CmapLoyaut(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(QLabel("Цветовая схема"))
        self.cmapList = ['viridis','gray', 'plasma', 'inferno', 'magma', 'cividis']
        self.cmapComboBox = QComboBox()
        self.cmapComboBox.addItems(self.cmapList)
        self.addWidget(self.cmapComboBox)
    def setCMaps(self, cmaps):
        self.cmapList = cmaps
        self.cmapComboBox.clear()
        self.cmapComboBox.addItems(cmaps)
    def getCMaps(self):
        return self.cmapList
    def setActiveCmap(self, cmap):
        index = self.cmapList.index(cmap)
        self.cmapComboBox.setCurrentIndex(index)
    def getActiveCmap(self):
        cmap = self.cmapComboBox.currentText()
        return cmap


class SigmaLoyaut(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.sigmaXInput = FloatNumberInput("σx")
        self.sigmaYInput = FloatNumberInput("σy")
        self.addLayout(self.sigmaXInput)
        self.addLayout(self.sigmaYInput)
    def getSigmas(self):
        return (self.sigmaXInput.getFloatNumber(), self.sigmaYInput.getFloatNumber())
    def setSigmas(self, sigmaX, sigmaY):
        self.sigmaXInput.setFloatNumber(str(sigmaX))
        self.sigmaYInput.setFloatNumber(str(sigmaY))

class GraphLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.canvas = MatplotlibGraph(self)
        self.addWidget(self.canvas)

    def clear(self):
        self.canvas.clear()

    def set_ylabel(self, label):
        self.canvas.set_ylabel(label)

    def set_xlabel(self, label):
        self.canvas.set_xlabel(label)

    def set_title(self, title):
        self.canvas.set_title(title)

    def plot(self, X, Y):
        self.canvas.plot(X, Y)

    def draw(self):
        self.canvas.Draw()

class TableWidget(QWidget):
    def __init__(self, headers):
        super().__init__()

        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_row(self, data):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            self.table.setItem(row_count, col, item)

    def clear_table(self):
        self.table.setRowCount(0)

class MatplotlibImageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Создание Figure и FigureCanvas
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(1, 1, 1)  # Добавляем оси

        # Настройка layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def show_image(self, image: np.array, cmap=None):
        """Отображает изображение на виджете."""
        self.ax.clear()  # Очищаем оси перед отображением нового изображения
        self.ax.set_axis_off()
        self.ax.imshow(image, cmap) 
        self.canvas.draw()

class MatplotlibGraph(FigureCanvas):
    def __init__(self, parent=None):
        # Создание Figure и добавление осей
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        # Инициализация FigureCanvas с созданной фигурой
        super(MatplotlibGraph, self).__init__(self.fig)

    def clear(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)

    def set_ylabel(self, label):
        self.ax.set_ylabel(label)

    def set_xlabel(self, label):
        self.ax.set_xlabel(label)

    def set_title(self, title):
        self.ax.set_title(title)

    def plot(self, X, Y):
        self.ax.plot(X, Y)

    def Draw(self):
        self.draw()



class ErrorDialog(QDialog):
    def __init__(self, errorMessage):
        super().__init__()

        self.setWindowTitle("Ошибка!")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(errorMessage)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class FloatNumberInput(QHBoxLayout):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.addWidget(QLabel(label))
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.ScientificNotation)  # Для ввода числа в экспоненциальной форме
        # Поле для ввода числа с плавающей точкой
        self.floatNumberLineEdit = QLineEdit()
        self.floatNumberLineEdit.setValidator(validator)
        self.addWidget(self.floatNumberLineEdit)

    def getFloatNumber(self):
        FloatNumberString = self.floatNumberLineEdit.text()
        return float(FloatNumberString)
    def setFloatNumber(self, text):
        self.floatNumberLineEdit.setText(text)

    def setReadOnly(self, state):
        self.floatNumberLineEdit.setReadOnly(state)
    
class IntNumberInput(QHBoxLayout):
    def __init__(self, label):
        super().__init__()
        self.label = label
        self.addWidget(QLabel(label))
        validator = QIntValidator(0, 200)
        self.intNumberLineEdit = QLineEdit()
        self.intNumberLineEdit.setValidator(validator)
        #startXLineEdit.setText(str(startX))
        self.addWidget(self.intNumberLineEdit)
    def getIntNumber(self):
        intNumberString = self.intNumberLineEdit.text()
        return int(intNumberString)
    def setIntNumber(self, text):
        self.intNumberLineEdit.setText(text)
    def setReadOnly(self, state):
        self.intNumberLineEdit.setReadOnly(state)

class KernelSizeInput(QHBoxLayout):
    def __init__(self, label):
        super().__init__()
        self.addWidget(QLabel(label))
        validator = QIntValidator(0, 200)
        self.intXSizeLineEdit = QLineEdit()
        self.intXSizeLineEdit.setValidator(validator)

        self.intYSizeLineEdit = QLineEdit()
        self.intYSizeLineEdit.setValidator(validator)
        #startXLineEdit.setText(str(startX))
        self.addWidget(self.intXSizeLineEdit)
        self.addWidget(self.intYSizeLineEdit)
    def getKernel(self):
        X = self.intXSizeLineEdit.text()
        Y = self.intYSizeLineEdit.text()
        return (int(X), int(Y))
    def setReadOnly(self, state):
        self.intXSizeLineEdit.setReadOnly(state)
        self.intYSizeLineEdit.setReadOnly(state)
    def setKernel(self, kernel):
        self.intXSizeLineEdit.setText(str(kernel[0]))
        self.intYSizeLineEdit.setText(str(kernel[1]))

class FloatNumberInputMany(QHBoxLayout):
    def __init__(self, label, count):
        super().__init__()
        self.label = label
        self.addWidget(QLabel(label))
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.ScientificNotation)  # Для ввода числа в экспоненциальной форме

        self.floatNumberLinesEdit = list[QLineEdit]()
        for i in range(count):
            self.floatNumberLineEdit = QLineEdit()
            self.floatNumberLineEdit.setValidator(validator)
            self.addWidget(self.floatNumberLineEdit)
    def getFloatNumbers(self):
        numbers = []
        for input in self.floatNumberLinesEdit:
            numbers.append(float(input.text()))
        return numbers
    def setReadOnly(self, state):
        for input in self.floatNumberLinesEdit:
            input.setReadOnly(state)
    def setValues(self, values):
        for lineEdit,value in zip(self.floatNumberLinesEdit, values):
            lineEdit.setText(value)