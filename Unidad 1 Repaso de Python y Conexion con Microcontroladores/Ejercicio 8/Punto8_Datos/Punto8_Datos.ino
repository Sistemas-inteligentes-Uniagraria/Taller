void setup() {
  // Iniciar comunicación serial
  Serial.begin(9600);
}

void loop() {
  // Leer el valor del potenciómetro (0-1023)
  int valor = analogRead(A0);

  // Enviar el valor al puerto serial
  Serial.println(valor);

  // Esperar un momento antes de la siguiente lectura
  delay(100);
}
