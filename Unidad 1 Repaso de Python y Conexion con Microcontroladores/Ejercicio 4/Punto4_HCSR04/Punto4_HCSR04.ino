// Definición de pines
const int trigPin = 9;  // Pin Trig del HC-SR04
const int echoPin = 10; // Pin Echo del HC-SR04

void setup() {
  // Configurar pines
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Iniciar comunicación serial
  Serial.begin(9600);
}

void loop() {
  // Medir la distancia
  long duracion, distancia;
  
  // Enviar un pulso corto al pin Trig
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Medir el tiempo de respuesta del pin Echo
  duracion = pulseIn(echoPin, HIGH);

  // Calcular la distancia en centímetros
  distancia = duracion * 0.034 / 2;

  // Enviar la distancia al puerto serial
  Serial.println(distancia);

  // Esperar un momento antes de la siguiente medición
  delay(100);
}
