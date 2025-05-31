from machine import Pin
import time

led = Pin(25, Pin.OUT)  # Onboard LED on GPIO 25

while True:
    led.toggle()
    time.sleep(0.5)  # Delay for 0.5 seconds
