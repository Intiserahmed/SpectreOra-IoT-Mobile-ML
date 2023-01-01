import network
import time
from machine import ADC
from umqtt.simple import MQTTClient
from machine import Pin

# Initialize the ADC on pin 26
adc = ADC(26)

ssid = 'SSID_NAME'
password = 'WIFI_PASSWORD'

# The Azure IoT Hub MQTT Module with 20days SAS
hostname = 'spectreoraiot.azure-devices.net'
clientid = 'spectreX'
user_name = 'spectreoraiot.azure-devices.net/spectreX/?api-version=2021-04-12'
passw = 'SharedAccessSignature sr=spectreoraiot.azure-devices.net%2Fdevices%2FspectreX&sig=0tQuLA%2F%2Fc7nQ73X4fxPnAWJ28FboMA8p4PMZL02Yigo%3D&se=1674296392'
topic_pub = b'devices/spectreX/messages/events/'
port_no = 0
subscribe_topic = "devices/spectreX/messages/devicebound/#"

#MQTT Connect Function
def mqtt_connect():

    certificate_path = "baltimore.cer"
    print('Loading Blatimore Certificate')
    with open(certificate_path, 'r') as f:
        cert = f.read()
    print('Obtained Baltimore Certificate')
    sslparams = {'cert':cert}
    
    client = MQTTClient(client_id=clientid, server=hostname, port=port_no, user=user_name, password=passw, keepalive=3600, ssl=True, ssl_params=sslparams)
    client.connect()
    print('Connected to IoT Hub MQTT Broker')
    return client


#MQTT Reconnect Function
def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()
    
    
# Connecting to Wifi Module
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

# Handle connection error / Error Handling 
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    try:
        client = mqtt_connect()
    except OSError as e:
        reconnect()
# Reads and prints the ECG data from the ADC every second indefinitely.
    while True:
    # Read the ECG data from the ADC
        ecg_data = adc.read_u16()
        
    # Sending the data to Azure IoT hub 
        client.publish(topic_pub, b'{"readings":"{ecg_data}"}')

    # Print the ECG data to the console
        print(ecg_data)

    # Delay for 1 second
        time.sleep(1)


