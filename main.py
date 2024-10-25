from gaussian_blur.gaussian_blur_manager import GaussianBlurManager
from convolution.convolution_manager import ConvolutionManager
from PySide6.QtWidgets import QMainWindow, QTabWidget, QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Меню выбора вкладок")

        # Создание основного виджета QTabWidget
        self.tab_widget = QTabWidget()

        # Создание вкладок
        self.create_tabs()

        # Устанавливаем QTabWidget как центральный виджет
        self.setCentralWidget(self.tab_widget)

    def create_tabs(self):
        # Вкладка 1
        self.blurManager = GaussianBlurManager()
        gaussianTab = self.blurManager.ui

        # Вкладка 2
        self.convolutionManager = ConvolutionManager()
        convolutionTab = self.convolutionManager.ui

        # Добавляем вкладки в QTabWidget
        self.tab_widget.addTab(gaussianTab, "Размытие по Гауссу")
        self.tab_widget.addTab(convolutionTab, "Свертка")

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()