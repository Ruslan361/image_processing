import cv2
import numpy as np
from PySide6.QtWidgets import QFileDialog

class ImageHandler:
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            None, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg)"
        )
        if file_name:
            return cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), cv2.IMREAD_COLOR)
        return None
    
    def save_image(self, image):
        file_name, _ = QFileDialog.getSaveFileName(
            None, "Сохранить изображение", "", "Изображения (*.png *.jpg *.jpeg)"
        )
        if file_name:
            # Сохраняем изображение с использованием OpenCV
            # cv2.imwrite требует байтовый массив, поэтому мы используем numpy для обработки пути с русскими символами.
            ext = file_name.split('.')[-1]  # Определяем расширение файла
            success, encoded_image = cv2.imencode(f'.{ext}', image)
            if success:
                encoded_image.tofile(file_name)
    
    def save_figure(self, figure):
        # Открываем диалоговое окно для сохранения
        file_name, _ = QFileDialog.getSaveFileName(
            None, "Сохранить изображение", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)"
        )
        
        # Если путь указан, сохраняем фигуру
        if file_name:
            figure.savefig(file_name)
