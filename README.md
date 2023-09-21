## Device ID Configuration

Each device is assigned a unique device ID. To configure your Arduino code for your specific device, follow these steps:

1. Open the Arduino code from the `arduino` directory in this repository.

2. Locate the following line in the Arduino code:

   ```cpp
   String url = "/send/B293C63ZW2/" + String(arValue) + "/" + String(cnValue) + "/" + String(lgValue) + "/" + String(smValue) + "/" + String(raValue) + "/";
### Replace "B293C63ZW2" with your unique device ID. Your modified line should look like this:

   ```cpp
   String url = "/send/your-device-id/" + String(arValue) + "/" + String(cnValue) + "/" + String(lgValue) + "/" + String(smValue) + "/" + String(raValue) + "/";
