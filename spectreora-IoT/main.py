import network
import time
from machine import ADC
from umqtt.simple import MQTTClient
from machine import Pin

# Initialize the ADC on pin 26
adc = ADC(26)

ssid = 'SSID_NAME'
password = 'WIFI_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
 
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    while True:
    # Read the ECG data from the ADC
        ecg_data = adc.read_u16()

    # Print the ECG data to the console
        print(ecg_data)

    # Delay for 1 second
        time.sleep(1)



    # Read the ECG data from the ADC
    ecg_data = adc.read_u16()

    # Print the ECG data to the console
    print(ecg_data)

    # Delay for 1 second
    time.sleep(1)


