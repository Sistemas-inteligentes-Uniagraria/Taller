void setup() {
  // Iniciar comunicación serial
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    // Leer el dato enviado desde Python
    String dato = Serial.readStringUntil('\n'); // Leer hasta el salto de línea

    // Imprimir el dato recibido en el monitor serial
    Serial.print("Dato recibido: ");
    Serial.println(dato); // Mostrar el dato en el monitor serial
  }
}
