#include <Servo.h>

// Definición de pines
#define LED1 2
#define LED2 3
#define IN1 4
#define IN2 5
#define ENA 6
#define SERVO 9

// Crear un objeto Servo
Servo miServo;

void setup() {
  // Configurar pines como salida
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  // Conectar el servomotor al pin 9
  miServo.attach(SERVO);

  // Iniciar comunicación serial
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Leer el comando enviado desde Python
    String comando = Serial.readStringUntil('\n'); // Leer hasta el salto de línea

    // Procesar el comando
    if (comando.startsWith("LED1")) {
      // Controlar LED 1
      int estado = comando.substring(5).toInt(); // Leer el estado (0 o 1)
      digitalWrite(LED1, estado);
      Serial.println("LED1 actualizado: " + String(estado));
    } else if (comando.startsWith("LED2")) {
      // Controlar LED 2
      int estado = comando.substring(5).toInt(); // Leer el estado (0 o 1)
      digitalWrite(LED2, estado);
      Serial.println("LED2 actualizado: " + String(estado));
    } else if (comando.startsWith("MOTOR")) {
      // Controlar el motor DC
      char accion = comando.charAt(6); // Leer la acción (D, A, S o velocidad)
      if (accion == 'D') {
        // Girar en sentido horario (adelante)
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        Serial.println("Motor: Adelante");
      } else if (accion == 'A') {
        // Girar en sentido antihorario (atrás)
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        Serial.println("Motor: Atrás");
      } else if (accion == 'S') {
        // Detener el motor
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        Serial.println("Motor: Detenido");
      } else if (accion >= '0' && accion <= '9') {
        // Ajustar la velocidad
        int velocidad = map(accion - '0', 0, 9, 0, 255); // Mapear a PWM (0-255)
        analogWrite(ENA, velocidad);
        Serial.println("Motor: Velocidad ajustada a " + String(velocidad));
      } else {
        Serial.println("Comando de motor no reconocido: " + String(accion));
      }
    } else if (comando.startsWith("SERVO")) {
      // Controlar el servomotor
      int angulo = comando.substring(6).toInt(); // Leer el ángulo (0-180)
      miServo.write(angulo);
      Serial.println("Servo movido a: " + String(angulo));
    } else {
      Serial.println("Comando no reconocido: " + comando);
    }
  }
}
