import serial
import matplotlib.pyplot as plt
from collections import deque
import time


arduino = serial.Serial('COM2', 9600, timeout=1)
time.sleep(2)  

# Configuración de la gráfica
plt.ion()  # Habilitar modo interactivo
fig, ax = plt.subplots()
x = deque(maxlen=100)  # Almacenar los últimos 100 valores
y = deque(maxlen=100)
line, = ax.plot(x, y)

# Configuración de la gráfica
ax.set_ylim(0, 1023)  # Rango del potenciómetro (0-1023)
ax.set_xlabel("Tiempo")
ax.set_ylabel("Valor del sensor")
ax.set_title("Gráfica en tiempo real del sensor")

try:
    while True:
        if arduino.in_waiting > 0:
            # Leer el valor enviado por Arduino
            valor = arduino.readline().decode('utf-8').rstrip()
            if valor.isdigit():  # Verificar que sea un número válido
                valor = int(valor)
                print(f"Valor recibido: {valor}")

                # Agregar el valor a la gráfica
                x.append(time.time())  # Usar el tiempo actual como eje X
                y.append(valor)

                # Actualizar la gráfica
                line.set_xdata(x)
                line.set_ydata(y)
                ax.set_xlim(min(x), max(x))  # Ajustar el rango del eje X
                plt.draw()
                plt.pause(0.01)  # Pausa para actualizar la gráfica

except KeyboardInterrupt:
    print("Programa terminado")

arduino.close()  # Cerrar el puerto serial