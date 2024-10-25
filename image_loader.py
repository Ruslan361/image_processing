import cv2
import numpy as np
from PySide6.QtWidgets import QFileDialog
class ImageLoader:
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            None, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg)"
        )
        if file_name:
            return cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), cv2.IMREAD_COLOR)
        return None
