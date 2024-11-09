import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, bgrImage):
        if bgrImage is None:
            raise ValueError("Изображение пусто")
        self.image = bgrImage
        self.Lchanel = self.calculateLchanel()
    def calculateLchanel(self):
        L_image, A, B = cv2.split(cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB))
        return L_image
    def getLChanel(self):
        return self.Lchanel
    def getRGBimage(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
    def blurGaussian(self, kernel: tuple, sigmaX: float, sigmaY: float) -> np.ndarray:
        return cv2.GaussianBlur(self.getLChanel(), kernel, sigmaX=sigmaX, sigmaY=sigmaY)
    def calculateMeanL(self):
        L = self.getLChanel()
        return np.mean(L)
    def calculateMeanRelativeToPartition(self, partition: list):
        partsOfImage = []
        L = self.getLChanel()
        print(np.shape(L))
        endPixelX = 0
        for part in partition:
            imageSlice = L[endPixelX:part, :]
            print(np.shape(imageSlice))
            partsOfImage.append(imageSlice)

    def applyConvolution(self, image, kernel):
        return cv2.filter2D(image, -1, kernel)