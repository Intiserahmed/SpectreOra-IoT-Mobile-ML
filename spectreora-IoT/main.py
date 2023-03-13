import time
from machine import ADC

# Initialize the ADC on pin 26
adc = ADC(26)

# Initialize the counter to 0
counter = 0

while True:
    # Read the ECG data from the ADC
    ecg_data = adc.read_u16()

    # Print the ECG data to the console
    print(ecg_data)

    # Increment the counter by 1
    counter += 1

    # Check if 1 second has passed
    if counter == 250:
        print("1 second has passed")
        counter = 0

    # Delay for 4 milliseconds (corresponding to the sampling rate of 250 Hz)
    time.sleep(0.004)
