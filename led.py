from machine import Pin
import time
p0 = Pin(16, Pin.OUT)    # create output pin on GPIO0
p0.on()                 # set pin to "on" (high) level
p0.off()                # set pin to "off" (low) level
p0.value(1)             # set pin to on/high

p2 = Pin(17, Pin.OUT)     # create input pin on GPIO2
print(p2.value())       # get value, 0 or 1


for i in range(0,20):
    p2.on()
    p0.off()
    time.sleep(1)
    p2.off()
    p0.on()
    time.sleep(1)
