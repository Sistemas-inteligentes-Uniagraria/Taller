import cv2
import os

ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_imagen = os.path.join(ruta_script, "rostros.jpg")

detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
imagen = cv2.imread(ruta_imagen)
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
rostros_d = detector.detectMultiScale(grises, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

for (x, y, w, h) in rostros_d:
    cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow('Detección de Rostros', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()

detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
video = cv2.VideoCapture(0)
while True:
    ret, frame = video.read()
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    caras = detector.detectMultiScale(gris, 1.3, 5)

    for (x, y, w, h) in caras:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),2)
    cv2.imshow("Rostro (Cierra con j)", frame)

    if cv2.waitKey(1)& 0xFF == ord('j'):
        break
video.release()
cv2.destroyAllWindows()    

