import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, bgrImage):
        if bgrImage is None:
            raise ValueError("Изображение пусто")
        self.image = bgrImage
    def getLchanel(self):
        L_image, A, B = cv2.split(cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB))
        return L_image
    def getRGBimage(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
    def blurGaussian(self, kernel: tuple, sigmaX: float, sigmaY: float) -> np.ndarray:
        return cv2.GaussianBlur(self.getLchanel(), kernel, sigmaX=sigmaX, sigmaY=sigmaY)
    def calculateMeanL(self):
        L = self.getLchanel()
        return np.mean(L)
    def applyConvolution(self, image, kernel):
        return cv2.filter2D(image, -1, kernel)