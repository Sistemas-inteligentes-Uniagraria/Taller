import cv2
import numpy as np

imagen_o = cv2.imread(r'C:\Users\dcosm\Documents\GitHub\Taller\Unidad 2 Vision Artificial con Python (OpenCV)\lady2.jpg')
imagen_o = cv2.resize(imagen_o, (600,450))
imagen = cv2.cvtColor(imagen_o, cv2.COLOR_BGR2GRAY)
desenfoque = cv2.GaussianBlur(imagen, (3,3),0)
bordes = cv2.Canny(desenfoque, 10, 50)
_, binaria =cv2.threshold(bordes, 60,250, cv2.THRESH_BINARY)

cv2.imshow("Imagen original", imagen_o)
cv2.imshow("Imagen procesada", binaria)

cv2.waitKey()
cv2.destroyAllWindows()
