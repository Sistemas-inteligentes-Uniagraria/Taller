import cv2
import numpy as np
import matplotlib.pyplot as plt

def draw_house_sun(image):
    # Dibujar casa (cuadrado)
    cv2.rectangle(image, (150, 250), (350, 450), (255, 0, 0), -1)  # Azul
    
    # Dibujar techo (triángulo)
    pts = np.array([[150, 250], [350, 250], [250, 150]], np.int32)
    cv2.polylines(image, [pts], isClosed=True, color=(0, 0, 255), thickness=3)
    cv2.fillPoly(image, [pts], (0, 0, 255))  # Rojo
    
    # Dibujar puerta (rectángulo)
    cv2.rectangle(image, (230, 350), (270, 450), (0, 255, 0), -1)  # Verde
    
    # Dibujar sol (círculo)
    cv2.circle(image, (400, 100), 50, (0, 255, 255), -1)  # Amarillo

# Crear imagen en negro
img = np.zeros((500, 500, 3), dtype=np.uint8)
draw_house_sun(img)

# Mostrar imagen original
plt.figure(figsize=(12, 4))
plt.subplot(1, 4, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Imagen Original")
plt.axis("off")

# Rotar 90 grados en sentido horario
matrix_rot = cv2.getRotationMatrix2D((250, 250), -90, 1)
rotated = cv2.warpAffine(img, matrix_rot, (500, 500))
plt.subplot(1, 4, 2)
plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
plt.title("Rotación 90°")
plt.axis("off")

# Escalar a tamaño menor (0.5x)
scaled = cv2.resize(img, None, fx=0.5, fy=0.5)
plt.subplot(1, 4, 3)
plt.imshow(cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB))
plt.title("Escalado 0.5x")
plt.axis("off")

# Trasladar imagen hacia la derecha y abajo
matrix_trans = np.float32([[1, 0, 50], [0, 1, 50]])
translated = cv2.warpAffine(img, matrix_trans, (500, 500))
plt.subplot(1, 4, 4)
plt.imshow(cv2.cvtColor(translated, cv2.COLOR_BGR2RGB))
plt.title("Traslación (50,50)")
plt.axis("off")

plt.show()