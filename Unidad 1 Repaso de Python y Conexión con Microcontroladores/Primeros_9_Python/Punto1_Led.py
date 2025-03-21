import serial
import time

# Configura el puerto serial
arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2) 

def encender_led():
    arduino.write(b'1')  # Envía el comando para encender el LED
    response = arduino.readline().decode('utf-8').strip()  # Lee la respuesta de Arduino
    print(response)

def apagar_led():
    arduino.write(b'0')  # Envía el comando para apagar el LED
    response = arduino.readline().decode('utf-8').strip()  # Lee la respuesta de Arduino
    print(response)

def mostrar_menu():
    print("\n--- Menú de Control del LED ---")
    print("1. Encender el LED")
    print("2. Apagar el LED")
    print("3. Salir")

# Bucle principal
while True:
    mostrar_menu()  # Muestra el menú
    opcion = input("Selecciona una opción (1, 2 o 3): ")  # Solicita la opción al usuario

    if opcion == '1':
        encender_led()  # Enciende el LED
    elif opcion == '2':
        apagar_led()  # Apaga el LED
    elif opcion == '3':
        print("Saliendo del programa...")
        break  # Sale del bucle y termina el programa
    else:
        print("Opción no válida. Por favor, selecciona 1, 2 o 3.")

# Cierra la conexión serial
arduino.close()