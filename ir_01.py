import utime
import sys 
sys.path.append('pico_ir')
from machine import Pin
from pico_ir import read_code, send_code, validate_code, InvalidCodeException
 
pin_in = Pin(28, Pin.IN, Pin.PULL_UP)
pin_out = Pin(21, mode=Pin.OUT)
 
while True:
    out = read_code(pin_in)
    # ignore random signals 
    if out:
        try:
            validate_code(out)
            print(out)
            utime.sleep_ms(100)
            send_code(pin_out, out)
        except InvalidCodeException:
            print("InvalidCodeException:" + out)