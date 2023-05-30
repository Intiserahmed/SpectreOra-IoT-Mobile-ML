import gc
from network import WLAN, STA_IF
from utime import sleep, ticks_ms, ticks_diff
import config
import ujson
from machine import ADC, Pin
import urequests

ecg_data_array = [0] * 3000
counter = 0


def wifi_connect():
    ssid, password = config.ssid, config.password
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(20):
        if wlan.isconnected():
            break
        print('Waiting for Wi-Fi connection...')
        sleep(1)

    if not wlan.isconnected():
        raise RuntimeError('Wi-Fi connection failed')

    print(f'Wi-Fi connected\nIP address: {wlan.ifconfig()[0]}')
    return wlan


def send_data(wlan, url, payload, headers):
    if not wlan.isconnected():
        print("Wi-Fi not connected. Unable to send data.")
        return

    for _ in range(3):
        try:
            with urequests.post(url, data=payload, headers=headers) as response:
                return response.status_code
        except OSError as e:
            print(f"Error: {e}\nRetrying...")
            sleep(1)

    print("Failed to send data after 3 retries.")


def read_adc(adc):
    global counter
    ecg_data = adc.read_u16()
    ecg_data_array[counter] = ecg_data
    counter = (counter + 1) % 3000
    gc.collect()
    return counter == 0


wlan = wifi_connect()
adc = ADC(Pin(26))
url, headers = config.SUPABASE_URL, {
    "apikey": config.API_KEY,
    "Content-Type": config.TYPE
}
sampling_interval, send_data_interval = 4, 15005
next_sample, last_send_time = ticks_ms(), ticks_ms()

while True:
    now = ticks_ms()
    if ticks_diff(next_sample, now) <= 0:
        if read_adc(adc) and ticks_diff(now, last_send_time) >= send_data_interval:
            payload = ujson.dumps(
                {"values": ecg_data_array, "user_id": config.USER_ID})
            gc.collect()
            send_data(wlan, url, payload, headers)
            gc.collect()
            last_send_time = ticks_ms()
        next_sample = ticks_ms() + sampling_interval
