import cv2
cap = cv2.VideoCapture(0) 

while True:
    ret, frame= cap.read()
    if not ret:
        break

    cv2.imshow("Camara en vivo (Se cierra con j)", frame) 
    frame = cv2.resize(frame, (800,800))
    if cv2.waitKey(1)& 0xFF == ord('j'):
        break
cap.release()
cv2.destroyAllWindows()    