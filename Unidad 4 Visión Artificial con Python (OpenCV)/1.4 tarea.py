import cv2

def detect_contours():
    cap = cv2.VideoCapture(0)  # Captura desde la cámara web
    
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Aplicar desenfoque para reducir ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detección de bordes con Canny
        edges = cv2.Canny(blurred, 50, 150)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Dibujar contornos sobre la imagen original
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
        
        # Mostrar los resultados
        cv2.imshow("Original con Contornos", frame)
        cv2.imshow("Escala de Grises", gray)
        cv2.imshow("Bordes Canny", edges)
        
        # Presionar 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_contours()
