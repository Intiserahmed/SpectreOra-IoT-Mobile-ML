import gc
from network import WLAN, STA_IF
from utime import sleep, sleep_ms, time, ticks_ms, ticks_diff
import config
import ujson
from machine import ADC, Pin
import urequests


ecg_data_array = [None] * 3000
counter = 0


def wifi_connect():
    ssid = config.SSID
    password = config.PASSWORD

    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 20
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    if not wlan.isconnected():
        raise RuntimeError('Wi-Fi connection failed')

    print('Wi-Fi connected')
    print('IP address:', wlan.ifconfig()[0])

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
                sleep(1)
        print("Failed to send data after 3 retries.")
    else:
        print("Wi-Fi not connected. Unable to send data.")


def read_adc(adc):
    global counter
    ecg_data = adc.read_u16()
    counter += 1

    if counter < 3000:
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
next_sample = ticks_ms()
send_data_interval = 15005  # 15 seconds
last_send_time = ticks_ms()

while True:
    now = ticks_ms()
    if ticks_diff(next_sample, now) <= 0:
        if read_adc(adc):
            if ticks_diff(now, last_send_time) >= send_data_interval:
                payload = ujson.dumps(
                    {"values": ecg_data_array, "user_id": config.USER_ID})
                gc.collect()
                # Send compressed payload
                send_data(wlan, url, payload, headers)
                gc.collect()
                last_send_time = ticks_ms()

        next_sample = ticks_ms() + sampling_interval
