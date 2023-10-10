from firebase_admin import credentials, db
from flask import Flask
from datetime import datetime
import pytz
import ast
import firebase_admin
import requests
# Initialize the Flask app
app = Flask(__name__)
# Initialize Firebase credentials
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "smartdevice-e2e79",
  "private_key_id": "eb71476ad6ac291ac9e87de263477c9cf1b9becd",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDtrC3yTitNIt4G\nEClV4X1gCsL8QrD2o/UXyHdiv5jJCXmYLoiUJIroJ+sQSyL+Fzko6JUMqsAX3Xyl\nvH7FfxmLdw+DiXrDziVTFvruMzNoReUQtWimCx7sIYfC8ht6yQGyBhB8aGeMNBYB\nWOnHkGHMsIl9R0RCr9KYMMsZ0XFTDid6DGAqBceMdFNQkLgd8ZwP5YPp4Zx2La8l\nBR54IlKXyYGnytc9ox9Ba0Ju6Y+57/py/sYQn4EBrXzff4lB/z595/BLyHky4rpH\n8siuj/j777DDumasgFsELUYQWA/A0VLgW2lYSLo5uxRXLAniOKmKZCKqixQNq0Xv\nxqQzpqWBAgMBAAECggEAHfGFGWO1S2LS75ceKhJ+YfkBH1iEpJI8CPrJ5cBHTr65\nmc11Chr/gCe1UwhwWGxTGH8S9jVV/bu7HkNdAmNUs9A0fWk29Q/V/n2k8Bk1xxOV\nPDFqxY6dnvjLeqlXgnTsGIJwlcfukcinJBTQYULku23baJPvuuodYWy2TeKoASNH\ncUkRUXaMlSecI+yAecTvDMAiGBhr0vjzt6+3kBJSPAB+pYTVcJWc8lhP5j4owkph\nTsH9opDacibEAFgW5cJwz7aSVm+JLu8ZK8dzV2rvjr8LXvWZ/M0oFX4r5eyZaZRz\nN1I5lcWF48N1a1+/AVvd/CICuK4oBDgMGnyLTl8RRQKBgQD+fnitf3lanU5066tW\nhZjhZKXs9wn37RHUo+0ItOOG3GBldoNnKKrn0S6VreHzDCXCaBPiFDXa2FeBluak\nBtNCz3PcODg+ODkD5PgvrtfYQuPmgsrTuaFIJ2UKZDaVEODdIUO2cjaSPxjEAXaI\nH5l46PcrTTGlB3fy8ehJ5rsD9QKBgQDvFDm926geiCi4Q8dBW2jBr5NequUZ8mKf\nyM2CqpOjnALP/1ihn2G5sv+Ei/KNR1phjdGh85OfI4IU1AgIay4iwicnUo/E9bV7\nuqY6v3vi0NrMcneSMS3YY+bIufOI9aCNEbr1TbuJ9BjBNqUKDAO0fpt0drEh/w9D\nYTA0Vmlv3QKBgQCc28Lx3SIlMdQLyL5Ag/Oo6OpEVje0slBNKgSNW0Dp/KcForh3\nOt+sJoh6BUTBE3mqi4/FxwMysimtXB8odnR8N3WIBLbV0r2Bov0+Fpw/VWs2xuLR\nARdha7ahYwcpdc/DPB+KMndkSLOxC93NJPzpQ14lOF0jBKlv+p5b/nTCiQKBgFZJ\nQXHBZlLmp3Ohmrd+6zcETDbdjOQpc+jhSzK+p5xkASvap71lTZr8/HV1IOxWdUtC\nKQe/ZmcIJLmpsOCA9ly7H/B0PslCOObX/Yi0dVzuLhmdsoQD1d0EaVXGrxueMvzX\nClfgXzAx9gE93KDcpzWsgCSvdcykRnj2CbTJ/zHNAoGASCPC0+73PaTW0V1vLeKu\nqW/8/YNO5f0ISCGpV/o7UPkeA88RDaSKwaYr5MHSrtGP7Hsor4k1O7YyFhr8sUx5\nu+hjzh3e7dCht1qsoDYBNf7bNSCZOnwNowzB0Xqe4dY8YloRXsIvML8o6QmMhM70\ne5D1mfEA2E1UHcfZ8tEZtEU=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-yz8ep@smartdevice-e2e79.iam.gserviceaccount.com",
  "client_id": "101542286294359985933",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-yz8ep%40smartdevice-e2e79.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://smartdevice-e2e79-default-rtdb.asia-southeast1.firebasedatabase.app'
})
# Initialize the Flask app

server_timezone = pytz.timezone('Asia/Kolkata')
# Function to get the formatted time
def get_formatted_time():
    current_time = datetime.now(server_timezone)
    formatted_time = current_time.strftime('%H:%M')
    return formatted_time
# Function to fetch data from Firebase
def fetch(key):
    ref = db.reference('/devices')
    try:
        data = ref.child(key).get()
        if data:
            return f'{data}'
        else:
            return f'No data found for key {key}'
    except Exception as e:
        return f'Error: {e}'
# Function to update log count in Firebase
def updateLogCount(key):
    ref = db.reference('/devices/' + key)
    try:
        data = ref.child('TotalLogs').get()
        data = data + 1
        ref.child("TotalLogs").set(data)
    except Exception as e:
        print(e)
# Function to calculate elapsed minutes
def elapsed_minutes(start_time_str):
    if start_time_str is not None:
        current_time = datetime.now()
        start_time = datetime.strptime(start_time_str, '%H:%M')
        elapsed_time = current_time - start_time
        elapsed_minutes = elapsed_time.total_seconds() / 60
        return elapsed_minutes
    return 0
# Function to send a WhatsApp message
def sendWhatsapp(key):
    currenttime = get_formatted_time()
    msgString = "Log Updated for device " + key + " at " + currenttime
    url = "https://iot-msg.praveenkumard1.repl.co/send_message?message=" + msgString
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        return "error"
# Function to send a notification
def sendNotification(key):
    ref = db.reference('/devices/' + key)
    ownerid = ref.child('OwnerId').get()
    try:
        ref = db.reference('/users/' + ownerid + "/Notifications/")
        currenttime = get_formatted_time()
        ref.push("Log Updated for device " + key + " at " + currenttime)
    except Exception as e:
        print(e)
# Function to write old data to Firebase
def writeOld(key):
    ref = db.reference('/devices')
    try:
        data = fetch(key)
        if data is None:
            data = {}
        data_dict = ast.literal_eval(data)
        olderData = {
            "Sensor1": data_dict["sensor1value"],
            "Sensor2": data_dict["sensor2value"],
            "Sensor3": data_dict["sensor3value"],
            "Sensor4": data_dict["sensor4value"],
            "Sensor5": data_dict["sensor5value"],
            "Sensor6": data_dict["sensor6value"],
            "CurrentDate": data_dict["CurrentDate"],
            "CurrentTime": data_dict["CurrentTIme"]
        }
        ref.child(key + "/PreviousLogs/").push(olderData)
        return f'Successfully updated data in Firebase for key {key}: {olderData}'
    except Exception as e:
        return f'Error updating data: {e}'
# Function to handle the relay control
# Define a dictionary to keep track of relay states
relay_states = {
    'relay1': False,
    'relay2': False,
    'relay3': False
}

# Function to get the current time in minutes
def get_current_minutes():
    now = datetime.now()
    return now.hour * 60 + now.minute

# Function to update relay states based on schedule
@app.route('/getrelaystatus/<int:relayid>/<string:deviceid>', methods=['GET'])
def get_relay_status(relayid, deviceid):
    ref = db.reference("/devices/" + deviceid)
    schedule = ref.get()
    current_time1 = get_formatted_time()

    if schedule:
        current_time1 = datetime.strptime(current_time1, '%H:%M').time()
        turned_on = schedule.get('TurnedOn', False)
        auto_mode = schedule.get('auto', False)
        if turned_on:
            if auto_mode:
                if relayid == 1:
                    start_time1 = datetime.strptime(schedule.get('StartTime', '00:00'), '%H:%M').time()
                    end_time1 = datetime.strptime(schedule.get('EndTime', '23:59'), '%H:%M').time()
                    if start_time1 <= current_time1 <= end_time1:
                        return "relay1_on"
                    else:
                        return "relay1_off"

                if relayid == 2:
                    start_time2 = datetime.strptime(schedule.get('SecondaryStartTime', '00:00'), '%H:%M').time()
                    end_time2 = datetime.strptime(schedule.get('SecondaryEndTime', '23:59'), '%H:%M').time()
                    if start_time2 <= current_time1 <= end_time2:
                        return "relay2_on"
                    else:
                        return "relay2_off"

                if relayid == 3:
                    interval_hours = schedule.get('interval', 0)
                    duration_minutes = schedule.get('Duration', 0)
                    # Convert interval hours to minutes
                    interval_minutes = interval_hours * 60
                    if interval_minutes == 0 or duration_minutes == 0:
                        return "relay3_off"
                    current_minutes = elapsed_minutes(current_time)
                    time_in_current_interval = current_minutes % interval_minutes

                    if time_in_current_interval < duration_minutes:
                        return "relay3_on"
                    else:
                        return "relay3_off"



            else:
                # If "Auto" is set to false, all relays work 24 hours
                return "relay" + str(relayid) + "_on"

        return "relay" + str(relayid) + "_off"
    # If the device doesn't have a schedule or "Auto" is not set, return "unknown"
    return "unknown"

# Function to send a signal to Arduino
def send_signal_to_arduino(command):
    pass
@app.route('/current_date')
def current_date():
  current_time = datetime.now(server_timezone)
  formatted_time = current_time.strftime('%Y-%m-%d ')
  return f'{formatted_time}'
@app.route('/current_time')
def current_time():
    formatted_time = get_formatted_time()
    return f'{formatted_time}'
# Function to send a heartbeat notification
def send_heartbeat_notification(device_id):
    ref = db.reference('/devices/' + device_id)

    try:
        last_heartbeat_time = ref.child('heartBeat').get()
        current_time = get_formatted_time()

        # Retrieve the configured interval for inactivity from Firebase
        inactivity_interval = ref.child('InactivityInterval').get()

        if last_heartbeat_time is not None and elapsed_minutes(last_heartbeat_time) > inactivity_interval:
            # Device is inactive for the configured interval, send a notification
            ref = db.reference('/users/' + owner_id + "/Notifications/")
            ref.push("Device inactive for device " + device_id + " at " + current_time)
        else:
            # Device is active, send a different notification or take other actions as needed
            # For example, send an "Device is active" notification
            ref.push("Device active for device " + device_id + " at " + current_time)
            # You can add more actions or customize this part based on your requirements.
    except Exception as e:
        print(e)
# Function to send a sensor alert notification
def send_sensor_alert_notification(owner_id, sensor, device_id):

    ref = db.reference('/users/' + owner_id + "/Notifications/")
    current_time = get_formatted_time()
    alert_message = f"Sensor {sensor} on device {device_id} detected an issue at {current_time}."
    ref.push(alert_message)
@app.route('/send/<div>/<sensor1value>/<sensor2value>/<sensor3value>/<sensor4value>/<sensor5value>/<sensor6value>', methods=['GET', 'POST'])
def handle_request(div, sensor1value, sensor2value, sensor3value, sensor4value, sensor5value, sensor6value):


    # Update data for the device
    current_time = get_formatted_time()
    CurrentDate = current_date()
    data_set = {
        'sensor1value': sensor1value,  # Correct the capitalization
        'sensor2value': sensor2value,  # Correct the capitalization
        'sensor3value': sensor3value,  # Correct the capitalization
        'sensor4value': sensor4value,  # Correct the capitalization
        'sensor5value': sensor5value,  # Correct the capitalization
        'sensor6value': sensor6value,  # Correct the capitalization
        'CurrentTime': current_time,
        'CurrentDate': CurrentDate
    }
    ref = db.reference('/devices/' + div)
    ref.update(data_set)
    updateLogCount(div)
    # Check sensor values for alerts
    owner_id = ref.child('OwnerId').get()
    error_messages = []


    sensor1 = ref.child('params/0/field').get()
    sensor2 = ref.child('params/1/field').get()
    sensor3 = ref.child('params/2/field').get()
    sensor4 = ref.child('params/3/field').get()
    sensor5 = ref.child('params/4/field').get()
    sensor6 = ref.child('params/5/field').get()

    if sensor1value == '1':
        if(sensor1!=None):
            error_messages.append('Sensor 1 detected an issue!')
            send_sensor_alert_notification(owner_id, sensor1, div)
        else:
            error_messages.append('Sensor 1 detected an issue!')
            send_sensor_alert_notification(owner_id, '1', div)
    if sensor2value == '1':
       if(sensor2!=None):
            error_messages.append('Sensor 2 detected an issue!')
            send_sensor_alert_notification(owner_id, sensor2, div)
       else:
            error_messages.append('Sensor 2 detected an issue!')
            send_sensor_alert_notification(owner_id, '2', div)
    if sensor3value == '1':
        if(sensor3!=None):
            error_messages.append('Sensor 3 detected an issue!')
            send_sensor_alert_notification(owner_id, sensor3, div)
        else:
            error_messages.append('Sensor 3 detected an issue!')
            send_sensor_alert_notification(owner_id, '3', div)
    if sensor4value == '1':
        if(sensor4!=None):
            error_messages.append('Sensor 4 detected an issue!')
            send_sensor_alert_notification(owner_id, sensor4, div)
        else:
            error_messages.append('Sensor 4 detected an issue!')
            send_sensor_alert_notification(owner_id, '4', div)
    if sensor5value == '1':
        if(sensor5!=None):
            error_messages.append('Sensor 5 detected an issue!')
            send_sensor_alert_notification(owner_id, sensor5, div)
        else:
            error_messages.append('Sensor 5 detected an issue!')
            send_sensor_alert_notification(owner_id, '5', div)
    if sensor6value == '1':
        if(sensor6!=None):
            error_messages.append('Sensor 6 detected an issue!')
            send_sensor_alert_notification(owner_id, sensor6, div)
        else:
            error_messages.append('Sensor 6 detected an issue!')
            send_sensor_alert_notification(owner_id, '6', div)
    sendNotification(div)
    # Pass an appropriate message here
    return "Data added to device: " + div

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=80)