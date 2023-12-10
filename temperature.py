import machine
import utime
 
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
 
while True:
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
#     print("12345678901234567890")
    print(f'{temperature:8.2f} °C')
#     print(temperature)
    utime.sleep(2)