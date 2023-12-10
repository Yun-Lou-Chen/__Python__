import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# wlan.connect('Home_CCS&Lou', 'f28203416f')
wlan.connect('YunLou', 'f28203416f')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print(wlan.ifconfig())