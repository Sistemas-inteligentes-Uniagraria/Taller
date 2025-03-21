import serial
import time


arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2)  

def mover_servo(angulo):
    # Enviar el ángulo a Arduino
    arduino.write(f"{angulo}\n".encode())  # Enviar como cadena con salto de línea
    print(f"Ángulo enviado: {angulo}")

try:
    while True:
        # Menú de opciones
        print("1. Mover a 0 grados")
        print("2. Mover a 90 grados")
        print("3. Mover a 180 grados")
        print("4. Ingresar ángulo manualmente")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            mover_servo(0)  # Mover a 0 grados
        elif opcion == '2':
            mover_servo(90)  # Mover a 90 grados
        elif opcion == '3':
            mover_servo(180)  # Mover a 180 grados
        elif opcion == '4':
            angulo = int(input("Ingresa el ángulo (0-180): "))
            if 0 <= angulo <= 180:
                mover_servo(angulo)  # Mover al ángulo especificado
            else:
                print("Ángulo inválido. Debe ser entre 0 y 180.")
        elif opcion == '5':
            break  # Salir del programa
        else:
            print("Opción inválida. Intenta de nuevo.")
except KeyboardInterrupt:
    print("Programa terminado")

arduino.close()