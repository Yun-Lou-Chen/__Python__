# ######################3
# D1-Mini
# ESP8266
# https://honeststore.com.tw/esp8266-pin-out/
# 開機可用  * 
# Tx  1  
# Rx  3
# A0 17 
# D1  5 *
# D2  4 *
# D3  0
# D4  2
# D5 14 *
# D6 12 *
# D7 13 *
# D8 15
##################

import machine 
import random
import time
import tm1637

# display = tm1637.TM1637(clk=Pin(13),dio=Pin(12))
display = tm1637.TM1637(clk=machine.Pin(13), dio=machine.Pin(12))

display.scroll("192-168-071-123", delay=200)
time.sleep(1)
display.show('    ')
time.sleep(1)
temp = 23     # random.int(10,15)
i = 2
for _ in range(8):
    display.brightness(_)
    temp = 23 # random.int(10,25)
    display.temperature(temp)
    time.sleep(i)
    display.show('    ')
    time.sleep(i)
    display.number(1234)  # 显示数字，范围0-9999
    time.sleep(i)
    display.hex(1015)  #十六进制A
    time.sleep(i)
    display.numbers(_,56,1) # 时间显示，传递2个数值，最后一位1是点亮0是灭
    time.sleep(i)
    display.show(" %.2d"%18) #显示06
    time.sleep(i)
    display.scroll("192 168 071 123",delay=200)  #向左滚动显示
#     time.sleep(i)
#     display.show("{}   ".format(8))
#  
 
#  
# def main():
#     smg.show("    ") # 四个空格，清屏
#     smg.hex(10)  #十六进制A
#     smg.number(1234)  # 显示数字，范围0-9999
#     smg.numbers(11,56,1) # 时间显示，传递2个数值，最后一位1是点亮0是灭
#     smg.temperature(22) #温度显示
#     smg.show("2  9") # 输入空格则不显示，可用于清屏
#     #smg.show("{}   ".format(8))
#     #smg.show(" %.2d"%6) #显示06
#     smg.scroll("0123 4567  89")  #向左滚动显示
#  
# if __name__=="__main__":
#     main()