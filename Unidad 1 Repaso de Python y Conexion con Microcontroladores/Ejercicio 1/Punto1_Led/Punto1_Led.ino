const int ledPin = 13;  // Pin donde está conectado el LED

void setup() {
  pinMode(ledPin, OUTPUT);  
  Serial.begin(9600);     
  Serial.println("Arduino listo. Envia '1' para encender el LED y '0' para apagarlo.");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readString();
    command.trim();  // Elimina espacios y saltos de línea

    if (command == "1") {
      digitalWrite(ledPin, HIGH);
      Serial.println("LED encendido");
    } else if (command == "0") {
      digitalWrite(ledPin, LOW);
      Serial.println("LED apagado");
    } else {
      Serial.println("Comando no reconocido");
    }
    
    delay(0);  // Pequeño retardo para evitar problemas de lectura
  }
}
