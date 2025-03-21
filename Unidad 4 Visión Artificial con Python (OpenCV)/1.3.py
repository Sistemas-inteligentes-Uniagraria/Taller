import cv2

def process_video():
    cap = cv2.VideoCapture(0)  # Captura desde la cámara web
    
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Aplicar filtro Gaussiano para reducir ruido
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        
        # Aplicar detección de bordes con Canny
        edges = cv2.Canny(blurred, 50, 150)
        
        # Mostrar los resultados
        cv2.imshow("Original", frame)
        cv2.imshow("Suavizado Gaussiano", blurred)
        cv2.imshow("Detección de Bordes (Canny)", edges)
        
        # Presionar 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video()
