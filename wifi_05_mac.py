import network
import ubinascii
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
 
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()

print('    mac =',mac)
# Other things you can query
print('Channel =',wlan.config('channel'))
print('  ESSID =',wlan.config('essid'))
print('TxPower =',wlan.config('txpower'))