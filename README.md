# Sistemas Inteligentes e IA

## 📌 Descripción del Proyecto

Este repositorio contiene las actividades y prácticas realizadas en el curso **Sistemas Inteligentes e IA**, de la **Fundación Universitaria Agraria de Colombia (UNIAGRARIA)**.

El objetivo principal es la integración de Python con microcontroladores y la implementación de visión artificial mediante OpenCV, abordando temas clave como comunicación serial, control de hardware y procesamiento de imágenes.

---

### 🔹 Unidad 1: Repaso de Python y Conexión con Microcontroladores

1. **Encender y apagar un LED desde Python**: Configuración de comunicación serial entre Python y Arduino para controlar un LED.
2. **Leer la temperatura con un sensor DHT11**: Lectura de valores de temperatura y humedad desde Arduino y visualización en Python.
3. **Controlar un motor DC desde Python**: Uso de un driver L298N para ajustar velocidad y dirección del motor.
4. **Recibir datos de un sensor ultrasónico HC-SR04**: Lectura de distancia en tiempo real mediante Python.
5. **Simular datos de sensores en Python**: Generación de datos ficticios para probar el procesamiento en Arduino.
6. **Controlar un servomotor desde Python**: Manipulación de un servomotor enviando comandos desde Python.
7. **Enviar múltiples comandos a Arduino**: Sistema de comunicación serial para gestionar distintos dispositivos.
8. **Registrar y visualizar datos en tiempo real**: Uso de Matplotlib para graficar información en vivo.
9. **Configurar un sistema de alertas**: Notificaciones en Python cuando sensores detectan valores críticos.

---

### 🔹 Unidad 2: Visión Artificial con Python (OpenCV)

1. **Capturar video en tiempo real con OpenCV**: Acceder a una cámara y visualizar la transmisión.
2. **Detectar colores en imágenes o video**: Identificación y resaltado de colores específicos.
3. **Identificar y seguir objetos en movimiento**: Seguimiento de trayectorias en tiempo real.
4. **Reconocimiento facial**: Implementación de detección de rostros con OpenCV.
5. **Segmentación de imágenes**: Técnicas para separar objetos del fondo.
6. **Detección de movimiento en video**: Comparación de frames para identificar cambios.
7. **Aplicación de filtros en imágenes**: Implementación de filtros como Canny y GaussianBlur.
8. **Extracción de características en imágenes**: Cálculo de área, perímetro y forma de objetos.
9. **Reconocimiento de patrones en imágenes**: Identificación de figuras geométricas.

---

### 🔹 Unidad 3: Python y Microcontroladores (Integración Completa)

Esta unidad integra los siguientes puntos en un mismo código de ESP32 y en la interfaz HMI de Python:

1. **Lectura y registro de datos de un sensor LDR**.
2. **Envío de datos desde Python a una pantalla LCD mediante I2C**.
3. **Comunicación bidireccional entre Python y Arduino**.
4. **Detección de interrupciones en Arduino desde Python**.
5. **Control de velocidad de un ventilador en función de la temperatura**.

---

### 🔹 Unidad 4: Visión Artificial con OpenCV

1. **Análisis de espacios de color en imágenes**.
2. **Transformaciones geométricas en imágenes**.
3. **Filtrado de imágenes en tiempo real**.
4. **Detección de contornos en video**.
5. **Detección de bordes con el operador de Sobel**.

---

## ⚙️ Instalación y Requisitos

Para ejecutar los scripts, asegúrate de tener instaladas las siguientes dependencias:

```bash
pip install opencv-python numpy matplotlib serial
```

Si trabajas con Arduino, instala la biblioteca `pyserial`:

```bash
pip install pyserial
```

---

## 🚀 Uso del Proyecto

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   ```
2. Accede al directorio del proyecto:
   ```bash
   cd tu_repositorio
   ```
3. Ejecuta los scripts según la unidad y tema que desees probar.

---

## 📜 Autor

**Ing. Christian Alejandro Pineda Torres**\
Departamento de Ingeniería Mecatrónica\
Fundación Universitaria Agraria de Colombia - UNIAGRARIA\
Versión: 1 (2025)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Puedes consultarla [aquí](LICENSE).

