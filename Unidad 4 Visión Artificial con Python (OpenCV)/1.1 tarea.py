import cv2

# Cargar imagen en BGR (OpenCV usa BGR por defecto)
imagen = cv2.imread("12.jpg")

# Convertir la imagen a diferentes espacios de color
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
imagen_lab = cv2.cvtColor(imagen, cv2.COLOR_BGR2LAB)
imagen_ycrcb = cv2.cvtColor(imagen, cv2.COLOR_BGR2YCrCb)
imagen_xyz = cv2.cvtColor(imagen, cv2.COLOR_BGR2XYZ)


# Mostrar las imágenes en ventanas separadas
cv2.imshow("Imagen Original (BGR)", imagen)
cv2.imshow("Escala de Grises", imagen_gris)
cv2.imshow("Espacio de Color HSV", imagen_hsv)
cv2.imshow("Espacio de Color LAB", imagen_lab)
cv2.imshow("Espacio de Color YCrCb", imagen_ycrcb)
cv2.imshow("Espacio de Color XYZ", imagen_xyz)

canales = {

    "HSV": imagen_hsv,
    "LAB": imagen_lab,
    "YCrCb": imagen_ycrcb,
    "XYZ": imagen_xyz
}

for espacio, img in canales.items():
    for i in range(3):  # Cada imagen tiene 3 canales
        cv2.imshow(f"{espacio} - Canal {i+1} (Shape: {img[:,:,i].shape})", img[:, :, i])


# Esperar tecla para cerrar todas las ventanas
cv2.waitKey(0)
cv2.destroyAllWindows()