import utime
from machine import Pin, ADC
import network
import ufirestore as firebase
import config
import ntptime


# Set the NTP server address
ntp_server = '0.pool.ntp.org'

# Initialize the ADC on pin 26
adc = ADC(26)

# Set up the Wi-Fi connection
ssid = config.SSID
password = config.PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection or fail
max_wait = 20
while max_wait > 0:
    if wlan.isconnected():
        break
    max_wait -= 1
    print('Waiting for Wi-Fi connection...')
    utime.sleep(1)

if not wlan.isconnected():
    raise RuntimeError('Wi-Fi connection failed')

print('Wi-Fi connected')
print('IP address:', wlan.ifconfig()[0])

# Synchronize the time with an NTP server
ntptime.host = ntp_server
ntptime.settime()


def get_current_timestamp():
    # Get the current time tuple
    current_time_tuple = utime.localtime()

    # Convert the time tuple to a timestamp in seconds since the epoch
    timestamp = utime.mktime(current_time_tuple)

    # Add the timezone offset to the timestamp if necessary
    timezone_offset = 8 * 3600  # 8 hours ahead of UTC
    timestamp += timezone_offset

    return timestamp


# Initialize counter
counter = 0


# Firebase URl Setup
firebase.setURL(config.FIREBASE_URL)


# Initialize the ECG data dictionary
ecg_data_array = []


def format_timestamp(timestamp):

    t = utime.localtime(get_current_timestamp())
    formatted_time = "{:02}:{:02}:{:02} {:02}-{:02}-{:04}".format(
        t[3], t[4], t[5], t[2], t[1], t[0])
    return formatted_time


# Format the timestamp
session_time = "Session of " + format_timestamp(get_current_timestamp())

try:
    firebase.put(session_time, get_current_timestamp(), bg=0)
except Exception as e:
    print(e)

led = machine.Pin("LED", machine.Pin.OUT)  # Set onboard LED pin

while True:
    if wlan.isconnected():
        led.high()
    else:
        led.toggle()

    # Read the ECG data from the ADC
    ecg_data = adc.read_u16()

    # Corresponding to the sampling rate of 250 Hz
    if counter < 1800:
        formatted_time = format_timestamp(get_current_timestamp())
        formatted_time = formatted_time[:8] + formatted_time[-5:]

        ecg_reading_json = {
            # Each value will be stored and referenced as key
            formatted_time: ecg_data,
        }

    ecg_data_array.append(ecg_reading_json)

    # If 1 second have elapsed, store the ECG data to Firebase Realtime Database
    if counter == 250:
        # Get the current timestamp in seconds
        formatted_time = format_timestamp(get_current_timestamp())

        # Store the ECG data to Firebase Realtime Database with the timestamp
        ecg_data_json = {
            "timestamp": formatted_time,
            'ecg_data': ecg_data_array}

        try:
            print("addTo")
            firebase.addto(session_time,
                           ecg_data_json, bg=0)

        except Exception as e:
            print(e)

        # Clear the ECG data array
        ecg_data_array.clear()

    # Increment the counter
    counter += 1

    # If the counter has reached 250, reset it to 0
    if counter > 250:
        counter = 0

    # Delay for 4 milliseconds
    utime.sleep(0.004)
