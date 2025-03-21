#include <Servo.h>

// Crear un objeto Servo
Servo miServo;

void setup() {
  // Iniciar comunicación serial
  Serial.begin(9600);

  // Conectar el servomotor al pin 9
  miServo.attach(9);
}

void loop() {
  if (Serial.available() > 0) {
    // Leer el ángulo enviado desde Python
    int angulo = Serial.parseInt(); // Leer un número entero

    // Verificar que el ángulo esté en el rango válido (0 a 180)
    if (angulo >= 0 && angulo <= 180) {
      // Mover el servomotor al ángulo especificado
      miServo.write(angulo);
      Serial.print("Servo movido a: ");
      Serial.println(angulo);
    } else {
      Serial.println("Ángulo inválido. Debe ser entre 0 y 180.");
    }
  }
}
