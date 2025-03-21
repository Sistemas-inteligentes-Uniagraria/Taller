// Definición de pines
#define IN1 8
#define IN2 9
#define ENA 10

void setup() {
  // Configurar pines como salida
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  // Iniciar comunicación serial
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Leer el comando enviado desde Python
    char comando = Serial.read();

    // Controlar el motor según el comando
    switch (comando) {
      case 'D': // Girar en sentido horario
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        break;
      case 'A': // Girar en sentido antihorario
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        break;
      case 'S': // Detener el motor
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        break;
      default:
        // Si el comando es un número (0-9), ajustar la velocidad
        if (comando >= '0' && comando <= '9') {
          int velocidad = map(comando - '0', 0, 9, 0, 255); // Mapear a PWM (0-255)
          analogWrite(ENA, velocidad);
        }
        break;
    }
  }
}
