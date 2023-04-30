import gc
import ujson
import urequests
import network
import utime
from machine import ADC, Pin
from urandom import getrandbits
import config
import usocket as socket
import ussl as ssl

ecg_data_array = [None] * 1000
counter = 0


def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Intiser", "12121212")

    print("Connecting to Wi-Fi", end="")
    while not wlan.isconnected():
        print(".", end="")
        utime.sleep(0.1)
    print(" Connected!")
    print("IP address:", wlan.ifconfig()[0])
    return wlan


def send_data(wlan, url, payload, headers):
    if wlan.isconnected():
        retries = 3
        while retries > 0:
            try:
                response = urequests.post(url, data=payload, headers=headers)
                response.close()
                return response.status_code
            except OSError as e:
                print("Error:", e)
                print("Retrying...")
                retries -= 1
                utime.sleep(1)
        print("Failed to send data after 3 retries.")
    else:
        print("Wi-Fi not connected. Unable to send data.")



def read_adc(adc):
    global counter
    ecg_data = int((getrandbits(8) % 251) + 300)  # limit between 300 and 550
    counter += 1

    if counter < 1000:
        print(ecg_data)
        ecg_data_array[counter] = ecg_data
    else:
        counter = 0
        return True
    gc.collect()

    return False


wlan = wifi_connect()
adc = ADC(Pin(26))
url = config.SUPABASE_URL
headers = {
    "apikey": config.API_KEY,
    "Content-Type": config.TYPE
}

sampling_interval = 4  # 4 milliseconds
next_sample = utime.ticks_ms()
send_data_interval = 1000  # 15 seconds
last_send_time = utime.ticks_ms()


while True:
    now = utime.ticks_ms()
    if utime.ticks_diff(next_sample, now) <= 0:
        if read_adc(adc):
            if utime.ticks_diff(now, last_send_time) >= send_data_interval:
                payload = ujson.dumps(
                    {"values" : ecg_data_array,
                        "user_id": config.USER_ID})
                gc.collect()
                # Send compressed payload
                send_data(wlan, url, payload, headers)
                gc.collect()
                last_send_time = utime.ticks_ms()

        next_sample = utime.ticks_add(next_sample, sampling_interval)