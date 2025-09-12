from machine import Pin, PWM, Timer
from time import sleep

# SETUP
dimmer = PWM(Pin(15))
dimmer.freq(1000)
# LOOP
while True:
   # Fade in over 2 seconds
 for duty in range(65536):
   dimmer.duty_u16(duty)
   sleep(2 / 65536)
   # Fade out over 1 second
 for duty in range(65535, 0, -1):
   dimmer.duty_u16(duty)
   sleep(1 / 65536)
