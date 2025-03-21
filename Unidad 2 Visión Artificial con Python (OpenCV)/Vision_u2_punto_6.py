import cv2
import numpy as np

video = cv2.VideoCapture(0)
ret, frame_b = video.read()
frame_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)
frame_b = cv2.GaussianBlur(frame_b, (21,21),0)

while True:
    ret, frame_a = video.read()
    if not ret:
        break
    gris = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (21,21),0)

    compara = cv2.absdiff(frame_b, gris)
    _, mascara = cv2.threshold(compara, 30, 55,cv2.THRESH_BINARY)
    mascara = cv2.dilate(mascara, None, iterations=2)
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contorno in contornos:
        if cv2.contourArea(contorno)< 500:
            continue
        (x,y,w,h)=cv2.boundingRect(contorno)
        cv2.rectangle(frame_a, (x,y), (x+w,y+h), (0,255,0),2)
    cv2.imshow("Imagen en movimiento (Se cierra con j)", frame_a)   
    frame_b = gris.copy()     
    if cv2.waitKey(1)& 0xFF == ord('j'):
        break

video.release()
cv2.destroyAllWindows()  