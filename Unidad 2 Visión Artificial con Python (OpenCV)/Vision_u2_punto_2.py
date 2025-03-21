import cv2
import numpy as np

bajo_verde = np.array([0,90,0], dtype=np.uint8) 
alto_verde = np.array([200,255,250], dtype=np.uint8) 
pregunta = int(input("""Desea analizar los verdes en:
                1. Video
                2. Imagen
                  :  """))

if pregunta == 1:
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame= cap.read()
        if not ret:
            break        
        mascara = cv2.inRange(frame, bajo_verde, alto_verde)
        frame = cv2.bitwise_or(frame, frame, mask=mascara)
        frame = cv2.resize(frame, (800,600))
        cv2.imshow("Camara en vivo (Se cierra con j)", frame) # Mostrar frame        
        if cv2.waitKey(1)& 0xFF == ord('j'):
            break
elif pregunta == 2:
    imagen = cv2.imread(r'C:\Users\Yesenia\Documents\poo\IA\bosque.jpg')
    imagen = cv2.resize(imagen, (700, 550))
    mascara_1 = cv2.inRange(imagen, bajo_verde, alto_verde)
    imagen = cv2.bitwise_or(imagen, imagen, mask=mascara_1)
    cv2.imshow("Imagen analizada", imagen) # Mostrar imagen
    cv2.waitKey()
    cv2.destroyAllWindows()
else:
    print("Error, en la lectura de datos")    
cap.release()
cv2.destroyAllWindows()       
           
