#include <DHT.h>

#define DHTPIN 2      // Pin donde está conectado el DHT11
#define DHTTYPE DHT11 // Tipo de sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  // Leer la humedad
  float humedad = dht.readHumidity();
  // Leer la temperatura en Celsius
  float temperatura = dht.readTemperature();

  // Verificar si la lectura falló
  if (isnan(humedad) || isnan(temperatura)) {
    Serial.println("Error al leer el sensor DHT11");
    return;
  }

  // Enviar los datos al puerto serial
  Serial.print("Humedad: ");
  Serial.print(humedad);
  Serial.print(" %\t");
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" *C");

  // Esperar 2 segundos antes de la siguiente lectura
  delay(2000);
}
