import cv2
import numpy as np
import matplotlib.pyplot as plt

def sobel_edge_detection(image_path):
    # Cargar imagen en escala de grises
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print("Error: No se pudo cargar la imagen.")
        return
    
    # Aplicar operador de Sobel en las direcciones X e Y
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    
    # Convertir a valores absolutos y escalar a 8 bits
    sobel_x = cv2.convertScaleAbs(sobel_x)
    sobel_y = cv2.convertScaleAbs(sobel_y)
    
    # Combinar los bordes detectados en X e Y
    sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
    
    # Mostrar resultados
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title("Imagen Original")
    plt.axis("off")
    
    plt.subplot(1, 3, 2)
    plt.imshow(sobel_x, cmap='gray')
    plt.title("Bordes Sobel X")
    plt.axis("off")
    
    plt.subplot(1, 3, 3)
    plt.imshow(sobel_y, cmap='gray')
    plt.title("Bordes Sobel Y")
    plt.axis("off")
    
    plt.show()

# Ejecutar la detección con una imagen de prueba
sobel_edge_detection('12.jpg')  # Reemplaza con la ruta de tu imagen
