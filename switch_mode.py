from machine import Pin, PWM, Timer
from time import sleep

# SETUP
dimmer = PWM(Pin(15))
dimmer.freq(1000)

button = Pin(14, Pin.IN, Pin.PULL_DOWN)

# Mode: 1 = fade (1/4 Hz: 2s up + 2s down), 2 = constant on
mode = 1

print("Mode 1 (fade). Press & release button on Pin 14 to toggle.")

def on_button_release(pin):
    # Toggle mode on RELEASE (falling edge: 1 -> 0 with PULL_DOWN)
    global mode
    mode = 2 if mode == 1 else 1
    print("Button released → Mode", mode)

# Trigger exactly on release
button.irq(trigger=Pin.IRQ_FALLING, handler=on_button_release)
# LOOP
while True:
    if mode == 1:
        # Fade in over 2 seconds
        for duty in range(65536):
            if mode != 1:
                break  # switch instantly if released
            dimmer.duty_u16(duty)
            sleep(2 / 65536)

        if mode != 1:
            continue

        # Fade out over 2 seconds
        for duty in range(65535, -1, -1):
            if mode != 1:
                break
            dimmer.duty_u16(duty)
            sleep(2 / 65536)

    else:
        # Mode 2: constant on
        dimmer.duty_u16(65535)
        # stay here until button release toggles back
        while mode == 2:
            sleep(0.01)
