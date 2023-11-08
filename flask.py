from firebase_admin import credentials, db
from flask import Flask
from datetime import datetime
import pytz
import ast
import firebase_admin
import requests
import time
# Initialize the Flask app
app = Flask(__name__)
# Initialize Firebase credentials
cred = credentials.Certificate({
"type": "service_account",
  "project_id": "eonroots-cb89d",
  "private_key_id": "995009ef8f99e0c4d439303831c3e914ea64cf48",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDUA0LfzcG6mrR/\nw2lJ46bacaEUpyxp+gkSWihfo1bghPkQIF2vzsmimWDr++DCBHf8BvZ8Gbr1XmVx\nRExQxX9g4gCFYuVerkpiMIyDtnMgWvA6sprvlkJP4WDcXU0gDh8mnZnu2fUQTFQz\nFdQ61Ed3Xx7Odo/MDqSCaiiovNDgziIxWnvGyi4Zjq1Uxt6sD8Ba1vvsQ+gEs5Tw\nN1Gn+4o56Q+jF3wRES/WuIdbiBO4t4iNzRhbFZ7rczOdnijgGJIS4+rvaDycKK4W\n+GtYi9ALtzeU9+3v+6A13apF+A++++yKLrxZakUHnBBzgEMg4VKslzXXio8jUWc2\nnpy9J7x3AgMBAAECggEADj57DDrjmxKdmBkVzLz3e76qbvV9j0//f9TZ2I8XUHW7\nbA3YoLqyb/LngNAgsIUiiia6zoMS1tbOo8NnozEzSfWOyZqa3kROEBApKKI/h65E\nbJUnKEilA0vmBfgoxqoPbFJzW9ZKvjUUOFIG1IsCYC7eWX28UusUh2rz315Y/d/Z\nCFFyK6A0jx2Wz2k3deiwnuhcViHnN7IlLIp81CzhWeQcYaVNHzqPw2o8FuK1ACW8\nQkgKol/3hsICtCKR+0drvscOEjwBEJGTn59h6LupgAWDebNwBgeZSn8fgeIQd0oy\nn5efif+swVmknjqVuvhreTDWowyl+9dSuFeRNOJncQKBgQDtQiyAq7I6jIBGuQS7\nfcGDXF/yrZFtES9kCmhQ13/k65Ngz76fKxsl4CdJ/JThHZjodyE8xN5qGaznljji\ncb6YhcNIWIXoRj0IbEE8LZk/tNRjclP9jXDwQ4y3/st2OFKTmoTBD0CtGasmJT1t\n9XfLyO+8VVeovGNdr8keYhE18QKBgQDkwpHDTE4uI2lZW64EOyPjAPRZsGIt1VB5\n+cm8xLtxMLDd5520GtvM5612BynPaJ3L5Y9JU6H26Nw06k2uO54b0dCo1xQvbeyo\nxAwUZhiLmhQh3OxFRz5J/DYA8lS2y/qplX2Z0jMbpWeWoYq28F4ErqWAhuLGL9RP\n6IFpy1EQ5wKBgFwUkacCe/KDMwm/ptmJbgAoasiJmmZFBCqEa4XsjSNwVkt9dRLb\nLPcfLsBlOfbAgOa/zXODSHrPKi7bO4qO8JTLXUYHrTi/gdJyCUNswwxZhxBtf7Fp\nIors/IEwbxCbvVix4JH49HX5/1WXoGa7nNnHS1vBl3rSWpIythCHqPxRAoGBAOHC\nFyIa2wjzj5NNRBYO22K63WrqBGphG1PVLL+rk6SoPdQxMVS+MO8uMOTLOvrirt+7\nhEYEUFIhCrj6BoGNeoLP9NG7uML6A9Wl7JnxDAYxn+6vXUkdfx561jzm6q2f7peP\n3W2BoUiGWw2wDPpviwmp5dFKzOBz8V6PAbCLo0w/AoGBAMPhsa3NLZJ3CxwPvR+8\ngTy3qa8qYdb4z7GIySdyE3PJE+zVeiOtlvnUEnE4Byou8nsp+xt3j1ZjkznRxNeH\nPkotQLZtdiMtihE6nfZc01aCqYIzBFe6kkarhouFGBkg7xLyhn5VwXAQ8C1ouSBY\nQ/5SQyl/JkMGCaFxIjD7KGVo\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-aj9a8@eonroots-cb89d.iam.gserviceaccount.com",
  "client_id": "105575099011322676911",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-aj9a8%40eonroots-cb89d.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://eonroots-cb89d-default-rtdb.asia-southeast1.firebasedatabase.app'
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
        div=deviceid
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
                if relayid == 3:  # Handle relay3
                    last_updated_time_str = schedule.get("LastupdatedRelay3")
                    if last_updated_time_str:
                        last_updated_time = datetime.strptime(last_updated_time_str, '%a %b %d %H:%M:%S %Y')
                    else:
                        last_updated_time = datetime(1970, 1, 1)  # Provide a default value
                    current_time = datetime.now()
                    interval = int(schedule.get("interval", 0))
                    duration = int(schedule.get("Duration", 0))
                    # Calculate the time difference in seconds
                    if interval or duration != 0:
                        time_difference = (current_time - last_updated_time).total_seconds()

                        if time_difference % (interval * 3600) < duration * 60:
                            ref.update({"LastupdatedRelay3": current_time.strftime("%c")})
                            return "relay3_on"
                        else:
                            return "relay3_off"
                    else:
                        return "relay3_off"
            else:
                # If "Auto" is set to false, all relays work 24 hours
                return "relay" + str(relayid) + "_on"

        return "relay" + str(relayid) + "_off"
    # If the device doesn't have a schedule or "Auto" is not set, return "unknown"
    return "unknown"

def elapsedminutes(current_time):
    # Implement this function to calculate elapsed minutes since midnight
    # You can use the current_time to calculate the elapsed minutes
    return current_time.hour * 60 + current_time.minute

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
