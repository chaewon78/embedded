import RPi.GPIO as GPIO
import time

SW_PINS = [5, 6, 13, 19]
SW_NAMES = ["SW1", "SW2", "SW3", "SW4"]

NUM_SWITCHES = len(SW_PINS)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for pin in SW_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

click_counts = [0] * NUM_SWITCHES
old_values = [0] * NUM_SWITCHES

try:
    while True:
        new_values = [GPIO.input(pin) for pin in SW_PINS]

        for i in range(NUM_SWITCHES):

            if new_values[i] == 1 and old_values[i] == 0:
                click_counts[i] += 1

                switch_name = SW_NAMES[i]
                count = click_counts[i]

                output_tuple = (f"{switch_name} click", count)

                print(output_tuple)

        old_values = new_values.copy()

        time.sleep(0.1)

except KeyboardInterrupt:
    pass

GPIO.cleanup()