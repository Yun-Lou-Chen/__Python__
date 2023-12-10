# UART
from machine                import UART,Pin,Timer
from time                   import sleep_us
 
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
led = Pin(25, Pin.OUT)
 
tim = Timer()
 
print("Send UART.")
 
def tick(timer):
    global uart, led
 
    led.toggle()
    uart.write(b'\x55')
 
tim.init(freq=10, mode=Timer.PERIODIC, callback=tick)
