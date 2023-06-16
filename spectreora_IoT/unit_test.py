import unittest

Define a test class that inherits from unittest.TestCase
class TestEcgData(unittest.TestCase):

# Define a setUp method that runs before each test case
def setUp(self):
    # Create an instance of the WLAN class and connect to Wi-Fi
    self.wlan = wifi_connect()
    # Create an instance of the ADC class and pass the pin number
    self.adc = ADC(Pin(26))
    # Set the url, headers, sampling interval, and send data interval
    self.url, self.headers = config.SUPABASE_URL, {
        "apikey": config.API_KEY,
        "Content-Type": config.TYPE
    }
    self.sampling_interval, self.send_data_interval = 8, 15 * 1000
    # Set the next sample and last send time to the current time
    self.next_sample, self.last_send_time = ticks_ms(), ticks_ms()

# Define a tearDown method that runs after each test case
def tearDown(self):
    # Disconnect from Wi-Fi and close the WLAN instance
    self.wlan.disconnect()
    self.wlan.active(False)
    self.wlan.close()
    # Close the ADC instance
    self.adc.close()

# Define a test case for reading adc values and sending data
def test_read_adc_and_send_data(self):
    # Use a loop to simulate 20 seconds of data collection and transmission
    for _ in range(20):
        # Get the current time
        now = ticks_ms()
        # Check if it is time to read adc values
        if ticks_diff(self.next_sample, now) <= 0:
            # Call the read_adc function and store the return value
            is_full = read_adc(self.adc)
            # Check if it is time to send data
            if is_full and ticks_diff(now, self.last_send_time) >= self.send_data_interval:
                # Prepare the payload as a JSON string
                payload = ujson.dumps(
                    {"values": ecg_data_array, "user_id": config.USER_ID})
                gc.collect()
                # Call the send_data function and store the return value
                status_code = send_data(self.wlan, self.url, payload, self.headers)
                gc.collect()
                # Assert that the status code is 200 (OK)
                self.assertEqual(status_code, 200)
                # Update the last send time
                self.last_send_time = ticks_ms()
            # Update the next sample time
            self.next_sample = ticks_ms() + self.sampling_interval
Copy
Run the test script if it is executed as the main module
if name == ‘main’: unittest.main()
