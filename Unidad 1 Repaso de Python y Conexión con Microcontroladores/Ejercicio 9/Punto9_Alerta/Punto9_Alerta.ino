#include <DHT.h>

// Definición de pines y constantes
#define DHTPIN 2          // Pin donde está conectado el DHT11
#define DHTTYPE DHT11     // Tipo de sensor DHT
#define pinSensorGas A0   // Pin donde está conectado el MQ-2

// Umbrales de alerta
const float umbralTemperatura = 30.0; // Umbral de temperatura en °C
const int umbralGas = 500;            // Umbral de gas (ajusta según el sensor)

// Crear un objeto DHT
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Iniciar comunicación serial
  Serial.begin(9600);

  // Iniciar el sensor DHT
  dht.begin();
}

void loop() {
  // Leer la temperatura
  float temperatura = dht.readTemperature();

  // Leer el valor del sensor de gas
  int valorGas = analogRead(pinSensorGas);

  // Verificar si las lecturas son válidas
  if (isnan(temperatura)) {
    Serial.println("Error al leer el sensor DHT11");
  } else {
    // Enviar la temperatura al puerto serial
    Serial.print("Temperatura: ");
    Serial.println(temperatura);

    // Enviar alerta si la temperatura supera el umbral
    if (temperatura > umbralTemperatura) {
      Serial.println("ALERTA: Temperatura alta!");
    }
  }

  // Enviar el valor del sensor de gas al puerto serial
  Serial.print("Valor de gas: ");
  Serial.println(valorGas);

  // Enviar alerta si el valor de gas supera el umbral
  if (valorGas > umbralGas) {
    Serial.println("ALERTA: Gas detectado!");
  }

  // Esperar 2 segundos antes de la siguiente lectura
  delay(2000);
}
