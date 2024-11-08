import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QPushButton
from PySide6.QtCore import Qt, QSize, QPoint, QRect, QRectF, Signal, Slot, QEvent
from PySide6.QtGui import QPainter, QColor, QPen, QMouseEvent, QLinearGradient


class MultiThumbSlider(QWidget):
    valuesChanged = Signal(list)
    thumbReleased = Signal()
    thumbs_pressed = []

    def __init__(self, minimum, maximum, num_thumbs, initial_values=None):
        super().__init__()
        self.minimum = minimum
        self.maximum = maximum
        self.num_thumbs = num_thumbs
        self.thumb_size = QSize(12, 20)
        self.thumb_positions = []
        self.dragging_thumb = -1
        self.track_height = 4
        self.min_distance = 1

        if initial_values is None:
            initial_values = self.calculate_initial_positions(minimum, maximum, num_thumbs, self.min_distance)
        else:
            # Проверка на корректность начальных значений
            if len(initial_values) != num_thumbs:
                raise ValueError("Number of initial values must match num_thumbs")
            initial_values.sort()
            for i in range(1, num_thumbs):
                if initial_values[i] <= initial_values[i - 1] + self.min_distance:
                    raise ValueError(
                        "Initial values must be unique and have at least min_distance between them.")

        self.values = initial_values
        self.setMouseTracking(True)
        self.update_thumb_positions()
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        # Кнопки для добавления и удаления ползунков
        self.add_button = QPushButton("+", self)
        self.remove_button = QPushButton("-", self)
        self.add_button.clicked.connect(self.add_thumb)
        self.remove_button.clicked.connect(self.remove_thumb)
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.dragging_thumb != -1:  # Only remove if a thumb was being dragged
                if self.thumbs_pressed[self.dragging_thumb]: # Check if this thumb was clicked, not just dragged

                    self.remove_thumb(self.dragging_thumb)
                self.dragging_thumb = -1
                self.thumbs_pressed = [False] * self.num_thumbs  # Reset after checking
                self.thumbReleased.emit()
                self.update()  # redraw

    def remove_thumb(self, index):
        if self.num_thumbs > 1:
            self.num_thumbs -= 1
            self.values.pop(index)

            self.update_thumb_positions()
            self.valuesChanged.emit(self.values)
            
    def calculate_initial_positions(self, minimum, maximum, num_thumbs, min_distance):
        """Вычисляет начальные позиции ползунков с учётом минимального расстояния."""
        if num_thumbs <= 1:
            return [minimum] if num_thumbs == 1 else []

        total_range = maximum - minimum
        available_range = total_range - (num_thumbs - 1) * min_distance
        if available_range <= 0:
            raise ValueError("Not enough space for all thumbs with given min_distance")

        step = available_range / (num_thumbs - 1)
        positions = [minimum + i * step for i in range(num_thumbs)]

        # Добавляем минимальное расстояние:
        for i in range(1, num_thumbs):
            positions[i] += i * min_distance

        return positions

    def update_thumb_positions(self):
        range_width = self.width() - self.thumb_size.width()
        if range_width <= 0:
            self.thumb_positions = []
            return
        self.thumb_positions = [int((v - self.minimum) / (self.maximum - self.minimum) * range_width)
                                 for v in self.values]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Дорожка слайдера
        track_y = (self.height() - self.track_height) // 2
        painter.fillRect(0, track_y, self.width(), self.track_height, QColor(150, 150, 150))

        # Градиентная дорожка (опционально)
        grad = QLinearGradient(0, track_y, self.width(), track_y)
        grad.setColorAt(0, QColor(100, 100, 100))
        grad.setColorAt(1, QColor(200, 200, 200))
        painter.fillRect(0, track_y, self.width(), self.track_height, grad)

        thumb_y = (self.height() - self.thumb_size.height()) // 2
        for pos in self.thumb_positions:
            painter.setPen(QPen(Qt.black, 1))
            painter.setBrush(QColor(50, 130, 184))
            painter.drawRoundedRect(pos, thumb_y, self.thumb_size.width(), self.thumb_size.height(), 3, 3)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for i, pos in enumerate(self.thumb_positions):
                thumb_rect = QRect(pos, 0, self.thumb_size.width(), self.height())
                if thumb_rect.contains(event.position().toPoint()):
                    self.dragging_thumb = i
                    self.thumbs_pressed = [False] * self.num_thumbs  # Track clicked thumbs

                    self.thumbs_pressed[i] = True  # Mark the clicked thumb
                    break

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging_thumb != -1:
            range_width = self.width() - self.thumb_size.width()
            if range_width <= 0:
                return

            new_pos = max(0, min(range_width, event.position().x()))
            new_value = int(self.minimum + (new_pos / range_width) * (self.maximum - self.minimum))

            # Проверка на пересечение и корректировка позиции
            new_values = self.values[:]
            new_values[self.dragging_thumb] = new_value
            new_values.sort()

            # Корректировка, чтобы предотвратить перекрытие (работает в обе стороны)
            for i in range(self.num_thumbs - 1):
                if new_values[i + 1] <= new_values[i] + self.min_distance:
                    new_values[i + 1] = new_values[i] + self.min_distance

            # Проверка правой границы
            if new_values[-1] > self.maximum:
                diff = new_values[-1] - self.maximum
                for i in range(self.num_thumbs):
                    new_values[i] -= diff

            self.values = new_values
            self.update_thumb_positions()
            self.valuesChanged.emit(self.values)
            self.update()


    def resizeEvent(self, event):
        self.update_thumb_positions()
        self.update()

    def add_thumb(self):
        self.num_thumbs += 1
        new_value = (self.maximum + self.minimum) // 2
        self.values.append(new_value)
        self.values.sort()
        # корректируем значения чтобы не было наложений
        for i in range(self.num_thumbs - 1):
            if self.values[i + 1] <= self.values[i] + self.min_distance:
                self.values[i + 1] = self.values[i] + self.min_distance
        self.update_thumb_positions()
        self.valuesChanged.emit(self.values)
        self.update()

    def remove_thumb(self):
        if self.num_thumbs > 1:
            self.num_thumbs -= 1
            self.values.pop()
            self.update_thumb_positions()
            self.valuesChanged.emit(self.values)
            self.update()

    def sizeHint(self):
        return QSize(200, 40)

    def get_values(self):
        return self.values[:]

    def get_values_normalized(self):
        return [(v - self.minimum) / (self.maximum - self.minimum) for v in self.values]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    my_slider = MultiThumbSlider(0, 100, 2)
    label = QLabel(f"Значения: {my_slider.values}")

    button_layout = QVBoxLayout()
    button_layout.addWidget(my_slider.add_button)
    button_layout.addWidget(my_slider.remove_button)

    layout.addLayout(button_layout)
    layout.addWidget(my_slider)
    layout.addWidget(label)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())