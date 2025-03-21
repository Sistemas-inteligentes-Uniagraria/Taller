import serial
import time


arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2) 

def enviar_comando(comando):
    # Enviar el comando a Arduino
    arduino.write(f"{comando}\n".encode())  # Enviar como cadena con salto de línea
    print(f"Comando enviado: {comando}")

try:
    while True:
        # Menú de opciones
        print("1. Encender/Apagar LED 1")
        print("2. Encender/Apagar LED 2")
        print("3. Mover motor adelante (D)")
        print("4. Mover motor atrás (A)")
        print("5. Detener motor (S)")
        print("6. Ajustar velocidad del motor (0-9)")
        print("7. Mover servomotor")
        print("8. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            estado = input("Estado de LED 1 (0 para apagar, 1 para encender): ")
            enviar_comando(f"LED1 {estado}")
        elif opcion == '2':
            estado = input("Estado de LED 2 (0 para apagar, 1 para encender): ")
            enviar_comando(f"LED2 {estado}")
        elif opcion == '3':
            enviar_comando("MOTOR D")  # Adelante
        elif opcion == '4':
            enviar_comando("MOTOR A")  # Atrás
        elif opcion == '5':
            enviar_comando("MOTOR S")  # Detener
        elif opcion == '6':
            velocidad = input("Ingresa la velocidad (0-9): ")
            if velocidad.isdigit() and 0 <= int(velocidad) <= 9:
                enviar_comando(f"MOTOR {velocidad}")  # Ajustar velocidad
            else:
                print("Velocidad inválida. Debe ser un número entre 0 y 9.")
        elif opcion == '7':
            angulo = input("Ángulo del servomotor (0-180): ")
            enviar_comando(f"SERVO {angulo}")
        elif opcion == '8':
            break  # Salir del programa
        else:
            print("Opción inválida. Intenta de nuevo.")
except KeyboardInterrupt:
    print("Programa terminado")

arduino.close()