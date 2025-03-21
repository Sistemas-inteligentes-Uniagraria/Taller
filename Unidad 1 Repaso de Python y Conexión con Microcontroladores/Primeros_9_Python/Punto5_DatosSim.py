import serial
import time
import random


arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2)  # Esperar a que se establezca la conexión

try:
    while True:
        # Generar un valor simulado de sensor 
        valor_simulado = random.uniform(20.0, 30.0)
        valor_simulado = round(valor_simulado, 2)  # Redondear a 2 decimales

        # Enviar el valor a Arduino
        arduino.write(f"{valor_simulado}\n".encode())  # Enviar como cadena con salto de línea
        print(f"Enviado: {valor_simulado}")

        # Esperar un momento antes de enviar el siguiente valor
        time.sleep(2)
except KeyboardInterrupt:
    print("Programa terminado")

arduino.close()