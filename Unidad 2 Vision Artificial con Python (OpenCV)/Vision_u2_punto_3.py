import cv2
import numpy as np

detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0)
while True:
    ret, frame = video.read()
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    caras = detector.detectMultiScale(gris, 1.3, 5)    
    mascara = np.zeros_like(frame)        
    
    for (x, y, w, h) in caras:
        cv2.rectangle(mascara, (x,y), (x+w,y+h), (255,155,255),-1)    

    fondo_negro = cv2.bitwise_and(frame, mascara)
    cv2.imshow("Seguimiento de Rostros (Se cierra con j)", fondo_negro)

    if cv2.waitKey(1)& 0xFF == ord('j'):
        break
video.release()
cv2.destroyAllWindows()   
