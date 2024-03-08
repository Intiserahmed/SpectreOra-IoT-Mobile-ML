#include "wokwi-api.h"
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>

// Internal state structure for simulated ECG
typedef struct {
  int index;
  int num_samples;
  float *ecg_samples;
} ecg_state_t;

// Custom map function for float values
float map_float(float value, float in_min, float in_max, float out_min, float out_max) {
  return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

// Generate a simple sinusoidal waveform
void generate_sinusoidal_waveform(float *buffer, int num_samples) {
  for (int i = 0; i < num_samples; i++) {
    buffer[i] = 0.5 + 0.5 * sin(2 * M_PI * i / num_samples);
  }
}

void ecg_tick(void *user_data) {
  ecg_state_t *state = (ecg_state_t *)user_data;

  // Output ECG signal to the OUT pin
  uint8_t pwm_value = (uint8_t)map_float(state->ecg_samples[state->index], 0, 1, 0, 255);
  pin_t out_pin = pin_init("OUT", OUTPUT);
  pin_write(out_pin, pwm_value);

  // Update index and loop back to the beginning when reaching the end of the sample data
  state->index = (state->index + 1) % state->num_samples;
}


void chip_init() {
  // Allocate memory for the simulated ECG internal state
  ecg_state_t *state = (ecg_state_t *)malloc(sizeof(ecg_state_t));

  // Initialize simulated ECG internal state
  int num_samples = 360;
  state->index = 0;
  state->num_samples = num_samples;
  state->ecg_samples = (float *)malloc(sizeof(float) * num_samples);
  generate_sinusoidal_waveform(state->ecg_samples, num_samples);

  // Set up the output pin
  pin_init("OUT", OUTPUT);

  // Set up a timer to update the ECG signal at a desired frequency
  timer_config_t timer_config = {
    .callback = ecg_tick,
    .user_data = state,
  };

  // Create a timer identifier from the timer configuration
  timer_t timer = timer_init(&timer_config);

  // Start the timer with an interval of one millisecond and repeat flag set to true
  timer_start(timer, 1000, true);
}
