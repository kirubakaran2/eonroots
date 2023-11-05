#define TINY_GSM_MODEM_SIM800
#define TINY_GSM_RX_BUFFER 256
#include <SoftwareSerial.h>
#include <TinyGsmClient.h>
#include <ArduinoHttpClient.h>

SoftwareSerial gprsSerial(3, 2);
const char SERVER_HOST[] = "kirubakaran21.pythonanywhere.com";
const int SERVER_PORT = 80;
char apn[] = "bsnlnet";
char user[] = "";
char pass[] = "";

// Create the modem, client, and HTTP client instances
TinyGsm modem(gprsSerial);
TinyGsmClient gsm_client_modem(modem);
HttpClient http_client(gsm_client_modem, SERVER_HOST, SERVER_PORT);

// Define relay pins
const int relay1 = 5;
const int relay2 = 6;
const int relay3 = 7;
const int led = 4;

// Define the device ID
const char DEVICE_ID[] = "A98DB973KW";

unsigned long previousMillis = 0;
const unsigned long interval = 10000; // 10 seconds

// Define sensor pins
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;
const int sensor4Pin = A3;
const int sensor5Pin = A4;
const int sensor6Pin = A5;

int sensor1value = 0;
int sensor2value = 0;
int sensor3value = 0;
int sensor4value = 0;
int sensor5value = 0;
int sensor6value = 0;

void getRelayStatus(int relayPin, const char* relayName) {
  String url = "https://kirubakaran21.pythonanywhere.com/getrelaystatus/" + String(relayName) + "/" + DEVICE_ID;
  Serial.print("Requesting ");
  Serial.print(relayName);
  Serial.print(" status: ");
  Serial.println(url);
  while (true) {
    http_client.get(url);
    int httpCode = http_client.responseStatusCode();
    String response = http_client.responseBody();

    if (httpCode == 200) {
      Serial.print("HTTP Code (");
      Serial.print(relayName);
      Serial.print("): ");
      Serial.println(httpCode);
      Serial.print("Response (");
      Serial.print(relayName);
      Serial.print("): ");
      Serial.println(response);

      if (response.indexOf(relayName) != -1) {
        // Turn on the corresponding relay
        digitalWrite(relayPin, HIGH);
        break; // Exit the loop once relay status is received
      } else {
        // Turn off the corresponding relay
        digitalWrite(relayPin, LOW);
        break; // Exit the loop once relay status is received
      }
    } else {
      Serial.print("HTTP request for ");
      Serial.print(relayName);
      Serial.println(" failed.");
      delay(1000); // Delay for a while and then retry
    }
  }
}

void setup() {
  Serial.begin(9600);
  gprsSerial.begin(9600);
  pinMode(led, OUTPUT);
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);

  pinMode(sensor1Pin, INPUT_PULLUP);
  pinMode(sensor2Pin, INPUT_PULLUP);
  pinMode(sensor3Pin, INPUT_PULLUP);
  pinMode(sensor4Pin, INPUT_PULLUP);
  pinMode(sensor5Pin, INPUT_PULLUP);
  pinMode(sensor6Pin, INPUT_PULLUP);

  // Initialize the modem
  Serial.println("Initializing modem...");
  modem.restart();
  String modemInfo = modem.getModemInfo();
  Serial.print("Modem: ");
  Serial.println(modemInfo);

  http_client.setHttpResponseTimeout(10 * 1000); // 10 seconds timeout
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    Serial.print(F("Connecting to "));
    Serial.print(apn);

    if (!modem.gprsConnect(apn, user, pass)) {
      Serial.println(" failed");
      delay(1000);
      return;
    }

    Serial.println(" Status Ok");

    sensor1value = digitalRead(sensor1Pin);
    sensor2value = digitalRead(sensor2Pin);
    sensor3value = digitalRead(sensor3Pin);
    sensor4value = digitalRead(sensor4Pin);
    sensor5value = digitalRead(sensor5Pin);
    sensor6value = digitalRead(sensor6Pin);

    // Create the URL to send sensor data to the server
    String url = "/send/" + String(DEVICE_ID) + "/" + String(sensor1value) + "/" + String(sensor2value) + "/" + String(sensor3value) + "/" +
                 String(sensor4value) + "/" + String(sensor5value) + "/" + String(sensor6value);

    // Send sensor data to the server
    http_client.get(url);
    int httpCode = http_client.responseStatusCode();

    if (httpCode == 200) {
      Serial.println("Sensor data sent successfully.");
    } else {
      Serial.println("Failed to send sensor data to the server.");
    }

    // Get the status of relay 1
    getRelayStatus(relay1, "1");

    // Get the status of relay 2
    getRelayStatus(relay2, "2");

    // Get the status of relay 3
    getRelayStatus(relay3, "3");

    if (!http_client.connected()) {
      Serial.println();
      http_client.stop();
      Serial.println("HTTP GET disconnected");
    }
  }
}
