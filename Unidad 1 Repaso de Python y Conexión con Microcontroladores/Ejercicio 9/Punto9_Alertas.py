import serial
import time

arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2) 

try:
    while True:
        if arduino.in_waiting > 0:
            # Leer la línea enviada por Arduino
            linea = arduino.readline().decode('utf-8').rstrip()
            print(linea)  # Mostrar la línea en la consola

            # Verificar si la línea contiene una alerta
            if "ALERTA" in linea:
                print("¡Atención! Se ha detectado una alerta:", linea)
except KeyboardInterrupt:
    print("Programa terminado")

arduino.close()