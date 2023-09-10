from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
import time

keypico = PMK(Hardware())
keys = keypico.keys

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], 
                          out_channel=0)

# Colour selection
snow = (0, 0, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
purple = (255, 0, 255)

# Set key colours for all keys
keypico.set_all(*snow)

# Orientation
# keypico.set_led(0, *red)
# keypico.set_led(3, *green)
# keypico.set_led(12, *blue)
# keypico.set_led(15, *purple)

# Set sleep time
keypico.led_sleep_enabled = True
keypico.led_sleep_time = 10

# Midi

start_note = 68
velocity = 127

# Loop

for key in keys:
    @keypico.on_press(key)
    def press_handler(key):
        key.set_led(*green)
        note = start_note + key.number
        midi.send(NoteOn(note, velocity))

    @keypico.on_release(key)
    def release_handler(key):
        if key.rgb == [255, 0, 0]:
            key.set_led(*green)
        else:
            key.set_led(*green)
        note = start_note + key.number
        midi.send(NoteOff(note, 0))

    @keypico.on_hold(key)
    def hold_handler(key):
        key.set_led(*purple)


time.sleep(10)
keypico.set_led(0, *red)
print("Morning Medication Reminder")
keypico.update()
time.sleep(10)
keypico.set_led(1, *red)
print("Afternoon Medication Reminder")
keypico.update()
time.sleep(10)
keypico.set_led(2, *red)
print("Evening Medication Reminder")
keypico.update()

while True:
  
    keypico.update()
