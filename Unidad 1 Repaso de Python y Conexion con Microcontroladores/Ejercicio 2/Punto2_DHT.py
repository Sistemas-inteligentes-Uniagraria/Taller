import serial
import time

# Configura el puerto serial (ajusta el puerto según tu sistema)
arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2)  # Espera a que se establezca la conexión

try:
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            print(line)
except KeyboardInterrupt:
    print("Programa terminado")

arduino.close()