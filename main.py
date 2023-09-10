from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
import time

keypico = PMK(Hardware())
keys = keypico.keys

# Medication schedule (time in seconds)
medication_schedule = {
    0: {"name": "Morning", "time": 10},  # Medication reminder every 10 seconds
    1: {"name": "Lunch", "time": 20},    # Medication reminder every 20 seconds
    2: {"name": "Dinner", "time": 30},   # Medication reminder every 30 seconds
}

# LED colors
led_off = (0, 0, 0)
led_red = (255, 0, 0)
led_green = (0, 255, 0)

# Initialize LED states for all keys
for key in keys:
    key.set_led(*led_off)

# Event handlers for key presses, releases, and holds
for key in keys:
    @keypico.on_press(key)
    def press_handler(key):
        print("Key {} pressed".format(key.number))
        key.set_led(*led_green)  # Turn the key green when pressed

    @keypico.on_release(key)
    def release_handler(key):
        print("Key {} released".format(key.number))
        if key.rgb == [255, 0, 0]:
            key.set_led(*led_red)
        else:
            key.set_led(*led_off)

    @keypico.on_hold(key)
    def hold_handler(key):
        print("Key {} held".format(key.number))
        key.set_led(*led_green)  # Continue showing green while the key is held

# Medication reminder loop
while True:
    keypico.update()
    current_time = int(time.time())  # Convert current time to integer

    for key_number, schedule_data in medication_schedule.items():
        if current_time >= schedule_data["time"]:
            # It's time to take medication
            key = keys[key_number]
            key.set_led(*led_red)  # Turn the key red to indicate medication time
            time.sleep(5)  # Keep it red for 5 seconds
            key.set_led(*led_off)  # Turn the key back to no color

    # Delay to check the medication schedule periodically (every 1 second)
    time.sleep(1)
