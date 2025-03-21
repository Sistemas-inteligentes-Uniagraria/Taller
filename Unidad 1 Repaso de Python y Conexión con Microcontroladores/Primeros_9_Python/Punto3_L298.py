import serial
import time


arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2)  

def control_motor(comando):
    arduino.write(comando.encode())  # Enviar comando a Arduino
    print(f"Comando enviado: {comando}")

try:
    while True:
        # Menú de opciones
        print("1. Girar en sentido horario (D)")
        print("2. Girar en sentido antihorario (A)")
        print("3. Detener motor (S)")
        print("4. Ajustar velocidad (0-9)")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            control_motor('D')  # Sentido horario
        elif opcion == '2':
            control_motor('A')  # Sentido antihorario
        elif opcion == '3':
            control_motor('S')  # Detener motor
        elif opcion == '4':
            velocidad = input("Ingresa la velocidad (0-9): ")
            if velocidad.isdigit() and 0 <= int(velocidad) <= 9:
                control_motor(velocidad)  # Ajustar velocidad
            else:
                print("Velocidad inválida. Debe ser un número entre 0 y 9.")
        elif opcion == '5':
            break  # Salir del programa
        else:
            print("Opción inválida. Intenta de nuevo.")
except KeyboardInterrupt:
    print("Programa terminado")

arduino.close()