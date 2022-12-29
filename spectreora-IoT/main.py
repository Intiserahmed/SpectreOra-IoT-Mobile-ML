import time
from machine import ADC

# Initialize the ADC on pin 26
adc = ADC(26)

while True:
    # Read the ECG data from the ADC
    ecg_data = adc.read_u16()

    # Print the ECG data to the console
    print(ecg_data)

    # Delay for 1 second
    time.sleep(1)


