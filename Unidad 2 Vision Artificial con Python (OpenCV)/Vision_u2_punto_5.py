import cv2
import numpy as np

imagen1 = cv2.imread(r'C:\Users\dcosm\Documents\GitHub\Taller\Unidad 2 Vision Artificial con Python (OpenCV)\cerebro.jpg')
imagen1 = cv2.resize(imagen1, (400,300))
imagen = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
_, binaria = cv2.threshold(imagen, 100, 255, cv2.THRESH_BINARY)
contornos,_ = cv2.findContours(binaria, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
pic = cv2.drawContours(imagen, contornos, -1,(15,255,10),2)

cv2.imshow("Original", imagen1)
cv2.imshow("Binaria", binaria)
cv2.imshow("Contornos", pic)

cv2.waitKey()
cv2.destroyAllWindows()
   
