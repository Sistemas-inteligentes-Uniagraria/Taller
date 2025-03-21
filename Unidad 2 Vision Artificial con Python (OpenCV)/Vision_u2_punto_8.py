import cv2
import numpy as np

imagen = cv2.imread(r'C:\Users\dcosm\Documents\GitHub\Taller\Unidad 2 Vision Artificial con Python (OpenCV)\formas2.jpeg')
imagen = cv2.resize(imagen, (600, 550))
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
gaus = cv2.GaussianBlur(gris, (5, 5), 0)
_, binaria = cv2.threshold(gaus, 200, 255, cv2.THRESH_BINARY_INV)

contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contorno in contornos:
    if cv2.contourArea(contorno) > 300:  
        cv2.drawContours(imagen, [contorno], -1, (0, 255, 0), 2)

        area = cv2.contourArea(contorno)
        perimetro = cv2.arcLength(contorno, True)
        epsilon = 0.02 * perimetro
        aproximacion = cv2.approxPolyDP(contorno, epsilon, True)

        if len(aproximacion) == 3:
            forma = "Triángulo"
        elif len(aproximacion) == 4:
            (x, y, w, h) = cv2.boundingRect(contorno)
            aspecto = w / float(h)
            forma = "Cuadrado" if 0.9 < aspecto < 1.1 else "Rectángulo"
        elif len(aproximacion) > 6:
            forma = "Círculo"
        else:
            forma = "Desconocido"

        M = cv2.moments(contorno)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.putText(imagen, f"{forma}, A:{int(area)}", (cx - 50, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

cv2.imshow("Detección de objetos", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()

