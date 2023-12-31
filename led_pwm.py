# PWM驅動LED
from machine                import Pin,PWM
import time
pwm = PWM(Pin(17))
pwm.freq(1000)


def led():
    duty = 0
    direction = 1
    for _ in range(16*255):
        duty += direction
     
        if duty > 255:
            duty = 255
            direction = -1
        elif duty < 0:
            duty = 0
            direction = 1
     
        pwm.duty_u16(duty*duty)
        time.sleep(0.002)

while 1:
    led()
