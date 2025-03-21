import serial
import time


arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2)  

try:
    while True:
        if arduino.in_waiting > 0:
            # Leer la línea enviada por Arduino
            distancia = arduino.readline().decode('utf-8').rstrip()
            print(f"Distancia: {distancia} cm")
except KeyboardInterrupt:
    print("Programa terminado")

arduino.close()