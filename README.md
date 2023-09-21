**"Device ID Configuration"**
Each device is assigned a unique device ID. Modify the Arduino code to include the specific device ID for your device. Replace the "B293C63ZW2" with your unique device ID in the Arduino code
String url = "/send/your-device-id/" + String(arValue) + "/" + String(cnValue) + "/" + String(lgValue) + "/" + String(smValue) + "/" + String(raValue) + "/";
