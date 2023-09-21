## Device ID Configuration

Each device is assigned a unique device ID. To configure your Arduino code for your specific device, follow these steps:

1. Open the Arduino code from the `arduino` directory in this repository.

2. Locate the following line in the Arduino code:

   ```cpp
   String url = "/send/B293C63ZW2/" + String(arValue) + "/" + String(cnValue) + "/" + String(lgValue) + "/" + String(smValue) + "/" + String(raValue) + "/";
### Replace "B293C63ZW2" with your unique device ID. Your modified line should look like this:
    String url = "/send/your-device-id/" + String(arValue) + "/" + String(cnValue) + "/" + String(lgValue) + "/" + String(smValue) + "/" + String(raValue) + "/";
### Also in this line:

      if (response.indexOf("Data pushing is not allowed at this time for device: your-device-id") != -1) {
      // Turn off the buttons
      digitalWrite(in1, HIGH);
      digitalWrite(in2, HIGH);
      digitalWrite(in3, HIGH);
      digitalWrite(in4, HIGH);
      digitalWrite(clear, HIGH);
      } else if (response.indexOf("Data added to device: your-device-id") != -1) {
      // Turn on the buttons
     digitalWrite(in1, LOW);
     digitalWrite(in2, LOW);
     digitalWrite(in3, LOW);
     digitalWrite(in4, LOW);
    digitalWrite(clear, LOW);
    }
## Replace "your-device-id" in the above code with the specific device ID.

### Please make sure to replace "your-device-id" with your actual device ID throughout the code.
