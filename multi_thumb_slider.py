import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt, QSize, QPoint, QRect, QRectF, Signal, Slot, QEvent
from PySide6.QtGui import QPainter, QColor, QPen, QMouseEvent, QLinearGradient, QPaintEvent

class MultiThumbSlider(QWidget):
    valuesChanged = Signal(list)
    thumbReleased = Signal()

    def __init__(self, minimum, maximum, num_thumbs, step, initial_values=None):
        super().__init__()
        self.minimum = minimum
        self.maximum = maximum
        self.num_thumbs = num_thumbs
        self.thumb_size = QSize(12, 20)
        self.thumb_positions = []
        self.step = step
        self.dragging_thumb = -1
        self.track_height = 4
        self.min_distance = 1

        if initial_values is None:
            self.values = self.calculate_initial_positions()
        else:
            self.validate_initial_values(initial_values)
            self.values = initial_values

        self.setMouseTracking(True)
        self.update()
        self.update_thumb_positions()
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        self.setFixedHeight(20)



    def calculate_initial_positions(self):
        if self.num_thumbs <= 1:
            return [self.minimum] if self.num_thumbs == 1 else []

        total_range = self.maximum - self.minimum
        available_range = total_range - (self.num_thumbs - 1) * self.min_distance
        if available_range <= 0:
            raise ValueError("Not enough space for all thumbs with given min_distance")

        step = available_range / (self.num_thumbs - 1)
        positions = [self.minimum + i * step for i in range(self.num_thumbs)]

        for i in range(1, self.num_thumbs):
            positions[i] += i * self.min_distance

        return positions

    def validate_initial_values(self, initial_values):
        if len(initial_values) != self.num_thumbs:
            raise ValueError("Number of initial values must match num_thumbs")
        initial_values.sort()
        for i in range(1, self.num_thumbs):
            if initial_values[i] <= initial_values[i - 1] + self.min_distance:
                raise ValueError("Initial values must be unique and have at least min_distance between them.")

    def update_thumb_positions(self):
        range_width = self.width() - self.thumb_size.width()
        if range_width <= 0:
            self.thumb_positions = []
            return
        self.thumb_positions = [int((v - self.minimum) / (self.maximum - self.minimum) * range_width) for v in self.values]

    def get_thumb_rect(self, index):
        thumb_y = (self.height() - self.thumb_size.height()) // 2
        return QRect(self.thumb_positions[index], thumb_y, self.thumb_size.width(), self.thumb_size.height())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for i, pos in enumerate(self.thumb_positions):
                if self.get_thumb_rect(i).contains(event.position().toPoint()):
                    self.dragging_thumb = i
                    self.update()
                    break
        elif event.button() == Qt.RightButton:  # Right-click handling
            for i in range(len(self.thumb_positions)):
                if self.get_thumb_rect(i).contains(event.position().toPoint()):
                    # Remove thumb
                    self.values.pop(i)
                    self.num_thumbs -= 1
                    self.update_thumb_positions()
                    self.update()
                    self.valuesChanged.emit(self.values)
                    return  # Important: Exit after removing a thumb

            # Add a new thumb at the clicked position if not removing
            pos = event.position().x()
            range_width = self.width() - self.thumb_size.width()
            if range_width > 0:
                value = self.minimum + (self.maximum - self.minimum) * pos / range_width
                value = round(value / self.step) * self.step  # Snap to step

                # Check if the snapped value is already present
                if value not in self.values:  # Only add if the value is unique
                    self.values.append(value)
                    self.values.sort()
                    self.num_thumbs += 1
                    self.update_thumb_positions()
                    self.update()
                    self.valuesChanged.emit(self.values)
        



    def mouseMoveEvent(self, event):
        if self.dragging_thumb != -1:
            range_width = self.width() - self.thumb_size.width()
            pos = event.position().x()
            new_value = self.minimum + (pos / range_width) * (self.maximum - self.minimum)
            new_value = min(max(self.minimum, new_value), self.maximum)
            new_value = round(new_value / self.step) * self.step  # Snap to step

            # Check for collisions and boundaries:
            if self.dragging_thumb > 0:
                new_value = max(new_value, self.values[self.dragging_thumb-1] + self.min_distance)
            if self.dragging_thumb < self.num_thumbs-1:
                new_value = min(new_value, self.values[self.dragging_thumb + 1] - self.min_distance)


            self.values[self.dragging_thumb] = new_value


            self.values.sort()
            self.update_thumb_positions()
            self.valuesChanged.emit(self.values)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging_thumb != -1:
            self.dragging_thumb = -1
            self.thumbReleased.emit()
            self.update()

    def paintEvent(self, event: QPaintEvent):
        self.update_thumb_positions()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        track_y = (self.height() - self.track_height) // 2
        painter.fillRect(0, track_y, self.width(), self.track_height, QColor(150, 150, 150))

        grad = QLinearGradient(0, track_y, self.width(), track_y)
        grad.setColorAt(0, QColor(100, 100, 100))
        grad.setColorAt(1, QColor(200, 200, 200))
        painter.fillRect(0, track_y, self.width(), self.track_height, grad)

        thumb_y = (self.height() - self.thumb_size.height()) // 2
        for pos in self.thumb_positions:
            painter.setPen(QPen(Qt.black, 1))
            painter.setBrush(QColor(50, 130, 184))
            painter.drawRoundedRect(pos, thumb_y, self.thumb_size.width(), self.thumb_size.height(), 3, 3)

    def showEvent(self, event):
        self.update_thumb_positions() # Если позиции зависят от размера
        self.update()
        super().showEvent(event) # Важно!
    def get_values(self):
        return self.values
    def get_maximum(self):
        return self.maximum
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    my_slider = MultiThumbSlider(0, 100, 2, 1)
    label = QLabel(f"Values: {my_slider.values}") # Fixed label text
    layout.addWidget(my_slider)
    layout.addWidget(label)
    window.setLayout(layout)

    def update_label(values):
        label.setText(f"Values: {values}")

    my_slider.valuesChanged.connect(update_label)


    window.show()
    sys.exit(app.exec())