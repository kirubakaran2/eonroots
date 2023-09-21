#define TINY_GSM_MODEM_SIM800
#define TINY_GSM_RX_BUFFER 256
#include <SoftwareSerial.h>
#include <TinyGsmClient.h>
#include <ArduinoHttpClient.h>

SoftwareSerial gprsSerial(10, 11);
const char SERVER_HOST[] = "kirubakaran21.pythonanywhere.com";
const int SERVER_PORT = 80; // Change to appropriate port if needed
char apn[] = "airtelgprs.com";
char user[] = "";
char pass[] = "";
TinyGsm modem(gprsSerial);
TinyGsmClient gsm_client_modem(modem);
HttpClient http_client = HttpClient(gsm_client_modem, SERVER_HOST, SERVER_PORT);
const int in1 = 2;  // the number of the pushbutton pin
const int in2 = 3;
const int in3 = 4;
const int in4 = 5;
const int clear = 6;
const int led = 7;

unsigned long previousMillis = 0; // Store the previous time
const unsigned long interval = 10000; // Interval in milliseconds (10 seconds)

void setup() {
  Serial.begin(9600);
  gprsSerial.begin(9600);
  pinMode(led, OUTPUT);
  pinMode(in1, INPUT);
  pinMode(in2, INPUT);
  pinMode(in3, INPUT);
  pinMode(in4, INPUT);
  pinMode(clear, INPUT);
  delay(1000);

  Serial.println("Initializing modem...");
  modem.restart();
  String modemInfo = modem.getModemInfo();
  Serial.print("Modem: ");
  Serial.println(modemInfo);

  http_client.setHttpResponseTimeout(10 * 1000); // 10 secs timeout
}
void loop() {
  unsigned long currentMillis = millis(); // Get the current time

  // Check if the desired interval has elapsed
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis; // Save the current time

    Serial.print(F("Connecting to "));
    Serial.print(apn);
    if (!modem.gprsConnect(apn, user, pass)) {
      Serial.println(" failed");
      delay(1000);
      return;
    }
    Serial.println(" Status Ok");

    // Read button states
    int arValue = digitalRead(in1);
    int cnValue = digitalRead(in2);
    int lgValue = digitalRead(in3);
    int smValue = digitalRead(in4);
    int raValue = digitalRead(clear);

    String url = "/send/B293C63ZW2/" + String(arValue) + "/" + String(cnValue) + "/" + String(lgValue) + "/" + String(smValue) + "/" + String(raValue) + "/";

    http_client.beginRequest();
    int httpCode = http_client.get(url);
    http_client.endRequest();

    if (httpCode == HTTP_SUCCESS) {
      String response = http_client.responseBody();
      Serial.println("Response: " + response);
      
      if (response.indexOf("Data pushing is not allowed at this time for device: B293C63ZW2") != -1) {
        // Turn off the buttons
        digitalWrite(in1, HIGH);
        digitalWrite(in2, HIGH);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, HIGH);
        digitalWrite(clear, HIGH);
      } else if (response.indexOf("Data added to device: B293C63ZW2") != -1) {
        // Turn on the buttons
        digitalWrite(in1, LOW);
        digitalWrite(in2, LOW);
        digitalWrite(in3, LOW);
        digitalWrite(in4, LOW);
        digitalWrite(clear, LOW);
      }
    } else {
      Serial.println("HTTP request failed.");
    }

    if (!http_client.connected()) {
      Serial.println();
      http_client.stop(); // Shutdown
      Serial.println("HTTP GET disconnected");
    }
  }
}
