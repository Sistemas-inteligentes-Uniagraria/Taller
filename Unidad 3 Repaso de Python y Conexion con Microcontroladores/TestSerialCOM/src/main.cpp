#include <Arduino.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <max6675.h>

#define LDR_PIN 34
#define TEMP_SENSOR_DO 19
#define TEMP_SENSOR_CS 23
#define TEMP_SENSOR_CLS 5
#define FAN_PWM_PIN 25
#define BUTTON_PIN 13

LiquidCrystal_I2C lcd(0x27, 16, 2);

MAX6675 thermocouple(TEMP_SENSOR_CLS, TEMP_SENSOR_CS, TEMP_SENSOR_DO);
float temp;
int SetTemp = 50;
int MinTemp = 15;

int LDR;

enum class DisplayMode : uint8_t {
  NONE      = 0x00,
  TEMP      = 0x01,
  LDR       = 0x02,
  LCD       = 0x04,
  BUTTON    = 0x08
};
DisplayMode displayMode = DisplayMode::NONE;
DisplayMode lastDisplayMode = DisplayMode::NONE;

float lastTemp;
float lastSetTemp;
int lastLDR = -1;
bool lastButtonState = false;

const unsigned long BAUD_RATE = 250000;
const size_t BUFFER_SIZE = 256;

volatile bool buttonPressed = false;
bool lastStateSent = false;  // Guarda el último estado enviado

bool ldrEnabled = false;
bool lcdEnabled = false;
bool tempEnabled = false;
bool buttonEnabled = false;

const unsigned long sendInterval = 2000;
unsigned long lastSendTime = 0;

void IRAM_ATTR buttonISR() {
  buttonPressed = digitalRead(BUTTON_PIN);
}

class Sensor {
public:
  static int readLDR() {
    int ldrValue = analogRead(LDR_PIN);
    ldrValue = map(ldrValue, 0, 4095, 0, 100);
    return ldrValue;
  }

  static float readTemperature() {
    float analogValue = thermocouple.readCelsius();
    return analogValue;
  }
};

class Actuator {
public:
  static void setFanSpeed(int speed) {
    speed = constrain(speed, 0, 255);
    ledcWrite(0, speed);
  }

  static void displayOnLCD(const String& line1, const String& line2) {
    if (displayMode == DisplayMode::LCD) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(line1);
      lcd.setCursor(0, 1);
      lcd.print(line2);
    }
  }
};

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(LDR_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT);

  ledcSetup(0, 25000, 8);
  ledcAttachPin(FAN_PWM_PIN, 0);

  lcd.init();
  lcd.noBacklight();
  lcd.off();

  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, CHANGE);
}

void processSerialCommands() {
  if (Serial.available() > 0) {
    char inputBuffer[BUFFER_SIZE];
    size_t len = Serial.readBytesUntil('\n', inputBuffer, BUFFER_SIZE);
    inputBuffer[len] = '\0';

    JsonDocument requestDoc;
    DeserializationError error = deserializeJson(requestDoc, inputBuffer);

    if (error) {
      Serial.println("{\"ERROR\": \"Invalid JSON\"}");
      return;
    }

    if (requestDoc["cmd"].is<const char*>()) {
      String cmd = requestDoc["cmd"].as<String>();

      if (cmd == "ID?") {
        JsonDocument responseDoc;
        responseDoc["id"] = "ESP32_31125";
        serializeJson(responseDoc, Serial);
        Serial.println();
      } 
      else if (cmd == "LCD") {
        if (requestDoc["line1"].is<const char*>() && requestDoc["line2"].is<const char*>()) {
            String line1 = requestDoc["line1"].as<String>();
            String line2 = requestDoc["line2"].as<String>();
            Actuator::displayOnLCD(line1, line2);
        }
      }
      else if (cmd == "SetTemp") {
        if (requestDoc["setpoint"].is<int>()) {
          SetTemp = requestDoc["setpoint"].as<int>();
        }
      }
      else if (cmd == "CONFIG") {
        displayMode = DisplayMode::NONE;  // Reinicia el estado antes de actualizar

        if (requestDoc["ldr"].is<const char*>()) {
          ldrEnabled = String(requestDoc["ldr"].as<const char*>()) == "true";
        }
        if (requestDoc["lcd"].is<const char*>()) {
          lcdEnabled = String(requestDoc["lcd"].as<const char*>()) == "true";
          if (lcdEnabled) {
            lcd.backlight();
            lcd.on();
          } else {
            lcd.clear();
            lcd.noBacklight();
            lcd.off();
          }
        }
        if (requestDoc["button"].is<const char*>()) {
          buttonEnabled = String(requestDoc["button"].as<const char*>()) == "true";
        }
        if (requestDoc["temp"].is<const char*>()) {
          tempEnabled = String(requestDoc["temp"].as<const char*>()) == "true";
        }
        
        if (requestDoc["show_temp"].is<const char*>() && 
            String(requestDoc["show_temp"].as<const char*>()) == "true") {
            displayMode = DisplayMode::TEMP;
        }
        if (requestDoc["show_ldr"].is<const char*>() && 
            String(requestDoc["show_ldr"].as<const char*>()) == "true") {
            displayMode = DisplayMode::LDR;
        }
        if (requestDoc["show_lcd"].is<const char*>() && 
            String(requestDoc["show_lcd"].as<const char*>()) == "true") {
            displayMode = DisplayMode::LCD;
        }
        if (requestDoc["show_button"].is<const char*>() && 
            String(requestDoc["show_button"].as<const char*>()) == "true") {
            displayMode = DisplayMode::BUTTON;
        }
        

        JsonDocument responseDoc;
        responseDoc["ldr"] = ldrEnabled ? "true" : "false";
        responseDoc["temp"] = tempEnabled ? "true" : "false";
        responseDoc["button"] = buttonEnabled ? "true" : "false";
        serializeJson(responseDoc, Serial);
        Serial.println();
      }
    }
  }
}

void sendSensorData() {
  if (millis() - lastSendTime >= sendInterval) {
    lastSendTime = millis();

    JsonDocument jsonDoc;
    bool sendData = false;

    if (ldrEnabled) {
      LDR = Sensor::readLDR();
      jsonDoc["LDR"] = LDR;
      sendData = true;
    }
    if (tempEnabled) {
      temp = Sensor::readTemperature();
      if (!isnan(temp)) {
        jsonDoc["TEMP"] = temp;
      } else {
        jsonDoc["TEMP"] = -1;
      }

      sendData = true;
    }

    if (sendData) {
      serializeJson(jsonDoc, Serial);
      Serial.println();
    }
  }
}

void sendInterruptData() {
  JsonDocument jsonDoc;
  bool sendInterrupt = false;

  if (buttonEnabled && buttonPressed != lastStateSent) {
    lastStateSent = buttonPressed;

    jsonDoc["BUTTON"] = buttonPressed;

    sendInterrupt = true;
  }

  if (sendInterrupt) {
    serializeJson(jsonDoc, Serial);
    Serial.println();
  }
}

void controlTemp() {
  if (tempEnabled) {
    if (isnan(temp)) {
      Actuator::setFanSpeed(0);
    }
    else {
      int speed = map(temp, MinTemp, SetTemp, 50, 255);
      Actuator::setFanSpeed(speed);
    }
  }
  else {
    Actuator::setFanSpeed(0);
  }
}

void showLCD() {
  if (!lcdEnabled) return;

  if (displayMode == DisplayMode::TEMP) {
    if (temp != lastTemp || SetTemp != lastSetTemp) {
      if (isnan(temp)) {
        
        lcd.setCursor(0, 0);
        lcd.print("Temp:      Set:");
        lcd.setCursor(0, 1);
        lcd.print("ERROR");
        lcd.setCursor(11, 1);
        lcd.print(SetTemp);
      } 
      else {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Temp:      Set:");
        lcd.setCursor(0, 1);
        lcd.print(temp);
        lcd.setCursor(11, 1);
        lcd.print(SetTemp);
      }

      lastTemp = temp; 
      lastSetTemp = SetTemp;
    }
  }
  else if (displayMode == DisplayMode::LDR) {
    if (LDR != lastLDR) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("LDR: ");
      lcd.setCursor(0, 1);
      lcd.print(LDR);
      
      lastLDR = LDR;
    }
  }
  else if (displayMode == DisplayMode::BUTTON) {
    if (buttonPressed != lastButtonState) { 
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(buttonPressed ? "Interrupt..." : "");
      lastButtonState = buttonPressed;
    }
  }
  else if (displayMode == DisplayMode::LCD) {
    //Funcion trabajando en Actuator::displayOnLCD(line1, line2);
  }
  else if (displayMode == DisplayMode::NONE) {
    lcd.clear();
  }
}

void loop() {
  processSerialCommands();
  sendSensorData();
  sendInterruptData();
  controlTemp();
  showLCD();
}